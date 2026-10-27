import sys, heapq, collections, itertools
import mota_core as M
CNT=itertools.count()
def make_h():
    G=(11,6,10); dist={G:0}; q=collections.deque([G])
    while q:
        f,x,y=q.popleft(); d=dist[(f,x,y)]; nb=[]
        for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
            nx,ny=x+dx,y+dy
            if 0<=nx<13 and 0<=ny<13 and M.terrain(f,nx,ny)!=1: nb.append((f,nx,ny))
        if M.terrain(f,x,y)==2:
            w=M.WARP.get((f,x,y))
            if w: nb.append(w)
        for c in nb:
            if c not in dist: dist[c]=d+1; q.append(c)
    dist[(10,6,11)]=1
    return dist
def start_at(hp, y=1,b=1,r=0,gold=100000,atk=20,dfn=10,f=7,x=11,yy=10):
    w=M.World.new(event_mode='on_entry',trap_mode='apply')
    h=w.hero; h.f,h.x,h.y=f,x,yy; h.hp,h.atk,h.dfn,h.gold=hp,atk,dfn,gold
    h.keys['y'],h.keys['b'],h.keys['r']=y,b,r
    w.trap_done=True; w.flag3F=1; w.applied_events.clear(); w.apply_floor_events(f); return w
def key(w):
    h=w.hero; return (h.f,h.x,h.y,h.keys['y'],h.keys['b'],h.keys['r'],h.atk,h.dfn,w.boss10)
def solve(hp,max_exp=3000000,fmin=7,fmax=11,start=None):
    H=make_h(); st=start or start_at(hp)
    s=next(CNT)
    pq=[(H.get((st.hero.f,st.hero.x,st.hero.y),50),-st.hero.hp,0,s,st)]
    best={key(st):st.hero.hp}; par={s:None}; wmap={s:st}
    expanded=0; maxf=fmin
    while pq:
        _,_,steps,sid,w=heapq.heappop(pq); h=w.hero
        if h.f==11:
            path=[]; c=sid
            while c is not None:
                ww=wmap[c]; hh=ww.hero
                path.append((hh.f,hh.x,hh.y,hh.hp,hh.atk,hh.dfn,tuple(sorted((k,v) for k,v in hh.keys.items())),hh.gold,ww.boss10))
                c=par[c]
            return w,list(reversed(path)),expanded
        k=key(w)
        if best.get(k,-10**9)>h.hp: continue
        expanded+=1; maxf=max(maxf,h.f)
        if expanded>max_exp: return ('cap',expanded,maxf)
        for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
            w2=w.clone(); log=w2.move(dx,dy)
            if M.blocked(log) or w2.hero.hp<=0: continue
            if w2.hero.f<fmin or w2.hero.f>fmax: continue
            k2=key(w2)
            if best.get(k2,-10**9)>=w2.hero.hp: continue
            best[k2]=w2.hero.hp
            s2=next(CNT); par[s2]=sid; wmap[s2]=w2
            heapq.heappush(pq,(H.get((w2.hero.f,w2.hero.x,w2.hero.y),50),-w2.hero.hp,steps+1,s2,w2))
    return (None,expanded,maxf)
if __name__=='__main__':
    hp=int(sys.argv[1]); mx=int(sys.argv[2]) if len(sys.argv)>2 else 3000000
    r=solve(hp,mx)
    if r and r[0] is not None and not isinstance(r[0],str):
        w,path,ex=r
        print(f"HP={hp} 成功 展开={ex} 步数={len(path)-1} 余血={w.hero.hp} ATK={w.hero.atk} DEF={w.hero.dfn} keys={dict(w.hero.keys)} G={w.hero.gold}")
        for p in path: print("   ",p)
    else: print(f"HP={hp} 结果:",r)
