# -*- coding: utf-8 -*-
"""定位 obj106 中心对称飞行器 & 39F 地形全图"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import mota_core as M

print('=== 全塔静态 obj106 出现位置 ===')
hit = []
for f in M.WALKABLE:
    for y in range(13):
        for x in range(13):
            if M.obj_raw(f, x, y) == 106:
                hit.append((f, x, y))
print('  ', hit if hit else '（静态图中无 obj106）')

print()
print('=== FLOOR_WRITES 里 obj106 ===')
for f, lst in sorted(M.FLOOR_WRITES.items()):
    for x, y, o in lst:
        if o == 106:
            print('   %dF(%d,%d)=obj106' % (f, x, y))

print()
print('=== 39F 地形全图（obj%100；<> = 楼梯）===')
f = 39
for y in range(13):
    row = ''
    for x in range(13):
        if M.terrain(f, x, y) == 1:
            row += '##'
            continue
        o = M.obj_raw(f, x, y)
        if M.terrain(f, x, y) == 2:
            row += '<>'
        elif o:
            row += '%2d' % (o % 100)
        else:
            row += ' .'
    print(' y%2d %s' % (y, row))
print('     ' + ''.join('%2d' % x for x in range(13)))
print()
print('39F STAIRS / FLY_LAND:', M.STAIRS[39], M.FLY_LAND[39])
print()
print('=== 39F 带动态写入（模拟进层）后的物件表 ===')
w = M.World.new()
w.apply_floor_events(39)
for y in range(13):
    cells = []
    for x in range(13):
        o = w.at(39, x, y)
        if o:
            cells.append('(%d,%d)=%d %s' % (x, y, o, M.oname(o)[:14]))
    if cells:
        print('  y%-2d %s' % (y, ' | '.join(cells)))
