# -*- coding: utf-8 -*-
"""11F→20F 完整路线 v2（基于 v3 入口 HP247/ATK26/DEF46/G178/钥0）
手工 waypoint + BFS 层内导航（排除楼梯/换层格，跟踪累计钥匙消耗）。
路线：
  0. 回补：10F 黄钥(9,4)(11,4)+蓝药(1,4)(3,4) → 9F 黄钥(2,2) → 回 11F
  1. 11F：黄门(5,9) → B史(4,9) → 钥匙区5黄 → 蝙蝠(10,9) → 12F
  2. 12F：祭坛献攻×3 → 13F
  3. 13F：穿石廊 → 14F
  4. 14F：蓝钥(1,11) + 暗墙红钥匙(1,3) + 黄钥(6,1)(9,1)(10,1)(11,1) + 红药(5,10)(9,6)(1,5)
  5. 15F：蓝钥(3,6) + 黄钥(3,5)(3,7) + 蓝药(11,8) + 青晶(1,1) + 盗贼(9,1)凿墙 → 16F
  6. 16F：黄钥(1,1)(1,2)(1,3)(2,5)(7,3)(7,7) + 蓝钥(11,7) + 青晶(1,7) + 红药(11,3)(5,5)(1,6) + 红晶(1,5)
  7. 17F：银剑(2,2) + 蓝药(10,2) + 黄钥(9,3)(11,3) + 青晶(9,1) + 红晶(11,1) → 18F
  8. 18F：黄钥(11,1)(11,2)(11,4)(11,5) + 蓝钥(11,3) → 19F
  9. 19F：十字架(6,3) + 蓝钥(8,1) + 红药(4,1)(9,9) + 红晶(11,1) → 20F
 10. 20F：BOSS 吸血鬼 → 21F
"""
import sys, io, csv, math, heapq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
V3 = SRC + '../09_TAS推演/魔塔1_route_1F到11F_合法_v3.csv'
OUT = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/魔塔1_route_11F到20F_v2.csv'

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
        if nf == tf: nxt = (nx - tx, ny - ty)
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

h = w.hero
print('入口: %dF(%d,%d) HP%d ATK%d DEF%d G%d 钥%d/%d/%d altar_k=%d items=%s' % (
    h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], w.altar_k, sorted(h.items)))

# ---------- 记录 ----------
REC = []
_orig_move = w.move
def rec_move(dx, dy):
    lg = _orig_move(dx, dy)
    hh = w.hero
    REC.append((hh.f, hh.x, hh.y, hh.hp, hh.atk, hh.dfn, hh.gold,
                hh.keys['y'], hh.keys['b'], hh.keys['r'],
                ';'.join(lg)[:90] if lg else '', '%d,%d' % (dx, dy)))
    return lg
w.move = rec_move

# ---------- 工具 ----------
def warp_cells(f):
    cells = set()
    up, down = M.STAIRS[f]
    if up: cells.add(up)
    if down: cells.add(down)
    if f == 10 and w.boss10: cells.add((6, 11))
    if f == 20 and w.boss20: cells.add((6, 1))
    return cells

def st():
    return 'HP%-5d A%-3d D%-3d G%-5d 钥%d/%d/%d %dF(%d,%d)' % (
        h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y)

def move_cost(cell, d, ky_used=0, kb_used=0, kr_used=0):
    nx, ny = cell[0]+d[0], cell[1]+d[1]
    if not (0<=nx<13 and 0<=ny<13): return 0,0,False
    if (nx, ny) in warp_cells(h.f):
        return 0,0,False
    t = w.terrain_at(h.f, nx, ny)
    if t == 1 or t == 2: return 0,0,False
    o = w.at(h.f, nx, ny)
    if o == 0: return 0,0,True
    ty = M.TYPE.get(M.oatr(o,3),'?')
    if o in M.KEY_OF: return 0,0,True
    if ty in ('STATUS','ITEM'): return 0,0,True
    if o == 20: return 0,0,True
    if o == 21 or o == 23: return 0,0,True
    if o == 89: return 0,0,False
    if o == 2 and h.keys['y'] - ky_used > 0: return 0,1,True
    if o == 4 and h.keys['b'] - kb_used > 0: return 0,2,True
    if o == 27 and h.keys['r'] - kr_used > 0: return 0,3,True
    if ty in ('NORMAL','SCORE','MESSAGE'): return 0,0,False
    if ty == 'MONSTER':
        mhp, matk, mdef = M.oatr(o,10), M.oatr(o,11), M.oatr(o,12)
        myd = max(h.atk-mdef,1)
        r = math.ceil(mhp/myd)
        loss = (r-1)*max(matk-h.dfn,1)
        if loss < h.hp: return loss,0,True
        return 0,0,False
    return 0,0,False

def bfs(f, start, goal):
    if start == goal: return []
    hp0 = h.hp
    dist={start:0}; cum={start:0}; ky={start:0}; kb={start:0}; kr={start:0}; prev={}
    pq=[(0,0,start)]
    while pq:
        cst,sp,c = heapq.heappop(pq)
        if cst != dist.get(c): continue
        if c == goal: break
        for d in DIRS:
            n=(c[0]+d[0],c[1]+d[1])
            if not (0<=n[0]<13 and 0<=n[1]<13): continue
            loss,kused,ok = move_cost(c,d, ky.get(c,0), kb.get(c,0), kr.get(c,0))
            if not ok: continue
            ncum = cum[c]+loss
            if ncum >= hp0: continue
            nky = ky[c]+(1 if kused==1 else 0)
            nkb = kb[c]+(1 if kused==2 else 0)
            nkr = kr[c]+(1 if kused==3 else 0)
            nc = cst+loss+100*kused
            if n not in dist or nc<dist[n]:
                dist[n]=nc; cum[n]=ncum; ky[n]=nky; kb[n]=nkb; kr[n]=nkr; prev[n]=(c,d)
                heapq.heappush(pq,(nc,sp+1,n))
    if goal not in dist: return None
    path=[]; cur=goal
    while cur != start:
        c,d = prev[cur]; path.append(d); cur=c
    return list(reversed(path))

def goto(f, x, y, note=''):
    if h.f != f:
        print('  !! goto 层 %d 但当前 %dF' % (f, h.f)); return False
    start=(h.x,h.y)
    if start == (x,y):
        print('  [%s] 已在' % note); return True
    p = bfs(f,start,(x,y))
    if p is None:
        print('  !! 不可达 %dF(%d,%d) from %s' % (f,x,y,start))
        return False
    for d in p:
        before = (h.x, h.y)
        lg = w.move(*d)
        if lg and lg[0].startswith(('打不动','打不过','blocked','无')):
            print('  !! 卡在 (%d,%d): %s' % (h.x,h.y,lg)); return False
        if (h.x,h.y)==before and lg and lg[0].startswith('开'):
            print('  !! 开门失败 (%d,%d): %s' % (h.x,h.y,lg)); return False
    print('  [%s] %s' % (note, st()))
    return True

def act(f, x, y, note=''):
    """从邻格走进 (x,y)：战斗/拾取/开门/撞墙/祭坛/商店。"""
    if h.f != f:
        print('  !! act 层 %d 但当前 %dF' % (f, h.f)); return False
    dx, dy = x-h.x, y-h.y
    if abs(dx)+abs(dy) != 1:
        print('  !! %s 不在邻格 %s' % (note, (h.x,h.y))); return False
    lg = w.move(dx, dy)
    if lg and lg[0].startswith(('打不动','打不过','blocked','无')):
        print('  !! %s 失败: %s' % (note, lg)); return False
    print('  [%s] %s' % (note, st()))
    return True

def stair(f, x, y, note=''):
    """走到 (f,x,y) 楼梯邻格并踏上（换层）。"""
    if h.f != f:
        print('  !! stair 层 %d 但当前 %dF' % (f, h.f)); return False
    cands = []
    for d in DIRS:
        n = (x+d[0], y+d[1])
        if not (0<=n[0]<13 and 0<=n[1]<13): continue
        if n in warp_cells(f): continue
        t = w.terrain_at(f, n[0], n[1])
        if t == 1: continue
        o = w.at(f, n[0], n[1])
        if o not in (0,) and M.TYPE.get(M.oatr(o,3),'?') not in ('STATUS','ITEM') and o not in M.KEY_OF and o not in (20,21,23):
            continue
        cands.append(n)
    best = None
    for c in cands:
        p = bfs(f, (h.x,h.y), c)
        if p is None: continue
        if best is None or len(p) < len(best[1]): best = (c, p)
    if best is None:
        print('  !! 楼梯 %dF(%d,%d) 无可达邻格' % (f,x,y)); return False
    c, p = best
    for d in p:
        before = (h.x, h.y)
        lg = w.move(*d)
        if lg and lg[0].startswith(('打不动','打不过','blocked','无')):
            print('  !! 去楼梯途中卡 (%d,%d): %s' % (h.x,h.y,lg)); return False
        if (h.x,h.y)==before and lg and lg[0].startswith('开'):
            print('  !! 开门失败: %s' % lg); return False
    dx, dy = x-h.x, y-h.y
    lg = w.move(dx, dy)
    if lg and lg[0].startswith(('blocked','无')):
        print('  !! 上楼梯失败: %s' % lg); return False
    print('  [%s] %s' % (note, st()))
    return True

def step(label):
    print('  >> %-30s %s' % (label, st()))

print('\n==== 0. 回补 10F/9F ====')
if not stair(11, 6, 11, '11F(6,11)->10F'): sys.exit(1)
if not goto(10, 9, 4, '10F 黄钥(9,4)'): sys.exit(1)
if not goto(10, 11, 4, '10F 黄钥(11,4)'): sys.exit(1)
if not goto(10, 1, 4, '10F 蓝药(1,4)'): sys.exit(1)
if not goto(10, 3, 4, '10F 蓝药(3,4)'): sys.exit(1)
if not goto(10, 1, 10, '10F 到(1,10)'): sys.exit(1)
if not stair(10, 1, 11, '10F(1,11)->9F'): sys.exit(1)
if not goto(9, 2, 2, '9F 黄钥(2,2)'): sys.exit(1)
# 回 11F：9F(1,11)上梯 -> 10F(1,10)，10F(6,11)动态上梯 -> 11F(6,10)
# 注：楼梯格由 stair() 处理（自动找可达邻格），不能用 goto 直达楼梯格
if not stair(9, 1, 11, '9F(1,11)->10F'): sys.exit(1)
if not stair(10, 6, 11, '10F(6,11)->11F'): sys.exit(1)
step('回11F')

print('\n==== 1. 11F ====')
if not goto(11, 6, 9, '11F (6,10)->(6,9)'): sys.exit(1)
if not act(11, 5, 9, '黄门(5,9)'): sys.exit(1)
if not goto(11, 4, 9, '11F 到(4,9)'): sys.exit(1)
if not act(11, 4, 9, 'Ｂスライム(4,9)'): sys.exit(1)
if not goto(11, 4, 11, '11F 钥匙区(4,11)'): sys.exit(1)
if not goto(11, 1, 10, '11F 5黄钥(1,10)'): sys.exit(1)
if not goto(11, 10, 9, '11F 到(10,9)'): sys.exit(1)
if not act(11, 10, 9, '蝙蝠(10,9)'): sys.exit(1)
if not goto(11, 11, 10, '11F 到(11,10)'): sys.exit(1)
if not stair(11, 11, 11, '11F(11,11)->12F'): sys.exit(1)

print('\n==== 2. 12F 祭坛献攻×3 ====')
# 落点 12F(10,11)。先到祭坛 (6,9)。沿途打蝙蝠(8,11)？
if not goto(12, 8, 11, '12F 到(8,11)'): sys.exit(1)
if not act(12, 8, 11, '蝙蝠(8,11)'): sys.exit(1)
if not goto(12, 7, 10, '12F 红药(7,10)'): sys.exit(1)
if not goto(12, 6, 9, '12F 祭坛旁(6,9)'): sys.exit(1)
w.altar_policy = 'atk'
for i in range(3):
    if not act(12, 6, 9, '祭坛献攻 #%d' % (i+1)): sys.exit(1)
if not stair(12, 1, 11, '12F(1,11)->13F'): sys.exit(1)

print('\n==== 3. 13F 石廊 ====')
if not stair(13, 11, 11, '13F(11,11)->14F'): sys.exit(1)

print('\n==== 4. 14F ====')
# 落点 (10,11)。蓝钥(1,11)：开黄门(4,11)
if not goto(14, 4, 10, '14F 到(4,10)'): sys.exit(1)
if not act(14, 4, 11, '黄门(4,11)'): sys.exit(1)
if not goto(14, 1, 11, '14F 蓝钥(1,11)'): sys.exit(1)
# 暗墙红钥匙 (1,3)：从 (1,11) 沿左路上行。先看 (1,5) 红药
if not goto(14, 1, 5, '14F 红药(1,5)'): sys.exit(1)
if not act(14, 1, 3, '暗墙(1,3)红钥匙'): sys.exit(1)
# 红药(5,10)(9,6)
if not goto(14, 5, 10, '14F 红药(5,10)'): sys.exit(1)
if not goto(14, 9, 6, '14F 红药(9,6)'): sys.exit(1)
# 顶部黄钥(6,1)(9,1)(10,1)(11,1)
if not goto(14, 6, 1, '14F 黄钥(6,1)'): sys.exit(1)
if not goto(14, 9, 1, '14F 黄钥(9,1)'): sys.exit(1)
if not goto(14, 11, 1, '14F 黄钥(10,1)(11,1)'): sys.exit(1)
if not goto(14, 6, 10, '14F 到(6,10)上梯旁'): sys.exit(1)
if not stair(14, 6, 11, '14F(6,11)->15F'): sys.exit(1)

print('\n==== 5. 15F ====')
# 落点 (6,10)。蓝钥(3,6)+黄钥(3,5)(3,7)
if not goto(15, 3, 7, '15F 黄钥(3,7)'): sys.exit(1)
if not goto(15, 3, 6, '15F 蓝钥(3,6)'): sys.exit(1)
if not goto(15, 3, 5, '15F 黄钥(3,5)'): sys.exit(1)
# 蓝药(11,8)：过黄门(9,9)？
if not goto(15, 9, 9, '15F 到(9,9)黄门'): sys.exit(1)
if not act(15, 9, 9, '黄门(9,9)'): sys.exit(1)
if not goto(15, 11, 8, '15F 蓝药(11,8)'): sys.exit(1)
# 盗贼(9,1)凿墙
if not goto(15, 9, 1, '15F 盗贼(9,1)'): sys.exit(1)
# 青晶(1,1)：被兽人武士(2,1)挡，放弃
print('  [跳过 15F(1,1) 青晶：被(2,1)兽人武士挡]')
# 凿墙后上 16F：(6,1) 上梯。走 (8,1)(7,1)
if not stair(15, 6, 1, '15F(6,1)->16F'): sys.exit(1)

print('\n==== 6. 16F ====')
# 落点 (6,2)。黄钥(1,1)(1,2)(1,3)、红药(11,3)
if not goto(16, 1, 1, '16F 黄钥(1,1)'): sys.exit(1)
if not goto(16, 1, 3, '16F 黄钥(1,2)(1,3)'): sys.exit(1)
if not goto(16, 11, 3, '16F 红药(11,3)'): sys.exit(1)
if not goto(16, 7, 3, '16F 黄钥(7,3)'): sys.exit(1)
if not goto(16, 1, 5, '16F 红晶(1,5)'): sys.exit(1)
if not goto(16, 5, 5, '16F 红药(5,5)'): sys.exit(1)
if not goto(16, 1, 6, '16F 红药(1,6)'): sys.exit(1)
if not goto(16, 1, 7, '16F 青晶(1,7)'): sys.exit(1)
if not goto(16, 2, 5, '16F 黄钥(2,5)'): sys.exit(1)
if not goto(16, 7, 7, '16F 黄钥(7,7)'): sys.exit(1)
if not goto(16, 11, 7, '16F 蓝钥(11,7)'): sys.exit(1)
if not goto(16, 6, 10, '16F 到(6,10)上梯旁'): sys.exit(1)
if not stair(16, 6, 11, '16F(6,11)->17F'): sys.exit(1)

print('\n==== 7. 17F 银剑 ====')
# 落点 (6,10)。黄门(2,10) -> 银剑(2,2)
if not goto(17, 2, 10, '17F 到(2,10)'): sys.exit(1)
if not act(17, 2, 10, '黄门(2,10)'): sys.exit(1)
if not goto(17, 2, 2, '17F 银剑(2,2)'): sys.exit(1)
# 黄门(10,10) -> 蓝药(10,2)+黄钥(9,3)(11,3)+青晶(9,1)+红晶(11,1)
if not goto(17, 10, 10, '17F 到(10,10)'): sys.exit(1)
if not act(17, 10, 10, '黄门(10,10)'): sys.exit(1)
if not goto(17, 10, 2, '17F 蓝药(10,2)'): sys.exit(1)
if not goto(17, 9, 1, '17F 青晶(9,1)'): sys.exit(1)
if not goto(17, 11, 1, '17F 红晶(11,1)'): sys.exit(1)
if not goto(17, 9, 3, '17F 黄钥(9,3)'): sys.exit(1)
if not goto(17, 11, 3, '17F 黄钥(11,3)'): sys.exit(1)
if not stair(17, 6, 1, '17F(6,1)->18F'): sys.exit(1)

print('\n==== 8. 18F ====')
# 落点 (6,2)。右侧钥匙(11,1)(11,2)(11,3)(11,4)(11,5)
if not goto(18, 10, 2, '18F 到(10,2)'): sys.exit(1)
if not act(18, 10, 2, 'Ｂスライム(10,2)'): sys.exit(1)
if not goto(18, 11, 1, '18F 黄钥(11,1)'): sys.exit(1)
if not goto(18, 11, 2, '18F 黄钥(11,2)'): sys.exit(1)
if not goto(18, 11, 3, '18F 蓝钥(11,3)'): sys.exit(1)
if not goto(18, 11, 4, '18F 黄钥(11,4)'): sys.exit(1)
if not goto(18, 11, 5, '18F 黄钥(11,5)'): sys.exit(1)
if not stair(18, 1, 1, '18F(1,1)->19F'): sys.exit(1)

print('\n==== 9. 19F 十字架 ====')
# 落点 (1,2)。黄门(1,3) -> 蝙蝠(1,4) -> 黄门(1,6) -> 大蝙蝠(1,7) -> B史(3,8) -> 蓝门(6,7) -> 假墙(6,3)(6,4)十字架
if not act(19, 1, 3, '黄门(1,3)'): sys.exit(1)
if not act(19, 1, 4, '蝙蝠(1,4)'): sys.exit(1)
if not act(19, 1, 6, '黄门(1,6)'): sys.exit(1)
if not act(19, 1, 7, '大蝙蝠(1,7)'): sys.exit(1)
if not goto(19, 3, 8, '19F 到(3,8)'): sys.exit(1)
if not act(19, 3, 8, 'Ｂスライム(3,8)'): sys.exit(1)
if not goto(19, 6, 7, '19F 到(6,7)蓝门'): sys.exit(1)
if not act(19, 6, 7, '蓝门(6,7)'): sys.exit(1)
if not goto(19, 6, 3, '19F 到(6,3)假墙'): sys.exit(1)
if not act(19, 6, 3, '假墙(6,3)十字架'): sys.exit(1)
# 蓝钥(8,1)：需要从 (6,3) 走回。黄门(10,3) -> 大蝙蝠(10,2) -> 黄钥(10,1)+红晶(11,1)+蓝钥(8,1)
if not goto(19, 8, 5, '19F 黄钥(8,5)'): sys.exit(1)
if not goto(19, 11, 6, '19F 到(11,6)'): sys.exit(1)
if not goto(19, 11, 5, '19F B史(11,5)'): sys.exit(1)
if not act(19, 11, 5, 'Ｂスライム(11,5)'): sys.exit(1)
if not goto(19, 10, 3, '19F 到(10,3)黄门'): sys.exit(1)
if not act(19, 10, 3, '黄门(10,3)'): sys.exit(1)
if not act(19, 10, 2, '大蝙蝠(10,2)'): sys.exit(1)
if not goto(19, 10, 1, '19F 黄钥(10,1)'): sys.exit(1)
if not goto(19, 11, 1, '19F 红晶(11,1)'): sys.exit(1)
if not goto(19, 8, 1, '19F 蓝钥(8,1)'): sys.exit(1)
# 回 (6,11) 上梯？19F 上梯(6,11)。从 (8,1) 到 (6,11)
if not stair(19, 6, 11, '19F(6,11)->20F'): sys.exit(1)

print('\n==== 10. 20F BOSS ====')
# 落点 (6,10)。目标：红门(6,9) -> BOSS(6,6)。战前可吃 (11,4) 蓝药+400？但需要过怪。
# 先看落点周围。直接走向红门。
if not goto(20, 6, 9, '20F 到(6,9)红门'): sys.exit(1)
if not act(20, 6, 9, '红门(6,9)'): sys.exit(1)
if not goto(20, 6, 6, '20F 到(6,6)BOSS'): sys.exit(1)
if not act(20, 6, 6, '吸血鬼BOSS(6,6)'): sys.exit(1)
# BOSS 死后 (6,1) 现上行梯，由 stair() 处理
if not stair(20, 6, 1, '20F(6,1)->21F'): sys.exit(1)

print('\n==== 终态 ====')
h = W.hero
print('%dF(%d,%d) HP%d ATK%d DEF%d G%d 钥%d/%d/%d altar_k=%d items=%s' % (
    h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], w.altar_k, sorted(h.items)))

# ---------- 输出 CSV ----------
rows_out = [dict(step=0, floor=11, x=6, y=10, hp=247, atk=26, dfn=46, gold=178,
                ky=0, kb=0, kr=0, event='11F→20F v2起点(v3终态)', dir='')]
for i, r in enumerate(REC):
    f, x, y, hp, atk, dfn, gold, ky, kb, kr, ev, d = r
    rows_out.append(dict(step=i + 1, floor=f, x=x, y=y, hp=hp, atk=atk, dfn=dfn, gold=gold,
                        ky=ky, kb=kb, kr=kr, event=ev, dir=d))
with io.open(OUT, 'w', encoding='utf-8-sig', newline='') as fp:
    w2 = csv.DictWriter(fp, fieldnames=list(rows_out[0].keys()))
    w2.writeheader(); w2.writerows(rows_out)
print('已存 %s（%d 行）' % (OUT, len(rows_out)))