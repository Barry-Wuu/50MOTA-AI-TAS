# -*- coding: utf-8 -*-
"""43F 首次访问：向下过蓝门(1,4)、过黄门(1,8) → 上 45F（攻略 §8.2 行323）"""
import sys
sys.path.insert(0, 'tools')
import run_segs as R
import mota_core as M

w = M.World.new()
w.hero.hp, w.hero.atk, w.hero.dfn, w.hero.gold = 539, 170, 137, 802
w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'] = 6, 1, 1
w.hero.items = {25, 26, 103, 107, 110}
w.hero.f, w.hero.x, w.hero.y = 43, 1, 2
w.apply_floor_events(43)

def g(x, y, lab=''):
    ok = R.goto(w, x, y, lab)
    print('  %-22s %s' % (lab, R.st(w.hero)))
    return ok

print('起点(43F入口):', R.st(w.hero))
for c in [(1,3,''),(1,4,'蓝门(1->0)'),(1,5,''),(1,6,''),(1,7,''),(1,8,'黄门(6->5)'),
          (1,9,''),(1,10,'')]:
    if not g(*c): sys.exit(1)
print('== 上 45F ==')
if not R.stair(w, 1, 11, '43F(1,11)->45F'): sys.exit(1)
print('== 进 45F ==', R.st(w.hero))
print('items:', sorted(w.hero.items))
