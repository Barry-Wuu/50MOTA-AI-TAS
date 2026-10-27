"""7F→11F 全链规划：层内位掩码搜索，跨层允许 f→f+1。"""
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

def solve(hp, ky=6, kb=1, kr=0, gold=200, atk=20, dfn=10,
          fmin=7, fmax=11, max_exp=3000000, goal_f=11):
    st = L.mk_world(7, 11, 10, hp, atk, dfn, gold, ky, kb, kr)
    root = next(CNT)
    pq = [(0, -st.hero.hp, 0, root, st)]
    best = {gkey(st): st.hero.hp}; par = {root: None}; wm = {root: st}
    exp = 0; maxf = 7
    while pq:
        _, _, _, sid, w = heapq.heappop(pq)
        h = w.hero
        k = gkey(w)
        if best.get(k, -10**9) > h.hp:
            continue
        exp += 1
        maxf = max(maxf, h.f)
        if exp > max_exp:
            return ('cap', exp, None)
        if h.f == goal_f:
            return ('ok', exp, (w, par, wm, sid))
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            w2 = w.clone()
            log = w2.move(dx, dy)
            if M.blocked(log) or w2.hero.hp <= 0:
                continue
            if not (fmin <= w2.hero.f <= fmax):
                continue
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

if __name__ == '__main__':
    hp = int(sys.argv[1]); ky = int(sys.argv[2]); gold = int(sys.argv[3])
    mx = int(sys.argv[4]) if len(sys.argv) > 4 else 3000000
    r = solve(hp, ky=ky, gold=gold, max_exp=mx)
    print('结果:', r[0], 'exp', r[1])
    if r[2]:
        p = trace(r[2])
        print(f'步数={len(p)-1} 末态 11F({p[-1][1]},{p[-1][2]}) HP={p[-1][3]} ATK={p[-1][4]} DEF={p[-1][5]} keys={p[-1][6]} G={p[-1][7]}')
        for q in p:
            print('  ', q)
