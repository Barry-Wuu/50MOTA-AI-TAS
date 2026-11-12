# -*- coding: utf-8 -*-
"""V49 修复探针 #2：跑到 V48 末（33F 上 34F 楼梯前），转储 34F 实时布局，
并做 A* 可达性分析，确认哪些钥匙/门能在当前状态被触达，用于重新平衡钥匙账。"""
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
        print('\n######## V49 起点（34F 楼梯前）诊断 #2 ########')
        print(f'HP{h.hp} A{h.atk} D{h.dfn} G{h.gold} 钥 {h.keys["y"]}/{h.keys["b"]}/{h.keys["r"]}'
              f'  位置 {h.f}F({h.x},{h.y})')
        z2_route._dump_floor(w, 34)
        print('####################################\n')
    return _orig_need(w, y=y, b=b, r=r, g=g, label=label)

z2_route.need = need_hook
sys.exit(z2_route.main())
