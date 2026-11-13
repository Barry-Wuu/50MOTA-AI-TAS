# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
for f in (40,41,42,43,47):
    print('%dF STAIRS(up,down)=%s' % (f, M.STAIRS[f]))
    for y in range(13):
        for x in range(13):
            if M.terrain(f,x,y)==2:
                w = M.warp_to(f,x,y)
                print('   stair(%d,%d) %s -> %s' % (x,y,'UP' if M.stair_up(f,x,y) else 'DN', w))
