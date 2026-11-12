# -*- coding: utf-8 -*-
"""探测：10F 首段结束后，9F 右下补血区（攻略 line175 第1站）的可达性与剩余物件。"""
import manual as U
import mota_core as M
from collections import deque

# 截到「10F 首段结束」为止（下一动作是 '10F 右区南下'）
idx = next(i for i, a in enumerate(U.PLAN) if a[0] == 'w' and a[4].startswith('10F 右区南下'))
U.execute(U.PLAN[:idx], verbose=False)
h = U.W.hero
print('当前:', 'HP%d A%d D%d G%d 钥%d/%d/%d %dF(%d,%d)' % (
    h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y))

# 走到 9F 落点
U.walk(10, (1, 10))
U.enter(10, 1, 11, '下楼')
h = U.W.hero
print('到 9F:', 'HP%d A%d D%d G%d 钥%d/%d/%d %dF(%d,%d)' % (
    h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y))

# 9F 自由格连通域
seen = {(h.x, h.y)}
q = deque([(h.x, h.y)])
while q:
    c = q.popleft()
    for d in U.DIRS:
        n = (c[0] + d[0], c[1] + d[1])
        if n in seen or not U.free(9, n[0], n[1]):
            continue
        seen.add(n); q.append(n)
print('9F 可达 %d 格' % len(seen))
for target in [(7, 11), (9, 11), (11, 11), (11, 9), (9, 9), (11, 8), (11, 7)]:
    print('  %-8s free=%-5s reachable=%s  obj=%s' % (
        target, U.free(9, *target), target in seen,
        ('%s obj%d' % (M.oname(U.W.at(9, *target))[:12], U.W.at(9, *target))) if U.W.at(9, *target) else '空'))
print('\n9F 右下区全部物件:')
for y in range(6, 12):
    for x in range(5, 12):
        o = U.W.at(9, x, y)
        if o:
            print('  (%2d,%2d) obj%-4d %s' % (x, y, o, M.oname(o)))
