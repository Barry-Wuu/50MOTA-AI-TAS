# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
w = M.World.new()
# 直接踩 8F(10,4) 落穴
w.hero.f, w.hero.x, w.hero.y = 8, 10, 5
lg = w.move(0, -1)  # (10,5)->(10,4)
print('踩落穴:', lg)
print('位置:', w.hero.f, w.hero.x, w.hero.y, 'HP', w.hero.hp)
# 继续到红钥
lg = w.move(0, -1); print('->(10,3):', lg)
lg = w.move(0, -1); print('->(10,2):', lg)
