# -*- coding: utf-8 -*-
"""V25 预演：9F 左上骷髅战士(不伤) -> 黄钥(2,2) -> 逐层上 20F（攻略 line231）。"""
import sys, io
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import z2_route, run_segs

buf = io.StringIO(); old = sys.stdout; sys.stdout = buf
rc = z2_route.main()
sys.stdout = old
print('main rc =', rc)
w = run_segs.LAST_W
g = z2_route.goto
s = z2_route.stair
st = z2_route.st

print('起点', st(w.hero))

# ---- 9F 左上 ----
if not z2_route.need(w, y=1, label='9F 左上黄门(4,1)'): sys.exit(2)
for p in [(5,2,''),(5,1,''),(4,1,'黄门(4,1)'),(3,1,'スケルトンＣ'),
          (2,1,''),(2,2,'黄钥')]:
    if not g(w, p[0], p[1], p[2]): sys.exit(3)
print('取钥后', st(w.hero))
# ---- 左上 -> 左下上行梯 ----
for p in [(1,2,''),(1,3,'スケルトンＢ'),(1,4,''),(2,4,''),(2,5,''),(3,5,''),
          (4,5,''),(5,5,''),(6,5,''),(7,5,''),(7,6,''),(7,7,''),(7,8,''),
          (7,9,''),(7,10,''),(7,11,''),(6,11,''),(5,11,''),(5,10,''),(5,9,''),
          (5,8,''),(4,8,''),(4,7,''),(3,7,''),(2,7,''),(1,7,''),(1,8,''),
          (1,9,''),(1,10,'')]:
    if not g(w, p[0], p[1], p[2]): sys.exit(4)
print('到上行梯旁', st(w.hero))
if not s(w, 1, 11, '9F(1,11)->10F'): sys.exit(5)

# ---- 10F -> 20F 逐层 ----
if not g(w, 6, 10, '10F 到上梯旁'): sys.exit(6)
if not s(w, 6, 11, '10F(6,11)->11F'): sys.exit(7)
if not g(w, 11, 10, '11F 到上梯旁'): sys.exit(8)
if not s(w, 11, 11, '11F(11,11)->12F'): sys.exit(9)
if not g(w, 2, 11, '12F 到上梯旁'): sys.exit(10)
if not s(w, 1, 11, '12F(1,11)->13F'): sys.exit(11)
if not g(w, 10, 11, '13F 到上梯旁'): sys.exit(12)
if not s(w, 11, 11, '13F(11,11)->14F'): sys.exit(13)
if not g(w, 6, 10, '14F 到上梯旁'): sys.exit(14)
if not s(w, 6, 11, '14F(6,11)->15F'): sys.exit(15)
if not g(w, 6, 2, '15F 到上梯旁'): sys.exit(16)
if not s(w, 6, 1, '15F(6,1)->16F'): sys.exit(17)
if not g(w, 6, 10, '16F 到上梯旁'): sys.exit(18)
if not s(w, 6, 11, '16F(6,11)->17F'): sys.exit(19)
if not g(w, 6, 2, '17F 到上梯旁'): sys.exit(20)
if not s(w, 6, 1, '17F(6,1)->18F'): sys.exit(21)
if not g(w, 2, 1, '18F 到上梯旁'): sys.exit(22)
if not s(w, 1, 1, '18F(1,1)->19F'): sys.exit(23)
if not g(w, 7, 11, '19F 到上梯旁'): sys.exit(24)
if not s(w, 6, 11, '19F(6,11)->20F'): sys.exit(25)

print('到达 20F:', st(w.hero))
