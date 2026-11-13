# -*- coding: utf-8 -*-
"""_test_50f_chain.py —— 终局事件链自测（只验事件逻辑，不做寻路）

覆盖：49F 十字封印 → ゼノ战后演出 → 26F 假公主挖墙 → 24F ending() 传送
      → 50F 小偷对话/Zeno2 变身 → 真魔王战通关
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M


def st(w):
    h = w.hero
    return ('HP%-6d A%-4d D%-4d G%-5d %dF(%d,%d) 钥%d/%d/%d'
            % (h.hp, h.atk, h.dfn, h.gold, h.f, h.x, h.y,
               h.keys['y'], h.keys['b'], h.keys['r']))


def put(w, f, x, y):
    w.hero.f, w.hero.x, w.hero.y = f, x, y


def step(w, dx, dy, tag):
    log = w.move(dx, dy)
    print('  %-30s %s' % (tag, st(w)))
    for line in log:
        print('      · ' + line)
    return log


def main():
    w = M.World.new()
    h = w.hero
    h.hp, h.atk, h.dfn, h.gold = 20000, 400, 450, 5000
    h.keys['y'], h.keys['b'], h.keys['r'] = 10, 3, 8
    h.items.add(M.SACRED_SHIELD)          # 神盾(44F obj39)：免魔法夹击，隔离测试封印逻辑

    print('=== 49F 十字封印 ===')
    put(w, 49, 1, 11)
    w.apply_floor_events(49)
    print('  进层 (6,3)=%d (6,2)=%d (5,2)=%d (5,5)=%d(应为0)'
          % (w.at(49, 6, 3), w.at(49, 6, 2), w.at(49, 5, 2), w.at(49, 5, 5)))
    assert w.at(49, 6, 3) == M.SEAL_TARGET, 'ゼノ未登场'
    assert w.at(49, 5, 5) == 0, '战后道具被提前白送'

    for (gx, gy), (ax, ay) in (((6, 2), (6, 1)), ((6, 4), (6, 5)),
                               ((5, 3), (4, 3)), ((7, 3), (8, 3))):
        put(w, 49, ax, ay)
        step(w, gx - ax, gy - ay, '打正方向警卫(%d,%d)' % (gx, gy))

    print('  封印 seal49 =', w.seal49, ' obj57 四维 =', M.OA[57][10:13])
    assert w.seal49, '十字封印未触发'
    assert M.OA[57][10:13] == [800, 500, 100], '封印数值不对'

    put(w, 49, 6, 4)
    step(w, 0, -1, '打ゼノ(6,3)')
    print('  zeno49_dead =', w.zeno49_dead)
    for c, o in (((5, 5), 78), ((2, 4), 82), ((8, 4), 85), ((5, 2), 28), ((7, 2), 109)):
        print('  战后格 %s = %d (期望 %d)' % (c, w.at(49, *c), o))
        assert w.at(49, *c) == o, '战后演出道具缺失'

    print()
    print('=== 26F 假公主 → 挖开 24F ===')
    put(w, 26, 6, 8)
    step(w, 0, -1, '开红门(6,7)')          # 开门只扣钥匙，人不动
    step(w, 0, -1, '踩上(6,7)')
    print('  story26 =', w.story26,
          ' 24F(6,0)tile =', w.ter_over.get((24, 6, 0)),
          '(6,2..4) =', [w.ter_over.get((24, 6, y)) for y in (2, 3, 4)],
          '(5,1)(7,1) =', [w.ter_over.get((24, x, 1)) for x in (5, 7)])
    assert w.story26, '26F 剧情未触发'
    assert w.ter_over.get((24, 6, 0)) == 1, '24F(6,0) 未挖开'

    print()
    print('=== 24F(6,0) → ending() → 50F(6,7) ===')
    put(w, 24, 6, 1)
    step(w, 0, -1, '踩 (6,0)')
    print('  落点 = %dF(%d,%d)' % (h.f, h.x, h.y), ' story24_end =', w.story24_end)
    assert (h.f, h.x, h.y) == M.F50_LAND, '未传送到 50F(6,7)'
    print('  50F(6,5) =', w.at(50, 6, 5), '(期望 57)  对话计数 =', w.f50_talk)
    assert w.at(50, 6, 5) == M.SEAL_TARGET, 'Zeno2 未变身'
    print('  24F 已还原: (6,0)=%s (6,2)=%s (5,1)=%s'
          % (w.ter_over.get((24, 6, 0)), w.ter_over.get((24, 6, 2)), w.ter_over.get((24, 5, 1))))

    print()
    print('=== 50F 真魔王战 ===')
    step(w, 0, -1, '走到(6,6)')
    step(w, 0, -1, '打真魔王(6,5)')
    print('  won50 =', w.won50, '  ', st(w))
    assert w.won50, '未判定通关'

    print()
    print('全部断言通过 ✅')


if __name__ == '__main__':
    main()
