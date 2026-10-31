# -*- coding: utf-8 -*-
"""重放剧本段到越狱完成，然后导出【过滤后】的 1F-11F 权威状态：
   - 每层剩余物件（用 w.at()，已扣除被清掉的格）
   - 每层 ASCII 地图（带坐标尺）
   - 楼梯 / 门 / 怪物明细
不做任何寻路。
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
        print('重放失败 @row', i + 1); sys.exit(1)
    lg = w.move(*b[1])
    if lg and lg[0].startswith(FAIL):
        print('非法移动 @row', i + 1, lg); sys.exit(1)

h = w.hero
CH = {11: 'h', 12: 'H', 13: 'a', 14: 'd', 30: 'W', 35: 'D', 36: 'D', 80: 'a', 66: 'h', 76: 'H'}
MON = {'5': 's', '6': 'q', '7': 'v', '8': 'm', '9': 'c', '10': 'b',
       '16': 'A', '29': 'g', '15': 'G', '47': 'V', '45': 'S', '46': 'M', '48': 'Z'}


def ch_of(o):
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if o == 2: return 'y'
    if o == 4: return 'B'
    if o == 27: return 'R'
    if o == 1: return 'k'
    if o == 3: return 'K'
    if o == 28: return '*'
    if o == 19: return '%'
    if ty == 'MONSTER': return MON.get(str(o), 'X')
    if ty == 'STATUS': return CH.get(o, 'i')
    if ty == 'ITEM': return 'o'
    if ty == 'MESSAGE': return 'n'
    if ty == 'SAIDAN': return 'T'
    if o in (21, 23): return '?'
    if o == 20: return '.'
    if o == 79: return '~'
    if o == 89: return '#'
    if ty == 'SELL': return '$'
    if ty == 'SCORE': return 'S'
    return 'x'


out = []
out.append('=== 越狱完成局面 ===')
out.append('  %dF(%d,%d)  HP%d ATK%d DEF%d GOLD%d  黄%d 蓝%d 红%d  道具%s' % (
    h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], sorted(h.items)))
out.append('  trap_done=%s boss10=%s' % (w.trap_done, w.boss10))

for f in range(1, 12):
    out.append('')
    out.append('=' * 78)
    out.append('%dF   楼梯(up,down)=%s' % (f, M.STAIRS.get(f)))
    out.append('       0  1  2  3  4  5  6  7  8  9 10 11 12')
    for y in range(13):
        row = ''
        for x in range(13):
            t = w.terrain_at(f, x, y)
            o = w.at(f, x, y)
            if o:
                row += '  ' + ch_of(o)
            elif t == 1:
                row += '  #'
            elif t == 2:
                row += '  S'
            else:
                row += '  .'
        out.append('y%-2d  %s' % (y, row))
    out.append('--- 剩余物件(过滤后) ---')
    for y in range(13):
        for x in range(13):
            o = w.at(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            nm = M.oname(o)
            if ty == 'MONSTER':
                info = 'hp%d atk%d def%d g%d' % (M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13))
            elif ty in ('STATUS', 'ITEM'):
                info = 'HP+%d ATK+%d DEF+%d' % (M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12))
            elif o in (2, 4, 27):
                info = '门(%s)' % {2: '黄', 4: '蓝', 27: '红'}[o]
            elif o == 19:
                info = '监狱栅栏'
            else:
                info = ''
            out.append('  (%2d,%2d) obj%-3d %-8s %-9s %s' % (x, y, o, ty, nm[:9], info))

txt = '\n'.join(out)
io.open(DED + 'state_after_escape_filtered.txt', 'w', encoding='utf-8').write(txt)
print(txt[:4000])
print('...\n已写 state_after_escape_filtered.txt')
