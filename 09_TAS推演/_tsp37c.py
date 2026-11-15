# -*- coding: utf-8 -*-
"""37F 超级镐后收 32 个战利品的最短开路路径（精确求解）。

几何：破墙后内部 11x11 全通，战利品恰好落在 4 个「3x3 少一格」的方块里：
  B1 右下 (x7-9, y7-9) 缺 (9,9)
  B2 左下 (x3-5, y7-9) 缺 (3,9)
  B3 左上 (x3-5, y3-5) 缺 (3,3)
  B4 右上 (x7-9, y3-5) 缺 (9,3)
每块 8 格。块内枚举全部哈密顿路径（相邻才成边），再对 4 块的访问顺序 + 各块出入口做
穷举组合，取总步数最小。这是「块内最优 + 块序最优」，比 2-opt 启发式可靠。
"""
import itertools

START = (11, 10)
END = (11, 4)

BLOCKS = {
    'B1': [(x, y) for y in (7, 8, 9) for x in (7, 8, 9) if (x, y) != (9, 9)],
    'B2': [(x, y) for y in (7, 8, 9) for x in (3, 4, 5) if (x, y) != (3, 9)],
    'B3': [(x, y) for y in (3, 4, 5) for x in (3, 4, 5) if (x, y) != (3, 3)],
    'B4': [(x, y) for y in (3, 4, 5) for x in (7, 8, 9) if (x, y) != (9, 3)],
}
for k, v in BLOCKS.items():
    assert len(v) == 8, (k, len(v))


def d(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def hamilton_paths(cells):
    """块内全部哈密顿路径：(entry, exit, steps, path)。"""
    out = []
    for perm in itertools.permutations(cells):
        ok = all(d(perm[i], perm[i + 1]) == 1 for i in range(7))
        if ok:
            out.append((perm[0], perm[-1], 7, list(perm)))
    return out


OPTS = {k: hamilton_paths(v) for k, v in BLOCKS.items()}
for k, v in OPTS.items():
    print('%s 块内哈密顿路径 %d 条' % (k, len(v)))

best = None
for order in itertools.permutations(BLOCKS):
    # 逐块 DP：state = 当前块出口 -> (累计步数, 具体路径)
    states = {}
    for ent, ext, c, path in OPTS[order[0]]:
        total = d(START, ent) + c
        if ext not in states or total < states[ext][0]:
            states[ext] = (total, [path], ent)
    for bi in range(1, 4):
        nxt = {}
        for ext, (tot, paths, _e) in states.items():
            for ent2, ext2, c2, path2 in OPTS[order[bi]]:
                t2 = tot + d(ext, ent2) + c2
                if ext2 not in nxt or t2 < nxt[ext2][0]:
                    nxt[ext2] = (t2, paths + [path2], ent2)
        states = nxt
    for ext, (tot, paths, _e) in states.items():
        total = tot + d(ext, END)
        if best is None or total < best[0]:
            seq = [START]
            for p in paths:
                seq += p
            seq.append(END)
            best = (total, seq)

print()
print('最优总步数 =', best[0])
seq = best[1]
assert len(seq) == 34 and len(set(seq[1:-1])) == 32
for i, p in enumerate(seq):
    print('  %2d (%2d,%2d)' % (i, p[0], p[1]))
line = '        '
print('\n    seq = [')
for p in seq:
    s = '(%d, %d), ' % p
    if len(line) + len(s) > 96:
        print(line)
        line = '        '
    line += s
print(line)
print('    ]')
