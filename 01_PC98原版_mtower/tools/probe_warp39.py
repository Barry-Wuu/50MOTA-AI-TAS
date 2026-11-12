# -*- coding: utf-8 -*-
"""探查 39F 的楼梯/WARP 连接，确定 39F -> 31F 的机制。"""
import os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import mota_core as mc

print('=== STAIRS[39] (up, down):', mc.STAIRS.get(39))
print('=== FLY_LAND[39]:', mc.FLY_LAND.get(39))

# 遍历 39F 所有格子，找 terrain==2（楼梯）的 WARP
print('\n=== 39F 楼梯格 WARP ===')
for y in range(13):
    for x in range(13):
        if mc.terrain(39, x, y) == 2:
            w = mc.warp_to(39, x, y)
            up = mc.stair_up(39, x, y)
            print('  (%d,%d) terrain==2 stair_up=%s WARP=%s' % (x, y, up, w))

# 检查所有 WARP 目标为 31F 的源
print('\n=== 所有 WARP 目标为 31F ===')
for k, v in mc.WARP.items():
    if v[0] == 31:
        print('  src=%s -> %s' % (k, v))

# 检查 39F 是否有 warp 到任何层（含特殊）
print('\n=== 39F 全部 WARP ===')
for k, v in mc.WARP.items():
    if k[0] == 39:
        print('  src=%s -> %s' % (k, v))

# UP_PATCH
print('\n=== UP_PATCH ===', mc.UP_PATCH)
