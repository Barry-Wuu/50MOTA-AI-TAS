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
LAST_W = None


def st(h):
    return 'HP%-5d A%-3d D%-3d G%-5d 钥%d/%d/%d %dF(%2d,%2d)' % (
        h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y)


def _passable(w, f, nx, ny):
    return _cost(w, f, nx, ny)[0]


def _stair_cells(w, f):
    """该层所有会触发换层的格子（含 BOSS 死后动态出现的梯）。"""
    s = set()
    for c in M.STAIRS.get(f, (None, None)):
        if c:
            s.add(c)
    if f == 10 and getattr(w, 'boss10', False):
        s.add((6, 11))
    if f == 20 and getattr(w, 'boss20', False):
        s.add((6, 1))
    return s


def _cost(w, f, nx, ny):
    """(可否通过, 代价)。代价只用于选路偏好：怪物 100、门 25，避免"顺路打怪"违背攻略。"""
    if not (1 <= nx <= 11 and 1 <= ny <= 11):
        return False, 0
    # 楼梯格不进层内 BFS（踩上去会换层，破坏位置）
    if w.terrain_at(f, nx, ny) in (1, 2):
        # 盗贼凿开的暗道：地形仍是墙，但触发格已对话过 → 可通行
        trig = M.DIG_WALLS.get((f, nx, ny))
        if trig is not None and trig in w.cleared:
            return True, 1
        return False, 0
    if (nx, ny) in _stair_cells(w, f):
        return False, 0
    o = w.at(f, nx, ny)
    if not o:
        return True, 1
    ty = M.TYPE.get(M.oatr(o, 3))
    if o == 89:                      # 暗墙：撞塌后本人直接进入该格
        return True, 3
    if o in M.KEY_OF or ty in ('STATUS', 'ITEM', 'NORMAL', 'SCORE', 'MESSAGE'):
        return True, 1
    if ty == 'DOOR':
        col = M.DOOR_OF.get(o)
        return (col is not None and w.hero.keys[col] > 0), 25
    if ty == 'SELL':                 # 商店：钱够即可谈（谈完该格 cleared，下一步才能走上去）
        return (w.hero.gold >= M.SHOP_PRICE.get(o, 0)), 3
    if ty == 'SAIDAN':               # 祭坛：只有 ALTAR_CELLS 里的本体可踩（献祭后英雄站在祭坛上）
        return (f, nx, ny) in M.ALTAR_CELLS, 5
    if ty == 'MONSTER':
        r = w.battle(o)
        return (r is not None and r[0] < w.hero.hp), 100
    return False, 0


def _step(w, d):
    """走一步。开门/购物/对话后英雄不移动 → 补走一步。返回 (ok, log)"""
    broke = ('blocked', '打不动', '打不过', '无', '不可通行', '买不起', '祭坛金币不足')
    b = (w.hero.f, w.hero.x, w.hero.y)
    lg = w.move(*d)
    if lg and any(t in lg[0] for t in broke):
        return False, lg
    # ⚠️ 必须连楼层一起比：3F(11,10)→4F(11,10) 坐标相同但已换层
    if (w.hero.f, w.hero.x, w.hero.y) == b and lg:
        # 交互未位移（开门 obj2/4/27、商店 SELL、祭坛 SAIDAN）→ 补一步真正走进去
        lg2 = w.move(*d)
        if lg2 and any(t in lg2[0] for t in broke):
            return False, lg2
        lg = lg + lg2
    return True, lg


def goto(w, tx, ty, label=''):
    """带权最短路（怪物 100 / 门 25 / 空 1），逐步执行。
       权重只影响"选哪条路"，不影响可达性判断；唯一通路上的怪/门照样会打/开。"""
    h = w.hero
    start = (h.x, h.y)
    if start == (tx, ty):
        return True
    import heapq
    dist = {start: 0}
    prev = {start: None}
    pq = [(0, start)]
    found = False
    while pq:
        dcur, c = heapq.heappop(pq)
        if c == (tx, ty):
            found = True
            break
        if dcur > dist.get(c, 1e9):
            continue
        for dd in DIRS:
            n = (c[0] + dd[0], c[1] + dd[1])
            ok, wc = _cost(w, h.f, *n)
            if not ok:
                continue
            nd = dcur + wc
            if nd < dist.get(n, 1e9):
                dist[n] = nd
                prev[n] = c
                heapq.heappush(pq, (nd, n))
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
        dx, dy = nx - w.hero.x, ny - w.hero.y
        f0 = w.hero.f
        ok, lg = _step(w, (dx, dy))
        if not ok:
            print('  !! 卡在 %s: %s' % (st(w.hero), lg))
            return False
        if w.hero.f != f0:
            print('  !! 层内路径误踩楼梯 %dF(%d,%d)：%s' % (f0, nx, ny, lg))
            return False
        REC.append((w.hero.f, w.hero.x, w.hero.y, w.hero.hp, w.hero.atk, w.hero.dfn,
                    w.hero.gold, w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
                    ';'.join(lg)[:80] if lg else '', '%d,%d' % (dx, dy)))
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
    global LAST_W
    w = M.World.new()
    LAST_W = w
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

    print('\n--- 4F 第一次 ---')
    if not run_segs(w, 4, S[4], '4F'): return 1
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1

    print('\n--- 5F 第一次 ---')
    if not run_segs(w, 5, S[5], '5F'): return 1
    if not stair(w, 1, 11, '5F(1,11)->4F'): return 1

    print('\n--- 4F 第二次（回）---')
    w.altar_policy = 'dfn'          # 攻略：4F 祭坛加防（D10→D14）
    if not run_segs(w, 4, S['4b'], '4F回'): return 1
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1

    print('\n--- 5F 第二次（回）---')
    if not run_segs(w, 5, S['5b'], '5F回'): return 1
    if not stair(w, 1, 1, '5F(1,1)->6F'): return 1

    print('\n--- 6F 第一次 ---')
    if not run_segs(w, 6, S[6], '6F'): return 1
    if not stair(w, 11, 11, '6F(11,11)->7F'): return 1

    print('\n--- 7F 第一次 ---')
    if not run_segs(w, 7, S[7], '7F'): return 1
    if not stair(w, 1, 1, '7F(1,1)->8F'): return 1

    print('\n--- 8F ---')
    if not run_segs(w, 8, S[8], '8F'): return 1
    if not stair(w, 6, 1, '8F(6,1)->9F'): return 1

    print('\n--- 9F 段1（→铁盾）---')
    if not run_segs(w, 9, S['9a'], '9F'): return 1

    print('\n--- 9F 补钥：下 6F 取 (9,1) 黄钥（打 (7,1) 僧侣 -32）---')
    # ⚠️ 攻略未列此步：攻略 9F「过两个黄门」假定手上有 3 把黄钥匙，本路线到 9F 只有 2 把。
    #    7F 的「5 把/50G」商人在蓝门(5,5) 之后，而蓝钥匙必须留给 11F 银盾（抉择 5），故不走。
    #    6F (9,1) 黄钥只需打 (7,1) 僧侣（60/32/8，D24 时 -32），是当前唯一不耗钥匙/金币的补充。
    if not stair(w, 6, 1, '9F(6,1)->8F'): return 1
    if not stair(w, 1, 1, '8F(1,1)->7F'): return 1
    if not stair(w, 11, 11, '7F(11,11)->6F'): return 1
    if not run_segs(w, 6, [(6, 1, ''), (7, 1, '僧侶 -32'), (9, 1, '黄钥')], '6F补钥'): return 1
    if not stair(w, 11, 11, '6F(11,11)->7F'): return 1
    if not stair(w, 1, 1, '7F(1,1)->8F'): return 1
    if not stair(w, 6, 1, '8F(6,1)->9F'): return 1

    print('\n--- 9F 段2（→赤晶/青晶，然后下 7F）---')
    if not run_segs(w, 9, S['9b'], '9F'): return 1
    if not stair(w, 6, 1, '9F(6,1)->8F'): return 1
    if not stair(w, 1, 1, '8F(1,1)->7F'): return 1

    print('\n- 7F 段2')
    if not run_segs(w, 7, S['7b'], '7F回'): return 1
    if not stair(w, 11, 11, '7F(11,11)->6F'): return 1
    if not stair(w, 1, 1, '6F(1,1)->5F'): return 1
    if not stair(w, 1, 11, '5F(1,11)->4F'): return 1
    if not stair(w, 11, 11, '4F(11,11)->3F'): return 1

    print('\n- 3F 段2')
    if not run_segs(w, 3, S['3c'], '3F回'): return 1
    if not stair(w, 11, 11, '3F(11,11)->4F'): return 1

    print('\n- 4F 段3（回）')
    if not run_segs(w, 4, S['4c'], '4F回'): return 1
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1
    if not stair(w, 1, 1, '5F(1,1)->6F'): return 1
    if not stair(w, 11, 11, '6F(11,11)->7F'): return 1
    if not stair(w, 1, 1, '7F(1,1)->8F'): return 1

    print('\n- 8F 段2（回）')
    if not run_segs(w, 8, S['8b'], '8F回'): return 1
    if not stair(w, 1, 1, '8F(1,1)->7F'): return 1
    if not stair(w, 11, 11, '7F(11,11)->6F'): return 1
    if not stair(w, 1, 1, '6F(1,1)->5F'): return 1
    if not stair(w, 1, 11, '5F(1,11)->4F'): return 1
    if not stair(w, 11, 11, '4F(11,11)->3F'): return 1
    if not stair(w, 1, 11, '3F(1,11)->2F'): return 1
    if not stair(w, 1, 1, '2F(1,1)->1F'): return 1

    print('\n- 1F 段2（回）')
    if not run_segs(w, 1, S['1b'], '1F回'): return 1
    if not stair(w, 1, 1, '1F(1,1)->2F'): return 1
    if not stair(w, 1, 11, '2F(1,11)->3F'): return 1
    if not stair(w, 11, 11, '3F(11,11)->4F'): return 1

    print('\n- 4F 段4（回）')
    if not run_segs(w, 4, S['4d'], '4F回'): return 1
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1
    if not stair(w, 1, 1, '5F(1,1)->6F'): return 1

    print('\n- 6F 段2（回）')
    if not run_segs(w, 6, S['6b'], '6F回'): return 1
    if not stair(w, 1, 1, '6F(1,1)->5F'): return 1
    if not stair(w, 1, 11, '5F(1,11)->4F'): return 1
    if not stair(w, 11, 11, '4F(11,11)->3F'): return 1

    print('\n- 3F 段3（回）')
    if not run_segs(w, 3, S['3d'], '3F回'): return 1
    if not stair(w, 11, 11, '3F(11,11)->4F'): return 1

    print('\n- 4F 段5（回）')
    if not run_segs(w, 4, S['4e'], '4F回'): return 1
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1

    print('\n- 5F 段3（回）')
    if not run_segs(w, 5, S['5c'], '5F回'): return 1
    if not stair(w, 1, 11, '5F(1,11)->4F'): return 1

    print('\n到 4F（第6次）:', st(w.hero))

    print('\n--- 4F 段6（回）：左下打绿史莱姆 → 补钥 ---')
    if not run_segs(w, 4, [(4, 8, '黄门(4,8) 已开'), (4, 9, ''), (4, 10, ''),
                           (4, 11, 'Ｇスライム -1')], '4F回'): return 1

    print('\n--- 补钥：6F 蓝钥匙(50G) → 7F 蓝门(5,5) → 5 黄钥匙(50G) ---')
    # ⚠️ 攻略未列：本路线黄钥匙账持续偏紧（9F/1F 都需要连续两把黄门）。
    #    6F(8,4) 卖蓝钥匙 50G；拿到后开 7F 蓝门(5,5)，(6,1) 卖 5 黄钥匙 50G。零 HP 代价。
    #    代价：金币 -100，蓝钥匙被 7F(5,5) 用掉 → 11F 银盾前须另找（8F(7,10) 蓝钥匙仍在）
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1
    if not stair(w, 1, 1, '5F(1,1)->6F'): return 1
    if not run_segs(w, 6, [(11, 2, '黄门(11,2)'), (11, 3, ''), (11, 4, 'バット -8'),
                           (10, 4, ''), (9, 4, ''),
                           (9, 3, ''), (8, 3, '赤薬 +50'), (8, 4, '商店：蓝钥匙 50G')], '6F买蓝钥'): return 1
    if not stair(w, 11, 11, '6F(11,11)->7F'): return 1
    if not run_segs(w, 7, [(5, 6, 'y6 走廊'), (5, 5, '蓝门(5,5)'), (5, 4, ''),
                           (5, 3, 'Ｒスライム -1'), (5, 2, ''), (6, 2, ''),
                           (6, 1, '商店：5 黄钥匙 50G')], '7F买黄钥'): return 1

    print('\n--- 下 1F（7F→6F→5F→4F→3F→2F→1F）---')
    if not stair(w, 11, 11, '7F(11,11)->6F'): return 1
    if not stair(w, 1, 1, '6F(1,1)->5F'): return 1
    if not stair(w, 1, 11, '5F(1,11)->4F'): return 1
    if not stair(w, 11, 11, '4F(11,11)->3F'): return 1
    if not stair(w, 1, 11, '3F(1,11)->2F'): return 1
    if not stair(w, 1, 1, '2F(1,1)->1F'): return 1

    print('\n到 1F（第3次）:', st(w.hero))

    print('\n- 1F 段3（回）')
    if not run_segs(w, 1, S['1c'], '1F回'): return 1
    if not stair(w, 1, 1, '1F(1,1)->2F'): return 1
    if not stair(w, 1, 11, '2F(1,11)->3F'): return 1
    if not stair(w, 11, 11, '3F(11,11)->4F'): return 1
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1
    if not stair(w, 1, 1, '5F(1,1)->6F'): return 1
    if not stair(w, 11, 11, '6F(11,11)->7F'): return 1

    print('\n到 7F（第4次）:', st(w.hero))

    print('\n- 7F 段3（回）')
    if not run_segs(w, 7, S['7c'], '7F回'): return 1
    if not stair(w, 1, 1, '7F(1,1)->8F'): return 1
    if not stair(w, 6, 1, '8F(6,1)->9F'): return 1

    print('\n到 9F（第3次）:', st(w.hero))

    print('\n- 9F 段3（回）')
    if not run_segs(w, 9, S['9c'], '9F回'): return 1
    if not stair(w, 1, 11, '9F(1,11)->10F'): return 1

    print('\n到 10F:', st(w.hero))

    print('\n- 10F 下段')
    if not run_segs(w, 10, S['10a'], '10F'): return 1

    print('\n第一区（1F-10F）收集完成:', st(w.hero))

    H = segs_route.SEGS_HEAL
    F = segs_route.SEGS_FINAL
    E = segs_route.SEGS_11

    print('\n=== BOSS 前补血路线（攻略 §4.2）===')
    print('\n--- 10F→9F 右下 ---')
    if not stair(w, 1, 11, '10F(1,11)->9F'): return 1
    if not run_segs(w, 9, H['9d'], '9F补血'): return 1

    print('\n--- 9F→4F 右上 ---')
    if not stair(w, 6, 1, '9F(6,1)->8F'): return 1
    if not stair(w, 1, 1, '8F(1,1)->7F'): return 1
    if not stair(w, 11, 11, '7F(11,11)->6F'): return 1
    if not stair(w, 1, 1, '6F(1,1)->5F'): return 1
    if not stair(w, 1, 11, '5F(1,11)->4F'): return 1
    if not run_segs(w, 4, H['4f'], '4F补血'): return 1

    print('\n--- 4F→8F 右中 ---')
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1
    if not stair(w, 1, 1, '5F(1,1)->6F'): return 1
    if not stair(w, 11, 11, '6F(11,11)->7F'): return 1
    if not stair(w, 1, 1, '7F(1,1)->8F'): return 1
    if not run_segs(w, 8, H['8c'], '8F补血'): return 1

    print('\n--- 8F→7F 右数第3列 ---')
    if not stair(w, 1, 1, '8F(1,1)->7F'): return 1
    if not run_segs(w, 7, H['7d'], '7F补血'): return 1

    print('\n--- 7F→1F 右下 ---')
    if not stair(w, 11, 11, '7F(11,11)->6F'): return 1
    if not stair(w, 1, 1, '6F(1,1)->5F'): return 1
    if not stair(w, 1, 11, '5F(1,11)->4F'): return 1
    if not stair(w, 11, 11, '4F(11,11)->3F'): return 1
    if not stair(w, 1, 11, '3F(1,11)->2F'): return 1
    if not stair(w, 1, 1, '2F(1,1)->1F'): return 1
    if not run_segs(w, 1, H['1d'], '1F补血'): return 1

    print('\n--- 上 10F ---')
    if not stair(w, 1, 1, '1F(1,1)->2F'): return 1
    if not stair(w, 1, 11, '2F(1,11)->3F'): return 1
    if not stair(w, 11, 11, '3F(11,11)->4F'): return 1
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1
    if not stair(w, 1, 1, '5F(1,1)->6F'): return 1
    if not stair(w, 11, 11, '6F(11,11)->7F'): return 1
    if not stair(w, 1, 1, '7F(1,1)->8F'): return 1
    if not stair(w, 6, 1, '8F(6,1)->9F'): return 1
    if not stair(w, 1, 11, '9F(1,11)->10F'): return 1

    print('\n=== 10F 决战 ===')
    if not run_segs(w, 10, F['10b'], '10F决战'): return 1
    if not stair(w, 6, 11, '10F(6,11)->11F（BOSS 死后上行梯）'): return 1

    print('\n★★ 第一区完成，进 11F:', st(w.hero))

    print('\n--- 11F 第一趟（右下蓝药 + 左下 5 黄钥）---')
    if not run_segs(w, 11, E['11a'], '11F'): return 1
    if not stair(w, 11, 11, '11F(11,11)->12F'): return 1

    print('\n--- 12F 蓝钥匙（11F 银盾的门票）---')
    if not run_segs(w, 12, E['12a'], '12F'): return 1
    if not stair(w, 11, 11, '12F(11,11)->11F'): return 1

    print('\n--- 11F 第二趟（蓝门(2,8) → 蓝药 → 银盾）---')
    if not run_segs(w, 11, E['11b'], '11F银盾'): return 1

    print('\n--- 回 12F 祭坛献攻 4 次 ---')
    w.altar_policy = 'atk'          # 4F 用默认 dfn；12F 起改为加攻
    if not goto(w, 11, 10, '11F 到(11,10)'): return 1
    if not stair(w, 11, 11, '11F(11,11)->12F'): return 1
    if not run_segs(w, 12, E['12b'], '12F祭坛'): return 1
    if not stair(w, 11, 11, '12F(11,11)->11F'): return 1

    print('\n--- 11F 第三趟（红药x2 + 黄钥 + 红晶）---')
    if not run_segs(w, 11, E['11c'], '11F清怪'): return 1

    print('--- 12F -> 13F 熔岩层 -> 14F ---')
    if not stair(w, 11, 11, '11F(11,11)->12F'): return 1
    if not stair(w, 1, 11, '12F(1,11)->13F'): return 1
    if not run_segs(w, 13, E['13a'], '13F'): return 1
    if not stair(w, 11, 11, '13F(11,11)->14F'): return 1
    if not run_segs(w, 14, E['14a'], '14F'): return 1
    if not stair(w, 6, 11, '14F(6,11)->15F'): return 1

    print('--- 15F 右侧环线 -> 盗贼凿墙 ---')
    if not run_segs(w, 15, E['15a'], '15F'): return 1

    # ---------------- 下塔收尾：1F-10F 剩余血药 + 钥匙（8F(7,10) 还有 1 把蓝钥匙）----------------
    print(chr(10) + '--- 下塔 15F -> 3F ---')
    if not goto(w, 6, 10, '15F 回(6,10)'): return 1
    if not stair(w, 6, 11, '15F(6,11)->14F'): return 1
    if not goto(w, 11, 10, '14F 到(11,10)'): return 1
    if not stair(w, 11, 11, '14F(11,11)->13F'): return 1
    if not goto(w, 2, 11, '13F 到(2,11)'): return 1
    if not stair(w, 1, 11, '13F(1,11)->12F'): return 1
    if not goto(w, 10, 11, '12F 到(10,11)'): return 1
    if not stair(w, 11, 11, '12F(11,11)->11F'): return 1
    if not goto(w, 6, 10, '11F 到(6,10)'): return 1
    if not stair(w, 6, 11, '11F(6,11)->10F'): return 1
    if not goto(w, 1, 10, '10F 到(1,10)'): return 1
    if not stair(w, 1, 11, '10F(1,11)->9F'): return 1
    if not goto(w, 6, 2, '9F 到(6,2)'): return 1
    if not stair(w, 6, 1, '9F(6,1)->8F'): return 1
    if not goto(w, 1, 2, '8F 到(1,2)'): return 1
    if not stair(w, 1, 1, '8F(1,1)->7F'): return 1
    if not goto(w, 11, 10, '7F 到(11,10)'): return 1
    if not stair(w, 11, 11, '7F(11,11)->6F'): return 1
    if not goto(w, 1, 2, '6F 到(1,2)'): return 1
    if not stair(w, 1, 1, '6F(1,1)->5F'): return 1
    if not goto(w, 2, 11, '5F 到(2,11)'): return 1
    if not stair(w, 1, 11, '5F(1,11)->4F'): return 1
    if not goto(w, 11, 10, '4F 到(11,10)'): return 1
    if not stair(w, 11, 11, '4F(11,11)->3F'): return 1

    print(chr(10) + '--- 3F 收红药/黄钥 ---')
    if not goto(w, 11, 8, '3F 黄钥(11,8)'): return 1
    if not goto(w, 11, 7, '3F 红药(11,7)'): return 1
    if not goto(w, 11, 1, '3F 红药(11,1)'): return 1
    if not goto(w, 10, 11, '3F 回下梯旁'): return 1

    print(chr(10) + '--- 回程 3F -> 8F（收 8F 蓝钥匙）---')
    if not stair(w, 11, 11, '3F(11,11)->4F'): return 1
    if not goto(w, 1, 10, '4F 到(1,10)'): return 1
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1
    if not goto(w, 1, 3, '5F 到(1,3)'): return 1
    if not stair(w, 1, 1, '5F(1,1)->6F'): return 1
    if not goto(w, 11, 10, '6F 到(11,10)'): return 1
    if not stair(w, 11, 11, '6F(11,11)->7F'): return 1
    if not goto(w, 1, 2, '7F 到(1,2)'): return 1
    if not stair(w, 1, 1, '7F(1,1)->8F'): return 1
    # 8F 右下区内部有 (9,11) 黄门，而 (11,9) 黄门已耗掉最后一把黄钥匙
    #   → 先上 9F 取 (2,2) 黄钥，再回 8F 开 (9,11)，拿蓝钥匙/红药/黄钥
    if not goto(w, 11, 9, '8F 到(11,9) 黄门'): return 1
    if not goto(w, 6, 2, '8F 回(6,2)'): return 1
    if not stair(w, 6, 1, '8F(6,1)->9F'): return 1
    if not goto(w, 2, 2, '9F 黄钥(2,2)'): return 1
    if not goto(w, 6, 2, '9F 回(6,2)'): return 1
    if not stair(w, 6, 1, '9F(6,1)->8F'): return 1
    if not goto(w, 11, 11, '8F 回右下区(11,11)'): return 1
    if not goto(w, 9, 11, '8F 黄门(9,11)'): return 1
    if not goto(w, 8, 10, '8F 红药 +50'): return 1
    if not goto(w, 7, 10, '8F ★蓝钥匙'): return 1
    if not goto(w, 7, 11, '8F 黄钥'): return 1
    if not goto(w, 6, 2, '8F 回(6,2)'): return 1
    if not stair(w, 6, 1, '8F(6,1)->9F'): return 1
    if not goto(w, 1, 10, '9F 到(1,10)'): return 1
    if not stair(w, 1, 11, '9F(1,11)->10F'): return 1

    # ---------- 刷金币：1F-10F 剩余小怪（ATK41/DEF51 下多数 -0~-2 HP）----------
    #   ⚠️ 攻略没有这一步。11F-20F 的 ATK 缺口（起点 ATK77 vs 本路线 ATK41）只能靠
    #      12F 祭坛第 4 次献祭（220G）补，而金币需要自己赚。
    #      这批怪性价比极高：合计 112G / 18 HP。
    print(chr(10) + '--- 刷金币：10F/9F/8F/7F/6F 剩余小怪 ---')
    for (x2, y2, nm) in [(2, 7, 'スケルトンＢ'), (10, 7, 'スケルトンＢ'), (11, 6, 'スケルトンＣ')]:
        goto(w, x2, y2, '10F ' + nm)
    if not goto(w, 1, 10, '10F 回下梯旁'): return 1
    if not stair(w, 1, 11, '10F(1,11)->9F'): return 1

    for (x2, y2, nm) in [(3, 1, 'スケルトンＣ'), (10, 10, 'スケルトンＣ'),
                         (11, 6, 'スケルトンＢ'), (10, 2, 'Ｇスライム')]:
        goto(w, x2, y2, '9F ' + nm)
    if not goto(w, 6, 2, '9F 回下梯旁'): return 1
    if not stair(w, 6, 1, '9F(6,1)->8F'): return 1

    for (x2, y2, nm) in [(7, 2, 'Ｇスライム'), (9, 5, '門番Ｃ'), (11, 5, '門番Ｃ')]:
        goto(w, x2, y2, '8F ' + nm)
    if not goto(w, 1, 2, '8F 回下梯旁'): return 1
    if not stair(w, 1, 1, '8F(1,1)->7F'): return 1

    for (x2, y2, nm) in [(3, 10, 'Ｇスライム'), (7, 3, 'スケルトンＢ'),
                         (2, 11, 'Ｒスライム'), (11, 2, 'Ｒスライム')]:
        goto(w, x2, y2, '7F ' + nm)
    if not goto(w, 11, 10, '7F 回下梯旁'): return 1
    if not stair(w, 11, 11, '7F(11,11)->6F'): return 1

    for (x2, y2, nm) in [(9, 6, 'スケルトンＢ'), (8, 6, 'スケルトンＣ'),
                         (10, 3, 'スケルトンＣ'), (1, 8, '僧侶')]:
        goto(w, x2, y2, '6F ' + nm)
    print('刷金币完成:', st(w.hero))

    # ---------- 回 12F 献祭坛第 4 次（220G）→ ATK45 ----------
    print(chr(10) + '--- 回 12F 祭坛第 4 次 ---')
    if not goto(w, 11, 10, '6F 到(11,10)'): return 1
    if not stair(w, 11, 11, '6F(11,11)->7F'): return 1
    if not goto(w, 1, 2, '7F 到(1,2)'): return 1
    if not stair(w, 1, 1, '7F(1,1)->8F'): return 1
    if not goto(w, 6, 2, '8F 到(6,2)'): return 1
    if not stair(w, 6, 1, '8F(6,1)->9F'): return 1
    if not goto(w, 1, 10, '9F 到(1,10)'): return 1
    if not stair(w, 1, 11, '9F(1,11)->10F'): return 1
    if not goto(w, 6, 10, '10F 到(6,10)'): return 1
    if not stair(w, 6, 11, '10F(6,11)->11F'): return 1
    if not goto(w, 11, 10, '11F 到(11,10)'): return 1
    if not stair(w, 11, 11, '11F(11,11)->12F'): return 1
    if not goto(w, 6, 10, '12F 到祭坛下邻格'): return 1
    if not goto(w, 6, 9, '祭坛献攻 #4 -220G'): return 1
    if not goto(w, 6, 10, '退出祭坛'): return 1

    # ---------- 上 16F ----------
    print(chr(10) + '--- 12F -> 16F ---')
    if not goto(w, 2, 11, '12F 到(2,11)'): return 1
    if not stair(w, 1, 11, '12F(1,11)->13F'): return 1
    if not goto(w, 10, 11, '13F 到(10,11)'): return 1
    if not stair(w, 11, 11, '13F(11,11)->14F'): return 1
    if not goto(w, 6, 10, '14F 到(6,10)'): return 1
    if not stair(w, 6, 11, '14F(6,11)->15F'): return 1
    if not goto(w, 7, 1, '15F 到(7,1) 凿墙后'): return 1
    if not stair(w, 6, 1, '15F(6,1)->16F'): return 1

    # ---------- 16F ----------
    #   攻略 §三「16F 黄钥×5、蓝钥匙(11,7)、青晶、红药、红晶ATK+2」
    #   PC-98 实测：y=4 整行只有 (6,4) 蓝门 与 (10,4) 黄门（后者所在区封闭），
    #   故 (6,6) ゾンビナイト 是上下半区唯一通路（ATK45 → 11 回合 -690）。
    print(chr(10) + '--- 16F ---')
    # ⚠️ 主动放弃 (8,2) 黄门后的红药(11,3) +100 与 Ｂスライム：
    #    黄钥匙在 17F 是硬通货——(2,10) 黄门后面是 銀の剣 ATK+20（本路线 ATK 唯一大补）。
    #    用 1 把黄钥匙换 +100 HP 不如换 +20 ATK。
    if not goto(w, 7, 3, '16F 黄钥(7,3)'): return 1
    if not goto(w, 6, 3, '16F 回 x6'): return 1
    if not goto(w, 6, 4, '16F 蓝门(6,4)'): return 1
    if not goto(w, 5, 5, '16F 红药(5,5) +100'): return 1
    if not goto(w, 7, 7, '16F 黄钥(7,7)'): return 1
    if not goto(w, 6, 6, '16F ★ゾンビナイト(6,6)'): return 1
    if not goto(w, 6, 7, '16F 下半区'): return 1
    if not goto(w, 6, 8, '16F 黄门(6,8)'): return 1
    if not goto(w, 6, 10, '16F 上梯旁'): return 1
    if not stair(w, 6, 11, '16F(6,11)->17F'): return 1

    # ---------- 17F ----------
    #   落点 (6,10) 是 down 梯 (6,11) 上方的孤立格：只能经 (5,10)/(7,10) 走 y11 走廊，
    #   或穿 (6,9) 上級僧侶。主目标：★銀の剣 (2,2) ATK+20（攻略 §三「17F 蓝药+400(10,2)」的
    #   蓝药在右侧区，需先开 (10,10) 黄门，本路线黄钥不足 → 放弃）。
    print(chr(10) + '--- 17F ---')
    if not goto(w, 5, 11, '17F 到(5,11)'): return 1
    if not goto(w, 2, 11, '17F 经大バット(4,11)'): return 1
    if not goto(w, 1, 11, '17F 红药(1,11) +100'): return 1
    if not goto(w, 2, 10, '17F 黄门(2,10)'): return 1
    if not goto(w, 2, 7, '17F 落穴(2,7)'): return 1
    if not goto(w, 2, 4, '17F 落穴(2,4)'): return 1
    if not goto(w, 2, 2, '17F ★銀の剣 ATK+20'): return 1
    if not goto(w, 2, 11, '17F 回 y11 走廊'): return 1
    if not goto(w, 7, 11, '17F 到(7,11)'): return 1
    if not goto(w, 11, 11, '17F 红药(11,11) +100'): return 1
    if not goto(w, 7, 10, '17F 回(7,10)'): return 1
    if not goto(w, 6, 9, '17F 上級僧侶(6,9)'): return 1
    if not goto(w, 7, 7, '17F Ｂスライム(7,7)'): return 1
    if not goto(w, 7, 6, '17F 到(7,6)'): return 1
    # 蓝钥匙已在 16F(6,4) 用掉，(7,5) 蓝门开不了。
    # → 先去打 17F 四只門番Ｃ（ATK65/DEF51 下每只 -1 HP / 12G），凑 15F 商店的 200G 蓝钥匙
    if not goto(w, 2, 11, '17F 回 y11'): return 1
    for (x2, y2, nm) in [(1, 11, ''), (2, 6, ''), (1, 5, '門番Ｃ'), (3, 5, '門番Ｃ'),
                         (1, 8, '門番Ｃ'), (3, 8, '門番Ｃ')]:
        goto(w, x2, y2, '17F 刷金 ' + nm)
    print('17F 刷金后:', st(w.hero))

    # ---------- 下 15F 拿蓝药 +400（ATK65 后 (11,6) 上級僧侶 只 -88，净 +312）----------
    print(chr(10) + '--- 下 15F 蓝药(11,8) ---')
    if not goto(w, 7, 11, '17F 回(7,11)'): return 1
    if not stair(w, 6, 11, '17F(6,11)->16F'): return 1
    if not goto(w, 6, 2, '16F 到(6,2)'): return 1
    if not stair(w, 6, 1, '16F(6,1)->15F'): return 1
    for (x2, y2, nm) in [(6, 10, ''), (7, 10, ''), (7, 11, ''), (8, 11, ''), (9, 11, ''),
                         (9, 10, ''), (9, 9, ''), (9, 8, ''), (9, 7, ''), (9, 6, ''),
                         (9, 5, ''), (9, 4, ''), (10, 4, ''), (11, 4, ''),
                         (11, 5, ''), (11, 6, '上級僧侶 -88'), (11, 7, ''),
                         (11, 8, '★蓝药 +400')]:
        goto(w, x2, y2, '15F ' + nm)
    print('15F 蓝药后:', st(w.hero))

    # ---------- 回 17F 打 (5,7) ゾンビ（18G），凑够 200G 买蓝钥匙 ----------
    print(chr(10) + '--- 回 17F 打ゾンビ凑金币 ---')
    for (x2, y2, nm) in [(11, 7, ''), (11, 6, ''), (11, 5, ''), (11, 4, ''), (10, 4, ''),
                         (9, 4, ''), (9, 5, ''), (9, 6, ''), (9, 7, ''), (9, 8, ''),
                         (9, 9, ''), (9, 10, ''), (9, 11, ''), (10, 11, ''), (8, 11, ''),
                         (7, 11, ''), (6, 11, '')]:
        goto(w, x2, y2, '15F 回 ' + nm)
    if not stair(w, 6, 11, '15F(6,11)->14F'): return 1
    if not goto(w, 11, 10, '14F 到(11,10)'): return 1
    if not stair(w, 11, 11, '14F(11,11)->13F'): return 1
    if not goto(w, 2, 11, '13F 到(2,11)'): return 1
    if not stair(w, 1, 11, '13F(1,11)->12F'): return 1
    if not goto(w, 10, 11, '12F 到(10,11)'): return 1
    if not stair(w, 11, 11, '12F(11,11)->11F'): return 1
    if not goto(w, 11, 10, '11F 到(11,10)'): return 1
    if not stair(w, 11, 11, '11F(11,11)->12F'): return 1
    if not goto(w, 2, 11, '12F 到(2,11)'): return 1
    if not stair(w, 1, 11, '12F(1,11)->13F'): return 1
    if not goto(w, 10, 11, '13F 到(10,11)'): return 1
    if not stair(w, 11, 11, '13F(11,11)->14F'): return 1
    if not goto(w, 6, 10, '14F 到(6,10)'): return 1
    if not stair(w, 6, 11, '14F(6,11)->15F'): return 1
    if not goto(w, 7, 1, '15F 到(7,1)'): return 1
    if not stair(w, 6, 1, '15F(6,1)->16F'): return 1
    if not goto(w, 6, 2, '16F 到(6,2)'): return 1
    if not goto(w, 6, 10, '16F 到(6,10)'): return 1
    if not stair(w, 6, 11, '16F(6,11)->17F'): return 1
    if not goto(w, 6, 9, '17F 到(6,9)'): return 1
    if not goto(w, 6, 8, '17F 到(6,8)'): return 1
    if not goto(w, 5, 7, '17F ゾンビ(5,7) 18G'): return 1
    print('凑金币后:', st(w.hero))

    # ---------- 下 15F(11,11) 商店买蓝钥匙（200G）----------
    print(chr(10) + '--- 下 15F 买蓝钥匙 ---')
    if not goto(w, 6, 10, '17F 到(6,10)'): return 1
    if not stair(w, 6, 11, '17F(6,11)->16F'): return 1
    if not goto(w, 6, 2, '16F 到(6,2)'): return 1
    if not stair(w, 6, 1, '16F(6,1)->15F'): return 1
    for (x2, y2, nm) in [(7, 2, ''), (7, 1, ''), (8, 1, ''), (9, 1, ''), (9, 2, ''),
                         (10, 2, ''), (11, 2, ''), (11, 3, ''), (11, 4, ''), (10, 4, ''),
                         (9, 4, ''), (9, 5, ''), (9, 6, ''), (9, 7, ''), (9, 8, ''),
                         (9, 9, ''), (9, 10, ''), (9, 11, ''), (10, 11, ''),
                         (11, 11, '★商店：蓝钥匙 200G')]:
        goto(w, x2, y2, '15F ' + nm)
    print('买蓝钥匙后:', st(w.hero))
    if w.hero.keys['b'] < 1:
        print('  !! 蓝钥匙没买到，金币=%d' % w.hero.gold); return 1

    # ---------- 回 17F 开 (7,5) 蓝门 → 上 18F ----------
    print(chr(10) + '--- 回 17F 开蓝门上 18F ---')
    for (x2, y2) in [(10, 11), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (9, 6),
                     (9, 5), (9, 4), (10, 4), (11, 4), (11, 3), (11, 2), (10, 2),
                     (9, 2), (9, 1), (8, 1), (7, 1), (7, 2), (6, 2), (6, 10),
                     (7, 10), (7, 11)]:
        goto(w, x2, y2, '15F 回(6,10)')
    if not stair(w, 6, 11, '15F(6,11)->14F'): return 1
    if not goto(w, 11, 10, '14F 到(11,10)'): return 1
    if not stair(w, 11, 11, '14F(11,11)->13F'): return 1
    if not goto(w, 2, 11, '13F 到(2,11)'): return 1
    if not stair(w, 1, 11, '13F(1,11)->12F'): return 1
    if not goto(w, 10, 11, '12F 到(10,11)'): return 1
    if not stair(w, 11, 11, '12F(11,11)->11F'): return 1
    if not goto(w, 11, 10, '11F 到(11,10)'): return 1
    if not stair(w, 11, 11, '11F(11,11)->12F'): return 1
    if not goto(w, 2, 11, '12F 到(2,11)'): return 1
    if not stair(w, 1, 11, '12F(1,11)->13F'): return 1
    if not goto(w, 10, 11, '13F 到(10,11)'): return 1
    if not stair(w, 11, 11, '13F(11,11)->14F'): return 1
    if not goto(w, 6, 10, '14F 到(6,10)'): return 1
    if not stair(w, 6, 11, '14F(6,11)->15F'): return 1
    if not goto(w, 7, 1, '15F 到(7,1)'): return 1
    if not stair(w, 6, 1, '15F(6,1)->16F'): return 1
    if not goto(w, 6, 10, '16F 到(6,10)'): return 1
    if not stair(w, 6, 11, '16F(6,11)->17F'): return 1
    if not goto(w, 6, 9, '17F 到(6,9)'): return 1
    if not goto(w, 7, 6, '17F 到(7,6)'): return 1
    if not goto(w, 7, 5, '17F 蓝门(7,5)'): return 1
    if not goto(w, 7, 3, '17F 大バット(7,3)'): return 1
    if not goto(w, 6, 2, '17F 上梯旁'): return 1
    if not stair(w, 6, 1, '17F(6,1)->18F'): return 1

    return 0
    if not goto(w, 7, 3, '17F 大バット(7,3)'): return 1
    if not goto(w, 6, 2, '17F 上梯旁'): return 1
    if not stair(w, 6, 1, '17F(6,1)->18F'): return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
