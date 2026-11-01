# -*- coding: utf-8 -*-
import sys, os
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

f = 32
# 当前 32F 已清（怪/门/道具），来自 32a-32d 段的执行记录：
cleared_cells = {   # (x,y) -> 说明
    (6,9):'金騎士已清', (8,4):'死霊兵士已清',
    (3,1):'蓝门已开', (7,3):'黄门已开', (9,5):'黄门已开',
    (1,1):'青水晶已取', (2,2):'红水晶已取', (11,4):'青药已取',
    (10,4):'黄钥已取', (11,5):'黄钥已取',
    (1,7):'黄钥已取',(2,7):'黄钥已取',(3,7):'黄钥已取',(4,7):'黄钥已取',(4,8):'蓝钥已取',
}
DIRS = ((1,0),(-1,0),(0,1),(0,-1))

def desc(x,y):
    o = M.obj_raw(f,x,y); t = M.terrain(f,x,y)
    if (x,y) in cleared_cells:
        return '已清'
    if o:
        return 'obj%d[%s]' % (o, M.oname(o)[:6])
    if t == 1: return '墙'
    if t == 2: return '楼梯'
    return '空地'

def walkable(x,y):
    if not (1<=x<=11 and 1<=y<=11): return False
    if (x,y) in cleared_cells: return True
    o = M.obj_raw(f,x,y); t = M.terrain(f,x,y)
    if t == 1: return False
    if t == 2: return False  # 楼梯不可踩（会换层）
    if o: return False  # 未清怪/门/道具 → 需消耗
    return True

start = (6,10)
seen = {start}
q = deque([start])
while q:
    cx,cy = q.popleft()
    for dx,dy in DIRS:
        nx,ny = cx+dx, cy+dy
        if (nx,ny) not in seen and walkable(nx,ny):
            seen.add((nx,ny)); q.append((nx,ny))

print('=== 32F 当前可达（从落点 (6,10) 出发，仅走已清/空地）===')
for y in range(1,12):
    row=''
    for x in range(1,12):
        if (x,y)==start: row+='S'
        elif (x,y) in seen: row+='.'
        else: row+='#'
    print(' y%-2d %s' % (y,row))

print()
print('=== 不可达但未清的关键格（需打怪/开门才能进）===')
for y in range(1,12):
    for x in range(1,12):
        if (x,y) in seen or (x,y) in cleared_cells: continue
        o = M.obj_raw(f,x,y); t = M.terrain(f,x,y)
        if o:
            print('  (%d,%d) obj%d[%s]' % (x,y,o,M.oname(o)[:10]))
