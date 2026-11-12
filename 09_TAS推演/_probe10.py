# -*- coding: utf-8 -*-
"""对比 10F BOSS 击杀前后 10F 物件差异，确认事件生成的真实战利品。"""
import manual as U
import mota_core as M

W = U.W


def snap():
    return {(x, y): W.at(10, x, y) for x in range(1, 12) for y in range(1, 12)}


U.execute(U.PLAN[:-2], verbose=False)   # 执行到 BOSS 前
h = W.hero
print('BOSS 前:', 'HP%d A%d D%d G%d 钥%d/%d/%d %dF(%d,%d)' % (
    h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y))
before = snap()

U.execute(U.PLAN[-2:], verbose=False)   # BOSS + 上行梯
h = W.hero
print('BOSS 后:', 'HP%d A%d D%d G%d 钥%d/%d/%d %dF(%d,%d)' % (
    h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y))

after = snap()
print('\n--- 10F 差异（BOSS 前 -> 后）---')
for (x, y) in sorted(before):
    if before[(x, y)] != after[(x, y)]:
        o0, o1 = before[(x, y)], after[(x, y)]
        print('(%2d,%2d) %-30s -> %-30s' % (x, y,
              '%s obj%d' % (M.oname(o0)[:14], o0) if o0 else '空',
              '%s obj%d' % (M.oname(o1)[:14], o1) if o1 else '空'))

print('\n--- 10F 当前全部非空物件 ---')
for y in range(1, 12):
    for x in range(1, 12):
        o = W.at(10, x, y)
        if o:
            print('(%2d,%2d) obj%-4d %s' % (x, y, o, M.oname(o)))
