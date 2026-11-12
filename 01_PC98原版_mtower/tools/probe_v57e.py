# -*- coding: utf-8 -*-
"""V57 验证探针：跑完整路线至 V57 终点（38F），转储 12F/38F 布局。"""
import os
os.environ['MOTA_PROBE_FLOOR'] = '12,38'
import z2_route

if __name__ == '__main__':
    import sys
    sys.exit(z2_route.main())
