# -*- coding: utf-8 -*-
"""验证2：manual.PLAN 终点 8F(6,2) → 9F(6,2) → 打到 (1,10) → 踏上行梯 (1,11) → 10F(1,10)。
按人类攻略 §4.2 框架机械排步。观察沿途战损是否可承受。
"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import path as P
import manual

W = P.W
print('锚点: ' + P.st())

P.stair(8, 6, 1, '8F(6,1)→9F')
print('入9F: ' + P.st())

# 打到 (1,10)（(1,11) 是楼梯格，解析式视为不可达，须走到邻格再踏）
ok = P.goto(9, 1, 10, '9F 打到 (1,10)')
print('goto (1,10) ok=%s %s' % (ok, P.st()))
if not ok:
    sys.exit(1)

# 从 (1,10) 踏上行梯 (1,11) -> 10F
P.stair(9, 1, 11, '9F(1,11)→10F')
print('入10F: ' + P.st())
