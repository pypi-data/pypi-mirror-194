"""
构建mvi类，用于mvi文件读取，输入为mvi文件路径
"""

import numpy as np
import mudeConstant as mc

WIDTH = mc.WIDTH
HEIGHT = mc.HEIGHT
RESOLUTION = mc.RESOLUTION

DIGIT = mc.DIGIT
digit = mc.digit


class mvi:
    def __init__(self, path):
        """

        :param path: .mvi文件路径
        """
        f = np.fromfile(path, dtype='B', count=32)
        self.width = (((((f[0xf] * 0x100) + f[0xe]) * 0x100) + f[0xd]) * 0x100) + f[0xc]
        self.height = (((((f[0x13] * 0x100) + f[0x12]) * 0x100) + f[0x11]) * 0x100) + f[0x10]

        self.f = np.fromfile(path, dtype='int16', count=-1, offset=32).astype(np.int32)
        sum, self.index = 0, [0]
        for i in range(len(self.f)):
            if sum >= self.width:
                self.index.append(i)
                sum = abs(self.f[i])
            else:
                sum += abs(self.f[i])

    def mvi_line(self, n, x_min, x_max):
        i, t = self.index[n], self.f[self.index[n]]

        while t <= x_min:
            i += 1
            t += abs(self.f[i])
        result = str(int(self.f[i] < 0)) * (min(x_max, t) - x_min)
        if len(result) == x_max - x_min:
            return np.array(list(result)).astype(np.uint8).tolist()
        i += 1
        t += abs(self.f[i])
        while t < x_max:
            result += str(int(self.f[i] < 0)) * abs(self.f[i])
            i += 1
            t += abs(self.f[i])
        result += str(int(self.f[i] < 0)) * abs(x_max - t + abs(self.f[i]))
        return np.array(list(result)).astype(np.uint8).tolist()

    def mvi_show_bin(self, x, y, scale):
        x_min = x - int(scale / 2)
        x_max = x + int(scale / 2)
        y_min = y - int(scale / 2)
        y_max = y + int(scale / 2)

        if x_min < 0: x_min = 0
        if y_min < 0: y_min = 0
        if x_max > self.width: x_max = self.width
        if y_max > self.height: y_min = self.height

        t = []
        for i in range(y_min, y_max):
            t.append(self.mvi_line(i, x_min, x_max))
        t = np.array(t).astype(np.uint8)

        if t.shape == (scale, scale):
            return t
        else:
            result = np.zeros((scale, scale), dtype=np.uint8)
            result[max(0, x - int(scale / 2)):min(self.width, x + int(scale / 2)), max(0, y - int(scale / 2)):min(self.height, y + int(scale / 2))] = t
            return result

