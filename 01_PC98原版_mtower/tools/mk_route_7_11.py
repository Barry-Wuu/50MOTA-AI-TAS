"""搜索并复验「7F 入口 → 11F」速通路线（记录真实方向动作，复验即重放）。

起点态延续 route_enter_7f.csv：7F(11,10) ATK20/DEF10/GOLD44/蓝1/红0，但**必须携带来自 6F 的黄钥匙**
（(11,7) 黄门是口袋唯一出口）。对 起始HP 与 黄钥匙数 做扫描求可行阈值。

覆盖难点：
  购物(7F obj41 50G→5黄)、暗墙(9F obj89)、10F BOSS(obj16→(6,11)梯→11F)、
  8F 红钥(obj28 开 10F 红门 obj27)、9F 铁盾(obj35 DEF+10)、各层晶体/血瓶养成。
"""
import sys, csv, itertools, heapq, collections
import mota_core as M

TIE = itertools.count()

# 起始资源（来自 route_enter_7f.csv 的延续，黄钥匙从 6F 带入）
ATK0, DFN0, GOLD0, BLUE0, RED0 = 20, 10, 44, 1, 0

def start_world(hp, yellow):
    w = M.World.new(event_mode='on_entry', trap_mode='apply')
    h = w.hero
    h.f, h.x, h.y = 7, 11, 10
    h.hp, h.atk, h.dfn, h.gold = hp, ATK0, DFN0, GOLD0
    h.keys['y'], h.keys['b'], h.keys['r'] = yellow, BLUE0, RED0
    w.apply_floor_events(7)
    return w


def bfs(hp, yellow, cap=8000000):
    """按步数 BFS；状态键含 HP 分桶避免剪掉高血分支。返回 (route,acts,nexplored) 或 None/'cap'。"""
    st = start_world(hp, yellow)

    def state_key(w):
        h = w.hero
        return (h.f, h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'],
                h.hp // 25,
                frozenset(c for c in w.cleared if c in M.PICKUP_CELLS),
                frozenset(w.bought))

    seen = {state_key(st)}
    pq = collections.deque([st])
    st._par = None; st._act = None
    n = 0
    while pq:
        w = pq.popleft()
        n += 1
        if w.hero.f == 11:
            path, acts, cur = [], [], w
            while cur is not None:
                path.append(cur); acts.append(cur._act); cur = cur._par
            return list(reversed(path)), list(reversed(acts))[1:], n
        if n > cap:
            return ('cap', None, n)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            w2 = w.clone()
            log = w2.move(dx, dy)
            if M.blocked(log):
                continue
            k = state_key(w2)
            if k in seen:
                continue
            seen.add(k)
            w2._par = w; w2._act = (dx, dy)
            pq.append(w2)
    return None, None, n


def run():
    # 扫描：黄钥匙 1..6，起始 HP 从小到大
    YELLOWS = [1, 2, 3, 4, 5, 6]
    HPS = [34, 100, 200, 300, 400, 500, 600, 800, 1000, 1300, 1600, 2000]
    best = None
    for y in YELLOWS:
        for hp in HPS:
            r = bfs(hp, y)
            if isinstance(r, tuple) and r[0] == 'cap':
                print(f'黄{y} HP{hp}: 状态上限({r[2]})')
                continue
            if r[0] is not None:
                print(f'★ 可行：黄钥匙={y} 起始HP={hp}  步数={len(r[1])} 探索={r[2]}')
                best = (y, hp, r[0], r[1])
                break  # 该黄钥匙数下取最小 HP
        if best:
            break
    if not best:
        print('无可行解（所有 HP/黄钥匙组合均不可达 11F）')
        return None
    return best


if __name__ == '__main__':
    res = run()
    if not res:
        sys.exit(1)
    y, hp, route, actions = res
    print(f'\n采用：黄钥匙={y} 起始HP={hp}  路径步数={len(actions)}')
    print('终态:', 'HP', route[-1].hero.hp, 'ATK', route[-1].hero.atk, 'DEF', route[-1].hero.dfn,
          'GOLD', route[-1].hero.gold, '钥匙', dict(route[-1].hero.keys),
          '已购', sorted(route[-1].bought), 'boss10', route[-1].boss10,
          'caveats', sorted(route[-1].caveats))

    # —— 复验：从干净起点按方向重放 ——
    KEYMAP = {(0, -1): '8', (1, 0): '6', (0, 1): '2', (-1, 0): '4'}
    ver = start_world(hp, y)
    rows = []
    step = 0
    for d in actions:
        step += 1
        log = ver.move(*d)
        if M.blocked(log):
            print('!! 第', step, '步被拒:', log); break
        h = ver.hero
        rows.append([step, h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
                     h.keys['y'], h.keys['b'], h.keys['r'], ' | '.join(log)])
        if h.f == 11:
            break
    assert (ver.hero.f, ver.hero.x, ver.hero.y) == (11, 6, 10), \
        f'终点异常 {(ver.hero.f, ver.hero.x, ver.hero.y)}'
    print('复验通过：终点', (ver.hero.f, ver.hero.x, ver.hero.y), '步数', len(rows))

    with open('route_7f_to_11f.csv', 'w', newline='', encoding='utf8') as fh:
        wr = csv.writer(fh)
        wr.writerow(['step', 'floor', 'x', 'y', 'HP', 'ATK', 'DEF', 'GOLD', '黄钥', '蓝钥', '红钥', '事件'])
        wr.writerows(rows)

    keys = []
    ver2 = start_world(hp, y)
    for d in actions:
        log = ver2.move(*d)
        assert not M.blocked(log), f'复验失败 {d} {log}'
        keys.append(KEYMAP[d])
        if any('购物' in l for l in log):
            keys.append('E')
    with open('keys_7f_to_11f.txt', 'w', encoding='utf8') as fh:
        fh.write(''.join(keys))
    print('按键数', len(keys), '串:', ''.join(keys))
