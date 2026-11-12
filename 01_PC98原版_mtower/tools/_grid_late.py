# -*- coding: utf-8 -*-
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

SYM = {1: 'y', 2: 'Y', 3: 'b', 4: 'B', 27: 'R', 28: 'r'}
for f in [47, 48, 49, 25, 26, 24, 50]:
    print('=' * 60)
    print('%dF  up=%s down=%s' % (f, M.STAIRS[f][0], M.STAIRS[f][1]))
    print('    ' + ''.join('%d' % (x % 10) for x in range(13)))
    for y in range(13):
        row = ''
        for x in range(13):
            t = M.terrain(f, x, y)
            o = M.obj_raw(f, x, y)
            if o:
                if o in SYM:
                    row += SYM[o]
                else:
                    ty = M.TYPE.get(M.oatr(o, 3), '?')
                    if ty == 'DOOR':
                        row += 'D'
                    elif ty == 'MONSTER':
                        row += 'M'
                    elif ty == 'KEY':
                        row += 'k'
                    elif ty in ('STATUS', 'ITEM'):
                        row += '$'
                    else:
                        row += 'o'
            elif t == 1:
                row += '#'
            elif t == 2:
                row += 'S'
            else:
                row += '.'
        print('%3d %s' % (y, row))
    print()
