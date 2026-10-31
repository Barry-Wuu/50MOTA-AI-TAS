# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

w = M.World.new()
print('2F terrain/obj grid (x=1..11, y=1..11)')
print('    ' + ''.join('%4d' % x for x in range(1, 12)))
for y in range(1, 12):
    line = '%3d ' % y
    for x in range(1, 12):
        t = w.terrain_at(2, x, y)
        o = w.at(2, x, y)
        if t == 1:
            s = 'W'
        elif t == 2:
            s = 'S'
        elif o:
            s = str(o)
        else:
            s = '.'
        line += '%4s' % s
    print(line)
print()
for y in range(1, 12):
    for x in range(1, 12):
        o = w.at(2, x, y)
        if o:
            print('(%d,%d) obj%d %s type=%s' % (x, y, o, M.oname(o), M.TYPE.get(M.oatr(o, 3))))
