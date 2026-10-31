# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools")
import mota_core as M
for f in range(1,12):
    print(f,"F stairs",M.STAIRS[f], "warp:", {k[1:]:v for k,v in M.WARP.items() if k[0]==f})
