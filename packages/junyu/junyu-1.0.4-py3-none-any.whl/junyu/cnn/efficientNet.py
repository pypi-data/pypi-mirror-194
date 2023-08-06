import re
import torch
import torch.nn as nn
import torch.nn.functional as F
from junyu import utils


class MBConvBlock(nn.Module):
    def __init__(self, block_args, global_params, image_size=None):
        """

        :param block_args: 区块特定参数
        :param global_params: 全局参数
        :param image_size: 图片分辨率
        """
        super().__init__()
        self._block_args = block_args
        self._bn_mom = 1 - global_params.batch_norm_momentum
        self._bn_eps = global_params.batch_norm_epsilon
        self.has_se = (self._block_args.se_ratio is not None) and (0 < self._block_args.se_ratio <= 1)
        self.id_skip = block_args.id_skip

        # 扩展宽度，倒置瓶颈
        inp = self._block_args.input_filters  # 输入通道数
        oup = self._block_args.input_filters * self._block_args.expand_ratio  # 输出通道数

        if self._block_args.expand_ratio != 1:
            Conv2d = utils.get_same_padding_conv2d(image_size=image_size)
            self._expand_conv = Conv2d(in_channels=inp, out_channels=oup, kernel_size=1, bias=False)
            self._bn0 = nn.BatchNorm2d(num_features=oup, momentum=self._bn_mom, eps=self._bn_eps)
            # image_size = utils.calculate_output_image_size(image_size, 1)

        # 扩展深度
        k = self._block_args.kernel_size
        s = self._block_args.stride
        Conv2d = utils.get_same_padding_conv2d(image_size=image_size)
        self._depthwise_conv = Conv2d(in_channels=oup, out_channels=oup, groups=oup, kernel_size=k, stride=s, bias=False)
        self._bn1 = nn.BatchNorm2d(num_features=oup, momentum=self._bn_mom, eps=self._bn_eps)
        image_size = utils.calculate_output_image_size(image_size, s)  # 刷新图片分辨率

        # 压缩和激励层
        if self.has_se:
            Conv2d = utils.get_same_padding_conv2d(image_size=(1, 1))
            num_squeezed_channels = max(1, int(self._block_args.input_filters * self._block_args.se_ratio))
            self._se_reduce = Conv2d(in_channels=oup, out_channels=num_squeezed_channels, kernel_size=1)
            self._se_expand = Conv2d(in_channels=num_squeezed_channels, out_channels=oup, kernel_size=1)

        # 二维全连接层
        final_oup = self._block_args.output_filters
        Conv2d = utils.get_same_padding_conv2d(image_size=image_size)
        self._project_conv = Conv2d(in_channels=oup, out_channels=final_oup, kernel_size=1, bias=False)
        self._bn2 = nn.BatchNorm2d(num_features=final_oup, momentum=self._bn_mom, eps=self._bn_eps)
        self._swish = utils.MemoryEfficientSwish()

    def forward(self, inputs, drop_connect_rate=None):
        """

        :param inputs: 输入矩阵，N x C x H x W
        :param drop_connect_rate: 0~1
        :return:
        """
        x = inputs
        # 扩展宽度
        if self._block_args.expand_ratio != 1:
            x = self._expand_conv(inputs)
            x = self._bn0(x)
            x = self._swish(x)

        # 扩展深度
        x = self._depthwise_conv(x)
        x = self._bn1(x)
        x = self._swish(x)

        # 压缩和激励
        if self.has_se:
            x_squeezed = F.adaptive_avg_pool2d(x, 1)
            x_squeezed = self._se_reduce(x_squeezed)
            x_squeezed = self._swish(x_squeezed)
            x_squeezed = self._se_expand(x_squeezed)
            x = torch.sigmoid(x_squeezed) * x

        # 全连接
        x = self._project_conv(x)
        x = self._bn2(x)

        # Skip connection and drop connect
        input_filters, output_filters = self._block_args.input_filters, self._block_args.output_filters
        if self.id_skip and self._block_args.stride == 1 and input_filters == output_filters:
            # The combination of skip connection and drop connect brings about stochastic depth.
            if drop_connect_rate:
                x = utils.drop_connect(x, p=drop_connect_rate, training=self.training)
            x = x + inputs  # skip connection
        return x

    def set_swish(self, memory_effieient=True):
        self._swish = utils.MemoryEfficientSwish() if memory_effieient else utils.Swish()


class EffieientNet(nn.Module):
    def __init__(self, block_args=None, global_params=None):
        super().__init__()
        assert isinstance(block_args, list)
        assert len(block_args) > 0
        self._global_params = global_params
        self._block_args = block_args

        # BatchNorm参数
        bn_mom = 1 - self._global_params.batch_norm_momentum
        bn_eps = self._global_params.batch_norm_epsilon

        # 选择动态或静态卷积
        image_size = global_params.image_size
        Conv2d = utils.get_same_padding_conv2d(image_size=image_size)

        # Stem
        in_channels = 6
        self._change_in_channels(in_channels=in_channels)
        out_channels = utils.round_filters(32, self._global_params)
        self._conv_stem = Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=2, bias=False)
        self._bn0 = nn.BatchNorm2d(num_features=out_channels, momentum=bn_mom, eps=bn_eps)
        image_size = utils.calculate_output_image_size(image_size, 2)

        # Block
        self._blocks = nn.ModuleList([])
        for block_args in self._block_args:
            block_args = block_args._replace(
                input_filters=utils.round_filters(block_args.input_filters, self._global_params),
                output_filters=utils.round_filters(block_args.output_filters, self._global_params),
                num_repeat=utils.round_repeats(block_args.num_repeat, self._global_params)
            )

            self._blocks.append(MBConvBlock(block_args, self._global_params, image_size=image_size))
            image_size = utils.calculate_output_image_size(image_size, block_args.stride)
            if block_args.num_repeat > 1:  # modify block_args to keep same output size
                block_args = block_args._replace(input_filters=block_args.output_filters, stride=1)
            for _ in range(block_args.num_repeat - 1):
                self._blocks.append(MBConvBlock(block_args, self._global_params, image_size=image_size))

        # Head
        in_channels = block_args.output_filters  # output of final block
        out_channels = utils.round_filters(1280, self._global_params)
        Conv2d = utils.get_same_padding_conv2d(image_size=image_size)
        self._conv_head = Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self._bn1 = nn.BatchNorm2d(num_features=out_channels, momentum=bn_mom, eps=bn_eps)

        # Final linear layer
        self._avg_pooling = nn.AdaptiveAvgPool2d(1)
        self._dropout = nn.Dropout(self._global_params.dropout_rate)
        self._fc = nn.Linear(out_channels, self._global_params.num_classes)
        self._swish = utils.MemoryEfficientSwish()

    def extract_features(self, inputs):
        # Stem
        x = self._swish(self._bn0(self._conv_stem(inputs)))

        # Blocks
        for idx, block in enumerate(self._blocks):
            drop_connect_rate = self._global_params.drop_connect_rate
            if drop_connect_rate:
                drop_connect_rate *= float(idx) / len(self._blocks)  # scale drop connect_rate
            x = block(x, drop_connect_rate=drop_connect_rate)

        # Head
        x = self._swish(self._bn1(self._conv_head(x)))
        return x

    def forward(self, inputs):
        x = self.extract_features(inputs)
        # Pooling and final linear layer
        x = self._avg_pooling(x)
        if self._global_params.include_top:
            x = x.flatten(start_dim=1)
            x = self._dropout(x)
            x = self._fc(x)
        return x

    def _change_in_channels(self, in_channels):
        """
        调节输入channel如果不为3
        :param in_channels:
        :return:
        """
        if in_channels != 3:
            Conv2d = utils.get_same_padding_conv2d(image_size=self._global_params.image_size)
            out_channels = utils.round_filters(32, self._global_params)
            self._conv_stem = Conv2d(in_channels, out_channels, kernel_size=3, stride=2, bias=False)

    def set_swish(self, memory_efficient=True):
        self._swish = utils.MemoryEfficientSwish() if memory_efficient else utils.Swish()
        for block in self._blocks:
            block.set_swish(memory_efficient)


def efficientnet_params(model_name):
    """
    根据不同的EfficientNet版本定义参数值
    :param model_name:
    :return:
    """
    params_dict = {
        # Coefficients:   width,depth,res,dropout
        'efficientnet-b0': (1.0, 1.0, 224, 0.2),
        'efficientnet-b1': (1.0, 1.1, 240, 0.2),
        'efficientnet-b2': (1.1, 1.2, 260, 0.3),
        'efficientnet-b3': (1.2, 1.4, 300, 0.3),
        'efficientnet-b4': (1.4, 1.8, 380, 0.4),
        'efficientnet-b5': (1.6, 2.2, 456, 0.4),
        'efficientnet-b6': (1.8, 2.6, 528, 0.5),
        'efficientnet-b7': (2.0, 3.1, 600, 0.5),
        'efficientnet-b8': (2.2, 3.6, 672, 0.5),
        'efficientnet-l2': (4.3, 5.3, 800, 0.5),
    }
    return params_dict[model_name]


def efficientnet(width_coefficient=None, depth_coefficient=None, image_size=None, dropout_rate=0.2, drop_connect_rate=0.2, num_classes=1000, include_top=True):
    """
    构建block参数和全局参数
    :param width_coefficient:
    :param depth_coefficient:
    :param image_size:
    :param dropout_rate:
    :param drop_connect_rate:
    :param num_classes:
    :param include_top:
    :return:
    """
    # Blocks args for the whole model(efficientnet-b0 by default)
    # It will be modified in the construction of EfficientNet Class according to model
    blocks_args = [
        'r1_k3_s11_e1_i32_o16_se0.25',
        'r2_k3_s22_e6_i16_o24_se0.25',
        'r2_k5_s22_e6_i24_o40_se0.25',
        'r3_k3_s22_e6_i40_o80_se0.25',
        'r3_k5_s11_e6_i80_o112_se0.25',
        'r4_k5_s22_e6_i112_o192_se0.25',
        'r1_k3_s11_e6_i192_o320_se0.25',
    ]
    blocks_args = [decode(i) for i in blocks_args]

    global_params = utils.GlobalParams(
        width_coefficient=width_coefficient,
        depth_coefficient=depth_coefficient,
        image_size=image_size,
        dropout_rate=dropout_rate,
        num_classes=num_classes,
        batch_norm_momentum=0.99,
        batch_norm_epsilon=1e-3,
        drop_connect_rate=drop_connect_rate,
        depth_divisor=8,
        min_depth=None,
        include_top=include_top,
    )

    return blocks_args, global_params


def decode(block_string):
    """
    将string的block_args翻译成utils.BlockArgs格式
    :param block_string:
    :return:
    """
    ops = block_string.split('_')
    options = {}
    for op in ops:
        splits = re.split(r'(\d.*)', op)
        if len(splits) >= 2:
            key, value = splits[:2]
            options[key] = value
    # 检查stride
    assert (('s' in options and len(options['s']) == 1) or
            (len(options['s']) == 2 and options['s'][0] == options['s'][1]))

    return utils.BlockArgs(
        num_repeat=int(options['r']),
        kernel_size=int(options['k']),
        stride=[int(options['s'][0])],
        expand_ratio=int(options['e']),
        input_filters=int(options['i']),
        output_filters=int(options['o']),
        se_ratio=float(options['se']) if 'se' in options else None,
        id_skip=('noskip' not in block_string))


def get_model_params(model_name, override_params):
    if model_name.startswith('efficientnet'):
        w, d, s, p = efficientnet_params(model_name)
        # note: all models have drop connect rate = 0.2
        blocks_args, global_params = efficientnet(width_coefficient=w, depth_coefficient=d, dropout_rate=p, image_size=s)
    else:
        raise NotImplementedError('model name is not pre-defined: {}'.format(model_name))
    if override_params:
        # ValueError will be raised here if override_params has fields not included in global_params.
        global_params = global_params._replace(**override_params)
    return blocks_args, global_params


if __name__ == '__main__':
    blocks_args, global_params = get_model_params(model_name='efficientnet-b5', override_params={})

    model = EffieientNet(block_args=blocks_args, global_params=global_params)

    x = torch.rand(4, 6, 108, 108)
    out = model(x)

    print(out.shape)