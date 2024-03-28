'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 13:44:45
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 14:05:43
FilePath: /handwritingEval/fig_component.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np
import cv2
from intersect_area import IntersectArea
def fig_component(component_images, component_boxes):
    component_feature_vect = []
    
    component_num = len(component_boxes) // 2
    if component_num == 1:
        return []
    
    hm = {}
    wm = {}
    component_images_edge = {}
    startp = []
    gravity = []
    endp = []
    
    # 获取组件最小边界框的位置和重心
    for j in range(component_num):
        component_image_edge = cv2.Canny(component_images[j], 100, 200)
        h_component, w_component = component_images[j].shape
        _, hm[j], wm[j] = cv2.findNonZero(component_image_edge)
        
        mstart = component_boxes[2 * j - 1, :]
        
        startp.append((mstart[1], mstart[0]))
        gravity.append((startp[-1][0] + round(h_component / 2) - 1, startp[-1][1] + round(w_component / 2) - 1))
        endp.append((startp[-1][0] + h_component - 1, startp[-1][1] + w_component - 1))
        
        hm[j] += mstart[1] - 1
        wm[j] += mstart[0] - 1
    
    # 计算两个组件之间的距离和重叠
    for m in range(component_num - 1):
        for n in range(m + 1, component_num):
            pnum_m = len(hm[m])
            pnum_n = len(hm[n])
            count = 0
            maxdis = -1
            mindis = 100000
            meandisr = []
            d = {}
            minh = min(startp[m][0], startp[n][0])
            minw = min(startp[m][1], startp[n][1])
            maxh = max(endp[m][0], endp[n][0])
            maxw = max(endp[m][1], endp[n][1])
            diagonal = np.sqrt((maxh - minh) ** 2 + (maxw - minw) ** 2)
            for p in range(pnum_m):
                for q in range(pnum_n):
                    d[p, q] = np.sqrt((hm[m][p] - hm[n][q]) ** 2 + (wm[m][p] - wm[n][q]) ** 2)
                    if d[p, q] > maxdis:
                        maxdis = d[p, q]
                        maxdis_p = [hm[m][p], wm[m][p], hm[n][q], wm[n][q]]
                    if d[p, q] < mindis:
                        mindis = d[p, q]
                        mindis_p = [hm[m][p], wm[m][p], hm[n][q], wm[n][q]]
                    count += 1
            meandis = np.mean([d[p, :] for p in range(pnum_m)])
            
            Bbw = abs(gravity[m][1] - gravity[n][1]) / (component_images[m].shape[1] + component_images[n].shape[1])
            Bvh = abs(gravity[m][0] - gravity[n][0]) / (component_images[m].shape[0] + component_images[n].shape[0])
            interarea = IntersectArea(startp[m], endp[m], startp[n], endp[n])
            Bp = interarea / (component_images[m].shape[0] * component_images[m].shape[1] + component_images[n].shape[0] * component_images[n].shape[1] - interarea)
            
            component_feature_vect.extend([maxdis / diagonal, mindis / diagonal, meandis / diagonal])
            component_feature_vect.extend([Bbw, Bvh, Bp])
    
    return np.array(component_feature_vect)


# 示例使用
# 假设 component_images 是一个包含组件图像的列表
# 假设 component_boxes 是一个包含组件边界框位置的 NumPy 数组
# features = fig_component(component_images, component_boxes)
# print(features)