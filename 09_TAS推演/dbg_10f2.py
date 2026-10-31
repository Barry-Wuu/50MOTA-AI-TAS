# -*- coding: utf-8 -*-
"""调试：v7 BOSS 后 hero 在 10F(2,6)，为何 (10,6) 和 (11,11) 不可达？"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import path as P
import mota_core as M

W = P.W
h = W.hero

# 模拟 v7 BOSS 后状态：hero 在 10F(2,6)
h.f = 10; h.x = 2; h.y = 6
h.hp = 247; h.atk = 26; h.dfn = 46; h.gold = 178
h.keys['y'] = 0; h.keys['b'] = 0; h.keys['r'] = 0
W.boss10 = True
W.cleared.add((10, 6, 3))
W.cleared.add((10, 6, 9))
W.cleared.add((10, 1, 9))
W.cleared.add((10, 3, 9))
W.cleared.add((10, 2, 6))   # 蓝晶已捡

print('hero: %s' % P.st())

for goal in [(10, 6), (11, 11), (6, 11), (6, 10)]:
    p = P.bfs_advance(10, (h.x, h.y), goal)
    print('到 %s: %s' % (goal, '可达 len=%d' % len(p) if p else '不可达'))

# 逐格分析从 (2,6) 到 (10,6) 的所有 4 邻 move_cost
print('\n从 (2,6) 的 4 邻 move_cost:')
for d in [(1,0),(-1,0),(0,1),(0,-1)]:
    nx, ny = 2+d[0], 6+d[1]
    if 0 <= nx < 13 and 0 <= ny < 13:
        loss, kused, ok = P.move_cost((2,6), d)
        o = W.at(10, nx, ny)
        print('  move(%2d,%2d) -> (%d,%d) obj=%d loss=%d key=%d ok=%s' % (d[0], d[1], nx, ny, o, loss, kused, ok))

# 打印 10F 从 (2,6) 出发的 bfs_advance 可达格
dist = {}
prev = {}
import heapq
hp0 = h.hp
dist[(2,6)] = 0
pq = [(0, 0, (2,6))]
cum = {(2,6): 0}
while pq:
    cst, sp, c = heapq.heappop(pq)
    if cst != dist.get(c): continue
    for d in [(1,0),(-1,0),(0,1),(0,-1)]:
        n = (c[0]+d[0], c[1]+d[1])
        if not (0 <= n[0] < 13 and 0 <= n[1] < 13): continue
        loss, kused, ok = P.move_cost(c, d)
        if not ok: continue
        ncum = cum[c] + loss
        if ncum >= hp0: continue
        nc = cst + loss + 100*kused
        if n not in dist or nc < dist[n]:
            dist[n] = nc; cum[n] = ncum; prev[n] = (c, d)
            heapq.heappush(pq, (nc, sp+1, n))
print('\n从 (2,6) bfs_advance 可达 %d 格:' % len(dist))
for x in range(13):
    row = ['(%2d,%2d)' % c for c in sorted(dist) if c[0] == x]
    if row:
        print('  x=%2d: %s' % (x, ' '.join(row)))
print('包含 (10,6)?', (10,6) in dist, ' (11,11)?', (11,11) in dist)