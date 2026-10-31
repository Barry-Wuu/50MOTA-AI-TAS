# -*- coding: utf-8 -*-
"""调试 10F BOSS 后战利品可达性：打印 10F 地图、可达格、贴边关口。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W = M.World.new()

# 模拟 BOSS 后状态：hero 在 10F(6,3)，BOSS 已击败
h = W.hero
h.f = 10; h.x = 6; h.y = 3
h.hp = 247; h.atk = 26; h.dfn = 45; h.gold = 172
h.keys['y'] = 0; h.keys['b'] = 0; h.keys['r'] = 0
# 标记 BOSS 已击败、红门已开（(10,6,9) obj27 cleared）
W.boss10 = True
W.cleared.add((10, 6, 3))          # BOSS 格
# 红门 (6,9) 已开：manual.goto 开门时 cleared 会加吗？手动加
W.cleared.add((10, 6, 9))          # 红门已开
# 黄门 (1,9)(3,9) 已开
W.cleared.add((10, 1, 9))
W.cleared.add((10, 3, 9))

# 打印 10F 地图
print('10F 地图 (x=0..12 列, y=0..12 行):')
print('   y: ' + ' '.join('%2d' % y for y in range(13)))
for x in range(13):
    row = []
    for y in range(13):
        o = W.at(10, x, y)
        if o == 0:
            row.append(' .')
        elif o in (2, 4, 27):
            row.append(' D')
        elif o in (1, 3, 28):
            row.append(' K')
        elif o == 89:
            row.append(' W')
        elif o == 22:
            row.append(' A')
        elif o == 16:
            row.append(' B')
        else:
            row.append('%2d' % o)
    print('%2d %s' % (x, ' '.join(row)))

# 检查关键格
for c in [(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(6,11),
          (2,6),(10,6),(11,11),(1,9),(3,9),(2,8),(4,11)]:
    o = W.at(10, c[0], c[1])
    print('  (%d,%d) obj=%d' % (c[0], c[1], o))

# 可达性 BFS（从 (6,3) 出发，用 free 判定）
from collections import deque
def free(f, x, y):
    if not (0 <= x < 13 and 0 <= y < 13):
        return False
    t = W.terrain_at(f, x, y)
    if t == 1 or t == 2:
        return False
    o = W.at(f, x, y)
    if o == 0:
        return True
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if o in M.KEY_OF:
        return True
    if ty in ('STATUS', 'ITEM'):
        return True
    if ty in ('NORMAL', 'SCORE', 'MESSAGE'):
        return True
    return False

start = (6, 3)
seen = {start}
q = deque([start])
while q:
    c = q.popleft()
    for d in [(1,0),(-1,0),(0,1),(0,-1)]:
        n = (c[0]+d[0], c[1]+d[1])
        if n in seen:
            continue
        if free(10, n[0], n[1]):
            seen.add(n)
            q.append(n)
print('\n从 (6,3) 可达 %d 格:' % len(seen))
for x in range(13):
    print('  ' + ' '.join('(%2d,%2d)' % c for c in sorted(seen) if c[0]==x))
print('包含:', ' (2,6)' if (2,6) in seen else ' (2,6)✗', ' (10,6)' if (10,6) in seen else ' (10,6)✗', ' (11,11)' if (11,11) in seen else ' (11,11)✗')