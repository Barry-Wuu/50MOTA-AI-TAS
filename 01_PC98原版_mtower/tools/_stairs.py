# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M
for f in range(30, 42):
    s = M.STAIRS.get(f)
    print('%2dF: stairs=%s  FLY_LAND=%s' % (f, s, M.FLY_LAND.get(f)))
