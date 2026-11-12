# -*- coding: utf-8 -*-
"""probe_v56e.py —— 实现 V56 后跑通，dump 37F 起始布局 + 落点 12F。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ['MOTA_PROBE_FLOOR'] = '37,12'
import z2_route
rc = z2_route.main()
print('rc =', rc)
