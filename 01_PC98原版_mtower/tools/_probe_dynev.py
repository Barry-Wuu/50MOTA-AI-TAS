# -*- coding: utf-8 -*-
"""DYNEV 全量：floor 39 / 41 / 45 / 1 / 43 的所有写入条目（不过滤）"""
import sys, io, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import mota_core as M

print('=== mota_core 里 DYNEV 相关名字 ===')
for n in dir(M):
    if 'DYN' in n.upper() or 'EV' in n.upper():
        v = getattr(M, n)
        if isinstance(v, (list, dict, tuple)):
            print('  %-22s len=%d' % (n, len(v)))

# 直接从 json 读原始
p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'magic_tower1_map_50f.json')
print()
print('=== 原始 JSON 里含 "eventMT" 的写入点（按 floor 统计）===')
with open(p, encoding='utf-8') as fp:
    data = json.load(fp)

def walk(o, path=''):
    if isinstance(o, dict):
        if 'obj' in o and 'method' in o:
            yield o
        for k, v in o.items():
            yield from walk(v, path + '/' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + '[%d]' % i)

hits = list(walk(data))
print('  总条目:', len(hits))
from collections import Counter
print('  method 分布:', Counter(h.get('method') for h in hits))
print()
for h in hits:
    fl = str(h.get('floor'))
    if fl in ('39', '41', '45', '43', '1', '0'):
        print('  floor=%-3s x=%-3s y=%-3s obj=%-4s method=%-10s site=%s'
              % (h.get('floor'), h.get('x'), h.get('y'), h.get('obj'),
                 h.get('method'), h.get('site')))
