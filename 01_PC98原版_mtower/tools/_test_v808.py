# -*- coding: utf-8 -*-
"""_test_v808.py —— V80-8 49F 封印链真实验证（绕行避开 4 斜角警卫）

入口状态 = V80-8 前半终态：49F(6,6) HP3135 A233 D322 G1489 钥7/3/0
路线设计（斜角 (5,2)(7,2)(5,4)(7,4) 一格不踩）：
  打(6,4): (6,6)→(6,5)→(6,4)
  打(5,3): (6,5)→(5,5)→(4,5)→(4,4)→(4,3)→打(5,3)      ← 经 (4,5) 绕开 (5,4)
  打(6,2): (4,3)→(4,2)→(4,1)→(5,1)→(6,1)→打(6,2)      ← 经 y1 顶行绕开 (5,2)
  打(7,3): (6,1)→(7,1)→(8,1)→(8,2)→(8,3)→打(7,3)      ← 经 x8 列绕开 (7,2)
  打ゼノ:  (8,3)→(8,4)→(8,5)→(7,5)→(6,5)→(6,4)→打(6,3)
"""
import os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

def st(w):
    h = w.hero
    return ('HP%-6d A%-4d D%-4d G%-5d %dF(%d,%d) 钥%d/%d/%d'
            % (h.hp, h.atk, h.dfn, h.gold, h.f, h.x, h.y,
               h.keys['y'], h.keys['b'], h.keys['r']))

def walk(w, seq, tag):
    """seq: [(x,y,desc), ...] 逐格手动步进（贴脸攻击格）"""
    h = w.hero
    for (tx, ty, desc) in seq:
        assert h.f == 49, '不在49F'
        dx, dy = tx - h.x, ty - h.y
        assert abs(dx) + abs(dy) == 1, '非相邻步 %s -> %s' % ((h.x, h.y), (tx, ty))
        log = w.move(dx, dy)
        bad = [l for l in log if any(t in l for t in ('blocked', '打不动', '打不过', '不可通行', '无黄', '无蓝', '无红'))]
        if bad:
            print('  !! %s 失败: %s' % (desc, bad[0]))
            return False
        print('  %-34s %s' % (desc, st(w)))
        for l in log[1:]:
            print('      · ' + l)
    return True

def main():
    w = M.World.new()
    h = w.hero
    # V80-8 前半终态（真实模拟值）
    h.hp, h.atk, h.dfn, h.gold = 3135, 233, 322, 1489
    h.keys['y'], h.keys['b'], h.keys['r'] = 7, 3, 0
    h.items.add(M.SACRED_SHIELD)
    # 模拟已到达 49F：入层事件已触发，英雄站在 (6,6)
    h.f, h.x, h.y = 49, 6, 6
    w.apply_floor_events(49)
    assert w.at(49, 6, 3) == M.SEAL_TARGET, 'ゼノ未登场'

    A, D = h.atk, h.dfn
    # obj58 魔法警卫 230/450/100
    per = A - 100
    t = math.ceil(230 / per)
    loss = (450 - D)
    print('警卫战损预估: per=%d t=%d 被击=%d → 每只 -%d' % (per, t, loss, loss * (t - 1)))

    print('=== ① 打 (6,4) 正方向警卫 ===')
    if not walk(w, [(6, 5, '到(6,5)'), (6, 4, '打警卫(6,4)')], 's1'): return 1

    print('=== ② 绕行打 (5,3)：经(5,5)(4,5)(4,4) 避开(5,4) ===')
    if not walk(w, [
        (6, 5, '回(6,5)'), (5, 5, '到(5,5)'),
        (4, 5, '到(4,5) ←绕行关键格(非斜角)'),
        (4, 4, '到(4,4) ←绕行关键格(非斜角)'),
        (4, 3, '到(4,3) 攻击位'),
        (5, 3, '打警卫(5,3)'),
    ], 's2'): return 1

    print('=== ③ 顶行绕行打 (6,2)：避开(5,2) ===')
    if not walk(w, [
        (4, 3, '回(4,3)'), (4, 2, '到(4,2)'), (4, 1, '到(4,1)'),
        (5, 1, '到(5,1) ←顶行(非斜角)'), (6, 1, '到(6,1) 攻击位'),
        (6, 2, '打警卫(6,2)'),
    ], 's3'): return 1

    print('=== ④ 东列绕行打 (7,3)：避开(7,2) ===')
    if not walk(w, [
        (6, 1, '回(6,1)'), (7, 1, '到(7,1) ←顶行'), (8, 1, '到(8,1)'),
        (8, 2, '到(8,2) ←东列'), (8, 3, '到(8,3) 攻击位'),
        (7, 3, '打警卫(7,3)'),
    ], 's4'): return 1

    print('封印判据: seal49 =', w.seal49, ' OA[57][10:13] =', M.OA[57][10:13])
    print('  edges:', [(p, w.at(49, *p)) for p in M.F49_SEAL_EDGES])
    print('  corners:', [(p, w.at(49, *p)) for p in M.F49_SEAL_CORNERS])
    if not w.seal49:
        print('  !! 封印未成立'); return 1
    assert M.OA[57][10:13] == [800, 500, 100], '封印数值不对'

    print('=== ⑤ 打ゼノ(6,3)（封印后 800/500/100） ===')
    if not walk(w, [
        (8, 3, '回(8,3)'), (8, 4, '到(8,4)'), (8, 5, '到(8,5)'),
        (7, 5, '到(7,5)'), (6, 5, '到(6,5)'), (6, 4, '到(6,4) 攻击位'),
        (6, 3, '★打ゼノ(6,3)'),
    ], 's5'): return 1

    print('zeno49_dead =', w.zeno49_dead)
    if not w.zeno49_dead:
        print('  !! ゼノ未击败'); return 1

    print('=== 战后摆出 ===')
    for p, want in (((5,5),78),((6,5),78),((7,5),78),
                    ((2,4),82),((3,4),82),((4,4),82),
                    ((8,4),85),((9,4),85),((10,4),85),
                    ((5,2),28),((7,2),109),((6,3),69)):
        got = w.at(49, *p)
        flag = 'OK' if got == want else '!! 期望%d' % want
        print('  (%d,%d)=%d %s' % (p[0], p[1], got, flag))
    print()
    print('=== V80-8 全链终态 ===')
    print(' ', st(w))
    return 0

if __name__ == '__main__':
    sys.exit(main())
