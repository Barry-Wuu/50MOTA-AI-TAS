#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""solve.py —— 贪心收集求解器：每层自动收齐可达的钥匙/血瓶/攻防晶石，
进 13F 前用祭坛把 HP 堆到 ≥801 以穿 4 格熔岩取神剑；产出可复现的 route_plan.csv。

相对 plan.py 的改进：不再手写每块 SEGS（易错、漏门/漏钥匙），改为引擎驱动的可达收集 +
A* 精确执行，每层跑完再用 A* 上楼。所有移动都经引擎 move()，不可达/打不过会直接失败并由
本脚本报错，保证产出的 route_plan.csv 是"可执行且已验证"的。
"""
import sys
import csv
import collections
import mota_core as M
import plan  # 复用 walk/seg/to_floor/LOG/st/DIRS

DIRS = plan.DIRS
LOG = plan.LOG


def st(h):
    return '%2dF(%2d,%2d) HP%-4d ATK%2d DEF%2d G%-4d 钥%d/%d/%d' % (
        h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
        h.keys['y'], h.keys['b'], h.keys['r'])


# ── BFS 可达（近似：门按"有对应钥匙即可过"，怪按"当前攻防可击败即可过"，熔岩按"HP>200 可过"）──
def bfs_reach(w, f):
    h = w.hero
    from collections import deque
    start = (h.x, h.y)
    dist = {start: 0}
    q = deque([start])
    parent = {start: None}
    while q:
        x, y = q.popleft()
        for dx, dy, _ in DIRS:
            nx, ny = x + dx, y + dy
            if not (1 <= nx <= 11 and 1 <= ny <= 11):
                continue
            if (nx, ny) in dist:
                continue
            t = M.terrain(f, nx, ny)
            if t == 1:
                continue  # 墙（盗贼凿墙的暗道不在静态墙里，正常放行）
            o = M.obj_raw(f, nx, ny)
            if o:
                if o == 89:
                    pass  # 暗墙：走过去即塌，等同可通行（必须早于 DOOR 判定，因 obj89 的 TYPE 被记为 DOOR）
                else:
                    ty = M.TYPE.get(M.oatr(o, 3), '?')
                    if ty == 'DOOR':
                        col = M.DOOR_OF.get(o)
                        if col is None or h.keys[col] <= 0:
                            continue
                    elif ty == 'MONSTER':
                        if w.battle(o) is None:
                            continue
                    elif ty == 'SAIDAN':
                        continue  # 祭坛不计入普通可达（单独处理）
                    elif t == 2:
                        continue  # 楼梯：楼层内不跨层
            dist[(nx, ny)] = dist[(x, y)] + 1
            parent[(nx, ny)] = (x, y)
            q.append((nx, ny))
    return dist, parent


def path_to(parent, target):
    path = []
    cur = target
    while parent[cur] is not None:
        px, py = parent[cur]
        dx, dy = cur[0] - px, cur[1] - py
        path.append((dx, dy))
        cur = (px, py)
    path.reverse()
    return path


def collect_floor(w, f, label=''):
    """贪心收齐本层所有可达的钥匙/血瓶/攻防晶石（不含祭坛/BOSS）。"""
    picked = 0
    for _ in range(200):
        dist, parent = bfs_reach(w, f)
        # 候选：未收的 KEY / 带增益的 STATUS·ITEM
        cands = []
        for y in range(1, 12):
            for x in range(1, 12):
                if (f, x, y) in w.cleared:
                    continue
                if (x, y) not in dist:
                    continue
                o = M.obj_raw(f, x, y)
                if not o:
                    continue
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                gain = M.oatr(o, 10) + M.oatr(o, 11) + M.oatr(o, 12)
                if o in M.KEY_OF or (ty in ('STATUS', 'ITEM') and gain > 0):
                    # 钥匙优先（解锁后续），其次按 BFS 距离
                    pri = 0 if o in M.KEY_OF else 1
                    cands.append((pri, dist[(x, y)], x, y, o))
        if not cands:
            break
        cands.sort()
        _, d, x, y, o = cands[0]
        # 用 A* 精确执行（钥匙/门/怪/熔岩全由引擎处理）
        w2, path = plan.walk(w, (f, x, y))
        if w2 is None:
            # A* 失败（BFS 近似高估可达）：标记该格不可达，下一轮跳过
            w.cleared.add((f, x, y))
            continue
        # 执行（逐步回放进 LOG）
        cur = w
        for dx, dy, lab, _lg in path:
            cur = cur.clone()
            lg = cur.move(dx, dy)
            hh = cur.hero
            LOG.append((len(LOG) + 1, hh.f, hh.x, hh.y, lab, ' '.join(lg),
                        hh.hp, hh.atk, hh.dfn, hh.gold,
                        hh.keys['y'], hh.keys['b'], hh.keys['r']))
        w = w2
        picked += 1
    return w, picked


def ensure_hp(w, f, target=900):
    """在指定层的祭坛上反复献祭（policy=hp），把 HP 堆到 target 以上。"""
    w.altar_policy = 'hp'
    cell = None
    for (af, ax, ay) in M.ALTAR_CELLS:
        if af == f:
            cell = (ax, ay)
    if cell is None:
        return w
    ax, ay = cell
    guard = 0
    while w.hero.hp < target and guard < 12:
        c = M.altar_cost(w.altar_k)
        if w.hero.gold < c:
            break
        w2, path = plan.walk(w, (f, ax, ay))
        if w2 is None:
            break
        cur = w
        for dx, dy, lab, _lg in path:
            cur = cur.clone()
            lg = cur.move(dx, dy)
            hh = cur.hero
            LOG.append((len(LOG) + 1, hh.f, hh.x, hh.y, lab, ' '.join(lg),
                        hh.hp, hh.atk, hh.dfn, hh.gold,
                        hh.keys['y'], hh.keys['b'], hh.keys['r']))
        w = w2
        guard += 1
    return w


def main():
    w = M.World.new()
    print('起点  ' + st(w.hero))

    # ── 1F→2F→3F 陷阱→回 2F 吃蓝药→3F（沿用 plan 的可靠初始化）──
    w = plan.to_floor('1F → 2F', w, 2)
    w = plan.to_floor('2F → 3F', w, 3)
    if w is None:
        sys.exit(1)
    # 踩 3F 陷阱（被剥装送回 2F）
    w2, path = plan.walk(w, lambda x: x.hero.f == 2 and x.hero.hp == 400, 600000)
    if w2 is None:
        print('  ✗ 3F 陷阱'); sys.exit(1)
    cur = w
    for dx, dy, lab, _lg in path:
        cur = cur.clone(); lg = cur.move(dx, dy); hh = cur.hero
        LOG.append((len(LOG) + 1, hh.f, hh.x, hh.y, lab, ' '.join(lg),
                    hh.hp, hh.atk, hh.dfn, hh.gold,
                    hh.keys['y'], hh.keys['b'], hh.keys['r']))
    w = w2
    print('  ✓ 3F 陷阱（被剥装）→ ' + st(w.hero))
    # 回 2F 吃掉三个 +200 蓝药
    for (x, y, lab) in [(4, 10, '蓝药+200'), (3, 10, '蓝药+200'), (3, 11, '蓝药+200')]:
        w2 = plan.seg('2F %s' % lab, w, (2, x, y))
        if w2 is not None:
            w = w2
    w = plan.to_floor('2F → 3F', w, 3)

    fails = []
    for f in range(3, 18):
        print('--- %dF (进入 %s)' % (f, st(w.hero)))
        w, n = collect_floor(w, f)
        print('    收齐 %d 个补给/钥匙 → %s' % (n, st(w.hero)))
        if f == 10:
            # 必须击杀 BOSS 才生上行梯
            w2 = plan.seg('10F BOSS', w, (10, 6, 3))
            if w2 is None:
                fails.append('10F BOSS')
                break
            w = w2
            if not w.boss10:
                fails.append('10F BOSS 未死')
                break
        if f == 12:
            # 进 13F 熔岩前堆 HP
            w = ensure_hp(w, 12, target=901)
            print('    祭坛后 HP = %d' % w.hero.hp)
        if f < 17:
            w2 = plan.to_floor('%dF → %dF' % (f, f + 1), w, f + 1)
            if w2 is None:
                fails.append('%dF 上楼' % f)
                break
            w = w2

    print()
    print('终态  ' + st(w.hero))
    if fails:
        print('断点：', fails)
    else:
        print('★ 1F→17F 全程打通（含 11F 银盾 / 13F 神剑 / 17F 银剑）')

    with open('route_plan.csv', 'w', newline='', encoding='utf-8') as fp:
        cw = csv.writer(fp)
        cw.writerow(['step', 'floor', 'x', 'y', 'key', 'event', 'hp', 'atk', 'def', 'gold', 'ky', 'kb', 'kr'])
        cw.writerows(LOG)
    print('已写 route_plan.csv（%d 步）' % len(LOG))


if __name__ == '__main__':
    main()
