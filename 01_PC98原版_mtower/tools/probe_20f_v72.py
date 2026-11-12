# -*- coding: utf-8 -*-
"""V72 规划探针：跑完 V71 后检查 20F 右下口袋与 42F 的关键格状态。"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M
import z2_route

rc = z2_route.main()
print('main rc =', rc)
import run_segs
w = run_segs.LAST_W

for f, cells in [
    (20, [(11, 9), (11, 10), (11, 11), (10, 10), (10, 11), (9, 10), (9, 11),
          (1, 11), (10, 4), (11, 4), (1, 9), (6, 3), (6, 1), (10, 9)]),
    (42, [(1, 1), (6, 11), (6, 10), (9, 8), (11, 8), (9, 4), (11, 4), (11, 6),
          (10, 8), (10, 9), (10, 10), (9, 10), (10, 7), (8, 7)]),
]:
    print('--- %dF ---' % f)
    for (x, y) in cells:
        o = w.at(f, x, y)
        name = M.oname(o) if o else ''
        ty = M.TYPE.get(M.oatr(o, 3), '-') if o else '-'
        print('  (%2d,%2d) static=%-4d live=%-4d ter=%d cleared=%-5s %-9s %s' % (
            x, y, M.obj_raw(f, x, y), o, w.terrain_at(f, x, y),
            (f, x, y) in w.cleared, ty, name[:30]))
