# -*- coding: utf-8 -*-
"""V61 终点验证：跑全程到 V61 末，dump 31F 确认落点。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['MOTA_PROBE_FLOOR'] = '31'
import z2_route
sys.exit(z2_route.main())
