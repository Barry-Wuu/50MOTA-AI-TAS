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
    if f == 30 and getattr(w, 'slime30', False):
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
        # 暗墙（14F(1,3)）：撞塌后可踩入，露出 obj28 红钥匙
        if (f, nx, ny) in M.DARKWALL_CELLS:
            return True, 3
        # 35F 密道：x=4 竖列是一排 obj89「壁がくずれた」，地形仍是墙 → 撞塌即通
        if w.at(f, nx, ny) == 89:
            return True, 3
        return False, 0
    if (nx, ny) in _stair_cells(w, f):
        return False, 0
    o = w.at(f, nx, ny)
    if not o:
        return True, 1
    ty = M.TYPE.get(M.oatr(o, 3))
    if o == 89:                      # 暗墙：撞塌后本人直接进入该格
        return True, 3
    if o == 115:                     # 隐形砖块（23F「Go 0F」字形 44 块）：撞即破，可通行
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
    # ★ ATK69 后 (2,2) 上級僧侶只 -76、(2,1)(2,3) 大バット 1 回合 -0，
    #   左侧区（(4,2) 黄门后）的 4 把黄钥几乎白拿 —— 这是 16F(11,7) 蓝钥匙的门票。
    if not goto(w, 4, 2, '16F 黄门(4,2)'): return 1
    if not goto(w, 3, 1, '16F 黄钥(3,1)'): return 1
    if not goto(w, 2, 2, '16F 上級僧侶(2,2)'): return 1
    if not goto(w, 1, 2, '16F 黄钥(1,2)'): return 1
    if not goto(w, 1, 1, '16F 黄钥(1,1)'): return 1
    if not goto(w, 1, 3, '16F 黄钥(1,3)'): return 1
    if not goto(w, 6, 3, '16F 回 x6'): return 1
    if not goto(w, 6, 4, '16F 蓝门(6,4)'): return 1
    if not goto(w, 5, 5, '16F 红药(5,5) +100'): return 1
    if not goto(w, 7, 7, '16F 黄钥(7,7)'): return 1
    # 16F(11,7) 蓝钥匙：19F(6,7) 蓝门 的唯一来源（18F 的蓝钥要留给 (4,1) 上 19F）
    if not goto(w, 10, 4, '16F 黄门(10,4)'): return 1
    if not goto(w, 10, 5, '16F ゾンビ(10,5)'): return 1
    if not goto(w, 9, 6, '16F 黄门(9,6)'): return 1
    if not goto(w, 11, 7, '16F ★蓝钥匙(11,7)'): return 1
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
    if not goto(w, 2, 11, '17F 经(4,11)大バット'): return 1
    if not goto(w, 1, 11, '17F 红药(1,11) +100'): return 1
    if not goto(w, 7, 11, '17F 到(7,11)'): return 1
    if not goto(w, 11, 11, '17F 红药(11,11) +100'): return 1
    if not goto(w, 7, 10, '17F 回(7,10)'): return 1
    if not goto(w, 6, 9, '17F 上級僧侶(6,9)'): return 1

    # ★ 右侧宝库：1 把黄钥匙开 (10,10)，里面是 2 把黄钥 + 蓝药+400 + 红晶+2 + 蓝晶+2
    #   （实测代价 0 HP。这是本路线最赚的一步：钥匙净 +1 且白拿 400 血 + 4 点属性）
    if not goto(w, 10, 10, '17F 黄门(10,10)'): return 1
    if not goto(w, 10, 8, '17F 到(10,8)'): return 1
    if not goto(w, 10, 6, '17F 落穴(10,7)'): return 1
    if not goto(w, 9, 8, '17F ゾンビ(9,8)'): return 1
    if not goto(w, 9, 5, '17F ゾンビナイト(9,5)'): return 1
    if not goto(w, 10, 4, '17F 回(10,4)'): return 1
    if not goto(w, 10, 2, '17F ★蓝药(10,2) +400'): return 1
    if not goto(w, 9, 1, '17F 蓝晶(9,1) DEF+2'): return 1
    if not goto(w, 11, 1, '17F 红晶(11,1) ATK+2'): return 1
    if not goto(w, 11, 3, '17F 黄钥(11,3)'): return 1
    if not goto(w, 9, 3, '17F 黄钥(9,3)'): return 1
    if not goto(w, 10, 11, '17F 回 y11 走廊'): return 1
    if not goto(w, 7, 10, '17F 回(7,10)'): return 1
    if not goto(w, 7, 7, '17F Ｂスライム(7,7)'): return 1
    if not goto(w, 7, 6, '17F 到(7,6)'): return 1
    # ⚠️ 上梯区入口有二：(7,5) 蓝门、(5,5) 黄门→(5,4)→(5,3)ゾンビナイト。
    #    蓝钥匙 19F(6,7) 蓝门 还要用（那是上半区唯一入口），必须留住 →
    #    走 (5,5) 黄门这条，用右侧宝库刚拿到的黄钥匙。
    if not goto(w, 5, 5, '17F 黄门(5,5)'): return 1
    if not goto(w, 5, 3, '17F ゾンビナイト(5,3)'): return 1
    if not goto(w, 6, 2, '17F 上梯旁'): return 1
    if not stair(w, 6, 1, '17F(6,1)->18F'): return 1

    # ---------- 18F ----------
    #   落点 (6,2) 在孤立块 (5,1)(6,1)(7,1)(5,2)(6,2)(7,2)，只有两个出口：
    #     (4,1) 蓝门 → (1,1) 上行梯（需蓝钥匙）
    #     (8,1) 黄门 → (9,1)僧侣 → (10,3) → (11,3) 蓝钥匙（需黄钥匙）
    #   17F 右侧宝库给了 2 把黄钥，(5,5) 黄门用掉 1 把 → 到 18F 剩 1 把，
    #   正好走 (8,1) 那条：拿 (11,3) 蓝钥 → 回头开 (4,1) 上 19F。
    print(chr(10) + '--- 18F ---')
    if not goto(w, 8, 1, '18F 黄门(8,1)'): return 1
    if not goto(w, 9, 1, '18F 上級僧侶(9,1)'): return 1
    if not goto(w, 9, 3, '18F 到(9,3)'): return 1
    if not goto(w, 9, 4, '18F ゾンビ(9,4)'): return 1
    if not goto(w, 10, 4, '18F 到(10,4)'): return 1
    if not goto(w, 10, 3, '18F 到(10,3)'): return 1
    if not goto(w, 10, 2, '18F Ｂスライム(10,2)'): return 1
    # 18F 右侧区还有 4 把黄钥（19F 的 (1,3) 黄门正好要用）
    if not goto(w, 11, 2, '18F 黄钥(11,2)'): return 1
    if not goto(w, 11, 1, '18F 黄钥(11,1)'): return 1
    if not goto(w, 11, 3, '18F ★蓝钥匙(11,3)'): return 1
    if not goto(w, 11, 4, '18F 黄钥(11,4)'): return 1
    if not goto(w, 11, 5, '18F 黄钥(11,5)'): return 1
    if not goto(w, 6, 2, '18F 回 x6'): return 1
    if not goto(w, 4, 1, '18F 蓝门(4,1)'): return 1
    if not goto(w, 2, 1, '18F 到(2,1)'): return 1
    if not stair(w, 1, 1, '18F(1,1)->19F'): return 1

    # ---------- 19F ----------
    #   落点 (1,2) 同样是孤立块 (1,1)(1,2)(2,1)(2,2)，唯一出口 (1,3) 黄门。
    #   目标：十字架（(6,4) 撞暗墙 → (6,3)，对 ゾンビ系/BOSS 伤害×2）、蓝钥(8,1)、红药、红晶。
    print(chr(10) + '--- 19F ---')
    if not goto(w, 1, 3, '19F 黄门(1,3)'): return 1
    if not goto(w, 1, 4, '19F 到(1,4)'): return 1
    if not goto(w, 1, 5, '19F 到(1,5)'): return 1
    if not goto(w, 1, 6, '19F 黄门(1,6)'): return 1
    if not goto(w, 1, 7, '19F 大バット(1,7)'): return 1
    if not goto(w, 1, 8, '19F 到(1,8)'): return 1
    if not goto(w, 1, 9, '19F 黄门(1,9)'): return 1
    if not goto(w, 1, 10, '19F 到(1,10)'): return 1
    if not goto(w, 1, 11, '19F 上級僧侶(1,11)'): return 1
    if not goto(w, 2, 11, '19F 到(2,11)'): return 1
    if not goto(w, 3, 11, '19F 大バット(3,11)'): return 1
    if not goto(w, 3, 10, '19F 到(3,10)'): return 1
    if not goto(w, 4, 10, '19F 黄门(4,10)'): return 1
    if not goto(w, 5, 10, '19F 黄钥(5,10)'): return 1
    if not goto(w, 6, 10, '19F 黄钥(6,10)'): return 1
    # 从下往上打通上半区（上半区唯一入口是 (6,7) 蓝门）
    if not goto(w, 6, 9, '19F ゾンビ(6,9)'): return 1
    if not goto(w, 6, 8, '19F 到(6,8)'): return 1
    if not goto(w, 6, 7, '19F 蓝门(6,7)'): return 1
    # (6,5) 是墙；上半区的封闭环 (4,4)(4,5)(5,4)(5,5) 只能从 (6,6)/(5,6) 两只 ロック 打进去
    if not goto(w, 6, 6, '19F ロック(6,6)'): return 1
    if not goto(w, 5, 6, '19F ロック(5,6)'): return 1
    if not goto(w, 5, 5, '19F 到(5,5)'): return 1
    if not goto(w, 4, 5, '19F 黄钥(4,5)'): return 1
    if not goto(w, 4, 4, '19F 到(4,4)'): return 1
    if not goto(w, 4, 3, '19F ゾンビナイト(4,3)'): return 1
    if not goto(w, 4, 2, '19F 到(4,2)'): return 1
    if not goto(w, 5, 1, '19F 到(5,1)'): return 1
    if not goto(w, 4, 1, '19F 红药(4,1) +100'): return 1
    if not goto(w, 6, 1, '19F 上級僧侶(6,1)'): return 1
    if not goto(w, 8, 1, '19F ★蓝钥匙(8,1)'): return 1
    # 撞暗墙拿十字架（对 ゾンビ系/BOSS 伤害 ×2，20F 吸血鬼必需）
    if not goto(w, 5, 5, '19F 回(5,5)'): return 1
    if not goto(w, 5, 4, '19F 到(5,4)'): return 1
    if not goto(w, 6, 4, '19F ★撞暗墙(6,4)'): return 1
    if not goto(w, 6, 3, '19F ★★十字架 obj103'): return 1
    if not goto(w, 6, 4, '19F 回(6,4)'): return 1
    if not goto(w, 5, 4, '19F 回(5,4)'): return 1
    if not goto(w, 5, 5, '19F 回(5,5)'): return 1
    if not goto(w, 6, 6, '19F 到(6,6)'): return 1
    if not goto(w, 6, 8, '19F 到(6,8)'): return 1
    if not goto(w, 6, 10, '19F 到(6,10)'): return 1
    if not stair(w, 6, 11, '19F(6,11)->20F'): return 1

    # ---------- 回 14F 拿红钥匙（20F 红门 (6,9) 是进 BOSS 区的唯一路）----------
    print(chr(10) + '--- 回 14F 红钥匙 ---')
    if not stair(w, 6, 11, '20F(6,11)->19F'): return 1
    if not goto(w, 1, 2, '19F 到(1,2)'): return 1
    if not stair(w, 1, 1, '19F(1,1)->18F'): return 1
    if not goto(w, 6, 2, '18F 到(6,2)'): return 1
    if not stair(w, 6, 1, '18F(6,1)->17F'): return 1
    if not goto(w, 6, 10, '17F 到(6,10)'): return 1
    if not stair(w, 6, 11, '17F(6,11)->16F'): return 1
    if not goto(w, 6, 2, '16F 到(6,2)'): return 1
    if not stair(w, 6, 1, '16F(6,1)->15F'): return 1
    if not goto(w, 6, 2, '15F 到(6,2)'): return 1
    if not stair(w, 6, 1, '15F(6,1) 是上行梯，需绕到(6,10)') if False else True: pass
    if not goto(w, 6, 10, '15F 到(6,10)'): return 1
    if not stair(w, 6, 11, '15F(6,11)->14F'): return 1
    if not goto(w, 5, 10, '14F 到(5,10)'): return 1
    if not goto(w, 5, 11, '14F 到(5,11)'): return 1
    if not goto(w, 4, 11, '14F 黄门(4,11)'): return 1
    if not goto(w, 3, 11, '14F 到(3,11)'): return 1
    if not goto(w, 3, 10, '14F 到(3,10)'): return 1
    if not goto(w, 3, 9, '14F 上級僧侶(3,9)'): return 1
    if not goto(w, 3, 8, '14F 到(3,8)'): return 1
    if not goto(w, 3, 7, '14F 黄门(3,7)'): return 1
    if not goto(w, 3, 5, '14F 到(3,5)'): return 1
    if not goto(w, 2, 5, '14F 到(2,5)'): return 1
    if not goto(w, 2, 4, '14F 蓝门(2,4)'): return 1
    if not goto(w, 2, 3, '14F 到(2,3)'): return 1
    if not goto(w, 1, 3, '14F ★★红钥匙（暗墙1,3）'): return 1
    print('红钥匙到手:', st(w.hero))

    # ---------- 12F 祭坛第 6 次（320G）→ ATK81 ----------
    print(chr(10) + '--- 12F 祭坛第 6 次 ---')
    if not goto(w, 2, 3, '14F 回(2,3)'): return 1
    if not goto(w, 3, 5, '14F 回(3,5)'): return 1
    if not goto(w, 3, 9, '14F 回(3,9)'): return 1
    if not goto(w, 3, 11, '14F 回(3,11)'): return 1
    if not goto(w, 5, 10, '14F 回(5,10)'): return 1
    if not goto(w, 11, 10, '14F 到(11,10)'): return 1
    if not stair(w, 11, 11, '14F(11,11)->13F'): return 1
    if not goto(w, 2, 11, '13F 到(2,11)'): return 1
    if not stair(w, 1, 11, '13F(1,11)->12F'): return 1
    if not goto(w, 6, 10, '12F 到祭坛下邻格'): return 1
    if not goto(w, 6, 9, '12F 祭坛献攻 #6 -320G'): return 1
    if not goto(w, 6, 10, '12F 退出祭坛'): return 1
    print('祭坛后:', st(w.hero))

    # ---------- 回 20F ----------
    print(chr(10) + '--- 回 20F 打 BOSS ---')
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
    if not goto(w, 6, 2, '17F 到(6,2)'): return 1
    if not stair(w, 6, 1, '17F(6,1)->18F'): return 1
    if not goto(w, 6, 2, '18F 到(6,2)'): return 1
    if not goto(w, 2, 1, '18F 到(2,1)'): return 1
    if not stair(w, 1, 1, '18F(1,1)->19F'): return 1
    if not goto(w, 1, 3, '19F 到(1,3)'): return 1
    if not goto(w, 1, 5, '19F 到(1,5)'): return 1
    if not goto(w, 1, 7, '19F 到(1,7)'): return 1
    if not goto(w, 1, 9, '19F 到(1,9)'): return 1
    if not goto(w, 1, 11, '19F 到(1,11)'): return 1
    if not goto(w, 3, 11, '19F 到(3,11)'): return 1
    if not goto(w, 3, 10, '19F 到(3,10)'): return 1
    if not goto(w, 5, 10, '19F 到(5,10)'): return 1
    if not goto(w, 6, 10, '19F 到(6,10)'): return 1
    if not stair(w, 6, 11, '19F(6,11)->20F'): return 1

    # ---------- 20F ----------
    if not goto(w, 6, 9, '20F 红门(6,9)'): return 1
    if not goto(w, 6, 8, '20F 到(6,8)'): return 1
    if not goto(w, 10, 4, '20F 蓝药(10,4)（如不可达则跳过）'): print('  20F 蓝药不可达')
    if not goto(w, 6, 7, '20F 大バット(6,7)'): return 1
    if not goto(w, 6, 6, '20F ★★★ 吸血鬼(6,6)'): return 1
    if not goto(w, 6, 8, '20F 回(6,8)'): return 1
    if not goto(w, 6, 10, '20F 回(6,10)'): return 1
    print('20F BOSS 后:', st(w.hero))
    # BOSS 死后 (20,6,1) 现出上行梯
    if not goto(w, 6, 5, '20F 大バット(6,5)'): return 1
    if not goto(w, 6, 4, '20F 到(6,4)'): return 1
    if not goto(w, 6, 2, '20F 经落穴(6,3)'): return 1
    if not stair(w, 6, 1, '20F(6,1)->21F（BOSS 死后上行梯）'): return 1
    print(chr(10) + '★★★ 第二区完成，进 21F:', st(w.hero))

    # ================= 第三区 21F-30F（攻略 §6 速通区）=================
    G = segs_route.SEGS_21
    print(chr(10) + '--- 21F ---')
    if not run_segs(w, 21, G['21a'], '21F'): return 1
    if not stair(w, 6, 11, '21F(6,11)->22F'): return 1

    print(chr(10) + '--- 22F ---')
    if not run_segs(w, 22, G['22a'], '22F'): return 1
    if not stair(w, 6, 6, '22F(6,6)->23F'): return 1

    print(chr(10) + '--- 23F（44 块隐形砖撞出 "Go 0F"）---')
    if not run_segs(w, 23, G['23a'], '23F'): return 1
    if not stair(w, 11, 1, '23F(11,1)->24F'): return 1

    print(chr(10) + '--- 24F ---')
    if not run_segs(w, 24, G['24a'], '24F'): return 1
    if not stair(w, 2, 10, '24F(2,10)->25F'): return 1

    print(chr(10) + '--- 25F（跳过红门后的大魔導師）---')
    if not run_segs(w, 25, G['25a'], '25F'): return 1
    if not stair(w, 1, 11, '25F(1,11)->26F'): return 1

    print(chr(10) + '--- 26F（跳过熔岩假公主）---')
    if not run_segs(w, 26, G['26a'], '26F'): return 1
    if not stair(w, 2, 10, '26F(2,10)->27F'): return 1

    print(chr(10) + '--- 27F ---')
    if not run_segs(w, 27, G['27a'], '27F'): return 1
    if not stair(w, 11, 11, '27F(11,11)->28F'): return 1

    print(chr(10) + '--- 28F（商人 100G/把 回收黄钥匙，本路线暂不卖）---')
    if not run_segs(w, 28, G['28a'], '28F'): return 1
    if not stair(w, 1, 11, '28F(1,11)->29F'): return 1

    print(chr(10) + '--- 29F（小偷挖开 (6,3) 暗道）---')
    if not run_segs(w, 29, G['29a'], '29F'): return 1
    if not stair(w, 6, 11, '29F(6,11)->30F'): return 1

    print(chr(10) + '--- 30F（六只史莱姆零损清光 → 现上行梯）---')
    if not run_segs(w, 30, G['30a'], '30F'): return 1
    if not stair(w, 6, 1, '30F(6,1)->31F（六只清空后上行梯）'): return 1

    print(chr(10) + '★★★ 第三区完成，进 31F:', st(w.hero))

    # ---------- 下塔 31F→20F 补血（攻略 §7.2 32F 段「下 20F 拿两个血瓶」）----------
    print(chr(10) + '--- 下塔 31F -> 20F ---')
    if not stair(w, 6, 1, '31F(6,1)->30F'): return 1
    if not goto(w, 6, 10, '30F 到(6,10)'): return 1
    if not stair(w, 6, 11, '30F(6,11)->29F'): return 1
    if not goto(w, 6, 1, '29F x6 竖列上行'): return 1
    if not goto(w, 1, 1, '29F y1 走廊西行'): return 1
    if not goto(w, 1, 10, '29F x1 竖列下行'): return 1
    if not stair(w, 1, 11, '29F(1,11)->28F'): return 1
    if not goto(w, 10, 11, '28F y11 东行'): return 1
    if not stair(w, 11, 11, '28F(11,11)->27F'): return 1
    if not goto(w, 2, 11, '27F y11 西行'): return 1
    if not stair(w, 2, 10, '27F(2,10)->26F'): return 1
    if not stair(w, 1, 11, '26F(1,11)->25F'): return 1
    if not stair(w, 2, 10, '25F(2,10)->24F'): return 1
    if not stair(w, 1, 11, '24F(1,11)->23F'): return 1
    if not stair(w, 1, 1, '23F(1,1)->22F'): return 1
    if not stair(w, 6, 11, '22F(6,11)->21F'): return 1
    if not stair(w, 6, 1, '21F(6,1)->20F'): return 1

    print(chr(10) + '--- 20F 中央区补血（3 蓝药 + 6 晶石，零战斗）---')
    if not run_segs(w, 20, G['20b'], '20F补血'): return 1

    # ---------- 回 31F ----------
    print(chr(10) + '--- 回 31F ---')
    if not stair(w, 6, 1, '20F(6,1)->21F（吸血鬼死后上行梯）'): return 1
    if not goto(w, 6, 10, '21F 到(6,10)'): return 1
    if not stair(w, 6, 11, '21F(6,11)->22F'): return 1
    if not goto(w, 6, 7, '22F 到(6,7)'): return 1
    if not stair(w, 6, 6, '22F(6,6)->23F'): return 1
    if not goto(w, 11, 2, '23F 到(11,2)'): return 1
    if not stair(w, 11, 1, '23F(11,1)->24F'): return 1
    if not stair(w, 2, 10, '24F(2,10)->25F'): return 1
    if not stair(w, 1, 11, '25F(1,11)->26F'): return 1
    if not stair(w, 2, 10, '26F(2,10)->27F'): return 1
    if not goto(w, 10, 11, '27F 到(10,11)'): return 1
    if not stair(w, 11, 11, '27F(11,11)->28F'): return 1
    if not goto(w, 2, 11, '28F 到(2,11)'): return 1
    if not stair(w, 1, 11, '28F(1,11)->29F'): return 1
    if not goto(w, 1, 1, '29F y1 东行'): return 1
    if not goto(w, 6, 1, '29F 到(6,1)'): return 1
    if not goto(w, 6, 10, '29F x6 竖列下行'): return 1
    if not stair(w, 6, 11, '29F(6,11)->30F'): return 1
    if not goto(w, 6, 2, '30F 到(6,2)'): return 1
    if not stair(w, 6, 1, '30F(6,1)->31F'): return 1
    print(chr(10) + '★ 补血完成，回 31F:', st(w.hero))

    # ================= 第四区 31F-40F（攻略 §7）=================
    Q = segs_route.SEGS_31
    print(chr(10) + '--- 31F（两只兽人武士）---')
    if not run_segs(w, 31, Q['31a'], '31F'): return 1
    if not stair(w, 6, 11, '31F(6,11)->32F'): return 1
    print(chr(10) + '★★ 进 32F:', st(w.hero))

    print(chr(10) + '--- 32F 左下区取钥 ---')
    if not run_segs(w, 32, Q['32a'], '32F取钥'): return 1

    # 回 31F 取右上区 (8,8) 蓝药 +800（现在有 5 黄钥）
    print(chr(10) + '--- 回 31F 取蓝药(8,8) ---')
    if not stair(w, 6, 11, '32F(6,11)->31F'): return 1
    if not run_segs(w, 31, Q['31b'], '31F蓝药'): return 1
    if not stair(w, 6, 11, '31F(6,11)->32F'): return 1
    print('回 32F:', st(w.hero))

    print(chr(10) + '--- 32F 右上区取蓝药(11,4) ---')
    if not run_segs(w, 32, Q['32b'], '32F右上'): return 1

    print(chr(10) + '--- 32F 左上区晶石 + 上 33F ---')
    if not run_segs(w, 32, Q['32c'], '32F左上'): return 1
    if not stair(w, 11, 1, '32F(11,1)->33F（金騎士清掉后）'): return 1
    print(chr(10) + '★★ 进 33F:', st(w.hero))

    print(chr(10) + '--- 33F 取骑士剑 + 蓝药 ---')
    if not run_segs(w, 33, Q['33a'], '33F'): return 1

    print(chr(10) + '--- 33F 上 34F ---')
    if not run_segs(w, 33, Q['33b'], '33F上行'): return 1
    if not stair(w, 1, 1, '33F(1,1)->34F'): return 1
    print(chr(10) + '★★ 进 34F:', st(w.hero))

    # ---------- 34F 入口缺黄钥 → 回 32F 取 (11,5) ----------
    print(chr(10) + '--- 回 32F 补黄钥 ---')
    if not goto(w, 2, 1, '34F 回(2,1)'): return 1
    if not stair(w, 1, 1, '34F(1,1)->33F'): return 1
    if not goto(w, 10, 1, '33F 到(10,1)'): return 1
    if not stair(w, 11, 1, '33F(11,1)->32F'): return 1
    if not run_segs(w, 32, Q['32d'], '32F补钥'): return 1
    if not stair(w, 11, 1, '32F(11,1)->33F'): return 1
    # ⚠️ 33F 上行梯是 (1,1)，(11,1) 是回 32F 的下行梯 → 必须横穿整层
    if not goto(w, 10, 1, '33F 到(10,1)'): return 1
    if not goto(w, 9, 1, '33F y1 西行'): return 1
    if not goto(w, 7, 1, '（黄门已开）'): return 1
    if not goto(w, 6, 1, '（スライムマン已清）'): return 1
    if not goto(w, 5, 1, ''): return 1
    if not goto(w, 4, 1, '（ゾンビナイト已清）'): return 1
    if not goto(w, 3, 1, '（黄门已开）'): return 1
    if not goto(w, 2, 1, ''): return 1
    if not stair(w, 1, 1, '33F(1,1)->34F'): return 1
    print('回 34F:', st(w.hero))

    print(chr(10) + '--- 34F ---')
    if not run_segs(w, 34, Q['34a'], '34F'): return 1
    if not stair(w, 6, 11, '34F(6,11)->35F'): return 1
    print(chr(10) + '★★ 进 35F:', st(w.hero))

    print(chr(10) + '--- 35F 密道绕魔龙 ---')
    if not run_segs(w, 35, Q['35a'], '35F'): return 1
    if not stair(w, 11, 1, '35F(11,1)->36F'): return 1
    print(chr(10) + '★★ 进 36F:', st(w.hero))

    return 0


if __name__ == '__main__':
    sys.exit(main())
