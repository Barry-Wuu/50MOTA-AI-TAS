# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

for f in range(6, 21):
    up, dn = M.STAIRS[f]
    w = M.WARP.get((f,) + dn) if dn else None
    print('%2dF  up=%s dn=%s  dn_warp=%s  up_warp=%s' % (
        f, up, dn, w, M.WARP.get((f,) + up) if up else None))
