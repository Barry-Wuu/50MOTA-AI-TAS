# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
w = M.World.new()

for f in [7, 9, 11]:
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

print('==== 楼梯信息 ====')
for f in range(1, 12):
    pts = []
    for y in range(13):
        for x in range(13):
            if w.terrain_at(f, x, y) == 2:
                pts.append((x, y))
    if pts:
        print('%dF: %s' % (f, pts))

print('==== 涉及怪物属性 ====')
for o in sorted({5,6,7,8,9,10,16,29,40,41,42,43,44,45}):
    nm = M.oname(o)[:14]
    print('obj%-3d %-4s %-14s hp=%s atk=%s def=%s gold=%s' % (o, M.TYPE.get(M.oatr(o,3),'?'), nm, M.oatr(o,10), M.oatr(o,11), M.oatr(o,12), M.oatr(o,13)))
