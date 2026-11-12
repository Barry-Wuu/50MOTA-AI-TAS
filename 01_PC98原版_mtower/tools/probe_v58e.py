# -*- coding: utf-8 -*-
# V58 探测：验证 38F 段（line290）——右过红门打幽灵→拿钥匙→右打幽灵→过黄门→上楼
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['MOTA_PROBE_FLOOR'] = '39'
import z2_route
sys.exit(z2_route.main())
