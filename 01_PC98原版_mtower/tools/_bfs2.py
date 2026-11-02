# -*- coding: utf-8 -*-
"""通用逐层 BFS：某层 (start)->(goal)，A/D/钥 固定，最小战损路径。
用法: python _bfs2.py <floor> <sx> <sy> <gx> <gy> <ky> <kb> <kr> <A> <D>
"""
import sys, os, json, math, heapq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as mc

d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'magic_tower1_map_50f.json'), encoding='utf-8'))
OA, TYPE = mc.OA, mc.TYPE

def battle_loss(o, A, D):
    a = OA[o]
    hp, atk, dfn = a[10], a[11], a[12]
    per = A - dfn
    if per <= 0: return None
    turns = math.ceil(hp / per)
    return max(atk - D, 0) * (turns - 1)

fl = sys.argv[1]
sx, sy = int(sys.argv[2]), int(sys.argv[3])
gx, gy = int(sys.argv[4]), int(sys.argv[5])
ky, kb, kr = int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])
A, D = int(sys.argv[9]), int(sys.argv[10])

F = d[fl]
terr = F['terrain']; obj = F['objects']
def is_wall(y, x): return terr[y][x] == 3

start = (sx, sy); goal = (gx, gy)
INF = float('inf')
dist = {}; prev = {}
st0 = (sx, sy, ky, kb, kr)
dist[st0] = 0
pq = [(0, st0)]
best = None
while pq:
    cost, (x, y, KY, KB, KR) = heapq.heappop(pq)
    if cost > dist.get((x, y, KY, KB, KR), INF): continue
    if (x, y) == goal:
        best = (cost, (x, y, KY, KB, KR)); break
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x+dx, y+dy
        if not (1 <= nx <= 11 and 1 <= ny <= 11): continue
        if is_wall(ny, nx): continue
        o = obj[ny][nx]
        ncost = cost; nKY, nKB, nKR = KY, KB, KR
        if o == 2:
            if KY <= 0: continue
            nKY -= 1
        elif o == 4:
            if nKB <= 0: continue
            nKB -= 1
        elif o == 27:
            if nKR <= 0: continue
            nKR -= 1
        elif TYPE.get(OA[o][3], '?') == 'MONSTER':
            bl = battle_loss(o, A, D)
            if bl is None: continue
            ncost += bl
        st = (nx, ny, nKY, nKB, nKR)
        if ncost < dist.get(st, INF):
            dist[st] = ncost; prev[st] = (x, y, KY, KB, KR)
            heapq.heappush(pq, (ncost, st))

if best:
    cost, st = best
    p = [st]
    while p[-1] in prev: p.append(prev[p[-1]])
    p = list(reversed(p))
    print(f'=== {fl}F ({sx},{sy})->({gx},{gy}) 最小战损 = {cost}，终点钥 {st[2]}/{st[3]}/{st[4]}，格数 {len(p)} ===')
    for (x, y, *k) in p:
        o = obj[y][x]
        tag = ''
        if o == 2: tag = '黄门'
        elif o == 4: tag = '蓝门'
        elif o == 27: tag = '红门'
        elif TYPE.get(OA[o][3], '?') == 'MONSTER':
            a = OA[o]
            tag = f'{mc.oname(o)[:8]}({a[10]}/{a[11]}/{a[12]}) -{battle_loss(o,A,D)}'
        print(f'  ({x},{y}) {tag}')
else:
    print(f'=== {fl}F ({sx},{sy})->({gx},{gy}) 不可达 ===')
