# -*- coding: utf-8 -*-
"""引擎实测：BOSS 后 10F 是否能把 (2,6)(10,6)(11,11) 三个战利品收齐。
模拟 v7 BOSS 后状态（hero 在 10F(6,3)），用 W.move 实际走。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W = M.World.new()
h = W.hero
h.f = 10; h.x = 6; h.y = 3
h.hp = 247; h.atk = 26; h.dfn = 45; h.gold = 172
h.keys['y'] = 0; h.keys['b'] = 0; h.keys['r'] = 0
W.boss10 = True
W.cleared.add((10, 6, 3))      # BOSS 已死
# 红门 (6,9) 已开（v7 中 enter 开门会 cleared）
# 黄门 (1,9)(3,9) 已开
W.cleared.add((10, 6, 9))
W.cleared.add((10, 1, 9))
W.cleared.add((10, 3, 9))

def mv(dx, dy):
    lg = W.move(dx, dy)
    print('  move(%d,%d) -> %s' % (dx, dy, lg if lg else '(空)'))
    return lg

def st():
    return 'HP%d A%d D%d G%d 钥%d/%d/%d %dF(%d,%d)' % (
        h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y)

print('起点: ' + st())

# 路径1：从 BOSS (6,3) 先拿 (2,6) 蓝晶
print('\n== 阶段1: BOSS(6,3) -> (2,6) 蓝晶 ==')
# 手动路线：(6,3)->(6,4)->(6,5)->(6,6)->(6,7)->(6,8)->(6,9)红门->(6,10)->(6,11)->(5,11)->(4,11)僧侣->(3,11)->(3,10)->(3,9)->(3,8)->(2,8)->(2,7)->(2,6)
path1 = [(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(-1,0),(0,-1)]
# 重新想：(6,3) 到 (6,9) 是向下 6 步到 (6,9)？y 从 3 到 9 是 +6
# (6,3)->(6,9): move(0,1)x6 到 (6,9) 红门
# 红门后 (6,10),(6,11): move(0,1)x2 到 (6,11)
# 然后 (-1,0) 到 (5,11),(4,11)僧侣,(3,11),(2,11)? 看地图 (2,11) 是地板
# 从 (2,11) 北上 (2,10),(2,9),(2,8),(2,7),(2,6)
print('-- 试走 (6,3) -> (6,9) --')
for _ in range(6):
    mv(0, 1)
print('到 (6,9): ' + st())
mv(0, 1); print('到 (6,10): ' + st())
mv(0, 1); print('到 (6,11): ' + st())
mv(-1, 0); print('到 (5,11): ' + st())
mv(-1, 0); print('到 (4,11) 僧侣: ' + st())
mv(-1, 0); print('到 (3,11): ' + st())
mv(-1, 0); print('到 (2,11): ' + st())
mv(0, -1); print('到 (2,10): ' + st())
mv(0, -1); print('到 (2,9): ' + st())
mv(0, -1); print('到 (2,8): ' + st())
mv(0, -1); print('到 (2,7): ' + st())
mv(0, -1); print('到 (2,6) 蓝晶: ' + st())

# 路径2：从 (2,6) 到 (10,6) 红晶 + (11,11) 蓝药
print('\n== 阶段2: (2,6) -> 底部走廊 -> (10,6) -> (11,11) ==')
# (2,6) 原路返回 (2,11) 再往东 (6,11)(7,11)(8,11)(9,11) 北上
for _ in range(5):
    mv(0, 1)
print('到 (2,11): ' + st())
for _ in range(4):
    mv(1, 0)
print('到 (6,11): ' + st())
mv(1, 0); print('到 (7,11): ' + st())
mv(1, 0); print('到 (8,11) 僧侣: ' + st())
mv(1, 0); print('到 (9,11): ' + st())
mv(0, -1); print('到 (9,10): ' + st())
mv(0, -1); print('到 (9,9): ' + st())
mv(0, -1); print('到 (9,8): ' + st())
mv(0, -1); print('到 (9,7): ' + st())
mv(0, -1); print('到 (9,6) 骷髅C: ' + st())
mv(1, 0); print('到 (10,6) 红晶: ' + st())
mv(1, 0); print('到 (11,6) 骷髅C: ' + st())
mv(0, 1); print('到 (11,7): ' + st())
mv(0, 1); print('到 (11,8): ' + st())
mv(0, 1); print('到 (11,9): ' + st())
mv(0, 1); print('到 (11,10): ' + st())
mv(0, 1); print('到 (11,11) 蓝药: ' + st())

print('\n最终: ' + st())