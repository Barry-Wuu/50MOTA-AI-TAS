# -*- coding: utf-8 -*-
"""生成 PC-98/Java 原版（13x13）21F-30F 路线 CSV，并用地形做合法性校验。"""
import json, csv, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repo', '01_PC98原版_mtower')
D = json.load(open(os.path.join(BASE, 'magic_tower1_map_50f.json'), encoding='utf-8'))

def terr(fl, x, y):
    return D[str(fl)]['terrain'][y][x]

def objat(fl, x, y):
    return D[str(fl)]['objects'][y][x]

WALL = {3}
for v in range(30, 38):
    WALL.add(v)

# (floor, x, y, action, note)
R = []
def add(fl, x, y, act, note):
    R.append((fl, x, y, act, note))

# ---- F21 落点(6,2) 上梯(6,11)，NPC obj140 在 (6,6) 需绕 ----
add(21, 6, 2, '到达', '20F 上梯落点')
for p in [(6,3),(6,4),(6,5)]:
    add(21, p[0], p[1], '走', '')
add(21, 5, 5, '走', '开始绕 NPC')
add(21, 5, 6, '走', 'NPC obj140 在 (6,6)，擦身可看台词')
add(21, 5, 7, '走', '')
add(21, 6, 7, '走', '回到中线')
for p in [(6,8),(6,9),(6,10)]:
    add(21, p[0], p[1], '走', '')
add(21, 6, 11, '上梯', '→F22')

# ---- F22 落点(6,10) 上梯(6,6) ----
add(22, 6, 10, '到达', '')
for p in [(6,9),(6,8),(6,7)]:
    add(22, p[0], p[1], '走', '唯一竖井 x=6')
add(22, 6, 6, '上梯', '→F23')

# ---- F23 落点(1,2) 上梯(11,1)；obj115 隐形块撞了会变墙，必须绕 ----
add(23, 1, 2, '到达', '')
for y in range(3, 7):
    add(23, 1, y, '走', 'x=1 列下行')
for x in range(2, 7):
    add(23, x, 6, '走', 'y=6 横穿（该行无 115）')
for y in range(5, 0, -1):
    add(23, 6, y, '走', 'x=6 列上行')
for x in range(7, 12):
    add(23, x, 1, '走', 'y=1 右行到上梯')
add(23, 11, 1, '上梯', '→F24')

# ---- F24 1 步 ----
add(24, 2, 11, '到达', '')
add(24, 2, 10, '上梯', '→F25（红门(6,8)不必开，那是 50F 支线）')

# ---- F25 红门取 5 把红钥匙 ----
add(25, 2, 11, '到达', '')
for x in range(3, 7):
    add(25, x, 11, '走', 'y=11 横穿')
add(25, 6, 10, '开门', '红门 obj27：红钥匙 -1')
add(25, 6, 9, '触发', '评分石 obj69（只看评价，不改数值）')
add(25, 6, 8, '拾取', '红钥匙 +1')
add(25, 5, 8, '拾取', '红钥匙 +1')
add(25, 4, 8, '拾取', '红钥匙 +1')
add(25, 5, 8, '走', '折返')
add(25, 6, 8, '走', '')
add(25, 7, 8, '拾取', '红钥匙 +1')
add(25, 8, 8, '拾取', '红钥匙 +1')
add(25, 7, 8, '走', '折返（(6,6) 大魔導師不踩）')
add(25, 6, 8, '走', '')
add(25, 6, 9, '走', '')
add(25, 6, 10, '走', '')
add(25, 6, 11, '走', '')
for x in range(5, 1, -1):
    add(25, x, 11, '走', '')
add(25, 1, 11, '上梯', '→F26')

# ---- F26 1 步（熔岩/假公主全绕） ----
add(26, 2, 11, '到达', '')
add(26, 2, 10, '上梯', '→F27（熔岩18格、4道红门、假公主全不碰）')

# ---- F27 9 步 ----
add(27, 2, 11, '到达', '')
for x in range(3, 12):
    add(27, x, 11, '走', 'y=11 直走廊')
add(27, 11, 11, '上梯', '→F28')

# ---- F28 9 步 ----
add(28, 10, 11, '到达', '')
for x in range(9, 0, -1):
    add(28, x, 11, '走', 'y=11 直走廊')
add(28, 1, 11, '上梯', '→F29')

# ---- F29 往返触发开墙 + 26 步主路线 + 蓝钥匙 ----
add(29, 2, 11, '到达', '第一次进 29F，记录最高层=29')
add(29, 1, 11, '下梯', '→28F（故意下楼触发暗道开启）')
add(28, 2, 11, '到达', '29F 下梯落点')
add(28, 1, 11, '上梯', '→29F（此时 x=6,y=3 的墙已打通）')
add(29, 2, 11, '到达', '')
add(29, 2, 10, '走', '')
add(29, 1, 10, '走', '')
for y in range(9, 0, -1):
    add(29, 1, y, '走', 'x=1 列上行')
for x in range(2, 7):
    add(29, x, 1, '走', 'y=1 横穿')
add(29, 6, 2, '走', '')
add(29, 7, 2, '拾取', '蓝钥匙 +1')
add(29, 6, 2, '走', '折返')
for y in range(3, 12):
    add(29, 6, y, '走', 'x=6 列下行（y=3 原为墙，已开）')
add(29, 6, 11, '上梯', '→F30')

# ---- F30 封印 + 杀 6 史莱姆 + 上梯 ----
add(30, 6, 10, '到达', '')
for y in [9, 8, 7, 6]:
    add(30, 6, y, '走', '(6,6) 触发封印：上下两口变落穴')
add(30, 6, 5, '走', '进入 y=5 横道')
add(30, 5, 5, '战', 'G史 35/18/1 → 0 伤')
add(30, 4, 5, '战', 'R史 45/20/2 → 0 伤')
add(30, 3, 5, '战', 'B史 130/60/3 → 0 伤')
add(30, 4, 5, '走', '')
add(30, 5, 5, '走', '')
add(30, 6, 5, '走', '')
add(30, 7, 5, '战', 'G史 → 0 伤（第4只）')
add(30, 8, 5, '战', 'R史 → 0 伤（第5只）')
add(30, 9, 5, '战', 'B史 → 0 伤（第6只，全清→落穴消失+上梯生成）')
add(30, 8, 5, '走', '')
add(30, 7, 5, '走', '')
add(30, 6, 5, '走', '')
for y in [4, 3, 2]:
    add(30, 6, y, '走', '落穴已清')
add(30, 6, 1, '上梯', '→F31')

# 校验：目标格不能是墙；相邻步曼哈顿距离必须=1（同层）
bad = []
prev = None
for i, (fl, x, y, act, note) in enumerate(R):
    if terr(fl, x, y) in WALL and (fl, x, y) != (29, 6, 3):
        bad.append(('WALL', i, fl, x, y, act))
    if prev and prev[0] == fl and act not in ('到达', '上梯', '下梯'):
        d = abs(prev[1]-x) + abs(prev[2]-y)
        if d != 1:
            bad.append(('JUMP', i, fl, prev[1:], (x, y), act, d))
    prev = (fl, x, y)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '魔塔1_route_21F到30F_原版.csv')
with open(OUT, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.writer(fh)
    w.writerow(['楼层', 'x', 'y', '动作', '说明'])
    for row in R:
        w.writerow(row)

print('总步骤', len(R))
print('校验问题', len(bad))
for b in bad[:20]:
    print(' ', b)
print('输出', OUT)
