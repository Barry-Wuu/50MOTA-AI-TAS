# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

# 33F/34F 已清格（来自 33a/33b/34a 段）
clear = {
 33: {(11,3):'蓝药',(10,10):'骑士剑',(8,2):'黄门',(6,3):'黄钥',(6,1):'スライムマン',(4,1):'ゾンビナイト',(7,1):'黄门',(3,1):'黄门'},
 34: {(3,1):'赤药',(1,11):'青药',(2,6):'红钥',(1,5):'黄钥',(3,5):'黄钥',(1,7):'黄钥',(3,7):'黄钥',(2,4):'黄门',(2,8):'黄门',(4,10):'黄门',(2,3):'スライムマン',(3,9):'死霊兵士',(1,10):'剣士'},
}
for f in (33,34):
    print('=== %dF 未清内容 ===' % f)
    for y in range(1,12):
        for x in range(1,12):
            if (x,y) in clear[f]: continue
            o = M.obj_raw(f,x,y); t = M.terrain(f,x,y)
            if o:
                ty = M.TYPE.get(M.oatr(o,3))
                print('  (%d,%d) obj%d[%s:%s]' % (x,y,o,M.oname(o)[:18],ty))
    print()
