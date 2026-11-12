# -*- coding: utf-8 -*-
"""47F 连通性分析：从 (1,2) 出发 BFS，看各怪可达性与最短步数（不开门/开黄/开黄蓝）。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

F = 47

def passable(x, y):
    if not (1 <= x <= 11 and 1 <= y <= 11):
        return False
    if M.terrain(F, x, y) == 1:
        return False
    return True

def cell(x, y):
    o = M.obj_raw(F, x, y)
    if not o:
        return '.'
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if o in M.KEY_OF:
        return {'y': 'y', 'b': 'b', 'r': 'r'}[M.KEY_OF[o]]
    if o in M.DOOR_OF:
        return {'y': 'Y', 'b': 'B', 'r': 'R'}[M.DOOR_OF[o]]
    if ty == 'MONSTER':
        return 'm'
    if ty in ('ITEM', 'STATUS'):
        return '!'
    return '?'

def bfs(start, doors_open=()):
    from collections import deque
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if not passable(nx, ny):
                continue
            o = M.obj_raw(F, nx, ny)
            if o and M.TYPE.get(M.oatr(o, 3), '?') == 'DOOR':
                col = M.DOOR_OF.get(o)
                if col not in doors_open:
                    continue
            if (nx, ny) in dist:
                continue
            dist[(nx, ny)] = dist[(x, y)] + 1
            q.append((nx, ny))
    return dist

print('47F 静态网格（x1-11, y1-11, @起点(1,2)）:')
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        c = cell(x, y)
        if (x, y) == (1, 2):
            c = '@'
        row.append(c)
    print('y=%2d: %s' % (y, ' '.join(row)))
print()

# 从 (1,2) 出发：不开门
d1 = bfs((1, 2), ())
print('不开门：可达 %d 格' % len(d1))
# 开黄门
d2 = bfs((1, 2), ('y',))
print('开黄门：可达 %d 格' % len(d2))
# 开黄+蓝
d3 = bfs((1, 2), ('y', 'b'))
print('开黄+蓝：可达 %d 格' % len(d3))
print()

# 列出各怪位置与可达性/距离
monsters = []
for y in range(1, 12):
    for x in range(1, 12):
        o = M.obj_raw(F, x, y)
        if not o:
            continue
        if M.TYPE.get(M.oatr(o, 3), '?') != 'MONSTER':
            continue
        hp, atk, dfn, gold = M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13)
        monsters.append((x, y, o, hp, atk, dfn, gold, M.oname(o)))

print('47F 怪物（A217/D201 伤害计算）:')
tot_g = 0
tot_hp = 0
for (x, y, o, hp, atk, dfn, gold, name) in monsters:
    dmg = max(0, atk - 201) * ((hp + (217 - dfn) - 1) // (217 - dfn)) if 217 > dfn else 99999
    reach3 = d3.get((x, y), -1)
    print('(%2d,%2d) obj%-3d %-10s HP%d ATK%d DEF%d 金%d | 伤害%d 开黄蓝距离%d' % (
        x, y, o, name, hp, atk, dfn, gold, dmg, reach3))
    tot_g += gold
    tot_hp += dmg
print('合计：金币%d 伤害%d' % (tot_g, tot_hp))

# 关键目标距离
for tgt, label in [((5,7),'蓝钥'), ((5,2),'商店'), ((11,11),'下行梯'), ((2,6),'黄门(2,6)'), ((4,4),'黄门(4,4)')]:
    for label2, dist in [('不开门', d1.get(tgt, -1)), ('开黄', d2.get(tgt, -1)), ('开黄蓝', d3.get(tgt, -1))]:
        if dist >= 0:
            print('%s(%s) 距离%d' % (label, label2, dist))
