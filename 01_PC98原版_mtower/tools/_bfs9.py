# -*- coding: utf-8 -*-
"""_bfs9.py —— 9F 从 (1,10) 到楼梯 (6,1) 真实状态 BFS（完整状态：x,y,yk,bk,hp,已拾/清集合）。
代价=步数，求最短可行路径。拾取物和怪物均计入状态（拾取一次性、怪物清空一次性）。
"""
import mota_core as M
from collections import deque

w = M.World.new()
f = 9
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def otype(o):
    return M.TYPE.get(M.oatr(o, 3))

def passive(o):
    """拾取/状态/空地/楼梯旁可站格——不消耗钥匙不战斗，一次性拾取。"""
    if o == 0:
        return True
    ty = otype(o)
    return ty in ('STATUS', 'ITEM', 'NORMAL', 'SCORE', 'MESSAGE') or o in M.KEY_OF

# 起点 = V10 下 9F 时的真实状态（HP535 A61 D33 钥2/0/0）
start = (1, 10, 2, 0, 535, frozenset())  # x,y,yk,bk,hp,taken
seen = {start}
q = deque([(start, [])])
targets = {(5, 1), (7, 1)}  # 楼梯 (6,1) 的邻格（可站）
best = None

while q:
    (x, y, yk, bk, hp, taken), path = q.popleft()
    if (x, y) in targets:
        best = (x, y, yk, bk, hp, taken, path)
        break
    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if not (1 <= nx <= 11 and 1 <= ny <= 11):
            continue
        t = w.terrain_at(f, nx, ny)
        if t in (1, 2):
            continue
        o = w.at(f, nx, ny)
        if o == 0:
            st = (nx, ny, yk, bk, hp, taken)
        elif passive(o):
            if o in taken:
                st = (nx, ny, yk, bk, hp, taken)
            else:
                nyk, nbk = yk, bk
                if o == 1:
                    nyk += 1
                elif o == 3:
                    nbk += 1
                st = (nx, ny, nyk, nbk, hp, taken | {o})
        elif otype(o) == 'DOOR':
            if o == 2:
                if yk < 1:
                    continue
                st = (nx, ny, yk - 1, bk, hp, taken)
            elif o == 4:
                if bk < 1:
                    continue
                st = (nx, ny, yk, bk - 1, hp, taken)
            else:
                continue
        elif otype(o) == 'MONSTER':
            if o in taken:
                st = (nx, ny, yk, bk, hp, taken)
            else:
                r = w.battle(o)
                if r is None or r[0] >= hp:
                    continue
                st = (nx, ny, yk, bk, hp - r[0], taken | {o})
        else:
            continue
        if st in seen:
            continue
        seen.add(st)
        q.append((st, path + [(nx, ny)]))

if best:
    x, y, yk, bk, hp, taken, path = best
    print('REACHABLE end (%d,%d) yk=%d bk=%d hp=%d taken=%d steps=%d' % (x, y, yk, bk, hp, len(taken), len(path)))
    for i, (px, py) in enumerate(path):
        o = w.at(f, px, py)
        print('  %2d (%d,%d) obj%s' % (i + 1, px, py, o if o else '-'))
else:
    print('NOT REACHABLE. states=%d' % len(seen))
