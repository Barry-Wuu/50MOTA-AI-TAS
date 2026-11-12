# -*- coding: utf-8 -*-
"""执行 PLAN 后，列出每层自由格连通域 + 边界关口（不做任何决策）"""
import manual as U
import mota_core as M
from collections import deque

U.execute(verbose=False)
W = U.W
h = W.hero
print('当前: HP%d A%d D%d G%d 钥%d/%d/%d %dF(%d,%d)' % (
    h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y))

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def info(o):
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if ty == 'MONSTER':
        return '%s(%d/%d/%d)g%d' % (M.oname(o), M.oatr(o, 10), M.oatr(o, 11),
                                    M.oatr(o, 12), M.oatr(o, 13))
    return '%s obj%d' % (M.oname(o)[:12], o)


for f in range(1, 11):
    comps = []
    seen = set()
    for y in range(13):
        for x in range(13):
            if (x, y) in seen or not U.free(f, x, y):
                continue
            comp = set()
            q = deque([(x, y)])
            seen.add((x, y))
            while q:
                c = q.popleft()
                comp.add(c)
                for d in DIRS:
                    n = (c[0] + d[0], c[1] + d[1])
                    if n in seen or not U.free(f, n[0], n[1]):
                        continue
                    seen.add(n)
                    q.append(n)
            comps.append(comp)
    print('\n=== %dF：%d 个连通域 ===' % (f, len(comps)))
    for comp in sorted(comps, key=len, reverse=True):
        up, dn = M.STAIRS.get(f, (None, None))
        tags = []
        for nm, sc in (('上梯', up), ('下梯', dn), ('飞落', M.FLY_LAND.get(f))):
            if sc and sc in comp:
                tags.append(nm + '%s' % (sc,))
        if (h.f == f) and (h.x, h.y) in comp:
            tags.append('★当前')
        print('  域 %2d 格 %s' % (len(comp), ' '.join(tags)))
        front = []
        for (x, y) in comp:
            for d in DIRS:
                n = (x + d[0], y + d[1])
                if not (0 <= n[0] < 13 and 0 <= n[1] < 13):
                    continue
                if n in comp or not U.free(f, n[0], n[1]):
                    o = W.at(f, n[0], n[1])
                    if o and (o, n) not in front:
                        front.append((o, n))
        for o, c in front:
            print('     口 (%2d,%2d) %s' % (c[0], c[1], info(o)))
