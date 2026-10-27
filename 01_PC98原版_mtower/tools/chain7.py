# -*- coding: utf-8 -*-
"""6F → 11F 分层规划器（层内全枚举 + 跨层 Pareto 折叠）。

层内：直接用 mota_core 的真实状态机（规则保真），状态键紧凑：
      (格子, 本层已清阻断物位掩码, 已买商店掩码, 钥匙, 金币桶, atk, dfn)
      hp 用「同键取最大 hp」做支配剪枝。
跨层：到达本层上行梯 → warp 到下一层；把资源向量 (hp,atk,dfn,gold,ky,kb,kr) 做 Pareto 折叠。

必须项（本层内必须完成）：
      8F  必须拿到红钥 (10,2)（10F 红门要用）
      9F  必须拿到铁盾 (9,7)（BOSS 战 DEF 不够打不动）
      10F 必须打死 BOSS (6,3)
"""
import collections
import heapq
import itertools
import mota_core as M

CNT = itertools.count(1)
DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))

# 每层上行梯格（= warp 去 f+1 的那一格）
UPSTAIR = {6: (11, 11), 7: (1, 1), 8: (6, 1), 9: (1, 11), 10: (6, 11)}
# 每层必须拿到的格子（BOSS 战还要 10F 的 boss10 标记）
MUST = {6: [], 7: [], 8: [(10, 2)], 9: [(9, 7)], 10: [(6, 3)]}


def blockers(f):
    """(x,y)->bit，只含门与怪（含暗墙），用于位掩码。"""
    d = {}
    w = M.World.new()
    w.apply_floor_events(f)
    for y in range(13):
        for x in range(13):
            o = w.at(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            if ty in ('DOOR', 'MONSTER'):
                d[(x, y)] = len(d)
    return d


def mk_world(f, x, y, hp, atk, dfn, gold, ky, kb, kr, cleared=(), bought=(), boss10=False):
    w = M.World.new(event_mode='on_entry', trap_mode='apply')
    h = w.hero
    h.f, h.x, h.y = f, x, y
    h.hp, h.atk, h.dfn, h.gold = hp, atk, dfn, gold
    h.keys['y'], h.keys['b'], h.keys['r'] = ky, kb, kr
    w.trap_done = True
    w.flag3F = 1
    w.cleared = set(cleared)
    w.bought = set(bought)
    w.boss10 = boss10
    w.applied_events.clear()
    w.apply_floor_events(f)
    return w


def res_of(w):
    h = w.hero
    return (h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'])


def pareto(items):
    """items: [(res, payload)] → 只留非支配者"""
    out = []
    for r, p in items:
        if any(all(a >= b for a, b in zip(r2, r)) for r2, _ in out):
            continue
        out = [(r2, p2) for r2, p2 in out if not all(a >= b for a, b in zip(r, r2))]
        out.append((r, p))
    return out


def plan_floor(f, worlds, max_exp=1200000, verbose=True):
    """枚举本层内到达上行梯的所有状态（带必须项检查）。返回 [(res, world)]"""
    up = UPSTAIR[f]
    must = MUST[f]
    blk = blockers(f)
    shops = {}
    w0 = M.World.new()
    w0.apply_floor_events(f)
    for y in range(13):
        for x in range(13):
            o = w0.at(f, x, y)
            if o and o in M.SHOP:
                shops[(x, y)] = len(shops)

    def key(w):
        h = w.hero
        m = 0
        for c in w.cleared:
            if c[0] == f and c in blk:
                m |= 1 << blk[c]
        bo = 0
        for c in w.bought:
            if c[0] == f:
                bo |= 1 << shops.get(c[1:], 99)
        return (h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'],
                h.atk, h.dfn, h.gold // 25, m, bo)

    pq = []
    best = {}
    for w in worlds:
        k = key(w)
        if best.get(k, -1) >= w.hero.hp:
            continue
        best[k] = w.hero.hp
        heapq.heappush(pq, (0, next(CNT), w))
    outs = []
    exp = 0
    while pq:
        _, _, w = heapq.heappop(pq)
        h = w.hero
        exp += 1
        if exp > max_exp:
            if verbose:
                print('   [%dF] 达到展开上限 %d' % (f, exp))
            break
        if (h.x, h.y) == up and all((f, m[0], m[1]) in w.cleared for m in must):
            if f == 10 and not w.boss10:
                continue
            outs.append(w)
            continue
        for dx, dy in DIRS:
            w2 = w.clone()
            log = w2.move(dx, dy)
            if M.blocked(log):
                continue
            if w2.hero.hp <= 0:
                continue
            if w2.hero.f != f:
                continue          # 跨层只在踩到上行梯时由外部处理
            k2 = key(w2)
            if best.get(k2, -1) >= w2.hero.hp:
                continue
            best[k2] = w2.hero.hp
            heapq.heappush(pq, (0, next(CNT), w2))
    if verbose:
        print('   [%dF] 展开 %d 状态 → 出口候选 %d' % (f, exp, len(outs)))
    return [(res_of(w), w) for w in outs]


def warp_next(f, w):
    """把站在上行梯上的世界推进到下一层，返回下一层的世界列表。"""
    tgt = M.warp_to(f, w.hero.x, w.hero.y)
    if tgt is None:
        return []
    nf, nx, ny = tgt
    w2 = w.clone()
    w2.hero.f, w2.hero.x, w2.hero.y = nf, nx, ny
    w2.apply_floor_events(nf)
    return [w2]


def run(start_world, floors=(6, 7, 8, 9, 10)):
    cur = [start_world]
    for f in floors:
        outs = plan_floor(f, cur)
        nxt = []
        for res, w in outs:
            nxt.extend(warp_next(f, w))
        if not nxt:
            print('  !! %dF 无解' % f)
            return None
        # 折叠：同一资源向量只留一个；再 Pareto
        seen = {}
        items = []
        for w in nxt:
            r = res_of(w)
            if r in seen:
                continue
            seen[r] = w
            items.append((r, w))
        cur = [w for _, w in pareto(items)]
        print('  → %dF 入口候选 %d' % (f + 1, len(cur)))
    return cur
