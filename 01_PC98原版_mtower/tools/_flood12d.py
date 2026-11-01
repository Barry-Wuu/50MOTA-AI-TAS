import mota_core as M, run_segs as R
from collections import deque
w = M.World.new()
h = w.hero
h.f, h.x, h.y = 12, 10, 11
h.hp, h.atk, h.dfn, h.gold = 3745, 131, 69, 1007
h.keys={'y':1,'b':0,'r':1}
DIRS=((0,1),(0,-1),(1,0),(-1,0))
# 纯地形连通：把怪/NPC/钥匙/商店当可走，只墙和门挡路(门需对应钥匙)
def passable(nx,ny,ky,kb):
    if not(1<=nx<=11 and 1<=ny<=11): return None
    t=w.terrain_at(12,nx,ny)
    if t in (1,2):
        if w.at(12,nx,ny)==89: return True   # 暗墙可撞
        return False
    o=w.at(12,nx,ny)
    if not o: return True
    ty=M.TYPE.get(M.oatr(o,3))
    if o==89: return True
    if o==115: return True
    if o in M.KEY_OF or ty in ('STATUS','ITEM','NORMAL','SCORE','MESSAGE'): return True
    if ty=='DOOR':
        col=M.DOOR_OF.get(o)
        if col=='y': return ky>0
        if col=='b': return kb>0
        return False
    if ty in ('MONSTER','SELL','SAIDAN'): return True
    return False
# Dijkstra min 门数
import heapq
start=(10,11,1,0)
dist={start:0}; prev={}; pq=[(0,start)]
best=None
while pq:
    d,(cx,cy,ky,kb)=heapq.heappop(pq)
    if (cx,cy)==(1,1): best=(d,cx,cy,ky,kb); break
    if d>dist[(cx,cy,ky,kb)]: continue
    for dx,dy in DIRS:
        nx,ny=cx+dx,cy+dy
        p=passable(nx,ny,ky,kb)
        if p is None: continue
        if p is True:
            st=(nx,ny,ky,kb); nd=d
        else:
            st=(nx,ny,ky,kb); nd=d  # p为False但可能是门? 不会，门在passable已处理
            continue
        if nd<dist.get(st,1e9):
            dist[st]=nd; prev[st]=(cx,cy,ky,kb); heapq.heappush(pq,(nd,st))
print('商人可达(纯地形):',best)
if best:
    cur=best[:4]; path=[]
    while cur in prev: path.append(cur); cur=prev[cur]
    path.append(start); path.reverse()
    print('路径(门数=%d):'%best[0])
    for s in path: print('  ',s)
