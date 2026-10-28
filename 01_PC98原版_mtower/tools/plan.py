#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""plan.py —— 先定路线、再寻路。

和 crawl.py 的根本区别：这里**没有任何「挑性价比最高」的搜索**。
每层要去哪个格子、按什么顺序去，全部由人（攻略）写死在 SEGS 里；
程序只负责：给定当前状态 + 目标格，跑点到点最短路，并把钥匙/血量记成账。

目标格必须是可站格（门开会返回原地，所以不要把门当目标）。
"""
import sys
import collections
import csv
import json

import mota_core as M

DIRS = [(0, -1, '8'), (1, 0, '6'), (0, 1, '2'), (-1, 0, '4')]
LOG = []          # 全程序列 (步号, 层, x, y, 键, 备注, hp, atk, dfn, gold, ky, kb, kr)


def st(h):
    return '%2dF(%2d,%2d) HP%-4d ATK%2d DEF%2d G%-3d 钥%d/%d/%d' % (
        h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
        h.keys['y'], h.keys['b'], h.keys['r'])


_BLK = {}


def blockers_of(f):
    """本层所有「挡路物」坐标（门/怪/商店）。状态键只追踪这些，避免物品格让状态爆炸。"""
    if f not in _BLK:
        s = set()
        for y in range(1, 12):
            for x in range(1, 12):
                o = M.obj_raw(f, x, y)
                if not o:
                    continue
                ty = M.TYPE.get(M.oatr(o, 3))
                if ty in ('DOOR', 'MONSTER') or o in M.SHOP:
                    s.add((x, y))
        _BLK[f] = s
    return _BLK[f]


def _key(w):
    """状态键。

    必须纳入攻防与血量（粗桶）：魔塔是「属性门控」游戏——同一格在低攻防下打不过守门怪、
    在高攻防下能过，二者是不同状态。旧键只记 (楼层,坐标,钥匙,本层清障计数,购物数)，
    会把「先绕路堆攻防、回头再走关口格」的高攻防路径误判为已访问而剪枝，导致 BFS 说可达、
    A* 却返回不可达。现把 atk/dfn 与 hp//50 粗桶纳入，单楼层点到点 A* 状态数仍可控。
    """
    h = w.hero
    blk = blockers_of(h.f)
    n = 0
    for c in w.cleared:
        if c[0] == h.f and (c[1], c[2]) in blk:
            n += 1
    bo = len([c for c in w.bought if c[0] == h.f])
    return (h.f, h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'],
            h.atk, h.dfn, h.hp // 50, n, bo)


def walk(w, tgt, max_exp=300000):
    """A* 点到点最短路（曼哈顿启发）。tgt 可为 (f,x,y) 坐标或谓词。

    注意：走到楼梯格会立刻跨层，所以「上楼」必须用谓词当目标，不能用梯格坐标。
    返回 (world, [(dx,dy,键,log), ...]) 或 (None, 原因)。
    """
    import heapq
    if isinstance(tgt, int):
        tn = tgt
        done = lambda x: x.hero.f == tn
        heuristic = lambda x: 30 * abs(x.hero.f - tn)
    elif callable(tgt):
        done = tgt
        heuristic = lambda x: 0
    else:
        tf, tx, ty = tgt
        done = lambda x: (x.hero.f, x.hero.x, x.hero.y) == tgt
        heuristic = lambda x: 30 * abs(x.hero.f - tf) + (
            abs(x.hero.x - tx) + abs(x.hero.y - ty) if x.hero.f == tf else 0)

    if done(w):
        return w, []
    seen = {_key(w)}
    cnt = 0
    h0 = heuristic(w)
    heap = [(h0, 0, 0, w, [])]      # (h+步数, 计数, 步数, world, path)
    n = 0
    while heap:
        _, _, g, cur, path = heapq.heappop(heap)
        n += 1
        if n > max_exp:
            return None, '展开超限 %d' % n
        for dx, dy, lab in DIRS:
            w2 = cur.clone()
            lg = w2.move(dx, dy)
            if M.blocked(lg):
                continue
            if w2.hero.hp <= 0:
                continue
            k = _key(w2)
            if k in seen:
                continue
            seen.add(k)
            p = path + [(dx, dy, lab, lg)]
            if done(w2):
                return w2, p
            # 代价 = 步数 + 掉血/20：否则 A* 只图路近，会挑「步数少但一路打架」的门路
            loss = max(0, cur.hero.hp - w2.hero.hp)
            step = 1 + loss // 20
            cnt += 1
            heapq.heappush(heap, (heuristic(w2) + g + step, cnt, g + step, w2, p))
    return None, '不可达'


def seg(tag, w, tgt, max_exp=300000):
    """执行一段：打印前态→后态，并把路径灌进 LOG。"""
    h0 = w.hero
    s0 = (h0.hp, h0.atk, h0.dfn, h0.gold, dict(h0.keys))
    w2, path = walk(w, tgt, max_exp)
    if w2 is None:
        print('  ✗ %-24s %s  [%s]' % (tag, path, st(h0)))
        return None
    # 逐步回放以记录每一步的状态
    cur = w
    for (dx, dy, lab, _lg) in path:
        cur = cur.clone()
        lg = cur.move(dx, dy)
        h = cur.hero
        LOG.append((len(LOG) + 1, h.f, h.x, h.y, lab, ' '.join(lg),
                    h.hp, h.atk, h.dfn, h.gold,
                    h.keys['y'], h.keys['b'], h.keys['r']))
    h = w2.hero
    d = h.hp - s0[0]
    note = ''
    if h.atk != s0[1]:
        note += ' ATK%+d' % (h.atk - s0[1])
    if h.dfn != s0[2]:
        note += ' DEF%+d' % (h.dfn - s0[2])
    print('  ✓ %-24s → %-46s [%2d 步] HP%+d%s' % (tag, st(h), len(path), d, note))
    return w2


def to_floor(tag, w, n, max_exp=500000):
    """走到 n 层（谓词目标：一踩楼梯就跨层，故不能以梯格坐标为目标）。可上行也可下行。"""
    w2, path = walk(w, n, max_exp)
    if w2 is None:
        print('  ✗ %-24s 无路  [%s]' % (tag, st(w.hero)))
        return None
    cur = w
    for (dx, dy, lab, _lg) in path:
        cur = cur.clone()
        lg = cur.move(dx, dy)
        h = cur.hero
        LOG.append((len(LOG) + 1, h.f, h.x, h.y, lab, ' '.join(lg),
                    h.hp, h.atk, h.dfn, h.gold,
                    h.keys['y'], h.keys['b'], h.keys['r']))
    h = w2.hero
    print('  ✓ %-24s → %-46s [%2d 步]' % (tag, st(h), len(path)))
    return w2


# ──────────────────────────────────────────────────────────────────────
# 路线（人写的，不是搜出来的）
# 每条 = (楼层, x, y, 说明)。顺序即执行顺序。
# ──────────────────────────────────────────────────────────────────────
SEGS = {
    1: [],
    2: [(4, 10, '蓝药+200'), (3, 10, '蓝药+200'), (3, 11, '蓝药+200')],
    3: [(5, 1, '蓝药+200'), (4, 2, '蓝药+200'), (6, 2, '蓝药+200'),
        (4, 1, '黄钥'), (6, 1, '黄钥'), (5, 2, '黄钥'), (4, 3, '黄钥'),
        (6, 3, '黄钥'), (5, 3, '蓝钥')],
    # 4F：ATK10 时西侧全被僧侶(def8)/スケルトンＢ(def12) 堵死，只取走廊东侧 3 把黄钥
    4: [(5, 10, '黄钥'), (5, 11, '黄钥'), (3, 11, '黄钥')],
    # 5F：先撞暗墙取鉄の剣（ATK+10 是所有后续的前提），再回头收东南 4 把钥匙
    5: [(11, 11, '★鉄の剣 ATK+10（撞暗墙 9,11）'),
        (8, 3, '黄钥'), (9, 3, '黄钥'), (8, 4, '黄钥'), (9, 4, '黄钥'),
        (6, 2, '黄钥')],
    # ── 6F：只走「廉价钥匙 → 底部红药 → 商店蓝钥 → 上梯」；蓝晶(4,9) 160 血换 1 DEF 不值，跳过 ──
    6: [(3, 1, '黄钥'), (4, 1, '黄钥'), (3, 2, '黄钥'), (4, 2, '黄钥'),
        (6, 6, '黄钥'),
        (8, 11, '红药+50'), (9, 11, '红药+50'),
        (8, 4, '★商店 蓝钥 50G'), (8, 3, '红药+50')],
    # ── 7F：右侧蓝药 → 左侧钥匙/红药 → 红晶 → 下方钥匙 → 蓝药 → 左上上梯
    #    （中央商店 5 黄钥要掉 380 血穿走廊，纯亏，不买；8F 自带 8 把足够）
    7: [(9, 10, '黄钥'), (9, 11, '黄钥'), (9, 9, '蓝药+200'),
        (9, 1, '黄钥'), (9, 2, '黄钥'), (9, 3, '红药+50'),
        (3, 1, '红晶ATK+1'), (3, 2, '红药+50'),
        (5, 10, '黄钥'), (5, 11, '黄钥'),
        (7, 11, '蓝药+200')],
    # ── 8F：左角红药 → 中段 3 钥匙 → 绕开门番C 取红钥 → 区内药 → 蓝门内晶石 → 上梯 ──
    8: [(1, 5, '红药+50'),
        (3, 4, '黄钥'), (4, 4, '黄钥'), (5, 4, '黄钥'),
        (10, 2, '★赤色の扉の鍵(红钥)'),
        (9, 1, '黄钥'), (11, 1, '黄钥'), (9, 3, '蓝药+200'), (11, 3, '红药+50'),
        (4, 10, '红晶ATK+1'), (5, 11, '蓝晶DEF+1'), (5, 10, '黄钥'), (4, 11, '黄钥'),
        (7, 11, '黄钥'), (7, 10, '蓝钥')],
    # ── 9F：不碰蓝门，走 区1→(黄门8,1+Ｇスライム9,1)→区2→撞暗墙(10,5) 取铁盾
    #    铁盾到手 DEF 10→21，之后所有战斗都便宜一半，故排在最前
    9: [(9, 7, '★鉄の盾 DEF+10（撞暗墙 10,5）'),
        (11, 1, '红药+50'),
        (2, 4, '黄钥'), (1, 5, '蓝晶DEF+1'),
        (6, 5, '红晶ATK+1'), (5, 4, '黄钥'), (7, 4, '黄钥'),
        (2, 10, '红药+50'), (11, 11, '红药+50')],
    # ── 10F：先吃事件写入的双蓝药 + 晶石 + 黄钥，再破红门打 BOSS ──
    10: [(3, 4, '蓝药+200'), (1, 4, '蓝药+200'),
         (2, 6, '蓝晶DEF+1'),
         (9, 4, '黄钥'),
         (10, 6, '红晶ATK+1'),
         (11, 11, '蓝药+200'),
         (6, 3, '★★10F BOSS スケルトンＡ')],
    # ── 11F：落点 (6,10)。银盾 DEF+20 是全层最赚的一格，且路上不碰 def30 的上级僧侣
    #    （走 x=2 竖道从 (2,11) 直上 (2,2)，左右两只是怪、中间是地板）。黄钥 5 把沿路白捡
    11: [(2, 2, '★銀の盾 DEF+20'),
         (1, 7, '蓝药+400'), (2, 7, '蓝药+400'),
         (8, 11, '蓝药+400'),
         (9, 6, '红药+100'), (10, 1, '红药+100'), (5, 1, '红晶ATK+2')],
    # ── 12F：落点 (10,11)。祭坛 (6,9) 是不可走的 SAIDAN，东西分区只能绕 y=10/y=8
    #    商店 (1,1) 红钥 800G —— 14F 红门后只有 3 把黄钥+1 只怪，不值，不买
    12: [(5, 10, '红药+100'), (7, 10, '红药+100'),
         (6, 7, '蓝药+400'),
         (9, 5, '红药+100'), (10, 6, '青晶DEF+2'),
         (10, 1, '撞暗墙'), (11, 1, '撞暗墙'), (2, 1, '撞暗墙'),
         (6, 1, '红晶ATK+2'),
         (2, 8, '蓝钥'), (1, 8, '黄钥'), (2, 7, '黄钥'), (1, 7, '黄钥')],
    # ── 13F：落点 (2,11)。神剑房间被熔岩 obj79 封死（每步 -200），唯一入口是
    #    (6,10) 黄门 → 穿 (7,9)(7,8) 两格熔岩进 (7,7)，取剑后原路返回，共 4 格 -800 HP
    13: [(6, 5, '★神　剣 ATK+100（穿熔岩 4 格 -800）')],
    # ── 14F：落点 (10,11)。红门 (10,3) 要红钥（(1,3) 那把在 terrain=1 的墙里，拿不到），
    #    门后也无非 3 黄钥+1 怪，绕开；直接压 (6,11) 下 15F
    14: [(5, 10, '红药+100'), (5, 1, '青晶DEF+2'), (7, 1, '红药+100'),
         (1, 5, '红药+100'), (9, 6, '红药+100'), (6, 9, '撞暗墙')],
    # ── 15F：落点 (6,10)。中央 3×3 大章鱼 9 格全是战斗单位（每格 HP1200/ATK180），
    #    神剑 ATK126 下单格也要掉 1400+，九格 13000+，完全不划算；走右侧竖道绕：
    #    (8,10)→(8,2)→(7,2)→(7,1)→(6,1) 上梯（(8,1) 被 directCheck 写成墙，正好堵死抄近道）
    15: [(11, 8, '蓝药+400')],
    # ── 16F：落点 (6,10)。西侧一串红药/晶石沿 x=1 竖道一路捡完，再回 (6,1) 上梯
    16: [(1, 7, '青晶DEF+2'), (1, 6, '红药+100'), (1, 5, '红晶ATK+2'),
         (5, 5, '红药+100'), (11, 3, '红药+100')],
    # ── 17F：落点 (6,2)。银剑 (2,2) 就在落点旁 4 步，先拿；再扫四角晶石药瓶
    17: [(2, 2, '★銀の剣 ATK+20'),
         (9, 1, '青晶DEF+2'), (11, 1, '红晶ATK+2'), (10, 2, '蓝药+400'),
         (1, 11, '红药+100'), (11, 11, '红药+100')],
    18: [],
}

# 拿到铁盾（DEF21）之后回头清的资源：此时战斗成本只有当初的 1/3 左右
# 只挑「同一道黄门内」的点，别为了 50 血再绕 100 步、把黄钥匙耗光（黄钥匙是最后打 BOSS 开红门的前提）
BACK = {
    4: [(7, 10, '红晶ATK+1'), (9, 10, '红药+50')],
    3: [(11, 1, '红药+50'), (11, 7, '红药+50'), (1, 9, '红药+50'), (2, 9, '红晶ATK+1')],
}

# 3F 陷阱：踩了会被剥装并送回 2F(4,8)
TRAP = lambda x: (x.hero.f == 2 and x.hero.hp == 400)


def main():
    import os
    import pickle

    w = M.World.new()
    print('起点  ' + st(w.hero))

    # ── 断点续跑：已跑通的楼层直接读回来，避免每次迭代都重算 1F-3F ──
    done_upto = 1
    for f in range(11, 0, -1):
        p = 'ck_%d.pkl' % f
        if os.path.exists(p):
            with open(p, 'rb') as fp:
                w = pickle.load(fp)
            done_upto = f
            print('（从 %dF 断点续跑  %s）' % (f, st(w.hero)))
            break

    def ck(f, w):
        with open('ck_%d.pkl' % f, 'wb') as fp:
            pickle.dump(w, fp)

    if done_upto == 1:
        w = to_floor('1F → 2F', w, 2)
        w = to_floor('2F → 3F', w, 3)
        if w is None:
            sys.exit(1)

        w2, path = walk(w, lambda x: x.hero.f == 2 and x.hero.hp == 400, 600000)
        if w2 is None:
            print('  ✗ 3F 陷阱（踩上去被剥装并送回 2F）')
            sys.exit(1)
        cur = w
        for (dx, dy, lab, _lg) in path:
            cur = cur.clone()
            lg = cur.move(dx, dy)
            h = cur.hero
            LOG.append((len(LOG) + 1, h.f, h.x, h.y, lab, ' '.join(lg),
                        h.hp, h.atk, h.dfn, h.gold,
                        h.keys['y'], h.keys['b'], h.keys['r']))
        w = w2
        print('  ✓ %-24s → %-46s' % ('3F 踩陷阱（被剥装）', st(w.hero)))

        # 剥装后必须回 2F 吃掉三个 +200 蓝药再上楼，否则 3F 起血量见底
        for (x, y, lab) in SEGS[2]:
            w2 = seg('2F %s' % lab, w, (2, x, y))
            if w2 is not None:
                w = w2

        w = to_floor('2F → 3F', w, 3)
        ck(2, w)

    fails = []
    for f in range(max(3, done_upto), 18):
        print('--- %dF' % f)
        for (x, y, lab) in SEGS.get(f, []):
            w2 = seg('%dF %s' % (f, lab), w, (f, x, y))
            if w2 is None:
                fails.append('%dF(%d,%d) %s' % (f, x, y, lab))
            else:
                w = w2
        if f == 9:
            # 铁盾已在手（DEF 21），回 4F/3F 把当初打不动的血瓶与红晶一次性清掉
            for back in (4, 3):
                w2 = to_floor('9F → %dF 回程' % back, w, back)
                if w2 is None:
                    fails.append('回 %dF' % back)
                    continue
                w = w2
                for (x, y, lab) in BACK[back]:
                    w2 = seg('%dF %s' % (back, lab), w, (back, x, y))
                    if w2 is not None:
                        w = w2
            w2 = to_floor('回 9F', w, 9)
            if w2 is None:
                fails.append('回 9F')
                break
            w = w2

        if f < 17:
            w2 = to_floor('%dF → %dF' % (f, f + 1), w, f + 1)
            if w2 is None:
                fails.append('%dF 上楼' % f)
                break
            w = w2
            ck(f + 1, w)
        if f == 10 and not w.boss10:
            fails.append('10F BOSS 未击杀')
            break

    print()
    print('终态  ' + st(w.hero))
    if fails:
        print('断点：')
        for s in fails:
            print('   -', s)
    else:
        print('★ 1F→17F 全程打通（含 6F→11F 速通段）')

    with open('route_plan.csv', 'w', newline='', encoding='utf-8') as fp:
        cw = csv.writer(fp)
        cw.writerow(['step', 'floor', 'x', 'y', 'key', 'event', 'hp', 'atk', 'def', 'gold', 'ky', 'kb', 'kr'])
        cw.writerows(LOG)
    print('已写 route_plan.csv（%d 步）' % len(LOG))


if __name__ == '__main__':
    main()
