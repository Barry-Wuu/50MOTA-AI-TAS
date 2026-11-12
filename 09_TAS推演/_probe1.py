# -*- coding: utf-8 -*-
"""重放到 1F(2,1)，探测 1F 可达区"""
import manual as U

U.execute(U.PLAN, verbose=False)
print('当前:', U.st())
U.reach_report(1)
