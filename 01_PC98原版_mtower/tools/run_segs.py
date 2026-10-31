# -*- coding: utf-8 -*-
"""run_segs.py —— 执行 segs_route.py 的翻译表，逐层验证

职责边界：
  · 路线由 segs_route.py 决定（人工翻译自攻略）
  · 本文件只做「A 格走到 B 格」的直线导航 + 状态记录
  · 每步落格后与预期状态对照，任何 blocked / 打不过 立即报错

用法：
  python tools/run_segs.py            # 从 1F 起点跑序章，验证到 4F
"""
import sys, os, io, csv
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M
import segs_route

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
REC = []


def st(h):
    return 'HP%-5d A%-3d D%-3d G%-5d 钥%d/%d/%d %dF(%2d,%2d)' % (
        h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y)


def _passable(w, f, nx, ny):
    if not (1 <= nx <= 11 and 1 <= ny <= 11):
        return False
    # 楼梯格不进层内 BFS（踩上去会换层，破坏位置）
    if w.terrain_at(f, nx, ny) in (1, 2):
        return False
    o = w.at(f, nx, ny)
    if not o:
        return True
    ty = M.TYPE.get(M.oatr(o, 3))
    if o in M.KEY_OF or ty in ('STATUS', 'ITEM', 'NORMAL', 'SCORE', 'MESSAGE'):
        return True
    if ty == 'DOOR':
        col = M.DOOR_OF.get(o)
        return col is not None and w.hero.keys[col] > 0
    if ty == 'MONSTER':
        r = w.battle(o)
        return r is not None and r[0] < w.hero.hp
    return False


def _step(w, d):
    """走一步；开门不移动则补一步。返回 (ok, log)"""
    broke = ('blocked', '打不动', '打不过', '无', '不可通行')
    bx, by = w.hero.x, w.hero.y
    lg = w.move(*d)
    if lg and any(t in lg[0] for t in broke):
        return False, lg
    if (w.hero.x, w.hero.y) == (bx, by) and lg and '开' in lg[0]:
        lg2 = w.move(*d)
        if lg2 and any(t in lg2[0] for t in broke):
            return False, lg2
        lg = lg + lg2
    return True, lg


def goto(w, tx, ty, label=''):
    """BFS 找最短路（只走可通行格），逐步执行。"""
    h = w.hero
    start = (h.x, h.y)
    if start == (tx, ty):
        return True
    prev = {start: None}
    q = deque([start])
    found = False
    while q:
        c = q.popleft()
        if c == (tx, ty):
            found = True
            break
        for d in DIRS:
            n = (c[0] + d[0], c[1] + d[1])
            if n in prev:
                continue
            if not _passable(w, h.f, *n):
                continue
            prev[n] = c
            q.append(n)
    if not found:
        print('  !! 不可达 (%d,%d) from %s' % (tx, ty, start))
        return False
    seq = []
    cur = (tx, ty)
    while cur != start:
        seq.append(cur)
        cur = prev[cur]
    seq.reverse()
    for (nx, ny) in seq:
        ok, lg = _step(w, (nx - w.hero.x, ny - w.hero.y))
        if not ok:
            print('  !! 卡在 %s: %s' % (st(w.hero), lg))
            return False
        REC.append((w.hero.f, w.hero.x, w.hero.y, w.hero.hp, w.hero.atk, w.hero.dfn,
                    w.hero.gold, w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
                    ';'.join(lg)[:80] if lg else '', '%d,%d' % (w.hero.x - nx, w.hero.y - ny)))
    print('  %-22s %s' % (label or '(%d,%d)' % (tx, ty), st(w.hero)))
    return True


def stair(w, sx, sy, label=''):
    """走到楼梯邻格再踏上。"""
    h = w.hero
    for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        ax, ay = sx + d[0], sy + d[1]
        if not (1 <= ax <= 11 and 1 <= ay <= 11):
            continue
        if not _passable(w, h.f, ax, ay):
            continue
        if not goto(w, ax, ay):
            continue
        ok, lg = _step(w, (sx - w.hero.x, sy - w.hero.y))
        if not ok:
            print('  !! 上楼梯失败: %s' % lg)
            return False
        REC.append((w.hero.f, w.hero.x, w.hero.y, w.hero.hp, w.hero.atk, w.hero.dfn,
                    w.hero.gold, w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
                    ';'.join(lg)[:80] if lg else '', 'stair'))
        print('  %-22s %s' % (label, st(w.hero)))
        return True
    print('  !! 楼梯 %dF(%d,%d) 无可达入口' % (h.f, sx, sy))
    return False


def run_segs(w, f, segs, tag=''):
    for (x, y, lab) in segs:
        if not goto(w, x, y, '%s(%d,%d) %s' % (tag or '%dF' % f, x, y, lab)):
            return False
    return True


def main():
    w = M.World.new()
    h = w.hero
    h.f, h.x, h.y = 1, 6, 11
    h.hp, h.atk, h.dfn, h.gold = 1000, 100, 100, 0
    print('起点:', st(h))

    S = segs_route.SEGS_PRELUDE
    print('\n--- 1F ---')
    if not run_segs(w, 1, S[1]): return 1
    if not stair(w, 1, 1, '1F(1,1)->2F'): return 1

    print('\n--- 2F 下行 x1 竖列 ---')
    if not run_segs(w, 2, S[2]): return 1
    if not stair(w, 1, 11, '2F(1,11)->3F'): return 1

    print('\n--- 3F 第一次（触发剧本）---')
    if not run_segs(w, 3, S[3]): return 1
    ok, lg = _step(w, (5 - w.hero.x, 9 - w.hero.y))
    print('  踩 (5,9):', ';'.join(lg) if lg else '', '->', st(w.hero))
    if not ok: return 1

    print('\n--- 2F 牢房越狱 ---')
    if not run_segs(w, 2, S[2.5], '2F越狱'): return 1
    # STAIRS[2]=((1,11),(1,1)) → up=(1,11) 去 3F，down=(1,1) 回 1F
    if not stair(w, 1, 11, '2F(1,11)->3F'): return 1

    print('\n--- 3F 第二次（补蓝药+钥匙）---')
    if not run_segs(w, 3, S['3b'], '3F二次'): return 1
    if not stair(w, 11, 11, '3F(11,11)->4F'): return 1

    print('\n到达 4F:', st(w.hero))
    return 0


if __name__ == '__main__':
    sys.exit(main())
