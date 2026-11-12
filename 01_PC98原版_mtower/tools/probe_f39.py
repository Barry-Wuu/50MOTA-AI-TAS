# -*- coding: utf-8 -*-
"""dump 39F 完整对象：确认红晶数量与位置（V59 是否漏拿攻击宝石）。"""
import os
import sys
import io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import mota_core as mc

print('=== 39F 全部对象 ===')
for y in range(13):
    for x in range(13):
        o = mc.obj_raw(39, x, y)
        if o:
            name = mc.oname(o)
            print(f'  ({x:2d},{y:2d}) obj{o:3d}  {name}')
print()
print('=== 39F 含 ATK>0 的对象（攻击宝石/怪）===')
for y in range(13):
    for x in range(13):
        o = mc.obj_raw(39, x, y)
        if o:
            atk = mc.oatr(o, 11)
            hp = mc.oatr(o, 10)
            name = mc.oname(o)
            if atk > 0 or (hp > 0 and atk > 0):
                print(f'  ({x:2d},{y:2d}) obj{o:3d}  {name}  HP={hp} ATK={atk}')
