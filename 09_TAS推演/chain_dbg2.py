# -*- coding: utf-8 -*-
import sys, time
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

w0 = M.World.new()
print('start', w0.hero.f, w0.hero.x, w0.hero.y)
for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
    w2 = w0.clone(); log = w2.move(dx,dy)
    print(' move',(dx,dy),'->',w2.hero.f,w2.hero.x,w2.hero.y, log[:1])

# 用 goal_cell 指定启发目标，重新试 f==11
t=time.time()
r = M.plan(lambda f,x,y: f==11, goal_cell=(11,6,10), max_states=200000)
dt=time.time()-t
print('f==11 with goal_cell ->', 'OK steps' if r and not(isinstance(r,tuple) and r[0]=='cap') else r, '(%.1fs)'%dt)
if r and not(isinstance(r,tuple) and r[0]=='cap'):
    w,path=r; h=w.hero
    print('  HP%d ATK%d DEF%d G%d 钥%d/%d/%d'%(h.hp,h.atk,h.dfn,h.gold,h.keys['y'],h.keys['b'],h.keys['r']))
