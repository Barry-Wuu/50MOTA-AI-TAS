# -*- coding: utf-8 -*-
"""47F 清场：从(10,11)到上梯(1,1)必经怪与战损。"""
import json, math, heapq
d = json.load(open('../magic_tower1_map_50f.json', encoding='utf-8'))
f = d['47']
terr = f['terrain']
def is_wall(y, x): return terr[y][x] == 3
cells = {}
for e in f['entities']:
    cells[(e['x'], e['y'])] = e
DOOR = {2:'y', 3:'b', 4:'b'}  # 2黄门,3蓝钥?? 注意 obj3=蓝钥,obj4=蓝门
MONSTER_OBJS = {97,98,99,100,101}

# obj 语义重查：本文件 obj 编号与 43F 不同。用 role 判定
def kind(e):
    if e['role']=='monster': return 'M'
    if e['role']=='pickup': return 'D'  # 门
    return 'I'  # 道具/钥匙

def battle_loss(e, A, D):
    hp, atk, dfn = e['hp'], e['atk'], e['dfn']
    per = A - dfn
    if per <= 0: return None
    turns = math.ceil(hp / per)
    return max(atk - D, 0) * (turns - 1)

# 尝试多种 A/D
for (A, D) in [(170,137),(170,198),(166,198),(170,219)]:
    print('=== 47F (10,11)->(1,1) @A%d/D%d ===' % (A, D))
    # Dijkstra: cost=战损, 状态=(x,y); 门可过(记钥匙), 怪需可杀
    INF=float('inf'); dist={}; prev={}
    start=(10,11); goal=(1,1)
    dist[start]=0; pq=[(0,start)]
    while pq:
        cost,(x,y)=heapq.heappop(pq)
        if cost>dist.get((x,y),INF): continue
        if (x,y)==goal: break
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if not(1<=nx<=11 and 1<=ny<=11): continue
            if is_wall(ny,nx): continue
            e=cells.get((nx,ny)); ncost=cost
            if e is not None:
                if kind(e)=='M':
                    bl=battle_loss(e,A,D)
                    if bl is None: continue
                    ncost+=bl
            if ncost<dist.get((nx,ny),INF):
                dist[(nx,ny)]=ncost; prev[(nx,ny)]=(x,y)
                heapq.heappush(pq,(ncost,(nx,ny)))
    if goal in dist:
        p=[goal]
        while p[-1] in prev: p.append(prev[p[-1]])
        p=list(reversed(p))
        monsters=[(x,y,cells[(x,y)]['name_en']) for (x,y) in p if (x,y) in cells and kind(cells[(x,y)])=='M']
        doors=[(x,y,cells[(x,y)]['obj']) for (x,y) in p if (x,y) in cells and kind(cells[(x,y)])=='D']
        print('  战损=%d 路径=%d格' % (dist[goal], len(p)))
        print('   怪:', monsters)
        print('   门:', doors)
        print('   路:', p)
    else:
        print('  不可达')
