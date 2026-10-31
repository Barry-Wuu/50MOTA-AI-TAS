# -*- coding: utf-8 -*-
"""合法重排：从 2F 越狱点出发，用 mota_core 逐步实算，贪心扫图到 11F。

约束（来自仓库笔记 + 人类攻略）：
  · 2F 六个 obj19 栅栏门在两只門番Ｂ清空前不可通行 —— 1F-11F 段门后 3 蓝药 + 3 钥匙拿不到；
  · 合法出狱只能走盗贼凿开的洞 2F(2,7)；
  · 门后补给缺失的 600HP 只能靠 1F-10F 已存在但原路线跳过的补给补回来。

策略（人类攻略一区域的做法）：先拿 5F 铁剑、9F 铁盾，宝石/药水尽量拿，
高血怪（僧侣、骷髅B、骷髅C）能不打就不打，钥匙只开必经门。
"""
import sys, io, csv, heapq, collections

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
DED = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/'
sys.path.insert(0, TOOLS)
import mota_core as M

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIRCH = {(1, 0): '→', (-1, 0): '←', (0, 1): '↓', (0, -1): '↑', None: '·'}
FAIL = ('blocked', '打不动', '打不过', '无', '买不起', '熔岩烫死')

# 目标价值（HP 收益 / 属性 / 钥匙折算）
VAL = {30: 340, 35: 340,          # 铁剑 +10ATK / 铁盾 +10DEF
       13: 60, 14: 60,            # 赤/青水晶 +1ATK/DEF
       11: 50, 12: 200,           # 赤 +50 / 青 +200
       1: 24, 3: 50, 28: 80,      # 黄/蓝/红钥匙
       16: 400}                   # 10F BOSS 必须打
KEYCOST = 24                       # 一把钥匙的机会成本

rows_rec = list(csv.DictReader(io.open(SRC + '魔塔1_route_1F到21F.csv', encoding='utf-8-sig')))


def snap(h):
    return dict(hp=h.hp, atk=h.atk, dfn=h.dfn, gold=h.gold,
                ky=h.keys['y'], kb=h.keys['b'], kr=h.keys['r'])


w = M.World.new()
out = []          # 输出行（合法段）


def logstep(event, note=''):
    h = w.hero
    out.append(dict(floor=h.f, x=h.x, y=h.y, event=event, hp=h.hp, atk=h.atk,
                    def_=h.dfn, gold=h.gold, ky=h.keys['y'], kb=h.keys['b'], kr=h.keys['r']))


def try_move(d):
    lg = w.move(*d)
    return lg


def walk_to(path):
    """path: 目标格序列（不含起点）；逐格 move。"""
    for (nx, ny) in path:
        h = w.hero
        d = (nx - h.x, ny - h.y)
        lg = w.move(*d)
        if lg and lg[0].startswith(FAIL):
            return lg
        logstep(' ｜ '.join(lg) if lg else '')
    return None


# ---------------------------------------------------------------------------
# 1) 重放剧本段 1..42（1F 起手 → 3F 扒装丢牢房）
# ---------------------------------------------------------------------------
def pick_move(r):
    tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
    rec = dict(atk=int(r['atk']), dfn=int(r['def']), gold=int(r['gold']),
               ky=int(r['ky']), kb=int(r['kb']), kr=int(r['kr']))
    h = w.hero
    same = (h.f, h.x, h.y) == (tf, tx, ty)
    best = None
    for d in DIRS:
        c = w.clone()
        lg = c.move(*d)
        if lg and lg[0].startswith(FAIL):
            continue
        hh = c.hero
        sc = 0
        if (hh.f, hh.x, hh.y) == (tf, tx, ty):
            sc += 8
        elif same and (hh.f, hh.x, hh.y) == (h.f, h.x, h.y) and lg:
            sc += 4
        else:
            continue
        for k, cur in (('atk', hh.atk), ('dfn', hh.dfn), ('gold', hh.gold)):
            if cur == rec[k]:
                sc += 1
        for k, kk in (('ky', 'y'), ('kb', 'b'), ('kr', 'r')):
            if hh.keys.get(kk, 0) == rec[k]:
                sc += 1
        if bool(lg) == bool((r['event'] or '').strip()):
            sc += 1
        if best is None or sc > best[0]:
            best = (sc, d, c, lg)
    return best


for i in list(range(0, 42)) + list(range(60, 67)):
    r = rows_rec[i]
    b = pick_move(r)
    if b is None:
        print('剧本段重放失败 @row', i + 1, r['floor'], r['x'], r['y'])
        sys.exit(1)
    lg = w.move(*b[1])
    logstep(' ｜ '.join(lg) if lg else '', 'rec')

print('剧本段重放完成:', snap(w.hero), 'pos', w.hero.f, w.hero.x, w.hero.y)


# ---------------------------------------------------------------------------
# 2) 贪心规划
# ---------------------------------------------------------------------------
def cell_cost(f, x, y):
    """进入该格的代价（HP 损失 + 钥匙折算）；None = 不可通行。"""
    t = w.terrain_at(f, x, y)
    if t == 2:
        return None                      # 楼梯只在指定目标时踏入
    if t == 1:
        if (f, x, y) in M.DARKWALL_CELLS:
            return 0
        if M.DIG_WALLS.get((f, x, y)) in w.cleared:
            return 0
        return None
    o = w.at(f, x, y)
    if not o:
        return 0
    if o == 19 and (f, x, y) in M.GATE_2F:
        return None
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if ty == 'MONSTER':
        r = w.battle(o)
        if r is None:
            return None
        if r[0] >= w.hero.hp:
            return None
        return r[0]
    if ty == 'DOOR':
        col = M.DOOR_OF.get(o)
        if col is None:
            return 0
        return KEYCOST if w.hero.keys[col] > 0 else None
    if ty == 'BUY':
        return 0 if w.hero.gold >= M.SHOP_PRICE.get(o, 9999) else None
    return 0


def dijkstra(goal=None):
    f = w.hero.f
    start = (w.hero.x, w.hero.y)
    dist = {start: 0}
    prev = {start: None}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, 1e9):
            continue
        for dx, dy in DIRS:
            v = (u[0] + dx, u[1] + dy)
            if not (0 <= v[0] < 13 and 0 <= v[1] < 13):
                continue
            if v == goal:
                c = 0
            else:
                c = cell_cost(f, v[0], v[1])
                if c is None:
                    continue
            nd = d + c
            if nd < dist.get(v, 1e9):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev


def path_to(prev, cell):
    p = []
    c = cell
    while prev.get(c) is not None:
        p.append(c)
        c = prev[c]
    return p[::-1]


def target_value(o):
    return VAL.get(o, 0)


def plan_floor():
    """在当前层收集所有正收益目标，返回是否还有动作。"""
    h = w.hero
    f = h.f
    dist, prev = dijkstra()
    best = None
    for (x, y), d in dist.items():
        o = w.at(f, x, y)
        if not o:
            continue
        ty = M.TYPE.get(M.oatr(o, 3), '?')
        if not (ty in ('ITEM', 'STATUS') or o in (1, 3, 28, 30, 35, 16)):
            continue
        v = target_value(o)
        if v <= 0:
            continue
        if (f, x, y) == (h.x, h.y):
            continue
        if d >= h.hp - 50:               # 留 50 HP 安全余量
            continue
        sc = v - d
        if sc <= 0:
            continue
        if best is None or sc > best[0]:
            best = (sc, (x, y), d)
    if best is None:
        return False
    _, cell, d = best
    err = walk_to(path_to(prev, cell))
    if err:
        print('  执行失败', cell, err)
        return False
    return True


def go_up():
    h = w.hero
    f = h.f
    up = M.STAIRS[f][0]
    if up is None:
        return False
    dist, prev = dijkstra(goal=up)
    if up not in dist:
        return False
    p = path_to(prev, up)
    if dist[up] >= h.hp - 10:
        return False
    err = walk_to(p)
    return err is None


# 起始在 2F 牢房；先出牢房（剧本段已到 (1,10)），再按层扫
floor_target = 11
guard = 0
while w.hero.f < floor_target and guard < 60:
    guard += 1
    f0 = w.hero.f
    n = 0
    while plan_floor():
        n += 1
        if n > 40:
            break
    if w.hero.f != f0:
        continue
    if not go_up():
        print('卡住：%dF 无法上行' % f0, snap(w.hero), 'pos', w.hero.x, w.hero.y)
        break
    print('上行 → %dF  %s' % (w.hero.f, snap(w.hero)))

print('最终:', w.hero.f, w.hero.x, w.hero.y, snap(w.hero))

# ---------------------------------------------------------------------------
# 3) 输出 CSV
# ---------------------------------------------------------------------------
path_csv = DED + '魔塔1_route_1F到11F_合法重排.csv'
with io.open(path_csv, 'w', encoding='utf-8', newline='') as fh:
    wr = csv.writer(fh)
    wr.writerow(['step', 'floor', 'x', 'y', 'key', 'event', 'hp', 'atk', 'def', 'gold', 'ky', 'kb', 'kr'])
    for i, r in enumerate(out, 1):
        wr.writerow([i, r['floor'], r['x'], r['y'], '', r['event'], r['hp'], r['atk'],
                     r['def_'], r['gold'], r['ky'], r['kb'], r['kr']])
print('wrote', path_csv, len(out), 'rows')
