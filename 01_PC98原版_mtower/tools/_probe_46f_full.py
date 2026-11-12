# -*- coding: utf-8 -*-
"""46F 完整探测：全格对象 + 怪物伤害/金币 + 落点(11,10) BFS 连通性。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
from collections import deque

F = 46
ATK, DEF = 217, 201

def passable(x, y):
    if not (1 <= x <= 11 and 1 <= y <= 11):
        return False
    if M.terrain(F, x, y) == 1:
        return False
    return True

print('46F 全格对象（非空）:')
for y in range(1, 12):
    for x in range(1, 12):
        t = M.terrain(F, x, y)
        o = M.obj_raw(F, x, y)
        info = []
        if t:
            info.append('terr=%d(%s)' % (t, {1:'墙',2:'楼梯'}.get(t, '?')))
        if o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            info.append('obj%d type=%s name=%s' % (o, ty, M.oname(o)))
        if info:
            print('(%2d,%2d): %s' % (x, y, ' | '.join(info)))

print()
print('46F 楼梯: up/dn =', M.stairs_of(F))

def bfs(start, doors_open=()):
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

print()
print('46F 怪物（A%d/D%d）:' % (ATK, DEF))
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

tot_g, tot_hp = 0, 0
for (x, y, o, hp, atk, dfn, gold, name) in monsters:
    dmg = max(0, atk - DEF) * ((hp + (ATK - dfn) - 1) // (ATK - dfn)) if ATK > dfn else 99999
    print('(%2d,%2d) obj%-3d %-10s HP%d ATK%d DEF%d 金%d | 伤害%d' % (
        x, y, o, name, hp, atk, dfn, gold, dmg))
    tot_g += gold
    tot_hp += dmg
print('46F 合计：金币%d 伤害%d' % (tot_g, tot_hp))

print()
# 从落点 (11,10) BFS
for label, doors in [('不开门', ()), ('开黄', ('y',)), ('开黄+蓝', ('y', 'b'))]:
    d = bfs((11, 10), doors)
    print('落点(11,10) %s：可达 %d 格' % (label, len(d)))
    # 各怪距离
    reach = []
    for (x, y, o, hp, atk, dfn, gold, name) in monsters:
        dist = d.get((x, y), -1)
        dmg = max(0, atk - DEF) * ((hp + (ATK - dfn) - 1) // (ATK - dfn)) if ATK > dfn else 99999
        reach.append((dist, x, y, name, dmg, gold))
    for (dist, x, y, name, dmg, gold) in sorted(reach):
        if dist >= 0:
            print('  (%2d,%2d) %-10s 距离%d 伤害%d 金%d' % (x, y, name, dist, dmg, gold))
