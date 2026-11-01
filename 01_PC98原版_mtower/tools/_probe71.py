# -*- coding: utf-8 -*-
import mota_core as M
w = M.World.new()
h = w.hero
# 模拟 7F 段进入状态：HP1123 A166 D133 G785 钥2/0/1
h.f, h.x, h.y = 7, 7, 1
h.hp, h.atk, h.dfn, h.gold = 1123, 166, 133, 785
h.keys['y'], h.keys['b'], h.keys['r'] = 2, 0, 1
# 7F(7,1) 是空地，向西一步到 (6,1) 商人
print('before:', h.gold, h.keys)
lg = w.move(-1, 0)
print('move1:', lg, '| pos', h.x, h.y, '| gold', h.gold, 'keys', h.keys)
lg2 = w.move(-1, 0)
print('move2:', lg2, '| pos', h.x, h.y, '| gold', h.gold, 'keys', h.keys)
