'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 13:20:13
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 13:20:17
FilePath: /handwritingEval/matlab/drawline_dda2d.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE

这段 MATLAB 代码实现了 Bresenham 直线算法（Digital Differential Analyzer，DDA）的二维版本，
用于在离散像素网格上绘制一条直线。本质是像素填充算法.
该算法接受两个点 vert1 和 vert2 作为输入，并输出一个矩阵 P，其中包含了从 vert1 到 vert2 的直线路径上的点的坐标。
'''
import numpy as np

def draw_line_DDA2d(vert1, vert2, color='black'):
    x1, y1 = vert1
    x2, y2 = vert2

    length = abs(x2 - x1)
    if abs(y2 - y1) > length:
        length = abs(y2 - y1)

    P = np.zeros((2, length))
    
    dx = (x2 - x1) / length
    dy = (y2 - y1) / length

    x = x1 + 0.5 * np.sign(dx)
    y = y1 + 0.5 * np.sign(dy)
    
    for i_sub1 in range(length):
        P[0, i_sub1] = int(round(x))
        P[1, i_sub1] = int(round(y))
        # plot3(round(x), round(y), round(z), color=color)  # 如果需要绘图，取消注释并提供 z 值
        x += dx
        y += dy

    return P

# 示例使用
vert1 = (1, 2)
vert2 = (5, 6)
line_points = draw_line_DDA2d(vert1, vert2)
print(line_points)