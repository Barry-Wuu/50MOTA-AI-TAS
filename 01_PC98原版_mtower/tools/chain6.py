# -*- coding: utf-8 -*-
"""5F(取剑后) → 11F 分层规划器。

层内搜索用真实 mota_core 状态机（规则保真），状态键含「本层已清格集合」+资源。
跨层：到达本层上行梯 → warp 到下一层落点，作为下一层的入口世界。
跨层时对资源向量做 Pareto 折叠（只保留非支配者），控制爆炸。
"""
import collections, itertools, sys, time
import mota_core as M

CNT = itertools.count(1)
DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))

# 每层：本层上行梯格（= warp 目标层 f+1 的那一格）
UPSTAIR = {5: (1, 1), 6: (11, 11), 7: (1, 1), 8: (6, 1), 9: (1, 11), 10: (6, 11)}
# 每层必须拿到的格子（相对层）
MUST = {5: [], 6: [], 7: [], 8: [(10, 2)], 9: [(9, 7)], 10: [(6, 3)], 11: []}


def mk_world(f, x, y, hp, atk, dfn, gold, ky, kb, kr, cleared=(), bought=(), boss10=False, items=()):
    w = M.World.new(event_mode='on_entry', trap_mode='apply')
    h = w.hero
    h.f, h.x, h.y = f, x, y
    h.hp, h.atk, h.dfn, h.gold = hp, atk, dfn, gold
    h.keys['y'], h.keys['b'], h.keys['r'] = ky, kb, kr
    h.items = set(items)
    w.trap_done = True; w.flag3F = 1
    w.cleared = set(cleared); w.bought = set(bought); w.boss10 = boss10
    w.applied_events.clear(); w.apply_floor_events(f)
    return w


def res_of(w):
    h = w.hero
    return (h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'])


def pareto(items):
    out = []
    for r, p in items:
        if any(all(a >= b for a, b in zip(r2, r)) for r2, _ in out):
            continue
        out = [(r2, p2) for r2, p2 in out if not all(a >= b for a, b in zip(r, r2))]
        out.append((r, p))
    return out


def explore(f, worlds, cap=4000000, verbose=True, t0=None):
    """层内 BFS；返回到达上行梯（warp 到 f+1）的世界列表。"""
    up = UPSTAIR[f]
    must = set(MUST[f])
    seen = set()
    q = collections.deque()
    for w in worlds:
        k = skey(w, f)
        if k in seen:
            continue
        seen.add(k); q.append(w)
    n = 0; outs = []
    while q:
        w = q.popleft(); n += 1
        if n % 500000 == 0:
            print('   [%dF] %d 状态  %.1fs' % (f, n, time.time() - t0))
        if n > cap:
            print('   [%dF] 状态爆炸 cap' % f); break
        for dx, dy in DIRS:
            w2 = w.clone()
            lg = w2.move(dx, dy)
            if M.blocked(lg):
                continue
            if w2.hero.hp <= 0:
                continue
            if w2.hero.f != f:
                # 跨层：只接受 warp 到 f+1
                tgt = M.warp_to(f, w2.hero.x, w2.hero.y) if False else None
                # 判断是否踩到上行梯
                if (w2.hero.f == f + 1):
                    # 必须项都在本层清掉
                    if all((f, m[0], m[1]) in w2.cleared for m in must):
                        outs.append(w2)
                continue
            k2 = skey(w2, f)
            if k2 in seen:
                continue
            seen.add(k2); q.append(w2)
    if verbose:
        print('   [%dF] 枚举 %d 状态 → 出口候选 %d  (%.1fs)' % (f, n, len(outs), time.time() - t0))
    return outs


def skey(w, f):
    h = w.hero
    return (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
            h.keys['y'], h.keys['b'], h.keys['r'],
            frozenset(c for c in w.cleared if c[0] == f),
            frozenset(c for c in w.bought if c[0] == f),
            w.boss10)


def trim(w, f):
    """跨层时丢弃已离开层的痕迹。"""
    w.cleared = {c for c in w.cleared if c[0] == f}
    w.bought = {c for c in w.bought if c[0] == f}
    return w
