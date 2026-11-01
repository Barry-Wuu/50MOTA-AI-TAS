import mota_core as M, run_segs as R
from collections import deque
w = M.World.new()
h = w.hero
h.f, h.x, h.y = 12, 10, 11
h.hp, h.atk, h.dfn, h.gold = 3745, 131, 69, 1007
h.keys = {'y':1,'b':0,'r':1}
DIRS = ((0,1),(0,-1),(1,0),(-1,0))
# 状态 (x,y,keys)  keys=(y,b)  ; 门开过即 cleared，可重复走
start=(10,11,1,0)
# 记录每个状态是否可达到(含门开) — 用 (x,y,门开掩码) 太复杂；简化：BFS 逐门开，回溯记录
# 用 Dijkstra: cost=开门数, 优先最小门
import heapq
dist={(10,11,1,0):0}
prev={}
pq=[(0,10,11,1,0)]
best=None
while pq:
    d,cx,cy,ky,kb=heapq.heappop(pq)
    if (cx,cy)==(1,1):
        best=(d,cx,cy,ky,kb); break
    if d>dist.get((cx,cy,ky,kb),1e9): continue
    for dx,dy in DIRS:
        nx,ny=cx+dx,cy+dy
        # 试走：先看该格是否可通过（用当前钥匙）
        ok,wc=R._cost(w,12,nx,ny)
        if not ok:
            # 若是门且钥匙够→开门（状态转移）
            o=w.at(12,nx,ny)
            if o in M.DOOR_OF:
                col=M.DOOR_OF[o]
                if col=='y' and ky>0:
                    st=(nx,ny,ky-1,kb)
                    if d+1<dist.get(st,1e9):
                        dist[st]=d+1; prev[st]=(cx,cy,ky,kb); heapq.heappush(pq,(d+1,nx,ny,ky-1,kb))
                elif col=='b' and kb>0:
                    st=(nx,ny,ky,kb-1)
                    if d+1<dist.get(st,1e9):
                        dist[st]=d+1; prev[st]=(cx,cy,ky,kb); heapq.heappush(pq,(d+1,nx,ny,ky,kb-1))
            continue
        st=(nx,ny,ky,kb)
        if d<dist.get(st,1e9):
            dist[st]=d; prev[st]=(cx,cy,ky,kb); heapq.heappush(pq,(d,nx,ny,ky,kb))
print('商人可达:',best)
if best:
    # 回溯路径
    cur=best[:4]
    path=[]
    while cur in prev:
        path.append(cur); cur=prev[cur]
    path.append(start)
    path.reverse()
    print('路径(门数=%d):'%best[0])
    for s in path:
        print('  ',s)
