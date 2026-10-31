# -*- coding: utf-8 -*-
"""手工驱动「1F→3F落点→触发扒装→越狱」固定脚本，产出越狱态世界。"""
import sys, time
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import route_build as RB

t = time.time()
# 1) trap_mode='avoid' 到达 3F 落点（不踩中央 (5,9)）
r = RB.plan2(lambda f, x, y: f == 3, goal_cell=(3, 2, 11), max_states=200000, trap_mode='avoid')
if not r or (isinstance(r, tuple) and r[0] == 'cap'):
    print('到3F落点失败:', r); sys.exit()
w, path = r
h = w.hero
print('已到 3F(%d,%d) HP%d A%d D%d G%d (%.1fs)' % (h.x, h.y, h.hp, h.atk, h.dfn, h.gold, time.time()-t))
# 记录到落点的动作序列（后续拼成总路径）
seg1 = path

# 2) 切回 apply 模式，手工踩 (5,10)→(5,9) 触发扒装
w.trap_mode = 'apply'
# 从落点 (2,11) 到 (5,10)：左下口袋直走 (2,11)->(3,11)->(4,11)->(5,11)->(5,10)
moves = []
for (a, b) in [(3,11),(4,11),(5,11),(5,10),(5,9)]:
    dx, dy = a - h.x, b - h.y
    lg = w.move(dx, dy)
    moves.append((dx, dy))
    if lg and any(t in lg[0] for t in ('blocked','打不动','打不过','无黄','无蓝','无红')):
        print('  触发扒装路径卡在 ->%dF(%d,%d): %s' % (h.f, a, b, lg[:1])); sys.exit()
h = w.hero
print('触发扒装后: %dF(%d,%d) HP%d A%d D%d G%d' % (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold))
seg2 = moves

# 3) 越狱：(4,8)->(3,7)盗贼->(2,7)凿开->(1,7)->(1,8)->(1,9)->(1,10)
esc = [(3,7),(2,7),(1,7),(1,8),(1,9),(1,10)]
for (a, b) in esc:
    dx, dy = a - h.x, b - h.y
    lg = w.move(dx, dy)
    if lg and any(t in lg[0] for t in ('blocked','打不动','打不过','无黄','无蓝','无红')):
        print('  越狱卡在 ->2F(%d,%d): %s' % (a, b, lg[:1])); sys.exit()
h = w.hero
print('越狱后: %dF(%d,%d) HP%d A%d D%d G%d' % (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold))
