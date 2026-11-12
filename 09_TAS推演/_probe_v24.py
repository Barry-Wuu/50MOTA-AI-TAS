# -*- coding: utf-8 -*-
"""V24 探针：19F(11,1) → 楼梯旁 → 飞 6F → 6F(11,11) → 7F → 8F → 9F。只探路，不改 z2_route。"""
import sys, io, os
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import z2_route, run_segs, mota_core as M

buf = io.StringIO()
old = sys.stdout
sys.stdout = buf
rc = z2_route.main()
sys.stdout = old
print('z2 rc =', rc, '|', buf.getvalue().strip().splitlines()[-1])

w = run_segs.LAST_W
h = w.hero
print('START:', z2_route.st(h))

os.environ['Z2_PATH'] = '1'
print('\n--- 19F 走到 (7,11)（(6,11) 楼梯邻格，应为已清路径）---')
if not z2_route.goto(w, 7, 11, '19F->(7,11)'):
    print('!! 19F 到 (7,11) 失败'); sys.exit(1)
print('  state:', z2_route.st(h))

print('\n--- 飞行之珠 19F -> 6F ---')
if not run_segs.fly(w, 6, '19F→6F'):
    print('!! fly 失败'); sys.exit(1)
print('  state:', z2_route.st(h))

print('\n--- 6F (1,2) -> (11,10)（(11,11) 楼梯邻格）---')
if not z2_route.goto(w, 11, 10, '6F->(11,10)'):
    print('!! 6F 到 (11,10) 失败'); sys.exit(1)
print('  state:', z2_route.st(h))

print('\n--- 6F -> 7F -> 8F -> 9F ---')
if not z2_route.stair(w, 11, 11, '6F->7F'): sys.exit(1)
if not z2_route.stair(w, 1, 1, '7F->8F'): sys.exit(1)
if not z2_route.stair(w, 6, 1, '8F->9F'): sys.exit(1)
print('END:', z2_route.st(h))

for f in (6, 7, 8, 9):
    print('\n--- %dF 剩余 ---' % f)
    for y in range(1, 12):
        for x in range(1, 12):
            o = w.at(f, x, y)
            if o:
                print('(%2d,%2d) obj%-4d %-8s %s' % (x, y, o, M.TYPE.get(M.oatr(o, 3), '?'), M.oname(o)[:20]))
