# -*- coding: utf-8 -*-
"""在 PLAN 执行后的世界状态下，把主角临时放到指定格，探测该层可达区与贴边关口。
用法: python probe_at.py 8 6 2    （层 8F 格(6,2)）"""
import sys
import manual as m

m.execute(verbose=False)
W = m.W
f, x, y = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
W.hero.f, W.hero.x, W.hero.y = f, x, y
print('当前 ' + m.st())
m.reach_report(f)
