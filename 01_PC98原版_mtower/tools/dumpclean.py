# -*- coding: utf-8 -*-
"""干净的单格转储：每格一行，明确 区域/地形/物件。"""
import sys
import mota_core as M
import routelib as R

TAGS = {}
for o in range(1, 200):
    try:
        TAGS[o] = M.oname(o)
    except Exception:
        pass

f = int(sys.argv[1])
F = R.Floor(f)
w = M.World.new()
print("FLOOR %d  区数=%d" % (f, len(F.regcells)))
print("格坐标 | 区 | 地形 | 物件")
for y in range(1, 12):
    for x in range(1, 12):
        t = w.terrain_at(f, x, y)
        o = w.at(f, x, y)
        if t == 1 and not o:
            continue
        ty = M.TYPE.get(M.oatr(o, 3), '-') if o else '-'
        extra = ''
        if o and ty == 'MONSTER':
            extra = ' hp=%d atk=%d def=%d gold=%d' % (M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13))
        elif o and ty == 'STATUS':
            extra = ' HP+=%d ATK+=%d DEF+=%d' % (M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12))
        elif o and ty == 'DOOR':
            extra = ' 色=%s' % ('暗' if o == 89 else {'y': '黄', 'b': '蓝', 'r': '红'}[M.DOOR_OF[o]])
        elif o and ty == 'KEY':
            extra = ' 色=%s' % {'y': '黄', 'b': '蓝', 'r': '红'}[M.KEY_OF[o]]
        elif o in M.SHOP:
            extra = ' 价=%dG 获得=%s' % (M.SHOP_PRICE.get(o, 0), M.SHOP_GRANT.get(o))
        print("(%2d,%2d) | 区%-3s | %s | obj%-4d %-10s %s%s" % (
            x, y, F.reg.get((x, y), '-'), {0: '地板', 1: '墙', 2: '梯'}[t],
            o, ty, TAGS.get(o, ''), extra))
