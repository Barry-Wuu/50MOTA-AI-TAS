# -*- coding: utf-8 -*-
"""引擎级 Dijkstra：10F 从 (1,10) 到 BOSS(6,3) 的最优路径（避开战利品）。
clone+move 真实代价；禁踩 (2,6)(10,6)(11,11)。A26/D25 HP506 黄2蓝0红1。
输出：路径、每步战损、钥匙消耗、总代价。
"""
import sys, heapq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import manual
manual.execute(verbose=False)
W = manual.W
W.hero.f, W.hero.x, W.hero.y = 10, 1, 10
W.hero.atk, W.hero.dfn = 26, 25
W.hero.hp = 506
W.hero.keys = dict(y=2, b=0, r=1)
W.trap_mode = 'apply'

LOOT = {(2, 6), (10, 6), (11, 11)}
DIRS = [(1,0),(-1,0),(0,1),(0,-1)]

def try_move(cx, cy, dx, dy):
    c = W.clone()
    c.hero.x, c.hero.y = cx, cy
    lg = c.move(dx, dy)
    if lg and lg[0].startswith(('blocked', '打不动', '打不过', '无', '买不起', '熔岩烫死', '祭坛金币不足', '无黄钥匙', '无蓝钥匙', '无红钥匙')):
        return None, None, lg
    # 计算代价：HP 变化
    h0 = W.hero.hp
    hp_loss = h0 - c.hero.hp
    if hp_loss < 0: hp_loss = 0
    key_used = 0
    for e in (lg or []):
        if e.startswith('开黄门'): key_used = 1
        elif e.startswith('开蓝门'): key_used = 2
        elif e.startswith('开红门'): key_used = 3
    return (c.hero.x, c.hero.y), (hp_loss, key_used), lg

start = (1, 10)
goal = (6, 3)
dist = {start: 0}
prev = {}
pq = [(0, 0, start)]
while pq:
    cst, sp, c = heapq.heappop(pq)
    if cst != dist.get(c):
        continue
    if c == goal:
        break
    for d in DIRS:
        n = (c[0]+d[0], c[1]+d[1])
        if not (0 <= n[0] < 13 and 0 <= n[1] < 13) or n in LOOT:
            continue
        res, cost, lg = try_move(c[0], c[1], d[0], d[1])
        if res is None:
            continue
        hp_loss, key_used = cost
        nc = cst + hp_loss + 100 * key_used
        if n not in dist or nc < dist[n]:
            dist[n] = nc
            prev[n] = (c, d)
            heapq.heappush(pq, (nc, sp+1, n))

if goal not in dist:
    print('BOSS(6,3) 不可达！')
    # 打印可达格
    print('可达格:', ' '.join('(%d,%d)'%c for c in sorted(dist)))
    sys.exit(1)

# 回溯
path = []
cur = goal
while cur != start:
    p, d = prev[cur]
    path.append((d, cur))
    cur = p
path = list(reversed(path))

print('10F (1,10) -> BOSS(6,3) 最优路径（禁战利品）:')
tot_hp = 0
cx, cy = start
for i, (d, cell) in enumerate(path):
    res, cost, lg = try_move(cx, cy, d[0], d[1])
    hp_loss, key_used = cost
    tot_hp += hp_loss
    desc = ''
    if lg:
        desc = '; '.join(e[:40] for e in lg if not e.startswith('拾'))
    print('  %2d (%2d,%2d)->(%2d,%2d) HP-%d 钥%d %s' % (i+1, cx, cy, cell[0], cell[1], hp_loss, key_used, desc))
    cx, cy = cell
print('总战损(不含BOSS) %d，钥匙消耗 %d' % (tot_hp, sum(k for _, k in [ (d, k) for d, cell in path for k in [0]])))
# BOSS 战损
from math import ceil
loss = (ceil(100/max(26-15,1))-1) * max(65-25,1)
print('BOSS(100/65/15) 对 A26/D25 战损 %d' % loss)
print('10F 总战损(含BOSS) %d' % (tot_hp + loss))
print('到达 BOSS 前 HP = %d' % (506 - tot_hp))