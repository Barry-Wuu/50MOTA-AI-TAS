# -*- coding: utf-8 -*-
"""只做两件事：
  1) 重放固定剧本段（1F起手→3F扒装→2F牢房→越狱），得到真实局面；
  2) 打印 1F-11F 剩余物件与简单连通性（不做任何路线搜索）。
"""
import sys, io, csv

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
DED = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/'
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
        c = w.clone()
        lg = c.move(*d)
        if lg and lg[0].startswith(FAIL):
            continue
        hh = c.hero
        sc = 0
        if (hh.f, hh.x, hh.y) == (tf, tx, ty):
            sc += 8
        elif same and (hh.f, hh.x, hh.y) == (h.f, h.x, h.y) and lg:
            sc += 4
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
            best = (sc, d)
    return best


for i in list(range(0, 42)) + list(range(60, 67)):
    b = pick_move(rows_rec[i])
    if b is None:
        print('重放失败 @row', i + 1)
        sys.exit(1)
    lg = w.move(*b[1])
    if lg and lg[0].startswith(FAIL):
        print('非法移动 @row', i + 1, lg)
        sys.exit(1)

h = w.hero
print('=== 越狱完成局面 ===')
print('  %dF(%d,%d)  HP%d ATK%d DEF%d GOLD%d  黄%d 蓝%d 红%d' % (
    h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r']))

out = []
out.append('=== 越狱完成局面 ===')
out.append('  %dF(%d,%d)  HP%d ATK%d DEF%d GOLD%d  黄%d 蓝%d 红%d' % (
    h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r']))
out.append('  道具: %s' % sorted(h.items))

CH = {11: 'h', 12: 'H', 13: 'a', 14: 'd', 30: 'W', 35: 'D', 36: 'D', 80: 'a', 66: 'h', 76: 'H'}
for f in range(1, 12):
    out.append('')
    out.append('=' * 72)
    out.append('%dF  up/down=%s' % (f, M.STAIRS.get(f)))
    out.append('       0  1  2  3  4  5  6  7  8  9 10 11 12')
    for y in range(13):
        row = ''
        for x in range(13):
            t = w.terrain_at(f, x, y)
            o = w.at(f, x, y)
            if o:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if o == 2:
                    ch = 'y'
                elif o == 4:
                    ch = 'b'
                elif o == 27:
                    ch = 'r'
                elif o == 1:
                    ch = 'k'
                elif o == 3:
                    ch = 'K'
                elif o == 28:
                    ch = 'R'
                elif ty == 'MONSTER':
                    ch = {'5': 's', '6': 'q', '7': 'v', '8': 'm', '9': 'c', '10': 'b',
                          '16': 'A', '29': 'g', '15': 'G', '47': 'V', '45': 'S',
                          '46': 'M', '48': 'Z'}.get(str(o), 'X')
                elif ty == 'STATUS':
                    ch = CH.get(o, 'i')
                elif ty == 'ITEM':
                    ch = 'o'
                elif ty == 'MESSAGE':
                    ch = 'n'
                elif ty == 'SAIDAN':
                    ch = 'T'
                elif ty == 'SELL':
                    ch = '$'
                elif o == 19:
                    ch = '%'
                else:
                    ch = '?'
            else:
                ch = {0: '.', 1: '#', 2: 'S'}.get(t, '?')
            row += '%3s' % ch
        out.append('y%-3d%s' % (y, row))
    out.append('--- 剩余物件 ---')
    for y in range(13):
        for x in range(13):
            o = w.at(f, x, y)
            if o:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                tag = ''
                if ty == 'MONSTER':
                    tag = 'hp%d atk%d def%d g%d' % (M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13))
                elif ty == 'STATUS':
                    tag = 'HP+%d ATK+%d DEF+%d' % (M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12))
                out.append('  (%2d,%2d) obj%-4d %-12s %-8s %s' % (x, y, o, M.oname(o)[:12], ty, tag))

io.open(DED + 'state_after_escape.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('written state_after_escape.txt')
