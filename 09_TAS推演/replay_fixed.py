# -*- coding: utf-8 -*-
"""用修正后的 mota_core（2F 栅栏门不可穿）重放 1F→21F 路线。

2F 初段（越狱）改为合法路径：只能走盗贼挖的洞 (2,7) 出去。
不依赖录制态里的 HP（因为 2F 三瓶蓝药已不可得，HP 会整体下移 600），
但仍用 ATK/DEF/GOLD/钥匙 作为方向判别，按目标格推进，观察真实 HP 与首个暴毙点。
"""
import sys, csv, io
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/魔塔1_route_1F到21F.csv'
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
FAIL_PREFIX = ('blocked', '打不动', '无', '买不起', '熔岩烫死', '打不过')

rows = list(csv.DictReader(io.open(SRC, encoding='utf-8')))

# 合法 2F 越狱路径（落点 (4,8) 起）：洞在 (2,7)，只能从这里出去
LEGAL_2F = [(4, 7), (3, 7), (2, 7), (1, 7), (1, 8), (1, 9), (1, 10)]

w = M.World.new()
dead = None
floor_entry = {}


def go_row(r):
    global w, dead
    tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
    rec = dict(hp=int(r['hp']), atk=int(r['atk']), dfn=int(r['def']), gold=int(r['gold']),
               ky=int(r['ky']), kb=int(r['kb']), kr=int(r['kr']))
    h = w.hero
    same = (h.f, h.x, h.y) == (tf, tx, ty)
    best = None
    for d in DIRS:
        c = w.clone()
        lg = c.move(*d)
        if lg and lg[0].startswith(FAIL_PREFIX):
            continue
        hh = c.hero
        sc = 0
        if (hh.f, hh.x, hh.y) == (tf, tx, ty):
            sc += 4
        elif same and (hh.f, hh.x, hh.y) == (h.f, h.x, h.y) and lg:
            sc += 2
        else:
            continue
        for k, cur in (('atk', hh.atk), ('dfn', hh.dfn), ('gold', hh.gold)):
            if cur == rec[k]:
                sc += 1
        for k, kk in (('ky', 'y'), ('kb', 'b'), ('kr', 'r')):
            if hh.keys.get(kk, 0) == rec[k]:
                sc += 1
        if bool(lg) == bool((r['event'] or '').strip()):
            sc += 1
        if best is None or sc > best[0]:
            best = (sc, c, lg)
    if best is None:
        return None
    sc, c, lg = best
    if c.hero.hp <= 0:
        dead = (c.hero.f, c.hero.x, c.hero.y, lg)
    w = c
    return lg


def run(i, label):
    r = rows[i]
    res = go_row(r)
    if res is None:
        print('BLOCKED row', i + 1, r['floor'], r['x'], r['y'], repr(r['event']),
              '| pos', (w.hero.f, w.hero.x, w.hero.y), 'hp', w.hero.hp)
        return False
    if w.hero.f not in floor_entry:
        floor_entry[w.hero.f] = (w.hero.hp, w.hero.atk, w.hero.dfn, dict(w.hero.keys), i + 1)
        print('enter %2dF row%-4d hp=%-5d atk=%-4d def=%-4d keys=%s' %
              (w.hero.f, i + 1, w.hero.hp, w.hero.atk, w.hero.dfn, dict(w.hero.keys)))
    if dead:
        print('DEAD row', i + 1, 'pos', dead[:3], dead[3])
        print('  recorded hp', r['hp'], ' actual before-death', w.hero.hp)
        return False
    return True


# 1F→2F 首次到达（行 1..42）
for i in range(42):
    if not run(i, 'pre'):
        sys.exit(1)

print('drop ->', (w.hero.f, w.hero.x, w.hero.y), 'hp', w.hero.hp)

# 2F 合法越狱
for (x, y) in LEGAL_2F:
    h = w.hero
    ok = False
    for d in DIRS:
        c = w.clone()
        lg = c.move(*d)
        if (c.hero.f, c.hero.x, c.hero.y) == (2, x, y):
            w = c
            ok = True
            break
    print('  2F -> (%d,%d) %s hp=%d' % (x, y, 'ok' if ok else 'FAIL', w.hero.hp))
    if not ok:
        sys.exit(1)

# 3F 起（行 68 = idx 67）
for i in range(67, len(rows)):
    if not run(i, 'post'):
        break

print('--- floor entries ---')
for f in sorted(floor_entry):
    print('%2dF' % f, floor_entry[f])
print('final', (w.hero.f, w.hero.x, w.hero.y), 'hp', w.hero.hp, 'atk', w.hero.atk,
      'def', w.hero.dfn, 'gold', w.hero.gold, 'keys', dict(w.hero.keys))
