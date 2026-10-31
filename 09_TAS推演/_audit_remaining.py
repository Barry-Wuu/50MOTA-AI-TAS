# -*- coding: utf-8 -*-
"""从 v3 全流程 World（到 11F 终态）盘点 1-10F 剩余可拾取物。"""
import sys, io
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import importlib.util
spec = importlib.util.spec_from_file_location('run811', r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/run_811.py')
# 直接 import 会执行 run_811（到 11F 并写 CSV）。我们想要它的 World 终态。
# 改为手动执行到 11F 的 World 状态：用 mota_core 重放 v3 CSV。
import mota_core as M
import csv

SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
fn = SRC + '../09_TAS推演/魔塔1_route_1F到11F_合法_v3.csv'
rows = list(csv.DictReader(io.open(fn, encoding='utf-8-sig')))
w = M.World.new()
h = w.hero
DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
def_col = 'def' if 'def' in rows[0] else 'dfn'
prev_f = None
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
print('重放终态: %dF(%d,%d) HP%d ATK%d DEF%d G%d 钥%s/%s/%s' % (
    h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r']))

# 盘点 1-10F 剩余可拾取物（obj 仍在 = 未被 v3 拾取）
for f in range(1, 11):
    rem = []
    for x in range(1, 13):
        for y in range(1, 13):
            o = M.obj_raw(f, x, y)
            if not o: continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            if o in (1, 3, 28) or ty in ('STATUS', 'ITEM'):
                rem.append((x, y, o, M.oname(o)[:14]))
    if rem:
        print('==== %dF 剩余 %d 个 ====' % (f, len(rem)))
        for it in rem:
            print('   (%2d,%2d) obj%-3d %s' % it)
