# -*- coding: utf-8 -*-
"""手推所需静态数据：道具数值 / 楼梯落点 / 11F 地图。不做任何搜索。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

print('=== 道具数值 (id: type hp atk def gold) ===')
for o in (1, 2, 3, 4, 11, 12, 13, 14, 19, 20, 21, 22, 23, 26, 27, 28, 29, 30, 35,
          41, 87, 89, 152, 174, 16, 5, 6, 7, 8, 9, 10, 15, 58):
    print('  obj%-4d %-8s %-9s hp=%-4s atk=%-4s def=%-4s gold=%-4s %s' % (
        o, M.oatr(o, 3), M.TYPE.get(M.oatr(o, 3), '?'),
        M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13), M.oname(o)))

print('\n=== 楼梯 STAIRS / WARP (1..11F) ===')
for f in range(1, 12):
    print('  %2dF up/down=%s' % (f, M.STAIRS.get(f)))
print('  WARP:')
for k in sorted(M.WARP):
    if k[0] <= 11:
        print('    %s -> %s' % (k, M.WARP[k]))

print('\n=== 11F 地图 ===')
f = 11
print('--- terrain ---')
for y in range(13):
    row = ''
    for x in range(13):
        t = M.terrain(f, x, y)
        row += {0: '.', 1: '#', 2: 'S'}.get(t, '?')
    print('y%-3d %s' % (y, row))
print('--- obj ---')
for y in range(13):
    row = ''
    for x in range(13):
        o = M.obj_raw(f, x, y)
        row += ('%-4d' % o) if o else '  . '
    print('y%-3d %s' % (y, row))
print('--- obj detail ---')
for y in range(13):
    for x in range(13):
        o = M.obj_raw(f, x, y)
        if o:
            print('  (%2d,%2d) obj%-4d %-10s type=%-8s hp=%s atk=%s def=%s g=%s' % (
                x, y, o, M.oname(o)[:10], M.TYPE.get(M.oatr(o, 3), '?'),
                M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13)))
