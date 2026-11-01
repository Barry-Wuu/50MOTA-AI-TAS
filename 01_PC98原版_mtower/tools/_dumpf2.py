# -*- coding: utf-8 -*-
import sys, mota_core as M
f = int(sys.argv[1]) if len(sys.argv) > 1 else 40
sym = {}
print('=== %dF ===' % f)
for y in range(1, 12):
    row = 'y%2d ' % y
    for x in range(1, 12):
        t = M.terrain(f, x, y)
        o = M.obj_raw(f, x, y)
        if t == 1:
            c = '#'
        elif t == 2:
            c = 'S'
        elif o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            c = {'MONSTER': 'M', 'DOOR': 'D', 'STATUS': 'P', 'ITEM': 'P', 'KEY': 'K', 'SELL': '$',
                 'SAIDAN': 'A', 'MESSAGE': 'N', 'NORMAL': '.', 'SCORE': 'N'}.get(ty, '?')
        else:
            c = '.'
        row += c
    print(row)
print('--- 对象 ---')
for y in range(1, 12):
    for x in range(1, 12):
        o = M.obj_raw(f, x, y)
        if o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            print('(%2d,%2d) obj%-3d %-9s hp%-5s atk%-5s def%-5s g%-5s %s' % (
                x, y, o, ty, M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13), M.oname(o)[:34]))
