# -*- coding: utf-8 -*-
import mota_core as M
f = 34
# 结合 terrain + object，用 ASCII 表达
sym = {}
for y in range(1, 12):
    row = 'y%2d ' % y
    for x in range(1, 12):
        t = M.terrain(f, x, y)
        o = M.obj_raw(f, x, y)
        if t == 1:
            c = '#'   # 墙
        elif t == 2:
            c = 'S'   # 楼梯
        elif o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            mp = {'MONSTER': 'M', 'DOOR': 'D', 'STATUS': 'P', 'ITEM': 'P', 'KEY': 'K', 'SELL': '$',
                  'SAIDAN': 'A', 'MESSAGE': 'N', 'NORMAL': '.', 'SCORE': 'N'}.get(ty, '?')
            c = mp
        else:
            c = '.'
        row += c
    print(row)
