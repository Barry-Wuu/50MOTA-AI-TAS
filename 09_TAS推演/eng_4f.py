# -*- coding: utf-8 -*-
"""引擎级 BFS：4F 从落点 (11,10) 到祭坛 (6,1) 的最优路径。
返回：路径、钥匙消耗、战损。
"""
import sys, heapq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import manual
manual.execute(verbose=False)
W = manual.W
W.hero.f, W.hero.x, W.hero.y = 4, 11, 10
W.hero.atk, W.hero.dfn = 26, 25
W.hero.hp = 469
W.hero.keys = dict(y=4, b=1, r=1)
W.trap_mode = 'apply'

DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
def try_move(cx, cy, dx, dy):
    c = W.clone()
    c.hero.x, c.hero.y = cx, cy
    lg = c.move(dx, dy)
    if lg and lg[0].startswith(('blocked', '打不动', '打不过', '无', '买不起', '熔岩烫死', '祭坛金币不足', '无黄钥匙', '无蓝钥匙', '无红钥匙')):
        return None, None, lg
    h0 = W.hero.hp
    hp_loss = max(h0 - c.hero.hp, 0)
    key_used = 0
    for e in (lg or []):
        if e.startswith('开黄门'): key_used = 1
        elif e.startswith('开蓝门'): key_used = 2
        elif e.startswith('开红门'): key_used = 3
    return (c.hero.x, c.hero.y), (hp_loss, key_used), lg

start = (11, 10)
goal = (6, 1)
dist = {start: 0}
prev = {}
pq = [(0, 0, start)]
while pq:
    cst, sp, c = heapq.heappop(pq)
    if cst != dist.get(c): continue
    if c == goal: break
    for d in DIRS:
        n = (c[0]+d[0], c[1]+d[1])
        if not (0 <= n[0] < 13 and 0 <= n[1] < 13): continue
        res, cost, lg = try_move(c[0], c[1], d[0], d[1])
        if res is None: continue
        hp_loss, key_used = cost
        nc = cst + hp_loss + 100 * key_used
        if n not in dist or nc < dist[n]:
            dist[n] = nc; prev[n] = (c, d)
            heapq.heappush(pq, (nc, sp+1, n))

if goal not in dist:
    print('祭坛(6,1) 不可达！可达格:')
    print(' '.join('(%d,%d)'%c for c in sorted(dist)))
    sys.exit(1)

path = []
cur = goal
while cur != start:
    p, d = prev[cur]
    path.append((d, cur))
    cur = p
path = list(reversed(path))
print('4F (11,10)->祭坛(6,1) 路径:')
cx, cy = start
tot = 0
for i, (d, cell) in enumerate(path):
    res, cost, lg = try_move(cx, cy, d[0], d[1])
    hp_loss, key_used = cost
    tot += hp_loss
    desc = '; '.join(e[:36] for e in (lg or []) if not e.startswith('拾'))
    print('  %2d (%2d,%2d)->(%2d,%2d) HP-%d 钥%d %s' % (i+1, cx, cy, cell[0], cell[1], hp_loss, key_used, desc))
    cx, cy = cell
print('总战损 %d' % tot)
print('祭坛可到达：钥匙黄%d 蓝%d 红%d' % (W.hero.keys['y'], W.hero.keys['b'], W.hero.keys['r']))