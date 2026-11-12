# -*- coding: utf-8 -*-
"""probe_v53e.py —— V53 验证：跑完整路线（V52+V53），dump 35F 结束态。
无需环境变量（V53 末尾已自动 dump 35F，只需 MOTA_PROBE_FLOOR=35）。
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ['MOTA_PROBE_FLOOR'] = '35'
import z2_route
rc = z2_route.main()
print('rc =', rc)
