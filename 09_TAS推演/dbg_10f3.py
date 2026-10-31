# -*- coding: utf-8 -*-
"""检查 10F 关键格 terrain_at / at，找出 (4,6) 为何不可达。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W = M.World.new()

print('10F 关键格 terrain(1=墙,2=楼梯) / obj:')
for c in [(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),(11,6),
          (3,6),(2,6),(1,6),(4,5),(4,7),(10,5),(10,7),(11,5),(11,7),
          (4,4),(8,4),(4,8),(8,8),(6,9),(6,11)]:
    t = W.terrain_at(10, c[0], c[1])
    o = W.at(10, c[0], c[1])
    print('  (%2d,%2d) terrain=%d obj=%d' % (c[0], c[1], t, o))

# 打印 10F terrain 全图
print('\n10F terrain 图 (1=墙, 2=楼梯):')
for x in range(13):
    row = []
    for y in range(13):
        t = W.terrain_at(10, x, y)
        row.append('#' if t == 1 else ('S' if t == 2 else '.'))
    print('%2d %s' % (x, ' '.join(row)))