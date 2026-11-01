# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

# 已清格（按各段执行记录）—— 只列关键血瓶/宝石，便于看剩余
for f, cleared, nm in [
    (31, {(8,8):'蓝药',(10,1):'血瓶',(2,11):'血瓶',(8,4):'红水晶'}, '31F'),
    (33, {(11,3):'蓝药',(10,10):'骑士剑'}, '33F'),
    (34, {(3,1):'赤药',(1,11):'青药',(2,6):'红钥',(1,5):'黄钥',(3,5):'黄钥',(1,7):'黄钥',(3,7):'黄钥'}, '34F'),
]:
    print('=== %s 关键道具（剩余未取）===' % nm)
    for y in range(1,12):
        for x in range(1,12):
            if (x,y) in cleared: continue
            o = M.obj_raw(f,x,y)
            if not o: continue
            ty = M.TYPE.get(M.oatr(o,3))
            if ty in ('STATUS',) or o in M.KEY_OF:
                # 血瓶/宝石/钥匙
                print('  (%d,%d) obj%d[%s]' % (x,y,o,M.oname(o)[:30]))
    print()
