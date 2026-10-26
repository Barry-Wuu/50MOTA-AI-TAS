#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""state.py —— 回放 route_plan.csv 精确复现世界状态，然后做可达性分析。

用法:
  python3 state.py                       # 回放到 CSV 末尾，打印终态
  python3 state.py --at 1100             # 回放到第 1100 步
  python3 state.py --reach 10             # 终态下对 10F 做 BFS（同 reach.py）
  python3 state.py --reach 10 --hp 500    # 假想血量再 BFS
  python3 state.py --cleared 10           # 列出 10F 已清 / 未清挡路物
"""
import sys
import csv
import collections

import mota_core as M
import plan as P

DIRS = [(0, -1, '8'), (1, 0, '6'), (0, 1, '2'), (-1, 0, '4')]


def replay(path='route_plan.csv', upto=None):
    w = M.World.new()
    rows = list(csv.reader(open(path, encoding='utf-8')))[1:]
    if upto:
        rows = [r for r in rows if int(r[0]) <= upto]
    for r in rows:
        k = r[4]
        dx, dy = {('8'): (0, -1), ('6'): (1, 0), ('2'): (0, 1), ('4'): (-1, 0)}.get(k, (0, 0))
        if dx == 0 and dy == 0:
            continue
        w.move(dx, dy)
    return w


def bfs(w, cap=400000):
    best = {}
    q = collections.deque([(w, 0)])
    seen = {P._key(w)}
    n = 0
    while q and n < cap:
        cur, d = q.popleft()
        n += 1
        for dx, dy, _lab in DIRS:
            t = cur.clone()
            lg = t.move(dx, dy)
            if M.blocked(lg) or t.hero.hp <= 0:
                continue
            k = P._key(t)
            if k in seen:
                continue
            seen.add(k)
            pos = (t.hero.f, t.hero.x, t.hero.y)
            if pos not in best or best[pos][0] < t.hero.hp:
                best[pos] = (t.hero.hp, d + 1)
            q.append((t, d + 1))
    return best, n


def show(w, f):
    best, n = bfs(w)
    same = {p: v for p, v in best.items() if p[0] == f}
    print('同层可达格 %d 个；跨层触达 %d 格；BFS 展开 %d 状态' % (len(same), len(best), n))
    for y in range(13):
        row = []
        for x in range(13):
            if (f, x, y) in same:
                row.append('%X:%-4d' % (x, same[(f, x, y)][0]))
        if row:
            print('  y=%-2d %s' % (y, ' '.join(row)))
    unreach = []
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if o and (f, x, y) not in same:
                unreach.append('(%d,%d) obj%d %s' % (x, y, o, M.oname(o)[:16]))
    if unreach:
        print('本层不可达物件 %d 项：' % len(unreach))
        for s in unreach:
            print('   ', s)
    warps = sorted({'→ %dF(%d,%d)' % (p[0], p[1], p[2]) for p in best if p[0] != f})
    if warps:
        print('可跨层到：' + '；'.join(warps))
    return best


def parse_goal(g):
    g = g.strip().lstrip('@')
    if '(' in g:
        head, rest = g.split('(', 1)
        xy = rest.rstrip(')').split(',')
        return (int(head), int(xy[0]), int(xy[1]))
    return int(g)


def apply_seq(w, goals):
    """按目标序列走，返回 (world, 失败信息或None)"""
    for g in goals:
        w2, path = P.walk(w, g, 800000)
        if w2 is None:
            return w, '目标 %s 失败：%s' % (g, path)
        w = w2
    return w, None


def main():
    a = sys.argv[1:]
    upto = None
    reachf = None
    clearedf = None
    hp = None
    seq = []
    it = iter(a)
    for t in it:
        if t == '--at':
            upto = int(next(it))
        elif t == '--reach':
            reachf = int(next(it))
        elif t == '--cleared':
            clearedf = int(next(it))
        elif t == '--hp':
            hp = int(next(it))
        elif t == '--seq':
            seq = [parse_goal(x) for x in next(it).split()]
        else:
            seq.append(parse_goal(t))
    w = replay(upto=upto)
    if seq:
        w, err = apply_seq(w, seq)
        if err:
            print('✗ ' + err)
            print('停在 ' + P.st(w.hero))
            return
        print('（走完 %d 个目标）' % len(seq))
    h = w.hero
    print('状态  %s' % P.st(h))
    print('已清挡路物 %d 个；已购物 %d 次' % (len(w.cleared), len(w.bought)))
    if hp is not None:
        w.hero.hp = hp
        print('（假想 HP 改为 %d）' % hp)
    if clearedf is not None:
        blk = P.blockers_of(clearedf)
        done = {(c[1], c[2]) for c in w.cleared if c[0] == clearedf}
        print('%dF 挡路物：已清 %s' % (clearedf, sorted(done)))
        print('%dF 未清：' % clearedf)
        for c in sorted(blk - done):
            o = M.obj_raw(clearedf, c[0], c[1])
            print('   (%d,%d) obj%d %s' % (c[0], c[1], o, M.oname(o)[:20]))
    if reachf is not None:
        show(w, reachf)


if __name__ == '__main__':
    main()
