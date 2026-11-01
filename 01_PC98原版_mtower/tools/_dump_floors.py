# -*- coding: utf-8 -*-
"""Diagnostic: dump floor layouts (terrain + object id/type/name) for given floors."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

FLOORS = [36, 37, 38, 39, 40, 12, 7, 15, 41]

# monster attribute cols: 10=hp,11=atk,12=def
def mstat(o):
    return (M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12))

for f in FLOORS:
    print('=' * 60)
    print('FLOOR %d   STAIRS(up,dn)=%s   FLY_LAND=%s' % (f, M.STAIRS.get(f), M.FLY_LAND.get(f)))
    print('-' * 60)
    # header
    hdr = 'y\\x ' + ''.join('%3d' % x for x in range(1, 12))
    print(hdr)
    for y in range(1, 12):
        row = []
        for x in range(1, 12):
            t = M.terrain(f, x, y)
            o = M.obj_raw(f, x, y)
            # terrain 1=wall,2=stair (mota_core convention); but map json uses 3=wall/1=floor
            if t == 2:
                cell = 'S'
            elif t == 1:
                cell = '#'
            else:
                cell = '.'
            row.append((x, y, o, M.TYPE.get(M.oatr(o, 3)) if o else None, M.oname(o), t))
        # print compact: terrain char + obj id
        line = '%2d  ' % y
        for (x, y, o, ty, nm, t) in row:
            if t == 2:
                line += 'S  '
            elif t == 1:
                line += '#  '
            elif o == 0:
                line += '.  '
            else:
                line += '%-3d' % o
        print(line)
    # list objects
    print('  objects:')
    for y in range(1, 12):
        for x in range(1, 12):
            o = M.obj_raw(f, x, y)
            if o == 0:
                continue
            t = M.terrain(f, x, y)
            if t == 2:
                continue
            ty = M.TYPE.get(M.oatr(o, 3))
            extra = ''
            if ty == 'MONSTER':
                extra = ' hp/atk/def=%s' % (mstat(o),)
            elif ty == 'DOOR':
                extra = ' col=%s' % M.DOOR_OF.get(o)
            elif ty == 'KEY':
                extra = ' col=%s' % M.KEY_OF.get(o)
            elif ty in ('SELL', 'BUY'):
                extra = ' price=%s grant=%s' % (M.SHOP_PRICE.get(o), M.SHOP_GRANT.get(o))
            print('    (%2d,%2d) obj%-3d %-8s %s%s' % (x, y, o, ty, M.oname(o), extra))
    print()
