# -*- coding: utf-8 -*-
"""46F 首访：下 18F 拿血瓶(2,4) → 回 46F → 下穿 3 黄门 → 上 47F（攻略 §8.2 行325）"""
import sys
sys.path.insert(0, 'tools')
import run_segs as R
import mota_core as M

w = M.World.new()
w.hero.hp, w.hero.atk, w.hero.dfn, w.hero.gold = 539, 170, 137, 802
w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'] = 5, 0, 1
w.hero.items = {25, 26, 103, 107, 110}
w.hero.f, w.hero.x, w.hero.y = 46, 11, 2
w.apply_floor_events(46)
# 11F→20F 段已开 18F(4,1) 蓝门（run_segs 762 行「18F 蓝门(4,1)」），并已清右侧怪/取右侧钥
w.cleared.add((18, 4, 1))
for c in [(18,8,1),(18,9,1),(18,9,4),(18,10,2),(18,11,1),(18,11,2),(18,11,3),(18,11,4),(18,11,5)]:
    w.cleared.add(c)

def g(x, y, lab=''):
    ok = R.goto(w, x, y, lab)
    print('  %-24s %s' % (lab, R.st(w.hero)))
    return ok

print('起点(46F入口):', R.st(w.hero))
print('== 飞 18F ==')
if not R.fly(w, 18, '46F->18F'): sys.exit(1)
print('  落点:', R.st(w.hero))
# 左上过黄门(1,3)拿血瓶(2,4)
for c in [(5,2,''),(5,1,''),(4,1,'蓝门(已开)'),(3,1,''),(2,1,''),(2,2,''),(1,2,''),
          (1,3,'黄门(5->4)'),(1,4,''),(2,4,'血瓶obj66+100')]:
    if not g(*c): sys.exit(1)
print('== 回楼梯(6,2) → 飞回 46F ==')
for c in [(1,4,''),(1,3,'(已开)'),(1,2,''),(2,2,''),(2,1,''),(3,1,''),(4,1,'(已开)'),(5,1,''),(5,2,''),(6,2,'回(6,1下梯旁)')]:
    if not g(*c): sys.exit(1)
if not R.fly(w, 46, '18F->46F'): sys.exit(1)
print('  回 46F:', R.st(w.hero))
print('== 46F 下穿 3 黄门 ==')
for c in [(11,3,'黄门1(4->3)'),(11,4,''),(11,5,'黄门2(3->2)'),(11,6,''),(11,7,''),
          (11,8,'黄门3(2->1)'),(11,9,'邻(10,9)魔術師Ｂ -100'),(11,10,'')]:
    if not g(*c): sys.exit(1)
print('== 上 47F ==')
if not R.stair(w, 11, 11, '46F(11,11)->47F'): sys.exit(1)
print('== 进 47F ==', R.st(w.hero))
print('items:', sorted(w.hero.items))
