# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools")
import mota_core as M
for f in range(1,51):
    for y in range(13):
        for x in range(13):
            o=M.obj_raw(f,x,y)
            if o in (21,23):
                print("obj%d at %dF(%d,%d) name=%s"%(o,f,x,y,M.oname(o)))
