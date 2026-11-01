import mota_core as M, run_segs as R, heapq
def solve(y0,b0):
    w=M.World.new(); h=w.hero
    h.f,h.x,h.y=12,10,11; h.hp,h.atk,h.dfn,h.gold=3745,131,69,1007
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
    start=(10,11,y0,b0); dist={start:0}; prev={}; pq=[(0,start)]
    while pq:
        d,st=heapq.heappop(pq); cx,cy,ky,kb=st
        if (cx,cy)==(1,1):
            # 回溯
            path=[]; cur=st
            while cur in prev: path.append(cur); cur=prev[cur]
            path.append(start); path.reverse()
            return path
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
            ns=(nx,ny,nky,nkb)
            if d<dist.get(ns,1e9): dist[ns]=d; prev[ns]=st; heapq.heappush(pq,(d,ns))
    return None
for y0,b0 in [(4,0),(3,1)]:
    p=solve(y0,b0)
    print('=== 黄%d蓝%d: %s'%(y0,b0,'可达' if p else '不可达'))
    if p:
        doors=[]
        for i in range(1,len(p)):
            px,py,_,_=p[i-1]; nx,ny,_,_=p[i]
            o=w.at(12,nx,ny) if False else None
        # 打印门/暗墙事件
        cur=p[0]
        print('  起点',cur[:2])
        for s in p[1:]:
            print('  -> (%d,%d) 钥y%d b%d'%(s[0],s[1],s[2],s[3]))
