# -*- coding: utf-8 -*-
"""probe_v56w.py —— 校验 WARP/STAIRS/FLY_LAND 关键楼层连接（37F/12F/38F）。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

print('STAIRS[37]=', M.STAIRS[37], ' STAIRS[12]=', M.STAIRS[12], ' STAIRS[38]=', M.STAIRS[38])
print('FLY_LAND[12]=', M.FLY_LAND[12], ' FLY_LAND[38]=', M.FLY_LAND[38], ' FLY_LAND[39]=', M.FLY_LAND[39])
for f in (37, 12, 38, 39):
    wr = [(k, v) for k, v in M.WARP.items() if k[0] == f]
    print('WARP[%d]=%s' % (f, wr))
