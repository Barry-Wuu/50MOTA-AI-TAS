# -*- coding: utf-8 -*-
import sys, time
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
for gf in range(2, 12):
    t = time.time()
    r = M.plan(lambda f,x,y: f==gf, max_states=150000)
    dt = time.time()-t
    if r is None:
        print('f==%-2d -> None (%.1fs)' % (gf, dt))
    elif isinstance(r,tuple) and r[0]=='cap':
        print('f==%-2d -> CAP %s (%.1fs)' % (gf, r[1], dt))
    else:
        w,path=r; h=w.hero
        print('f==%-2d -> OK  steps=%d HP%d A%d D%d G%d 钥%d/%d/%d (%.1fs)' % (
            gf, len(path)-1, h.hp,h.atk,h.dfn,h.gold,h.keys['y'],h.keys['b'],h.keys['r'], dt))
