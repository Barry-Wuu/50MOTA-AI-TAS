# -*- coding: utf-8 -*-
"""Dump 31F,32F,33F full static layout."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

for f in (31, 32, 33):
    print('=== %dF ===' % f)
    for y in range(1, 12):
        row = []
        for x in range(1, 12):
            o = M.obj_raw(f, x, y)
            t = M.terrain(f, x, y)
            ch = '#' if t == 1 else '.'
            if o:
                if o in M.KEY_OF:
                    ch = {'y': 'y', 'b': 'b', 'r': 'r'}[M.KEY_OF[o]]
                elif o in M.DOOR_OF:
                    ch = {'y': 'Y', 'b': 'B', 'r': 'R'}[M.DOOR_OF[o]]
                else:
                    ty = M.TYPE.get(M.oatr(o, 3), '?')
                    ch = {'MONSTER': 'm', 'ITEM': '!', 'STATUS': '+', 'MESSAGE': '?'}.get(ty, '?')
            row.append(ch)
        print(' %2d %s' % (y, ' '.join(row)))
    print('    ' + ' '.join('%X' % x for x in range(1, 12)))
    # stairs
    print('  STAIRS:', M.STAIRS.get(f))
    print()
print('--- done ---')
