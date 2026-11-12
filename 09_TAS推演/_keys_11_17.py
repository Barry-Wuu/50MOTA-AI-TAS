# -*- coding: utf-8 -*-
import sys
TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
sys.path.insert(0, TOOLS)
import mota_core as M

for f in range(11, 18):
    print('==== %dF ====' % f)
    keys, doors = [], []
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3))
            if o in M.KEY_OF:
                keys.append('(%2d,%2d)obj%d' % (x, y, o))
            elif ty == 'DOOR':
                doors.append('(%2d,%2d)obj%d' % (x, y, o))
    print('  KEY : ' + ' '.join(keys))
    print('  DOOR: ' + ' '.join(doors))
    print()
