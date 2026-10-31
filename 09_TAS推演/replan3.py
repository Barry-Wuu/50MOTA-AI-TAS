# -*- coding: utf-8 -*-
"""合法重排 v3（修正：2F 奖励 NPC 在铁栅栏内，本段不可达）。

已确认事实（引擎 BFS + 用户实测）：
  · 从牢房 (4,8) 出发，可达区域只有 x1/x2 外侧走廊、y1 顶廊、以及中段 x6~x8
    的門番Ｂ房间；右区 x10/x11（两个奖励 NPC）被 x9 的 3 扇栅栏门 obj19 封死。
  · 因此 +1000G / +3% 在本段完全不可得，不能作为重排资源。

可用的合法资源：
  · 1F 还有大量原路线没捡的补给（红药 ×4、蓝药 +200、赤/青水晶），
    且 1F 在 2F 下方，出狱后可以走 2F(1,1) 下梯回到 1F 拿完再上来。
  · 4F 祭坛可把金币换成 ATK，但本段金币很少（到 4F 约 7G），只在顺路够钱时用。

策略：出狱 → 下 1F 扫图 → 逐层上行扫图 → 5F 铁剑 / 9F 铁盾 → 10F BOSS → 11F。
"""
import sys, io, csv, heapq

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
DED = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/'
sys.path.insert(0, TOOLS)
import mota_core as M

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIRCH = {(1, 0): '→', (-1, 0): '←', (0, 1): '↓', (0, -1): '↑', None: '·'}
FAIL = ('blocked', '打不动', '打不过', '无', '买不起', '熔岩烫死', '祭坛金币不足')

VAL = {30: 500, 35: 500,          # 铁剑 / 铁盾
       13: 120, 14: 120,          # 赤 / 青 水晶 +1
       11: 50, 12: 200,           # 赤 +50 / 青 +200
       1: 60, 3: 140, 28: 240}    # 黄 / 蓝 / 红 钥匙
ATK_CAP = 80
KEYCOST = 24

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
# 剧本段重放（1F 起手 → 3F 扒装 → 2F 牢房 → 盗贼洞越狱）
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
        print('剧本段重放失败 @row', i + 1)
        sys.exit(1)
    lg = w.move(*b[1])
    logstep(b[1], '剧本段', ' ｜ '.join(lg) if lg else '')

print('剧本段完成:', snap(w.hero), 'pos', w.hero.f, w.hero.x, w.hero.y)


# ---------------------------------------------------------------------------
# 单层 Dijkstra（带钥匙状态）
# ---------------------------------------------------------------------------
def transitions(f, x, y, ky, kb, kr, stair_goal=None, allow_altar=False):
    res = []
    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < 13 and 0 <= ny < 13):
            continue
        if stair_goal and (nx, ny) == stair_goal:
            res.append((nx, ny, ky, kb, kr, 0)); continue
        t = w.terrain_at(f, nx, ny)
        if t == 1:
            if (f, nx, ny) in M.DARKWALL_CELLS and (f, nx, ny) not in w.cleared:
                res.append((nx, ny, ky, kb, kr, 0)); continue
            if M.DIG_WALLS.get((f, nx, ny)) in w.cleared:
                res.append((nx, ny, ky, kb, kr, 0)); continue
            continue
        if t == 2:
            continue
        o = w.at(f, nx, ny)
        if not o:
            res.append((nx, ny, ky, kb, kr, 0)); continue
        if o == 19 and (f, nx, ny) in M.GATE_2F:
            continue
        if o in M.ALTAR_SIDE:
            continue
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
            continue
        if ty == 'SAIDAN':
            if allow_altar:
                res.append((nx, ny, ky, kb, kr, 0))
            continue
        res.append((nx, ny, ky, kb, kr, 0))
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
        err = go_stair(up=(tf > w.hero.f))
        if err:
            return err
    return None


# ---------------------------------------------------------------------------
# 扫图
# ---------------------------------------------------------------------------
ALTAR = (6, 1)


def altar_ready():
    h = w.hero
    return h.f == 4 and h.atk < ATK_CAP and h.gold >= M.altar_cost(w.altar_k)


def target_value(o):
    return VAL.get(o, 0)


def sweep(limit=60, quiet=False):
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
            if not o:
                continue
            v = target_value(o)
            if o == 22 and (f, x, y) in M.ALTAR_CELLS:
                v = 400 if altar_ready() else 0
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
            if not quiet:
                print('  扫图执行失败', cell, err)
            return n - 1
    return n


def sacrifice_loop():
    done = 0
    while altar_ready():
        if (w.hero.x, w.hero.y) != ALTAR:
            err = goto_cell(ALTAR, allow_altar=True, event='祭坛')
            if err:
                break
        else:
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
                break
        done += 1
    return done


# ---------------------------------------------------------------------------
# 阶段执行
# ---------------------------------------------------------------------------
print('\n--- 下到 1F，补捡原路线漏掉的补给 ---')
print('2F→1F:', goto_floor(1) or 'ok', snap(w.hero))
print('1F 扫图', sweep())
print('1F→2F:', goto_floor(2) or 'ok', snap(w.hero))
print('2F 扫图', sweep())

for tf in range(3, 12):
    print('\n--- %dF ---' % tf)
    e = goto_floor(tf)
    if e:
        print('上行失败:', e, snap(w.hero))
        break
    print('到达', snap(w.hero))
    print('扫图', sweep())
    if tf == 4:
        print('祭坛献祭', sacrifice_loop(), snap(w.hero))
        print('4F 扫图', sweep())
    if tf == 5:
        print('铁剑(11,11):', goto_cell((11, 11), event='铁剑') or 'ok', snap(w.hero))
        print('5F 扫图', sweep())
    if tf == 9:
        print('铁盾(9,7):', goto_cell((9, 7), event='铁盾') or 'ok', snap(w.hero))
        print('9F 扫图', sweep())
    if tf == 10:
        print('10F BOSS(6,3):', goto_cell((6, 3), event='10F BOSS') or 'ok', snap(w.hero))
        print('上行梯(6,11):', goto_cell((6, 11), event='BOSS后上行梯') or 'ok', snap(w.hero))
        break

print('\n最终:', w.hero.f, w.hero.x, w.hero.y, snap(w.hero))

# ---------------------------------------------------------------------------
# 输出 CSV
# ---------------------------------------------------------------------------
path_csv = DED + '魔塔1_route_1F到11F_合法重排.csv'
with io.open(path_csv, 'w', encoding='utf-8', newline='') as fh:
    wr = csv.writer(fh)
    wr.writerow(['step', 'floor', 'x', 'y', 'key', 'event', 'hp', 'atk', 'def', 'gold', 'ky', 'kb', 'kr'])
    for i, r in enumerate(out, 1):
        wr.writerow([i, r['floor'], r['x'], r['y'], '', (r['event'] + (('：' + r['note']) if r['note'] else '')),
                     r['hp'], r['atk'], r['def_'], r['gold'], r['ky'], r['kb'], r['kr']])
print('wrote', path_csv, len(out), 'rows')
