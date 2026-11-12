# -*- coding: utf-8 -*-
"""V49 钥匙赤字诊断：跑路线至 V48 末（V49 首个 need 触发点），
转储当时全图剩余钥匙格 + 各层黄门数，供重新平衡钥匙账用。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2_route
import mota_core as M

dumped = {'done': False}
_orig_need = z2_route.need

def need_hook(w, y=0, b=0, r=0, g=0, label=''):
    if not dumped['done'] and '34F 黄门(2,4)' in label:
        dumped['done'] = True
        h = w.hero
        print('\n######## V49 起点状态诊断 ########')
        print(f'HP{h.hp} A{h.atk} D{h.dfn} G{h.gold} 钥 {h.keys["y"]}/{h.keys["b"]}/{h.keys["r"]}'
              f'  位置 {h.f}F({h.x},{h.y})')
        print('--- 各层剩余钥匙（at() 反映已清/事件态）---')
        for f in range(1, 41):
            ks = []
            for yy in range(13):
                for xx in range(13):
                    o = w.at(f, xx, yy)
                    if o in M.KEY_OF:
                        ks.append(f'({xx},{yy}){M.KEY_OF[o]}')
            if ks:
                doors = sum(1 for yy in range(13) for xx in range(13)
                            if M.TYPE.get(M.oatr(w.at(f, xx, yy), 3)) == 'DOOR')
                print(f'  {f:2d}F: {" ".join(ks)}   [余门 {doors}]')
        print('--- 33F/34F 关键可达性核查 ---')
        for f in (33, 34):
            for xx, yy in ((5, 10), (1, 11), (6, 1), (9, 1), (10, 1), (10, 2), (10, 11)):
                o = w.at(f, xx, yy)
                print(f'  {f}F({xx},{yy}) obj={o} {M.oname(o)[:8]}')
        print('####################################\n')
    return _orig_need(w, y=y, b=b, r=r, g=g, label=label)

z2_route.need = need_hook
sys.exit(z2_route.main())
