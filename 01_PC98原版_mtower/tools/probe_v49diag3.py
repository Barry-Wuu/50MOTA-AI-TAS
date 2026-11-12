# -*- coding: utf-8 -*-
"""V49 修复探针 #3：跑到 V48 末（34F(2,1)），转储 33F + 34F 实时布局，
并做钥匙格可达性分析（当前 1 黄钥、0 蓝、0 红）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2_route
import mota_core as M

dumped = {'done': False}
_orig_need = z2_route.need

def reach(w, f, sx, sy):
    """BFS 可达（仅走空地/已清怪物格；不消耗钥匙/不进入未开格）。"""
    from collections import deque
    seen = {(sx, sy)}
    q = deque([(sx, sy)])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < 13 and 0 <= ny < 13) or (nx, ny) in seen:
                continue
            if w.terrain_at(f, nx, ny) == 1:
                continue
            o = w.at(f, nx, ny)
            if o in M.DOOR_OF:
                continue                      # 门未开：不可通行
            if o in M.KEY_OF:
                seen.add((nx, ny)); q.append((nx, ny)); continue
            if o and M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
                if (f, nx, ny) not in w.cleared:
                    continue                  # 未清怪：不可通行
            seen.add((nx, ny)); q.append((nx, ny))
    return seen

def need_hook(w, y=0, b=0, r=0, g=0, label=''):
    if not dumped['done'] and '34F 黄门(2,4)' in label:
        dumped['done'] = True
        h = w.hero
        print('\n######## V49 起点（34F(2,1)）诊断 #3 ########')
        print(f'HP{h.hp} A{h.atk} D{h.dfn} G{h.gold} 钥 {h.keys["y"]}/{h.keys["b"]}/{h.keys["r"]}'
              f'  位置 {h.f}F({h.x},{h.y})')
        for f in (33, 34):
            print(f'\n===== {f}F 布局 =====')
            z2_route._dump_floor(w, f)
        # 33F 钥匙格可达性
        print('\n--- 33F 钥匙格可达性（从 33F(1,1) 楼梯，0 消耗钥匙 BFS）---')
        r33 = reach(w, 33, 1, 1)
        for xx, yy in ((5, 10), (1, 11)):
            print(f'  33F({xx},{yy}) obj={w.at(33,xx,yy)} 可达={"是" if (xx,yy) in r33 else "否"}')
        # 34F 起点区可达性
        print('--- 34F 可达集（从 (2,1)，不消耗钥匙）---')
        r34 = reach(w, 34, 2, 1)
        for xx, yy in ((3,1),(4,2),(6,1),(2,4),(2,8),(4,10),(8,10),(10,11),(6,11)):
            print(f'  34F({xx},{yy}) 可达={"是" if (xx,yy) in r34 else "否"}')
        print('####################################\n')
    return _orig_need(w, y=y, b=b, r=r, g=g, label=label)

z2_route.need = need_hook
sys.exit(z2_route.main())
