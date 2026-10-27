"""最小钥匙消耗分析：BFS over (pos, opened_doors_mask)，代价按颜色计。"""
import collections, heapq
import mota_core as M

def door_bits(f):
    d = {}
    for y in range(13):
        for x in range(13):
            if M.terrain(f, x, y) == 1:
                continue
            o = M.obj_raw(f, x, y)
            if o and M.TYPE.get(M.oatr(o, 3)) == 'DOOR':
                d[(x, y)] = (len(d), M.DOOR_OF.get(o))
    return d

def min_keys(f, start, goals, monster_pass=True):
    """返回 (黄,蓝,红) 最小消耗 到 goals 集合（字典序最小）。"""
    db = door_bits(f)
    idx = {c: i for c, (i, _) in db.items()}
    # Dijkstra on (yused,bused,rused) with state (cell, opened_mask)
    pq = [(0, 0, 0, start, 0)]
    best = {}
    while pq:
        yc, bc, rc, cell, mask = heapq.heappop(pq)
        st = (cell, mask)
        cur = (yc, bc, rc)
        if st in best and best[st] <= cur:
            continue
        best[st] = cur
        if cell in goals:
            return cur
        x, y = cell
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < 13 and 0 <= ny < 13):
                continue
            if M.terrain(f, nx, ny) == 1:
                continue
            tgt = (nx, ny)
            nm = mask; y2, b2, r2 = yc, bc, rc
            if tgt in idx:
                i, col = db[tgt]
                if not (mask >> i) & 1:
                    nm = mask | (1 << i)
                    if col == 'y': y2 += 1
                    elif col == 'b': b2 += 1
                    elif col == 'r': r2 += 1
            else:
                o = M.obj_raw(f, nx, ny)
                if o and M.TYPE.get(M.oatr(o, 3)) == 'MONSTER' and not monster_pass:
                    continue
            heapq.heappush(pq, (y2, b2, r2, tgt, nm))
    return None

if __name__ == '__main__':
    import sys
    f = int(sys.argv[1]); sx = int(sys.argv[2]); sy = int(sys.argv[3])
    goals = set()
    for a in sys.argv[4:]:
        x, y = a.split(','); goals.add((int(x), int(y)))
    print(f'{f}F 从({sx},{sy}) 到 {sorted(goals)} 最小钥匙消耗(黄,蓝,红) =',
          min_keys(f, (sx, sy), goals))
