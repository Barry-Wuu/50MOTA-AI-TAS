# -*- coding: utf-8 -*-
"""复用 path.bfs_advance：从 BOSS(6,3) 到 (2,6) 的路径是什么？再到 (10,6)(11,11)。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import path as P
import mota_core as M

W = P.W
h = W.hero
h.f = 10; h.x = 6; h.y = 3
h.hp = 247; h.atk = 26; h.dfn = 45; h.gold = 172
h.keys['y'] = 0; h.keys['b'] = 0; h.keys['r'] = 0
W.boss10 = True
W.cleared.add((10, 6, 3))
W.cleared.add((10, 6, 9))
W.cleared.add((10, 1, 9))
W.cleared.add((10, 3, 9))

print('起点: %s' % P.st())

for goal, nm in [((2,6),'蓝晶'), ((10,6),'红晶'), ((11,11),'蓝药'), ((6,10),'楼梯邻格'), ((6,11),'楼梯')]:
    p = P.bfs_advance(10, (h.x, h.y), goal)
    if p:
        # 打印路径
        cx, cy = h.x, h.y
        path_desc = []
        for d in p:
            cx += d[0]; cy += d[1]
            o = W.at(10, cx, cy)
            path_desc.append('(%d,%d)%s' % (cx, cy, 'o%d'%o if o else ''))
        print('到 %s %s: 可达 len=%d\n   %s' % (nm, goal, len(p), ' -> '.join(path_desc)))
    else:
        print('到 %s %s: 不可达' % (nm, goal))

# 如果 (2,6) 可达，执行一遍并继续测 (10,6)
p = P.bfs_advance(10, (h.x, h.y), (2, 6))
if p:
    for d in p:
        W.move(*d)
    print('\n已走到 (2,6): %s' % P.st())
    for goal, nm in [((10,6),'红晶'), ((11,11),'蓝药')]:
        p2 = P.bfs_advance(10, (h.x, h.y), goal)
        if p2:
            cx, cy = h.x, h.y
            desc = []
            for d in p2:
                cx += d[0]; cy += d[1]
                o = W.at(10, cx, cy)
                desc.append('(%d,%d)%s' % (cx, cy, 'o%d'%o if o else ''))
            print('从 (2,6) 到 %s %s: 可达 len=%d\n   %s' % (nm, goal, len(p2), ' -> '.join(desc)))
        else:
            print('从 (2,6) 到 %s %s: 不可达' % (nm, goal))