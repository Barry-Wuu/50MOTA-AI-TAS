# -*- coding: utf-8 -*-
"""41F 事件后连通性（正确应用 ter_over：MA[tile][3]）。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
from collections import deque

ter = {(5,6):3,(6,6):3,(7,6):3,(5,7):0,(7,7):0}
WING=(6,5)

def terrain_at(x,y):
    if (x,y) in ter:
        t=ter[(x,y)]
        return M.MA[t][3] if t < len(M.MA) else 1
    return M.terrain(41,x,y)

def walkable(x,y):
    if terrain_at(x,y)==1: return False
    return True

def bfs(start, block_monsters=False):
    seen={start}; q=deque([start])
    while q:
        x,y=q.popleft()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if not(1<=nx<=11 and 1<=ny<=11): continue
            if (nx,ny) in seen: continue
            if not walkable(nx,ny): continue
            if block_monsters:
                o=M.obj_raw(41,nx,ny)
                if o and M.TYPE.get(M.oatr(o,3))=='MONSTER': continue
            seen.add((nx,ny)); q.append((nx,ny))
    return seen

print('== 几何连通（怪不算阻挡）==')
s=bfs((10,2)); print('from(10,2): wing=%s  40F(6,1)=%s  42F(6,11)=%s' % ((WING in s),(6,1) in s,(6,11) in s))
print('  可达:', sorted(s))
print()
print('== 怪阻挡（必须清怪才通）==')
s=bfs((10,2), block_monsters=True)
print('from(10,2) 怪阻挡: wing=%s  size=%d' % ((WING in s), len(s)))
