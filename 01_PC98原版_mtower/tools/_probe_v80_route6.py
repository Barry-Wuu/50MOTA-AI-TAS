# -*- coding: utf-8 -*-
"""41F 完整钥匙 BFS：找 (2,2)/(10,2)/(6,5)/(6,1)/(6,11) 的连通入口路径。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
from collections import deque

# 状态：层上可用的钥匙数（假设无限黄/蓝/红，探测连通性上限）
KEYCOL = {1: 'y', 3: 'b', 28: 'r'}
DOORCOL = {2: 'y', 4: 'b', 27: 'r'}

def bfs(f, start, keys={'y': 99, 'b': 99, 'r': 99}):
    # (x, y, 剩余黄, 剩余蓝, 剩余红) 状态 BFS，找最短钥匙消耗路径
    dist = {(start + (keys['y'], keys['b'], keys['r'])): 0}
    q = deque([start + (keys['y'], keys['b'], keys['r'])])
    best = {}
    while q:
        x, y, ky, kb, kr = q.popleft()
        key = (x, y)
        # 记录该格可达的钥匙状态（保留钥匙最多的）
        if key not in best or (ky, kb, kr) > best[key]:
            best[key] = (ky, kb, kr)
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if not (1 <= nx <= 11 and 1 <= ny <= 11):
                continue
            if M.terrain(f, nx, ny) in (1, 2):
                continue
            o = M.obj_raw(f, nx, ny)
            nky, nkb, nkr = ky, kb, kr
            if o:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if ty == 'MONSTER':
                    continue
                if ty == 'DOOR':
                    col = DOORCOL.get(o)
                    if col == 'y':
                        if nky <= 0: continue
                        nky -= 1
                    elif col == 'b':
                        if nkb <= 0: continue
                        nkb -= 1
                    elif col == 'r':
                        if nkr <= 0: continue
                        nkr -= 1
                    else:
                        continue
            nst = (nx, ny, nky, nkb, nkr)
            if nst in dist:
                continue
            dist[nst] = dist[(x, y, ky, kb, kr)] + 1
            q.append(nst)
    return best

# 从 (6,2) 落点开始，无限钥匙
best = bfs(41, (6, 2))
print('=== 41F 从(6,2) 无限钥匙可达格 ===')
targets = [(2,2,'魔術師Ａ(2,2)'), (10,2,'暗墙(10,2)'), (6,5,'翼格(6,5)'), (6,1,'下梯旁(6,1)'), (6,11,'上梯旁(6,11)'),
           (9,2,'(9,2)'), (10,3,'(10,3)'), (10,1,'蓝钥(10,1)'), (5,7,'(5,7)'), (7,7,'(7,7)'),
           (4,11,'红晶(4,11)'), (8,11,'蓝晶(8,11)'), (3,11,'黄钥(3,11)'), (9,11,'黄钥(9,11)')]
for tx, ty, label in targets:
    print('  %-22s %s' % (label, '可达 keys=%s' % str(best.get((tx,ty))) if (tx,ty) in best else '不可达'))

print()
print('=== 41F (10,2) 邻格入口 ===')
for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
    nx, ny = 10+dx, 2+dy
    if 1<=nx<=11 and 1<=ny<=11:
        t = M.terrain(41, nx, ny)
        o = M.obj_raw(41, nx, ny)
        reach = best.get((nx, ny))
        print('  (%d,%d) terr=%d obj=%d %s  可达=%s' % (nx, ny, t, o, M.oname(o) if o else '', 'keys=%s' % str(reach) if reach else '不可达'))
