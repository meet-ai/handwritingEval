'''
Author: meetai meetai@gmx.com
Date: 2024-03-26 14:04:01
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-26 14:05:17
FilePath: /handwritingEval/intersect_area.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

def IntersectArea(startm, endm, startn, endn):
    # 检查矩形 m 是否在矩形 n 的右侧且在左下方
    if startm[0] < endn[0] and startm[0] > startn[0] and startm[1] < endn[1] and startm[1] > startn[1]:
        intersh = startm[0]
        intersw = startm[1]
        intereh = min(endm[0], endn[0])
        interew = min(endm[1], endn[1])
        y = (intereh - intersh) * (interew - intersw)
    # 检查矩形 n 是否在矩形 m 的右侧且在左下方
    elif startn[0] < endm[0] and startn[0] > startm[0] and startn[1] < endm[1] and startn[1] > startm[1]:
        intersh = startn[0]
        intersw = startn[1]
        intereh = min(endm[0], endn[0])
        interew = min(endm[1], endn[1])
        y = (intereh - intersh) * (interew - intersw)
    else:
        # 如果没有交集，返回 0
        y = 0
    return y

# 示例使用
# 假设 startm 和 endm 是矩形 m 的左上角和右下角坐标
# 假设 startn 和 endn 是矩形 n 的左上角和右下角坐标
# area = intersect_area(startm, endm, startn, endn)
# print(area)