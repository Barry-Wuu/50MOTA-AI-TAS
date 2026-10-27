#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reach.py —— 用引擎判定「从当前状态出发，某层哪些格子可达」。

用法: python3 reach.py 11 6 10                        # 从 11F(6,10) 新建默认状态
      python3 reach.py 12 10 11 --hp 72 --atk 26 --dfn 23 --gold 155
      python3 reach.py 12 10 11 --keys 1,0,0          # 指定钥匙
输出：可达格集合（附首次到达 HP）+ 该层不可达物件清单。
"""
import sys
import collections
import mota_core as M
import plan as P

DIRS = [(0, -1, '8'), (1, 0, '6'), (0, 1, '2'), (-1, 0, '4')]


def build(f, x, y, kw):
    h = M.Hero.initial()
    h.f, h.x, h.y = f, x, y
    for k in ('hp', 'atk', 'dfn', 'gold'):
        if k in kw:
            setattr(h, k, kw[k])
    if 'keys' in kw:
        ky, kb, kr = kw['keys']
        h.keys = {'y': ky, 'b': kb, 'r': kr}
    return M.World.new(hero=h)


def bfs(w, cap=300000):
    """返回 {(f,x,y): (hp, steps)} 首次到达记录。"""
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


def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    f, x, y = int(a[0]), int(a[1]), int(a[2])
    kw = {}
    it = iter(sys.argv[1:])
    for t in it:
        if t == '--hp':
            kw['hp'] = int(next(it))
        elif t == '--atk':
            kw['atk'] = int(next(it))
        elif t == '--dfn':
            kw['dfn'] = int(next(it))
        elif t == '--gold':
            kw['gold'] = int(next(it))
        elif t == '--keys':
            kw['keys'] = tuple(int(v) for v in next(it).split(','))
    h = M.Hero.initial()
    h.f, h.x, h.y = f, x, y
    for k in ('hp', 'atk', 'dfn', 'gold'):
        if k in kw:
            setattr(h, k, kw[k])
    if 'keys' in kw:
        ky, kb, kr = kw['keys']
        h.keys = {'y': ky, 'b': kb, 'r': kr}
    print('起点 %dF(%d,%d) HP%d ATK%d DEF%d G%d 钥%d/%d/%d' % (
        f, x, y, h.hp, h.atk, h.dfn, h.gold,
        h.keys['y'], h.keys['b'], h.keys['r']))

    best, n = bfs(M.World.new(hero=h))
    same = {p: v for p, v in best.items() if p[0] == f}
    print('同层可达格 %d 个；跨层触达 %d 格；BFS 展开 %d 状态' % (len(same), len(best), n))
    print('   ' + ' '.join('%3X' % x2 for x2 in range(13)))
    for y2 in range(13):
        row = []
        for x2 in range(13):
            if (f, x2, y2) in same:
                row.append('%3d' % same[(f, x2, y2)][0])
            else:
                row.append('  .')
        print('%2d %s' % (y2, ' '.join(row)))
    # 不可达物件
    unreach = []
    for y2 in range(13):
        for x2 in range(13):
            o = M.obj_raw(f, x2, y2)
            if o and (f, x2, y2) not in same:
                unreach.append('(%d,%d) obj%d %s' % (x2, y2, o, M.oname(o)[:14]))
    if unreach:
        print('本层不可达物件 %d 项：' % len(unreach))
        for s in unreach:
            print('   ', s)
    # 可达跨层楼梯（供确定去向）
    warps = []
    for p, v in best.items():
        if p[0] != f:
            warps.append('→ %dF(%d,%d) HP%d' % (p[0], p[1], p[2], v[0]))
    if warps:
        print('可跨层到：' + '；'.join(sorted(set(warps))))


if __name__ == '__main__':
    main()
