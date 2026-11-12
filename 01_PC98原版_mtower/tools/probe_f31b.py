# -*- coding: utf-8 -*-
"""探查 31F 所有怪物的完整属性 + obj142 类型，判断哪个怪"不伤"（ATK<=133）。"""
import os
import sys
import io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import mota_core as mc

print('OA 表列含义: [0]=? [5]=名 [10]=HP [11]=ATK [12]=DEF [13]=GOLD')
print()

# 31F 所有对象，输出完整属性
print('=== 31F 对象属性（含战斗数值）===')
seen = {}
for y in range(13):
    for x in range(13):
        o = mc.obj_raw(31, x, y)
        if o:
            name = mc.oname(o)
            hp = mc.oatr(o, 10)
            atk = mc.oatr(o, 11)
            dfn = mc.oatr(o, 12)
            gold = mc.oatr(o, 13)
            if (o, name) not in seen:
                seen[(o, name)] = True
                print(f'  obj{o:3d}  {name:12s} HP={hp:5d} ATK={atk:5d} DEF={dfn:4d} GOLD={gold:4d}')
print()

# 31F 每个怪的位置
print('=== 31F 怪物位置 ===')
for y in range(13):
    for x in range(13):
        o = mc.obj_raw(31, x, y)
        if o and mc.oatr(o, 11) > 0:  # ATK>0 视为怪
            name = mc.oname(o)
            print(f'  ({x:2d},{y:2d}) obj{o:3d} {name:12s} ATK={mc.oatr(o,11)} DEF={mc.oatr(o,12)} HP={mc.oatr(o,10)} GOLD={mc.oatr(o,13)}')
print()

# 当前玩家 DEF=133，判定哪些怪不伤
print('=== 玩家 DEF=133 时各怪战斗伤害（per=ATK-DEF 或 146-怪DEF）===')
for y in range(13):
    for x in range(13):
        o = mc.obj_raw(31, x, y)
        if o and mc.oatr(o, 11) > 0:
            name = mc.oname(o)
            mhp, matk, mdef, mgold = mc.oatr(o,10), mc.oatr(o,11), mc.oatr(o,12), mc.oatr(o,13)
            per = 146 - mdef  # 玩家ATK146
            if per <= 0:
                print(f'  ({x:2d},{y:2d}) {name:12s}: 玩家打不动! per={per}')
                continue
            turns = -(-mhp // per)  # ceil
            loss = max(matk - 133, 0) * (turns - 1)
            print(f'  ({x:2d},{y:2d}) {name:12s}: per={per} turns={turns} loss={loss}  {"【不伤】" if loss==0 else ""}')
print()

# obj142 / obj92 的类型与完整 OA 行
for o in (142, 92, 49):
    row = mc.OA[o] if o < len(mc.OA) else None
    print(f'obj{o}: OA row = {row}')
    print(f'   name={mc.oname(o)}')
