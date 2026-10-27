#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recon.py —— 人类式侦察：把 1-17 层每层的怪物(四维)与关键道具位置列出，
供手排路线用（不求解，只报事实）。输出到 stdout，可重定向到文件。
"""
import sys
import mota_core as M

ROLE_INTEREST = {'MONSTER', 'DOOR', 'KEY', 'STATUS', 'ITEM', 'SAIDAN', 'SHOP', 'MESSAGE', 'SCORE', 'NORMAL'}


def monster_line(f, x, y, o):
    a = [M.oatr(o, c) for c in range(14)]
    return '  MON %2d,%-2d %-10s HP%-5s ATK%-4s DEF%-4s G%s' % (
        x, y, M.oname(o)[:8], a[10], a[11], a[12], a[13])


def item_line(f, x, y, o, ty):
    a = [M.oatr(o, c) for c in range(14)]
    gain = 'HP%+d ATK%+d DEF%+d' % (a[10], a[11], a[12]) if (a[10] or a[11] or a[12]) else ''
    col = M.DOOR_OF.get(o)
    keyc = M.KEY_OF.get(o)
    if ty == 'DOOR':
        name = '%s(%s)' % (M.oname(o)[:6], {None:'?', 'y':'黄', 'b':'蓝', 'r':'红'}.get(col))
    elif ty == 'KEY':
        name = '%s(%s)' % (M.oname(o)[:6], {None:'?', 'y':'黄', 'b':'蓝', 'r':'红'}.get(keyc))
    else:
        name = M.oname(o)[:10]
    return '  %-4s %2d,%-2d %-12s %s' % (ty[:4], x, y, name, gain)


def recon_floor(f):
    print('================ %2dF ================' % f)
    up = M.stairs_of(f) if hasattr(M, 'stairs_of') else None
    # 楼梯
    for y in range(1, 12):
        for x in range(1, 12):
            t = M.terrain(f, x, y)
            if t == 2:
                print('  STAIR %2d,%-2d (地形=楼梯)' % (x, y))
    # 暗墙 obj89
    dws = []
    for y in range(1, 12):
        for x in range(1, 12):
            if M.obj_raw(f, x, y) == 89:
                dws.append((x, y))
    if dws:
        print('  DARKWALL(obj89) ' + ' '.join('%d,%d' % c for c in dws))
    # 祭坛 obj22
    for (af, ax, ay) in M.ALTAR_CELLS:
        if af == f:
            print('  ALTAR(obj22) %d,%d' % (ax, ay))
    # 动态写入/事件
    for y in range(1, 12):
        for x in range(1, 12):
            o = M.obj_raw(f, x, y)
            if o and o in M.SHOP:
                print('  SHOP %2d,%-2d obj%d %s' % (x, y, o, M.oname(o)[:10]))
    # 怪物与道具
    mons = []
    items = []
    for y in range(1, 12):
        for x in range(1, 12):
            o = M.obj_raw(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            if ty == 'MONSTER':
                mons.append(monster_line(f, x, y, o))
            elif ty in ('DOOR', 'KEY', 'STATUS', 'ITEM', 'MESSAGE', 'SCORE'):
                items.append(item_line(f, x, y, o, ty))
    for s in mons:
        print(s)
    for s in items:
        print(s)


if __name__ == '__main__':
    fl = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else list(range(1, 18))
    for f in fl:
        recon_floor(f)
