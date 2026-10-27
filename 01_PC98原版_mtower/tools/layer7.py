import heapq, itertools, sys
import mota_core as M
C=itertools.count(1)
# 7F 内目标：踩 (1,1) 上楼（warp 8F），最大化剩余黄钥匙；hp 作为支配维度
CELLS=[(x,y) for y in range(13) for x in range(13) if M.terrain(7,x,y)!=1]
OBJ={c:M.obj_raw(7,*c) for c in CELLS}
ITEMS=[c for c in CELLS if OBJ[c]]
def start(hp=3000,yk=1,bk=1,rk=0,atk=20,dfn=10,gold=100000):
    w=M.World.new(event_mode='on_entry',trap_mode='apply')
    h=w.hero;h.f,h.x,h.y=7,11,10;h.hp,h.atk,h.dfn,h.gold=hp,atk,dfn,gold
    h.keys['y'],h.keys['b'],h.keys['r']=yk,bk,rk
    w.trap_done=True;w.flag3F=1;w.applied_events.clear();w.apply_floor_events(7);return w
def key(w):
    h=w.hero
    return (h.x,h.y,h.keys['y'],h.keys['b'],h.keys['r'],h.atk,h.dfn,w.boss10,
            tuple(sorted(w.cleared)))
def solve():
    st=start()
    pq=[(0,-st.hero.hp,0,0,next(C),st)]; best={key(st):st.hero.hp}; par={}; wm={}
    exp=0
    while pq:
        _,_,_,sid,w=heapq.heappop(pq); h=w.hero
        k=key(w)
        if best.get(k,-10**9)>h.hp: continue
        best[k]=h.hp; exp+=1
        if exp>1500000: return ('cap',exp,None)
        if h.f==8:
            return ('ok',exp,(w,par,wm,sid))
        for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
            w2=w.clone(); log=w2.move(dx,dy)
            if M.blocked(log) or w2.hero.hp<=0: continue
            if w2.hero.f!=7: continue
            k2=key(w2)
            if best.get(k2,-10**9)>=w2.hero.hp: continue
            best[k2]=w2.hero.hp; s2=next(C); par[s2]=sid; wm[s2]=w2
            heapq.heappush(pq,(0,-w2.hero.hp,0,0,s2,w2))
    return ('fail',exp,None)
st,exp,res=solve()
print("7F→8F:",st,"exp",exp)
if res:
    w,par,wm,sid=res; path=[]; c=sid
    while c is not None:
        ww=wm[c]; hh=ww.hero
        path.append((hh.f,hh.x,hh.y,hh.hp,hh.atk,hh.dfn,tuple(sorted(hh.keys.items())),hh.gold))
        c=par[c]
    path=list(reversed(path))
    print("步数",len(path)-1,"到8F时 keys",path[-1][6],"HP",path[-1][3],"ATK",path[-1][4],"DEF",path[-1][5])
    for p in path: print("  ",p)
