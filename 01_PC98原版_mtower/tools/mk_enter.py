"""推算「从 1F 起点踏入 2F / 3F / 4F」的最少移动步数。

踏入判定：hero.f == N（任意格）。启发式取该层楼梯落点格的下界（可采纳）：
  2F 落点 (x1,y2)  ← 1F(c1,r1) ter4 上梯，实机确认
  3F 落点 (x2,y11) ← ter6 传送表 [16]=28 [17]=11
  4F 落点 (x11,y10)← ter8 传送表 [16]=50 [17]=10
"""
import heapq, itertools, json, collections
import mota_core as M

LANDING = {2: (2, 1, 2), 3: (3, 2, 11), 4: (4, 11, 10)}


def astar(target_floor, cap=600000):
    goal_cell = LANDING[target_floor]
    H = M.heuristic(goal_cell)
    TIE = itertools.count()
    st = M.World.new(event_mode='static', trap_mode='apply')
    pq = [(H.get((st.hero.f, st.hero.x, st.hero.y), 99), 0, next(TIE), st)]
    closed = set()
    n = 0
    while pq:
        _, gg, _, w = heapq.heappop(pq)
        k = (w.hero.f, w.hero.x, w.hero.y, w.hero.keys['y'], w.hero.keys['b'],
             frozenset(c for c in w.cleared if c in M.PICKUP_CELLS))
        if k in closed:
            continue
        closed.add(k)
        if w.hero.f == target_floor:          # 踏入该层即达成
            path, acts, cur = [], [], w
            while cur is not None:
                path.append(cur); acts.append(getattr(cur, '_act', None)); cur = getattr(cur, '_par', None)
            return list(reversed(path)), list(reversed(acts))[1:], n, gg
        if n > cap:
            return None
        n += 1
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            w2 = w.clone()
            log = w2.move(dx, dy)
            if M.blocked(log):
                continue
            kk = (w2.hero.f, w2.hero.x, w2.hero.y, w2.hero.keys['y'], w2.hero.keys['b'],
                  frozenset(c for c in w2.cleared if c in M.PICKUP_CELLS))
            if kk in closed:
                continue
            w2._par = w; w2._act = (dx, dy)
            hf = 0 if w2.hero.f == target_floor else H.get((w2.hero.f, w2.hero.x, w2.hero.y), 99)
            heapq.heappush(pq, (gg + 1 + hf, gg + 1, next(TIE), w2))
    return None


def replay(actions):
    """按动作串重放，逐帧记录"""
    w = M.World.new(event_mode='static', trap_mode='apply')
    rows = []
    step = 0
    for d in actions:
        step += 1
        log = w.move(*d)
        if M.blocked(log):
            return None, f'第{step}步被拒：{log}'
        rows.append([step, w.hero.f, w.hero.x, w.hero.y, w.hero.hp, w.hero.atk, w.hero.dfn,
                     w.hero.gold, w.hero.keys['y'], w.hero.keys['b'],
                     ' | '.join(log)])
    return w, rows


if __name__ == '__main__':
    out = {}
    for N in (2, 3, 4):
        res = astar(N)
        assert res, f'{N}F 搜索失败'
        path, acts, nodes, cost = res
        w, rows = replay(acts)
        assert w is not None, rows
        assert w.hero.f == N, f'复验终点层={w.hero.f}'
        # 每层次数：按「该步结束时所在层」计数
        per = collections.Counter(r[1] for r in rows)
        # 踏入该层的步号
        enter_step = next(r[0] for r in rows if r[1] == N)
        out[N] = {
            'steps': len(rows),
            'enter_step': enter_step,
            'per_floor_steps': {str(k): v for k, v in sorted(per.items())},
            'final_cell': [int(w.hero.x), int(w.hero.y)],
            'HP': int(w.hero.hp), 'ATK': int(w.hero.atk), 'DEF': int(w.hero.dfn),
            'GOLD': int(w.hero.gold), 'keys_y': int(w.hero.keys['y']), 'keys_b': int(w.hero.keys['b']),
            'nodes': nodes,
            'events': [r[10] for r in rows if ('剧本' in r[10] or '掉血' in r[10])],
        }
        with open(f'route_enter_{N}f.csv', 'w', newline='', encoding='utf8') as fh:
            import csv
            wr = csv.writer(fh)
            wr.writerow(['step', 'floor', 'x', 'y', 'HP', 'ATK', 'DEF', 'GOLD', '黄钥匙', '蓝钥匙', '本步事件'])
            wr.writerows(rows)
        # 导出按键串（8上 2下 4左 6右，同 keys_1f_to_5f.json 约定）
        KS = {(0,-1):'8', (0,1):'2', (-1,0):'4', (1,0):'6'}
        keys = ''.join(KS[d] for d in acts)
        out[N]['keys'] = keys
        json.dump({'keys_numpad': keys, 'steps': len(acts),
                   'note': '8上/2下/4左/6右；开门需连按两次同方向（撞门+进入）'},
                  open(f'keys_enter_{N}f.json','w'), ensure_ascii=False)
        open(f'keys_enter_{N}f.txt','w').write(keys)
        print(f'按键串({len(keys)}): {keys}')
        print(f'== 进入 {N}F ==')
        print(json.dumps(out[N], ensure_ascii=False, indent=1))
        print()
    json.dump(out, open('route_enter_summary.json', 'w'), ensure_ascii=False, indent=1)
