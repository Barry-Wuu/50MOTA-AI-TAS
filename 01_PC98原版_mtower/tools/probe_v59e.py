# -*- coding: utf-8 -*-
"""V59 验证探针：跑完整路线到 39F，dump 31F 布局与 V59 末状态。"""
import os
import sys
import io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import z2_route

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 只 dump 31F（fly 落点层）
os.environ['MOTA_PROBE_FLOOR'] = '31'

rc = z2_route.main()
sys.exit(rc)
