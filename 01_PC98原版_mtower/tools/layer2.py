"""层内位掩码规划器：cleared 只记"门+怪"（影响通行），物品效果直接进状态键。"""
import heapq, itertools
import mota_core as M
CNT = itertools.count(1)

def blockers(f):
    """返回 {(x,y):bit} 只含门与怪（通行阻断物）"""
    d = {}
    for y in range(13):
        for x in range(13):
            if M.terrain(f, x, y) == 1:
                continue
            o = M.obj_raw(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3))
            if ty in ('DOOR', 'MONSTER'):
                d[(x, y)] = len(d)
    return d

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

def plan_layer(f, start, goal_pred, max_exp=600000, cross=True):
    """层内搜索。cross=True 允许踩楼梯跨层（终点判定用 goal_pred）。"""
    st = start
    blk = blockers(f)
    # ⚠️ blk 的键是 (x,y)，而 cleared/bought 存的是 (f,x,y) —— 必须用 c[1:] 取键，
    #    否则 mask 恒为 0：开门/击杀状态记不住，搜索会把"门还没开"和"门已开"当成同一状态剪掉。
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
        mask = 0
        for c in w.cleared:
            if c[0] == f:
                b = blk.get(c[1:])
                if b is not None:
                    mask |= 1 << b
        bo = 0
        for c in w.bought:
            if c[0] == f:
                s = shops.get(c[1:])
                if s is not None:
                    bo |= 1 << s
        return (h.f, h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'],
                h.atk, h.dfn, min(h.gold // 50, 10), mask, bo)
    root = next(CNT)
    pq = [(0, -st.hero.hp, 0, root, st)]
    best = {key(st): st.hero.hp}; par = {root: None}; wm = {root: st}
    exp = 0
    while pq:
        _, _, _, sid, w = heapq.heappop(pq)
        h = w.hero
        k = key(w)
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
            if not cross and w2.hero.f != f:
                continue
            if cross and w2.hero.f not in (f, f + 1):
                continue
            k2 = key(w2)
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
