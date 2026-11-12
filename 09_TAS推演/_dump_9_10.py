# -*- coding: utf-8 -*-
import sys, os
TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
sys.path.insert(0, TOOLS)
import mota_core as M

def show(f):
    print('==== %dF ====' % f)
    for y in range(13):
        row = []
        for x in range(13):
            o = M.obj_raw(f, x, y)
            t = M.terrain(f, x, y)
            if t == 1:
                row.append('  # ')
            elif t == 2:
                row.append(' UP ' if M.stair_up(f, x, y) else ' DN ')
            elif o:
                nm = M.oname(o)
                row.append('%4s' % (str(o)))
            else:
                row.append('  . ')
        print('y%2d ' % y + ''.join(row))
    print('--- objects ---')
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if o:
                print('(%2d,%2d) obj%-4d %-8s %s' % (x, y, o, M.TYPE.get(M.oatr(o, 3)), M.oname(o)))
    print()

for f in (9, 10):
    show(f)
