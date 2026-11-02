# -*- coding: utf-8 -*-
"""43F 青药：最小战损路径 Dijkstra（细胞只访一次；门记钥匙、怪记战损）。"""
import json, math, heapq
from collections import deque

d = json.load(open('../magic_tower1_map_50f.json', encoding='utf-8'))
f = d['43']
terr = f['terrain']
def is_wall(y, x):
    return terr[y][x] == 3

cells = {}
for e in f['entities']:
    cells[(e['x'], e['y'])] = e

DOOR = {2: 'y', 4: 'b'}
MONSTER_OBJS = {58, 97, 98, 99, 100, 101}
targets = {(6,6), (4,9), (4,10), (4,11)}
start = (1, 2)
A, D = 170, 137

def battle_loss(e, A, D):
    hp = e['hp']; atk = e['atk']; dfn = e['dfn']
    dmg = A - dfn
    if dmg <= 0: return None
    turns = math.ceil(hp / dmg)
    back = atk - D
    if back <= 0: return 0
    return back * (turns - 1)

# Dijkstra: cost=战损(HP)，状态=(x,y)，记录路径+钥匙
INF = float('inf')
dist = {}; prev = {}; keyuse = {}
dist[start] = 0; keyuse[start] = (0, 0)
pq = [(0, start)]
while pq:
    cost, (x, y) = heapq.heappop(pq)
    if cost > dist.get((x, y), INF): continue
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x+dx, y+dy
        if not (1 <= nx <= 11 and 1 <= ny <= 11): continue
        if is_wall(ny, nx): continue
        e = cells.get((nx, ny))
        ncost = cost; uy, ub = keyuse[(x, y)]
        if e is not None:
            obj = e['obj']
            if obj in DOOR:
                if DOOR[obj] == 'y': uy += 1
                else: ub += 1
            elif obj in MONSTER_OBJS:
                bl = battle_loss(e, A, D)
                if bl is None: continue
                ncost += bl
        if ncost < dist.get((nx, ny), INF):
            dist[(nx, ny)] = ncost
            keyuse[(nx, ny)] = (uy, ub)
            prev[(nx, ny)] = (x, y)
            heapq.heappush(pq, (ncost, (nx, ny)))

def path_to(t):
    p = [t]
    while p[-1] in prev:
        p.append(prev[p[-1]])
    return list(reversed(p))

print('=== 43F 青药最小战损路径 @A%d/D%d（黑骑士不可杀=不可过）===' % (A, D))
for t in sorted(targets):
    if t in dist:
        p = path_to(t)
        uy, ub = keyuse[t]
        # 收集路径上的怪/门
        monsters = [(x, y, cells[(x,y)]['name_en']) for (x,y) in p if (x,y) in cells and cells[(x,y)]['obj'] in MONSTER_OBJS]
        doors = [(x, y, cells[(x,y)]['obj']) for (x,y) in p if (x,y) in cells and cells[(x,y)]['obj'] in DOOR]
        print('%s 战损=%d 黄门x%d 蓝门x%d 路径=%d格' % (t, dist[t], uy, ub, len(p)))
        print('   怪:', monsters)
        print('   门:', doors)
        print('   路:', p)
    else:
        print('%s 不可达' % (t,))
