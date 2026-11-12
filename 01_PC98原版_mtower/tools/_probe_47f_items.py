# -*- coding: utf-8 -*-
"""47F 物品/特殊格详情：区分金币、钥匙、楼梯、商店，列出全部非空格。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

F = 47

print('47F 全格对象（非空）:')
for y in range(1, 12):
    for x in range(1, 12):
        t = M.terrain(F, x, y)
        o = M.obj_raw(F, x, y)
        info = []
        if t:
            info.append('terr=%d(%s)' % (t, {1:'墙',2:'楼梯'}.get(t, '?')))
        if o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            info.append('obj%d type=%s name=%s' % (o, ty, M.oname(o)))
        if info:
            print('(%2d,%2d): %s' % (x, y, ' | '.join(info)))

print()
print('47F 楼梯: up/dn =', M.stairs_of(F))

# 商店格：STATUS 类型的 obj 且不是战斗
print()
print('47F STATUS/ITEM 对象细节:')
for y in range(1, 12):
    for x in range(1, 12):
        o = M.obj_raw(F, x, y)
        if not o:
            continue
        ty = M.TYPE.get(M.oatr(o, 3), '?')
        if ty in ('ITEM', 'STATUS'):
            # 打印 oatr 各列
            cols = [M.oatr(o, c) for c in range(16)]
            print('(%2d,%2d) obj%d type=%s name=%s oatr=%s' % (x, y, o, ty, M.oname(o), cols))
