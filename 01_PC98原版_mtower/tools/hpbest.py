#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hpbest.py —— HP 最大化搜索（Dijkstra/最长路）。
从给定起点（默认：回放 CSV 到踩 3F 陷阱后）出发，在不限战斗的前提下，
求到达目标格 (tf,tx,ty) 时的最大 HP（即"理论上界"），并回溯路径。

用法: python3 hpbest.py [tf,tx,ty] [floors...]
  例: python3 hpbest.py 13,6,10 2 3 4 5 6 7 8 9 10 11 12 13
"""
import sys, collections, heapq
import state as S
import plan as P
import mota_core as M

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def key(w):
    h = w.hero
    return (h.f, h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'],
            frozenset(sorted(w.cleared)), frozenset(sorted(w.bought)),
            h.atk, h.dfn)


def main():
    argv = sys.argv[1:]
    if not argv or ',' in argv[0]:
        tf, tx, ty = (int(v) for v in (argv[0] if argv and ',' in argv[0] else '13,6,10').split(','))
        rest = argv[1:]
    else:
        tf, tx, ty = 13, 6, 10
        rest = argv
    floors = set(int(x) for x in rest) if rest else set(range(2, 14))

    # 起点：回放 CSV 到踩陷阱后（第42步），即真实 post-trap 状态
    w0 = S.replay(upto=42)
    print('起点', P.st(w0.hero), 'floors', sorted(floors))

    best = {}
    prev = {}
    cnt = 0
    pq = [(-w0.hero.hp, cnt, w0, None)]   # (-hp, tie, world, parent_key)
    seen = {key(w0): w0.hero.hp}
    n = 0
    target_key = None
    while pq and n < 2000000:
        neg_hp, _, cur, _ = heapq.heappop(pq)
        n += 1
        k = key(cur)
        if -neg_hp < seen.get(k, -1):
            continue
        if (cur.hero.f, cur.hero.x, cur.hero.y) == (tf, tx, ty):
            target_key = k
            break
        for dx, dy in DIRS:
            t = cur.clone()
            lg = t.move(dx, dy)
            if M.blocked(lg) or t.hero.hp <= 0:
                continue
            if t.hero.f not in floors:
                continue
            tk = key(t)
            th = t.hero.hp
            if tk not in seen or th > seen[tk]:
                seen[tk] = th
                prev[tk] = (k, (t.hero.f, t.hero.x, t.hero.y), lg)
                cnt += 1
                heapq.heappush(pq, (-th, cnt, t, tk))

    if target_key is None:
        print('✗ 在 %d 状态内未到达 %dF(%d,%d)' % (n, tf, tx, ty))
        # 看看最接近的目标层可达情况
        return
    print('展开 %d 状态；到达 %dF(%d,%d) 最大 HP=%d' % (n, tf, tx, ty, seen[target_key]))
    # 回溯
    path = []
    kk = target_key
    while kk in prev:
        pk, pos, lg = prev[kk]
        path.append((pos, lg))
        kk = pk
    path.reverse()
    print('路径 %d 步：' % len(path))
    for pos, lg in path:
        print('  %dF(%d,%d)  %s' % (pos[0], pos[1], pos[2], lg))


main()
