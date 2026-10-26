#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""grid.py —— 带坐标标注的楼层图。每个格子打印「地形符号 + 物件缩写」。

用法: python3 grid.py 12
"""
import sys
import mota_core as M

SYM = {1: '#', 2: 'T'}


def main():
    f = int(sys.argv[1])
    up, dn = set(), set()
    for (wf, x, y), (tf, tx, ty) in M.WARP.items():
        if wf != f:
            continue
        (up if tf > wf else dn).add((x, y))
    print('%dF   (#=墙 ^上 v下  m怪 D门 k钥 +物 $商 L熔岩 A祭坛)' % f)
    print('     ' + ''.join('%X' % x for x in range(13)))
    for y in range(13):
        cells = []
        for x in range(13):
            t = M.terrain(f, x, y)
            o = M.obj_raw(f, x, y)
            if t == 1:
                s = '#'
            elif (x, y) in up:
                s = '^'
            elif (x, y) in dn:
                s = 'v'
            else:
                s = '.'
            if o:
                ty2 = M.TYPE.get(M.oatr(o, 3))
                ab = {'MONSTER': 'm', 'DOOR': 'D', 'SHOP': '$', 'SELL': '$',
                      'STATUS': '+', 'KEY': 'k', 'SAIDAN': 'A'}.get(ty2, '?')
                if o == 79:
                    ab = 'L'
                if o in (21, 22, 23):
                    ab = 'A'
                if o == 89:
                    ab = 'w'
                if o == 115:
                    ab = 'i'
                s = ab if ab != '?' else s
            cells.append(s)
        print('%3d  %s' % (y, ''.join(cells)))
    print()
    print('图例: m=怪 D=门(黄/蓝/红/暗) $=商店 +=状态物 k=钥匙 L=熔岩 A=祭坛')
    print()
    print('--- 物件全表 ---')
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if o:
                ty2 = M.TYPE.get(M.oatr(o, 3))
                print('  (%2d,%2d) obj%-4d %-8s %s' % (x, y, o, ty2, M.oname(o)[:34]))


if __name__ == '__main__':
    main()
