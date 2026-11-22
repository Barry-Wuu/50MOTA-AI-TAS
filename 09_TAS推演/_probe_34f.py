# -*- coding: utf-8 -*-
import sys, os
TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
sys.path.insert(0, TOOLS); os.chdir(TOOLS)
import mota_core as M
import z2_route as Z
import run_segs
orig = M.World.move
step = [0]
def mv(self, dx, dy):
    step[0]+=1
    return orig(self,dx,dy)
M.World.move = mv
of = M.World.fly
def fy(self,tf):
    step[0]+=1
    return of(self,tf)
M.World.fly = fy
# 跑到 34F 第二次访问前
rc = Z.main()
