'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 13:56:26
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 13:57:04
FilePath: /handwritingEval/fig_projection.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np
import cv2

def fig_projection(img):
    h, w = img.shape
    x, y = np.where(img == 0)
    projection = [np.std(y) / w, np.std(x) / h]
    
    img_black = np.ones((h, w), dtype=img.dtype) - img
    img_ro_black = cv2.rotate(img_black, cv2.ROTATE_90_CLOCKWISE)
    img_ro = ~img_ro_black
    
    min_x = np.min(x)
    max_x = np.max(x)
    min_y = np.min(y)
    max_y = np.max(y)
    img_ro = img_ro[min_x:max_x, min_y:max_y]
    x, y = np.where(img_ro == 0)
    
    projection.extend([np.std(y) / w, np.std(x) / h])
    return projection

# 示例使用
# 假设 img 是一个二维 NumPy 数组，代表你的图像
# proj_values = fig_projection(img)
# print(proj_values)