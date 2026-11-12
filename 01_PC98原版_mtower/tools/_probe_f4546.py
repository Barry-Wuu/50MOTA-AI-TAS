# -*- coding: utf-8 -*-
"""盘点 45F/46F/47F 完整怪物与金币分布，评估 V80 补 99G 缺口的路径。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

A, D = 217, 201  # V79 后属性（圣剑已拿）

def battle_loss(o):
    """计算单次战斗战损（mota_core.battle 同款公式）。"""
    hp, atk, dfn, gold = M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13)
    per = A - dfn
    if per <= 0:
        return None, gold
    return max(atk - D, 0) * (int(-(-hp // per)) - 1), gold

for f in [45, 46, 47]:
    print('=' * 72)
    print('%dF up=%s down=%s  STAIRS' % (f, M.STAIRS[f][0], M.STAIRS[f][1]))
    tot = 0
    mon = []
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if o:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if ty == 'MONSTER':
                    hp, atk, dfn, gold = M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13)
                    loss, _ = battle_loss(o)
                    tot += gold
                    mon.append((x, y, o, M.oname(o)[:8], hp, atk, dfn, gold, loss))
    print('  怪物总值: %dG  数量: %d' % (tot, len(mon)))
    for m in sorted(mon, key=lambda t: -t[8] if t[8] else 0):
        print('   (%2d,%2d) obj%-3d %-8s hp%3d atk%3d dfn%3d g%3d  战损=%s' % (
            m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8]))
    print('  非怪物件:')
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if o:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if ty != 'MONSTER':
                    print('   (%2d,%2d) obj%-3d %-10s %s' % (x, y, o, M.oname(o)[:10], ty))
