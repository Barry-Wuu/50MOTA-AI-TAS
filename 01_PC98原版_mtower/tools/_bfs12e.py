import mota_core as M, run_segs as R, heapq
w=M.World.new(); h=w.hero
h.f,h.x,h.y=12,10,11; h.hp,h.atk,h.dfn,h.gold=3745,131,69,1007
y0,b0=1,0   # 实测进12F钥匙
def can(nx,ny,ky,kb):
    if not(1<=nx<=11 and 1<=ny<=11): return False
    t=w.terrain_at(12,nx,ny)
    if t in (1,2): return w.at(12,nx,ny)==89
    if (nx,ny) in R._stair_cells(w,12): return False
    o=w.at(12,nx,ny)
    if not o: return True
    ty=M.TYPE.get(M.oatr(o,3))
    if o==89 or o==115: return True
    if o in M.KEY_OF or ty in ('STATUS','ITEM','NORMAL','SCORE','MESSAGE'): return True
    if ty=='DOOR':
        c=M.DOOR_OF.get(o); return (c=='y' and ky>0) or (c=='b' and kb>0)
    if ty in ('SELL','SAIDAN','MONSTER'):
        if ty=='MONSTER': r=w.battle(o); return r is not None and r[0]<h.hp
        return True
    return False
start=(10,11,y0,b0)
dist={start:0}; prev={}; pq=[(0,start)]
goal=None
while pq:
    d,st=heapq.heappop(pq); cx,cy,ky,kb=st
    if (cx,cy)==(1,1): goal=st; break
    if d>dist.get(st,1e9): continue
    for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)):
        nx,ny=cx+dx,cy+dy
        if not can(nx,ny,ky,kb): continue
        o=w.at(12,nx,ny); ty=M.TYPE.get(M.oatr(o,3)) if o else None
        nky,nkb=ky,kb
        if ty=='DOOR':
            c=M.DOOR_OF.get(o)
            if c=='y': nky-=1
            if c=='b': nkb-=1
        elif o in M.KEY_OF:
            c=M.KEY_OF[o]
            if c=='y': nky+=1
            if c=='b': nkb+=1
        ns=(nx,ny,nky,nkb)
        if d<dist.get(ns,1e9): dist[ns]=d; prev[ns]=st; heapq.heappush(pq,(d,ns))
print('商人可达(含捡钥):',goal)
if goal:
    cur=goal; path=[]
    while cur in prev: path.append(cur); cur=prev[cur]
    path.append(start); path.reverse()
    print('路径:')
    for s in path:
        tag=''
        o=w.at(12,s[0],s[1]); ty=M.TYPE.get(M.oatr(o,3)) if o else None
        if ty=='DOOR': tag='  [开门]'
        if o in M.KEY_OF: tag='  [拾钥]'
        if o==89: tag='  [暗道]'
        if s[0]==1 and s[1]==1: tag='  [商人]'
        print('  (%d,%d) 钥y%d b%d%s'%(s[0],s[1],s[2],s[3],tag))
