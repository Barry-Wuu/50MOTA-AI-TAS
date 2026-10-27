"""Dijkstra（按 掉血, 步数）求 7F(11,10) → 11F 最少掉血路线，记录真实方向动作。
起点高血量（100000）以避免“打不过”提前阻断、探索全图求最优；最终掉血即血线需求。
"""
import sys, csv, heapq, itertools
import mota_core as M

ATK0, DFN0, GOLD0, BLUE0, RED0 = 20, 10, 44, 1, 0
TIE = itertools.count()

def make_start(yellow, hp=100000):
    w = M.World.new(event_mode='on_entry', trap_mode='apply')
    h = w.hero
    h.f, h.x, h.y = 7, 11, 10
    h.hp, h.atk, h.dfn, h.gold = hp, ATK0, DFN0, GOLD0
    h.keys['y'], h.keys['b'], h.keys['r'] = yellow, BLUE0, RED0
    w.apply_floor_events(7)
    return w

def key(w):
    h = w.hero
    return (h.f, h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'],
            frozenset(c for c in w.cleared if c in M.PICKUP_CELLS),
            frozenset(w.bought))

def solve(yellow, cap=8000000):
    st = make_start(yellow)
    pq = [(0, 0, next(TIE), st)]
    seen = {}
    n = 0
    while pq:
        loss, steps, _, w = heapq.heappop(pq)
        if w.hero.f == 11:
            path, acts, cur = [], [], w
            while cur is not None:
                path.append(cur); acts.append(cur._act); cur = cur._par
            return list(reversed(path)), list(reversed(acts))[1:], n, loss
        k = key(w)
        if k in seen and (seen[k][0], seen[k][1]) <= (loss, steps):
            continue
        seen[k] = (loss, steps)
        n += 1
        if n > cap:
            return ('cap', n)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            w2 = w.clone()
            before = w2.hero.hp
            log = w2.move(dx, dy)
            if M.blocked(log):
                continue
            add = before - w2.hero.hp
            w2._par = w; w2._act = (dx, dy)
            heapq.heappush(pq, (loss + max(add, 0), steps + 1, next(TIE), w2))
    return None, None, n, None

KEYMAP = {(0, -1): '8', (1, 0): '6', (0, 1): '2', (-1, 0): '4'}

if __name__ == '__main__':
    yellow = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 8000000
    print(f'规划：黄钥匙={yellow} 起始HP=100000 上限={cap}')
    r = solve(yellow, cap)
    if isinstance(r, tuple) and r[0] == 'cap':
        print('状态上限', r[1]); sys.exit(1)
    if r[0] is None:
        print('图不可达（无解）'); sys.exit(1)
    route, acts, n, loss = r
    print(f'探索态={n} 路径步数={len(acts)} 累计掉血={loss}')
    w = route[-1]
    print('终态:', 'HP', w.hero.hp, 'ATK', w.hero.atk, 'DEF', w.hero.dfn,
          'GOLD', w.hero.gold, '钥匙', dict(w.hero.keys), 'boss10', w.boss10,
          'caveats', sorted(w.caveats), '已购', sorted(w.bought))

    ver = make_start(yellow)
    rows = []
    for k, d in enumerate(acts, 1):
        log = ver.move(*d)
        if M.blocked(log):
            print('!! 第', k, '步被拒:', log); break
        h = ver.hero
        rows.append([k, h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
                     h.keys['y'], h.keys['b'], h.keys['r'], ' | '.join(log)])
        if h.f == 11:
            break
    print('复验终点', (ver.hero.f, ver.hero.x, ver.hero.y), '步数', len(rows))
    with open('route_7f_to_11f.csv', 'w', newline='', encoding='utf8') as fh:
        wr = csv.writer(fh)
        wr.writerow(['step', 'floor', 'x', 'y', 'HP', 'ATK', 'DEF', 'GOLD', '黄钥', '蓝钥', '红钥', '事件'])
        wr.writerows(rows)

    keys = []
    ver2 = make_start(yellow)
    for d in acts:
        log = ver2.move(*d)
        assert not M.blocked(log), f'复验失败 {d} {log}'
        keys.append(KEYMAP[d])
        if any('购物' in l for l in log):
            keys.append('E')
    with open('keys_7f_to_11f.txt', 'w', encoding='utf8') as fh:
        fh.write(''.join(keys))
    print('按键数', len(keys), '串:', ''.join(keys))
