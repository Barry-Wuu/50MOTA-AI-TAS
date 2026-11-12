# -*- coding: utf-8 -*-
"""Probe 32F cells along the candidate lower-left pocket access path."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

cells = [
    (6,11), (5,11), (4,11), (3,11), (2,11),   # row 11 approach
    (2,10),                                    # up column x=2
    (2,9),                                     # message cell - KEY question
    (2,8), (2,7), (1,7), (3,7), (4,7), (4,8),  # lower-left pocket
]
for (x, y) in cells:
    o = M.obj_raw(32, x, y)
    t = M.terrain(32, x, y)
    ty = M.TYPE.get(M.oatr(o, 3), '?') if o else '-'
    atk = M.oatr(o, 4) if o else '-'
    print('(%2d,%2d) obj=%s terrain=%s type=%s atk=%s' % (x, y, M.oname(o), t, ty, atk))

# Also show any monster adjacent to the path
print()
print('--- monsters near row11/col2 path ---')
for (x, y) in [(8,11),(1,10),(3,10),(2,9)]:
    o = M.obj_raw(32, x, y)
    ty = M.TYPE.get(M.oatr(o, 3), '?') if o else '-'
    if ty == 'MONSTER':
        print('(%2d,%2d) %s atk=%d def=%d hp=%d gold=%d' % (x, y, M.oname(o), M.oatr(o,4), M.oatr(o,5), M.oatr(o,6), M.oatr(o,7)))
print('--- done ---')
