# -*- coding: utf-8 -*-
"""跨层多源 Dijkstra：逐层求解 6F→11F，直接用 mota_core 状态机（保证规则保真）。

代价：先最小化累计掉血，再最小化步数。
"""
import heapq, itertools, sys
import mota_core as M

CNT = itertools.count(1)

# 各层目标（进入下一层的落点）
FLOOR_ORDER = [6, 7, 8, 9, 10, 11]
NEXT_F = {6: 7, 7: 8, 8: 9, 9: 10, 10: 11}

# 各层「必须拿到」的格子（拾取后 cleared 里出现）
MUST = {
    6: [],
    7: [],
    8: [(10, 2)],        # 8F 红钥 → 开 10F 红门
    9: [(9, 7)],         # 9F 铁盾（走暗墙拿）
    10: [(6, 3)],        # 10F BOSS
    11: [],
}

# 楼层事件在构造 world 时应用
def mk(f, hp, atk, dfn, gold, ky, kb, kr, cleared=(), bought=(), items=(), boss10=False):
    w = M.World.new(event_mode='on_entry', trap_mode='apply')
    h = w.hero
    h.f, h.x, h.y = f, 1, 2
    h.hp, h.atk, h.dfn, h.gold = hp, atk, dfn, gold
    h.keys['y'], h.keys['b'], h.keys['r'] = ky, kb, kr
    h.items = set(items)
    w.trap_done = True; w.flag3F = 1
    w.cleared = set(cleared); w.bought = set(bought); w.boss10 = boss10
    w.applied_events.clear(); w.apply_floor_events(f)
    return w


def skey(w):
    h = w.hero
    return (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
            h.keys['y'], h.keys['b'], h.keys['r'],
            frozenset(w.cleared), frozenset(w.bought), w.boss10)


def plan_layer(f, entry_worlds, must=(), max_exp=400000, log=print):
    """多源 Dijkstra：层内搜索，目标 = 抵达 f+1 层落点。返回 Pareto 前沿(世界列表)。"""
    must = set(must)
    nxt = NEXT_F.get(f)
    pq = []
    best = {}
    parents = {}
    for w0 in entry_worlds:
        hp0 = w0.hero.hp
        c = next(CNT); parents[c] = None
        heapq.heappush(pq, (0, 0, c, w0, hp0))
        best[skey(w0)] = (0, 0)
    exp = 0
    goals = []
    while pq:
        loss, steps, c, w, hp0 = heapq.heappop(pq)
        h = w.hero
        k = skey(w)
        if best.get(k, (1e18, 1e18)) < (loss, steps):
            continue
        exp += 1
        if exp > max_exp:
            log('  [%dF] 状态上限 %d' % (f, exp)); return goals
        # 目标判定
        if h.f == nxt:
            if all((f, m[0], m[1]) in w.cleared for m in must):
                goals.append(w)
            continue
        if h.f != f:
            continue
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            w2 = w.clone()
            lg = w2.move(dx, dy)
            if M.blocked(lg):
                continue
            if w2.hero.hp <= 0:
                continue
            if w2.hero.f != f and w2.hero.f != nxt:
                continue
            if w2.hero.f == nxt:
                if not all((f, m[0], m[1]) in w2.cleared for m in must):
                    continue
            k2 = skey(w2)
            l2 = hp0 - w2.hero.hp
            s2 = steps + 1
            if best.get(k2, (1e18, 1e18)) <= (l2, s2):
                continue
            best[k2] = (l2, s2)
            c2 = next(CNT); parents[c2] = (c, (dx, dy))
            heapq.heappush(pq, (l2, s2, c2, w2, hp0))
    return goals


def trace(w, parents_by_obj):
    """需要 parents 映射才能回溯；这里用 world 对象 id 存父链。"""
    return []
