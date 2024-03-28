'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 13:53:50
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 13:53:53
FilePath: /handwritingEval/matlab/fig_gravity_conv.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np
from scipy.spatial import ConvexHull
from skimage import draw

def fig_gravity_conv(img):
    h, w = img.shape
    x, y = np.where(img == 0)

    Xmax = np.max(x)
    Xmin = np.min(x)
    Ymax = np.max(y)
    Ymin = np.min(y)
    sum_rect = 2 * (Xmax - Xmin) + 2 * (Ymax - Ymin)
    
    Kcon = ConvexHull(x, y)
    numPts = len(Kcon.vertices)
    conv_img = np.ones((h, w), dtype=img.dtype)
    
    # 绘制凸包边并更新conv_img
    for i in range(numPts - 1):
        vert0 = (x[Kcon.vertices[i]], y[Kcon.vertices[i]])
        vert1 = (x[Kcon.vertices[i + 1]], y[Kcon.vertices[i + 1]])
        vertLine_temp = draw.line(vert0[1], vert0[0], vert1[1], vert1[0])
        for l in range(len(vertLine_temp[0])):
            conv_img[vertLine_temp[1, l], vertLine_temp[0, l]] = 0

    # 计算凸包的重心
    sum_pixels_x = 0
    sum_pixels_y = 0
    sum_pt = 0
    for i in range(h):
        I = np.where(conv_img[i, :] == 0)
        if I[0].size == 0:
            continue
        minI = np.min(I[0])
        maxI = np.max(I[0])
        sum_pt += maxI - minI + 1
        sum_pixels_x += (minI + maxI) * (maxI - minI + 1) / 2.0
        sum_pixels_y += i * (maxI - minI + 1)
    
    gravity_x = int(sum_pixels_x / sum_pt)
    gravity_y = int(sum_pixels_y / sum_pt)
    
    sum = np.zeros((2, 2))
    for j in range(h):
        I = np.where(conv_img[j, :] == 0)
        if I[0].size == 0:
            continue
        minI = np.min(I[0])
        maxI = np.max(I[0])
        if j <= gravity_y:
            for a in range(minI, gravity_x):
                if img[j, a] == 0:
                    sum[0, 0] += gravity_x - minI
            for b in range(gravity_x, maxI):
                if img[j, b] == 0:
                    sum[0, 1] += maxI - gravity_x
        else:
            for a in range(minI, gravity_x):
                if img[j, a] == 0:
                    sum[1, 0] += gravity_x - minI
            for b in range(gravity_x, maxI):
                if img[j, b] == 0:
                    sum[1, 1] += maxI - gravity_x
    
    sum_pixel = sum[0, 0] + sum[0, 1] + sum[1, 0] + sum[1, 1]
    pixel_r = [sum[0, 0] / sum_pixel, sum[0, 1] / sum_pixel, sum[1, 0] / sum_pixel, sum[1, 1] / sum_pixel]
    
    return pixel_r

# 示例使用
# 假设 img 是一个二维 NumPy 数组，代表你的图像
# pixel_distribution = fig_gravity_conv(img)
# print(pixel_distribution)