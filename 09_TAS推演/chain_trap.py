# -*- coding: utf-8 -*-
import sys, time, heapq as _hq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

goal = lambda f,x,y: f==4
start = M.World.new(); start._par=None
H = None
pq=[(0,0,0,start)]
seen={}
n=0; maxf=1; stall={}
while pq:
    loss,steps,_,w=_hq.heappop(pq)
    if goal(w.hero.f,w.hero.x,w.hero.y):
        print('GOAL 4F at (%d,%d) n=%d' % (w.hero.x,w.hero.y,n)); break
    n+=1
    if n>200000: print('cap'); break
    maxf=max(maxf,w.hero.f)
    k=(w.hero.f,w.hero.x,w.hero.y,w.hero.keys['y'],w.hero.keys['b'],w.hero.keys['r'],
       frozenset(c for c in w.cleared if c in M.PICKUP_CELLS), frozenset(w.bought))
    if k in seen and seen[k][0]<=loss and seen[k][1]<=steps: continue
    seen[k]=(loss,steps)
    for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
        before=(w.hero.hp,w.hero.f,w.hero.x,w.hero.y)
        w2=w.clone(); log=w2.move(dx,dy)
        if M.blocked(log): continue
        add=before[0]-w2.hero.hp
        w2._par=w
        _hq.heappush(pq,(loss+max(add,0)+0, steps+1, next(M._TIE), w2))
    if n in (1,2,3,4,5,10,20,50,100,150,200,300,500,800,1200,1800,2500,4000,7000,12000):
        print('n=%d pq=%d maxf=%d cur=%dF(%d,%d) hp=%d A%d D%d 钥%d/%d/%d'%(
            n,len(pq),maxf,w.hero.f,w.hero.x,w.hero.y,w.hero.hp,w.hero.atk,w.hero.dfn,
            w.hero.keys['y'],w.hero.keys['b'],w.hero.keys['r']))
print('END n=%d maxf=%d seen=%d'%(n,maxf,len(seen)))
