#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mota_core as M
from collections import deque

def dump(f):
    print('==== %dF 详细 ===='%f)
    for y in range(1,12):
        for x in range(1,12):
            t=M.terrain(f,x,y)
            o=M.obj_raw(f,x,y)
            nm=M.oname(o)[:4] if o else ''
            print('%d,%d t%d o%d %s'%(x,y,t,o,nm))
        print()

# BFS from a start treating doors as passable-if-key (we don't have keys here, so mark door cells as 'D' and forbid)
def reach(f, sx, sy):
    seen={(sx,sy)}
    q=deque([(sx,sy)])
    while q:
        x,y=q.popleft()
        for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
            nx,ny=x+dx,y+dy
            if not(1<=nx<=11 and 1<=ny<=11): continue
            if (nx,ny) in seen: continue
            t=M.terrain(f,nx,ny)
            if t==1: continue
            o=M.obj_raw(f,nx,ny)
            ty=M.TYPE.get(M.oatr(o,3),'?') if o else '空'
            if ty=='DOOR': continue   # 无钥匙视为不可过（门格单独分析）
            if ty=='SAIDAN': continue
            seen.add((nx,ny))
            q.append((nx,ny))
    return seen

for f in (11,12):
    print('==== %dF 可达(无钥匙,从落点) ===='%f)
    ent = (2,11) if f==13 else None
    # 11F 落点 (6,10); 12F 落点 (10,11)
    sx,sy = (6,10) if f==11 else (10,11)
    s=reach(f,sx,sy)
    grid=[['··']*11 for _ in range(11)]
    for (x,y) in s: grid[y-1][x-1]='RR'
    grid[sy-1][sx-1]='SS'
    for y in range(1,12):
        print('%2d '%y+''.join(grid[y-1]))
    print('可达数:',len(s))
