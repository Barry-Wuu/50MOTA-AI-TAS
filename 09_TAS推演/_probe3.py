# -*- coding: utf-8 -*-
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import manual

PLAN = manual.PLAN
idx = [i for i, a in enumerate(PLAN) if a[0] == 'w' and a[1] == 3 and a[2] == 1 and a[3] == 11]
print('目标步索引', idx)
k = idx[0]
manual.execute(PLAN[:k], verbose=False)
h = manual.W.hero
print('当前', manual.st())
print('free(1,11)=', manual.free(3, 1, 11), 'free(2,11)=', manual.free(3, 2, 11))
seen, frontier = manual.reach_report(3)
