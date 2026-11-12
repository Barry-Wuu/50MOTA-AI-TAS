# -*- coding: utf-8 -*-
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

for f in [47, 48]:
    print('=' * 70)
    print('%dF up=%s down=%s' % (f, M.STAIRS[f][0], M.STAIRS[f][1]))
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            t = M.terrain(f, x, y)
            if o:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                print('  (%2d,%2d) t=%d obj%-3d %-10s %s' % (x, y, t, o, M.oname(o)[:10], ty))
            elif t == 1:
                pass
    print()
