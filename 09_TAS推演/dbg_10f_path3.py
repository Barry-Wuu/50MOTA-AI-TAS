# -*- coding: utf-8 -*-
"""检查 (6,10)->(7,10)->(7,11)->(8,11)->(9,11)->(9,6)->(10,6) 路径为何 bfs 不可达。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import path as P
import mota_core as M

W = P.W
h = W.hero
h.f = 10; h.x = 6; h.y = 10
h.hp = 247; h.atk = 26; h.dfn = 45; h.gold = 172
h.keys['y'] = 0; h.keys['b'] = 0; h.keys['r'] = 0
W.boss10 = True
W.cleared.add((10, 6, 3))
W.cleared.add((10, 6, 9))
W.cleared.add((10, 1, 9))
W.cleared.add((10, 3, 9))

print('hero: %s' % P.st())

# 路径关键格 terrain/obj
print('\n路径关键格:')
for c in [(6,10),(7,10),(7,11),(8,11),(9,11),(9,10),(9,9),(9,8),(9,7),(9,6),(10,6),(11,6),(11,7),(11,8),(11,9),(11,10),(11,11)]:
    t = W.terrain_at(10, c[0], c[1])
    o = W.at(10, c[0], c[1])
    print('  (%2d,%2d) terrain=%d obj=%d %s' % (c[0], c[1], t, o, M.oname(o) if o else ''))

# 逐段 move_cost
print('\n逐段 move_cost:')
path = [(6,10),(7,10),(7,11),(8,11),(9,11),(9,10),(9,9),(9,8),(9,7),(9,6),(10,6),(11,6),(11,7),(11,8),(11,9),(11,10),(11,11)]
for i in range(len(path)-1):
    cur = path[i]
    nxt = path[i+1]
    d = (nxt[0]-cur[0], nxt[1]-cur[1])
    loss, kused, ok = P.move_cost(cur, d)
    o = W.at(10, nxt[0], nxt[1])
    print('  %s -> %s move(%d,%d): loss=%d key=%d ok=%s obj=%d' % (cur, nxt, d[0], d[1], loss, kused, ok, o))

# 从 (6,10) bfs 到 (10,6)
print('\nbfs_advance (6,10)->(10,6):')
p = P.bfs_advance(10, (6,10), (10,6))
print('  结果:', p if p else '不可达')