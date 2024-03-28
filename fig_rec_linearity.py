'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 14:02:24
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 14:02:29
FilePath: /handwritingEval/fig_rec_linearity.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import numpy as np
from scipy.spatial import ConvexHull
from numpy import linalg as LA

def fig_rec_linearity(img):
    x, y = np.where(img == 0)
    Xmax = np.max(x)
    Xmin = np.min(x)
    Ymax = np.max(y)
    Ymin = np.min(y)
    sum_rect = 2 * (Xmax - Xmin) + 2 * (Ymax - Ymin)
    
    Kcon = ConvexHull(x, y)
    numPts = len(Kcon.vertices)
    sum_per = 0
    
    for i in range(numPts - 1):
        vert0 = (x[Kcon.vertices[i]], y[Kcon.vertices[i]])
        vert1 = (x[Kcon.vertices[i + 1]], y[Kcon.vertices[i + 1]])
        vert_sub = vert0 - vert1
        sum_per += LA.norm(vert_sub)
    
    c = sum_per / sum_rect
    return c

# 示例使用
# 假设 img 是一个二维 NumPy 数组，代表你的图像
# linearity = fig_rec_linearity(img)
# print(linearity)