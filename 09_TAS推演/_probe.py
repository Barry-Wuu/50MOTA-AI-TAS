# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

for f in (23, 24, 28, 29, 30, 31, 32):
    print(f, 'F stairs', M.STAIRS.get(f))
for c in [(23, 11, 1), (24, 2, 10), (28, 1, 11), (29, 1, 11), (29, 6, 11), (30, 6, 11), (31, 6, 2), (31, 1, 11)]:
    print(c, 'terrain', M.terrain(*c), 'obj', M.obj_raw(*c), 'warp', M.warp_to(*c))
print('30F(6,1) terrain', M.terrain(30, 6, 1), 'obj', M.obj_raw(30, 6, 1))
print('MA index for 30F(6,1) =', M.MAPT[M.rc(30, 6, 1)[0]][M.rc(30, 6, 1)[1]], 'MA entry', M.MA[M.MAPT[M.rc(30, 6, 1)[0]][M.rc(30, 6, 1)[1]]])
print('29F(6,3) terrain', M.terrain(29, 6, 3), 'obj', M.obj_raw(29, 6, 3))
# which MA idx has [16],[17] pointing to 31F(6,2)?
b, s = M.BAND_SLOT[31]
r, c = 13 + 2, 13 + 6
print('global rc of 31F(6,2)', r, c)
for idx, a in enumerate(M.MA):
    if len(a) > 17 and a[16] == c and a[17] == r:
        print('MA idx', idx, '=', a)
