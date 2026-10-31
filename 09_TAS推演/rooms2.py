# -*- coding: utf-8 -*-
"""静态连通块分析（不做寻路）：
  passable = 非墙/非门/非怪/非栅栏/非熔岩/非祭坛侧格（拾取格算可走）
  把每层切分成若干"房间块"，并列出每块的：
    · 内含物件（药/晶/钥/道具/NPC/祭坛/商店）
    · 边界关口（门/怪，带坐标与四维）
用法: python rooms2.py [楼层...]  默认 4..9
"""
import sys, io, csv
from collections import deque

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
sys.path.insert(0, TOOLS)
import mota_core as M

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
rows_rec = list(csv.DictReader(io.open(SRC + '魔塔1_route_1F到21F.csv', encoding='utf-8-sig')))
W = M.World.new()


def pick_move(r):
    tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
    rec = dict(atk=int(r['atk']), dfn=int(r['def']), gold=int(r['gold']),
               ky=int(r['ky']), kb=int(r['kb']), kr=int(r['kr']))
    h = W.hero
    same = (h.f, h.x, h.y) == (tf, tx, ty)
    best = None
    for d in DIRS:
        c = W.clone(); lg = c.move(*d)
        if lg and lg[0].startswith(('blocked', '打不动', '打不过', '无', '买不起', '熔岩烫死', '祭坛金币不足')): continue
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
    W.move(*pick_move(rows_rec[i])[1])


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


def moninfo(o):
    return '%s(%d/%d/%d)' % (M.oname(o)[:6], M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12))


def analyze(f):
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
        items = []
        for (x, y) in comp:
            o = W.at(f, x, y)
            if o:
                items.append('(%d,%d)%s' % (x, y, moninfo(o) if M.TYPE.get(M.oatr(o, 3)) == 'MONSTER' else M.oname(o)[:8] + '#' + str(o)))
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
                if ty == 'DOOR':
                    s = '门(%d,%d)obj%d' % (n[0], n[1], o)
                elif ty == 'MONSTER':
                    s = '怪(%d,%d)%s' % (n[0], n[1], moninfo(o))
                else:
                    continue
                if s not in bd:
                    bd.append(s)
        print('  块#%d  %d格  物件: %s' % (k, len(comp), '; '.join(items) if items else '-'))
        print('      关口: %s' % ('; '.join(bd) if bd else '-'))


floors = [int(a) for a in sys.argv[1:]] or list(range(4, 10))
for f in floors:
    analyze(f)
