'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 13:54:30
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 13:55:48
FilePath: /handwritingEval/fig_gravity_pos.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np

def fig_gravity_pos(img):
    h, w = img.shape
    x, y = np.where(img == 0)
    x_gra = np.mean(x)
    y_gra = np.mean(y)
    x_rec = h / 2
    y_rec = w / 2
    gravity_pos = [x_gra / h, y_gra / w]
    return gravity_pos

# 示例使用
# 假设 img 是一个二维 NumPy 数组，代表你的图像
# pos = fig_gravity_pos(img)
# print(pos)