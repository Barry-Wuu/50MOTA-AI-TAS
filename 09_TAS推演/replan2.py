# -*- coding: utf-8 -*-
"""合法重排 v2：2F 越狱 → 3F 蓝钥匙 → 回 2F 拿 +1000G → 4F 祭坛换 ATK → 5F~11F。

关键发现（本次重排的核心）：
  · 原录制路线从未进入 2F 右区，漏掉了两个奖励 NPC：
      (2,11,4) obj174「やあ、助けてくれてありがとう…」→ +1000 GOLD
      (2,11,7) obj152 → 攻防 +3%（ATK 低时收益为 0，故先不碰）
    右区唯一合法入口是 2F(3,1) 的蓝门，需要 3F(5,3) 的蓝钥匙。
  · 4F(6,1) 祭坛可把金币换成属性（hp/atk/dfn），代价 20/40/80/140/220/320…
    1000G 足够 6 次献祭 = ATK +60。ATK 10→70 后，6F 骷髅B(HP55/DEF12)
    只需 1 回合击杀（掉血 0），原本必交的 252 血「过路费」直接消失。
  · 于是 6F~9F 全部怪基本一击必杀，铁剑/铁盾照拿，10F BOSS 只掉 55 血，
    可顺利抵达 11F。

策略：按阶段走，段内用「带钥匙状态的 Dijkstra」寻路 + 贪心扫图。
"""
import sys, io, csv, heapq, collections

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
DED = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/'
sys.path.insert(0, TOOLS)
import mota_core as M

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIRCH = {(1, 0): '→', (-1, 0): '←', (0, 1): '↓', (0, -1): '↑', None: '·'}
FAIL = ('blocked', '打不动', '打不过', '无', '买不起', '熔岩烫死', '祭坛金币不足')

VAL = {30: 500, 35: 500,          # 铁剑 / 铁盾
       13: 90, 14: 90,            # 赤 / 青 水晶 +1
       11: 50, 12: 200,           # 赤 +50 / 青 +200
       1: 55, 3: 130, 28: 220}    # 黄 / 蓝 / 红 钥匙
ALTAR_VALUE = 350                 # 一次献祭（ATK+10）的估值
ATK_CAP = 80                      # 超过此值后不再献祭
KEYCOST = 24

# 不该踩的 NPC（3% 在 ATK 低时收益为 0，留到属性起来后再吃；本路线直接跳过）
AVOID_MSG = {152}

rows_rec = list(csv.DictReader(io.open(SRC + '魔塔1_route_1F到21F.csv', encoding='utf-8-sig')))

w = M.World.new()
out = []


def snap(h):
    return dict(hp=h.hp, atk=h.atk, dfn=h.dfn, gold=h.gold,
                ky=h.keys['y'], kb=h.keys['b'], kr=h.keys['r'])


def logstep(d, event, note=''):
    h = w.hero
    out.append(dict(floor=h.f, x=h.x, y=h.y, dir=d, event=event, note=note,
                    hp=h.hp, atk=h.atk, def_=h.dfn, gold=h.gold,
                    ky=h.keys['y'], kb=h.keys['b'], kr=h.keys['r']))


def move_dir(d, event=''):
    lg = w.move(*d)
    if lg and lg[0].startswith(FAIL):
        return lg
    logstep(d, event, ' ｜ '.join(lg) if lg else '')
    return None


# ---------------------------------------------------------------------------
# 1) 重放剧本段 1..42 + 60..67（1F 起手 → 3F 扒装 → 丢 2F 牢房 → 盗贼洞越狱）
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
    logstep(b[1], '剧本段', ' ｜ '.join(lg) if lg else '')

print('剧本段完成:', snap(w.hero), 'pos', w.hero.f, w.hero.x, w.hero.y)


# ---------------------------------------------------------------------------
# 2) 带钥匙状态的单层 Dijkstra
# ---------------------------------------------------------------------------
def transitions(f, x, y, ky, kb, kr, stair_goal=None, allow_altar=False):
    """从 (x,y,keys) 出发的 4 向邻居。返回 [(nx,ny,nky,nkb,nkr,cost)]。"""
    res = []
    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < 13 and 0 <= ny < 13):
            continue
        if stair_goal and (nx, ny) == stair_goal:
            res.append((nx, ny, ky, kb, kr, 0))
            continue
        t = w.terrain_at(f, nx, ny)
        if t == 1:
            if (f, nx, ny) in M.DARKWALL_CELLS and (f, nx, ny) not in w.cleared:
                res.append((nx, ny, ky, kb, kr, 0)); continue
            if M.DIG_WALLS.get((f, nx, ny)) in w.cleared:
                res.append((nx, ny, ky, kb, kr, 0)); continue
            continue
        if t == 2:
            continue                      # 楼梯单独处理
        o = w.at(f, nx, ny)
        if not o:
            res.append((nx, ny, ky, kb, kr, 0)); continue
        if o == 19 and (f, nx, ny) in M.GATE_2F:
            continue
        if o in M.ALTAR_SIDE:
            continue                      # 祭坛左右两格属于祭坛本体，不可踩
        ty = M.TYPE.get(M.oatr(o, 3), '?')
        if ty == 'MONSTER':
            r = w.battle(o)
            if r is None:
                continue
            loss, gold = r
            if loss >= w.hero.hp:
                continue
            res.append((nx, ny, ky, kb, kr, loss)); continue
        if ty == 'DOOR':
            col = M.DOOR_OF.get(o)
            if col is None:
                res.append((nx, ny, ky, kb, kr, 0)); continue
            k = {'y': ky, 'b': kb, 'r': kr}
            if k[col] <= 0:
                continue
            k[col] -= 1
            res.append((nx, ny, k['y'], k['b'], k['r'], KEYCOST)); continue
        if o in (1, 3, 28):
            k = {'y': ky, 'b': kb, 'r': kr}
            k[M.KEY_OF[o]] += 1
            res.append((nx, ny, k['y'], k['b'], k['r'], 0)); continue
        if o in M.SHOP:
            continue                      # 实体店，需单独"撞"
        if ty == 'SAIDAN':
            if allow_altar:
                res.append((nx, ny, ky, kb, kr, 0))
            continue
        if o in AVOID_MSG:
            continue
        res.append((nx, ny, ky, kb, kr, 0))     # ITEM/STATUS/MESSAGE/SCORE/NORMAL/DECOR
    return res


def dijkstra_floor(stair_goal=None, allow_altar=False):
    f = w.hero.f
    h = w.hero
    start = (h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'])
    dist = {start: 0}
    prev = {start: None}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, 1e9):
            continue
        ux, uy, ky, kb, kr = u
        for nx, ny, nky, nkb, nkr, c in transitions(f, ux, uy, ky, kb, kr,
                                                    stair_goal, allow_altar):
            v = (nx, ny, nky, nkb, nkr)
            nd = d + c
            if nd < dist.get(v, 1e9):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev


def best_state_at(dist, cell):
    best = None
    for st, d in dist.items():
        if (st[0], st[1]) == cell:
            if best is None or d < best[0]:
                best = (d, st)
    return best


def path_of(prev, st):
    p = []
    while st is not None:
        p.append((st[0], st[1]))
        st = prev[st]
    return p[::-1]


def walk_cells(cells, event=''):
    """按格序列走（不含起点），逐格 move。返回错误日志或 None。"""
    h = w.hero
    for (nx, ny) in cells:
        d = (nx - h.x, ny - h.y)
        if abs(d[0]) + abs(d[1]) != 1:
            return ['路径不连续']
        err = move_dir(d, event)
        if err:
            return err
        h = w.hero
    return None


def goto_cell(cell, allow_altar=False, event=''):
    dist, prev = dijkstra_floor(allow_altar=allow_altar)
    b = best_state_at(dist, cell)
    if b is None:
        return ['不可达 %s' % (cell,)]
    d, st = b
    if d >= w.hero.hp - 20:
        return ['血量不足（需 %d，有 %d）' % (d, w.hero.hp)]
    return walk_cells(path_of(prev, st)[1:], event)


def go_stair(up=True):
    f = w.hero.f
    stair = M.STAIRS[f][0 if up else 1]
    if stair is None:
        return ['本层无%s行梯' % ('上' if up else '下')]
    dist, prev = dijkstra_floor(stair_goal=stair)
    b = best_state_at(dist, stair)
    if b is None:
        return ['楼梯 %s 不可达' % (stair,)]
    d, st = b
    if d >= w.hero.hp - 10:
        return ['血量不足到楼梯（需 %d，有 %d）' % (d, w.hero.hp)]
    err = walk_cells(path_of(prev, st)[1:])
    return err


def goto_floor(tf):
    guard = 0
    while w.hero.f != tf and guard < 12:
        guard += 1
        up = tf > w.hero.f
        err = go_stair(up=up)
        if err:
            return err
    return None


# ---------------------------------------------------------------------------
# 3) 扫图：本层所有正收益目标，按 (价值 - 代价) 选最优
# ---------------------------------------------------------------------------
def altar_ready():
    h = w.hero
    if h.f != 4 or h.atk >= ATK_CAP:
        return False
    c = M.altar_cost(w.altar_k)
    return h.gold >= c


def target_value(o, cell):
    if o == 174:
        return 1600                     # +1000 GOLD
    if o in AVOID_MSG:
        return 0
    return VAL.get(o, 0)


def sweep(limit=60):
    n = 0
    while n < limit:
        n += 1
        dist, prev = dijkstra_floor(allow_altar=altar_ready())
        f = w.hero.f
        h = w.hero
        best = None
        for st, d in dist.items():
            x, y = st[0], st[1]
            if (x, y) == (h.x, h.y):
                continue
            o = w.at(f, x, y)
            v = 0
            if o:
                v = target_value(o, (f, x, y))
            if v <= 0:
                continue
            if d >= h.hp - 80:
                continue
            sc = v - d
            if sc <= 0:
                continue
            if best is None or sc > best[0]:
                best = (sc, (x, y), d, st)
        if best is None:
            return n - 1
        sc, cell, d, st = best
        err = walk_cells(path_of(prev, st)[1:], '扫图')
        if err:
            print('  扫图执行失败', cell, err)
            return n - 1
    return n


# ---------------------------------------------------------------------------
# 4) 祭坛：连续献祭 n 次（ATK+10/次）
# ---------------------------------------------------------------------------
ALTAR = (6, 1)


def sacrifice(n):
    f = w.hero.f
    assert f == 4, 'not on 4F'
    done = 0
    for _ in range(n):
        if not altar_ready():
            break
        # 确保站在祭坛旁
        if (w.hero.x, w.hero.y) != ALTAR:
            err = goto_cell(ALTAR, allow_altar=True, event='祭坛')
            if err:
                print('  祭坛不可达:', err); break
        else:
            # 先退开一格再进，才能再次触发
            back = None
            for dx, dy in DIRS:
                nx, ny = w.hero.x + dx, w.hero.y + dy
                if (nx, ny) == ALTAR:
                    continue
                c = w.clone()
                lg = c.move(dx, dy)
                if not (lg and lg[0].startswith(FAIL)):
                    back = (dx, dy); break
            if back is None:
                break
            err = move_dir(back, '退开祭坛')
            if err:
                break
            err = goto_cell(ALTAR, allow_altar=True, event='祭坛')
            if err:
                print('  祭坛回踩失败:', err); break
        done += 1
    return done


# ---------------------------------------------------------------------------
# 5) 阶段执行
# ---------------------------------------------------------------------------
print('\n--- 阶段 1：2F 越狱 → 3F 拿蓝钥匙 / 蓝药 ---')
print(goto_floor(3) or 'ok', snap(w.hero))
print('3F 扫图次数', sweep())

print('\n--- 阶段 2：回 2F，开蓝门拿 +1000G ---')
print(goto_floor(2) or 'ok', snap(w.hero))
# 直接以 NPC174 为目标（路径会自动消耗蓝钥匙开 (3,1) 蓝门）
err = goto_cell((11, 4), event='奖励NPC')
print('NPC174:', err or 'ok', snap(w.hero))
print('2F 扫图次数', sweep())

print('\n--- 阶段 3：上 4F，拿蓝钥匙 + 祭坛换 ATK ---')
print(goto_floor(4) or 'ok', snap(w.hero))
print('取 4F 蓝钥匙(2,1):', goto_cell((2, 1), event='蓝钥匙') or 'ok', snap(w.hero))
print('去祭坛:', goto_cell(ALTAR, allow_altar=True, event='祭坛') or 'ok', snap(w.hero))
used = sacrifice(6)
print('献祭次数', used, snap(w.hero))
print('4F 扫图次数', sweep())

print('\n--- 阶段 4：5F 铁剑 ---')
print(goto_floor(5) or 'ok', snap(w.hero))
print('铁剑(11,11):', goto_cell((11, 11), event='铁剑') or 'ok', snap(w.hero))
print('5F 扫图次数', sweep())

for tf in (6, 7, 8, 9):
    print('\n--- 阶段：%dF ---' % tf)
    e = goto_floor(tf)
    print('上行', e or 'ok', snap(w.hero))
    print('扫图次数', sweep())

print('\n--- 9F 铁盾 ---')
print('铁盾(9,7):', goto_cell((9, 7), event='铁盾') or 'ok', snap(w.hero))

print('\n--- 10F BOSS → 11F ---')
print(goto_floor(10) or 'ok', snap(w.hero))
print('BOSS(6,3):', goto_cell((6, 3), event='10F BOSS') or 'ok', snap(w.hero))
print('上行梯(6,11):', goto_cell((6, 11), event='BOSS后上行梯') or 'ok', snap(w.hero))

print('\n最终:', w.hero.f, w.hero.x, w.hero.y, snap(w.hero))

# ---------------------------------------------------------------------------
# 6) 输出 CSV
# ---------------------------------------------------------------------------
path_csv = DED + '魔塔1_route_1F到11F_合法重排.csv'
with io.open(path_csv, 'w', encoding='utf-8', newline='') as fh:
    wr = csv.writer(fh)
    wr.writerow(['step', 'floor', 'x', 'y', 'key', 'event', 'hp', 'atk', 'def', 'gold', 'ky', 'kb', 'kr'])
    for i, r in enumerate(out, 1):
        wr.writerow([i, r['floor'], r['x'], r['y'], '', (r['event'] + (('：' + r['note']) if r['note'] else '')), r['hp'], r['atk'],
                     r['def_'], r['gold'], r['ky'], r['kb'], r['kr']])
print('wrote', path_csv, len(out), 'rows')
