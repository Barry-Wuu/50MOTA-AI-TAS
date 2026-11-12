# -*- coding: utf-8 -*-
"""找 39F -> 32F 的最短楼梯路径并列出中间层。"""
import os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import mota_core as mc
from collections import deque

def neighbors(f):
    """该层所有楼梯的 (目标层, 落点, 楼梯格)。"""
    res = []
    for (sf, sx, sy), dst in mc.WARP.items():
        if sf == f:
            res.append((dst[0], dst, (sx, sy)))
    return res

# BFS: (f, x, y) 落点状态
start = (39, 11, 2)
goal_f = 32
q = deque([(start, [])])
seen = {start}
while q:
    (f, x, y), path = q.popleft()
    if f == goal_f:
        print('=== 到达 %dF ===' % goal_f)
        for step in path:
            print('  ', step)
        break
    for df, dst, stair in neighbors(f):
        nxt = (df, dst[1], dst[2])
        if nxt not in seen:
            seen.add(nxt)
            label = '%dF楼梯(%d,%d)->%dF(%d,%d)' % (f, stair[0], stair[1], df, dst[1], dst[2])
            q.append((nxt, path + [label]))

# 也打印 40F 和 37F 楼梯
print('\n=== 40F 楼梯 ===')
for (sf, sx, sy), dst in mc.WARP.items():
    if sf == 40:
        print('  40F(%d,%d) -> %dF(%d,%d)' % (sx, sy, dst[0], dst[1], dst[2]))
print('\n=== 37F 楼梯 ===')
for (sf, sx, sy), dst in mc.WARP.items():
    if sf == 37:
        print('  37F(%d,%d) -> %dF(%d,%d)' % (sx, sy, dst[0], dst[1], dst[2]))
print('\n=== 32F 楼梯 ===')
for (sf, sx, sy), dst in mc.WARP.items():
    if sf == 32:
        print('  32F(%d,%d) -> %dF(%d,%d)' % (sx, sy, dst[0], dst[1], dst[2]))
