#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""region.py —— 楼层连通分量分析。

把 terrain==1 当墙、其余当地板，算「忽略门/怪」的连通分量（跨层用 WARP 连通）。
每个分量列出：格子数、里面的物件（门/怪/钥/药/晶石/商店/楼梯）。

用法: python3 region.py 15
      python3 region.py 11 12 13 14 15 16 17
"""
import sys
import collections
import mota_core as M

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def comps(floors):
    """返回 {代表格: [格子...]}，跨 floors 联合计算。"""
    allc = []
    for f in floors:
        for y in range(13):
            for x in range(13):
                if M.terrain(f, x, y) != 1:
                    allc.append((f, x, y))
    adj = collections.defaultdict(list)
    for c in allc:
        f, x, y = c
        for dx, dy in DIRS:
            n = (f, x + dx, y + dy)
            if n in set(allc):
                adj[c].append(n)
        w = M.WARP.get(c)
        if w and w in set(allc):
            adj[c].append(w)
    seen = set()
    out = []
    for c in allc:
        if c in seen:
            continue
        q = collections.deque([c])
        seen.add(c)
        grp = []
        while q:
            u = q.popleft()
            grp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        out.append(grp)
    return out


def cellinfo(c):
    f, x, y = c
    o = M.obj_raw(f, x, y)
    if not o:
        return ''
    ty = M.TYPE.get(M.oatr(o, 3))
    if o == 79:
        return '熔岩'
    if o in (21, 22, 23):
        return '祭坛(不可走)'
    tag = {'MONSTER': '怪', 'DOOR': '门', 'KEY': '钥', 'STATUS': '物',
           'SELL': '商', 'ITEM': '品'}.get(ty, ty or '')
    w = M.WARP.get(c)
    if w:
        tag += ' 梯→%dF(%d,%d)' % w
    return '%s %s' % (tag, M.oname(o)[:22])


def main():
    floors = [int(a) for a in sys.argv[1:]] or list(range(1, 22))
    cs = comps(floors)
    cs.sort(key=lambda g: (min(c[0] for c in g), -len(g)))
    print('=== %s 连通分量 %d 个（墙已排除；门/怪不阻断） ===' % ('/'.join(map(str, floors)), len(cs)))
    for i, g in enumerate(cs):
        byf = collections.defaultdict(list)
        for c in g:
            byf[c[0]].append(c)
        head = '、'.join('%dF×%d' % (f, len(v)) for f, v in sorted(byf.items()))
        print('\n[分量%d] %s  共%d格' % (i + 1, head, len(g)))
        # 只列「有内容」的格子
        items = [(c, cellinfo(c)) for c in g if cellinfo(c)]
        if not items:
            print('    （空格）')
            continue
        for c, s in sorted(items):
            print('    %dF(%2d,%2d)  %s' % (c[0], c[1], c[2], s))


if __name__ == '__main__':
    main()
