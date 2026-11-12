# -*- coding: utf-8 -*-
"""probe_v56d.py —— 跑完整路线到 37F（V55 末），dump 12F/38F/39F 初始布局。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ['MOTA_PROBE_FLOOR'] = '12,38,39'
import z2_route
rc = z2_route.main()
print('rc =', rc)
