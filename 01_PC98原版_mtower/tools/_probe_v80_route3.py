# -*- coding: utf-8 -*-
"""确认 0F/1F warp 落点 + 0F 金币格可站性 + 1F 飞行条件。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

print('=== 0F/1F 楼梯 warp ===')
for f in (0, 1):
    up, dn = M.stairs_of(f)
    for label, cell in (('up', up), ('dn', dn)):
        if cell is None:
            continue
        w = M.warp_to(f, cell[0], cell[1])
        print('%dF %s梯(%d,%d) -> %s' % (f, label, cell[0], cell[1], w))

print()
print('=== 0F(1,1) 上行梯踩上后落点（WARP）===')
print('WARP[0,1,1] =', M.WARP.get((0, 1, 1)))
print('WARP[1,1,1] =', M.WARP.get((1, 1, 1)))

print()
print('=== 0F 金币 obj113 (6,6) 邻格可走 ===')
for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
    nx, ny = 6+dx, 6+dy
    if 1<=nx<=11 and 1<=ny<=11:
        t = M.terrain(0, nx, ny)
        o = M.obj_raw(0, nx, ny)
        print('  (%d,%d) terr=%d obj=%d %s' % (nx, ny, t, o, M.oname(o) if o else ''))

print()
print('=== 1F 楼梯旁（飞行条件）===')
up, dn = M.stairs_of(1)
for label, cell in (('up', up), ('dn', dn)):
    if cell is None:
        continue
    sx, sy = cell
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = sx+dx, sy+dy
        if 1<=nx<=11 and 1<=ny<=11:
            t = M.terrain(1, nx, ny)
            o = M.obj_raw(1, nx, ny)
            print('  %s梯(%d,%d) 邻(%d,%d) terr=%d obj=%d %s' % (label, sx, sy, nx, ny, t, o, M.oname(o) if o else ''))
