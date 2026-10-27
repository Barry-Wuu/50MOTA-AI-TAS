#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 20F 相关机制补充：十字架双倍、19F 暗墙获十字架、(20,6,9) 杀 BOSS 才开门禁。"""
import mota_core as M

print('=== 1) 吸血鬼(obj59) 战斗：有/无十字架 ===')
for cross in (True, False):
    w = M.World.new(); h = w.hero
    h.hp, h.atk, h.dfn = 800, 77, 47
    if cross:
        h.items = {103}
    r = w.battle(59)
    print('  十字架=%s battle=%s' % (cross, r))
    # 用 move 全流程模拟：直接把英雄放 20F(6,6) 旁，撞吸血鬼
    w2 = M.World.new(); h2 = w2.hero
    h2.f, h2.x, h2.y = 20, 6, 7
    h2.hp, h2.atk, h2.dfn = 800, 77, 47
    if cross:
        h2.items = {103}
    # 走到 (6,6) 吸血鬼
    lg = w2.move(0, -1)  # (6,7)->(6,6)
    print('  十字架=%s 走(6,6)后 hp=%s boss20=%s log尾=%s' % (cross, h2.hp, w2.boss20, lg[-1] if lg else lg))

print('=== 2) 19F 暗墙 (19,6,3) 撞开获十字架 ===')
w = M.World.new(); h = w.hero
h.f, h.x, h.y = 19, 6, 2
lg = w.move(0, 1)  # (6,2)->(6,3) 暗墙
print('  撞墙后 items=%s log=%s' % (h.items, [l for l in lg if '十字' in l or '暗墙' in l]))

print('=== 3) (20,6,9) 门禁：未 boss20 挡路，boss20 后放行 ===')
w = M.World.new(); h = w.hero
h.f, h.x, h.y = 20, 6, 10
lg = w.move(0, -1)  # (6,10)->(6,9)
print('  未 boss20: log=%s' % lg)
w.boss20 = True
lg2 = w.move(0, -1)
print('  已 boss20: hp=%s log尾=%s' % (h.hp, lg2[-1] if lg2 else lg2))

print('=== 4) 19F/20F 入口 WARP 链路 ===')
print('  19F(6,11)→', M.WARP.get((19, 6, 11)))
print('  20F(6,11)→', M.WARP.get((20, 6, 11)))
print('  17F(6,1)→', M.WARP.get((17, 6, 1)))
print('  18F(1,1)→', M.WARP.get((18, 1, 1)))
