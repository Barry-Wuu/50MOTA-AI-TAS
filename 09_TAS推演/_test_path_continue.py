# -*- coding: utf-8 -*-
"""测试：重放 v3 到 11F，把 manual.W / path.W 指向重放 World，再用 P.goto 续走。"""
import sys, io
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import csv

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
        print('卡在第 %d 行' % (i+1)); break
    w.move(*ok)
print('重放终态:', w.hero.f, w.hero.x, w.hero.y, w.hero.hp, w.hero.atk, w.hero.dfn, w.hero.gold, w.hero.keys)

# 替换 manual.W / path.W
import manual
import path as P
manual.W = w
P.W = w
# 测试 P.goto 回补 10F
# 先踩 11F(6,11) 下 10F —— 用 manual.approach/enter
w.move(0, 1)
print('下10F:', w.hero.f, w.hero.x, w.hero.y)
ok = P.goto(10, 9, 4, '10F 黄钥(9,4)')
print('goto结果:', ok, w.hero.f, w.hero.x, w.hero.y, w.hero.keys)
