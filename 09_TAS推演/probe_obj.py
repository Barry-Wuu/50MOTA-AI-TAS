# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools")
import mota_core as M
for o in (21,22,23):
    print(o, "attr3(type)=", M.oatr(o,3), "->", M.TYPE.get(M.oatr(o,3)), "name=", repr(M.oname(o)), "cols=", [M.oatr(o,i) for i in range(14)])
