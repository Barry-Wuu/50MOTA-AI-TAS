# -*- coding: utf-8 -*-
"""临时探针：在 41F 入口 need 前注入 EXTRA_Y 把黄钥匙，重跑全流程看后续是否通关。
不修改 z2_route.py / build_full50.py 源码，仅 monkeypatch。
"""
import os
import sys

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
sys.path.insert(0, TOOLS)

import z2_route as Z

_n = int(os.environ.get('EXTRA_Y', '0'))
if _n:
    _orig_need = Z.need

    def _need(w, *a, **k):
        if '41F 入口' in k.get('label', ''):
            w.hero.keys['y'] += _n
            print('=== PROBE 41F 入口前补黄钥匙 +%d，当前 黄%d/蓝%d ==='
                  % (_n, w.hero.keys['y'], w.hero.keys['b']))
        return _orig_need(w, *a, **k)

    Z.need = _need

if os.environ.get('PROBE_14F'):
    _orig_need14 = Z.need

    def _need14(w, *a, **k):
        if '14F 黄门(6,6)' in k.get('label', ''):
            print('=== 14F 运行时地图（V31 入口）hero=(%d,%d,%d) keys=%s ==='
                  % (w.hero.f, w.hero.x, w.hero.y, dict(w.hero.keys)))
            Z._dump_floor(w, 14)
        return _orig_need14(w, *a, **k)

    Z.need = _need14

if os.environ.get('ADAPT_SELL'):
    _orig_sell = Z.sell_keys

    def _sell(w, n, label=''):
        if 'V83 28F 商人卖钥第' in label and w.hero.keys['y'] <= 0:
            return True          # 钥匙已卖完，静默跳过剩余次数
        return _orig_sell(w, n, label)

    Z.sell_keys = _sell

_src = open('build_full50.py', encoding='utf-8').read()
exec(compile(_src, 'build_full50.py', 'exec'), {'__name__': '__main__'})
