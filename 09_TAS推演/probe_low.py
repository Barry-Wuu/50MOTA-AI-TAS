# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
w = M.World.new()
for f in [1, 3, 4, 5, 6]:
    print('==== %dF 物件 ====' % f)
    for y in range(13):
        row = []
        for x in range(13):
            o = w.at(f, x, y)
            t = w.terrain_at(f, x, y)
            if t == 1: row.append('##')
            elif t == 2: row.append('SS')
            elif o == 0: row.append('..')
            else: row.append('%2d' % o)
        print('%3d ' % y + ' '.join(row))
    print()
print('==== 楼梯 ====')
for f in range(1, 12):
    pts = [(x,y) for y in range(13) for x in range(13) if w.terrain_at(f,x,y)==2]
    if pts: print('%dF: %s' % (f, pts))
