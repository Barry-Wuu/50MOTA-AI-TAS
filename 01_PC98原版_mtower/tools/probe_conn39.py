# -*- coding: utf-8 -*-
"""探查楼梯连通图：39F -> 31F 的具体路径。WARP 键为 (f,x,y)。"""
import os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import mota_core as mc

print('=== 39F 楼梯 ===')
for (sf, sx, sy), dst in mc.WARP.items():
    if sf == 39:
        print('  39F(%d,%d) -> %dF(%d,%d)' % (sx, sy, dst[0], dst[1], dst[2]))

print('\n=== 38F 楼梯 ===')
for (sf, sx, sy), dst in mc.WARP.items():
    if sf == 38:
        print('  38F(%d,%d) -> %dF(%d,%d)' % (sx, sy, dst[0], dst[1], dst[2]))

print('\n=== 31F 楼梯 ===')
for (sf, sx, sy), dst in mc.WARP.items():
    if sf == 31:
        print('  31F(%d,%d) -> %dF(%d,%d)' % (sx, sy, dst[0], dst[1], dst[2]))

# BFS：从 39F 出发沿楼梯，找 31F
from collections import deque
print('\n=== BFS 沿楼梯找 31F ===')
# 状态：(f, x, y) 落点；边 = 走到楼梯格 -> warp
start = (39, 11, 2)
q = deque([start])
seen = {start}
found = None
while q:
    f, x, y = q.popleft()
    # 找该层所有楼梯，尝试 warp
    for (sf, sx, sy), dst in mc.WARP.items():
        if sf == f:
            df, dx, dy = dst
            if df == 31:
                print('  FOUND: %dF(%d,%d) -> 31F(%d,%d)' % (f, sx, sy, dx, dy))
                found = (f, sx, sy, dst)
            nxt = (df, dx, dy)
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)

print('\n=== 从 39F 出发全部可达层（沿楼梯）===')
print(sorted(set(k[0] for k in seen)))

# 哪些层可达 31F（反向）
print('\n=== 哪些层楼梯可达 31F ===')
for (sf, sx, sy), dst in mc.WARP.items():
    if dst[0] == 31:
        print('  %dF(%d,%d) -> 31F(%d,%d)' % (sf, sx, sy, dst[1], dst[2]))
