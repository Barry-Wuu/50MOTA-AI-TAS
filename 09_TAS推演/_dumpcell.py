# -*- coding: utf-8 -*-
"""逐格打印指定楼层的 (x,y) terrain/obj/type，便于精确核对。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W = M.World.new()
f = int(sys.argv[1])

for y in range(1, 12):
    for x in range(1, 12):
        t = W.terrain_at(f, x, y)
        o = W.at(f, x, y)
        if t in (1, 2):
            continue
        if not o:
            continue
        ty = M.TYPE.get(M.oatr(o, 3), '?')
        extra = ''
        if ty == 'MONSTER':
            extra = ' hp=%d atk=%d def=%d g=%d' % (
                M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13))
        print('(%2d,%2d) t=%d obj%-4d %-9s %s%s' % (x, y, t, o, ty, M.oname(o)[:20], extra))
print('stairs:', M.STAIRS.get(f))
