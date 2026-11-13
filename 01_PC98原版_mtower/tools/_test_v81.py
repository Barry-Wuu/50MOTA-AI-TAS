# -*- coding: utf-8 -*-
"""_test_v81.py —— V81：35F 打魔龙取雪之结晶 → 13F 用雪之结晶清熔岩 → 神剣 obj34

入口状态 = V80-9 终态：49F(2,4) HP4495 A248 D337 G3729 钥7/3/1
           持有 神盾39 / 屠龙匕109 / 飞行之珠26

要点：
  · 熔岩 obj79 **不可通行**（MTower.java @785 directCheck bl=false，只弹 texts[183]）
    → 13F 神剣 obj34 唯一通路 = 雪之结晶 obj110（itemFlag==11，清四邻各 1 格、不消耗）
  · 魔龙 obj74 1500/600/250/800；带屠龙匕 mult=2：
      A248 → per=246 t=7 战损 1578
      A348 → per=446 t=4 战损  789   ← 先拿神剣再打龙，省 789
    但神剣需要雪之结晶、雪之结晶需要杀魔龙 → 只能 A248 先打龙（1578）
  · 35F (6,5) 雪之结晶 / (5,4)(6,4)(7,4) 蓝药800×3 都在进层事件里静态摆好
"""
import os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

def st(w):
    h = w.hero if hasattr(w, 'hero') else w
    return ('HP%-6d A%-4d D%-4d G%-5d %dF(%2d,%2d) 钥%d/%d/%d'
            % (h.hp, h.atk, h.dfn, h.gold, h.f, h.x, h.y,
               h.keys['y'], h.keys['b'], h.keys['r']))

def orth(w, seq, tag=''):
    """正交步进校验"""
    h = w.hero
    for (tx, ty, desc) in seq:
        assert abs(tx - h.x) + abs(ty - h.y) == 1, '非正交 %s->%s' % ((h.x, h.y), (tx, ty))
        log = w.move(tx - h.x, ty - h.y)
        mark = '!! ' if log and 'blocked' in log[0] else ''
        print('  %s%-40s %s' % (mark, desc or '(%d,%d)' % (tx, ty), st(w)))
        if log and 'blocked' in log[0]:
            print('      !! ' + log[0]); return False
        for l in log:
            if '★' in l or '击杀' in l or '拾取' in l:
                print('      · ' + l)
    return True

def main():
    w = M.World.new()
    h = w.hero
    h.hp, h.atk, h.dfn, h.gold = 4495, 248, 337, 3729
    h.keys['y'], h.keys['b'], h.keys['r'] = 7, 3, 1
    h.items.update({M.SACRED_SHIELD, 109, 26})
    h.f, h.x, h.y = 49, 2, 11       # 49F 下行梯旁（上一段 (2,4) 走回梯旁）

    print('=== 入口:', st(h), '===')
    print('  屠龙匕 109:', 109 in h.items, ' 飞行之珠 26:', 26 in h.items)
    print()

    # ① 珠飞 35F（V53 已到访）
    print('=== ① 珠飞 35F ===')
    lg = w.fly(35)
    print('  ', lg[0][:70] if lg else '')
    if h.f != 35:
        print('  !! 珠飞失败'); return 1
    print('  ', st(h))
    w.apply_floor_events(35)
    print('  雪之结晶(6,5)=%d  魔龙(6,7)=%d  蓝药(5,4)(6,4)(7,4)=%d/%d/%d'
          % (w.at(35, 6, 5), w.at(35, 6, 7), w.at(35, 5, 4), w.at(35, 6, 4), w.at(35, 7, 4)))
    print()

    # ② 打魔龙 (6,7) + 雪之结晶 (6,5)
    print('=== ② 中列北上：打魔龙 → 拿雪之结晶 ===')
    if not orth(w, [
        (6, 9, '到(6,9)'), (6, 8, '到(6,8)'),
        (6, 7, '★魔龙 obj74（屠龙匕×2，A248 per=246 t=7）'),
        (6, 6, '到(6,6)'),
        (6, 5, '★雪之结晶 obj110'),
    ], '35F'): return 1
    if 110 not in h.items:
        print('  !! 雪之结晶未入包'); return 1
    print()

    # ③ 三蓝药
    print('=== ③ 三蓝药 obj77 (+800×3) ===')
    if not orth(w, [
        (6, 4, '★蓝药(6,4)'),
        (5, 4, '★蓝药(5,4)'),
        (6, 4, '回(6,4)'),
        (7, 4, '★蓝药(7,4)'),
    ], '35F'): return 1
    print()

    # ④ 回上行梯 (11,1) 旁
    print('=== ④ 绕到上行梯旁 (10,1) ===')
    print('  35F 中央区 x4..x8 / y1..y11 地形（## 墙 == 梯）:')
    for y in range(1, 12):
        row = []
        for x in range(4, 9):
            o, t = w.at(35, x, y), w.terrain_at(35, x, y)
            row.append('##' if t == 1 else '==' if t == 2 else ('%2d' % o if o else ' .'))
        print('   %2d %s' % (y, ' '.join(row)))
    return 0

if __name__ == '__main__':
    sys.exit(main())