# -*- coding: utf-8 -*-
"""重放当前 PLAN，输出终态 + 3F/4F/5F/6F 可达区与贴边关口"""
import manual as U

U.execute(U.PLAN, verbose=False)
print('当前:', U.st())
for f in (3, 4, 5, 6):
    U.reach_report(f)
