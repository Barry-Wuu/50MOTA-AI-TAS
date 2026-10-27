#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mota_core as M

# 1) 12F 上行梯落点（即 13F 入口）
up, dn = M.STAIRS[12]
print('12F 上行梯坐标:', up, ' 下行:', dn)
print('12F(6,1) 是否上行梯:', M.stair_up(12,6,1))
# 找 13F 入口：所有 terrain==2 的格 + warp 落点
print('WARP 涉及 13F 的:', {k:v for k,v in M.WARP.items() if v[0]==13 or k[0]==13})

# 2) 13F 详细网格：每格输出 terrain 与 obj
print('\n=== 13F 详细 (terrain,obj,name) ===')
for y in range(1,12):
    row=[]
    for x in range(1,12):
        t=M.terrain(13,x,y)
        o=M.obj_raw(13,x,y)
        nm=M.oname(o)[:3] if o else ''
        row.append('%d%s%s'%(t, o if o else '-', nm))
    print('%2d '%y + ' | '.join('%-9s'%c for c in row))

# 3) 假设入口，做 BFS 看可达与到 (6,5) 的最短路（不计战斗，仅墙/熔岩/门）
from collections import deque
def entry():
    # 12F 上行梯落点
    for k,v in M.WARP.items():
        if k[0]==12 and M.stair_up(*k):
            return v
    return None
ent=entry()
print('\n推测 13F 入口:', ent)
if ent:
    sx,sy=ent[1],ent[2]
    seen=set([(sx,sy)])
    q=deque([(sx,sy,0)])
    reach={'%d,%d'%(sx,sy):0}
    while q:
        x,y,d=q.popleft()
        for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
            nx,ny=x+dx,y+dy
            if not(1<=nx<=11 and 1<=ny<=11): continue
            if (nx,ny) in seen: continue
            t=M.terrain(13,nx,ny)
            if t==1: continue  # 墙
            # 熔岩可走但掉血；门需钥匙，这里先当可走看连通
            seen.add((nx,ny))
            reach['%d,%d'%(nx,ny)]=d+1
            q.append((nx,ny,d+1))
    print('可达格子数:', len(seen))
    print('(6,5) 是否可达:', '(6,5)' in reach, ' 距离:', reach.get('6,5'))
    print('(6,6) 是否可达:', '(6,6)' in reach)
    # 打印哪些格子可达
    grid=[['  ']*11 for _ in range(11)]
    for s,d in reach.items():
        xx,yy=map(int,s.split(','))
        grid[yy-1][xx-1]='R ' if (xx,yy)!=(sx,sy) else 'S '
    grid[sy-1][sx-1]='S '
    for y in range(1,12):
        print('%2d '%y+''.join(grid[y-1]))
