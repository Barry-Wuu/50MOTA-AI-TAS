# -*- coding: utf-8 -*-
"""11F→20F 手工排 v1（Phase A：11F→19F 连续推进，含 17F 银剑、19F 十字架）。
入口：v3 终态 11F(6,10) HP247/ATK26/DEF46/G178/钥0-0-0（重放魔塔1_route_1F到11F_合法_v3.csv）。
路线（人类攻略，手工指定）：
  0. 回补 10F：(9,4) 黄钥 + (3,4) 蓝药(+200)
  1. 11F：开黄门(5,9) → 打(4,9)Ｂスライム → 钥匙区5黄 → 蝙蝠(10,9) → 上12F
  2. 12F：y11 走廊 2蝙蝠 → 红药(7,10)(5,10) → 上13F
  3. 13F：y11 石廊 0战 → 上14F
  4. 14F：黄门(9,9)(6,8) → 打(8,8)Ｂスライム → 撞(6,9)假墙 → 下15F
  5. 15F：商店买蓝钥(200G) → 黄门(9,9)(9,6)(11,3) → 大蝙蝠(9,4)+Ｂスライム(11,2)
     → 盗贼(9,1)凿墙 → 上16F
  6. 16F：蓝门(6,4) → 黄钥(7,7) → 黄门(6,8) → 上17F
  7. 17F：黄门(2,10) → 落穴 → 银剑(2,2) → 回 → 黄门(10,10) → x10竖道
     → 黄钥(9,3)(11,3) + 蓝药(10,2) + 赤晶(10,1) + 青晶(9,1) → y6通道 → 上18F
  8. 18F：打(10,2)Ｂスライム → 黄钥(11,1)(11,4)(11,5) + 蓝钥(11,3) → 上19F
  9. 19F：黄门(1,3)(1,6) → 蝙蝠(1,4)+大蝙蝠(1,7)+Ｂスライム(3,8)
     → 蓝门(6,7) → 撞(6,4)(6,3)假墙 → 十字架
     → 黄钥(8,5) → 黄门(10,3) → 大蝙蝠(10,2) → 黄钥(10,1)+赤晶(11,1)
     → 黄门(11,7) → ゾンビ(11,8) → 大蝙蝠(11,10) → 黄门(8,11) → 上20F
产出：魔塔1_route_11F到19F_PhaseA.csv
"""
import sys, csv, io
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import path as P
import manual

SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
V3 = SRC + '../09_TAS推演/魔塔1_route_1F到11F_合法_v3.csv'

# ---------- 重放 v3 ----------
rows = list(csv.DictReader(io.open(V3, encoding='utf-8-sig')))
w = M.World.new()
DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
def_col = 'def' if 'def' in rows[0] else 'dfn'
for i, r in enumerate(rows):
    tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
    ev = (r['event'] or '').strip()
    if '祭坛献金' in ev:
        if 'dfn+10' in ev: w.altar_policy = 'dfn'
        elif 'atk+10' in ev: w.altar_policy = 'atk'
        elif 'hp+200' in ev: w.altar_policy = 'hp'
    nxt = None
    if i + 1 < len(rows):
        nf, nx, ny = int(rows[i+1]['floor']), int(rows[i+1]['x']), int(rows[i+1]['y'])
        if nf == tf:
            nxt = (nx - tx, ny - ty)
    cands = []
    for d in DIRS:
        c = w.clone(); lg = c.move(*d)
        hh = c.hero
        if (hh.f, hh.x, hh.y) != (tf, tx, ty): continue
        sc = 0
        for k, cur in (('hp', hh.hp), ('atk', hh.atk), (def_col, hh.dfn), ('gold', hh.gold)):
            if cur == int(r[k]): sc += 1
        for k, kk in (('ky','y'), ('kb','b'), ('kr','r')):
            if hh.keys.get(kk, 0) == int(r[k]): sc += 1
        if bool(ev) == bool(lg): sc += 1
        if nxt == d: sc += 2
        cands.append((sc, d))
    ok = max(cands)[1] if cands else None
    if ok is None:
        print('!! 重放卡第 %d 行' % (i+1)); sys.exit(1)
    w.move(*ok)

manual.W = w
P.W = w
W = w
h = w.hero
print('入口: %dF(%d,%d) HP%d ATK%d DEF%d G%d 钥%d/%d/%d altar_k=%d items=%s' % (
    h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], w.altar_k, sorted(h.items)))

# ---------- 步进记录 ----------
REC = []
_orig_move = W.move
def rec_move(dx, dy):
    lg = _orig_move(dx, dy)
    hh = W.hero
    REC.append((hh.f, hh.x, hh.y, hh.hp, hh.atk, hh.dfn, hh.gold,
                hh.keys['y'], hh.keys['b'], hh.keys['r'],
                ';'.join(lg)[:90] if lg else '', '%d,%d' % (dx, dy)))
    return lg
W.move = rec_move

def step(label):
    h = W.hero
    print('  >> %-30s HP%-4d A%-3d D%-3d G%-4d 钥%d/%d/%d %dF(%d,%d)' % (
        label, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y))

# ---------- 0. 回补 10F ----------
print('\n==== 0. 回补 10F ====')
manual.approach(11, 6, 11)
o, lg = manual.enter(11, 6, 11, '11F(6,11)→10F')
step('入10F')
P.goto(10, 9, 4, '10F 黄钥(9,4)')
P.goto(10, 3, 4, '10F 蓝药(3,4)')
step('回补完成')
manual.approach(10, 6, 11)
o, lg = manual.enter(10, 6, 11, '10F(6,11)→11F')
step('回11F')

# ---------- 1. 11F ----------
print('\n==== 1. 11F ====')
P.goto(11, 6, 9, '11F (6,10)→(6,9)')
manual.approach(11, 5, 9)
o, lg = manual.enter(11, 5, 9, '黄门(5,9)')
P.goto(11, 4, 9, '11F 到(4,9)')
manual.approach(11, 4, 9)
o, lg = manual.enter(11, 4, 9, 'Ｂスライム(4,9)')
step('打Ｂスライム')
P.goto(11, 4, 11, '11F 钥匙区(4,11)')
P.goto(11, 1, 10, '11F 拿5黄钥')
P.goto(11, 10, 9, '11F 到(10,9)')
manual.approach(11, 10, 9)
o, lg = manual.enter(11, 10, 9, '蝙蝠(10,9)')
step('打蝙蝠')
P.goto(11, 11, 11, '11F 上行梯旁')
manual.approach(11, 11, 11)
o, lg = manual.enter(11, 11, 11, '11F(11,11)→12F')
step('入12F')

# ---------- 2. 12F ----------
print('\n==== 2. 12F ====')
P.goto(12, 8, 11, '12F 到(8,11)')
manual.approach(12, 8, 11)
o, lg = manual.enter(12, 8, 11, '蝙蝠(8,11)')
P.goto(12, 7, 10, '12F 红药(7,10)')
P.goto(12, 5, 10, '12F 红药(5,10)')
P.goto(12, 4, 11, '12F 到(4,11)')
manual.approach(12, 4, 11)
o, lg = manual.enter(12, 4, 11, '蝙蝠(4,11)')
P.goto(12, 1, 11, '12F 上行梯旁')
manual.approach(12, 1, 11)
o, lg = manual.enter(12, 1, 11, '12F(1,11)→13F')
step('入13F')

# ---------- 3. 13F ----------
print('\n==== 3. 13F ====')
P.goto(13, 11, 11, '13F y11石廊')
manual.approach(13, 11, 11)
o, lg = manual.enter(13, 11, 11, '13F(11,11)→14F')
step('入14F')

# ---------- 4. 14F ----------
print('\n==== 4. 14F ====')
P.goto(14, 9, 10, '14F (10,11)→(9,10)')
manual.approach(14, 9, 9)
o, lg = manual.enter(14, 9, 9, '黄门(9,9)')
P.goto(14, 8, 8, '14F 到(8,8)')
manual.approach(14, 8, 8)
o, lg = manual.enter(14, 8, 8, 'Ｂスライム(8,8)')
step('打Ｂスライム')
P.goto(14, 6, 8, '14F 到(6,8)')
manual.approach(14, 6, 8)
o, lg = manual.enter(14, 6, 8, '黄门(6,8)')
P.goto(14, 6, 9, '14F 撞假墙(6,9)')
manual.approach(14, 6, 9)
o, lg = manual.enter(14, 6, 9, '撞假墙(6,9)')
P.goto(14, 6, 11, '14F 下行梯旁')
manual.approach(14, 6, 11)
o, lg = manual.enter(14, 6, 11, '14F(6,11)→15F')
step('入15F')

# ---------- 5. 15F ----------
print('\n==== 5. 15F ====')
P.goto(15, 10, 10, '15F (6,10)→(10,10)')
manual.approach(15, 10, 10)
o, lg = manual.enter(15, 10, 10, '蝙蝠(10,10)')
P.goto(15, 11, 11, '15F 商店旁')
manual.approach(15, 11, 11)
o, lg = manual.enter(15, 11, 11, '商店买蓝钥200G')
step('买蓝钥')
P.goto(15, 9, 10, '15F 回(9,10)')
manual.approach(15, 9, 9)
o, lg = manual.enter(15, 9, 9, '黄门(9,9)')
P.goto(15, 9, 7, '15F (9,8)(9,7)')
manual.approach(15, 9, 6)
o, lg = manual.enter(15, 9, 6, '黄门(9,6)')
P.goto(15, 9, 4, '15F 到(9,4)')
manual.approach(15, 9, 4)
o, lg = manual.enter(15, 9, 4, '大蝙蝠(9,4)')
step('打大蝙蝠')
P.goto(15, 11, 4, '15F (10,4)(11,4)')
manual.approach(15, 11, 3)
o, lg = manual.enter(15, 11, 3, '黄门(11,3)')
P.goto(15, 11, 2, '15F 到(11,2)')
manual.approach(15, 11, 2)
o, lg = manual.enter(15, 11, 2, 'Ｂスライム(11,2)')
step('打Ｂスライム')
P.goto(15, 9, 1, '15F 盗贼(9,1)')
step('盗贼凿墙')
P.goto(15, 6, 1, '15F (8,1)(7,1)→(6,1)')
manual.approach(15, 6, 1)
o, lg = manual.enter(15, 6, 1, '15F(6,1)→16F')
step('入16F')

# ---------- 6. 16F ----------
print('\n==== 6. 16F ====')
P.goto(16, 6, 3, '16F (6,2)→(6,3)')
manual.approach(16, 6, 4)
o, lg = manual.enter(16, 6, 4, '蓝门(6,4)')
P.goto(16, 7, 7, '16F (6,5)(7,5)(7,6)→(7,7)黄钥')
P.goto(16, 6, 7, '16F 回(6,7)')
manual.approach(16, 6, 8)
o, lg = manual.enter(16, 6, 8, '黄门(6,8)')
P.goto(16, 6, 11, '16F (6,9)(6,10)→(6,11)')
manual.approach(16, 6, 11)
o, lg = manual.enter(16, 6, 11, '16F(6,11)→17F')
step('入17F')

# ---------- 7. 17F ----------
print('\n==== 7. 17F ====')
P.goto(17, 2, 10, '17F (6,10)→(2,10)')
manual.approach(17, 2, 10)
o, lg = manual.enter(17, 2, 10, '黄门(2,10)')
P.goto(17, 2, 2, '17F x2竖道 银剑(2,2)')
step('拿银剑')
P.goto(17, 10, 10, '17F 回(10,10)')
manual.approach(17, 10, 10)
o, lg = manual.enter(17, 10, 10, '黄门(10,10)')
P.goto(17, 10, 6, '17F x10竖道 (10,9)(10,8)(10,7)落穴→(10,6)')
# 顺路收集 x10 竖道道具
P.goto(17, 10, 1, '17F (10,5)(10,4)落穴→(10,3)(10,2)蓝药→(10,1)赤晶')
P.goto(17, 9, 1, '17F 青晶(9,1)')
P.goto(17, 9, 3, '17F 黄钥(9,3)')
P.goto(17, 11, 3, '17F 黄钥(11,3)')
step('x10道具')
P.goto(17, 10, 6, '17F 回(10,6)')
P.goto(17, 6, 6, '17F y6通道 (9,6)(8,6)(7,6)→(6,6)')
P.goto(17, 6, 1, '17F x6竖道 (6,5)(6,4)(6,3)(6,2)→(6,1)')
manual.approach(17, 6, 1)
o, lg = manual.enter(17, 6, 1, '17F(6,1)→18F')
step('入18F')

# ---------- 8. 18F ----------
print('\n==== 8. 18F ====')
P.goto(18, 10, 2, '18F (6,2)→(10,2)')
manual.approach(18, 10, 2)
o, lg = manual.enter(18, 10, 2, 'Ｂスライム(10,2)')
step('打Ｂスライム')
P.goto(18, 11, 1, '18F (11,2)→(11,1)黄钥')
P.goto(18, 11, 3, '18F (11,2)→(11,3)蓝钥')
P.goto(18, 11, 5, '18F (11,4)(11,5)黄钥')
step('18F右侧道具')
P.goto(18, 1, 1, '18F 回(1,1)上行梯')
manual.approach(18, 1, 1)
o, lg = manual.enter(18, 1, 1, '18F(1,1)→19F')
step('入19F')

# ---------- 9. 19F ----------
print('\n==== 9. 19F ====')
manual.approach(19, 1, 3)
o, lg = manual.enter(19, 1, 3, '黄门(1,3)')
P.goto(19, 1, 4, '19F 蝙蝠(1,4)')
manual.approach(19, 1, 4)
o, lg = manual.enter(19, 1, 4, '蝙蝠(1,4)')
P.goto(19, 1, 5, '19F (1,5)')
manual.approach(19, 1, 6)
o, lg = manual.enter(19, 1, 6, '黄门(1,6)')
P.goto(19, 1, 7, '19F 大蝙蝠(1,7)')
manual.approach(19, 1, 7)
o, lg = manual.enter(19, 1, 7, '大蝙蝠(1,7)')
P.goto(19, 3, 8, '19F (2,7)(3,7)→(3,8)')
manual.approach(19, 3, 8)
o, lg = manual.enter(19, 3, 8, 'Ｂスライム(3,8)')
P.goto(19, 6, 8, '19F (4,8)(5,8)→(6,8)')
manual.approach(19, 6, 7)
o, lg = manual.enter(19, 6, 7, '蓝门(6,7)')
P.goto(19, 6, 3, '19F (6,6)(6,5)(6,4)假墙→(6,3)十字架')
step('拿十字架')
P.goto(19, 8, 5, '19F (7,3)(7,4)(8,4)→(8,5)黄钥')
P.goto(19, 11, 6, '19F (8,6)(9,6)(10,6)→(11,6)')
P.goto(19, 11, 5, '19F (11,5)Ｂスライム')
manual.approach(19, 11, 5)
o, lg = manual.enter(19, 11, 5, 'Ｂスライム(11,5)')
P.goto(19, 10, 4, '19F (11,4)→(10,4)')
manual.approach(19, 10, 3)
o, lg = manual.enter(19, 10, 3, '黄门(10,3)')
P.goto(19, 10, 2, '19F 大蝙蝠(10,2)')
manual.approach(19, 10, 2)
o, lg = manual.enter(19, 10, 2, '大蝙蝠(10,2)')
P.goto(19, 10, 1, '19F 黄钥(10,1)')
P.goto(19, 11, 1, '19F 赤晶(11,1)')
step('19F右侧')
P.goto(19, 11, 6, '19F 回(11,6)')
manual.approach(19, 11, 7)
o, lg = manual.enter(19, 11, 7, '黄门(11,7)')
P.goto(19, 11, 8, '19F ゾンビ(11,8)')
manual.approach(19, 11, 8)
o, lg = manual.enter(19, 11, 8, 'ゾンビ(11,8)')
P.goto(19, 11, 10, '19F (11,9)→(11,10)大蝙蝠')
manual.approach(19, 11, 10)
o, lg = manual.enter(19, 11, 10, '大蝙蝠(11,10)')
P.goto(19, 10, 11, '19F (11,11)→(10,11)蝙蝠')
manual.approach(19, 10, 11)
o, lg = manual.enter(19, 10, 11, '蝙蝠(10,11)')
P.goto(19, 9, 11, '19F (9,11)')
manual.approach(19, 8, 11)
o, lg = manual.enter(19, 8, 11, '黄门(8,11)')
P.goto(19, 6, 11, '19F (7,11)→(6,11)')
step('19F完成')

print('\n==== Phase A 结果 ====')
h = W.hero
print('终态 %dF(%d,%d) HP%d ATK%d DEF%d G%d 钥%d/%d/%d altar_k=%d' % (
    h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], w.altar_k))

# ---------- 输出 CSV ----------
out = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/魔塔1_route_11F到19F_PhaseA.csv'
rows_out = [dict(step=0, floor=11, x=6, y=10, hp=247, atk=26, dfn=46, gold=178,
                 ky=0, kb=0, kr=0, event='PhaseA起点(v3终态)', dir='')]
for i, r in enumerate(REC):
    f, x, y, hp, atk, dfn, gold, ky, kb, kr, ev, d = r
    rows_out.append(dict(step=i + 1, floor=f, x=x, y=y, hp=hp, atk=atk, dfn=dfn, gold=gold,
                         ky=ky, kb=kb, kr=kr, event=ev, dir=d))
with io.open(out, 'w', encoding='utf-8-sig', newline='') as fp:
    w2 = csv.DictWriter(fp, fieldnames=list(rows_out[0].keys()))
    w2.writeheader(); w2.writerows(rows_out)
print('已存 %s（%d 行）' % (out, len(rows_out)))