# -*- coding: utf-8 -*-
"""16F 下半区 BFS：从 (11,7) 到 (6,11) 楼梯，A45/D51，钥2/1/0。
最小战损（门耗钥、怪战损），验证绕行路线格序。
"""
import sys, os, json, math, heapq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as mc

d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'magic_tower1_map_50f.json'), encoding='utf-8'))
OA, TYPE = mc.OA, mc.TYPE
F = d['16']
terr = F['terrain']; obj = F['objects']

def battle_loss(o, A, D):
    a = OA[o]
    hp, atk, dfn = a[10], a[11], a[12]
    per = A - dfn
    if per <= 0: return None
    turns = math.ceil(hp / per)
    return max(atk - D, 0) * (turns - 1)

def is_wall(y, x): return terr[y][x] == 3

# 怪物表：列出 16F 所有怪，供参考
print('=== 16F 怪物 ===')
for y in range(13):
    for x in range(13):
        o = obj[y][x]
        if o and TYPE.get(OA[o][3], '?') == 'MONSTER':
            a = OA[o]
            print(f'  ({x},{y}) obj{o} {mc.oname(o)[:8]} hp{a[10]} atk{a[11]} def{a[12]} gold{a[13]}')

start = (11, 7); goal = (6, 11)
ky, kb, kr = 2, 1, 0
A, D = 45, 51
INF = float('inf')
dist = {}; prev = {}
st0 = (start[0], start[1], ky, kb, kr)
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
    print(f'\n=== 16F (11,7)->(6,11) 最小战损 = {cost}，终点钥 {st[2]}/{st[3]}/{st[4]}，格数 {len(p)} ===')
    for (x, y, *k) in p:
        o = obj[y][x]
        tag = ''
        if o == 2: tag = '黄门'
        elif o == 4: tag = '蓝门'
        elif o == 27: tag = '红门'
        elif TYPE.get(OA[o][3], '?') == 'MONSTER':
            a = OA[o]
            tag = f'{mc.oname(o)[:8]} -{battle_loss(o,A,D)}'
        print(f'  ({x},{y}) {tag}')
else:
    print('不可达')
