# -*- coding: utf-8 -*-
"""三个回复药可行性：Dijkstra 最小战损+门消耗，对照钥匙预算。
A170/D137。门: 2黄门扣黄钥,4蓝门扣蓝钥,27红门扣红钥。
零战损怪(atk<=D) 免费杀。
"""
import json, math, heapq, sys
sys.path.insert(0, 'tools')
import mota_core as mc

d = json.load(open('magic_tower1_map_50f.json', encoding='utf-8'))
OA = mc.OA
TYPE = mc.TYPE

def battle_loss(o, A, D):
    a = OA[o]
    hp, atk, dfn = a[10], a[11], a[12]
    per = A - dfn
    if per <= 0: return None
    turns = math.ceil(hp / per)
    return max(atk - D, 0) * (turns - 1)

def solve(fl, start, goal, keys, A=170, D=137, cleared=(), ignore_obj=()):
    f = d[fl]
    terr = f['terrain']
    obj = f['objects']
    def is_wall(y, x): return terr[y][x] == 3
    # 状态 (x,y,ky,kb,kr)
    ky, kb, kr = keys
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
            best = (cost, (x, y, KY, KB, KR))
            break
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if not (1 <= nx <= 11 and 1 <= ny <= 11): continue
            if is_wall(ny, nx): continue
            o = obj[ny][nx]
            ncost = cost
            nKY, nKB, nKR = KY, KB, KR
            if o == 2:  # 黄门
                if KY <= 0: continue
                nKY -= 1
            elif o == 4:  # 蓝门
                if nKB <= 0: continue
                nKB -= 1
            elif o == 27:  # 红门
                if nKR <= 0: continue
                nKR -= 1
            elif TYPE.get(OA[o][3], '?') == 'MONSTER':
                if o in cleared: pass  # 已清
                else:
                    bl = battle_loss(o, A, D)
                    if bl is None: continue
                    ncost += bl
            st = (nx, ny, nKY, nKB, nKR)
            if ncost < dist.get(st, INF):
                dist[st] = ncost; prev[st] = (x, y, KY, KB, KR)
                heapq.heappush(pq, (ncost, st))
    return best, dist, prev

def path_of(prev, st):
    p = [st]
    while p[-1] in prev: p.append(prev[p[-1]])
    return list(reversed(p))

def describe(fl, p):
    obj = d[fl]['objects']
    out = []
    for (x, y, *k) in p:
        o = obj[y][x]
        if o == 2: out.append(f'黄门({x},{y})')
        elif o == 4: out.append(f'蓝门({x},{y})')
        elif o == 27: out.append(f'红门({x},{y})')
        elif TYPE.get(OA[o][3], '?') == 'MONSTER':
            a = OA[o]
            out.append(f'怪{({x},{y})}obj{o}({a[10]}/{a[11]}/{a[12]})')
    return out

# 场景: 42F 起点(6,5) 目标(1,9) 钥2/0/1  (42b 段在(6,5)处分叉)
# 已清: 42b 段已杀 金騎士(6,9)? 实际42b段路径 6,9是剧情清场区(骑士队长剧情)。简化: cleared 空(保守)
print('=== 42F (6,5)->(1,9)H 钥2/0/1 ===')
best, dist, prev = solve('42', (6,5), (1,9), (2,0,1))
if best:
    cost, st = best
    p = path_of(prev, st)
    print(f'  战损={cost} 余钥{st[2]}/{st[3]}/{st[4]} 格{len(p)}')
    print('  ', describe('42', p))
else:
    print('  不可达')

# 45F 起点(2,1) 目标(11,11) 钥5/0/1 (45a段落点)
print('=== 45F (2,1)->(11,11)H 钥5/0/1 ===')
best, dist, prev = solve('45', (2,1), (11,11), (5,0,1))
if best:
    cost, st = best
    p = path_of(prev, st)
    print(f'  战损={cost} 余钥{st[2]}/{st[3]}/{st[4]} 格{len(p)}')
    print('  ', describe('45', p))
else:
    print('  不可达')

# 15F 起点(6,10) 目标(11,8) 钥1/0/1, 大乌贼3x3已清(5..7,4..6)
print('=== 15F (6,10)->(11,8)H 钥1/0/1 (大乌贼已清) ===')
cleared = set()
for yy in range(4,7):
    for xx in range(5,8):
        o = d['15']['objects'][yy][xx]
        if TYPE.get(OA[o][3], '?') == 'MONSTER':
            cleared.add(o)
best, dist, prev = solve('15', (6,10), (11,8), (1,0,1), cleared=cleared)
if best:
    cost, st = best
    p = path_of(prev, st)
    print(f'  战损={cost} 余钥{st[2]}/{st[3]}/{st[4]} 格{len(p)}')
    print('  ', describe('15', p))
else:
    print('  不可达')
