# -*- coding: utf-8 -*-
"""V80 探针：查 47F/46F 楼梯 WARP 精确落点 + 46F 全部门/怪/物件坐标。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

print('===== 楼梯 WARP 表（关键段） =====')
for f in (47, 46, 45, 48, 44):
    up, dn = M.STAIRS.get(f, (None, None))
    wu = M.WARP.get((f, *up)) if up else None
    wd = M.WARP.get((f, *dn)) if dn else None
    print('%dF: up=%s -> %s | dn=%s -> %s' % (f, up, wu, dn, wd))

print()
print('===== 46F 全部物件（门/怪/钥匙/道具） =====')
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        o = M.obj_raw(46, x, y)
        if not o:
            row.append('   .  ')
            continue
        ty = M.TYPE.get(M.oatr(o, 3), '?')
        if ty == 'MONSTER':
            hp, atk, dfn, gold = M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13)
            row.append('o%03d%s' % (o, 'M'))
        elif ty == 'DOOR':
            row.append('o%03d%s' % (o, 'D'))
        elif o in M.KEY_OF:
            row.append('o%03d%s' % (o, 'K'))
        elif ty == 'ITEM':
            row.append('o%03d%s' % (o, 'I'))
        elif ty == 'STATUS':
            row.append('o%03d%s' % (o, 'S'))
        else:
            row.append('o%03d%s' % (o, ty[0] if ty else '?'))
    print('y=%2d: %s' % (y, ' '.join(row)))

print()
print('===== 46F 怪物属性明细 =====')
seen = set()
for y in range(1, 12):
    for x in range(1, 12):
        o = M.obj_raw(46, x, y)
        if not o:
            continue
        if M.TYPE.get(M.oatr(o, 3), '?') != 'MONSTER':
            continue
        hp, atk, dfn, gold = M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13)
        print('46F(%2d,%2d) obj%d hp%d atk%d dfn%d gold%d' % (x, y, o, hp, atk, dfn, gold))

print()
print('===== 47F 剩余怪物明细（obj_raw 视图，未清） =====')
for y in range(1, 12):
    for x in range(1, 12):
        o = M.obj_raw(47, x, y)
        if not o:
            continue
        if M.TYPE.get(M.oatr(o, 3), '?') != 'MONSTER':
            continue
        hp, atk, dfn, gold = M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13)
        print('47F(%2d,%2d) obj%d hp%d atk%d dfn%d gold%d' % (x, y, o, hp, atk, dfn, gold))

print()
print('===== 46F 蓝门/B门与黄门/Y门坐标 =====')
for y in range(1, 12):
    for x in range(1, 12):
        o = M.obj_raw(46, x, y)
        if not o:
            continue
        if M.TYPE.get(M.oatr(o, 3), '?') != 'DOOR':
            continue
        col = M.DOOR_OF.get(o)
        print('46F(%2d,%2d) obj%d %s门' % (x, y, o, {'y': '黄', 'b': '蓝', 'r': '红'}.get(col, col)))
