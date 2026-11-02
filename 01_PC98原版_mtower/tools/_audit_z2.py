# -*- coding: utf-8 -*-
"""2区（11-20F）血瓶审计：枚举所有药水瓶 + 交叉 run 轨迹（进11F 后到断点前已收集）。
"""
import sys, os, json, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as mc

d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'magic_tower1_map_50f.json'), encoding='utf-8'))
OA, TYPE = mc.OA, mc.TYPE

potions = {}
for fl in range(11, 21):
    f = d[str(fl)]
    obj = f['objects']
    for y in range(len(obj)):
        for x in range(len(obj[y])):
            o = obj[y][x]
            if not o: continue
            t = TYPE.get(OA[o][3] if o < len(OA) else 0, '?')
            hp = OA[o][10] if o < len(OA) else 0
            if t in ('STATUS', 'ITEM') and hp:
                potions.setdefault(fl, []).append((x, y, o, hp, mc.oname(o)))

print('=== 11-20F 药水瓶枚举 ===')
for fl in sorted(potions):
    for (x, y, o, hp, nm) in sorted(potions[fl], key=lambda z: (z[1], z[0])):
        print(f'  {fl}F({x},{y}) obj{o} HP+{hp}')
print(f'  合计 {sum(len(v) for v in potions.values())} 瓶 / {sum(v[3] for vv in potions.values() for v in vv)} HP')

# 枚举 11-20F 怪物（参考：A45/D51 下战损）
print('\n=== 11-20F 怪物（A45/D51 战损）===')
import math
for fl in range(11, 21):
    obj = d[str(fl)]['objects']
    for y in range(13):
        for x in range(13):
            o = obj[y][x]
            if o and TYPE.get(OA[o][3], '?') == 'MONSTER':
                a = OA[o]
                per = 45 - a[12]
                if per <= 0:
                    loss = '打不动'
                else:
                    turns = math.ceil(a[10]/per)
                    loss = max(a[11]-51,0)*(turns-1)
                print(f'  {fl}F({x},{y}) obj{o} {mc.oname(o)[:8]} hp{a[10]}/atk{a[11]}/def{a[12]} -> -{loss}')
