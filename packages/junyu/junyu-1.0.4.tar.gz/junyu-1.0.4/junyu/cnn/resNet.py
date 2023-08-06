"""
CNN模型，主要采用Inception-ResNet结构
源图像为108*108*3 RGB图像，输出1024*3*3，池化层降低分辨率到1024*1*1，再通过MLP全连接到指定分类数目
"""

import torch
import torch.nn as nn

BATCH_SIZE = 1024


class Stem(nn.Module):
    def __init__(self, in_channel=6):
        """
        图像预处理，缩小分辨率为 1/4，扩展通道
        in_channel = 3
        out_channel = 384
        """
        super(Stem, self).__init__()

        self.pre = nn.Conv2d(in_channels=in_channel, out_channels=16, kernel_size=1, padding=0, stride=1, bias=False)

        self.step_1_1 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1, stride=1, bias=False)
        self.step_1_2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1, stride=1, bias=False)

        self.step_2_chain_1 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=4, padding=1, stride=2, bias=False)
        self.step_2_chain_2 = nn.MaxPool2d(kernel_size=4, padding=1, stride=2)

        self.step_3_chain_1 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=64, kernel_size=1, padding=0, stride=1, bias=False),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1, bias=False)
        )
        self.step_3_chain_2 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=64, kernel_size=1, padding=0, stride=1, bias=False),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(7, 1), padding=(3, 0), stride=1, bias=False),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(1, 7), padding=(0, 3), stride=1, bias=False),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1, stride=1, bias=False)
        )

        self.step_4_chain_1 = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=4, padding=1, stride=2, bias=False)
        self.step_4_chain_2 = nn.MaxPool2d(kernel_size=4, padding=1, stride=2)

    def forward(self, x):
        """
        :param x: 输入图像，fig, ref, dri合并而成，3*216*216
        :return:
        """
        out = self.pre(x)

        out = self.step_1_1(out)
        out = self.step_1_2(out)  # 64*108*108

        out_1 = self.step_2_chain_1(out)
        out_2 = self.step_2_chain_2(out)
        out = torch.cat([out_1, out_2], dim=1)  # 192*54*54

        out_1 = self.step_3_chain_1(out)
        out_2 = self.step_3_chain_2(out)
        out = torch.cat([out_1, out_2], dim=1)  # 128*54*54

        out_1 = self.step_4_chain_1(out)
        out_2 = self.step_4_chain_2(out)
        out = torch.cat([out_1, out_2], dim=1)  # 256*27*27
        return out


class Inception_Resnet_A(nn.Module):
    def __init__(self, in_channel=256):
        """
        Inception模块 输入in_channel, 中间展开, 输出in_channel, 保持channel不变
        :param in_channel:
        """
        super(Inception_Resnet_A, self).__init__()
        self.chain_1 = nn.Conv2d(in_channels=in_channel, out_channels=32, kernel_size=1, stride=1, padding=0,
                                 bias=False)

        self.chain_2 = nn.Sequential(
            nn.Conv2d(in_channels=in_channel, out_channels=32, kernel_size=1, stride=1, padding=0, bias=False),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1, bias=False)
        )

        self.chain_3 = nn.Sequential(
            nn.Conv2d(in_channels=in_channel, out_channels=32, kernel_size=1, stride=1, padding=0, bias=False),
            nn.Conv2d(in_channels=32, out_channels=48, kernel_size=3, stride=1, padding=1, bias=False),
            nn.Conv2d(in_channels=48, out_channels=64, kernel_size=3, stride=1, padding=1, bias=False),
        )

        self.fc = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=1, stride=1, padding=0, bias=False)

    def forward(self, x):
        out = torch.cat([self.chain_1(x), self.chain_2(x), self.chain_3(x)], dim=1)
        return x + self.fc(out)


class Reduction_A(nn.Module):
    def __init__(self, in_channel=256, s=2):
        """
        Residual模块, 降低图像分辨率为 1/s, 只包含方形卷积核
        :param in_channel:
        :param s : 缩放倍数
        """
        super(Reduction_A, self).__init__()
        self.chain_1 = nn.Sequential(
            nn.Conv2d(in_channels=in_channel, out_channels=64, kernel_size=1, stride=1, padding=0, bias=False),
            nn.Conv2d(in_channels=64, out_channels=96, kernel_size=3, stride=1, padding=1, bias=False),
            nn.Conv2d(in_channels=96, out_channels=128, kernel_size=3, stride=s, padding=1, bias=False)
        )

        self.chain_2 = nn.Conv2d(in_channels=in_channel, out_channels=128, kernel_size=3, stride=s, padding=1,
                                 bias=False)

        self.chain_3 = nn.MaxPool2d(kernel_size=3, stride=s, padding=1)

    def forward(self, x):
        return torch.cat([self.chain_1(x), self.chain_2(x), self.chain_3(x)], dim=1)


class Inception_Resnet_B(nn.Module):
    def __init__(self, in_channel=512):
        """
        Inception模块 输入in_channel, 中间展开inter_channel, 输出in_channel, 保持channel不变
        :param in_channel: in channel 数目
        """
        super(Inception_Resnet_B, self).__init__()

        self.chain_1 = nn.Conv2d(in_channels=in_channel, out_channels=192, kernel_size=1, stride=1, padding=0,
                                 bias=False)

        self.chain_2 = nn.Sequential(
            nn.Conv2d(in_channels=in_channel, out_channels=128, kernel_size=1, stride=1, padding=0, bias=False),
            nn.Conv2d(in_channels=128, out_channels=160, kernel_size=(1, 7), stride=1, padding=(0, 3), bias=False),
            nn.Conv2d(in_channels=160, out_channels=192, kernel_size=(7, 1), stride=1, padding=(3, 0), bias=False),
        )

        self.fc = nn.Conv2d(in_channels=384, out_channels=512, kernel_size=1, stride=1, padding=0, bias=False)

    def forward(self, x):
        out = torch.cat([self.chain_1(x), self.chain_2(x)], dim=1)
        return x + self.fc(out)


class Reduction_B(nn.Module):
    def __init__(self, in_channel=512, s=2):
        super(Reduction_B, self).__init__()
        self.chain_1 = nn.MaxPool2d(kernel_size=4, stride=s, padding=1)

        self.chain_2 = nn.Sequential(
            nn.Conv2d(in_channels=in_channel, out_channels=128, kernel_size=1, stride=1, padding=0, bias=False),
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=4, stride=s, padding=1, bias=False)
        )

        self.chain_3 = nn.Sequential(
            nn.Conv2d(in_channels=in_channel, out_channels=128, kernel_size=1, stride=1, padding=0, bias=False),
            nn.Conv2d(in_channels=128, out_channels=192, kernel_size=3, stride=1, padding=1, bias=False),
            nn.Conv2d(in_channels=192, out_channels=256, kernel_size=4, stride=s, padding=1, bias=False)
        )

    def forward(self, x):
        out = torch.cat([self.chain_1(x), self.chain_2(x), self.chain_3(x)], dim=1)
        return out


class Inception_Resnet_C(nn.Module):
    def __init__(self, in_channel=1024):
        """
        Inception模块 输入in_channel, 中间展开inter_channel, 输出in_channel, 保持channel不变
        :param in_channel: in channel 数目
        """
        super(Inception_Resnet_C, self).__init__()

        self.chain_1 = nn.Conv2d(in_channels=in_channel, out_channels=256, kernel_size=1, stride=1, padding=0,
                                 bias=False)

        self.chain_2 = nn.Sequential(
            nn.Conv2d(in_channels=in_channel, out_channels=192, kernel_size=1, stride=1, padding=0, bias=False),
            nn.Conv2d(in_channels=192, out_channels=224, kernel_size=(1, 3), stride=1, padding=(0, 1), bias=False),
            nn.Conv2d(in_channels=224, out_channels=256, kernel_size=(3, 1), stride=1, padding=(1, 0), bias=False),
        )

        self.fc = nn.Conv2d(in_channels=512, out_channels=1024, kernel_size=1, stride=1, padding=0, bias=False)

    def forward(self, x):
        out = torch.cat([self.chain_1(x), self.chain_2(x)], dim=1)
        return x + self.fc(out)


class MLP_Head(nn.Module):
    def __init__(self, in_channel=1024, out_channel=2):
        super(MLP_Head, self).__init__()
        self.step = nn.Sequential(
            nn.Linear(in_features=in_channel, out_features=1024, bias=True),
            nn.Tanh(),
            nn.Linear(in_features=1024, out_features=256, bias=True),
            nn.Tanh(),
            nn.Linear(in_features=256, out_features=64, bias=True),
            nn.Tanh(),
            nn.Linear(in_features=64, out_features=out_channel, bias=False),
        )

    def forward(self, x):
        return self.step(x)


class ResNet_CNN(nn.Module):
    def __init__(self, layers=None, in_channel=3, out_channel=2):
        super(ResNet_CNN, self).__init__()

        if layers is None:
            layers = {'A': 3, 'B': 5, 'C': 3}

        self.stem = nn.Sequential(Stem(in_channel=in_channel), nn.ReLU())  # 256*27*27

        self.A = Inception_Resnet_A(in_channel=256)

        self.step_A = nn.Sequential(
            *[nn.Sequential(self.A, nn.BatchNorm2d(num_features=256), nn.ELU()) for _ in
              range(layers['A'])],
            Reduction_A(in_channel=256, s=2),  # 512*14*14
            nn.BatchNorm2d(num_features=512)
        )

        self.B = Inception_Resnet_B(in_channel=512)

        self.step_B = nn.Sequential(
            *[nn.Sequential(self.B, nn.BatchNorm2d(num_features=512), nn.ELU()) for _
              in range(layers['B'])],
            Reduction_B(in_channel=512, s=2),  # 1024*7*7
            nn.BatchNorm2d(num_features=1024)
        )

        self.C = Inception_Resnet_C(in_channel=1024)

        self.step_C = nn.Sequential(
            *[nn.Sequential(self.C, nn.BatchNorm2d(num_features=1024), nn.ELU()) for _
              in range(layers['C'])],
            nn.AvgPool2d(kernel_size=3, stride=2, padding=0)  # 1024*3*3
        )

        self.pooling = nn.MaxPool2d(kernel_size=3)

        self.MLP_head = MLP_Head(in_channel=1024, out_channel=out_channel)

        self.dropout = nn.Dropout(p=0.5)

    def forward(self, fig):
        """
        向前传播
        :param x: 输入图像，batch_size * 108 * 108 * 3|4
        :return: batch_size * feature_size (暂定256)
        """
        out = self.stem(fig)  # 256*27*27
        out = self.step_A(out)  # 512*14*14
        out = self.step_B(out)  # 1024*7*7
        out = self.step_C(out)  # 1024*3*3
        out = self.pooling(out).squeeze()  # 1024 channel
        out = self.dropout(out)
        out = self.MLP_head(out)
        return out


if __name__ == '__main__':
    print('The program is starting!')

    model = ResNet_CNN(layers={'A': 3, 'B': 5, 'C': 3}, in_channel=6, out_channel=88)
    x = torch.rand(16, 6, 108, 108)
    out = model(x)
    print(out.shape)

    print('The program is over!')
