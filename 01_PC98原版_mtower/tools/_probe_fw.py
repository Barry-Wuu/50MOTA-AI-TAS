# -*- coding: utf-8 -*-
# 检查 mota_core 中 39F 的 FLOOR_WRITES 与 DYNEV 条目
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

print('=== 39F FLOOR_WRITES ===')
for (x, y, o) in M.FLOOR_WRITES.get(39, []):
    print('  (%d,%d)=obj%d %s' % (x, y, o, M.oname(o)))

print()
print('=== 39F TERR_WRITES ===')
for (x, y, to) in M.TERR_WRITES.get(39, []):
    print('  (%d,%d) terrain→%d' % (x, y, to))

print()
print('=== 45F FLOOR_WRITES ===')
for (x, y, o) in M.FLOOR_WRITES.get(45, []):
    print('  (%d,%d)=obj%d %s' % (x, y, o, M.oname(o)))

print()
print('=== 43F/44F/41F FLOOR_WRITES ===')
for f in (41, 43, 44):
    print('--- %dF ---' % f)
    for (x, y, o) in M.FLOOR_WRITES.get(f, []):
        print('  (%d,%d)=obj%d %s' % (x, y, o, M.oname(o)))

print()
print('=== obj106/107/108 定义 ===')
for oid in (106, 107, 108):
    print('  obj%d type=%s name=%s' % (oid, M.oatr(oid, 3), M.oname(oid)))
