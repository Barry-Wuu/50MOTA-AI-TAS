"""生成并复验「1F 起点 → 5F 铁剑」路线：输出 route_sword_1f_to_5f.csv + 摘要，供 README/MAP_NOTES 引用。"""
import heapq, collections, itertools, csv, json, time
import mota_core as M

TIE = itertools.count()
GOAL = M.make_goal('sword')          # (5, 11, 11)


def astar(cap=400000):
    H = M.heuristic(GOAL)
    st = M.World.new(event_mode='static', trap_mode='apply')
    pq = [(H.get((st.hero.f, st.hero.x, st.hero.y), 99), 0, next(TIE), st)]
    closed = set()
    g = {}
    n = 0
    while pq:
        _, gg, _, w = heapq.heappop(pq)
        k = (w.hero.f, w.hero.x, w.hero.y, w.hero.keys['y'], w.hero.keys['b'],
             frozenset(c for c in w.cleared if c in M.PICKUP_CELLS))
        if k in closed:
            continue
        closed.add(k)
        if (w.hero.f, w.hero.x, w.hero.y) == GOAL:
            path, cur, acts = [], w, []
            while cur is not None:
                path.append(cur)
                acts.append(getattr(cur, '_act', None))
                cur = getattr(cur, '_par', None)
            return list(reversed(path)), list(reversed(acts))[1:], n
        if n > cap:
            return None
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            w2 = w.clone()
            log = w2.move(dx, dy)
            if M.blocked(log):
                continue
            kk = (w2.hero.f, w2.hero.x, w2.hero.y, w2.hero.keys['y'], w2.hero.keys['b'],
                  frozenset(c for c in w2.cleared if c in M.PICKUP_CELLS))
            if kk in closed:
                continue
            w2._par = w
            w2._act = (dx, dy)              # 记录真实动作，复验时照单执行
            heapq.heappush(pq, (gg + 1 + H.get((w2.hero.f, w2.hero.x, w2.hero.y), 99), gg + 1, next(TIE), w2))
    return None


route, actions, n = astar()
assert route, '搜索失败'

# —— 复验：从干净世界按同一串方向重放，逐帧记录 ——
dirs = [(d, 0, 0) for d in actions]        # 动作即按键，无需从坐标反推
w = M.World.new(event_mode='static', trap_mode='apply')
rows, err = [], None
step = 0
prevf = w.hero.f
for d, f_from, f_to in dirs:
    step += 1
    log = w.move(*d)
    if M.blocked(log):
        err = f'第{step}步被拒：{log}'
        break
    rows.append([step, w.hero.f, w.hero.x, w.hero.y, w.hero.hp, w.hero.atk, w.hero.dfn,
                 w.hero.gold, w.hero.keys['y'], w.hero.keys['b'],
                 ' | '.join(l for l in log if not l.startswith('拾') or True)])
end_cell = (w.hero.f, w.hero.x, w.hero.y)
assert err is None, err
assert (w.hero.f, w.hero.x, w.hero.y) == GOAL, f'终点不符：{w.hero.f},{w.hero.x},{w.hero.y}'

out = 'route_sword_1f_to_5f.csv'
with open(out, 'w', newline='', encoding='utf8') as fh:
    wr = csv.writer(fh)
    wr.writerow(['step', 'floor', 'x', 'y', 'HP', 'ATK', 'DEF', 'GOLD', '黄钥匙', '蓝钥匙', '本步事件'])
    wr.writerows(rows)
per = collections.Counter(r[1] for r in rows)
hurt = [(r[0], int(r[4])) for r in rows]
drops = [r for r in rows if '掉血' in r[10] or '剧本' in r[10]]
summary = {
    'steps_replayed': len(rows),
    'nodes_expanded': n,
    'final': {'floor': int(w.hero.f), 'cell': [int(w.hero.x), int(w.hero.y)],
              'HP': int(w.hero.hp), 'ATK': int(w.hero.atk), 'DEF': int(w.hero.dfn),
              'GOLD': int(w.hero.gold), 'keys_y': int(w.hero.keys['y']), 'keys_b': int(w.hero.keys['b'])},
    'sword_taken': (w.hero.atk == 20 and w.at(*GOAL) != 30),   # ATK 10→20 且格子已空 = 已拾取
    'per_floor_steps': dict(sorted(per.items())),
    'hp_drops': [[r[0], r[4], r[10][:60]] for r in drops][:14],
    'trap_fired': bool(w.trap_done),
    'caveats': sorted(w.caveats),
    'assumptions': ['obj2 吃黄钥匙(obj1)=DOOR_OF 推断 ⚠️', 'obj19/21/23 饰件可踩 ⚠️',
                    '剧本收尾后四角魔导师撤走、3F(5,9) 复原、2F(2,7) 挖通 ✅指令流',
                    '落点 2F(3,8) 取盗贼邻格 ⚠️（指令给的是空白演出块 (band5,slot0)）'],
}
json.dump(summary, open('route_sword_summary.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1)[:1700])
