#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""play20.py —— 「模仿人类玩法」的 11F→20F 通关路线。

与 build20.py（A* 全局搜索）的根本区别：
  1. **没有 A***：导航是自研 BFS（队列、无启发式），且严格限制在「当前层 ∪ 目标层」，
     因此不会像 A* 那样跨层乱搜、在楼层间反复横跳。
  2. **逐层推进**：人类是一层一层爬塔的，不做「一次性规划 6 层」的全局最优解。
  3. **路线决策 100% 人工**：每层去哪几个格子、按什么顺序，写死在 SEGS 里；
     BFS 只负责「从当前格走到指定格的最短路」（等同于人类走路，不是搜索解法）。

目标：从 1F→17F 成品路线的终态 11F(2,2) 出发，补满血 → 收 11~17F 遗留补给
      → 18F 开蓝门 → 19F 撞十字暗墙取十字架 → 20F 吃大补血 → 击杀吸血鬼 BOSS → 上 21F。
"""
import sys
import os
import csv
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state as S
import mota_core as M

HERE = os.path.dirname(os.path.abspath(__file__))
# 地基 = 1F→17F 成品路线。优先取脚本同目录，回退 /workspace（便于两处都能直接跑）
BASE_CSV = os.path.join(HERE, '魔塔1_route_1F到17F.csv')
if not os.path.exists(BASE_CSV):
    BASE_CSV = '/workspace/魔塔1_route_1F到17F.csv'
OUT_CSV = os.path.join(HERE, '魔塔1_route_11F到21F_人类玩法.csv')

DIRS = [(0, -1, '8'), (1, 0, '6'), (0, 1, '2'), (-1, 0, '4')]
LOG = []
_BLK = {}


def blockers_of(f):
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


def key(w):
    h = w.hero
    blk = blockers_of(h.f)
    n = sum(1 for c in w.cleared if c[0] == h.f and (c[1], c[2]) in blk)
    return (h.f, h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'],
            h.atk, h.dfn, h.hp // 50, n)


def nav(w, tgt, cap=400000):
    """BFS 最短路（无启发式）。tgt 为 (f,x,y) 坐标，或目标楼层 int。

    BFS 严格限制在「当前层 ∪ 目标层」，不向其它楼层扩散 —— 这是逐层推进的关键，
    也是它不会像跨层 A* 那样状态爆炸的原因。
    """
    cur_f = w.hero.f
    if isinstance(tgt, int):
        tf = tgt
        done = lambda x: x.hero.f == tf
    else:
        tf = tgt[0]
        done = lambda x: (x.hero.f, x.hero.x, x.hero.y) == tgt

    # 允许在「当前层/目标层」的相邻层内绕路 —— 部分补给点必须绕相邻层才能进，
    # 但仍严格限制在 ±1 层，不会像跨层 A* 那样向全塔扩散。
    lo = min(cur_f, tf) - 1
    hi = max(cur_f, tf) + 1

    def allowed(x):
        return lo <= x.hero.f <= hi

    if done(w):
        return w, []
    seen = {key(w)}
    q = collections.deque([(w, [])])
    n = 0
    while q and n < cap:
        cur, path = q.popleft()
        n += 1
        for dx, dy, lab in DIRS:
            t = cur.clone()
            lg = t.move(dx, dy)
            if M.blocked(lg) or t.hero.hp <= 0 or not allowed(t):
                continue
            k = key(t)
            if k in seen:
                continue
            seen.add(k)
            p = path + [(dx, dy, lab, lg)]
            if done(t):
                return t, p
            q.append((t, p))
    return None, '不可达(BFS 展开 %d)' % n


def dump_reach(w, f, cap=200000):
    """诊断：BFS 列出 f 层的可达格（#=可达 .=不可达）。"""
    seen = {key(w)}
    q = collections.deque([w])
    reach = set()
    n = 0
    if w.hero.f == f:
        reach.add((w.hero.x, w.hero.y))
    while q and n < cap:
        c = q.popleft()
        n += 1
        for dx, dy, lab in DIRS:
            t = c.clone()
            lg = t.move(dx, dy)
            if M.blocked(lg) or t.hero.hp <= 0:
                continue
            if t.hero.f != f:
                continue
            k = key(t)
            if k in seen:
                continue
            seen.add(k)
            reach.add((t.hero.x, t.hero.y))
            q.append(t)
    print('    ' + ''.join(str(x % 10) for x in range(1, 12)), flush=True)
    for y in range(1, 12):
        print('  y=%-2d %s' % (y, ''.join('#' if (x, y) in reach else '.'
                                          for x in range(1, 12))), flush=True)
    for (x, y, lab) in [(6, 6, '吸血鬼BOSS'), (6, 9, '门禁obj27'), (2, 6, '蓝门'),
                        (10, 6, '蓝门'), (1, 9, '黄门'), (11, 9, '黄门'), (6, 1, '上梯')]:
        print('    (%2d,%2d) %-10s %s' % (x, y, lab, '可达' if (x, y) in reach else '不可达'),
              flush=True)
    print('    （BFS 展开 %d）' % n, flush=True)


def descend(w, target_f):
    """逐层下行到 target_f —— 一次只规划一层，不跨层搜索。

    人类下楼就是一层一层下。跨层 BFS/A* 会把多层状态空间乘在一起而爆炸，
    逐层则每层的状态空间只有一百来个格子，稳。
    """
    while w.hero.f > target_f:
        f = w.hero.f
        w2 = seg('%dF → %dF 下行' % (f, f - 1), w, f - 1)
        if w2 is None:
            print('  ✗ 下行卡在 %dF' % f, flush=True)
            return None
        w = w2
    return w


def ascend(w, target_f):
    """逐层上行到 target_f（同上，一次只规划一层）。"""
    while w.hero.f < target_f:
        f = w.hero.f
        w2 = seg('%dF → %dF 上行' % (f, f + 1), w, f + 1)
        if w2 is None:
            print('  ✗ 上行卡在 %dF' % f, flush=True)
            return None
        w = w2
    return w


def st(h):
    return '%2dF(%2d,%2d) HP%-5d ATK%-3d DEF%-3d G%-4d 钥%d/%d/%d' % (
        h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
        h.keys['y'], h.keys['b'], h.keys['r'])


def apply_path(w, path):
    """把 BFS 找到的路径逐步执行并记账。"""
    cur = w
    for dx, dy, lab, _ in path:
        cur = cur.clone()
        lg = cur.move(dx, dy)
        h = cur.hero
        LOG.append((len(LOG) + 1, h.f, h.x, h.y, lab, ' '.join(lg),
                    h.hp, h.atk, h.dfn, h.gold,
                    h.keys['y'], h.keys['b'], h.keys['r']))
    return cur


def seg(tag, w, tgt):
    w2, path = nav(w, tgt)
    if w2 is None:
        print('  ✗ %-28s %s   [%s]' % (tag, path, st(w.hero)), flush=True)
        return None
    cur = apply_path(w, path)
    print('  ✓ %-28s → %s  [%2d 步]' % (tag, st(cur.hero), len(path)), flush=True)
    return cur


# ──────────────────────────────────────────────────────────────────────
# 路线（人写的攻略）：每层去哪几个格子、按什么顺序
# ──────────────────────────────────────────────────────────────────────
SEGS = {
    # 11F：HP5 起步，先把血拉起来；钥匙优先（后面开门全靠它）
    #   注：(5,1) 红晶 ATK+2 要开 2 道黄门，性价比极低（换来的 ATK+2 远不如留下的 2 把钥匙），主动放弃
    11: [(1, 7, '蓝药+400'), (10, 1, '红药+100'), (9, 6, '红药+100'),
         (11, 1, '黄钥')],
    12: [(6, 7, '蓝药+400'), (9, 5, '红药+100'), (10, 6, '青晶DEF+2'),
         (5, 1, '黄钥'), (7, 1, '黄钥'), (9, 7, '黄钥')],
    13: [],                                    # 神剑 (6,5) 被熔岩封死，不可达，直接穿过
    # 14F：先扫钥匙（黄×5 + 蓝×1 + ★红×1），再收补给
    #   ★ 红钥匙在 (1,3)，是 dyn_raw 的动态写入（静态底图此处为空，故查静态会漏）。
    #     8F(10,2) 那把已用于开 10F 红门，20F(6,9) 就靠这一把 —— 见 BOSS 的门槛。
    #     16F(1,11) NPC 的「赤い鍵は２ヶ所で手に入る」正是印证这两处。
    14: [(6, 1, '黄钥'), (9, 1, '黄钥'), (10, 1, '黄钥'), (11, 1, '黄钥'), (11, 2, '黄钥'),
         (1, 11, '★蓝钥匙'), (1, 3, '★★红钥匙(20F用)'),
         (1, 5, '红药+100'), (9, 6, '红药+100'), (5, 1, '青晶DEF+2'), (7, 1, '红药+100')],
    15: [(3, 5, '黄钥'), (3, 6, '★蓝钥匙'), (3, 7, '黄钥'),
         (11, 8, '蓝药+400'), (1, 1, '青晶DEF+2')],
    #   注：(11,3) 红药+100 要耗 1 把黄钥匙，而黄钥匙是 18F 开 (8,1) 黄门、
    #   进而拿到 18F 右侧整串钥匙的前提 —— 宁可少 100 血也要把钥匙留到 18F
    16: [(1, 1, '黄钥'), (1, 2, '黄钥'), (1, 3, '黄钥'), (2, 5, '黄钥'), (2, 7, '黄钥'),
         (11, 7, '★蓝钥匙'),
         (1, 7, '青晶DEF+2'), (1, 6, '红药+100'), (1, 5, '红晶ATK+2')],
    17: [(9, 3, '黄钥'), (11, 3, '黄钥'),
         (9, 1, '青晶DEF+2'), (11, 1, '红晶ATK+2'), (10, 2, '蓝药+400'),
         (1, 11, '红药+100'), (11, 11, '红药+100')],
    18: [(11, 1, '黄钥'), (11, 2, '黄钥'), (11, 3, '★蓝钥匙'), (11, 4, '黄钥'), (11, 5, '黄钥')],
    19: [(6, 3, '★十字架(撞暗墙)'), (8, 1, '★蓝钥匙(20F 中央门用)'),
         (4, 1, '红药+100'), (9, 9, '红药+100'), (11, 1, '红晶ATK+2')],
    #   注：(1,4) 青晶 DEF+2 同样耗 1 把蓝钥匙，蓝钥匙必须留给中央区的门，故放弃
    20: [(11, 4, '★蓝药+400'),
         (10, 4, '红药+50'), (1, 11, '红药+50'), (11, 11, '红药+50')],
}


def main():
    w = S.replay(BASE_CSV)
    print('地基:', st(w.hero), flush=True)

    # 阶段 0：地基只剩 1 把黄钥匙，而 12~18F 全是黄门。
    # 人类玩法会先回底层把钥匙补够再上塔 —— 9F 有 4 把黄钥匙可达。
    print('--- 补钥匙：下行 9F', flush=True)
    for (x, y) in [(2, 2), (1, 7), (5, 7), (9, 9)]:
        w2 = seg('9F 黄钥(%d,%d)' % (x, y), w, (9, x, y))
        if w2:
            w = w2
    w2 = seg('回到 11F', w, 11)
    if w2:
        w = w2
    print('  补钥匙后:', st(w.hero), flush=True)

    for f in range(11, 20):          # 11F..19F；19F 上梯后即抵达 20F
        print('--- %dF' % f, flush=True)
        for (x, y, lab) in SEGS.get(f, []):
            w2 = seg('%dF %s' % (f, lab), w, (f, x, y))
            if w2:
                w = w2
        if w.hero.f != f:
            print('  （已跨层，跳过本层上梯）', flush=True)
            continue
        w2 = seg('%dF → %dF 上梯' % (f, f + 1), w, f + 1)
        if w2 is None:
            print('✗ 卡在 %dF' % f, flush=True)
            break
        w = w2

    if w.hero.f != 20:
        print('✗ 未到达 20F，终止')
        return
    print('  → 进入 20F，落点', st(w.hero), flush=True)

    # ── 20F：先把能拿的补给拿完 ──
    print('--- 20F', flush=True)
    for (x, y, lab) in SEGS.get(20, []):
        w2 = seg('20F %s' % lab, w, (20, x, y))
        if w2:
            w = w2

    # ── 回 12F 祭坛献攻（+ATK，而非献血）──
    #    吸血鬼 HP444/ATK199/DEF66，持有十字架 obj103 → 伤害翻倍。
    #    本路线 ATK 从 85 献 3 次到 115（每次 +10，成本 140+220+320=680G）。
    #    献攻后每击 = 115×2−66 = 164，3 回合解决；掉血 = (199−57)×2 = 284。
    #    献血(+HP)虽也便宜，但献攻更直接压低回合数与掉血，且本路线血够用（详见路线说明）。
    print('--- 回 12F：祭坛献攻（红钥匙已在 14F 暗墙免费取得）', flush=True)
    w = descend(w, 12)
    if w is None:
        print('✗ 回不到 12F')
        return
    # ⚠️ 刻意不改 altar_policy：CSV 只记移动方向、无法记录祭坛菜单选项，
    #    设成 'hp' 会让回放回落到默认 'atk'，路线无法忠实复现。故固定用默认 'atk'。
    # 预算：红钥匙已在 14F(1,3) 免费拿到，不必再攒 800G 买钥匙，
    #    故 GOLD 可全部投入祭坛（3 次共 680G）。
    for i in range(3):
        # 献祭后英雄站在祭坛格上，必须先离开再撞回来才能触发下一次
        if (w.hero.f, w.hero.x, w.hero.y) == (12, 6, 9):
            w2 = seg('  离开祭坛', w, (12, 6, 10))
            if w2:
                w = w2
        c = M.altar_cost(w.altar_k)
        if w.hero.gold < c:
            print('  金不足（需 %d，有 %d），停止献祭' % (c, w.hero.gold), flush=True)
            break
        w2 = seg('12F 祭坛第%d次(ATK+10)' % (i + 1), w, (12, 6, 9))
        if w2 is None:
            break
        w = w2
    print('  献祭后:', st(w.hero), flush=True)

    # ── 红钥匙：14F(1,3) 动态写入的那把，用于开 20F(6,9) 红门 ──
    #    8F(10,2) 的静态红钥匙已用于 10F 红门（10F 红门是通往 11F 的必经路，必须开），
    #    12F(1,1) 商店虽卖红钥匙但实测不可达（其左上区封闭），故 20F 全靠 14F 这一把。
    print('--- 红钥匙检查（20F 红门用）', flush=True)
    print('  红钥匙 =', w.hero.keys['r'], flush=True)
    if w.hero.keys['r'] <= 0:
        print('✗ 无红钥匙，20F(6,9) 红门开不了，见不到 BOSS')
        return

    # ── 回 20F ──
    w = ascend(w, 20)
    if w is None:
        print('✗ 回不去 20F')
        return
    print('  回到 20F:', st(w.hero), flush=True)

    # ── 打吸血鬼 BOSS：BFS 直接走到 (20,6,6)，沿途大蝙蝠会自动战斗 ──
    print('--- 20F 击杀吸血鬼 BOSS (6,6)', flush=True)
    print('  诊断 20F(6,6) obj_raw=%s 引擎 at=%s；落点可达格：'
          % (M.obj_raw(20, 6, 6), w.at(20, 6, 6)), flush=True)
    dump_reach(w, 20)
    h = w.hero
    cross = 103 in h.items
    per = h.atk * (2 if cross else 1) - M.oatr(59, 12)
    turns = -(-M.oatr(59, 10) // per) if per > 0 else 999
    loss = max(M.oatr(59, 11) - h.dfn, 0) * (turns - 1)
    print('  战前 %s；十字架=%s；每击%d，需%d击，预计掉血%d'
          % (st(h), cross, per, turns, loss), flush=True)
    w2 = seg('20F ★★吸血鬼 BOSS (6,6)', w, (20, 6, 6))
    if w2 is None:
        print('✗ 打不过 / 走不到 BOSS')
        return
    w = w2
    print('  BOSS 后:', st(w.hero), 'boss20 =', w.boss20, flush=True)

    # ── BOSS 死后 (20,6,1) 现出上行梯 → 21F ──
    if w.boss20:
        w2 = seg('20F → 21F 上梯', w, 21)
        if w2:
            w = w2
            print('★ 通关第 20 层，抵达', st(w.hero), flush=True)

    out = OUT_CSV
    with open(out, 'w', newline='', encoding='utf-8') as fp:
        cw = csv.writer(fp)
        cw.writerow(['step', 'floor', 'x', 'y', 'key', 'event',
                     'hp', 'atk', 'def', 'gold', 'ky', 'kb', 'kr'])
        cw.writerows(LOG)
    print('\n已写', out, '（%d 步）' % len(LOG))


if __name__ == '__main__':
    main()
