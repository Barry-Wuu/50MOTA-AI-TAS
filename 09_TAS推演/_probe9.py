# -*- coding: utf-8 -*-
"""重放到 9F(6,2)，探测 9F 可达区"""
import manual as U

U.execute(U.PLAN, verbose=False)
print('当前:', U.st())
U.reach_report(9)
