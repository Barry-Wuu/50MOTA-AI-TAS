# -*- coding: utf-8 -*-
"""基于 manual.py 执行完 PLAN 后的实时局面，做静态连通块分析（含格子清单，不做寻路）。"""
import sys
from collections import deque
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演')
import manual as MAN
import mota_core as M

W = MAN.W
DIRS = MAN.DIRS


def passable(f, x, y):
    if not (0 <= x < 13 and 0 <= y < 13):
        return False
    if W.terrain_at(f, x, y) in (1, 2):
        return False
    o = W.at(f, x, y)
    if o == 0:
        return True
    if o in (19, 79, 89) or o in M.ALTAR_SIDE:
        return False
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    return ty in ('STATUS', 'ITEM', 'KEY', 'NORMAL', 'SCORE', 'MESSAGE', 'SAIDAN', 'SELL', 'BUY')


def desc(o):
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if ty == 'MONSTER':
        return '%s(%d/%d/%d)' % (M.oname(o)[:8], M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12))
    return '%s#%d' % (M.oname(o)[:8], o)


MAN.execute(MAN.PLAN, verbose=False)
print('当前 ' + MAN.st())

for f in [int(a) for a in sys.argv[1:] if a.isdigit()]:
    cells = [(x, y) for y in range(13) for x in range(13) if passable(f, x, y)]
    seen = set(); comps = []
    for c in cells:
        if c in seen:
            continue
        q = deque([c]); seen.add(c); comp = [c]
        while q:
            cur = q.popleft()
            for d in DIRS:
                n = (cur[0] + d[0], cur[1] + d[1])
                if n in seen or not passable(f, n[0], n[1]):
                    continue
                seen.add(n); comp.append(n); q.append(n)
        comps.append(sorted(comp))
    print('=' * 70)
    print('%dF  自由连通块 %d 个' % (f, len(comps)))
    for k, comp in enumerate(comps, 1):
        its = ['(%d,%d)%s' % (x, y, desc(W.at(f, x, y))) for (x, y) in comp if W.at(f, x, y)]
        bd = []
        for (x, y) in comp:
            for d in DIRS:
                n = (x + d[0], y + d[1])
                if not (0 <= n[0] < 13 and 0 <= n[1] < 13) or passable(f, n[0], n[1]):
                    continue
                o = W.at(f, n[0], n[1])
                if not o or o in (19, 79, 89) or o in M.ALTAR_SIDE:
                    continue
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if ty in ('DOOR', 'MONSTER'):
                    s = '(%d,%d)%s' % (n[0], n[1], desc(o))
                    if s not in bd:
                        bd.append(s)
        print('  块#%-2d %2d格 格: %s' % (k, len(comp), ' '.join('(%d,%d)' % c for c in comp)))
        print('       物件: %s' % ('; '.join(its) if its else '-'))
        print('       关口: %s' % ('; '.join(bd) if bd else '-'))
