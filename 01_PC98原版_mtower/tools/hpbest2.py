#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hpbest2.py —— HP 最大化搜索（精简状态键，快速上界）。
状态键去掉 cleared/bought，仅 (f,x,y,ky,kb,kr,atk,defn)，从而状态空间大幅缩小。
给出到达目标格的最大 HP 上界，并回溯格子序列供 walk_seq 精确复核。

用法: python3 -u hpbest2.py 13,6,10 2 3 4 5 6 7 8 9 10 11 12 13
"""
import sys, heapq
import state as S
import plan as P
import mota_core as M

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def key(w):
    h = w.hero
    return (h.f, h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'], h.atk, h.dfn)


def main():
    full = 'FULL' in sys.argv[1:]
    argv = [a for a in sys.argv[1:] if a != 'FULL']
    if argv and ',' in argv[0]:
        tf, tx, ty = (int(v) for v in argv[0].split(','))
        rest = argv[1:]
    else:
        tf, tx, ty = 13, 6, 10
        rest = argv
    floors = set(int(x) for x in rest) if rest else set(range(2, 14))

    w0 = S.replay() if full else S.replay(upto=42)
    print('起点', P.st(w0.hero), 'floors', sorted(floors), flush=True)

    seen = {key(w0): w0.hero.hp}
    prev = {}
    cnt = 0
    pq = [(-w0.hero.hp, cnt, w0)]
    n = 0
    target_key = None
    while pq and n < 4000000:
        neg_hp, _, cur = heapq.heappop(pq)
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
                heapq.heappush(pq, (-th, cnt, t))

    if target_key is None:
        print('✗ %d 状态内未到达 %dF(%d,%d)；当前最大 HP 状态示例:' % (n, tf, tx, ty), flush=True)
        # 打印 13F 内已见最大 HP
        best13 = max((v for kk, v in seen.items() if kk[0] == 13), default=None)
        print('   13F 内最大可达 HP =', best13, flush=True)
        return
    print('展开 %d 状态；%dF(%d,%d) 最大 HP(上界)=%d' % (n, tf, tx, ty, seen[target_key]), flush=True)
    path = []
    kk = target_key
    while kk in prev:
        pk, pos, lg = prev[kk]
        path.append((pos, lg))
        kk = pk
    path.reverse()
    print('格子序列 %d 步（供 walk_seq 复核）:' % len(path), flush=True)
    cells = [p[0] for p in path]
    # 压缩输出：按层分组
    seq = []
    for (f, x, y) in cells:
        seq.append('%d(%d,%d)' % (f, x, y))
    print('SEQ=' + ' '.join(seq), flush=True)
    # 同时打印带动作的行
    for pos, lg in path:
        print('  %dF(%d,%d) %s' % (pos[0], pos[1], pos[2], lg), flush=True)


main()
