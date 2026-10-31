# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
w = M.World.new()

def oid(f, x, y):
    o = w.at(f, x, y)
    return o

for f in [8, 10]:
    print('==== %dF 物件 ====' % f)
    for y in range(13):
        row = []
        for x in range(13):
            o = w.at(f, x, y)
            t = w.terrain_at(f, x, y)
            if t == 1: row.append('##')
            elif t == 2: row.append('SS')
            elif o == 0: row.append('..')
            else:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                row.append('%2d' % o)
        print('%3d ' % y + ' '.join(row))
    print()

print('==== 怪物/物件 属性 ====')
seen = set()
for f in [8, 10]:
    for y in range(13):
        for x in range(13):
            o = w.at(f, x, y)
            if o and o not in seen:
                seen.add(o)
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                nm = M.oname(o)[:14]
                print('obj%-3d %-4s %-14s a3=%s a4=%s hp=%s atk=%s def=%s gold=%s' % (
                    o, ty, nm, M.oatr(o,3), M.oatr(o,4), M.oatr(o,10), M.oatr(o,11), M.oatr(o,12), M.oatr(o,13)))
