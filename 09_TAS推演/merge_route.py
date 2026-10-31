# -*- coding: utf-8 -*-
"""拼接 1F→9F 合法段 + 8F→11F 合法段 → 魔塔1_route_1F到11F_合法_v2.csv。
两段在 8F(6,2) 重叠：8F→11F 段的 step0 就是 1F→9F 段的最后一行，去掉重复。"""
import csv, io

DIR = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/'
F9 = DIR + '魔塔1_route_1F到9F_合法_v2.csv'
F811 = DIR + '魔塔1_route_8F到11F_合法.csv'
OUT = DIR + '魔塔1_route_1F到11F_合法_v2.csv'

def read(fn):
    with io.open(fn, encoding='utf-8-sig', newline='') as fp:
        return list(csv.DictReader(fp))

r9 = read(F9)
r811 = read(F811)

# 检查重叠点
last9 = r9[-1]
first811 = r811[0]
print('1F→9F 末行: step=%s %sF(%s,%s) HP%s A%s D%s G%s 钥%s/%s/%s' % (
    last9['step'], last9['floor'], last9['x'], last9['y'], last9['hp'], last9['atk'],
    last9['dfn'], last9['gold'], last9['ky'], last9['kb'], last9['kr']))
print('8F→11F 首行: step=%s %sF(%s,%s) HP%s A%s D%s G%s 钥%s/%s/%s' % (
    first811['step'], first811['floor'], first811['x'], first811['y'], first811['hp'],
    first811['atk'], first811['dfn'], first811['gold'], first811['ky'], first811['kb'], first811['kr']))

assert (last9['floor'], last9['x'], last9['y']) == (first811['floor'], first811['x'], first811['y']), '重叠点不一致！'

# 拼接：r9 全部 + r811 从第 2 行起
rows = []
for i, r in enumerate(r9):
    row = dict(r)
    row['step'] = str(i)
    rows.append(row)
base = len(r9)  # r9 行数，r811[0] 与之重复
for j, r in enumerate(r811[1:]):
    row = dict(r)
    row['step'] = str(base + j)
    rows.append(row)

# 写 OUT
with io.open(OUT, 'w', encoding='utf-8-sig', newline='') as fp:
    w2 = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
    w2.writeheader(); w2.writerows(rows)

print('拼接完成：%d 行 = 1F→9F %d 行 + 8F→11F %d 行，去重 %d 行' % (
    len(rows), len(r9), len(r811), len(r9) + len(r811) - len(rows)))
print('已存 %s' % OUT)
print('末行: %sF(%s,%s) HP%s A%s D%s G%s 钥%s/%s/%s' % (
    rows[-1]['floor'], rows[-1]['x'], rows[-1]['y'], rows[-1]['hp'], rows[-1]['atk'],
    rows[-1]['dfn'], rows[-1]['gold'], rows[-1]['ky'], rows[-1]['kb'], rows[-1]['kr']))