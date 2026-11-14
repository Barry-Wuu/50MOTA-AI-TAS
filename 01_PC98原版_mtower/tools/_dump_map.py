# -*- coding: utf-8 -*-
"""打印某层的地形/物件全表（静态 map json）。
用法: python _dump_map.py <floor>
"""
import sys, json, os, glob

SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
f = int(sys.argv[1])

# 找 map json
cands = glob.glob(SRC + '**/map*.json', recursive=True)
print('cands:', cands[:5])

import mota_core as M
w = M.World.new()
print('=== %dF terrain/obj（terrain: 1=墙 2=楼梯 0=地板）===' % f)
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        t = w.terrain_at(f, x, y)
        o = w.at(f, x, y)
        if t == 1:
            c = '#'
        elif t == 2:
            c = 'S'
        else:
            c = '.'
        if o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            nm = M.oname(o)
            c = {1: 'k', 2: 'D', 3: 'K', 4: 'd'}.get(o, None)
            if c is None:
                if ty == 'MONSTER':
                    c = 'M'
                elif ty == 'DOOR':
                    c = 'd' if o == 89 else 'D'
                elif ty == 'KEY':
                    c = 'K'
                else:
                    c = 'o'
            row.append('%s' % c)
        else:
            row.append(c)
    print('y%-2d ' % y + ' '.join(row))
print('    ' + ' '.join('x%d' % x for x in range(1, 12)))
