# -*- coding: utf-8 -*-
"""转储 merged_route_full.json 指定步号区间的路径，用于分析浪费环。用法：_dump_block.py <a> <b>"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, '09_TAS推演', 'merged_route_full.json')

a = int(sys.argv[1]); b = int(sys.argv[2])
d = json.load(open(P, encoding='utf-8'))
for s in d['steps']:
    if a <= s['i'] <= b:
        print('%5d f%-2d(%2d,%2d) %s HP%-6d A%-4d D%-4d G%-5d %s' % (
            s['i'], s['f'], s['x'], s['y'], s.get('d', ''), s['hp'], s['a'], s['df'],
            s['g'], s.get('l', '')[:70]))