# -*- coding: utf-8 -*-
"""统计 1..10F 的 HP 补给点，并标注 1F→11F 基线是否已经捡过（按路线 CSV 的 cleared 结果）。"""
import sys, csv, io, collections
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/魔塔1_route_1F到21F.csv'
rows = list(csv.DictReader(io.open(SRC, encoding='utf-8')))

# 仅为统计旧基线捡了哪些补给：临时放行 2F 栅栏门（不用于正式重放）
M.GATE_2F = set()

# 用旧引擎跑到 11F 前（1..1243 行），记录 cleared（这些格子已被消耗）
w = M.World.new()
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
FAIL = ('blocked', '打不动', '无', '买不起', '熔岩烫死', '打不过')


def go(r):
    global w
    tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
    rec = (int(r['atk']), int(r['def']), int(r['gold']), int(r['ky']), int(r['kb']), int(r['kr']))
    h = w.hero
    same = (h.f, h.x, h.y) == (tf, tx, ty)
    best = None
    for d in DIRS:
        c = w.clone(); lg = c.move(*d)
        if lg and lg[0].startswith(FAIL):
            continue
        hh = c.hero
        sc = 0
        if (hh.f, hh.x, hh.y) == (tf, tx, ty):
            sc += 4
        elif same and (hh.f, hh.x, hh.y) == (h.f, h.x, h.y) and lg:
            sc += 2
        else:
            continue
        if (hh.atk, hh.dfn, hh.gold, hh.keys.get('y', 0), hh.keys.get('b', 0), hh.keys.get('r', 0)) == rec:
            sc += 3
        if best is None or sc > best[0]:
            best = (sc, c)
    if best is None:
        return False
    w = best[1]
    return True


for i in range(1243):
    if not go(rows[i]):
        print('stop at', i + 1)
        break

print('reached', (w.hero.f, w.hero.x, w.hero.y), 'hp', w.hero.hp)

print('\n== 1..10F 所有 HP/属性 补给（obj 11/12/13/14 等 STATUS）==')
tot = collections.defaultdict(lambda: [0, 0, 0])  # floor -> [collected hp, missed hp, count]
for f in range(1, 11):
    for y in range(1, 12):
        for x in range(1, 12):
            o = M.obj_raw(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3))
            if ty != 'STATUS':
                continue
            hp, atk, dfn = M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12)
            got = (f, x, y) in w.cleared
            if hp:
                tot[f][0 if got else 1] += hp
                tot[f][2] += 1
            print('%2dF(%2d,%2d) obj%-4d %-8s hp%+d atk%+d def%+d  %s' %
                  (f, x, y, o, M.oname(o)[:8], hp, atk, dfn, '已捡' if got else '★未捡'))
print('\n== 每层汇总 ==')
for f in range(1, 11):
    print('%2dF 已捡+%d  未捡+%d  (%d 个)' % (f, tot[f][0], tot[f][1], tot[f][2]))
