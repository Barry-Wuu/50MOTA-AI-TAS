# -*- coding: utf-8 -*-
"""从「农取 → 11F 钥匙 → 12F 资源 → 13/14/15F 商店买蓝钥」终态出发，
   做受限 BFS，盘出所有可达格中仍未捡的 HP 补给 / 攻防晶石，并给出到各格的最大 HP。
   用法: python3 probe15.py [楼层...]
"""
import sys, collections
import mota_core as M
import state as S
import plan as P

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

GOALS = ['10', '9', '8', '7', '6', '5', '4', '3', '3(2,2)', '3(2,1)', '3(1,1)',
         '2', '2(3,4)', '2(4,4)', '2(3,5)', '1', '1(10,11)', '1(1,11)', '1(1,10)',
         '1(1,3)', '1(8,4)', '1(7,3)', '1(7,4)', '1(8,3)', '1(1,6)', '1(3,10)',
         '1(3,11)', '1(2,11)', '2', '3', '4', '4(11,2)', '4(1,2)', '4(9,2)',
         '5', '5(3,9)', '5(1,9)', '5(4,9)', '6', '6(4,9)', '7', '8', '9', '10',
         '11', '11(4,10)', '11(1,11)', '11(2,11)', '11(3,11)', '11(4,11)',
         '11(1,10)', '12', '12(5,10)', '12(7,10)', '13', '14', '15', '15(11,11)']


def main():
    floors = set(int(a) for a in sys.argv[1:]) or set(range(1, 17))
    w0 = S.replay()
    print('CSV 终态:', P.st(w0.hero), flush=True)
    w, err = S.apply_seq(w0, [S.parse_goal(g) for g in GOALS])
    if err:
        print('序列中断:', err, flush=True)
    print('序列终态:', P.st(w.hero), flush=True)

    best = {}          # (f,x,y) -> (maxhp, steps)
    q = collections.deque([(w, 0)])
    seen = {P._key(w)}
    n = 0
    cap = 400000
    while q and n < cap:
        cur, d = q.popleft(); n += 1
        for dx, dy in DIRS:
            t = cur.clone()
            lg = t.move(dx, dy)
            if M.blocked(lg) or t.hero.hp <= 0:
                continue
            if t.hero.f not in floors:
                continue
            k = P._key(t)
            if k in seen:
                continue
            seen.add(k)
            pos = (t.hero.f, t.hero.x, t.hero.y)
            if pos not in best or best[pos][0] < t.hero.hp:
                best[pos] = (t.hero.hp, d + 1)
            q.append((t, d + 1))
    print('展开 %d 状态；可达 %d 格，楼层 %s' % (n, len(best), sorted(set(p[0] for p in best))), flush=True)

    base_cleared = set(w.cleared)          # 序列终态已捡/已清的格子，排除掉

    print('\n=== 可达且【尚未捡】的 HP/攻防补给 ===')
    tot = 0
    rows = []
    for (f, x, y), (hp, d) in sorted(best.items()):
        o = M.obj_raw(f, x, y)
        if not o or (f, x, y) in base_cleared:
            continue
        ty = M.TYPE.get(M.oatr(o, 3))
        if ty not in ('STATUS', 'ITEM'):
            continue
        dh, da, dd = M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12)
        if dh <= 0 and da <= 0 and dd <= 0:
            continue
        rows.append((f, x, y, dh, da, dd, hp, d))
        tot += dh
    for f, x, y, dh, da, dd, hp, d in rows:
        print('  %2dF(%2d,%2d) HP%+d ATK%+d DEF%+d   到达时 HP%d (%d 步)  %s'
              % (f, x, y, dh, da, dd, hp, d, M.oname(M.obj_raw(f, x, y))[:16]))
    print('  可达补给 HP 合计 %d；ATK+%d DEF+%d'
          % (tot, sum(r[4] for r in rows), sum(r[5] for r in rows)))

    print('\n=== 关键目标可达性 ===')
    for f, x, y, lab in [(11, 2, 2, '11F 银盾'), (11, 1, 7, '11F +400'),
                         (11, 8, 11, '11F +400(右)'), (15, 6, 1, '15F 上梯'),
                         (15, 9, 1, '15F 盗贼'), (12, 9, 5, '12F +100'),
                         (12, 10, 6, '12F DEF+2'), (16, 6, 2, '16F 落点'),
                         (17, 2, 2, '17F 银剑')]:
        if (f, x, y) in best:
            print('  ✅ %-12s %2dF(%d,%d) 可达 HP%d (%d 步)' % (lab, f, x, y, best[(f, x, y)][0], best[(f, x, y)][1]))
        else:
            print('  ❌ %-12s %2dF(%d,%d) 不可达' % (lab, f, x, y))


if __name__ == '__main__':
    main()
