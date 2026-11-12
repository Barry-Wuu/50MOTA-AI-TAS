# -*- coding: utf-8 -*-
# 探测 39F 的 obj106/107 实际位置 + 12点/3点黄门区布局
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

print('=== 39F 全部物件（非0）===')
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        o = M.obj_raw(39, x, y)
        if o:
            row.append('(%d,%d)=%d%s' % (x, y, o, M.oname(o)[:6] if M.oname(o) else ''))
    if row:
        print('  ' + '; '.join(row))

print()
print('=== 39F terrain==0（走格）全图 ===')
for y in range(1, 12):
    row = ''
    for x in range(1, 12):
        row += '.' if M.terrain(39, x, y) == 0 else '#'
    print('  %2d %s' % (y, row))
print('     ' + ''.join(str(x) for x in range(1,12)))
