# -*- coding: utf-8 -*-
"""导出 17F 网格 + 物件清单（静态，不含运行态清场）。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W = M.World.new()
f = int(sys.argv[1]) if len(sys.argv) > 1 else 17

print('    ' + ''.join('%2d' % x for x in range(1, 12)))
for y in range(1, 12):
    row = '%2d  ' % y
    for x in range(1, 12):
        t = W.terrain_at(f, x, y)
        o = W.at(f, x, y)
        if t in (1, 2):
            ch = '##'
        elif o == 0:
            ch = ' .'
        else:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            mp = {'DOOR': 'D', 'MONSTER': 'M', 'KEY': 'K', 'ITEM': 'I',
                  'STATUS': 'S', 'SELL': '$', 'SAIDAN': 'A', 'MESSAGE': 'T',
                  'NORMAL': '.', 'SCORE': 'C'}
            ch = ' ' + mp.get(ty, '?')
        row += ch
    print(row)

print('\n--- %dF 物件 ---' % f)
for y in range(1, 12):
    for x in range(1, 12):
        o = W.at(f, x, y)
        if o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            extra = ''
            if ty == 'MONSTER':
                extra = ' hp=%d atk=%d def=%d g=%d' % (
                    M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13))
            print('(%2d,%2d) obj%-4d %-10s %s%s' % (x, y, o, ty, M.oname(o)[:18], extra))
print('\n楼梯:', M.STAIRS.get(f))
