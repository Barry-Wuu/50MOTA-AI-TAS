# -*- coding: utf-8 -*-
"""重放到 5F(1,2)，探测 5F 可达区"""
import manual as U

n = min(i for i, a in enumerate(U.PLAN)
        if a[0] == 's' and a[1] == 6 and a[2] == 1 and a[3] == 1)
U.execute(U.PLAN[:n + 1], verbose=False)
print('当前:', U.st())
U.reach_report(5)
