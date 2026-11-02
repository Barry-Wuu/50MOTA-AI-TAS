# -*- coding: utf-8 -*-
"""47F 清怪：从 (10,11) 到 (1,1) 上 48F，强制拿蓝晶(6,8)+红药(4,10)，最小战损。
对照 47F 段完成 HP(352 或 若保留11F药=752)。钥匙: 黄2/蓝1/红1。"""
import json, math, heapq, sys
sys.path.insert(0, 'tools')
import mota_core as mc
d = json.load(open('magic_tower1_map_50f.json', encoding='utf-8'))
f = d['47']; terr = f['terrain']; obj = f['objects']
OA = mc.OA; TYPE = mc.TYPE

def bl(o, A, D):
    a = OA[o]; hp, atk, dfn = a[10], a[11], a[12]
    per = A - dfn
    if per <= 0: return None
    return max(atk - D, 0) * (math.ceil(hp / per) - 1)

def solve(A, D, start=(10,11), goal=(1,1), must=(), keys=(2,1,1), forbid_red=False):
    ky, kb, kr = keys
    INF = float('inf'); dist = {}; prev = {}
    st0 = (start[0], start[1], ky, kb, kr, 0)  # 末位=已拿must的bitmask
    mreq = {p: i for i, p in enumerate(must)}
    dist[st0] = 0; pq = [(0, st0)]
    while pq:
        cost, (x, y, KY, KB, KR, m) = heapq.heappop(pq)
        if cost > dist.get((x,y,KY,KB,KR,m), INF): continue
        if (x, y) == goal and m == (1 << len(must)) - 1:
            return cost, (x,y,KY,KB,KR,m)
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if not (1<=nx<=11 and 1<=ny<=11): continue
            if terr[ny][nx] == 3: continue
            o = obj[ny][nx]
            nc = cost; nKY, nKB, nKR = KY, KB, KR
            if o == 2:
                if nKY <= 0: continue
                nKY -= 1
            elif o == 4:
                if nKB <= 0: continue
                nKB -= 1
            elif o == 27:
                if forbid_red: continue
                if nKR <= 0: continue
                nKR -= 1
            elif TYPE.get(OA[o][3], '?') == 'MONSTER':
                b = bl(o, A, D)
                if b is None: continue
                nc += b
            nm = m
            if (nx, ny) in mreq:
                nm |= 1 << mreq[(nx, ny)]
            st = (nx, ny, nKY, nKB, nKR, nm)
            if nc < dist.get(st, INF):
                dist[st] = nc; prev[st] = (x,y,KY,KB,KR,m)
                heapq.heappush(pq, (nc, st))
    return None, None

def show(A, D, must, keys, label, forbid_red=False):
    r = solve(A, D, must=must, keys=keys, forbid_red=forbid_red)
    if r[0] is None:
        print(f'{label} @A{A}/D{D}: 不可达')
    else:
        print(f'{label} @A{A}/D{D}: 战损={r[0]} 余钥{r[1][2]}/{r[1][3]}/{r[1][4]}')

# 场景1: 仅到上梯 (1,1)，不强制拿晶/药（捷径）
show(170,137, (), (2,1,1), 'A仅上梯')
# 场景2: 强制拿蓝晶(6,8)+红药(4,10)（照攻略意图）
show(170,137, ((6,8),(4,10)), (2,1,1), 'B拿蓝晶+红药')
# 场景3: 强制拿蓝晶 不拿红药
show(170,137, ((6,8),), (2,1,1), 'C拿蓝晶')
# 场景4: 蓝晶+红药，高DEF D149
show(170,149, ((6,8),(4,10)), (2,1,1), 'D拿蓝晶+红药@D149')
# 场景5: 蓝晶+红药，D198
show(170,198, ((6,8),(4,10)), (2,1,1), 'E拿蓝晶+红药@D198')
