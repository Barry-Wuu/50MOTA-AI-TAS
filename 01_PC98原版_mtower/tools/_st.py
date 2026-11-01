# -*- coding: utf-8 -*-
import mota_core as M
for f in (33, 34, 35, 39, 40, 41):
    print('STAIRS[%d] = %s' % (f, M.STAIRS.get(f)))
print('FLY_LAND:', {k: M.FLY_LAND.get(k) for k in (34, 40, 39, 41, 15)})
