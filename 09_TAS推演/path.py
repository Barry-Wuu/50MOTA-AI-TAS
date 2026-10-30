# -*- coding: utf-8 -*-
"""层内低损+省钥匙 Dijkstra 自动寻路（机械式移动，不做全局路线搜索）。
目标点由调用方按人类攻略手工指定；本工具只负责"从当前格走到目标格"。
- 每步代价 = HP 损耗 + 100*钥匙消耗（优先省钥匙，再省血）
用法:
  python path.py                     # 加载到锚点，打印 st()
"""
import sys, math, heapq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import manual
manual.execute(verbose=False)        # 重放 1F→9F → 8F(6,2)

W = manual.W
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DNAME0 = {(1, 0): 'R', (-1, 0): 'L', (0, 1): 'D', (0, -1): 'U'}
STEPS = [0]
LOGE = []

def st():
    h = W.hero
    return 'HP%-5d A%-3d D%-3d G%-4d 钥%d/%d/%d %dF(%d,%d)' % (
        h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y)

def move_cost(cell, d):
    """返回 (hp_loss, key_used, ok)。解析式（引擎公式实测验证）。
    key_used: 1=黄钥, 2=蓝钥, 3=红钥, 0=无。"""
    nx, ny = cell[0] + d[0], cell[1] + d[1]
    if not (0 <= nx < 13 and 0 <= ny < 13):
        return 0, 0, False
    t = W.terrain_at(W.hero.f, nx, ny)
    if t == 1 or t == 2:
        return 0, 0, False
    o = W.at(W.hero.f, nx, ny)
    if o == 0:
        return 0, 0, True
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    h = W.hero
    if o in M.KEY_OF:
        return 0, 0, True
    if ty in ('STATUS', 'ITEM'):
        return 0, 0, True
    if o == 20:
        return 0, 0, True
    if o == 2 and h.keys['y'] > 0:
        return 0, 1, True
    if o == 4 and h.keys['b'] > 0:
        return 0, 2, True
    if o == 27 and h.keys['r'] > 0:
        return 0, 3, True
    if ty in ('NORMAL', 'SCORE', 'MESSAGE'):
        return 0, 0, False
    if ty == 'MONSTER':
        mhp, matk, mdef = M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12)
        myd = max(h.atk - mdef, 1)
        r = math.ceil(mhp / myd)
        loss = (r - 1) * max(matk - h.dfn, 1)
        if loss < h.hp:
            return loss, 0, True
        return 0, 0, False
    return 0, 0, False

def bfs_advance(f, start, goal):
    """层内 Dijkstra：代价 = hp_loss + 100*key_used，HP 感知（累计战损 < 当前 HP）。
    返回 dir 列表或 None。"""
    if start == goal:
        return []
    h = W.hero
    hp0 = h.hp
    dist = {start: 0}
    cum = {start: 0}
    prev = {}
    pq = [(0, 0, start)]
    while pq:
        cst, sp, c = heapq.heappop(pq)
        if cst != dist.get(c):
            continue
        if c == goal:
            break
        for d in DIRS:
            n = (c[0] + d[0], c[1] + d[1])
            if not (0 <= n[0] < 13 and 0 <= n[1] < 13):
                continue
            loss, kused, ok = move_cost(c, d)
            if not ok:
                continue
            new_cum = cum[c] + loss
            if new_cum >= hp0:               # 会死：拒绝（含刚好扣到0）
                continue
            nc = cst + loss + 100 * kused
            if n not in dist or nc < dist[n]:
                dist[n] = nc
                cum[n] = new_cum
                prev[n] = (c, d)
                heapq.heappush(pq, (nc, sp + 1, n))
    if goal not in dist:
        return None
    path = []
    cur = goal
    while cur != start:
        c, d = prev[cur]
        path.append(d)
        cur = c
    return list(reversed(path))

def goto(f, x, y, note=''):
    """层内走到 (x,y)，省钥匙+低损优先。门/怪按引擎实际执行。"""
    if W.hero.f != f:
        raise RuntimeError('goto 目标层 %d 但当前在 %dF' % (f, W.hero.f))
    start = (W.hero.x, W.hero.y)
    if start == (x, y):
        return True
    path = bfs_advance(f, start, (x, y))
    if path is None:
        print('!! 不可达 %dF(%d,%d)（当前 %s）' % (f, x, y, (W.hero.x, W.hero.y)))
        return False
    for d in path:
        before = (W.hero.x, W.hero.y)
        lg = W.move(*d)
        STEPS[0] += 1
        for e in (lg or []):
            if e.startswith(('拾取', '拾 ', 'NPC', '踩', '撞击', '撞塌', '隐形', '盗賊', '购物', '祭坛', '击杀')):
                LOGE.append('    · ' + e)
        if (W.hero.x, W.hero.y) == before and lg and lg[0].startswith('开'):
            lg2 = W.move(*d)
            STEPS[0] += 1
            for e in (lg2 or []):
                if e.startswith(('拾取', '拾 ', 'NPC', '踩', '撞击', '撞塌', '隐形', '盗賊', '购物', '祭坛', '击杀')):
                    LOGE.append('    · ' + e)
    if note:
        print('[%s] %s' % (note, st()))
    for e in LOGE:
        print(e)
    LOGE.clear()
    return True

def collect(f, targets, label='', hp_floor=120):
    """层内按代价（省钥+低损）顺序收集多个目标；HP 将低于 hp_floor 时停止。
    路径代价用累计战损（HP 感知），避免半路暴毙。"""
    got = []
    while targets:
        h = W.hero
        if h.hp < hp_floor:
            print('  !! HP%d < %d，停止收集' % (h.hp, hp_floor))
            break
        best = None
        for (tx, ty, nm) in targets:
            p = bfs_advance(f, (h.x, h.y), (tx, ty))
            if p is None:
                continue
            est_hp = 0; est_key = 0; okp = True
            cx, cy = h.x, h.y
            for d in p:
                loss, kused, ok = move_cost((cx, cy), d)
                if not ok:
                    okp = False; break
                est_hp += loss; est_key += kused
                cx += d[0]; cy += d[1]
            if not okp:
                continue
            cost = est_hp + 100 * est_key
            if best is None or cost < best[0]:
                best = (cost, est_hp, tx, ty, nm)
        if best is None:
            print('  !! 层 %d 无可达目标: %s' % (f, [t[2] for t in targets]))
            break
        cost, est_hp, tx, ty, nm = best
        if h.hp - est_hp < hp_floor:
            print('  !! 目标 %s 需 %d HP，HP%d 会跌破 %d，跳过' % (nm, est_hp, h.hp, hp_floor))
            targets.remove((tx, ty, nm))
            continue
        goto(f, tx, ty, nm)
        got.append(nm)
        targets.remove((tx, ty, nm))
    if label:
        print('[collect %s] %s' % (label, st()))
    return got

def stair(f, x, y, note=''):
    """走到 (f,x,y) 楼梯相邻格，踏上楼梯（换层）。"""
    manual.approach(f, x, y)
    o, lg = manual.enter(f, x, y, '楼梯')
    if note:
        print('[%s] %s' % (note, st()))
    return lg

if __name__ == '__main__':
    print('锚点: ' + st())
    if 'demo' in sys.argv:
        print('--- 测试 8F 红钥(10,2) ---')
        goto(8, 10, 2, '红钥(10,2)')
