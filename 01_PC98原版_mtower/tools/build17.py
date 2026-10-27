#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build17.py —— 以提交的 1F→11F 路线为地基，按已建立的 11F→17F 策略（扫荡收资源 +
12F 祭坛堆攻防 + 11F 银盾 + 15F 盗贼暗道绕大ダコ + 17F 银剑）构建并验证完整路线，
最终写出 route_plan.csv（1F→17F，银盾+银剑齐全）。引擎逐步验证，失败即报错。
"""
import sys
import csv
import mota_core as M
import plan as P
import state as S
import probe15 as PR

LOG = P.LOG
DIRS = P.DIRS


def st(h):
    return P.st(h)


def seg(w, tgt, max_exp=800000):
    w2, path = P.walk(w, tgt, max_exp)
    if w2 is None:
        return None, '✗ 目标 %s 失败：%s' % (tgt, path)
    cur = w
    for dx, dy, lab, _lg in path:
        cur = cur.clone(); lg = cur.move(dx, dy); hh = cur.hero
        LOG.append((len(LOG) + 1, hh.f, hh.x, hh.y, lab, ' '.join(lg),
                    hh.hp, hh.atk, hh.dfn, hh.gold,
                    hh.keys['y'], hh.keys['b'], hh.keys['r']))
    return w2, None


def altar_boost(w, f, target_atk=58, max_hits=8):
    """到 f 层祭坛反复献祭（atk 优先），把 ATK 堆到 target_atk 或金不足为止。"""
    w.altar_policy = 'atk'
    cell = next(((ax, ay) for (af, ax, ay) in M.ALTAR_CELLS if af == f), None)
    if cell is None:
        return w
    ax, ay = cell
    guard = 0
    while w.hero.atk < target_atk and guard < max_hits:
        c = M.altar_cost(w.altar_k)
        if w.hero.gold < c:
            break
        w2, err = seg(w, (f, ax, ay))
        if w2 is None:
            print('  祭坛中断:', err); break
        w = w2; guard += 1
        print('  祭坛第%d次 → %s (金%d)' % (guard, st(w.hero), w.hero.gold))
    return w


def main():
    # 把提交的 1F→11F 地基路线原样灌入 LOG（连续编号），再接延伸段 → 一条 1F→17F 完整路线
    with open('/tmp/committed_route.csv', encoding='utf-8') as fp:
        for r in csv.reader(fp):
            if r and r[0].isdigit():
                LOG.append(tuple(r))

    w = S.replay('/tmp/committed_route.csv')
    print('地基 11F:', st(w.hero))

    # 1) 已建立的扫荡序列（收资源 + 到 15F，并确认 11F 银盾可达）
    #    逐目标用 seg（每步写 LOG），保证整条 1F→17F 连续可回放
    goals = [S.parse_goal(g) for g in PR.GOALS]
    for gi, g in enumerate(goals):
        w, err = seg(w, g)
        if err:
            print('✗ 扫荡目标 %s(%d/%d): %s' % (g, gi, len(goals), err)); sys.exit(1)
    print('扫荡终态 15F:', st(w.hero))

    # 2) 回到 12F 祭坛堆 ATK
    w, err = seg(w, 12)
    if err:
        print('✗ 去 12F:', err); sys.exit(1)
    w = altar_boost(w, 12, target_atk=58)
    print('祭坛后:', st(w.hero))

    # 3) 试 17F 银剑(17,2,2)
    w, err = seg(w, 17)
    if err:
        print('✗ 到 17F 层:', err)
    else:
        w, err = seg(w, (17, 2, 2))
        if err:
            print('✗ 17F 银剑:', err)
        else:
            print('✓ 17F 银剑:', st(w.hero))
            # 4) 回头 11F 银盾(11,2,2)
            w, err = seg(w, 11)
            if err:
                print('✗ 回 11F:', err)
            else:
                w, err = seg(w, (11, 2, 2))
                if err:
                    print('✗ 11F 银盾:', err)
                else:
                    print('✓ 11F 银盾:', st(w.hero))

    print('\n终态:', st(w.hero))
    with open('route_plan.csv', 'w', newline='', encoding='utf-8') as fp:
        cw = csv.writer(fp)
        cw.writerow(['step', 'floor', 'x', 'y', 'key', 'event', 'hp', 'atk', 'def', 'gold', 'ky', 'kb', 'kr'])
        cw.writerows(LOG)
    print('已写 route_plan.csv（%d 步）' % len(LOG))


if __name__ == '__main__':
    main()
