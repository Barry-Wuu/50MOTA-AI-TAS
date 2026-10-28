# -*- coding: utf-8 -*-
"""11F→38F 逐层「绕门优先」规划（口径对齐 mota_core 引擎）。

引擎口径（与 magic_tower1_map_50f.json 的 terrain 字段**相反**）：
  · M.terrain()==1 → 墙；==2 → 楼梯
  · 钥匙只有 obj1(黄)/obj3(蓝)/obj28(红)  ← obj88 是盗贼 NPC，不是钥匙
  · obj21/obj23 是可踩装饰，不是落穴；obj20 实心
"""
import sys, heapq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W_Y, W_B, W_R = 800, 60000, 200000
W_MON, W_LAVA = 300, 25

JOBS = [
    (11, (6, 11), (11, 11)), (12, (10, 11), (1, 11)), (13, (2, 11), (11, 11)),
    (14, (10, 11), (6, 11)), (15, (6, 10), (6, 1)),   (16, (6, 2),  (6, 11)),
    (17, (6, 10), (6, 1)),   (18, (6, 2),  (1, 1)),   (19, (1, 2),  (6, 11)),
    (20, (6, 10), (6, 1)),   (21, (6, 2),  (6, 11)),  (22, (6, 10), (6, 6)),
    (23, (1, 2),  (11, 1)),  (24, (2, 11), (2, 10)),  (25, (2, 11), (1, 11)),
    (26, (2, 11), (2, 10)),  (27, (2, 11), (11, 11)), (28, (10, 11), (1, 11)),
    (29, (1, 10), (6, 11)),  (30, (6, 10), (6, 1)),   (31, (6, 2),  (6, 11)),
    (32, (6, 10), (11, 1)),  (33, (10, 1), (1, 1)),   (34, (2, 1),  (6, 11)),
    (35, (6, 10), (11, 1)),  (36, (11, 2), (11, 11)), (37, (11, 10), (1, 1)),
    (38, (2, 1),  (11, 1)),
]
MUST = {13: [(6, 5)], 15: [(6, 6)], 19: [(6, 3)], 38: [(2, 7)]}


def cell_cost(f, x, y):
    t = M.terrain(f, x, y)
    if t == 1:
        return (2, '暗墙') if (f, x, y) in M.DARKWALL_CELLS else None
    o = M.obj_raw(f, x, y)
    if o == 89:
        return 2, '暗墙'
    if o == 115:
        return 2, '隐形块'
    if o == 79:
        return W_LAVA, '熔岩'
    if o in (2, 4, 27):
        return {2: W_Y, 4: W_B, 27: W_R}[o], {2: '黄门', 4: '蓝门', 27: '红门'}[o]
    if o == 20:
        return None
    if o in (21, 23):
        return 1, ''
    if o and M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
        return W_MON, '怪'
    return 1, ''


def dijkstra(f, s, g):
    dist = {s: 0}
    pre = {s: None}
    h = [(0, s)]
    while h:
        d, c = heapq.heappop(h)
        if c == g:
            break
        if d > dist.get(c, 1 << 60):
            continue
        x, y = c
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if not (0 <= n[0] < 13 and 0 <= n[1] < 13):
                continue
            cc = cell_cost(f, n[0], n[1])
            if cc is None:
                continue
            nd = d + cc[0]
            if nd < dist.get(n, 1 << 60):
                dist[n] = nd
                pre[n] = c
                heapq.heappush(h, (nd, n))
    if g not in pre:
        return None
    p, c = [], g
    while c is not None:
        p.append(c)
        c = pre[c]
    return p[::-1]


def main():
    tot = {'黄门': 0, '蓝门': 0, '红门': 0}
    for f, s, g in JOBS:
        chain = [s] + MUST.get(f, []) + [g]
        full, ok = [], True
        for a, b in zip(chain, chain[1:]):
            p = dijkstra(f, a, b)
            if p is None:
                ok = False
                print('%2dF %s→%s ✗不通' % (f, a, b))
                continue
            full += p if not full else p[1:]
        doors, keys, mons = [], [], []
        for (x, y) in full:
            o = M.obj_raw(f, x, y)
            if o == 2:
                doors.append('黄(%d,%d)' % (x, y)); tot['黄门'] += 1
            elif o == 4:
                doors.append('蓝(%d,%d)' % (x, y)); tot['蓝门'] += 1
            elif o == 27:
                doors.append('红(%d,%d)' % (x, y)); tot['红门'] += 1
            elif o == 3:
                keys.append('蓝钥(%d,%d)' % (x, y))
            elif o == 1:
                keys.append('黄钥(%d,%d)' % (x, y))
            elif o == 28:
                keys.append('红钥(%d,%d)' % (x, y))
            elif o == 79:
                mons.append('熔岩(%d,%d)' % (x, y))
            elif o and M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
                mons.append('%s(%d,%d)' % (M.oname(o)[:5], x, y))
        print('%2dF %s→%s 步%-3s 门:%-24s 拾:%-22s 战/险:%s' % (
            f, s, g, len(full) - 1 if ok else '—',
            ' '.join(doors) or '无', ' '.join(keys) or '无', ' '.join(mons) or '无'))
    print()
    print('主线开门合计（绕门优先后）:', tot)


if __name__ == '__main__':
    main()
