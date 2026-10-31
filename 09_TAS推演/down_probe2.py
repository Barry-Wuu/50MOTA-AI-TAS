# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
w = M.World.new()
# 遍历所有层楼梯，测试 move 到楼梯格后落点
DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
for f in range(1, 12):
    for y in range(13):
        for x in range(13):
            if w.terrain_at(f, x, y) == 2:
                # 站到楼梯邻格
                for dx, dy in DIRS:
                    nx, ny = x+dx, y+dy
                    if not (0<=nx<13 and 0<=ny<13): continue
                    if w.terrain_at(f, nx, ny) != 0 and w.terrain_at(f, nx, ny) != 2: continue
                    # 复制世界，站邻格，朝楼梯走
                    c = w.clone()
                    c.hero.f, c.hero.x, c.hero.y = f, nx, ny
                    lg = c.move(x-nx, y-ny)
                    if lg and any('楼梯' in e or '移動' in e or '階' in e for e in lg):
                        print('%dF(%d,%d)楼梯 从(%d,%d)走 -> %s' % (f, x, y, nx, ny, lg))
                        break
