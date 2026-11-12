# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import mota_core as M

d = M.DYNEV
print('type:', type(d), 'len:', len(d))
for i, part in enumerate(d):
    print('  part[%d] type=%s len=%s' % (i, type(part), len(part) if hasattr(part, '__len__') else '-'))
    if hasattr(part, '__len__') and len(part):
        print('    sample:', repr(part[0])[:300])

rows = None
for part in d:
    if isinstance(part, (list, tuple)) and part and isinstance(part[0], dict):
        rows = part

print()
print('rows:', len(rows))
keys = set()
for r in rows:
    keys |= set(r.keys())
print('keys:', sorted(keys))
print()
print('=== 目标层条目 ===')
want = {'39', '41', '45', '43', '1', '0', 39, 41, 45, 43, 1, 0}
for r in rows:
    fl = r.get('floor')
    if fl in want or str(fl) in {'39', '41', '45', '43', '1', '0'}:
        print(' ', r)
