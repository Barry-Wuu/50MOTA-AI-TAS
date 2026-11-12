# -*- coding: utf-8 -*-
"""重放到 4F 祭坛后，探测 4F 可达格与贴边关口"""
import manual as U

U.execute(U.PLAN[:-2], verbose=False)
print('当前:', U.st())
U.reach_report(4)
