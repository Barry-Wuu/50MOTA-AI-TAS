# -*- coding: utf-8 -*-
"""11F→20F 路线 v2 探测（基于 v3 入口 HP247/ATK26/DEF46/G178/钥0）
回补策略：
  10F 黄钥(9,4)(11,4) + 蓝药(1,4)(3,4)(11,11)
  9F  黄钥(2,2)(9,9) + 红药(2,10)(11,11)
  2F  黄钥(3,4)(4,4)(3,5) + 蓝药(3,10)(3,11)(4,10)
然后：
  11F 开黄门(5,9) 打B史(4,9) → 钥匙区5黄 → 蝙蝠(10,9) → 12F
  12F 祭坛献攻×3 → 13F → 14F 蓝钥(1,11)+暗墙红钥匙(1,3)+黄钥(6,1)(9,1)(10,1)(11,1)+红药
  15F 蓝钥(3,6)+黄钥(3,5)(3,7)+蓝药(11,8)+青晶(1,1)+盗贼(9,1)凿墙 → 16F
  16F 收集黄钥/蓝钥(11,7)/红药/青晶/红晶 → 17F 银剑 → 18F → 19F 十字架 → 20F
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
    if o == 89: return 0,0,False
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
    """从邻格走进 (x,y)（战斗/拾取/开门/撞墙/祭坛/商店）。"""
    if h.f != f:
        print('  !! act 层 %d 但当前 %dF' % (f, h.f)); return False
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
    """走到 (f,x,y) 楼梯邻格并踏上。"""
    if h.f != f:
        print('  !! stair 层 %d 但当前 %dF' % (f, h.f)); return False
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
    dx, dy = x-h.x, y-h.y
    lg = w.move(dx, dy)
    if lg and lg[0].startswith(('blocked','无')):
        print('  !! 上楼梯失败: %s' % lg); return False
    print('  [%s] %s' % (note, st()))
    return True

print('\n==== 0. 回补 10F/9F/2F ====')
# 踩 11F(6,11) 下 10F
if not stair(11, 6, 11, '11F(6,11)->10F'): sys.exit(1)
if not goto(10, 9, 4, '10F 黄钥(9,4)'): sys.exit(1)
if not goto(10, 11, 4, '10F 黄钥(11,4)'): sys.exit(1)
if not goto(10, 1, 4, '10F 蓝药(1,4)'): sys.exit(1)
if not goto(10, 3, 4, '10F 蓝药(3,4)'): sys.exit(1)
if not goto(10, 11, 11, '10F 蓝药(11,11)'): sys.exit(1)
# 回 9F：10F(1,10) -> 9F(1,10) 下行梯
if not goto(10, 1, 10, '10F 到(1,10)下行梯'): sys.exit(1)
if not stair(10, 1, 10, '10F(1,10)->9F'): sys.exit(1)
if not goto(9, 2, 2, '9F 黄钥(2,2)'): sys.exit(1)
if not goto(9, 9, 9, '9F 黄钥(9,9)'): sys.exit(1)
if not goto(9, 2, 10, '9F 红药(2,10)'): sys.exit(1)
if not goto(9, 11, 11, '9F 红药(11,11)'): sys.exit(1)
# 回 8F/7F/6F/5F/4F/3F/2F 拿钥匙和药？
# 9F(6,1) -> 8F(6,2)，8F(6,1)->7F(1,2)，7F(1,1)->6F(1,2)，6F(1,1)? 查楼梯
print('  [回补 9F 完成]')

print('\n==== 结果 ====')
print(st())
print('items=', sorted(h.items))