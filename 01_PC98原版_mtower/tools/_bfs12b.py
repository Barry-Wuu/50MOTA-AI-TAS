import mota_core as M, run_segs as R
import heapq
w = M.World.new()
h = w.hero
h.f,h.x,h.y=12,10,11
h.hp,h.atk,h.dfn,h.gold=3745,131,69,1007
# 状态 BFS：keys=(y,b)。passable 精确复刻 _cost（不含楼梯）
def can(nx,ny,ky,kb):
    if not(1<=nx<=11 and 1<=ny<=11): return False,0
    t=w.terrain_at(12,nx,ny)
    if t in (1,2):
        if w.at(12,nx,ny)==89: return True,3   # 暗墙
        return False,0
    if (nx,ny) in R._stair_cells(w,12): return False,0
    o=w.at(12,nx,ny)
    if not o: return True,1
    ty=M.TYPE.get(M.oatr(o,3))
    if o==89 or o==115: return True,3
    if o in M.KEY_OF or ty in ('STATUS','ITEM','NORMAL','SCORE','MESSAGE'): return True,1
    if ty=='DOOR':
        col=M.DOOR_OF.get(o)
        if col=='y': return ky>0,25
        if col=='b': return kb>0,25
        if col=='r': return False,0
        return False,0
    if ty=='SELL': return h.gold>=M.SHOP_PRICE.get(o,0),3
    if ty=='SAIDAN': return (12,nx,ny) in M.ALTAR_CELLS,5
    if ty=='MONSTER':
        r=w.battle(o); return (r is not None and r[0]<h.hp),100
    return False,0
start=(10,11,1,0)
dist={start:0}; prev={}
pq=[(0,start)]
goal=None
while pq:
    d,st=heapq.heappop(pq)
    cx,cy,ky,kb=st
    if (cx,cy)==(1,1): goal=st; break
    if d>dist.get(st,1e9): continue
    for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)):
        nx,ny=cx+dx,cy+dy
        ok,_=can(nx,ny,ky,kb)
        if not ok: continue
        o=w.at(12,nx,ny); ty=M.TYPE.get(M.oatr(o,3)) if o else None
        nky,nkb=ky,kb
        if ty=='DOOR' and M.DOOR_OF.get(o)=='y': nky=ky-1
        if ty=='DOOR' and M.DOOR_OF.get(o)=='b': nkb=kb-1
        ns=(nx,ny,nky,nkb)
        if d<dist.get(ns,1e9):
            dist[ns]=d; prev[ns]=st; heapq.heappush(pq,(d,ns))
print('商人可达:',goal)
if goal:
    cur=goal; path=[]
    while cur in prev: path.append(cur); cur=prev[cur]
    path.append(start); path.reverse()
    print('步数=%d'%len(path))
    for s in path: print('  ',s)
