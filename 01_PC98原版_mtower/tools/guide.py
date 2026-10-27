# -*- coding: utf-8 -*-
"""把人类攻略翻译成可执行走法：逐层「贪心吃资源 → 上楼」并用真实状态机回放。

对应攻略意图（magic_tower1_walkroute.md 一区域）：
  · 不去商店加攻防
  · 铁剑(5F 已取) → 铁盾(9F)，剑盾宝石全拿
  · 先取蓝宝石（防御）→ 降伤
  · 10F BOSS 要凑够 ATK 破防 + DEF 减伤

实现：层内贪心——每次枚举「尚未拿到的资源点」，用 plan_layer 实算到达后的 HP，
      取「到达后 HP 最高」的那个执行（血瓶净赚 → 自然优先；宝石低代价时也会被选）。
      资源吃不动了，再走上行梯。
"""
import sys
import layer2 as L2
import mota_core as M

# 每层资源点：(x, y, 名称, 类别)  类别 hp=血瓶 atk=红晶 def=蓝晶 key=钥匙
RES = {
    6: [(8, 3, '红药+50', 'hp'), (8, 11, '红药+50', 'hp'), (9, 11, '红药+50', 'hp'),
        (4, 9, '蓝晶DEF+1', 'def'),
        (3, 1, '黄钥', 'key'), (4, 1, '黄钥', 'key'), (3, 2, '黄钥', 'key'), (4, 2, '黄钥', 'key'),
        (6, 6, '黄钥', 'key'), (9, 1, '黄钥', 'key')],
    7: [(3, 2, '红药+50', 'hp'), (9, 3, '红药+50', 'hp'),
        (9, 9, '蓝药+200', 'hp'), (7, 11, '蓝药+200', 'hp'),
        (3, 1, '红晶ATK+1', 'atk'),
        (9, 1, '黄钥', 'key'), (9, 2, '黄钥', 'key'),
        (5, 10, '黄钥', 'key'), (5, 11, '黄钥', 'key'), (9, 10, '黄钥', 'key'), (9, 11, '黄钥', 'key')],
    8: [(9, 3, '蓝药+200', 'hp'), (11, 3, '红药+50', 'hp'), (1, 5, '红药+50', 'hp'), (8, 10, '红药+50', 'hp'),
        (4, 10, '红晶ATK+1', 'atk'), (5, 11, '蓝晶DEF+1', 'def'),
        (10, 2, '红钥', 'rkey'),
        (9, 1, '黄钥', 'key'), (11, 1, '黄钥', 'key'),
        (3, 4, '黄钥', 'key'), (4, 4, '黄钥', 'key'), (5, 4, '黄钥', 'key'),
        (5, 10, '黄钥', 'key'), (4, 11, '黄钥', 'key'), (7, 11, '黄钥', 'key'),
        (7, 10, '蓝钥', 'bkey')],
    9: [(11, 1, '红药+50', 'hp'), (2, 10, '红药+50', 'hp'), (11, 11, '红药+50', 'hp'),
        (1, 5, '蓝晶DEF+1', 'def'), (6, 5, '红晶ATK+1', 'atk'),
        (9, 7, '铁盾DEF+10', 'shield'),
        (2, 2, '黄钥', 'key'), (2, 4, '黄钥', 'key'), (5, 4, '黄钥', 'key'), (7, 4, '黄钥', 'key'),
        (1, 7, '黄钥', 'key'), (5, 7, '黄钥', 'key'), (9, 9, '黄钥', 'key')],
    10: [(1, 4, '蓝药+200', 'hp'), (3, 4, '蓝药+200', 'hp'), (11, 11, '蓝药+200', 'hp'),
         (2, 6, '蓝晶DEF+1', 'def'), (10, 6, '红晶ATK+1', 'atk'),
         (9, 4, '黄钥', 'key'), (11, 4, '黄钥', 'key')],
}
UP = {6: (11, 11), 7: (1, 1), 8: (6, 1), 9: (1, 11), 10: (6, 11)}
SEG = []


def g_floor(f):
    return lambda w: w.hero.f == f


def g_pick(f, x, y):
    return lambda w: (f, x, y) in w.cleared


def g_boss(w):
    return w.boss10


def st(w):
    h = w.hero
    return '%2dF(%2d,%2d) HP%-4d ATK%-3d DEF%-3d G%-3d 钥%d/%d/%d' % (
        h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
        h.keys['y'], h.keys['b'], h.keys['r'])


def try_pick(f, w, x, y, cross=False):
    r = L2.plan_layer(f, w, g_pick(f, x, y), max_exp=3000000, cross=cross)
    if r[0] != 'ok':
        return None
    return r[2][0], r[2]


def commit(tag, w, res):
    SEG.append((tag, L2.trace(res)))
    print('    + %-20s → %s' % (tag, st(w)))


def greedy(f, w, min_hp=40, allow=('hp', 'atk', 'def', 'shield', 'rkey', 'bkey', 'key')):
    """层内贪心吃资源：每轮选「到达后 HP 最高」的候选。"""
    pool = [r for r in RES.get(f, [])]
    progress = True
    while progress:
        progress = False
        best = None
        for (x, y, name, kind) in pool:
            if (f, x, y) in w.cleared:
                continue
            if kind not in allow:
                continue
            got = try_pick(f, w, x, y)
            if got is None:
                continue
            w2, res = got
            # 血瓶/钥匙必吃；宝石要求到达后仍有余量
            if kind in ('atk', 'def') and w2.hero.hp < min_hp:
                continue
            if best is None or w2.hero.hp > best[0].hero.hp:
                best = (w2, res, name, kind, x, y)
        if best is not None:
            w2, res, name, kind, x, y = best
            commit('%dF %s(%d,%d)' % (f, name, x, y), w2, res)
            w = w2
            progress = True
    return w


def up(f, w):
    """走到本层上行梯并上传。"""
    r = L2.plan_layer(f, w, g_floor(f + 1), max_exp=3000000, cross=True)
    if r[0] != 'ok':
        print('  ✗ %dF 上楼失败' % f)
        return None
    w2 = r[2][0]
    commit('%dF 上楼 → %dF' % (f, f + 1), w2, r[2])
    return w2


if __name__ == '__main__':
    cur = L2.mk_world(6, 1, 2, 162, 20, 10, 35, 2, 1, 0)
    print('起点  ' + st(cur))
    for f in (6, 7, 8, 9, 10):
        if f == 10:
            cur = greedy(f, cur)
            # BOSS 前必须有红钥
            print('    boss 前状态 ' + st(cur))
            r = L2.plan_layer(10, cur, g_boss, max_exp=3000000)
            if r[0] != 'ok':
                print('  ✗ 10F 打不动 BOSS')
                break
            cur = r[2][0]
            commit('10F ★打 BOSS', cur, r[2])
            cur = up(10, cur)
            if cur is None:
                break
        else:
            cur = greedy(f, cur)
            if cur.hero.hp <= 0:
                break
            cur = up(f, cur)
            if cur is None:
                break
    print()
    print('终态  ' + st(cur))
