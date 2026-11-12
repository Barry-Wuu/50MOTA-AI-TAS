# -*- coding: utf-8 -*-
"""重放 manual.PLAN 后，列出 1-11F 剩余物件（供手工排 1 区收尾路线）"""
import manual as U
import mota_core as M

U.execute(verbose=False)
W = U.W
h = W.hero
print('当前: HP%d A%d D%d G%d 钥%d/%d/%d %dF(%d,%d)' % (
    h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y))
for f in range(1, 12):
    print('\n=== %dF ===' % f)
    rows = []
    for y in range(13):
        for x in range(13):
            o = W.at(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            if ty == 'MONSTER':
                desc = '%s(%d/%d/%d) g%d' % (M.oname(o), M.oatr(o, 10), M.oatr(o, 11),
                                             M.oatr(o, 12), M.oatr(o, 13))
            else:
                desc = '%s obj%d' % (M.oname(o)[:14], o)
            rows.append('  (%2d,%2d) %-6s %s' % (x, y, ty, desc))
    print('\n'.join(rows) if rows else '  (空)')
