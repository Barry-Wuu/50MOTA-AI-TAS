# -*- coding: utf-8 -*-
"""中心对称飞行器 obj106 落点反查：sym(P) = (12-x, 12-y)"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import mota_core as M

def sym(x, y):
    return 12 - x, 12 - y

for f in (41, 42, 45):
    print('=' * 60)
    print('%dF  STAIRS' % f, M.STAIRS[f])
    print('-' * 60)
    for y in range(13):
        row = ''
        for x in range(13):
            if M.terrain(f, x, y) == 1:
                row += '##'
                continue
            o = M.obj_raw(f, x, y)
            if M.terrain(f, x, y) == 2:
                row += '<>'
            elif o:
                row += '%2d' % (o % 100)
            else:
                row += ' .'
        print(' y%2d %s' % (y, row))
    print('     ' + ''.join('%2d' % x for x in range(13)))
    print()

print('=' * 60)
print('反查：想让英雄落到目标格 T，须站在 sym(T)')
print('=' * 60)
checks = [
    (41, '上行梯邻格', (6, 10)),
    (42, '上行梯邻格', (1, 2)),
    (42, '上行梯邻格', (2, 1)),
    (45, '昇華の翼 obj107', (2, 10)),
    (45, '上行梯邻格', (10, 1)),
]
for f, tag, T in checks:
    P = sym(*T)
    tp = M.terrain(f, P[0], P[1])
    op = M.obj_raw(f, P[0], P[1])
    print('%dF  目标 %-16s T=%s  → 站位 P=%s  terrain=%d obj=%d %s'
          % (f, tag, T, P, tp, op, M.oname(op) if op else ''))
