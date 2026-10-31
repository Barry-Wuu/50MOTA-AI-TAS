# -*- coding: utf-8 -*-
import sys, time
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

w0 = M.World.new()
print('start', w0.hero.f, w0.hero.x, w0.hero.y, w0.hero.hp)

# 目标 f==2（几步行）
for goal in [lambda f,x,y: f==2, lambda f,x,y: f==3, lambda f,x,y: f==4]:
    t=time.time()
    r = M.plan(goal, max_states=50000)
    print('goal f==%s ->' % '2' , 'OK' if r and not (isinstance(r,tuple) and r[0]=='cap') else r, '(%.1fs)'%(time.time()-t))
