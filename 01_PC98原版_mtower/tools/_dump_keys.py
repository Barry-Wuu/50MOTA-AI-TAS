# -*- coding: utf-8 -*-
"""Dump yellow/blue/red keys on floors 31F-34F to find cheap extra keys."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

for f in (31, 32, 33, 34):
    print('=== %dF KEYS ===' % f)
    for y in range(1, 12):
        for x in range(1, 12):
            o = M.obj_raw(f, x, y)
            if o in M.KEY_OF:
                col = M.KEY_OF[o]
                print('  (%2d,%2d) %s  %s' % (x, y, {'y': '黄钥', 'b': '蓝钥', 'r': '红钥'}[col], M.oname(o)))
print('--- done ---')
