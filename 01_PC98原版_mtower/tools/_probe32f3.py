# -*- coding: utf-8 -*-
"""BFS walkability on 32F lower-left pocket to confirm key pickups (1,7)(2,7)(3,7)(4,7)(4,8) reachable from row 11."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
from collections import deque

def enterable(f, x, y):
    """Mimic engine: walkable if not wall terrain and not altar-side."""
    if M.terrain(f, x, y) == 1:
        return False
    o = M.obj_raw(f, x, y)
    if o in M.ALTAR_SIDE:
        return False
    return True

# BFS from 32F(6,11) (floor entrance near stairs)
start = (6, 11)
targets = {(1,7),(2,7),(3,7),(4,7),(4,8)}
seen = {start}
q = deque([start])
prev = {}
while q:
    x, y = q.popleft()
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x+dx, y+dy
        if not (1 <= nx <= 11 and 1 <= ny <= 11):
            continue
        if (nx, ny) in seen or not enterable(32, nx, ny):
            continue
        seen.add((nx, ny))
        prev[(nx, ny)] = (x, y)
        q.append((nx, ny))

print('=== 32F reachable set from (6,11) ===')
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        if (x, y) in seen:
            row.append('R' if (x,y) in targets else 'o')
        else:
            row.append('.')
    print(' %2d %s' % (y, ' '.join(row)))
print('    ' + ' '.join('%X' % x for x in range(1, 12)))

print()
print('Targets reachable:', {t: (t in seen) for t in targets})
for t in sorted(targets):
    if t in seen:
        path = []
        cur = t
        while cur != start:
            path.append(cur)
            cur = prev[cur]
        path.append(start)
        print('  path to %s: %s' % (t, ' '.join('(%d,%d)'%p for p in reversed(path))))
print('--- done ---')
