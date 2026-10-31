# -*- coding: utf-8 -*-
"""从 v3 终态：回补10F → 11F 全清（银盾+钥匙+药）→ 上 12F。"""
import sys, io, math, heapq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import csv

SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
fn = SRC + '../09_TAS推演/魔塔1_route_1F到11F_合法_v3.csv'
rows = list(csv.DictReader(io.open(fn, encoding='utf-8-sig')))
w = M.World.new()
h = w.hero
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
        print('卡在第 %d 行' % (i+1)); break
    w.move(*ok)
print('起点: %dF(%d,%d) HP%d ATK%d DEF%d G%d 钥%s/%s/%s' % (
    h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r']))

def st():
    return 'HP%d A%d D%d G%d 钥%d/%d/%d %dF(%d,%d)' % (
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
    start=(h.x,h.y)
    p = bfs(f,start,(x,y))
    if p is None:
        print('  !! 不可达 %dF(%d,%d) from %s' % (f,x,y,start))
        return False
    for d in p:
        lg = w.move(*d)
        if lg and lg[0].startswith(('打不动','打不过','blocked')):
            print('  !! 卡在 (%d,%d): %s' % (h.x,h.y,lg))
            return False
        if (h.x,h.y)==start and lg and lg[0].startswith('开'):
            w.move(*d)
    print('  [%s] %s' % (note, st()))
    return True

# ---- 回补 10F ----
goto(10, 9, 4, '10F 黄钥(9,4)')
goto(10, 3, 4, '10F 蓝药(3,4)')
goto(10, 6, 10, '10F 回(6,10)')
w.move(0,1)
print('  上11F:', st())

# ---- 11F ----
# 开黄门(5,9) → 收集钥匙区
# 黄门(5,9) 在 (5,9)，从 (6,9) 向左进
w.move(-1,0)  # (6,10)->(6,9)?? 需要先到 (6,9)。当前在 11F(6,10)，(6,9) 可达
# 实际上用 goto 到 (6,9)，然后 approach (5,9) 开门
goto(11, 6, 9, '11F 到(6,9)')
# 开黄门(5,9)：从(6,9) 向左
lg = w.move(-1,0)
print('  开黄门(5,9):', lg, st())
if h.x == 5 and h.y == 9:
    print('  进入(5,9)')
# 现在收集 11F：钥匙 (4,11)(3,11)(2,11)(1,11)(1,10)(11,1)、银盾(2,2)、药 (1,7)(8,11)(9,6)(10,1)(11,1)
# 先走源 CSV 路径： (4,9)B史→(4,10)(4,11)(3,11)(2,11)(1,11)(1,10)
goto(11, 4, 9, '11F (4,9) B史莱姆')
goto(11, 4, 11, '11F (4,11) 黄钥')
goto(11, 1, 11, '11F (1,11) 黄钥')
goto(11, 1, 10, '11F (1,10) 黄钥')
# 银盾(2,2)：需要从 (1,10) 走 (1,9)? 看图 (1,9) 是墙？看 11F 图：y9 行 x1 是墙？需要路径
goto(11, 2, 2, '11F 银盾(2,2)')
goto(11, 11, 11, '11F 上梯(11,11)')
