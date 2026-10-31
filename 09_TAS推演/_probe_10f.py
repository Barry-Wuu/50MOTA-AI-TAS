# -*- coding: utf-8 -*-
"""从 v3 终态 World 探测 10F 回补可达性。"""
import sys, io
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

# 11F(6,10) → 下行梯 11F(6,11) → 10F
lg = w.move(0, 1)  # (6,10)->(6,11) 踩下行梯?
print('下(6,11):', w.hero.f, w.hero.x, w.hero.y, lg)
if w.hero.f == 10:
    print('到10F:', w.hero.x, w.hero.y)
    # 探测 10F 可达区与剩余 obj
    from collections import deque
    def free(f,x,y):
        if not (0<=x<13 and 0<=y<13): return False
        t=w.terrain_at(f,x,y)
        if t==1 or t==2: return False
        o=w.at(f,x,y)
        if o==0: return True
        ty=M.TYPE.get(M.oatr(o,3),'?')
        if o in M.KEY_OF: return True
        if ty in ('STATUS','ITEM'): return True
        if o==20: return True
        return False
    start=(w.hero.x,w.hero.y)
    seen={start}; q=deque([start])
    while q:
        c=q.popleft()
        for d in DIRS:
            n=(c[0]+d[0],c[1]+d[1])
            if n in seen: continue
            if free(10,*n):
                seen.add(n); q.append(n)
    print('10F 可达 %d 格' % len(seen))
    # 可达格中的剩余 obj
    for c in sorted(seen):
        o=w.at(10,*c)
        if o:
            print('   可达 (%2d,%2d) obj%-3d %s' % (c[0],c[1],o,M.oname(o)[:16]))
    # 关口
    front=[]
    for c in seen:
        for d in DIRS:
            n=(c[0]+d[0],c[1]+d[1])
            if n in seen: continue
            o=w.at(10,*n)
            if o and n not in [x[1] for x in front]:
                front.append((o,n))
    print('关口:')
    for o,n in sorted(front,key=lambda z:(z[1][1],z[1][0])):
        print('   (%2d,%2d) obj%-3d %s' % (n[0],n[1],o,M.oname(o)[:12]))
