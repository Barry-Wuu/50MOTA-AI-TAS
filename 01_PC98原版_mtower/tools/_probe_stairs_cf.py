# -*- coding: utf-8 -*-
# 探测 41-47F 的 STAIRS + 中心对称落点（中心 = (6,6)，对称点 = (12-x, 12-y)）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

def cf_sym(x, y):
    return 12 - x, 12 - y

for f in (41, 42, 43, 44, 45, 46, 47):
    up, dn = M.STAIRS[f]
    print('=== %dF ===' % f)
    print('  STAIRS up=%s dn=%s' % (up, dn))
    # 找该层所有走格（非墙）并给出 上行梯旁可走邻格
    if up:
        sx, sy = up
        nb = []
        for d in ((0,-1),(0,1),(-1,0),(1,0)):
            ax, ay = sx+d[0], sy+d[1]
            if 1<=ax<=11 and 1<=ay<=11 and M.terrain(f,ax,ay)==0:
                nb.append((ax,ay))
        print('  上行梯 %s 旁走格: %s' % (up, nb))
    if dn:
        sx, sy = dn
        nb = []
        for d in ((0,-1),(0,1),(-1,0),(1,0)):
            ax, ay = sx+d[0], sy+d[1]
            if 1<=ax<=11 and 1<=ay<=11 and M.terrain(f,ax,ay)==0:
                nb.append((ax,ay))
        print('  下行梯 %s 旁走格: %s' % (dn, nb))

print()
print('=== 中心对称落点检验 ===')
for f, pts in {
    41: [(6,2),(6,10)],
    42: [(11,2),(1,10),(6,10),(6,2)],
}.items():
    for (x,y) in pts:
        sx, sy = cf_sym(x,y)
        t = M.terrain(f,sx,sy)
        o = M.obj_raw(f,sx,sy)
        print('  %dF(%d,%d) 中心对称→(%d,%d) terrain=%s obj=%s' % (f,x,y,sx,sy,t,o))
