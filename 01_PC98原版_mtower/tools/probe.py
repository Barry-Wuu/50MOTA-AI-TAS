# -*- coding: utf-8 -*-
"""诊断：从给定状态出发，到本层每个资源点的「实算代价」。"""
import sys
import layer2 as L2
import mota_core as M
from guide import RES, st, g_pick

f = int(sys.argv[1]) if len(sys.argv) > 1 else 6
hp = int(sys.argv[2]) if len(sys.argv) > 2 else 162
atk = int(sys.argv[3]) if len(sys.argv) > 3 else 20
dfn = int(sys.argv[4]) if len(sys.argv) > 4 else 10
g = int(sys.argv[5]) if len(sys.argv) > 5 else 35
ky = int(sys.argv[6]) if len(sys.argv) > 6 else 2
kb = int(sys.argv[7]) if len(sys.argv) > 7 else 1
kr = int(sys.argv[8]) if len(sys.argv) > 8 else 0
sx = int(sys.argv[9]) if len(sys.argv) > 9 else 1
sy = int(sys.argv[10]) if len(sys.argv) > 10 else 2

w = L2.mk_world(f, sx, sy, hp, atk, dfn, g, ky, kb, kr)
print('起点', st(w))
for (x, y, name, kind) in RES.get(f, []):
    r = L2.plan_layer(f, w, g_pick(f, x, y), max_exp=3000000, cross=False)
    if r[0] != 'ok':
        print('  %-14s(%2d,%2d)  %s' % (name, x, y, r[0]))
        continue
    w2 = r[2][0]
    h = w2.hero
    print('  %-14s(%2d,%2d)  到达HP%-4d  ΔHP%+5d  ATK%d DEF%d G%d 钥%d/%d/%d' % (
        name, x, y, h.hp, h.hp - hp, h.atk, h.dfn, h.gold,
        h.keys['y'], h.keys['b'], h.keys['r']))
