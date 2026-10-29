# -*- coding: utf-8 -*-
"""重放校验：把已有路线 CSV 的逐格记录在一个全新 World 里重走一遍，
   每步用 4 方向试走、取结果坐标与 CSV 记录一致的那一方向，再逐行比对 HP/ATK/DEF/G/钥匙。
   用途：确认这份基线不是脚本崩坏的产物。"""
import csv
import io
import sys

sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'


def replay(fn, maxrows=None, quiet=False):
    rows = list(csv.DictReader(io.open(SRC + fn, encoding='utf-8', errors='replace')))
    if maxrows:
        rows = rows[:maxrows]
    w = M.World.new()
    h = w.hero
    bad = []
    per_floor = {}
    prev_f = None
    for i, r in enumerate(rows):
        tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
        ev = (r['event'] or '').strip()
        nxt = None
        if i + 1 < len(rows):
            nf, nx, ny = int(rows[i + 1]['floor']), int(rows[i + 1]['x']), int(rows[i + 1]['y'])
            if nf == tf:
                nxt = (nx - tx, ny - ty)
        if True:
            cands = []
            for d in DIRS:
                c = w.clone()
                lg = c.move(*d)
                hh = c.hero
                if (hh.f, hh.x, hh.y) != (tf, tx, ty):
                    continue
                sc = 0
                for k, cur in (('hp', hh.hp), ('atk', hh.atk), ('def', hh.dfn), ('gold', hh.gold)):
                    if cur == int(r[k]):
                        sc += 1
                for k, kk in (('ky', 'y'), ('kb', 'b'), ('kr', 'r')):
                    if hh.keys.get(kk, 0) == int(r[k]):
                        sc += 1
                if bool(ev) == bool(lg):
                    sc += 1
                if nxt == d:          # 开门不落格：优先「朝下一行所在方向」开
                    sc += 2
                cands.append((sc, d))
            ok = max(cands)[1] if cands else None
            if ok is None:
                bad.append((i + 1, '无方向可达', prev_f, h.x, h.y, tf, tx, ty, ev))
                break
            w.move(*ok)
        # 比对
        mism = []
        for k, cur in (('hp', h.hp), ('atk', h.atk), ('def', h.dfn), ('gold', h.gold)):
            want = int(r[k])
            if cur != want:
                mism.append('%s 记录%s 实得%s' % (k, want, cur))
        for k, kk in (('ky', 'y'), ('kb', 'b'), ('kr', 'r')):
            want = int(r[k])
            cur = h.keys.get(kk, 0)
            if cur != want:
                mism.append('%s 记录%d 实得%d' % (k, want, cur))
        if mism:
            bad.append((i + 1, ' | '.join(mism), (h.f, h.x, h.y), ev))
        if h.f != prev_f:
            per_floor[h.f] = dict(step=i + 1, hp=h.hp, atk=h.atk, dfn=h.dfn, gold=h.gold,
                                  ky=h.keys.get('y', 0), kb=h.keys.get('b', 0), kr=h.keys.get('r', 0))
            prev_f = h.f
    return rows, bad, per_floor, w


if __name__ == '__main__':
    fn = sys.argv[1] if len(sys.argv) > 1 else '魔塔1_route_1F到21F.csv'
    rows, bad, per, w = replay(fn)
    print('文件 %s  记录 %d 行' % (fn, len(rows)))
    print('不一致 %d 处' % len(bad))
    for b in bad[:25]:
        print('   ', b)
    print('--- 首次进入各层时的状态（重放实测）---')
    for f in sorted(per):
        d = per[f]
        print('  %2dF step%-5d HP%-5d ATK%-3d DEF%-3d G%-5d 钥%d/%d/%d'
              % (f, d['step'], d['hp'], d['atk'], d['dfn'], d['gold'], d['ky'], d['kb'], d['kr']))
    h = w.hero
    print('终态 %dF(%d,%d) HP%d ATK%d DEF%d G%d 钥%d/%d/%d'
          % (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
             h.keys.get('y', 0), h.keys.get('b', 0), h.keys.get('r', 0)))
