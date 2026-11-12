# -*- coding: utf-8 -*-
"""探测 V80 重排关键：0F 楼梯/金币路径 + 41F 落点 + 46F 直飞 41F 条件。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

print('=== 0F/1F 楼梯 ===')
for f in (0, 1):
    up, dn = M.stairs_of(f)
    print('%dF up=%s dn=%s  flyland=%s  STAIRS=%s' % (f, up, dn, M.FLY_LAND.get(f), M.STAIRS.get(f)))

print()
print('=== 0F 网格（.空地 #墙 ^上梯 v下梯 Y黄 B蓝 y/b钥 !物 m怪）===')
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        t = M.terrain(0, x, y)
        o = M.obj_raw(0, x, y)
        if t == 1:
            ch = '#'
        elif t == 2:
            ch = '^' if M.stair_up(0, x, y) else 'v'
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

print()
print('=== 0F(1,1) 上行梯 邻格可走性（飞行条件）===')
up, dn = M.stairs_of(0)
for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
    nx, ny = up[0]+dx, up[1]+dy
    if 1<=nx<=11 and 1<=ny<=11:
        t = M.terrain(0, nx, ny)
        o = M.obj_raw(0, nx, ny)
        print('  (%d,%d) terr=%d obj=%d %s' % (nx, ny, t, o, M.oname(o) if o else ''))

print()
print('=== 41F 落点 (6,2) 及邻格（飞行落点可站性）===')
for dx, dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
    nx, ny = 6+dx, 2+dy
    if 1<=nx<=11 and 1<=ny<=11:
        t = M.terrain(41, nx, ny)
        o = M.obj_raw(41, nx, ny)
        print('  (%d,%d) terr=%d obj=%d %s' % (nx, ny, t, o, M.oname(o) if o else ''))

print()
print('=== 41F 事件后 (6,5) 降臨の翼 邻格（事件后地形变化）===')
# 事件后：(5,6)(6,6)(7,6) 变暗墙，(5,7)(7,7) 变地板，(6,5) 生成 obj108
print('  事件后 (6,5) obj108 目标格 terr=%d' % M.terrain(41, 6, 5))
for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
    nx, ny = 6+dx, 5+dy
    if 1<=nx<=11 and 1<=ny<=11:
        t = M.terrain(41, nx, ny)
        o = M.obj_raw(41, nx, ny)
        print('  (%d,%d) terr=%d obj=%d %s' % (nx, ny, t, o, M.oname(o) if o else ''))

print()
print('=== 46F 楼梯旁（直飞 41F 条件）===')
up, dn = M.stairs_of(46)
print('46F up=%s dn=%s' % (up, dn))
for label, cell in (('up', up), ('dn', dn)):
    if cell is None:
        continue
    sx, sy = cell
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = sx+dx, sy+dy
        if 1<=nx<=11 and 1<=ny<=11:
            t = M.terrain(46, nx, ny)
            o = M.obj_raw(46, nx, ny)
            print('  %s梯(%d,%d) 邻(%d,%d) terr=%d obj=%d %s' % (label, sx, sy, nx, ny, t, o, M.oname(o) if o else ''))
