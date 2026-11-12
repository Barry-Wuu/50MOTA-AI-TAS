# -*- coding: utf-8 -*-
"""Dump 41F full 16x16 terrain+obj grid and manual connectivity analysis."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"D:\B++\WorkBuddy\mota_tas_tmp2\repo\01_PC98原版_mtower")

import mota_core as M
from collections import deque

f = 41
def terr(x, y):
    return M.terrain(f, x, y)
def obj(x, y):
    return M.obj_raw(f, x, y)
def oname(o):
    return M.oname(o) if o else ''

print("=== 41F grid (terr/obj) x=0..11, y=0..11 ===")
hdr = "     " + "".join("%7d" % x for x in range(12))
print(hdr)
for y in range(12):
    row = []
    for x in range(12):
        t = terr(x, y)
        o = obj(x, y)
        s = "%d/%s" % (t, M.oname(o) if o else '-')
        row.append("%8s" % s)
    print("%3d %s" % (y, "".join(row)))

# terrain legend summary
print()
print("terrain: 0=walk 1=wall 2=?   obj: '-', 'Y'=黄门, 'B'=蓝门, 'R'=红门, digit=obj#")
