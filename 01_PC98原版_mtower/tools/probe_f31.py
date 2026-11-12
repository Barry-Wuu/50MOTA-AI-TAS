# -*- coding: utf-8 -*-
"""探查 31F：楼梯(up/dn)、FLY_LAND、对象清单（找双手剑士/钥匙）、WARP 连通性。"""
import os
import sys
import io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import mota_core as mc

print('STAIRS[31] =', mc.STAIRS.get(31))
print('STAIRS[38] =', mc.STAIRS.get(38))
print('FLY_LAND[31] =', mc.FLY_LAND.get(31))
print('FLY_LAND[38] =', mc.FLY_LAND.get(38))
print('FLY_LAND[32] =', mc.FLY_LAND.get(32))
print()

# 31F 楼梯连通：检查 31F 的上行梯/下行梯各自通向哪层
for f in (31, 38, 32):
    up, dn = mc.STAIRS.get(f, (None, None))
    print(f'{f}F 楼梯: up={up} dn={dn}')
    if up:
        t = mc.terrain(f, up[0], up[1])
        print(f'   up 梯 terrain={t}, stair_up={mc.stair_up(f, up[0], up[1]) if hasattr(mc,"stair_up") else "?"}')
    if dn:
        print(f'   dn 梯 terrain={mc.terrain(f, dn[0], dn[1])}')
print()

# WARP 中涉及 31F / 38F 的条目
print('WARP 条目（含31F/38F作为源或目标）:')
for (sf, sx, sy), (tf, tx, ty) in mc.WARP.items():
    if sf in (31, 38) or tf in (31, 38):
        print(f'   ({sf}F,{sx},{sy}) -> ({tf}F,{tx},{ty})')
print()

# 31F 对象清单（完整）
print('=== 31F 全部对象 ===')
cnt = 0
for y in range(13):
    for x in range(13):
        o = mc.obj_raw(31, x, y)
        if o:
            name = mc.oname(o)
            otype = mc.OATYPE.get(o, '?') if hasattr(mc, 'OATYPE') else '?'
            # 打印 obj 类型名（对象表 OA 的第0列可能是类型）
            t = mc.oatr(o, 0) if hasattr(mc, 'oatr') else '?'
            print(f'  ({x:2d},{y:2d}) obj{o}  type={t}  {name}')
            cnt += 1
print(f'--- 共 {cnt} 个对象 ---')
print()

# 打印 31F 地形网格（0=空 1=墙 2=楼梯）
print('=== 31F 地形（0空/1墙/2梯）===')
for y in range(13):
    row = ''.join(str(mc.terrain(31, x, y)) for x in range(13))
    print(f'  {row}')
