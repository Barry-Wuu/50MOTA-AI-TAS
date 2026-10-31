# -*- coding: utf-8 -*-
"""从 v3 终态：回补 10F 拿 2 钥+药 → 回 11F 开黄门(5,9) → 收集 11F 上梯。"""
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

def walk(dx, dy, note=''):
    lg = w.move(dx, dy)
    print('  [%s] %s' % (note, st()))
    return lg

# 1) 11F(6,10) → 下行 (6,11) → 10F(6,10)
walk(0, 1, '踩11F下梯')
# 2) 10F: 捡 (9,4) 黄钥、(3,4) 蓝药
#    用层内手动：先到 (9,4)
#    (6,10)->(6,9)? 10F 的 (6,9) 是红门 obj27（已开？v3 开过红门(6,9)）
print('10F 红门(6,9) 状态: obj=%s' % w.at(10,6,9))
# 直接尝试从 (6,10) 走向 (9,4)：先 (7,10)(8,10)(9,10)(9,9)... 需要看哪些格 free
# 用手动逐格试探太慢，改用 path.goto 逻辑（这里直接 import path 会重放 manual，不行）
# 改用 bfs_advance 移植：基于运行时 w 的解析式 move_cost
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

# 回补 10F
goto(10, 9, 4, '10F 捡黄钥(9,4)')
goto(10, 3, 4, '10F 捡蓝药(3,4)')
# 回 11F：到 (6,10) 踩 (6,11) 上梯
goto(10, 6, 10, '10F 回 (6,10)')
lg = w.move(0, 1)  # 踩 (6,11) 上梯
print('  上11F:', w.hero.f, w.hero.x, w.hero.y, lg)
print('回补后: %s' % st())
