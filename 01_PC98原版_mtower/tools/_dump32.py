# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

def cell_desc(f, x, y):
    o = M.obj_raw(f, x, y)
    t = M.terrain(f, x, y)
    if not o and t in (0, None):
        return None
    parts = []
    if o:
        ty = M.TYPE.get(M.oatr(o, 3))
        parts.append('obj%d[%s:%s]' % (o, M.oname(o), ty))
    else:
        parts.append('terrain=%s' % t)
    return ','.join(parts)

f = 32
print('=== 32F 全部非空格 (x,y) 描述 ===')
for y in range(1, 12):
    row = []
    for x in range(1, 12):
        d = cell_desc(f, x, y)
        if d:
            row.append('(%d,%d)%s' % (x, y, d))
    if row:
        print(' y%-2d: %s' % (y, ' | '.join(row)))
