# -*- coding: utf-8 -*-
"""确认 48F→47F 下楼梯落点与 47F/48F 楼梯配置。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

for f in (46, 47, 48):
    up, dn = M.stairs_of(f)
    print('%dF 楼梯: up=%s dn=%s' % (f, up, dn))
    # 落点数据
    print('   FLY_LAND[%d] = %s' % (f, M.FLY_LAND.get(f)))
