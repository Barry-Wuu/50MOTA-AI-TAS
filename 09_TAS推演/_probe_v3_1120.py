# -*- coding: utf-8 -*-
"""从 v3 终态出发，探测 11F→20F 新路线可行性：
  1) 11F 钥匙区(5黄钥) + 打B史(4,9) + 蝙蝠(10,9)
  2) 12F 祭坛献攻×3 (ATK26->56, G178->38)
  3) 13F 穿石廊
  4) 14F 拿蓝钥(1,11) + 暗墙红钥匙(1,3) + 黄钥(6,1)(9,1)(10,1)(11,1) + 红药(5,10)(9,6)(1,5)
  5) 15F 拿蓝钥(3,6) + 黄钥(3,5)(3,7) + 蓝药(11,8) + 青晶(1,1) + 盗贼(9,1)凿墙
  6) 16F 拿黄钥(1,1)(1,2)(1,3)(2,5)(7,3)(7,7) + 蓝钥(11,7) + 青晶(1,7) + 红药(11,3)(5,5)(1,6) + 红晶(1,5)
  7) 17F 银剑(2,2) + 蓝药(10,2) + 黄钥(9,3)(11,3) + 青晶(9,1) + 红晶(11,1)
"""
import sys, io, csv, math, heapq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
fn = SRC + '../09_TAS推演/魔塔1_route_1F到11F_合法_v3.csv'
rows = list(csv.DictReader(io.open(fn, encoding='utf-8-sig')))
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
h = w.hero
print('入口: %dF(%d,%d) HP%d ATK%d DEF%d G%d 钥%d/%d/%d altar_k=%d items=%s' % (
    h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], w.altar_k, sorted(h.items)))

def st():
    return 'HP%-5d A%-3d D%-3d G%-5d 钥%d/%d/%d %dF(%d,%d)' % (
        h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y)

def move_cost(cell, d):
    nx, ny = cell[0]+d[0], cell[1]+d[1]
    if not (0<=nx<13 and 0<=ny<13): return 0,0,False
    t = w.terrain_at(w.hero.f, nx, ny)
    if t == 1 or t == 2: return 0,0,False
    o = w.at(w.hero.f, nx, ny)
    if o == 0: return 0,0,True
    ty = M.TYPE.get(M.oatr(o,3),'?')
    if o in M.KEY_OF: return 0,0,True
    if ty in ('STATUS','ITEM'): return 0,0,True
    if o == 20: return 0,0,True
    if o == 21 or o == 23: return 0,0,True
    if o == 89: return 0,0,False      # 暗墙需手动撞
    if o == 2 and h.keys['y']>0: return 0,1,True
    if o == 4 and h.keys['b']>0: return 0,2,True
    if o == 27 and h.keys['r']>0: return 0,3,True
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
    dist={start:0}; cum={start:0}; prev={}
    pq=[(0,0,start)]
    while pq:
        cst,sp,c = heapq.heappop(pq)
        if cst != dist.get(c): continue
        if c == goal: break
        for d in DIRS:
            n=(c[0]+d[0],c[1]+d[1])
            if not (0<=n[0]<13 and 0<=n[1]<13): continue
            loss,kused,ok = move_cost(c,d)
            if not ok: continue
            ncum = cum[c]+loss
            if ncum >= hp0: continue
            nc = cst+loss+100*kused
            if n not in dist or nc<dist[n]:
                dist[n]=nc; cum[n]=ncum; prev[n]=(c,d)
                heapq.heappush(pq,(nc,sp+1,n))
    if goal not in dist: return None
    path=[]; cur=goal
    while cur != start:
        c,d = prev[cur]; path.append(d); cur=c
    return list(reversed(path))

def goto(f, x, y, note=''):
    global h
    if h.f != f:
        print('  !! goto 层 %d 但当前 %dF' % (f, h.f)); return False
    start=(h.x,h.y)
    if start == (x,y):
        print('  [%s] 已在' % note)
        return True
    p = bfs(f,start,(x,y))
    if p is None:
        print('  !! 不可达 %dF(%d,%d) from %s' % (f,x,y,start))
        return False
    for d in p:
        before = (h.x, h.y)
        lg = w.move(*d)
        if lg and lg[0].startswith(('打不动','打不过','blocked','无')):
            print('  !! 卡在 (%d,%d): %s' % (h.x,h.y,lg))
            return False
        # 开门失败（钥匙不足）时 move 不移动，需重试逻辑；这里直接失败
        if (h.x,h.y)==before and lg and lg[0].startswith('开'):
            print('  !! 开门失败 (%d,%d): %s' % (h.x,h.y,lg))
            return False
    print('  [%s] %s' % (note, st()))
    return True

def fight(f, x, y, note=''):
    """从邻格走进 (x,y) 战斗/拾取/开门/撞墙。"""
    global h
    if h.f != f:
        print('  !! fight 层 %d 但当前 %dF' % (f, h.f)); return False
    dx, dy = x-h.x, y-h.y
    if abs(dx)+abs(dy) != 1:
        print('  !! %s 不在邻格 %s' % (note, (h.x,h.y))); return False
    o = w.at(f, x, y)
    lg = w.move(dx, dy)
    if lg and lg[0].startswith(('打不动','打不过','blocked','无')):
        print('  !! %s 失败: %s' % (note, lg)); return False
    print('  [%s] %s' % (note, st()))
    return True

def stair(f, x, y, note=''):
    """走到 (f,x,y) 的邻格并踏上楼梯。"""
    global h
    if h.f != f:
        print('  !! stair 层 %d 但当前 %dF' % (f, h.f)); return False
    # 找可达邻格
    cands = []
    for d in DIRS:
        n = (x+d[0], y+d[1])
        if not (0<=n[0]<13 and 0<=n[1]<13): continue
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
    # 现在在邻格，踏上楼梯
    dx, dy = x-h.x, y-h.y
    lg = w.move(dx, dy)
    if lg and lg[0].startswith(('blocked','无')):
        print('  !! 上楼梯失败: %s' % lg); return False
    print('  [%s] %s' % (note, st()))
    return True

print('\n==== 1. 11F 钥匙区 ====')
if not goto(11, 6, 9, '(6,10)->(6,9)'): sys.exit(1)
if not fight(11, 5, 9, '黄门(5,9)'): sys.exit(1)
if not goto(11, 4, 9, '到(4,9)'): sys.exit(1)
if not fight(11, 4, 9, 'B史(4,9)'): sys.exit(1)
if not goto(11, 4, 11, '钥匙区(4,11)'): sys.exit(1)
if not goto(11, 1, 10, '5黄钥(1,10)'): sys.exit(1)
if not goto(11, 10, 9, '到(10,9)'): sys.exit(1)
if not fight(11, 10, 9, '蝙蝠(10,9)'): sys.exit(1)

print('\n==== 2. 上12F 祭坛献攻 ====')
if not stair(11, 11, 11, '11F(11,11)->12F'): sys.exit(1)
# 12F 落点 (10,11)。祭坛 (6,9)。先走 (8,11) 蝙蝠？
if not goto(12, 8, 11, '到(8,11)'): sys.exit(1)
if not fight(12, 8, 11, '蝙蝠(8,11)'): sys.exit(1)
if not goto(12, 7, 10, '红药(7,10)'): sys.exit(1)
if not goto(12, 6, 9, '祭坛旁(6,9)'): sys.exit(1)
# 献攻 3 次
for i in range(3):
    if not fight(12, 6, 9, '祭坛献攻 #%d' % (i+1)): sys.exit(1)

print('\n==== 3. 13F 穿石廊 ====')
if not stair(12, 1, 11, '12F(1,11)->13F'): sys.exit(1)
if not stair(13, 11, 11, '13F(11,11)->14F'): sys.exit(1)

print('\n==== 4. 14F 蓝钥+红钥匙 ====')
# 落点 14F(10,11)。先拿蓝钥(1,11)：开黄门(4,11)
if not goto(14, 4, 10, '到(4,10)'): sys.exit(1)
if not fight(14, 4, 11, '黄门(4,11)'): sys.exit(1)
if not goto(14, 1, 11, '蓝钥(1,11)'): sys.exit(1)
# 暗墙红钥匙 (1,3)：需从 (1,4)/(1,5) 区域撞 (1,3)
# 先看路径：从 (1,11) 到 (1,5) 经过 (2,4) 蓝门？地图 y4 x2 蓝门。
# 走 y11 -> (2,11)(3,11) -> (3,10)? 看地图 14F y10 x3 是 '·'
# 实际上 (1,3) 暗墙在左上角，周围 (1,4)(2,3)(1,2) 清空后裂开。
if not goto(14, 3, 10, '到(3,10)'): sys.exit(1)
if not goto(14, 3, 7, '到(3,7)附近'): sys.exit(1)
# 撞 (1,3) 暗墙需要先接近。先看 (1,5) 红药
if not goto(14, 1, 5, '红药(1,5)'): sys.exit(1)
if not fight(14, 1, 3, '暗墙(1,3)红钥匙'): sys.exit(1)
# 拿 14F 其余：黄钥(6,1)(9,1)(10,1)(11,1)、红药(5,10)(9,6)
if not goto(14, 5, 10, '红药(5,10)'): sys.exit(1)
if not goto(14, 9, 6, '红药(9,6)'): sys.exit(1)
if not goto(14, 6, 1, '黄钥(6,1)'): sys.exit(1)
if not goto(14, 9, 1, '黄钥(9,1)'): sys.exit(1)
if not goto(14, 11, 1, '黄钥(10,1)(11,1)'): sys.exit(1)

print('\n==== 5. 15F 蓝钥+凿墙 ====')
if not stair(14, 6, 11, '14F(6,11)->15F'): sys.exit(1)
# 15F 落点 (6,10)。目标：蓝钥(3,6)、黄钥(3,5)(3,7)、蓝药(11,8)、青晶(1,1)、盗贼(9,1)
# 路线：先拿 (3,6) 蓝钥。从 (6,10) 到 (3,6)？
if not goto(15, 3, 7, '到(3,7)黄钥'): sys.exit(1)
if not goto(15, 3, 6, '蓝钥(3,6)'): sys.exit(1)
if not goto(15, 3, 5, '黄钥(3,5)'): sys.exit(1)
# 蓝药(11,8)：走 (9,9) 黄门？地图 15F y9 x9 黄门，(11,8) 蓝药。
if not goto(15, 9, 9, '到(9,9)黄门'): sys.exit(1)
if not fight(15, 9, 9, '黄门(9,9)'): sys.exit(1)
if not goto(15, 11, 8, '蓝药(11,8)'): sys.exit(1)
# 盗贼 (9,1)：从 (11,8) 到 (9,1)
if not goto(15, 9, 1, '盗贼(9,1)'): sys.exit(1)
# 青晶 (1,1)：需要走左上，可能过 (2,1) 兽人武士？地图 15F (2,1) 兽人武士，不能打。跳过？
print('  [跳过 15F(1,1) 青晶：被兽人武士(2,1)挡]')
# 凿墙后上 16F
if not stair(15, 6, 1, '15F(6,1)->16F'): sys.exit(1)

print('\n==== 6. 16F 收集 ====')
# 16F 落点 (6,2)。拿黄钥(1,1)(1,2)(1,3)、红药(11,3)、黄钥(7,3)、红晶(1,5)、红药(5,5)(1,6)、青晶(1,7)、黄钥(2,5)(7,7)、蓝钥(11,7)
if not goto(16, 1, 1, '黄钥(1,1)'): sys.exit(1)
if not goto(16, 1, 3, '黄钥(1,2)(1,3)'): sys.exit(1)
if not goto(16, 11, 3, '红药(11,3)'): sys.exit(1)
if not goto(16, 7, 3, '黄钥(7,3)'): sys.exit(1)
if not goto(16, 1, 5, '红晶(1,5)'): sys.exit(1)
if not goto(16, 5, 5, '红药(5,5)'): sys.exit(1)
if not goto(16, 1, 6, '红药(1,6)'): sys.exit(1)
if not goto(16, 1, 7, '青晶(1,7)'): sys.exit(1)
if not goto(16, 2, 5, '黄钥(2,5)'): sys.exit(1)
if not goto(16, 7, 7, '黄钥(7,7)'): sys.exit(1)
if not goto(16, 11, 7, '蓝钥(11,7)'): sys.exit(1)

print('\n==== 7. 17F 银剑 ====')
if not stair(16, 6, 11, '16F(6,11)->17F'): sys.exit(1)
# 17F 落点 (6,10)。银剑(2,2)。先开黄门(2,10)
if not goto(17, 2, 10, '到(2,10)'): sys.exit(1)
if not fight(17, 2, 10, '黄门(2,10)'): sys.exit(1)
if not goto(17, 2, 2, '银剑(2,2)'): sys.exit(1)
# 蓝药(10,2)：开黄门(10,10)
if not goto(17, 10, 10, '到(10,10)'): sys.exit(1)
if not fight(17, 10, 10, '黄门(10,10)'): sys.exit(1)
if not goto(17, 10, 2, '蓝药(10,2)'): sys.exit(1)
if not goto(17, 9, 1, '青晶(9,1)'): sys.exit(1)
if not goto(17, 11, 1, '红晶(11,1)'): sys.exit(1)
if not goto(17, 9, 3, '黄钥(9,3)'): sys.exit(1)
if not goto(17, 11, 3, '黄钥(11,3)'): sys.exit(1)

print('\n==== 结果 ====')
print(st())
print('items=', sorted(h.items))