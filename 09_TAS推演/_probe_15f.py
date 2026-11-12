# -*- coding: utf-8 -*-
"""探测：重放到 16F(6,10) 后，测试 15F 内若干关键格的可达性。"""
import sys, io
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import z2_route, run_segs, mota_core as M

buf = io.StringIO(); old = sys.stdout; sys.stdout = buf
z2_route.main()
sys.stdout = old
w = run_segs.LAST_W
h = w.hero
print('起点', h.f, (h.x, h.y), 'HP%d A%d D%d 钥%d/%d/%d' % (h.hp, h.atk, h.dfn, h.keys['y'], h.keys['b'], h.keys['r']))

# 手动走到 16F 下行梯 (6,1)
z2_route.goto(w, 6, 1, '16F 下行梯')
z2_route.stair(w, 6, 1, '16F->15F')
print('落 15F:', h.f, (h.x, h.y))

import heapq
def reach(w, start):
    dist = {start: 0}; prev = {start: None}; pq = [(0, start)]
    while pq:
        d, c = heapq.heappop(pq)
        if d > dist.get(c, 1e9): continue
        for dd in z2_route.DIRS:
            n = (c[0]+dd[0], c[1]+dd[1])
            ok, wc = z2_route._cost(w, h.f, *n)
            if ok and d + wc < dist.get(n, 1e9):
                dist[n] = d + wc; prev[n] = c; heapq.heappush(pq, (d+wc, n))
    return dist, prev

start = (h.x, h.y)
dist, prev = reach(w, start)
for tgt in [(6,10), (6,11), (1,10), (3,5), (3,6), (3,7), (1,7), (2,9), (1,4), (7,1), (6,1)]:
    if tgt in dist:
        p = []; c = tgt
        while c is not None:
            p.append(c); c = prev[c]
        print('可达 %-8s 代价%-6.1f 路径%d步 %s' % (str(tgt), dist[tgt], len(p)-1, p[::-1][-14:]))
    else:
        print('不可达', tgt)
