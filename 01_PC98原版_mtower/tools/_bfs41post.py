# -*- coding: utf-8 -*-
"""41F 事件后网格连通性：把 (5,6)(6,6)(7,6) 设墙、(5,7)(7,7) 设地板、(6,5) 放翼，
从若干起点 BFS，看 (6,5) 是否可达（先纯几何=怪可走，再怪阻挡）。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
from collections import deque

# 应用事件
ter = {}
ter[(5,6)]=3; ter[(6,6)]=3; ter[(7,6)]=3   # 墙 (tile3→wall)
ter[(5,7)]=0; ter[(7,7)]=0                   # 地板
WING=(6,5)

def walkable(x,y):
    if ter.get((x,y))==3: return False
    # 静态地形
    t=M.terrain(41,x,y)
    if t==1: return False
    if (x,y)==(6,11): return False  # 上行梯（可走但要转层，这里当连通）
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

for start in [(10,2),(9,2),(6,5),(6,6),(6,2),(3,7),(3,6)]:
    s=bfs(start)
    reach=sorted(s)
    print('start(%d,%d) size=%d  wing可达=%s  40F梯(6,1)可达=%s  42F梯(6,11)可达=%s' % (
        start[0],start[1],len(s),(WING in s),((6,1) in s),((6,11) in s)))
# 全图（怪阻挡视角）
print()
print('== 几何连通（怪不算阻挡）==')
for start in [(10,2),(6,5)]:
    s=bfs(start)
    print('from(%d,%d):'%start, sorted(s))
