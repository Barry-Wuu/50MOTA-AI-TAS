# -*- coding: utf-8 -*-
"""从 (6,10) 出发的连通格（只走空/钥匙/装饰/物品，不开门不战斗）"""
import sys
from collections import deque
sys.path.insert(0, 'tools')
import mota_core as M

w = M.World.new()
w.apply_floor_events(42)
start = (6, 10)

def walkable(f, x, y):
    if w.terrain_at(f, x, y) in (1, 2):
        return False
    if (x, y) in M.STAIRS.get(f, (None, None)) and (x, y) != start:
        return False
    o = w.at(f, x, y)
    if not o:
        return True
    t = M.TYPE.get(M.oatr(o, 3), '?')
    if o in M.KEY_OF or t in ('STATUS', 'ITEM', 'NORMAL', 'SCORE', 'MESSAGE'):
        return True
    if o in M.DECOR_PASS:
        return True
    return False

seen = {start}
dq = deque([start])
while dq:
    x, y = dq.popleft()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n = (x + dx, y + dy)
        if n in seen or not (1 <= n[0] <= 11 and 1 <= n[1] <= 11):
            continue
        if walkable(42, *n):
            seen.add(n)
            dq.append(n)

print('=== 42F 从 (6,10) 连通（不战斗不开门）===')
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        o = w.at(42, x, y)
        t = M.TYPE.get(M.oatr(o, 3), '?')
        ch = '·'
        if (x, y) == start:
            ch = '@'
        elif (x, y) in seen:
            ch = '.'
        elif o and t == 'MONSTER':
            ch = 'M'
        elif o and t == 'DOOR':
            ch = 'D'
        elif o in M.KEY_OF:
            ch = 'k'
        elif o:
            ch = '?'
        elif w.terrain_at(42, x, y) == 1:
            ch = '#'
        row.append(ch)
    print('%2d' % y, ' '.join(row))
