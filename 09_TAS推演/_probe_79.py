# -*- coding: utf-8 -*-
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import manual
import mota_core as M

manual.execute(manual.PLAN, verbose=False)
W = manual.W
print('当前', manual.st())
for f in (7, 9):
    print('--- %dF 剩余物件 ---' % f)
    for y in range(1, 12):
        for x in range(1, 12):
            o = W.at(f, x, y)
            if o and (f, x, y) not in W.cleared:
                print('  (%2d,%2d) obj=%-3d %-8s %s' % (x, y, o, M.TYPE.get(M.oatr(o, 3), '?'), manual.info(o)[:46]))
