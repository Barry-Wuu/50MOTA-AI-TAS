"""严谨 BFS 求解器：从 1F 起点按真实事件推「进入第 N 层」或「走到某格」的最少步数。

正确性保证：
  · event_mode='on_entry'：进层即写入 FLOOR_WRITES（与实机一致）
  · trap_mode='apply'：踩 3F 中央 (5,9) 必触发扒装剧本（HP1000→400、ATK/DEF→10、
    神装没收、丢到 2F(4,8)、2F(2,7) 被挖通）——这是不可避免的特殊事件
  · 状态键含 (层,坐标,黄/蓝/红钥匙,trap_done,已拾取掩码) → BFS 首达即严格最少数
  · 战斗失败（打不过/打不动）视为不可走，避免走进必死分支
"""
import collections, json, csv, sys
import mota_core as M

DIRS = ((0, -1, '8'), (0, 1, '2'), (-1, 0, '4'), (1, 0, '6'))  # (dx,dy,键)


def is_blocked(log):
    # move() 成功时返回 []（无事件），仅当返回失败文案才算被拒
    if not log:
        return False
    s = log[0]
    return any(k in s for k in ('blocked', '打不动', '不可通行', '无黄', '无蓝', '无红', '打不过'))


def key_of(w):
    return (w.hero.f, w.hero.x, w.hero.y,
            w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
            w.trap_done,
            frozenset(c for c in w.cleared if c in M.PICKUP_CELLS))


def bfs(goal_f=None, goal_cell=None, cap=3000000):
    """goal_f: 进入该层即停；goal_cell=(f,x,y): 走到该格即停。返回 (动作串, 终点世界, 展开状态数)。"""
    assert goal_f or goal_cell
    start = M.World.new(event_mode='on_entry', trap_mode='apply')

    def reached(w):
        return w.hero.f == goal_f if goal_f else (w.hero.f, w.hero.x, w.hero.y) == goal_cell

    if reached(start):
        return [], start, 0
    seen = {key_of(start)}
    q = collections.deque([(start, [])])
    n = 0
    while q:
        w, acts = q.popleft()
        n += 1
        if n > cap:
            return None, None, n
        for dx, dy, k in DIRS:
            w2 = w.clone()
            log = w2.move(dx, dy)
            if is_blocked(log):
                continue
            kk = key_of(w2)
            if kk in seen:
                continue
            seen.add(kk)
            nacts = acts + [k]
            if reached(w2):
                return nacts, w2, n
            q.append((w2, nacts))
    return None, None, n


def replay(keys):
    KS = {'8': (0, -1), '2': (0, 1), '4': (-1, 0), '6': (1, 0)}
    w = M.World.new(event_mode='on_entry', trap_mode='apply')
    rows = []
    for i, ch in enumerate(keys, 1):
        log = w.move(*KS[ch])
        if is_blocked(log):
            return None, f'第{i}步被拒：{log}'
        rows.append([i, w.hero.f, w.hero.x, w.hero.y, w.hero.hp, w.hero.atk, w.hero.dfn,
                     w.hero.gold, w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
                     ' | '.join(log)])
    return w, rows


def run(target, goal_f=None, goal_cell=None, tag=None):
    keys, w, n = bfs(goal_f=goal_f, goal_cell=goal_cell)
    assert keys is not None, f'{target} 搜索失败（状态上限 {n}）'
    wr, rows = replay(keys)
    assert wr is not None, rows
    assert (goal_f and wr.hero.f == goal_f) or (goal_cell and (wr.hero.f, wr.hero.x, wr.hero.y) == goal_cell), \
        f'{target} 复验终点不符：{wr.hero.f},{wr.hero.x},{wr.hero.y}'
    tag = tag or target
    with open(f'route_{tag}.csv', 'w', newline='', encoding='utf8') as fh:
        cw = csv.writer(fh)
        cw.writerow(['step', 'floor', 'x', 'y', 'HP', 'ATK', 'DEF', 'GOLD', '黄钥', '蓝钥', '红钥', '事件'])
        cw.writerows(rows)
    open(f'keys_{tag}.txt', 'w').write(''.join(keys))
    out = {'tag': tag, 'steps': len(keys), 'nodes': n,
           'final': [wr.hero.f, wr.hero.x, wr.hero.y], 'HP': int(wr.hero.hp),
           'ATK': int(wr.hero.atk), 'DEF': int(wr.hero.dfn), 'GOLD': int(wr.hero.gold),
           'keys_y': int(wr.hero.keys['y']), 'keys_b': int(wr.hero.keys['b']),
           'keys_r': int(wr.hero.keys['r']),
           'events': [r[11] for r in rows if any(k in r[11] for k in ('剧本', '掉血', '楼梯'))]}
    print(f'== {target} == 步数={len(keys)} 状态={n} 终点={out["final"]} HP/ATK/DEF={out["HP"]}/{out["ATK"]}/{out["DEF"]} 金={out["GOLD"]} 黄/蓝/红={out["keys_y"]}/{out["keys_b"]}/{out["keys_r"]}')
    print('  ', out['events'])
    return out


if __name__ == '__main__':
    jobs = [
        ('enter2', dict(goal_f=2), 'enter_2f'),
        ('enter3', dict(goal_f=3), 'enter_3f'),
        ('enter4', dict(goal_f=4), 'enter_4f'),
        ('enter5', dict(goal_f=5), 'enter_5f'),
        ('sword5', dict(goal_cell=(5, 11, 11)), 'sword_5f'),
    ]
    summary = {}
    for t, g, tag in jobs:
        summary[t] = run(t, **g, tag=tag)
    json.dump(summary, open('route_enter_any_summary.json', 'w'), ensure_ascii=False, indent=1)
    print('\n已写入 route_enter_any_summary.json 与各 route_*.csv / keys_*.txt')
