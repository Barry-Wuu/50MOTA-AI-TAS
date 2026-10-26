#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出指定楼层所有怪的属性，以及给定 ATK/DEF 下的战斗成本。"""
import sys, math
import mota_core as M

def cost(hp, atk, dfn, hatk, hdfn):
    per = hatk * M.MULT.get(atk, 1) - dfn if hasattr(M, 'MULT') else None
    return per

def main():
    args = sys.argv[1:]
    hatk, hdfn = 27, 45
    if args and ':' in args[0]:
        a, b = args[0].split(':')
        hatk, hdfn = int(a), int(b)
        args = args[1:]
    fs = [int(x) for x in args]
    print('英雄 ATK%d DEF%d' % (hatk, hdfn))
    for f in fs:
        print('--- %dF' % f)
        for y in range(1, 12):
            for x in range(1, 12):
                o = M.obj_raw(f, x, y)
                if not o:
                    continue
                if M.TYPE.get(M.oatr(o, 3)) != 'MONSTER':
                    continue
                nm = M.oname(o)
                mhp = M.oatr(o,10); matk = M.oatr(o,11); mdfn = M.oatr(o,12)
                mult = 1
                per = hatk * mult - mdfn
                if per <= 0:
                    s = '打不动'
                else:
                    turns = math.ceil(mhp / per)
                    loss = max(matk - hdfn, 0) * (turns - 1)
                    s = '%d 回合 -%d' % (turns, loss)
                print('  (%2d,%2d) %-12s HP%-5d ATK%-4d DEF%-3d  %s' % (x, y, nm, mhp, matk, mdfn, s))

main()
