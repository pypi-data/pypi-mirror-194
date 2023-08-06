"""
图片预处理，原始数据为光学扫描数据，不同批次的拍照条件迥异，造成数据的批次差别
此程序对原始图片进行：曝光度平衡
"""
import numpy as np


def WB(fig):
    """
    根据红色通道调节白平衡
    :param fig: 3通道BGR图片文件，数据类型为 np.array
    :return: 返回RGB图片文件，数据类型为 np.arrayv
    """
    R, G, B = fig[:, :, 2], fig[:, :, 1], fig[:, :, 0]
    mask = (R > 180) * (R < 300)
    if np.sum(mask) < 9:
        return np.concatenate([B[:, :, np.newaxis], G[:, :, np.newaxis], R[:, :, np.newaxis]], axis=2)
    ravg = (np.sum(R * mask) + 9) / (np.sum(mask) + 9)
    gavg = (np.sum(G * mask) + 9) / (np.sum(mask) + 9)
    bavg = (np.sum(B * mask) + 9) / (np.sum(mask) + 9)
    R = np.floor(R / ravg * 200).astype(np.uint8)
    G = np.floor(G / gavg * 160).astype(np.uint8)
    B = np.floor(B / bavg * 120).astype(np.uint8)
    R = R - (R > 255) * (R - 255)
    R = R - (G > 167) * (R - 196)
    G = G - (G > 167) * (G - 167)
    R = R - (B > 100) * (R - 196)
    B = B - (B > 100) * (B - 100)
    return np.concatenate([B[:, :, np.newaxis], G[:, :, np.newaxis], R[:, :, np.newaxis]], axis=2)


def Ref_Drl_Cat(ref, *args, **kwargs):
    """
    合并线路与钻孔的二值图片文件
    :param ref: 线路二值图片文件，np.array
    :param args:
    :param kwargs: 'drl', 'dr2', 'drvia'
    :return:
    """
    scale = ref.shape[0]
    paras = {'drl': np.zeros((scale, scale), dtype=np.uint8),
             'dr2': np.zeros((scale, scale), dtype=np.uint8),
             'drvia': np.zeros((scale, scale), dtype=np.uint8)}
    keys = ['drl', 'dr2', 'drvia']
    for i in range(len(args)):
        try:
            paras[keys[i]] = args[i]
        except Exception as e:
            raise e
    for key, value in kwargs.items():
        try:
            paras[key] = value
        except Exception as e:
            raise e
    drl, dr2, drvia = paras['drl'], paras['dr2'], paras['drvia']
    return np.concatenate([(ref * (1 - drvia) * (1 - dr2) * (1 - drl) * 196 + drvia * (1 - dr2) * (1 - drl) * 191 + dr2 * (1 - drl) * 0 + drl * 0)[:, :, np.newaxis].astype(np.uint8),
                           (ref * (1 - drvia) * (1 - dr2) * (1 - drl) * 167 + drvia * (1 - dr2) * (1 - drl) * 40 + dr2 * (1 - drl) * 162 + drl * 162)[:, :, np.newaxis].astype(np.uint8),
                           (ref * (1 - drvia) * (1 - dr2) * (1 - drl) * 0 + drvia * (1 - dr2) * (1 - drl) * 55 + dr2 * (1 - drl) * 232 + drl * 232)[:, :, np.newaxis].astype(np.uint8)],
                          axis=2)


if __name__ == '__main__':
    pass
