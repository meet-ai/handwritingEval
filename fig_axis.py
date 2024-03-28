'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 13:41:25
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 18:51:30
FilePath: /handwritingEval/fig_axis.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np
from scipy.spatial import ConvexHull
from numpy import polyfit
from drawline_dda2d import draw_line_DDA2d

def fig_axis(img):
    h, w = img.shape
    x, y = np.where(img == 0)
    print(x,y)
    Kcon = ConvexHull(list(zip(x, y)))
    numPts = len(Kcon.vertices)
    conv_img = np.tile(img[:, :, np.newaxis], (1, 1, 3))

    for i in range(numPts - 1):
        vert0 = (x[Kcon.vertices[i]], y[Kcon.vertices[i]])
        vert1 = (x[Kcon.vertices[i + 1]], y[Kcon.vertices[i + 1]])
        vertLine_temp = draw_line_DDA2d(vert0, vert1)
        numVexLine_temp = vertLine_temp.shape[1]
        for l in range(numVexLine_temp):
            print(vertLine_temp[0,l])
            print(vertLine_temp[1,l])
            conv_img[80,8,1] = 0
            conv_img[int(vertLine_temp[0, l]), int(vertLine_temp[1, l]), 1] = 0
            conv_img[int(vertLine_temp[0, l]), int(vertLine_temp[1, l]), 2] = 0

    p, _ = polyfit(x, y, 1)
    print(p,"p")
    leep = p[0]
    point = p[1] / w

    sum_pixels_left = 0
    sum_pixels_right = 0
    for i in range(h):
        temp_sum_left = 0
        temp_sum_right = 0
        I = np.where(conv_img[i, :, 0] == 0)
        minI = np.min(I[0])
        maxI = np.max(I[0])
        y1 = int(np.round(leep * i + point))
        if y1 <= 0:
            y1 = 1
        for j in range(minI, y1):
            if conv_img[i, j, 0] != 0:
                temp_sum_left += 1
        for j in range(y1, maxI):
            if conv_img[i, j, 0] != 0:
                temp_sum_right += 1
        sum_pixels_left += temp_sum_left
        sum_pixels_right += temp_sum_right

    left_ratio = sum_pixels_left / (sum_pixels_left + sum_pixels_right)
    kd = np.array([leep, point, left_ratio])
    return kd

# 示例使用
# 假设 img 是一个二维 NumPy 数组，代表你的图像
# img = ...
from PIL import Image
import numpy as np

# 读取图像文件到 NumPy 数组
image_path = 'data/GB104/001.jpg'  # 替换为你的图像文件路径
image = Image.open(image_path)

# 将 PIL 图像转换为 NumPy 数组
image_array = np.array(image)

print(image_array.shape)  # 打印图像的尺寸
features = fig_axis(image_array)
print(features)