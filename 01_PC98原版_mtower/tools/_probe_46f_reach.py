# -*- coding: utf-8 -*-
"""46F 连通性分析：从各入口 BFS，看哪些怪可达、路径怎么走。
46F 是左右对称层（obj149 提示）。用静态 obj_raw 数据 + WARP 楼梯做 BFS。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

F = 46

def passable(x, y):
    if not (1 <= x <= 11 and 1 <= y <= 11):
        return False
    if M.terrain(F, x, y) == 1:
        return False
    return True

def cell(x, y):
    o = M.obj_raw(F, x, y)
    if not o:
        return '.'
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if o in M.KEY_OF:
        return {'y': 'y', 'b': 'b', 'r': 'r'}[M.KEY_OF[o]]
    if o in M.DOOR_OF:
        return {'y': 'Y', 'b': 'B', 'r': 'R'}[M.DOOR_OF[o]]
    if ty == 'MONSTER':
        return 'm'
    if ty in ('ITEM', 'STATUS'):
        return '!'
    return '?'

def bfs(start, doors_open=()):
    """BFS from start, opening doors in doors_open (treat as passable). Return reachable set."""
    from collections import deque
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if not passable(nx, ny):
                continue
            o = M.obj_raw(F, nx, ny)
            if o and M.TYPE.get(M.oatr(o, 3), '?') == 'DOOR':
                col = M.DOOR_OF.get(o)
                if col not in doors_open:
                    continue
            if (nx, ny) in seen:
                continue
            seen.add((nx, ny))
            q.append((nx, ny))
    return seen

def dump_reach(reach, label):
    print('==== %s（%d 格）====' % (label, len(reach)))
    for y in range(1, 12):
        row = []
        for x in range(1, 12):
            if (x, y) in reach:
                row.append(cell(x, y))
            else:
                row.append('·')
        print('y=%2d: %s' % (y, ' '.join(row)))
    print()

# 起点：右上区 (11,10)（46F 上行梯落点旁）
print('楼梯：46F up=(11,11)->47F(10,11); dn=(11,1)->45F(10,1)')
print('46F 静态网格（x1-11, y1-11）:')
for y in range(1, 12):
    print('y=%2d: %s' % (y, ' '.join(cell(x, y) for x in range(1, 12))))
print()

# 从右上区 (11,10) 出发，不开任何门
r1 = bfs((11, 10), ())
dump_reach(r1, '右上区(11,10) 不开门')

# 从右上区出发，只开黄门
r2 = bfs((11, 10), ('y',))
dump_reach(r2, '右上区(11,10) 开黄门')

# 从右上区出发，开黄+蓝门
r3 = bfs((11, 10), ('y', 'b'))
dump_reach(r3, '右上区(11,10) 开黄+蓝')

# 从蓝门(6,11) 西侧进入：起点 (5,11)
r4 = bfs((5, 11), ('y',))
dump_reach(r4, '左下区(5,11)入口 开黄门')

# 从黄门(9,11) 西侧：起点 (8,11)
r5 = bfs((8, 11), ('y',))
dump_reach(r5, '底行(8,11) 开黄门')
