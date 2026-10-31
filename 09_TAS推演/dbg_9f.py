# -*- coding: utf-8 -*-
"""调试 path.py 解析式 与 真实引擎 在 9F 的分歧。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import path as P
import manual
W = P.W

P.stair(8, 6, 1, '8F(6,1)→9F')  # 现在在 9F(6,2)

# 用解析式 BFS 从 (6,2) 出发，打印所有可达 + 每格被拒的理由
DIRS = P.DIRS
from collections import deque
seen = {(6, 2)}
q = deque([(6, 2)])
blocked = []
while q:
    c = q.popleft()
    for d in DIRS:
        n = (c[0]+d[0], c[1]+d[1])
        if not (0 <= n[0] < 13 and 0 <= n[1] < 13) or n in seen:
            continue
        loss, kused, ok = P.move_cost(c, d)
        if ok:
            seen.add(n); q.append(n)
        else:
            t = W.terrain_at(9, n[0], n[1])
            o = W.at(9, n[0], n[1])
            blocked.append((n, o, t, loss, kused))

print('解析式可达 %d 格' % len(seen))
print('  (1,11) 在可达? %s' % ((1, 11) in seen))
print('被拒的贴边格（非墙）:')
for n, o, t, loss, kused in blocked:
    if t == 1 or t == 2:
        continue
    print('  %s obj%d terrain%d loss%d key%d' % (n, o, t, loss, kused))
