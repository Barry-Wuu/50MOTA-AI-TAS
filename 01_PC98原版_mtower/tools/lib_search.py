import heapq, itertools
import mota_core as M
C=itertools.count(1)
def start_at(hp,y=1,b=1,r=0,f=7,x=11,yy=10,gold=100000,atk=20,dfn=10):
    w=M.World.new(event_mode='on_entry',trap_mode='apply')
    h=w.hero;h.f,h.x,h.y=f,x,yy;h.hp,h.atk,h.dfn,h.gold=hp,atk,dfn,gold
    h.keys['y'],h.keys['b'],h.keys['r']=y,b,r
    w.trap_done=True;w.flag3F=1;w.applied_events.clear();w.apply_floor_events(f);return w
def kk(w):
    h=w.hero
    return (h.f,h.x,h.y,h.keys['y'],h.keys['b'],h.keys['r'],h.atk,h.dfn,min(h.gold//50,4),w.boss10)
def search(fmin,fmax,goal,hp,y=1,b=1,r=0,cap=600000,st=None,keep=True):
    if st is None: st=start_at(hp,y,b,r)
    pq=[(0,0,0,st)]; best={kk(st):st.hero.hp}; par={0:None}; wm={0:st}
    exp=0
    while pq:
        _,_,sid,w=heapq.heappop(pq); h=w.hero
        k=kk(w)
        if best.get(k,-10**9)>h.hp: continue
        exp+=1
        if exp>cap: return ('cap',exp,None)
        if goal(w): return ('ok',exp,(w,par,wm,sid))
        for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
            w2=w.clone(); log=w2.move(dx,dy)
            if M.blocked(log) or w2.hero.hp<=0: continue
            if w2.hero.f<fmin or w2.hero.f>fmax: continue
            k2=kk(w2)
            if best.get(k2,-10**9)>=w2.hero.hp: continue
            best[k2]=w2.hero.hp; s2=next(C); par[s2]=sid; wm[s2]=w2
            heapq.heappush(pq,(0,0,s2,w2))
    return ('fail',exp,None)
def trace(res):
    w,par,wm,sid=res; path=[]; c=sid
    while c is not None:
        ww=wm[c]; hh=ww.hero
        path.append((hh.f,hh.x,hh.y,hh.hp,hh.atk,hh.dfn,tuple(sorted(hh.keys.items())),hh.gold,ww.boss10))
        c=par[c]
    return list(reversed(path))
