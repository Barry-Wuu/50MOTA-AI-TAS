#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""show_floor.py —— 打印指定楼层的字符地图 + 物件清单。

用法: python3 show_floor.py 12 13 ...
地形:  #=墙  ·=地板  ^=上行梯  v=下行梯
物件:  y/b/r=钥匙  Y/B/R=门  m=怪  $=商店  D=暗墙(obj89)  !=物品  +=状态
"""
import sys
import mota_core as M


def show(f):
    print('=' * 66)
    print('%dF' % f)
    up = set()
    dn = set()
    for (sf, sx, sy), dst in M.WARP.items():
        if sf == f:
            if dst and dst[0] > f:
                up.add((sx, sy))
            elif dst and dst[0] < f:
                dn.add((sx, sy))
    for y in range(13):
        row = []
        for x in range(13):
            t = M.terrain(f, x, y)
            o = M.obj_raw(f, x, y)
            ch = '#' if t == 1 else ('^' if (x, y) in up else ('v' if (x, y) in dn else '·'))
            if o:
                if o in M.KEY_OF:
                    ch = {'y': 'y', 'b': 'b', 'r': 'r'}[M.KEY_OF[o]]
                elif o in M.DOOR_OF:
                    ch = {'y': 'Y', 'b': 'B', 'r': 'R'}[M.DOOR_OF[o]]
                elif o == 89:
                    ch = 'D'
                elif o in M.SHOP:
                    ch = '$'
                else:
                    ty = M.TYPE.get(M.oatr(o, 3), '?')
                    ch = {'MONSTER': 'm', 'ITEM': '!', 'STATUS': '+', 'MESSAGE': '?'}.get(ty, '?')
            row.append(ch)
        print('%2d %s' % (y, ' '.join(row)))
    print('   ' + ' '.join('%X' % x for x in range(13)))
    # 物件表
    items = []
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            c10, c11, c12, c13 = (M.oatr(o, c) for c in (10, 11, 12, 13))
            tag = ''
            if o == 89:
                tag = '暗墙'
            elif o in M.KEY_OF:
                tag = {'y': '黄钥', 'b': '蓝钥', 'r': '红钥'}[M.KEY_OF[o]]
            elif o in M.DOOR_OF:
                tag = {'y': '黄门', 'b': '蓝门', 'r': '红门'}[M.DOOR_OF[o]]
            elif o in M.SHOP:
                tag = '商店'
            elif ty == 'MONSTER':
                tag = 'HP%d ATK%d DEF%d 金%d' % (c10, c11, c12, c13)
            elif ty in ('ITEM', 'STATUS'):
                tag = 'HP%s ATK%s DEF%s 价%s' % tuple(
                    ('%d' % v if v else '-') for v in (c10, c11, c12, c13))
            items.append('  (%2d,%2d) obj%-3d %-8s %s %s' % (x, y, o, ty, M.oname(o), tag))
    print('--- 物件 (%d) ---' % len(items))
    for s in items:
        print(s)
    w = M.FLOOR_WRITES.get(f)
    if w:
        print('--- 进层写入 ---')
        for (x, y, o) in w:
            print('  (%2d,%2d) <- obj%d %s' % (x, y, o, M.oname(o)))


if __name__ == '__main__':
    for a in sys.argv[1:]:
        show(int(a))
