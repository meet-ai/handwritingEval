'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 13:51:49
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 13:51:52
FilePath: /handwritingEval/fig_fillin.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np
import cv2

def fig_fillin(img):
    h, w = img.shape
    img = cv2.threshold(img, 0.5, 1, cv2.THRESH_BINARY)[1].astype(np.uint8) * -1 + 1

    min_fill = 1
    max_fill = 0
    max_direction = -1
    min_direction = -1

    for rotate_angle in range(0, 91):
        img_ro_black = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        
        img_ro = ~img_ro_black
        nPts = np.where(img_ro == 0)[0].size

        # Fill the image in rows
        img_h = np.zeros((h, w, 3), dtype=np.uint8)
        img_h[:, :, 0] = img_ro
        img_h[:, :, 1] = img_ro
        img_h[:, :, 2] = img_ro
        nPts_h = 0
        for i in range(h):
            for j in range(w):
                if img_ro[i, j] == 0:
                    img_h[i, j, 0] = 0
                    img_h[i, j, 1] = 236
                    img_h[i, j, 2] = 0
                    nPts_h += 1
        fill_h = nPts_h / (nPts_h + nPts)

        # Fill the image in columns
        img_s = np.zeros((h, w, 3), dtype=np.uint8)
        img_s[:, :, 0] = img_ro
        img_s[:, :, 1] = img_ro
        img_s[:, :, 2] = img_ro
        nPts_s = 0
        for i in range(w):
            for j in range(h):
                if img_ro[j, i] == 0:
                    img_s[j, i, 0] = 0
                    img_s[j, i, 1] = 236
                    img_s[j, i, 2] = 0
                    nPts_s += 1
        fill_s = nPts_s / (nPts_s + nPts)

        if fill_h > max_fill:
            max_fill = fill_h
            max_angle = rotate_angle
            max_direction = 1
            max_fill_img = img_h

        if fill_s > max_fill:
            max_fill = fill_s
            max_angle = rotate_angle
            max_direction = 0

    return max_fill

# 示例使用
# 假设 img 是一个二维 NumPy 数组，代表你的图像
# fill_ratio = fig_fillin(img)
# print(fill_ratio)