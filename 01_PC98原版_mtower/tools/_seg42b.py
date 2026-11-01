# -*- coding: utf-8 -*-
"""42F 段②诊断：从 (6,10) 过 (8,5) 黄门打 2初级巫师+2魔法警卫，看战损"""
import sys
sys.path.insert(0, 'tools')
import run_segs as R
import mota_core as M

w = M.World.new()
w.hero.hp, w.hero.atk, w.hero.dfn, w.hero.gold = 1189, 170, 137, 780
w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'] = 2, 0, 1
w.hero.items = {25, 26, 103, 107, 110}
w.hero.f, w.hero.x, w.hero.y = 42, 6, 10
w.apply_floor_events(42)

def g(x, y, lab=''):
    ok = R.goto(w, x, y, lab)
    print('  ->', 'OK' if ok else 'FAIL', R.st(w.hero))
    return ok

print('起点:', R.st(w.hero))
# 剧情清场区上行
for c in [(6,9,''),(6,8,''),(6,7,''),(6,6,''),(6,5,'')]:
    if not g(*c): sys.exit(1)
if not g(7,5,''): sys.exit(1)
if not g(8,5,'黄门'): sys.exit(1)   # 黄2→1
if not g(9,5,''): sys.exit(1)
if not g(9,4,'初级巫师魔術師Ｂ#1'): sys.exit(1)
if not g(9,5,'回'): sys.exit(1)
if not g(10,5,''): sys.exit(1)
if not g(11,5,''): sys.exit(1)
if not g(11,6,'初级巫师魔術師Ｂ#2'): sys.exit(1)
if not g(11,5,'回'): sys.exit(1)
if not g(10,5,''): sys.exit(1)
if not g(10,6,''): sys.exit(1)
if not g(10,7,''): sys.exit(1)
if not g(10,8,''): sys.exit(1)
if not g(9,8,'魔法警卫魔導師#1'): sys.exit(1)
if not g(10,8,'回'): sys.exit(1)
if not g(11,8,'魔法警卫魔導師#2'): sys.exit(1)
print('最终:', R.st(w.hero))
