"""逐层链式规划器：每层单独求最优路径，资源跨层传递。"""
import heapq, itertools
import mota_core as M

CNT = itertools.count(1)

def mk_world(f, x, y, hp, atk, dfn, gold, ky, kb, kr, cleared=frozenset(), bought=frozenset()):
    w = M.World.new(event_mode='on_entry', trap_mode='apply')
    h = w.hero
    h.f, h.x, h.y = f, x, y
    h.hp, h.atk, h.dfn, h.gold = hp, atk, dfn, gold
    h.keys['y'], h.keys['b'], h.keys['r'] = ky, kb, kr
    w.trap_done = True; w.flag3F = 1
    w.cleared = set(cleared); w.bought = set(bought)
    w.applied_events.clear(); w.apply_floor_events(f)
    return w

def lkey(w, f):
    """层内状态键：位置/钥匙/攻防/金币桶/本层已清格。"""
    h = w.hero
    cl = frozenset(k for k in w.cleared if k[0] == f)
    return (h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'],
            h.atk, h.dfn, min(h.gold // 50, 8), cl,
            frozenset(k for k in w.bought if k[0] == f))

def plan_layer(f, start, goal_pred, max_exp=400000, forbidden_floors=()):
    """start: world。goal_pred(world)->bool。返回 (ok, path_worlds, expanded)"""
    st = start
    pq = [(0, -st.hero.hp, 0, next(CNT), st)]
    best = {lkey(st, f): st.hero.hp}
    par = {}; wm = {}
    exp = 0
    while pq:
        _, _, _, sid, w = heapq.heappop(pq)
        h = w.hero
        k = lkey(w, f)
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
            if w2.hero.f in forbidden_floors:
                continue
            if w2.hero.f != f:
                continue          # 本层规划：不许跨层
            k2 = lkey(w2, f)
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
                    (hh.keys['y'], hh.keys['b'], hh.keys['r']), hh.gold))
        c = par[c]
    return list(reversed(out))
