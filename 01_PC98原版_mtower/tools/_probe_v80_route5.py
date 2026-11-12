# -*- coding: utf-8 -*-
"""41F 事件路径连通性 BFS：落点(6,2)→杀(2,2)→撞(10,2)→杀埋伏→得(6,5)翼。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
from collections import deque

def passable(f, x, y, doors=('y','b')):
    if not (1 <= x <= 11 and 1 <= y <= 11):
        return False
    if M.terrain(f, x, y) in (1, 2):
        return False
    o = M.obj_raw(f, x, y)
    if o:
        ty = M.TYPE.get(M.oatr(o, 3), '?')
        if ty == 'DOOR':
            col = M.DOOR_OF.get(o)
            if col not in doors:
                return False
        if ty == 'MONSTER':
            return False
    return True

def bfs(f, start, doors=('y','b')):
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if not passable(f, nx, ny, doors):
                continue
            if (nx, ny) in dist:
                continue
            dist[(nx, ny)] = dist[(x, y)] + 1
            q.append((nx, ny))
    return dist

# 41F 事件前：杀(2,2) 前，需从落点(6,2) 走到 (2,2) 邻格
print('=== 41F 事件前 BFS（开黄+蓝门，从落点(6,2)）===')
d = bfs(41, (6, 2))
targets = [(2,2,'魔術師Ａ(2,2)'), (10,2,'暗墙/埋伏(10,2)'), (6,5,'降臨の翼格(6,5)'), (6,1,'下行梯旁(6,1)'), (6,11,'上行梯旁(6,11)')]
for tx, ty, label in targets:
    # 杀怪前，(2,2) 是怪格，检查其邻格可达
    if (tx, ty) == (2, 2):
        nb = [(2+dx, 2+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))]
        reach = {n: d.get(n) for n in nb if n in d}
        print('  %s 邻格可达: %s' % (label, reach))
    else:
        print('  %s 距离: %s' % (label, d.get((tx, ty), '不可达')))

print()
print('=== 41F 事件后（假设 (5,6)(6,6)(7,6) 暗墙、(5,7)(7,7) 地板、(6,5) 翼）===')
# 事件后：杀(2,2)(10,2)后，(5,6)(6,6)(7,6)变暗墙（不可走），(5,7)(7,7)变地板
# 从(6,5)翼格 到 下行梯旁(6,1) / 上行梯旁(6,11) 的连通性
# 用简化模型：把(5,6)(6,6)(7,6)标记为不可走
print('  事件后 (6,5) 翼格邻: (6,4)走,(6,6)暗墙,(5,5)墙,(7,5)墙')
print('  事件后关键: 从(6,5)需走到(6,1)下行梯旁或(6,11)上行梯旁')
print('  路径: (6,5)→(6,4)→(6,3)→(6,2)→(6,1) 或 (6,5)→(6,4)→...→(6,11)')
# 检查 (6,1)-(6,11) 竖列连通性（x=6 列）
for y in range(1, 12):
    t = M.terrain(41, 6, y)
    o = M.obj_raw(41, 6, y)
    print('  (6,%d) terr=%d obj=%d %s' % (y, t, o, M.oname(o) if o else ''))
