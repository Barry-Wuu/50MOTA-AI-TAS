# -*- coding: utf-8 -*-
# 验证：45F(2,10) 是否静态 obj107；39F(4,4) 原始与事件后；DYNEV 39F 原始条目
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
import json

print('=== 45F obj_raw(2,10) ===')
o = M.obj_raw(45, 2, 10)
print('  45F(2,10) = obj%d %s' % (o, M.oname(o)))

print()
print('=== 39F(4,4) 静态 obj_raw ===')
o = M.obj_raw(39, 4, 4)
print('  39F(4,4) 静态 = obj%d %s' % (o, M.oname(o)))

# DYNEV 里 floor==39 的 obj 写入（查源）
print()
print('=== DYNEV floor=39 的 obj 条目 ===')
for e in M.DYNEV.get('obj', []):
    if e.get('floor') == '39' or e.get('floor') == 39:
        print('  ', e)
print()
print('=== DYNEV floor=45 的 obj 条目 ===')
for e in M.DYNEV.get('obj', []):
    if e.get('floor') == '45' or e.get('floor') == 45:
        print('  ', e)

print()
print('=== 45F 全部物件（非0）===')
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        o = M.obj_raw(45, x, y)
        if o:
            row.append('(%d,%d)=%d%s' % (x, y, o, M.oname(o)[:8] if M.oname(o) else ''))
    if row:
        print('  ' + '; '.join(row))
