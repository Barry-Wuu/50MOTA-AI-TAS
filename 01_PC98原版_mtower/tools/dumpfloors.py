#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dumpfloors.py —— 把指定楼层打印成可读网格，标注物件/墙/熔岩/祭坛/楼梯。"""
import sys
import mota_core as M

WALL = '▓'  # 墙 terrain==1
UNK = '·'

def short(o):
    if o == 0:
        return '  '
    t = M.TYPE.get(M.oatr(o, 3), '?')
    nm = M.oname(o)
    # 用物件id + 首2字
    return '%s' % (nm[:2] if nm else ('#' + str(o)))

def dump(f):
    print('==== %dF ====' % f)
    # 顶栏 x
    line = '    ' + ''.join('%2d' % x for x in range(1, 12)) + '   (x\\y)'
    print(line)
    for y in range(1, 12):
        cells = []
        for x in range(1, 12):
            if M.terrain(f, x, y) == 1:
                cells.append('██')
                continue
            o = M.obj_raw(f, x, y)
            if o == 0:
                cells.append('  ')
                continue
            t = M.TYPE.get(M.oatr(o, 3), '?')
            nm = M.oname(o)[:2]
            if o == 79:
                cells.append('熔')
            elif t == 'SAIDAN':
                cells.append('坛')
            elif t == 'STAIR' or M.stair_up(f, x, y):
                cells.append('梯')
            elif t == 'MONSTER':
                cells.append('怪')
            elif t == 'DOOR':
                cells.append('门')
            elif o == 89:
                cells.append('暗')
            else:
                cells.append(nm if nm else ('#' + str(o)))
        print('%2d  ' % y + ''.join('%2s' % c for c in cells) + '  %2d' % y)
    print()

for f in (11, 12, 13):
    dump(f)
