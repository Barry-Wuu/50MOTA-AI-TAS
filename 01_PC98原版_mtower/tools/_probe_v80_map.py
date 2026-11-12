# -*- coding: utf-8 -*-
"""转储 47F/46F 完整网格（地形+物件），用于设计 V80 挣钱路径。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

for f in [47, 46]:
    print('=' * 76)
    print('%dF up=%s down=%s' % (f, M.STAIRS[f][0], M.STAIRS[f][1]))
    print('   ' + ' '.join('%X' % x for x in range(13)))
    for y in range(13):
        row = []
        for x in range(13):
            t = M.terrain(f, x, y)
            o = M.obj_raw(f, x, y)
            if t == 1:
                ch = '#'
            elif t == 2:
                ch = '^' if M.stair_up(f, x, y) else 'v'
            elif o:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if ty == 'MONSTER':
                    ch = 'm'
                elif ty == 'DOOR':
                    ch = 'Y' if o == 2 else ('B' if o == 4 else ('R' if o == 27 else 'D'))
                elif o in M.KEY_OF:
                    ch = {'y': 'y', 'b': 'b', 'r': 'r'}[M.KEY_OF[o]]
                elif ty in ('SELL', 'BUY'):
                    ch = '$'
                elif ty == 'ITEM':
                    ch = '!'
                elif ty == 'STATUS':
                    ch = '+'
                else:
                    ch = '?'
            else:
                ch = '.'
            row.append(ch)
        print('%2d %s' % (y, ' '.join(row)))
    print()
