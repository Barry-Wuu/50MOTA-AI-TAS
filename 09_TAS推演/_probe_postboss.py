# -*- coding: utf-8 -*-
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import manual

manual.execute(manual.PLAN, verbose=False)
h = manual.W.hero
print('终态', manual.st())
print('boss10=', getattr(manual.W, 'boss10', None))
cells = [(3, 3), (4, 3), (5, 3), (7, 3), (8, 3), (9, 3), (4, 4), (8, 4), (6, 3), (6, 4), (6, 7), (6, 11)]
for (x, y) in cells:
    o = manual.W.at(10, x, y)
    print('10F(%2d,%2d) obj=%-4s %s' % (x, y, o, manual.info(o) if o else ''))
