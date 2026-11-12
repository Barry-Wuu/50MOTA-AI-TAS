# -*- coding: utf-8 -*-
"""探明 46F→41F 楼梯链 + 46F 魔法钥匙入口路径 + 41F 事件路径。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
from collections import deque

print('=== 41F-46F 楼梯表 ===')
for f in range(41, 47):
    up, dn = M.stairs_of(f)
    print('%dF up=%s dn=%s  flyland=%s' % (f, up, dn, M.FLY_LAND.get(f)))

def passable(f, x, y, doors=('y','b')):
    if not (1 <= x <= 11 and 1 <= y <= 11):
        return False
    if M.terrain(f, x, y) == 1:
        return False
    o = M.obj_raw(f, x, y)
    if o and M.TYPE.get(M.oatr(o, 3), '?') == 'DOOR':
        col = M.DOOR_OF.get(o)
        if col not in doors:
            return False
    return True

def bfs(f, start, doors=('y','b')):
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if not passable(f, nx, ny, doors):
                continue
            if (nx, ny) in dist:
                continue
            dist[(nx, ny)] = dist[(x, y)] + 1
            q.append((nx, ny))
    return dist

print()
print('=== 46F 从落点(11,10) 开黄+蓝 BFS 到魔法钥匙(3,8) ===')
d = bfs(46, (11, 10))
target = (3, 8)
print('魔法钥匙(3,8) 距离:', d.get(target, '不可达'))
print('魔法钥匙(3,8) 邻居:')
for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
    nx, ny = target[0]+dx, target[1]+dy
    if 1<=nx<=11 and 1<=ny<=11:
        o = M.obj_raw(46, nx, ny)
        t = M.terrain(46, nx, ny)
        print('  (%d,%d) terr=%d obj=%d name=%s' % (nx, ny, t, o, M.oname(o) if o else ''))

print()
print('=== 46F 关键门/墙检查（魔法钥匙(3,8) 区域）===')
for y in range(7, 10):
    for x in range(2, 8):
        t = M.terrain(46, x, y)
        o = M.obj_raw(46, x, y)
        if t == 1:
            ch = '#'
        elif o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            ch = 'm' if ty=='MONSTER' else ('B' if o==4 else ('Y' if o==2 else '?'))
        else:
            ch = '.'
        print('  ', end='')
    print()

# 重构 46F 网格
print()
print('=== 46F 网格（Y黄/B蓝/x钥/m怪/!物品）===')
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        t = M.terrain(46, x, y)
        o = M.obj_raw(46, x, y)
        if t == 1:
            ch = '#'
        elif t == 2:
            ch = '^' if M.stair_up(46, x, y) else 'v'
        elif o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            if ty == 'MONSTER':
                ch = 'm'
            elif ty == 'DOOR':
                ch = 'Y' if o == 2 else ('B' if o == 4 else 'D')
            elif o in M.KEY_OF:
                ch = {'y':'y','b':'b','r':'r'}[M.KEY_OF[o]]
            elif ty == 'ITEM':
                ch = '!'
            elif ty == 'STATUS':
                ch = '+'
            elif ty == 'MESSAGE':
                ch = '?'
            else:
                ch = '?'
        else:
            ch = '.'
        row.append(ch)
    print('%2d %s' % (y, ' '.join(row)))

print()
print('=== 41F 事件路径检查：杀(2,2)→撞(10,2)→杀埋伏 → 得(6,5)降臨の翼 ===')
print('41F(2,2) 魔術師Ａ 邻格:')
for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
    nx, ny = 2+dx, 2+dy
    o = M.obj_raw(41, nx, ny)
    print('  (%d,%d) obj=%d %s' % (nx, ny, o, M.oname(o) if o else ''))
print('41F(10,2) 暗墙 obj89? 当前 obj=%d' % M.obj_raw(41, 10, 2))
print('41F(6,5) 目标降臨の翼格 当前 obj=%d' % M.obj_raw(41, 6, 5))
print('41F 上行梯(6,11) 下行梯(6,1)')
print('41F(6,5) 邻格:')
for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
    nx, ny = 6+dx, 5+dy
    t = M.terrain(41, nx, ny)
    o = M.obj_raw(41, nx, ny)
    print('  (%d,%d) terr=%d obj=%d %s' % (nx, ny, t, o, M.oname(o) if o else ''))
