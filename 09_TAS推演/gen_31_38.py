# -*- coding: utf-8 -*-
"""31F→38F 取骑士盾 路线生成 + 地形校验（PC-98/Java 原版 13x13）"""
import json, csv, math, os

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repo/01_PC98原版_mtower')
D = json.load(open(os.path.join(REPO, 'magic_tower1_map_50f.json'), encoding='utf-8'))

# 怪物 四维（obj -> hp/atk/def/gold）
ENT = {}
for fl in range(1, 51):
    for e in D[str(fl)].get('entities', []):
        o = e['obj']
        if e.get('hp') and o not in ENT:
            ENT[o] = (e['hp'], e['atk'], e['dfn'])

ATK, DEF, HP = 186, 76, 0
DOUBLE = {48, 49, 59}   # 十字架：兽人 / 兽人武士 / 吸血鬼

rows = []
cum = 0
def add(fl, x, y, act, note='', dmg=0, atk_d=0, def_d=0, hp_d=0):
    global ATK, DEF, HP, cum
    ATK += atk_d; DEF += def_d; HP += hp_d; cum += dmg
    rows.append([len(rows)+1, '%dF' % fl, '(%d,%d)' % (x, y), act, note,
                 dmg if dmg else '', cum, '%d/%d' % (ATK, DEF)])

def fight(fl, x, y, obj, note=''):
    """标准战斗结算"""
    global ATK, DEF
    hp, atk, dfn = ENT[obj]
    dbl = 2 if obj in DOUBLE else 1
    per = ATK * dbl - dfn
    if per <= 0:
        add(fl, x, y, '战', note + ' [打不过]')
        return
    rnd = math.ceil(hp / per)
    dmg = max(0, atk - DEF) * (rnd - 1)
    add(fl, x, y, '战', '%s %d/%d/%d  %d回合  -%d' % (note, hp, atk, dfn, rnd, dmg), dmg)

# ============ 31F 下(6,1) 上(6,11) 落点(6,2) ============
add(31, 6, 2, '到达', '自 30F(6,1) 上梯')
for y in range(3, 12):
    if y == 8:
        fight(31, 6, y, 49, '兽人武士(十字架×2)')
    elif y == 9:
        fight(31, 6, y, 49, '兽人武士(十字架×2)')
    else:
        add(31, 6, y, '走')
add(31, 6, 11, '上梯', '→32F 落点(6,10)')

# ============ 32F 下(6,11) 上(11,1) 落点(6,10) ============
add(32, 6, 10, '到达', '自 31F(6,11) 上梯')
for y in [9, 8, 7, 6, 5, 4, 3, 2, 1]:
    if y == 9:
        fight(32, 6, y, 90, 'obj90 楼梯守卫')
    else:
        add(32, 6, y, '走')
for x in [5, 4, 3]:
    if x == 3:
        add(32, 3, 1, '拾取', '蓝钥匙 obj3')
    else:
        add(32, x, 1, '走')
add(32, 2, 1, '走')
add(32, 1, 1, '拾取', '青の水晶  DEF+4', def_d=4)
add(32, 1, 2, '走')
add(32, 2, 2, '拾取', '赤の水晶  ATK+4', atk_d=4)
add(32, 2, 1, '走')
for x in [3, 4, 5, 6, 7, 8, 9, 10]:
    add(32, x, 1, '走')
add(32, 11, 1, '上梯', '→33F 落点(10,1)；本格 obj90 守卫已由 (6,9) 记，此处同型 1 击')

# ============ 33F 下(11,1) 上(1,1) 落点(10,1) ============
add(33, 10, 1, '到达', '自 32F(11,1) 上梯')
add(33, 9, 1, '走')
add(33, 8, 1, '走')
add(33, 7, 1, '开门', '黄门 obj2  -1 黄钥匙')
fight(33, 6, 1, 95, '幽灵')
add(33, 5, 1, '走')
fight(33, 4, 1, 49, '兽人武士(十字架×2)')
add(33, 3, 1, '开门', '黄门 obj2  -1 黄钥匙')
add(33, 2, 1, '走')
add(33, 1, 1, '上梯', '→34F 落点(2,1)')

# ============ 34F 下(1,1) 上(6,11) 落点(2,1) ============
add(34, 2, 1, '到达', '自 33F(1,1) 上梯')
add(34, 2, 2, '走')
fight(34, 2, 3, 95, '幽灵')
add(34, 2, 4, '开门', '黄门 obj2  -1 黄钥匙')
add(34, 2, 5, '走')
add(34, 2, 6, '拾取', '红钥匙 obj28（dyn 写入）')
add(34, 2, 7, '走')
add(34, 2, 8, '开门', '黄门 obj2  -1 黄钥匙')
add(34, 2, 9, '走')
fight(34, 3, 9, 94, '鬼战士')
add(34, 3, 10, '走')
add(34, 4, 10, '开门', '黄门 obj2  -1 黄钥匙')
add(34, 5, 10, '走')
add(34, 6, 10, '走')
add(34, 6, 11, '上梯', '→35F 落点(6,10)')

# ============ 35F 下(6,11) 上(11,1) 落点(6,10) ============
add(35, 6, 10, '到达', '自 34F(6,11) 上梯；魔龙 3×3 (5..7,5..7) 封死中线')
add(35, 5, 10, '拾取', '蓝钥匙 obj88（dyn 写入）')
add(35, 5, 9, '走')
add(35, 4, 9, '凿墙', '10F 盗贼挖的暗道 (4,9) 已通')
add(35, 3, 9, '撞墙', '隐形墙 obj89')
add(35, 3, 10, '走')
add(35, 3, 11, '撞墙', '隐形墙 obj89')
add(35, 2, 11, '撞墙', '隐形墙 obj89')
add(35, 1, 11, '撞墙', '隐形墙 obj89')
for y in [10, 9, 8, 7, 6, 5, 4, 3, 2]:
    add(35, 1, y, '撞墙' if y in (3, 2) else '走')
add(35, 2, 2, '撞墙', '隐形墙 obj89')
add(35, 3, 2, '撞墙', '隐形墙 obj89')
add(35, 4, 2, '撞墙', '隐形墙 obj89')
add(35, 5, 2, '走')
add(35, 5, 1, '走')
for x in [6, 7, 8, 9, 10]:
    add(35, x, 1, '走')
add(35, 11, 1, '上梯', '→36F 落点(11,2)')

# ============ 36F 下(11,1) 上(11,11) 落点(11,2) ============
add(36, 11, 2, '到达', '自 35F(11,1) 上梯')
fight(36, 11, 3, 95, '幽灵')
add(36, 11, 4, '走')
fight(36, 11, 5, 92, '双手剑士 100HP 一击')
fight(36, 11, 6, 91, '骑士')
add(36, 11, 7, '走')
add(36, 11, 8, '走')
add(36, 11, 9, '走')
add(36, 11, 10, '走')
add(36, 11, 11, '上梯', '→37F 落点(11,10)')

# ============ 37F 下(11,11) 上(1,1) 落点(11,10) ============
add(37, 11, 10, '到达', '自 36F(11,11) 上梯；下梯(11,11) 不可踩')
add(37, 10, 10, '走')
add(37, 10, 11, '走')
fight(37, 9, 11, 94, '鬼战士')
for x in [8, 7, 6, 5, 4]:
    add(37, x, 11, '走')
fight(37, 3, 11, 95, '幽灵')
add(37, 2, 11, '走')
add(37, 1, 11, '走')
add(37, 1, 10, '走')
fight(37, 1, 9, 93, '战士')
add(37, 1, 8, '镐', '站此用镐破 (2,8)，开下左库（镐一次性消耗）')
add(37, 2, 8, '走')
add(37, 3, 8, '走')
add(37, 3, 7, '拾取', '青の水晶  DEF+4', def_d=4)
add(37, 4, 7, '拾取', '赤の水晶  ATK+4', atk_d=4)
add(37, 5, 7, '拾取', '青い回復薬  HP+800', hp_d=800)
add(37, 5, 8, '拾取', '黄钥匙 obj1')
add(37, 5, 9, '拾取', '蓝钥匙 obj3')
add(37, 4, 9, '拾取', '蓝钥匙 obj3')
add(37, 4, 8, '拾取', '黄钥匙 obj1')
add(37, 3, 8, '走')
add(37, 2, 8, '走')
add(37, 1, 8, '走')
for y in [7, 6, 5, 4]:
    add(37, 1, y, '走')
add(37, 1, 3, '开门', '蓝门 obj4  -1 蓝钥匙')
add(37, 1, 2, '走')
add(37, 1, 1, '上梯', '→38F 落点(2,1)')

# ============ 38F 下(1,1) 上(11,1) 落点(2,1) ============
add(38, 2, 1, '到达', '自 37F(1,1) 上梯；下梯(1,1) 不可踩')
add(38, 2, 2, '走')
add(38, 1, 2, '走')
fight(38, 1, 3, 94, '鬼战士')
add(38, 1, 4, '走')
add(38, 2, 4, '走')
add(38, 2, 5, '走', '（此刻仍是空地板）')
add(38, 2, 6, '触发', '踩此格 → 源码 @2528 把 (2,5) 变落穴（回程断路）')
add(38, 2, 7, '拾取', '★骑士盾 obj37  DEF+40', def_d=40)
add(38, 1, 7, '走')
add(38, 1, 6, '走')
add(38, 2, 6, '走')
add(38, 3, 6, '走')
add(38, 4, 6, '开门', '蓝门 obj4  -1 蓝钥匙')
add(38, 5, 6, '开门', '蓝门 obj4  -1 蓝钥匙')
add(38, 5, 5, '开门', '蓝门 obj4  -1 蓝钥匙')
add(38, 5, 4, '走')
fight(38, 4, 4, 93, '战士')
fight(38, 3, 4, 93, '战士')
add(38, 2, 4, '走')
add(38, 1, 4, '走')
add(38, 1, 3, '走')
add(38, 1, 2, '走')
add(38, 2, 2, '走')
add(38, 2, 1, '走')
add(38, 3, 1, '开门', '红门 obj27  -1 红钥匙')
fight(38, 4, 1, 95, '幽灵')
for x in [5, 6, 7]:
    add(38, x, 1, '走')
fight(38, 8, 1, 95, '幽灵')
add(38, 9, 1, '开门', '黄门 obj2  -1 黄钥匙')
add(38, 10, 1, '走')
add(38, 11, 1, '上梯', '→39F 落点(11,2)')

# ================= 校验 =================
bad = []
WALL_BORDER = set(range(30, 38))
prev = None
for r in rows:
    fl = int(r[1].rstrip('F'))
    x, y = eval(r[2])
    t = D[str(fl)]['terrain'][y][x]
    act = r[3]
    if t in WALL_BORDER:
        bad.append(('BORDER', r))
    if act in ('走', '拾取', '战', '开门', '撞墙', '凿墙', '镐', '触发') and t == 3:
        if not (fl == 35 and act in ('撞墙', '凿墙')) \
           and not (fl == 38 and (x, y) == (2, 9)) \
           and not (fl == 37 and (x, y) == (2, 8)):   # 镐破开的库房入口
            bad.append(('WALL', r))
    if prev and prev[0] == fl and act not in ('到达', '上梯', '下梯'):
        d = abs(prev[1] - x) + abs(prev[2] - y)
        if d != 1:
            bad.append(('JUMP%d' % d, r))
    prev = (fl, x, y)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '魔塔1_route_31F到38F_取骑士盾.csv')
with open(out, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['序号', '楼层', '坐标(x,y)', '动作', '说明', '本格战损', '累计战损', 'ATK/DEF'])
    w.writerows(rows)

print('行数', len(rows), ' 校错', len(bad))
for b in bad[:20]:
    print('  BAD', b)
mv = {}
for r in rows:
    mv[r[1]] = mv.get(r[1], 0) + 1
print('各层行数', mv)
print('总战损', rows[-1][6], ' 终态', rows[-1][7])
