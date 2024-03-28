'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 13:47:23
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 18:09:08
FilePath: /handwritingEval/fig_convexity.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np
from scipy.spatial import ConvexHull
from skimage import draw

def fig_convexity(img):
    h, w = img.shape
    x, y = np.where(img == 0)
    Kcon = ConvexHull(list(zip(x, y)))
    numPts = len(Kcon.vertices)
    conv_img = np.tile(img[:, :, np.newaxis], (1, 1, 3))
    sum_pixels = 0

    # 绘制凸包边并更新conv_img
    for i in range(numPts - 1):
        vert0 = (x[Kcon.vertices[i]], y[Kcon.vertices[i]])
        vert1 = (x[Kcon.vertices[i + 1]], y[Kcon.vertices[i + 1]])
        vertLine_temp = draw.line(vert0[1], vert0[0], vert1[1], vert1[0])
        for l in range(len(vertLine_temp[0])):
            conv_img[vertLine_temp[0, l], vertLine_temp[1, l], 0] = 0
            conv_img[vertLine_temp[0, l], vertLine_temp[1, l], 1] = 0
            conv_img[vertLine_temp[0, l], vertLine_temp[1, l], 2] = 0

    # 计算凸包内非零像素的总数
    for i in range(h):
        temp_sum = 0
        I = np.where(conv_img[i, :, 0] == 0)
        minI = np.min(I[0])
        maxI = np.max(I[0])
        for j in range(minI, maxI + 1):
            if conv_img[i, j, 0] != 0:
                temp_sum += 1
        sum_pixels += temp_sum

    ratio = len(x) / sum_pixels
    return ratio

# 示例使用
# 假设 img 是一个二维 NumPy 数组，代表你的图像
# ratio = fig_convexity(img)
# print(ratio)
from PIL import Image
import numpy as np

# 读取图像文件到 NumPy 数组
image_path = 'data/GB104/001.jpg'  # 替换为你的图像文件路径
image = Image.open(image_path)

# 将 PIL 图像转换为 NumPy 数组
image_array = np.array(image)
features = fig_convexity(image_array)
print(features)