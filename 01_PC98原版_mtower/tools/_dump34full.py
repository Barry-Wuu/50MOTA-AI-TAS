# -*- coding: utf-8 -*-
"""Dump 34F full static layout: cells, monsters, doors, keys, terrain."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

print('=== 34F STATIC FULL ===')
for y in range(13):
    row = []
    for x in range(13):
        o = M.obj_raw(34, x, y)
        t = M.terrain(34, x, y)
        ch = '#'
        if t != 1:
            ch = '.'
        if o:
            if o in M.KEY_OF:
                ch = {'y': 'y', 'b': 'b', 'r': 'r'}[M.KEY_OF[o]]
            elif o in M.DOOR_OF:
                ch = {'y': 'Y', 'b': 'B', 'r': 'R'}[M.DOOR_OF[o]]
            else:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                ch = {'MONSTER': 'm', 'ITEM': '!', 'STATUS': '+', 'MESSAGE': '?'}.get(ty, '?')
        row.append(ch)
    print('%2d %s' % (y, ' '.join(row)))
print('   ' + ' '.join('%X' % x for x in range(13)))
print()
for y in range(13):
    for x in range(13):
        o = M.obj_raw(34, x, y)
        if not o:
            continue
        ty = M.TYPE.get(M.oatr(o, 3), '?')
        c10, c11, c12, c13 = (M.oatr(o, c) for c in (10, 11, 12, 13))
        if o in M.KEY_OF:
            tag = {'y': '黄钥', 'b': '蓝钥', 'r': '红钥'}[M.KEY_OF[o]]
        elif o in M.DOOR_OF:
            tag = {'y': '黄门', 'b': '蓝门', 'r': '红门'}[M.DOOR_OF[o]]
        elif ty == 'MONSTER':
            tag = 'HP%d ATK%d DEF%d 金%d' % (c10, c11, c12, c13)
        elif ty in ('ITEM', 'STATUS'):
            tag = 'HP%s ATK%s DEF%s 价%s' % tuple(('%d' % v if v else '-') for v in (c10, c11, c12, c13))
        else:
            tag = ''
        print('  (%2d,%2d) obj%-3d %-8s %-16s %s' % (x, y, o, ty, M.oname(o), tag))
print('--- done ---')
