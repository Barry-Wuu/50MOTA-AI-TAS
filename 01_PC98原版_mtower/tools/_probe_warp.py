# -*- coding: utf-8 -*-
"""打印 46F/47F/48F 全部楼梯 WARP 目标。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

for f in (46, 47, 48):
    for y in range(13):
        for x in range(13):
            if M.terrain(f, x, y) == 2:
                t = M.warp_to(f, x, y)
                kind = 'UP' if M.stair_up(f, x, y) else 'DN'
                print('%dF(%d,%d) %s -> %s' % (f, x, y, kind, t))
