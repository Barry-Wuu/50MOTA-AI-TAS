# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
w = M.World.new()
for (x,y) in [(5,10),(5,11),(6,10),(6,11),(7,10),(7,11),(6,9),(3,10),(1,10),(1,11),(2,11),(3,11),(3,3)]:
    o = w.at(1,x,y); ty = M.TYPE.get(M.oatr(o,3),'?') if o else '空'
    print('1F(%d,%d) obj=%s type=%s' % (x,y,o,ty))
print('KEY_OF:', M.KEY_OF)
print('PICKUP_CELLS 含(1,5,10)?', (1,5,10) in M.PICKUP_CELLS, ' 含(1,5,11)?', (1,5,11) in M.PICKUP_CELLS)
