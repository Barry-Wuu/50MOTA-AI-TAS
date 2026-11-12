# -*- coding: utf-8 -*-
"""探测 7F/34F/40F/15F/39F/41F 商店、楼梯、钥匙、怪物，为 V66-V71 做准备。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

def dump(f, title):
    print(f"\n===== {title} ({f}F) =====")
    up, dn = M.STAIRS.get(f, (None, None))
    print(f"STAIRS: up={up} down={dn}  FLY_LAND={M.FLY_LAND.get(f)}")
    for y in range(1, 12):
        row = []
        for x in range(1, 12):
            o = M.obj_raw(f, x, y)
            t = M.terrain(f, x, y)
            if o:
                # 尝试命名
                name = M.oname(o)[:6]
                row.append(f"{o:>2}")
            else:
                row.append(" ." if t == 0 else (" #" if t == 1 else " S"))
        print(f"y{y:>2}: " + ' '.join(row))
    # 详细列出关键 obj
    print("--- 关键物件 ---")
    seen = {}
    for y in range(1, 12):
        for x in range(1, 12):
            o = M.obj_raw(f, x, y)
            if o:
                seen.setdefault(o, []).append((x, y))
    for o, cells in sorted(seen.items()):
        typ = M.TYPE.get(M.oatr(o, 3), '?')
        name = M.oname(o)
        grant = M.SHOP_GRANT.get(o)
        price = M.SHOP_PRICE.get(o)
        extra = ''
        if grant:
            extra = f" SHOP{grant}@{price}G"
        elif o in M.SHOP:
            extra = f" SHOP?@{price}G"
        elif o in M.KEY_OF:
            extra = f" KEY:{M.KEY_OF[o]}"
        elif o in M.DOOR_OF:
            extra = f" DOOR:{M.DOOR_OF[o]}"
        print(f"  obj{o:>3} {typ:>7} {name[:18]:<18} {cells}{extra}")

for f in [7, 34, 40, 15, 39, 41]:
    dump(f, f"floor{f}")
