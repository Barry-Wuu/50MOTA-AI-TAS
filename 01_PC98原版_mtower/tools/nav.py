"""段式导航：在 mota_core 世界状态上，用 BFS（真实 move 判定）从当前状态走到目标格。
返回 (新世界, 动作串, 摘要)。每次 clone 试走，状态数小段内可控。
"""
import collections
import mota_core as M

DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
KN = {(0, -1): '8', (0, 1): '2', (-1, 0): '4', (1, 0): '6'}


def bfs_step(w, goal, max_states=200000):
    """goal: (f,x,y)。返回 (动作串, 终点世界) 或 None。BFS 逐动作（代价=步数）"""
    start = w.clone()
    if (start.hero.f, start.hero.x, start.hero.y) == goal:
        return [], start
    prev = {None: None}
    q = collections.deque()
    q.append((start, None, None))          # (world, act, parent_id)
    store = [None]
    seen = set()
    nid = 0
    store[0] = (start, None, None)
    q = collections.deque([0])
    seen.add((start.hero.f, start.hero.x, start.hero.y, start.hero.keys['y'], start.hero.keys['b'],
              w.trap_done))
    n = 0
    while q:
        idx = q.popleft()
        wcur, act, par = store[idx]
        n += 1
        if n > max_states:
            return None
        for d in DIRS:
            w2 = wcur.clone()
            log = w2.move(*d)
            if M.blocked(log):
                continue
            k = (w2.hero.f, w2.hero.x, w2.hero.y, w2.hero.keys['y'], w2.hero.keys['b'], w2.trap_done,
                 frozenset(c for c in w2.cleared if c in M.PICKUP_CELLS))
            if k in seen:
                continue
            seen.add(k)
            nid += 1
            store.append((w2, d, idx))
            if (w2.hero.f, w2.hero.x, w2.hero.y) == goal:
                acts = []
                cur = nid
                while cur is not None:
                    ww, a, p = store[cur]
                    if a is not None:
                        acts.append(a)
                    cur = p
                return list(reversed(acts)), w2
            q.append(nid)
    return None
