# -*- coding: utf-8 -*-
import mota_core as M
f = 34
print('=== %dF 布局（行=y，列=x）===' % f)
hdr = '    ' + ''.join('%3d' % x for x in range(1, 12))
print(hdr)
for y in range(1, 12):
    row = '%2d  ' % y
    for x in range(1, 12):
        t = M.terrain(f, x, y)
        o = M.obj_raw(f, x, y)
        if t == 1:
            ch = '#'   # 墙
        elif t == 2:
            ch = '='   # 楼梯
        elif o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            nm = M.oname(o)[:3]
            ch = nm
        else:
            ch = '.'
        row += '%3s' % ch[:3]
    print(row)
print()
print('--- 对象明细 ---')
for y in range(1, 12):
    for x in range(1, 12):
        o = M.obj_raw(f, x, y)
        if o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            hp = M.oatr(o, 10); atk = M.oatr(o, 11); dfn = M.oatr(o, 12); g = M.oatr(o, 13)
            print('(%2d,%2d) obj%-3d %-12s hp%-5s atk%-5s def%-5s g%-5s  %s' % (
                x, y, o, ty, hp, atk, dfn, g, M.oname(o)[:40]))
