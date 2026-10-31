# -*- coding: utf-8 -*-
"""从 PLAN 终态 8F(6,2) 逐层下行，记录各楼梯落点。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import manual
manual.execute(verbose=False)
print('起点', manual.st())
W = manual.W
# 下行：8F(1,1)->7F
def go_to(f, x, y, label):
    manual.walk(f, (x, y)); print('到 %s' % label, manual.st())
    return manual.st()
# 8F(6,2)->(1,1) 楼梯
try:
    manual.walk(8, (1, 1))
    lg = W.move(0, 0)  # 触发楼梯? 需要 move 到楼梯
except Exception as e:
    print('walk(1,1):', e)
print('在(1,1)楼梯前', manual.st())
# 直接测试 move 上楼梯
for dx, dy in [(0,0)]:
    pass
