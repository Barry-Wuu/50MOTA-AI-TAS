# -*- coding: utf-8 -*-
"""Deep-probe 32F(2,9) object to ensure it's a safe walkable cell."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

for (x, y) in [(2,9),(2,8),(2,10),(4,8),(2,7),(1,7),(3,7),(4,7),(6,11),(6,10)]:
    o = M.obj_raw(32, x, y)
    print('(%2d,%2d) obj=%r oname=%r oattr=%r terrain=%d' % (x, y, o, M.oname(o), [M.oatr(o,c) for c in range(1,9)], M.terrain(32,x,y)))

# Check walkability via the same logic the engine uses
print()
print('--- walkability check (blocking if obj present and not pickupable) ---')
for (x, y) in [(2,9),(2,8),(2,10),(2,11),(6,11),(6,10),(2,7),(4,8)]:
    o = M.obj_raw(32, x, y)
    # mimic: is cell enterable? terrain floor + (no obj or obj is pickup)
    print('(%2d,%2d) terrain=%d obj=%r -> enterable=%s' % (
        x, y, M.terrain(32,x,y), o, M.terrain(32,x,y)==0 and (not o or M.TYPE.get(M.oatr(o,3)) in ('KEY','ITEM','STATUS','MESSAGE') or M.TYPE.get(M.oatr(o,3)) is None)))
print('--- done ---')
