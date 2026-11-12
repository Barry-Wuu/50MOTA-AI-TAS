# -*- coding: utf-8 -*-
"""probe_v53.py —— V53 规划探针：跑到 V52 结束（31F(6,2)），dump 31F 完整活状态。

原理：z2_route.main() 的 V52 段末尾（line 2619-2622）已用 MOTA_PROBE_FLOOR
转储当前层。设 MOTA_PROBE_FLOOR=31 即可在 V52 落点 31F(6,2) 时 dump 31F。
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

os.environ['MOTA_PROBE_FLOOR'] = '31'
import z2_route
rc = z2_route.main()
print('rc =', rc)
