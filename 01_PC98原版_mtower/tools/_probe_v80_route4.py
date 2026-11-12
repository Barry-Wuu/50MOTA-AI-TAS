# -*- coding: utf-8 -*-
"""确认 47F/46F 楼梯 warp 落点 + 41F/46F 飞行目标可达性。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

print('=== 47F/46F 楼梯 warp ===')
for f in (47, 46, 45, 44, 43, 42, 41):
    up, dn = M.stairs_of(f)
    for label, cell in (('up', up), ('dn', dn)):
        if cell is None:
            print('%dF %s梯 = None' % (f, label))
            continue
        w = M.warp_to(f, cell[0], cell[1])
        print('%dF %s梯(%d,%d) -> %s' % (f, label, cell[0], cell[1], w))

print()
print('=== 41F 落点 (6,2) 邻格（事件前可站性 + 到 (2,2) 路径起点）===')
for dx, dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
    nx, ny = 6+dx, 2+dy
    if 1<=nx<=11 and 1<=ny<=11:
        t = M.terrain(41, nx, ny)
        o = M.obj_raw(41, nx, ny)
        print('  (%d,%d) terr=%d obj=%d %s' % (nx, ny, t, o, M.oname(o) if o else ''))

print()
print('=== 41F 完整网格（事件前）===')
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        t = M.terrain(41, x, y)
        o = M.obj_raw(41, x, y)
        if t == 1:
            ch = '#'
        elif t == 2:
            ch = '^' if M.stair_up(41, x, y) else 'v'
        elif o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            if ty == 'MONSTER':
                ch = 'm'
            elif ty == 'DOOR':
                ch = 'Y' if o == 2 else ('B' if o == 4 else ('R' if o == 27 else 'D'))
            elif o in M.KEY_OF:
                ch = {'y': 'y', 'b': 'b', 'r': 'r'}[M.KEY_OF[o]]
            elif ty in ('ITEM', 'STATUS', 'SCORE', 'MESSAGE'):
                ch = '!'
            else:
                ch = '?'
        else:
            ch = '.'
        row.append(ch)
    print('%2d %s' % (y, ' '.join(row)))
