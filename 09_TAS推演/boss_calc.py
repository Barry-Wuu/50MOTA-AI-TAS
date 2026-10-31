# -*- coding: utf-8 -*-
"""实算 10F BOSS+路径小怪战损。"""
import sys, math
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

def fight_loss(atk, dfn, o):
    hp, a, d = M.oatr(o,10), M.oatr(o,11), M.oatr(o,12)
    my_dmg = max(atk - d, 1)
    r = math.ceil(hp / my_dmg)
    return r * max(a - dfn, 1), r

def boss_total(atk, dfn):
    # 10F 路径小怪：骷髅C(1,6), 骷髅B(2,7), 骷髅B(4,11), BOSS(6,3)
    tot = 0
    for o, nm in [(9,'骷髅C'), (10,'骷髅B'), (10,'骷髅B'), (16,'BOSS')]:
        l, r = fight_loss(atk, dfn, o)
        tot += l
    return tot

for atk in range(21, 28):
    for dfn in range(21, 27):
        t = boss_total(atk, dfn)
        mark = ' <<<' if t <= 534 else ''
        print('A%d/D%d 10F战损=%d%s' % (atk, dfn, t, mark))
