# -*- coding: utf-8 -*-
"""扫描 merged_route_full.json：按「同层连续访问段」统计停留步数，列出 Top 浪费环。
环 = 该层段内被重复访问（形成环）的额外步数 = 段长 - 不同格数。
"""
import json, collections, sys

P = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/merged_route_full.json'
d = json.load(open(P, encoding='utf-8'))
steps = d['steps']

# 切段：floor 变化即断（fly 也换层）
blocks = []
cur = []
for s in steps:
    if cur and s['f'] != cur[-1]['f']:
        blocks.append(cur)
        cur = []
    cur.append(s)
if cur:
    blocks.append(cur)

rows = []
for b in blocks:
    cells = [(s['x'], s['y']) for s in b]
    cnt = collections.Counter(cells)
    dup = sum(v - 1 for v in cnt.values())
    rows.append(dict(f=b[0]['f'], start=b[0]['i'], end=b[-1]['i'], n=len(b),
                     dup=dup, distinct=len(cnt),
                     entry=(b[0]['x'], b[0]['y']), exit=(b[-1]['x'], b[-1]['y'])))

print('总步数', len(steps), ' 段数', len(rows))
print()
print('== Top 25 按段长 ==')
for r in sorted(rows, key=lambda r: -r['n'])[:25]:
    print('f%-3d 步%-4d 段长%-4d 重复%-4d 入%s 出%s' % (
        r['f'], r['start'], r['n'], r['dup'], r['entry'], r['exit']))
print()
print('== Top 15 按重复步数 ==')
for r in sorted(rows, key=lambda r: -r['dup'])[:15]:
    print('f%-3d 步%-4d 段长%-4d 重复%-4d 入%s 出%s' % (
        r['f'], r['start'], r['n'], r['dup'], r['entry'], r['exit']))
