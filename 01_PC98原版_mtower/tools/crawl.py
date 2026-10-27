# -*- coding: utf-8 -*-
"""完整通关走法（1F → 11F），按人类攻略意图，逐层「顺路吃资源 → 上楼」。

对应 magic_tower1_walkroute.md「一区域」：
  不去商店加攻防；铁剑(5F) → 铁盾(9F)；剑盾宝石全拿，优先蓝宝石（防御）
  10F 打 BOSS 才能生 11F 上行梯

关键真实约束（全部来自提取数据）：
  · 8F(10,2) 红钥 → 10F(6,9) 红门是 BOSS 唯一入口
  · 9F(10,5) 暗墙 → 铁盾 DEF+10（不必打门番Ｃ）
  · 10F(6,11) 只在 BOSS 死后才变上行梯
"""
import collections
import sys
import layer2 as L2
import mota_core as M

SEG = []


def st(w):
    h = w.hero
    return '%2dF(%2d,%2d) HP%-4d ATK%-3d DEF%-3d G%-3d 钥%d/%d/%d' % (
        h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
        h.keys['y'], h.keys['b'], h.keys['r'])


def go(tag, w, goal, max_exp=400000):
    f = w.hero.f
    r = L2.plan_layer(f, w, goal, max_exp=max_exp, cross=True)
    if r[0] != 'ok':
        print('  ✗ %-22s %s exp=%d' % (tag, r[0], r[1]))
        return None
    w2 = r[2][0]
    tr = L2.trace(r[2])
    SEG.append((tag, tr))
    print('  ✓ %-22s → %-56s [%d 步]' % (tag, st(w2), len(tr) - 1))
    return w2


def g_floor(n):
    return lambda w: w.hero.f == n


def g_pick(f, x, y):
    return lambda w: (f, x, y) in w.cleared


def bfs_any(tag, w, goal, cap=300000):
    seen = {(w.hero.f, w.hero.x, w.hero.y)}
    q = collections.deque([(w, [])])
    n = 0
    while q:
        x, path = q.popleft()
        n += 1
        if n > cap:
            return None
        if goal(x):
            SEG.append((tag, path))
            print('  ✓ %-22s → %-56s [%d 步]' % (tag, st(x), len(path)))
            return x
        for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            w2 = x.clone()
            lg = w2.move(*d)
            if M.blocked(lg) or w2.hero.hp <= 0:
                continue
            k = (w2.hero.f, w2.hero.x, w2.hero.y)
            if k in seen:
                continue
            seen.add(k)
            q.append((w2, path + [d]))
    return None


# 每层顺路资源点：(x, y, 类别)
#   hp=血瓶 / key=钥匙 / atk=红晶 / def=蓝晶 / shield=铁盾 / rkey=红钥 / bkey=蓝钥
# 顺序＝优先级：先把血补足（血见底后什么都做不了），再拿钥匙，最后宝石。
PICK = {
    3: [(2, 2, 'hp'), (4, 1, 'key'), (6, 1, 'key'), (5, 2, 'key'), (4, 3, 'key'),
        (6, 3, 'key'), (5, 3, 'key'), (2, 1, 'def')],
    4: [(1, 2, 'hp'), (11, 2, 'hp'), (9, 2, 'key'), (5, 10, 'key'), (5, 11, 'key'),
        (3, 11, 'key'), (6, 1, 'key'), (3, 2, 'key'), (2, 1, 'key'), (7, 10, 'atk')],
    5: [(3, 9, 'hp'), (6, 2, 'key'), (8, 3, 'key'), (9, 3, 'key'), (8, 4, 'key'),
        (9, 4, 'key'), (1, 5, 'key'), (1, 6, 'key'), (2, 9, 'key'),
        (1, 9, 'def'), (11, 11, 'atk')],
    6: [(8, 3, 'hp'), (8, 11, 'hp'), (9, 11, 'hp'), (6, 6, 'key'), (3, 1, 'key'),
        (4, 1, 'key'), (3, 2, 'key'), (4, 2, 'key'), (9, 1, 'key'), (4, 9, 'def'),
        (8, 4, 'shopb')],
    7: [(3, 2, 'hp'), (9, 3, 'hp'), (9, 9, 'hp'), (7, 11, 'hp'),
        (6, 1, 'shopy'),
        (9, 1, 'key'), (9, 2, 'key'), (5, 10, 'key'), (5, 11, 'key'),
        (9, 10, 'key'), (9, 11, 'key'), (3, 1, 'atk')],
    8: [(9, 3, 'hp'), (11, 3, 'hp'), (1, 5, 'hp'), (8, 10, 'hp'),
        (10, 2, 'rkey'), (9, 1, 'key'), (11, 1, 'key'), (3, 4, 'key'), (4, 4, 'key'),
        (5, 4, 'key'), (5, 10, 'key'), (4, 11, 'key'), (7, 11, 'key'),
        (7, 10, 'bkey'), (4, 10, 'atk'), (5, 11, 'def')],
    9: [(11, 1, 'hp'), (2, 10, 'hp'), (11, 11, 'hp'),
        (2, 2, 'key'), (2, 4, 'key'), (5, 4, 'key'), (7, 4, 'key'), (1, 7, 'key'),
        (5, 7, 'key'), (9, 9, 'key'), (9, 7, 'shield'), (1, 5, 'def'), (6, 5, 'atk')],
    10: [(1, 4, 'hp'), (3, 4, 'hp'), (11, 11, 'hp'), (9, 4, 'key'), (11, 4, 'key'),
         (2, 6, 'def'), (10, 6, 'atk')],
}

# 亏血上限：钥匙/宝石是长期收益，允许适度亏，但不能像 3F 蓝宝石那样 700 血换 1 点防御
LOSS_CAP = {'key': 120, 'bkey': 200, 'atk': 120, 'def': 120, 'shield': 9999, 'rkey': 9999,
            'shopb': 9999, 'shopy': 9999}


def eat(f, w, hp_floor=25, rounds=6):
    """多遍扫资源点：每遍按 PICK 顺序尝试，直到一整遍毫无进展。

    为什么多遍：血瓶常在小怪/门之后，必须先靠前一遍拿到钥匙才够得着；
    单遍会把「现在够不着」当成「永远够不着」。
    """
    before = (w.hero.hp, w.hero.atk, w.hero.dfn, dict(w.hero.keys))
    for _ in range(rounds):
        got = 0
        for (x, y, kind) in PICK.get(f, []):
            if (f, x, y) in w.cleared:
                continue
            r = L2.plan_layer(f, w, g_pick(f, x, y), max_exp=400000, cross=True)
            if r[0] != 'ok':
                continue
            w2 = r[2][0]
            d = w2.hero.hp - w.hero.hp
            if d < 0:
                cap = LOSS_CAP.get(kind, 0)
                if -d > cap or w2.hero.hp < hp_floor:
                    continue
            if w2.hero.hp < hp_floor:
                continue
            tr = L2.trace(r[2])
            SEG.append(('%dF 拾(%d,%d)' % (f, x, y), tr))
            print('  ✓ %-22s → %-56s [%d 步] HP%+d' % (
                '%dF 拾(%d,%d)' % (f, x, y), st(w2), len(tr) - 1, d))
            w = w2
            got += 1
        if not got:
            break
    after = (w.hero.hp, w.hero.atk, w.hero.dfn, dict(w.hero.keys))
    print('    [%dF 净变化 HP%+d ATK%+d DEF%+d 钥%s→%s]' % (
        f, after[0] - before[0], after[1] - before[1], after[2] - before[2],
        before[3], after[3]))
    return w


if __name__ == '__main__':
    w = M.World.new()
    print('起点  ' + st(w))
    w = go('1F → 2F', w, g_floor(2))
    w = go('2F → 3F', w, g_floor(3))
    w = bfs_any('3F 踩陷阱(扒装)', w, lambda x: x.hero.f == 2 and x.hero.hp == 400)
    for (x, y) in [(4, 10), (3, 10), (3, 11)]:
        w = go('2F 蓝药(%d,%d)' % (x, y), w, g_pick(2, x, y))
    w = go('2F → 3F', w, g_floor(3))

    for f in (3, 4, 5, 6, 7, 8, 9):
        w = eat(f, w)
        if w is None:
            sys.exit(1)
        w = go('%dF → %dF' % (f, f + 1), w, g_floor(f + 1))
        if w is None:
            print('  !! 断在 %dF 上楼' % f)
            sys.exit(1)

    # 10F：吃资源 → 打 BOSS → 上 11F
    w = eat(10, w)
    w = go('10F ★打 BOSS', w, lambda x: x.boss10)
    if w is None:
        sys.exit(1)
    w = go('10F → 11F', w, g_floor(11))
    print()
    print('终态  ' + st(w) if w else '终态 失败')
