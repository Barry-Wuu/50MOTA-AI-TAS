# -*- coding: utf-8 -*-
"""probe_v55e.py —— V55 验证：跑完整路线（V52+V53+V54+V55），dump 37F 结束态。
无需环境变量（V55 末尾已自动 dump 37F，只需 MOTA_PROBE_FLOOR=37）。
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ['MOTA_PROBE_FLOOR'] = '37'
import z2_route
rc = z2_route.main()
print('rc =', rc)
