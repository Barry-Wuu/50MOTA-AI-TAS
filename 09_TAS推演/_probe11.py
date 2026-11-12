# -*- coding: utf-8 -*-
"""从真实 1 区终态出发，探测 11F 当前可达的怪/道具（用于补金币与补攻）。"""
import os, sys
HERE = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
sys.path.insert(0, HERE)
os.environ['MOTA_STOP_11F'] = '1'
import run_segs
import z2_route as Z
import mota_core as M
from collections import deque

run_segs.main()
w = run_segs.LAST_W
h = w.hero
print('起点', Z.st(h))

f = 11
seen = {(h.x, h.y)}
q = deque([(h.x, h.y)])
while q:
    cx, cy = q.popleft()
    for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n = (cx + d[0], cy + d[1])
        if n in seen:
            continue
        ok, c = Z._cost(w, f, *n)
        if not ok:
            continue
        seen.add(n)
        q.append(n)

mons, items = [], []
for (x, y) in sorted(seen):
    o = w.at(f, x, y)
    if not o:
        continue
    ty = M.TYPE.get(M.oatr(o, 3))
    if ty == 'MONSTER':
        r = w.battle(o)
        dmg = (r[1] if r else -1)
        mons.append((x, y, o, M.oname(o), M.oatr(o, 13), dmg))
    elif ty in ('STATUS', 'ITEM') or o in M.KEY_OF:
        items.append((x, y, o, M.oname(o)[:14]))
print('\n可达怪（坐标, 名字, 金币, 战损）:')
for m in mons:
    print('  (%2d,%2d) obj%-3d %-10s g%-3d 损%d' % m)
print('\n可达道具/钥匙:')
for it in items:
    print('  (%2d,%2d) obj%-3d %s' % it)
