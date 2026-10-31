# -*- coding: utf-8 -*-
"""probe_reach.py —— 站在当前状态，列出本层「能打到/能拿到什么、代价多少」

用途：翻译攻略时，把「打蝙蝠 / 拿钥匙」这类方位词落到具体格子。
本工具只读，不改路线、不写文件。

用法：
  python tools/probe_reach.py 9        # 在当前所在层做可达性/代价清单
  python tools/probe_reach.py 9 12     # 指定层（同层才有效）
"""
import sys, os, io, math, heapq, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M
import run_segs as R


def step_cost(w, f, nx, ny):
    """(可通过, HP代价, 钥匙数, 说明)"""
    if not (1 <= nx <= 11 and 1 <= ny <= 11):
        return False, 0, 0, ''
    if w.terrain_at(f, nx, ny) in (1, 2):
        return False, 0, 0, ''
    o = w.at(f, nx, ny)
    if not o:
        return True, 0, 0, ''
    ty = M.TYPE.get(M.oatr(o, 3))
    if o == 89:
        return True, 0, 0, '暗墙'
    if o in M.KEY_OF or ty in ('STATUS', 'ITEM', 'NORMAL', 'SCORE', 'MESSAGE'):
        return True, 0, 0, ''
    if ty == 'DOOR':
        col = M.DOOR_OF.get(o)
        if col is None or w.hero.keys[col] <= 0:
            return False, 0, 0, ''
        return True, 0, 1, '门'
    if ty == 'SELL':
        return (w.hero.gold >= M.SHOP_PRICE.get(o, 0)), 0, 0, '商店'
    if ty == 'SAIDAN':
        return (f, nx, ny) in M.ALTAR_CELLS, 0, 0, '祭坛'
    if ty == 'MONSTER':
        r = w.battle(o)
        if r is None or r[0] >= w.hero.hp:
            return False, 0, 0, ''
        return True, r[0], 0, '怪'
    return False, 0, 0, ''


def probe(w, f):
    h = w.hero
    if h.f != f:
        print('当前在 %dF，不在 %dF' % (h.f, f))
        return
    start = (h.x, h.y)
    dist = {start: (0, 0)}          # (hp 累计, 钥匙累计)
    prev = {start: None}
    pq = [(0, 0, start)]
    while pq:
        hp_c, k_c, c = heapq.heappop(pq)
        if (hp_c, k_c) > dist.get(c, (1e9, 1e9)):
            continue
        for d in R.DIRS:
            n = (c[0] + d[0], c[1] + d[1])
            ok, dh, dk, _ = step_cost(w, f, *n)
            if not ok:
                continue
            nv = (hp_c + dh, k_c + dk)
            if nv[0] >= h.hp:        # 累计战损超过当前 HP 视为不可达
                continue
            if nv < dist.get(n, (1e9, 1e9)):
                dist[n] = nv
                prev[n] = c
                heapq.heappush(pq, (nv[0], nv[1], n))
    print('当前 %s' % R.st(h))
    print('可达格数 %d' % len(dist))
    print()
    rows = []
    for (x, y) in sorted(dist, key=lambda p: (dist[p][0], p[1], p[0])):
        o = w.at(f, x, y)
        if not o:
            continue
        ty = M.TYPE.get(M.oatr(o, 3), '?')
        tag = ''
        if o in M.KEY_OF:
            tag = 'KEY'
        elif ty == 'DOOR':
            tag = 'DOOR'
        elif ty == 'MONSTER':
            tag = 'MON'
        elif ty in ('STATUS', 'ITEM'):
            tag = 'ITEM'
        elif o == 89:
            tag = 'DARK'
        elif ty == 'SELL':
            tag = 'SHOP'
        else:
            tag = ty
        rows.append('  (%2d,%2d) %-4s obj%-3d %-20s 累计战损%-5d 耗钥%d'
                    % (x, y, tag, o, M.oname(o)[:20], dist[(x, y)][0], dist[(x, y)][1]))
    for r in rows:
        print(r)


if __name__ == '__main__':
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = R.main()
    w = R.LAST_W
    print('=== 已推进到 %s ===' % R.st(w.hero))
    f = int(sys.argv[1]) if len(sys.argv) > 1 else w.hero.f
    print()
    probe(w, f)
