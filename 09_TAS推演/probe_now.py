# -*- coding: utf-8 -*-
"""按 manual.py 的 PLAN 执行到当前进度后，探测指定楼层的可达区与贴边关口。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演')
import manual as MAN

MAN.execute(MAN.PLAN, verbose=False)
print('当前 ' + MAN.st())
for f in [int(a) for a in sys.argv[1:] if a.isdigit()]:
    MAN.reach_report(f)
    print()
