# -*- coding: utf-8 -*-
"""重放 z2_route.main() 后，打印指定楼层的剩余物件（运行时真值）。"""
import sys, io, os
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import z2_route, run_segs, mota_core as M

buf = io.StringIO()
old = sys.stdout
sys.stdout = buf
rc = z2_route.main()
sys.stdout = old
print('main rc =', rc, '|', buf.getvalue().strip().splitlines()[-1])

w = run_segs.LAST_W
h = w.hero
print('HERO: HP%d A%d D%d G%d keys %d/%d/%d %dF(%d,%d)' % (
    h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y))

for f in [int(a) for a in sys.argv[1:]] or [16, 18]:
    print('\n--- %dF 剩余物件 ---' % f)
    for y in range(1, 12):
        for x in range(1, 12):
            o = w.at(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            print('(%2d,%2d) obj%-4d %-9s %s' % (x, y, o, ty, M.oname(o)[:22]))
