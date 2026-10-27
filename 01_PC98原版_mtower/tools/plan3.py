# -*- coding: utf-8 -*-
"""逐层规划 5F→11F。

设计要点：
- 层内状态 = (x, y, cleared∩本层, bought∩本层)。这些集合唯一决定 hp/atk/dfn/gold/钥匙
  （战斗/拾取都是确定性的），因此不需要把资源塞进状态键。
- 层内用 BFS 枚举全部可达局部状态；出口（上层楼梯 / 击杀BOSS）在出口处收集所有状态，
  再对资源向量 (hp, atk, dfn, gold, ky, kb, kr) 做 Pareto 折叠，得到跨层传递的入口集合。
- 跨层资源只增不减，所以 Pareto 折叠安全。
"""
import collections, itertools, sys
import mota_core as M

CNT = itertools.count(1)

# ---- 层定义：入口落点、出口判定 --------------------------------------------
# 5F 起点（已拿铁剑）与各层出口楼梯
LAYERS = {
    5: dict(start=(10, 11), exit_cells=[(1, 1)],        # (5,1,1)→(6,1,2)
            need=[]),
    6: dict(start=None, exit_cells=[(11, 11)],          # (6,11,11)→(7,11,10)
            need=[]),
    7: dict(start=None, exit_cells=[(1, 1)],           # (7,1,1)→(8,1,2)
            need=[]),
    8: dict(start=None, exit_cells=[(6, 1)],           # (8,6,1)→(9,6,2)
            need=[(10, 2)]),                           # 必须拿红钥
    9: dict(start=None, exit_cells=[(1, 11)],          # (9,1,11)→(10,1,10)
            need=[(9, 7)]),                            # 必须拿铁盾（走暗墙）
    10: dict(start=None, exit_cells=[(6, 11)],         # BOSS死后 (6,11)→(11,6,10)
             need=[(6, 3)]),                           # 必须击杀 BOSS obj16
}

DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def mk_world(f, x, y, hp, atk, dfn, gold, ky, kb, kr, cleared=(), bought=(), boss10=False, items=()):
    w = M.World.new(event_mode='on_entry', trap_mode='apply')
    h = w.hero
    h.f, h.x, h.y = f, x, y
    h.hp, h.atk, h.dfn, h.gold = hp, atk, dfn, gold
    h.keys['y'], h.keys['b'], h.keys['r'] = ky, kb, kr
    h.items = set(items)
    w.trap_done = True; w.flag3F = 1
    w.cleared = set(cleared); w.bought = set(bought); w.boss10 = boss10
    w.applied_events.clear(); w.apply_floor_events(f)
    return w


def res(w):
    h = w.hero
    return (h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'])


def pareto(items):
    """items: [(res_tuple, payload)] → 去掉被支配者。"""
    out = []
    for r, p in items:
        dominated = False
        for r2, _ in out:
            if all(a >= b for a, b in zip(r2, r)) and r2 != r:
                dominated = True; break
        if dominated:
            continue
        out = [(r2, p2) for (r2, p2) in out
               if not (all(a >= b for a, b in zip(r, r2)) and r != r2)]
        out.append((r, p))
    return out


def explore(f, worlds, need=(), cap=3000000, verbose=True):
    """在 f 层内 BFS 枚举可达状态，返回出口处的 Pareto 集合 [(res, world)]。"""
    exits = set(LAYERS[f]['exit_cells'])
    need = set(need)
    seen = set()
    q = collections.deque()
    for w in worlds:
        k = (w.hero.x, w.hero.y,
             frozenset(c for c in w.cleared if c[0] == f),
             frozenset(c for c in w.bought if c[0] == f),
             w.boss10)
        if k in seen:
            continue
        seen.add(k); q.append(w)
    n = 0
    found = []
    while q:
        w = q.popleft(); n += 1
        if n % 200000 == 0:
            print('   ...%d 状态' % n)
        if n > cap:
            print('   [%dF] 状态爆炸 cap=%d' % (f, cap)); break
        h = w.hero
        # 出口判定
        if (h.x, h.y) in exits:
            if all((f, m[0], m[1]) in w.cleared for m in need):
                found.append(w)
                continue          # 出口格不必再扩展
        for dx, dy in DIRS:
            w2 = w.clone()
            lg = w2.move(dx, dy)
            if M.blocked(lg):
                continue
            if w2.hero.hp <= 0:
                continue
            if w2.hero.f != f:
                # 跨层（可能是上楼梯）→ 交给上层处理，这里只保留上楼梯落到下一层的
                if w2.hero.f == f + 1:
                    k2 = (w2.hero.x, w2.hero.y,
                          frozenset(c for c in w2.cleared if c[0] == f),
                          frozenset(c for c in w2.bought if c[0] == f),
                          w2.boss10)
                    if k2 not in seen:
                        seen.add(k2); q.append(w2)
                continue
            k2 = (w2.hero.x, w2.hero.y,
                  frozenset(c for c in w2.cleared if c[0] == f),
                  frozenset(c for c in w2.bought if c[0] == f),
                  w2.boss10)
            if k2 in seen:
                continue
            seen.add(k2); q.append(w2)
    if verbose:
        print('   [%dF] 枚举 %d 状态，出口候选 %d' % (f, n, len(found)))
    return found
