# -*- coding: utf-8 -*-
"""打印 merged_route_full.json 指定步区间的逐格路径（含事件/日志）。
用法: python _dump_block.py <start_step> <end_step>
"""
import json, sys

P = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/merged_route_full.json'
d = json.load(open(P, encoding='utf-8'))
steps = d['steps']
a = int(sys.argv[1]); b = int(sys.argv[2])
for s in steps:
    if a <= s['i'] <= b:
        ev = (s.get('e') or '') + ' ' + (s.get('l') or '')
        print('%5d f%-3d (%2d,%2d) %-2s HP%-6d A%-4d D%-4d G%-6d 钥%d/%d/%d  %s' % (
            s['i'], s['f'], s['x'], s['y'], s.get('d', ''), s['hp'], s['a'], s['df'], s['g'],
            s['ky'], s['kb'], s['kr'], ev.strip()[:90]))
