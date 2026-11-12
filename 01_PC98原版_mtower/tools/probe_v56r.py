# -*- coding: utf-8 -*-
"""probe_v56r.py —— 37F 连通性探测：跑完整路线到 37F 落点，BFS 可达集 + 可达物件列表。"""
import sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ['MOTA_PROBE_FLOOR'] = ''
import z2_route as Z
import mota_core as M

# 跑 main() 拿到 LAST_W？main() 内部用 run_segs.LAST_W，main 不返回 w。
# 但我们可以在 main() 执行到一半时，用 hook 捕获 w。
# 简化：直接调用 run_segs + z2_route 的 main，然后从 run_segs.LAST_W 取不到（z2_route 内部新建?）
# 查看 z2_route.main() 是否复用 run_segs.LAST_W —— 是（line 309 w = run_segs.LAST_W）。
# 所以 main() 结束后 run_segs.LAST_W 就是最后世界？不一定，main 内 w 是局部。
# 更稳：monkeypatch Z.run / Z.stair / Z.fly 记录最后 w。

captured = {}
orig_run = Z.run
def spy_run(w, pts, tag=''):
    captured['w'] = w
    return orig_run(w, pts, tag)
Z.run = spy_run
# 也 spy stair/fly（它们在 run 之后执行）
orig_stair = Z.stair
def spy_stair(w, *a, **k):
    captured['w'] = w
    return orig_stair(w, *a, **k)
Z.stair = spy_stair
orig_fly = Z.fly
def spy_fly(w, *a, **k):
    captured['w'] = w
    return orig_fly(w, *a, **k)
Z.fly = spy_fly

rc = Z.main()
print('main rc =', rc)
w = captured.get('w')
if w is None:
    print('!! 未捕获 w')
    sys.exit(1)
h = w.hero
print('终点:', Z.st(h))
print('hero items =', sorted(h.items))
f = h.f

# BFS 连通性（仅层内，忽略楼梯格，用 _cost 判定可走）
from collections import deque
start = (h.x, h.y)
dist = {start: 0}
q = deque([start])
while q:
    c = q.popleft()
    for dx, dy in Z.DIRS:
        n = (c[0] + dx, c[1] + dy)
        if n in dist:
            continue
        if not (1 <= n[0] <= 11 and 1 <= n[1] <= 11):
            continue
        ok, _ = Z._cost(w, f, *n)
        if not ok:
            continue
        dist[n] = dist[c] + 1
        q.append(n)
print('\n--- %dF 可达集（从落点 %s，共 %d 格）---' % (f, start, len(dist)))
for y in range(13):
    row = []
    for x in range(13):
        if (x, y) == start:
            ch = '@'
        elif (x, y) in dist:
            ch = '.'
        else:
            ch = ' '
        # 物件叠加
        o = w.at(f, x, y)
        if o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            if o in M.KEY_OF:
                ch = {'y': 'y', 'b': 'b', 'r': 'r'}[M.KEY_OF[o]]
            elif o in M.DOOR_OF:
                ch = {'y': 'Y', 'b': 'B', 'r': 'R'}[M.DOOR_OF[o]]
            elif o == 89:
                ch = 'D'
            elif o in M.SHOP:
                ch = '$'
            elif ty == 'MONSTER':
                ch = 'm'
            elif ty == 'ITEM':
                ch = '!'
            elif ty == 'STATUS':
                ch = '+'
            elif ty == 'MESSAGE':
                ch = '?'
        row.append(ch)
    print('%2d %s' % (y, ' '.join(row)))
print('   ' + ' '.join('%X' % x for x in range(13)))

# 列出可达格上的物件
print('\n--- 可达格物件（在 BFS 可达集内）---')
for (x, y) in sorted(dist, key=lambda p: (p[1], p[0])):
    o = w.at(f, x, y)
    if not o:
        continue
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    print('  (%2d,%2d) obj%-4d %-8s %s' % (x, y, o, ty, M.oname(o)[:40]))
