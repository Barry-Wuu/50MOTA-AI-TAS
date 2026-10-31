# -*- coding: utf-8 -*-
"""调试 4F 祭坛第二次献祭卡住问题：打印祭坛周边格子状态与 free 判定。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W = M.World.new()

# 直接摆好状态：模拟 run_811 v7 到祭坛入口 (6,2)
# 直接构造：把 hero 放到 4F(6,2)
h = W.hero
h.f = 4; h.x = 6; h.y = 2
h.hp = 469; h.atk = 26; h.dfn = 25; h.gold = 170
h.keys['y'] = 4; h.keys['b'] = 0; h.keys['r'] = 1

print('hero at %dF(%d,%d)' % (h.f, h.x, h.y))
for c in [(6,1), (5,1), (7,1), (6,2), (5,2), (7,2), (6,3)]:
    o = W.at(4, c[0], c[1])
    print('  (%d,%d) obj=%-3d name=%-10s type=%s' % (c[0], c[1], o, M.oname(o) if o else '-', M.TYPE.get(M.oatr(o,3),'?') if o else '-'))

# 第一次献祭：从 (6,2) 向上 move(0,-1)
print('\n-- 第一次 enter (0,-1) --')
lg = W.move(0, -1)
print('move:', lg)
print('now hero at %dF(%d,%d) A%d D%d G%d' % (h.f, h.x, h.y, h.atk, h.dfn, h.gold))
print('altar_k =', W.altar_k)

# 尝试从祭坛格离开：向下 move(0,1)
print('\n-- 尝试离开 (0,1) --')
lg = W.move(0, 1)
print('move:', lg)
print('now hero at %dF(%d,%d)' % (h.f, h.x, h.y))

# 如果已到 (6,2)，再向上第二次献祭
print('\n-- 第二次 enter (0,-1) --')
W.altar_policy = 'dfn'
lg = W.move(0, -1)
print('move:', lg)
print('now hero at %dF(%d,%d) A%d D%d G%d' % (h.f, h.x, h.y, h.atk, h.dfn, h.gold))
print('altar_k =', W.altar_k)