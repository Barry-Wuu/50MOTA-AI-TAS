# -*- coding: utf-8 -*-
"""盘点 45F-47F 剩余怪物金币，寻找补足 4000G 超级镐的缺口。
正确列号：hp=10, atk=11, dfn=12, gold=13（mota_core.battle 实证）。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

for f in [45, 46, 47]:
    print('=' * 70)
    print('%dF up=%s down=%s' % (f, M.STAIRS[f][0], M.STAIRS[f][1]))
    total_g = 0
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if o:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if ty == 'MONSTER':
                    g = M.oatr(o, 13)
                    total_g += g
                    print('  (%2d,%2d) obj%-3d %-10s hp%-4d atk%-4d dfn%-4d g%d' % (
                        x, y, o, M.oname(o)[:10], M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), g))
    print('  >> 该层怪物金币总值: %d' % total_g)
    print()
