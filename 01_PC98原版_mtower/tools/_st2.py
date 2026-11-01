# -*- coding: utf-8 -*-
import mota_core as M
for f in (15, 39, 40, 41):
    print('STAIRS[%d] = %s' % (f, M.STAIRS.get(f)))
print('FLY_LAND:', {k: M.FLY_LAND.get(k) for k in (15, 39, 40, 41)})
