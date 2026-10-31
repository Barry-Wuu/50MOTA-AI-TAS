# -*- coding: utf-8 -*-
import sys, time, collections
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

goal = lambda f,x,y: f==11
start = M.World.new()
start._par = None
H = M.heuristic((11,6,10))
print('H size', len(H), 'start in H?', (1,6,11) in H)
h0 = H.get((1,6,11), 0)
import heapq as _hq
pq=[(h0,0,0,start)]
seen={}
n=0; pushed=0; blockedn=0
while pq:
    loss,steps,_,w=_hq.heappop(pq)
    if goal(w.hero.f,w.hero.x,w.hero.y):
        print('GOAL at', w.hero.f, w.hero.x, w.hero.y, 'n=',n, 'pushed=',pushed); break
    n+=1
    if n>200000: print('cap'); break
    k=(w.hero.f,w.hero.x,w.hero.y,w.hero.keys['y'],w.hero.keys['b'],w.hero.keys['r'],
       frozenset(c for c in w.cleared if c in M.PICKUP_CELLS), frozenset(w.bought))
    if k in seen and seen[k][0]<=loss and seen[k][1]<=steps: continue
    seen[k]=(loss,steps)
    for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
        before=(w.hero.hp,w.hero.f,w.hero.x,w.hero.y)
        w2=w.clone(); log=w2.move(dx,dy)
        if M.blocked(log): blockedn+=1; continue
        add=before[0]-w2.hero.hp
        w2._par=w
        ns=steps+1
        nh=H.get((w2.hero.f,w2.hero.x,w2.hero.y),0)
        _hq.heappush(pq,(loss+max(add,0)+nh*1000000, ns, next(M._TIE), w2))
        pushed+=1
    if n<=3 or n%5000==0:
        print('n=%d pq=%d pushed=%d blocked=%d cur=(%d,%d,%d) hp=%d' % (n,len(pq),pushed,blockedn,w.hero.f,w.hero.x,w.hero.y,w.hero.hp))
    if n>3000: break
print('END n=%d pushed=%d blocked=%d'%(n,pushed,blockedn))
