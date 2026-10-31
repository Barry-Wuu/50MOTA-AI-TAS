# -*- coding: utf-8 -*-
"""重新生成 1F→9F 合法段 CSV（修复越狱斜穿为合法 4 方向）。
复用 manual 的前奏+PLAN，不跑 plan2（用户要求手工排路线）。"""
import sys, csv, io
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import manual

moves = list(manual.PREAMBLE_MOVES)
_orig = manual.W.move
def rec(dx, dy):
    lg = _orig(dx, dy)
    moves.append((dx, dy))
    return lg
manual.W.move = rec
manual.execute(verbose=False)
h = manual.W.hero
print('PLAN 后: %dF(%d,%d) HP%d A%d D%d G%d 钥%d/%d/%d 步%d' % (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
      h.keys['y'], h.keys['b'], h.keys['r'], len(moves)))

out = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/魔塔1_route_1F到9F_合法.csv'
wc = M.World.new()
rows = [dict(step=0, floor=wc.hero.f, x=wc.hero.x, y=wc.hero.y, hp=wc.hero.hp,
             atk=wc.hero.atk, dfn=wc.hero.dfn, gold=wc.hero.gold,
             ky=wc.hero.keys['y'], kb=wc.hero.keys['b'], kr=wc.hero.keys['r'],
             event='', dir='')]
for i, (dx, dy) in enumerate(moves):
    lg = wc.move(dx, dy)
    rows.append(dict(step=i + 1, floor=wc.hero.f, x=wc.hero.x, y=wc.hero.y, hp=wc.hero.hp,
                     atk=wc.hero.atk, dfn=wc.hero.dfn, gold=wc.hero.gold,
                     ky=wc.hero.keys['y'], kb=wc.hero.keys['b'], kr=wc.hero.keys['r'],
                     event=';'.join(lg)[:80], dir='%d,%d' % (dx, dy)))
with io.open(out, 'w', encoding='utf-8-sig', newline='') as fp:
    w2 = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
    w2.writeheader(); w2.writerows(rows)
print('已存 %s（%d 行）' % (out, len(rows)))