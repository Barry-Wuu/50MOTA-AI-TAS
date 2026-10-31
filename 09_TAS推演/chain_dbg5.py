# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

w = M.World.new()
for (x,y) in [(8,11),(9,11),(10,10),(8,9),(10,9),(9,10),(10,11)]:
    o = w.at(1,x,y)
    print('1F(%d,%d) obj=%s type=%s' % (x,y,o, M.TYPE.get(M.oatr(o,3),'?') if o else '空'))
    if o and M.TYPE.get(M.oatr(o,3))=='MONSTER':
        print('   hp=%s atk=%s def=%s gold=%s' % (M.oatr(o,10),M.oatr(o,11),M.oatr(o,12),M.oatr(o,13)))
# 试打 (8,11)
w2=w.clone(); log=w2.move(1,0)  # 从(7,11)向右
print('move right from (7,11):', log[:1])
