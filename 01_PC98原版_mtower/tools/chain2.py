"""链式规划：逐层求解，层内位掩码搜索，目标是抵达上层楼梯并最大化剩余资源。"""
import heapq, itertools, sys
import mota_core as M
import layer2 as L

CNT = itertools.count(1)
BLK = {f: L.blockers(f) for f in range(1, 13)}

def gkey(w):
    h = w.hero
    mask = 0
    for c in w.cleared:
        b = BLK.get(c[0], {}).get(c)
        if b is not None:
            mask |= 1 << b
    bo = 0
    for c in w.bought:
        b = BLK.get(c[0], {}).get(c)
        bo |= 1 << (b if b is not None else 200)
    return (h.f, h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'],
            h.atk, h.dfn, min(h.gold // 50, 20), mask, bo, w.boss10)

def search(start, goal_pred, fmin, fmax, max_exp=1500000, allow_up=True, allow_down=True):
    root = next(CNT)
    pq = [(0, -start.hero.hp, 0, root, start)]
    best = {gkey(start): start.hero.hp}; par = {root: None}; wm = {root: start}
    exp = 0
    while pq:
        _, _, _, sid, w = heapq.heappop(pq)
        h = w.hero
        k = gkey(w)
        if best.get(k, -10**9) > h.hp:
            continue
        exp += 1
        if exp > max_exp:
            return ('cap', exp, None)
        if goal_pred(w):
            return ('ok', exp, (w, par, wm, sid))
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            w2 = w.clone()
            log = w2.move(dx, dy)
            if M.blocked(log) or w2.hero.hp <= 0:
                continue
            f2 = w2.hero.f
            if f2 > h.f and not allow_up: continue
            if f2 < h.f and not allow_down: continue
            if not (fmin <= f2 <= fmax): continue
            k2 = gkey(w2)
            if best.get(k2, -10**9) >= w2.hero.hp:
                continue
            best[k2] = w2.hero.hp
            s2 = next(CNT); par[s2] = sid; wm[s2] = w2
            heapq.heappush(pq, (0, -w2.hero.hp, 0, s2, w2))
    return ('fail', exp, None)

def trace(res):
    w, par, wm, sid = res
    out = []; c = sid
    while c is not None:
        ww = wm[c]; hh = ww.hero
        out.append((hh.f, hh.x, hh.y, hh.hp, hh.atk, hh.dfn,
                    (hh.keys['y'], hh.keys['b'], hh.keys['r']), hh.gold, ww.boss10))
        c = par[c]
    return list(reversed(out))
