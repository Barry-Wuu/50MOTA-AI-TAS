# -*- coding: utf-8 -*-
"""精确打印某层地形/物件（3 字符一格，避免手工解析错位）。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W = M.World.new()
f = int(sys.argv[1])
print('     ' + ''.join('%3d' % x for x in range(1, 12)))
for y in range(1, 12):
    row = '%3d  ' % y
    for x in range(1, 12):
        t = W.terrain_at(f, x, y)
        o = W.at(f, x, y)
        if t == 2:
            ch = 'ST'
        elif t == 1:
            ch = '##'
        elif not o:
            ch = '..'
        else:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            ch = {'DOOR': 'DD', 'MONSTER': 'MM', 'KEY': 'KK', 'ITEM': 'II',
                  'STATUS': 'SS', 'SELL': '$', 'SAIDAN': 'AT', 'MESSAGE': 'TT',
                  'NORMAL': 'NN', 'SCORE': 'CC'}.get(ty, '??')
        row += '%3s' % ch
    print(row)
print('stairs up/dn:', M.STAIRS.get(f))
