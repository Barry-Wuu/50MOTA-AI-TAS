# -*- coding: utf-8 -*-
"""清晰网格：每格 4 字符，行首 5 字符。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W = M.World.new()
f = int(sys.argv[1])
up, dn = M.STAIRS.get(f, (None, None))

print('     ' + ''.join(('%4d' % x) for x in range(1, 12)))
for y in range(1, 12):
    row = '%3d  ' % y
    for x in range(1, 12):
        t = W.terrain_at(f, x, y)
        o = W.at(f, x, y)
        if t in (1, 2):
            ch = ' ## '
        elif (x, y) == up:
            ch = ' UU '
        elif (x, y) == dn:
            ch = ' DN '
        elif not o:
            ch = '  . '
        else:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            ch = '  ' + {'DOOR': 'd', 'MONSTER': 'M', 'KEY': 'k', 'ITEM': 'I',
                         'STATUS': 's', 'SELL': '$', 'SAIDAN': 'A', 'MESSAGE': 'T',
                         'NORMAL': '.', 'SCORE': 'C', 'BUY': 'b'}.get(ty, '?') + ' '
        row += ch
    print(row + ' %2d' % y)
