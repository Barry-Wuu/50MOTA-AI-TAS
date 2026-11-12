# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import mota_core as M

d = M.DYNEV
for k, v in d.items():
    print('DYNEV[%r] type=%s len=%s' % (k, type(v), len(v) if hasattr(v, '__len__') else '-'))
    if hasattr(v, '__len__') and len(v):
        print('   sample:', repr(v[0])[:400])
print()
print('=== floor 39/41/45/43/1/0 全部条目 ===')
want = {'39', '41', '45', '43', '1', '0'}
for k, v in d.items():
    if not isinstance(v, (list, tuple)):
        continue
    for r in v:
        if isinstance(r, dict):
            fl = str(r.get('floor'))
            if fl in want:
                print(' [%s] %s' % (k, r))
