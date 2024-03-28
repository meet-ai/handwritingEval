'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 13:49:25
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 13:50:07
FilePath: /handwritingEval/fig_elastic_mesh.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np

def fig_elastic_mesh(img):
    h, w = img.shape
    x, y = np.where(img == 0)
    nPts = x.shape[0]
    mesh_num = 4  # 网格数量，例如 4x4 网格

    y0 = 1
    count = 0
    fig_elastic_mesh = []
    
    for i in range(mesh_num - 1):
        for mesh_y in range(y0, w):
            y_left = (y <= mesh_y) & (y > y0)
            
            if y_left.sum() > (nPts // mesh_num):
                break
            
            y0 = mesh_y
            count += 1
            fig_elastic_mesh.append(y0 / w)
    
    x0 = 1
    for i in range(mesh_num - 1):
        for mesh_x in range(x0, h):
            x_up = (x <= mesh_x) & (x > x0)
            
            if x_up.sum() > (nPts // mesh_num):
                break
            
            x0 = mesh_x
            count += 1
            fig_elastic_mesh.append(x0 / h)

    return np.array(fig_elastic_mesh)

# 示例使用
# 假设 img 是一个二维 NumPy 数组，代表你的图像
# mesh_layout = fig_elastic_mesh(img)
# print(mesh_layout)