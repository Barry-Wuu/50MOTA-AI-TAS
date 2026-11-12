# -*- coding: utf-8 -*-
"""probe_v54e.py —— V54 验证：跑完整路线（V52+V53+V54），dump 36F 结束态。
无需环境变量（V54 末尾已自动 dump 36F，只需 MOTA_PROBE_FLOOR=36）。
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ['MOTA_PROBE_FLOOR'] = '36'
import z2_route
rc = z2_route.main()
print('rc =', rc)
