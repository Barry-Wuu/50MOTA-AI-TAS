# -*- coding: utf-8 -*-
"""42F 首次访问：只取右上区钥匙（避开(10,8)夹击），看魔法穿行伤害"""
import sys
sys.path.insert(0, 'tools')
import run_segs as R
import mota_core as M

w = M.World.new()
w.hero.hp, w.hero.atk, w.hero.dfn, w.hero.gold = 1239, 170, 137, 802
w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'] = 2, 0, 1
w.hero.items = {25, 26, 103, 107, 110}
w.hero.f, w.hero.x, w.hero.y = 42, 6, 10
w.apply_floor_events(42)

def g(x, y, lab=''):
    ok = R.goto(w, x, y, lab)
    print('  %-16s -> %s %s' % (lab, 'OK' if ok else 'FAIL', R.st(w.hero)))
    return ok

print('起点:', R.st(w.hero))
for c in [(6,9,''),(6,8,''),(6,7,''),(6,6,''),(6,5,'')]:
    if not g(*c): sys.exit(1)
if not g(7,5,''): sys.exit(1)
if not g(8,5,'黄门(2->1)'): sys.exit(1)
if not g(9,5,'(邻(9,4)魔術師Ｂ)'): sys.exit(1)
if not g(10,5,''): sys.exit(1)
if not g(10,4,'(邻(9,4)B+(11,4)A)'): sys.exit(1)
if not g(10,3,''): sys.exit(1)
if not g(10,2,'拾黄钥'): sys.exit(1)
if not g(10,1,'拾蓝钥'): sys.exit(1)
for c in [(9,1,'拾黄钥'),(11,1,'拾黄钥'),(9,2,'拾黄钥'),(11,2,'拾黄钥')]:
    if not g(*c): sys.exit(1)
print('== 右上区取完，回程 ==')
for c in [(10,1,'回'),(10,2,''),(10,3,''),(10,4,'(再邻双魔術師)'),(10,5,'')]:
    if not g(*c): sys.exit(1)
print('== 昇華の翼 → 楼梯 → 43F ==')
if not R.wing_up(w, '昇華の翼'): sys.exit(1)
print('  wing_up:', R.st(w.hero))
if not R.stair(w, 1, 1, '42F(1,1)->43F'): sys.exit(1)
print('== 进 43F ==', R.st(w.hero))
print('items:', sorted(w.hero.items))
