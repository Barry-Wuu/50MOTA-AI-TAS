# -*- coding: utf-8 -*-
"""精确打印指定层/区域的逐格地形+物件（避免 ASCII 对齐误读）。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

f = int(sys.argv[1])
xs = [int(v) for v in sys.argv[2].split(',')]
ys = [int(v) for v in sys.argv[3].split(',')]
for y in ys:
    for x in xs:
        t = M.terrain(f, x, y)
        o = M.obj_raw(f, x, y)
        if t == 1:
            s = '墙'
        elif t == 2:
            s = '楼梯'
        elif o == 0:
            s = '地板'
        else:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            s = 'obj%d %s %s' % (o, ty, M.oname(o)[:16])
        print('%dF(%2d,%2d) %s' % (f, x, y, s))
    print()
