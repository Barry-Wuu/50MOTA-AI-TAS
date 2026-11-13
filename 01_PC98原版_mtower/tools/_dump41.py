# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
f = 41
print("    " + "".join("%5d" % x for x in range(12)))
for y in range(12):
    row = []
    for x in range(12):
        t = M.terrain(f, x, y)
        o = M.obj_raw(f, x, y)
        row.append("%5s" % ("%d/%d" % (t, o)))
    print("%3d %s" % (y, "".join(row)))
