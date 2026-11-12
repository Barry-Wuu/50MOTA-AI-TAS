# -*- coding: utf-8 -*-
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import manual
import mota_core as M

manual.execute(manual.PLAN, verbose=False)
W = manual.W
print('当前', manual.st())
for f in range(1, 12):
    items = []
    for y in range(1, 12):
        for x in range(1, 12):
            o = W.at(f, x, y)
            if o and (f, x, y) not in W.cleared:
                items.append((x, y, o, M.TYPE.get(M.oatr(o, 3), '?')))
    print('--- %dF 剩余 %d ---' % (f, len(items)))
    for (x, y, o, ty) in items:
        print('  (%2d,%2d) obj=%-3d %-8s %s' % (x, y, o, ty, manual.info(o)[:44]))
