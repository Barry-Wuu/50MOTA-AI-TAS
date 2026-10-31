# -*- coding: utf-8 -*-
"""逐格打印指定楼层的 terrain 原值 + obj + 通行性，用于核对 ASCII 图。"""
import sys, io, csv
TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
sys.path.insert(0, TOOLS)
import mota_core as M

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
FAIL = ('blocked', '打不动', '打不过', '无', '买不起', '熔岩烫死', '祭坛金币不足')
rows_rec = list(csv.DictReader(io.open(SRC + '魔塔1_route_1F到21F.csv', encoding='utf-8-sig')))
w = M.World.new()


def pick_move(r):
    tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
    rec = dict(atk=int(r['atk']), dfn=int(r['def']), gold=int(r['gold']),
               ky=int(r['ky']), kb=int(r['kb']), kr=int(r['kr']))
    h = w.hero
    same = (h.f, h.x, h.y) == (tf, tx, ty)
    best = None
    for d in DIRS:
        c = w.clone(); lg = c.move(*d)
        if lg and lg[0].startswith(FAIL): continue
        hh = c.hero; sc = 0
        if (hh.f, hh.x, hh.y) == (tf, tx, ty): sc += 8
        elif same and (hh.f, hh.x, hh.y) == (h.f, h.x, h.y) and lg: sc += 4
        else: continue
        for k, cur in (('atk', hh.atk), ('dfn', hh.dfn), ('gold', hh.gold)):
            if cur == rec[k]: sc += 1
        for k, kk in (('ky', 'y'), ('kb', 'b'), ('kr', 'r')):
            if hh.keys.get(kk, 0) == rec[k]: sc += 1
        if bool(lg) == bool((r['event'] or '').strip()): sc += 1
        if best is None or sc > best[0]: best = (sc, d)
    return best


for i in list(range(0, 42)) + list(range(60, 67)):
    b = pick_move(rows_rec[i]); lg = w.move(*b[1])

FL = int(sys.argv[1])
Y0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
Y1 = int(sys.argv[3]) if len(sys.argv) > 3 else 12
for y in range(Y0, Y1 + 1):
    parts = []
    for x in range(13):
        t = w.terrain_at(FL, x, y); o = w.at(FL, x, y)
        parts.append('%d:(t%d,o%d)' % (x, t, o))
    print('y%-2d ' % y + ' '.join(parts))
print('raw terrain row check:')
for y in range(Y0, Y1 + 1):
    print(' y%d:' % y, [M.terrain(FL, x, y) for x in range(13)])
