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


# ---- 逐格 TRACE 录制（供 build_current.py 生成 merged_route.json）----
TRACE = []          # 每步：dict(floor,x,y,dir,before,after,cl,log,kind)
TRACE_LAST = set()  # 上一步的 w.cleared，用于算本步新消耗格
RECORDING = os.environ.get('RECORD_TRACE') == '1'


def _snap(h):
    return dict(hp=h.hp, atk=h.atk, dfn=h.dfn, gold=h.gold,
                ky=h.keys.get('y', 0), kb=h.keys.get('b', 0), kr=h.keys.get('r', 0),
                items=sorted(h.items))


def _delta(a, b):
    return dict(hp=b['hp'] - a['hp'], atk=b['atk'] - a['atk'], dfn=b['dfn'] - a['dfn'],
                gold=b['gold'] - a['gold'], ky=b['ky'] - a['ky'],
                kb=b['kb'] - a['kb'], kr=b['kr'] - a['kr'])


def _trace(w, before, dch, lg, kind='move'):
    """记录一步：before/after 快照 + 本步新消耗格 + 日志。"""
    global TRACE_LAST
    if not RECORDING:
        return
    after = _snap(w.hero)
    cl = sorted(w.cleared - TRACE_LAST)
    TRACE_LAST = set(w.cleared)
    TRACE.append(dict(floor=w.hero.f, x=w.hero.x, y=w.hero.y, dir=dch,
                      before=before, after=after, cl=cl,
                      log=';'.join(lg) if lg else '', kind=kind))



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
    if o == 20 and (f, nx, ny) in M.PIT_GUARD_CLEAR:
        # ✅ 2026-11-14 落穴 obj20：守卫未清则实心挡路（原版 @3780-3845）。
        _gd = M.PIT_GUARD_CLEAR[(f, nx, ny)]
        if not all((f, gx, gy) in w.cleared for gx, gy in _gd):
            return False, 0
    if o in M.KEY_OF or ty in ('STATUS', 'ITEM', 'NORMAL', 'SCORE', 'MESSAGE'):
        return True, 1
    if ty == 'DOOR':
        col = M.DOOR_OF.get(o)
        return (col is not None and w.hero.keys[col] > 0), 25
    if ty == 'SELL':                 # 商店：钱够即可谈（谈完该格 cleared，下一步才能走上去）
        return (w.hero.gold >= M.SHOP_PRICE.get(o, 0)), 3
    if ty == 'SAIDAN':               # 祭坛本体不可走格（Java 面朝触发，face_altar 处理）
        return False, 0
    if ty == 'MONSTER':
        r = w.battle(o)
        return (r is not None and r[0] < w.hero.hp), 100
    return False, 0


def _step(w, d):
    """走一步。开门/购物后英雄不移动 → 补走一步。返回 (ok, log)
    ✅ 2026-11-13：祭坛不再走格触发（Java directCheck 面朝触发，face_altar 处理），
    补步逻辑只覆盖开门/商店。"""
    broke = ('blocked', '打不动', '打不过', '无', '不可通行', '买不起', '祭坛金币不足')
    b = (w.hero.f, w.hero.x, w.hero.y)
    before = _snap(w.hero)
    lg = w.move(*d)
    if lg and any(t in lg[0] for t in broke):
        return False, lg
    # ⚠️ 必须连楼层一起比：3F(11,10)→4F(11,10) 坐标相同但已换层
    if (w.hero.f, w.hero.x, w.hero.y) == b and lg \
            and not any('祭坛' in t for t in lg):
        # 交互未位移（开门 obj2/4/27、商店 SELL）→ 补一步真正走进去
        lg2 = w.move(*d)
        if lg2 and any(t in lg2[0] for t in broke):
            return False, lg2
        lg = lg + lg2
    _trace(w, before, d, lg, 'move')
    return True, lg


def _dist_to(w, tx, ty):
    """到 (tx,ty) 的 Dijkstra 距离（与 goto 同权重；不可达返回 None）。只读，不改状态。"""
    import heapq
    h = w.hero
    start = (h.x, h.y)
    if start == (tx, ty):
        return 0
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        dcur, c = heapq.heappop(pq)
        if c == (tx, ty):
            return dcur
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
                heapq.heappush(pq, (nd, n))
    return None


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
    """走到**最近**的楼梯邻格再踏上。
    ⚠️ 2026-11-14：原实现按 (0,1)(0,-1)(1,0)(-1,0) 固定顺序取第一个可站邻格，
       25F 上梯 (1,11) 会先取 (1,10)，导致从落点 (2,11) 绕外圈 38 步；
       现改为按 Dijkstra 距离取最近邻格（与 goto 同一套 _cost 权重）。"""
    h = w.hero
    cands = []
    for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        ax, ay = sx + d[0], sy + d[1]
        if not (1 <= ax <= 11 and 1 <= ay <= 11):
            continue
        if not _passable(w, h.f, ax, ay):
            continue
        cands.append((ax, ay))
    best = None
    for (ax, ay) in cands:
        d = _dist_to(w, ax, ay)
        if d is None:
            continue
        if best is None or d < best[0]:
            best = (d, ax, ay)
    if best is None:
        print('  !! 楼梯 %dF(%d,%d) 无可达入口' % (h.f, sx, sy))
        return False
    ax, ay = best[1], best[2]
    if not goto(w, ax, ay):
        print('  !! 楼梯 %dF(%d,%d) 无可达入口' % (h.f, sx, sy))
        return False
    ok, lg = _step(w, (sx - w.hero.x, sy - w.hero.y))
    if not ok:
        print('  !! 上楼梯失败: %s' % lg)
        return False
    REC.append((w.hero.f, w.hero.x, w.hero.y, w.hero.hp, w.hero.atk, w.hero.dfn,
                w.hero.gold, w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
                ';'.join(lg)[:80] if lg else '', 'stair'))
    print('  %-22s %s' % (label, st(w.hero)))
    return True


def fly(w, target_f, label=''):
    """飞行之珠 obj26：英雄须站在当前层楼梯旁，传送到 target_f（落点 FLY_LAND）。"""
    h = w.hero
    before = _snap(w.hero)
    lg = w.fly(target_f)
    # 失败消息形如「飞行之珠：尚未持有…」「飞行之珠：目标层…」「飞行之珠：须站在…」（带全角冒号）；
    # 成功消息是「飞行之珠传送 → …」（无冒号）。用「飞行之珠：」或「无法」判定失败。
    if lg and ('飞行之珠：' in lg[0] or '无法' in lg[0]):
        print('  !! 飞行失败 %dF→%dF: %s' % (h.f, target_f, lg))
        return False
    _trace(w, before, '·', lg, 'fly')
    REC.append((w.hero.f, w.hero.x, w.hero.y, w.hero.hp, w.hero.atk, w.hero.dfn,
                w.hero.gold, w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
                ';'.join(lg)[:80], 'FLY'))
    print('  %-22s %s' % (label, st(w.hero)))
    return True


def wing_up(w, label=''):
    """同层飞行器 obj107 昇華の翼：瞬移到本层上行梯旁踏出格（同层，不动层）。"""
    h = w.hero
    before = _snap(w.hero)
    lg = w.wing_up()
    if lg and ('尚未持有' in lg[0] or '无上行梯' in lg[0] or '无可走邻格' in lg[0]):
        print('  !! 昇華の翼失败: %s' % lg)
        return False
    _trace(w, before, '·', lg, 'wing')
    REC.append((w.hero.f, w.hero.x, w.hero.y, w.hero.hp, w.hero.atk, w.hero.dfn,
                w.hero.gold, w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
                ';'.join(lg)[:80], 'WING'))
    print('  %-22s %s' % (label, st(w.hero)))
    return True


def run_segs(w, f, segs, tag=''):
    for (x, y, lab) in segs:
        if not goto(w, x, y, '%s(%d,%d) %s' % (tag or '%dF' % f, x, y, lab)):
            return False
    return True


def main():
    global LAST_W, TRACE_LAST
    if RECORDING:
        TRACE.clear()
        TRACE_LAST = set()
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
    # ✅ 2026-11-13 祭坛面朝触发：4b1 走到祭坛邻格 (6,2) → 原地 face_altar(6,1)
    #    献防 DEF+4 → 14 → 4b2 原路回下梯（Java directCheck：人物不移动，零位移）
    if not run_segs(w, 4, S['4b1'], '4F回'): return 1
    lg = w.face_altar(6, 1)
    print('  4F祭坛(面朝):', ';'.join(lg))
    if any(('不足' in t or '错误' in t or '必须' in t) for t in lg): return 1
    if not run_segs(w, 4, S['4b2'], '4F回'): return 1
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

    print('\n- 7F x9 列上方支路【提前】（原 7c 段前移）')
    # ✅ 2026-11-14 提前清理 7F x9 列上方支路，把 2 把黄钥 + 血瓶+50 提前 ~880 步，
    #    使 Toy 1019（1F）能凑够 3 把黄钥提前拿飛行のオーブ（obj26）。
    #    代价：骷髅C(9,5) 在 A23/D27 打掉 -30（原 7c 段 A26/D30 时 -24，多 6 HP）；
    #    血瓶(9,3)+50 立即回补，净 +20 HP。原 7c 段同步缩短为仅下方支路（净 0 步）。
    if not run_segs(w, 7, [
        (9, 6, 'x9 竖列'),
        (9, 5, 'スケルトンＣ -30'),
        (9, 4, ''),
        (9, 3, '赤薬 +50'),
        (9, 2, '黄钥'),
        (9, 1, '黄钥'),
        (9, 6, '回 x9'),
    ], '7F上方支路'): return 1
    if not stair(w, 11, 11, '7F(11,11)->6F'): return 1
    if not stair(w, 1, 1, '6F(1,1)->5F'): return 1
    if not stair(w, 1, 11, '5F(1,11)->4F'): return 1
    if not stair(w, 11, 11, '4F(11,11)->3F'): return 1
    if not stair(w, 1, 11, '3F(1,11)->2F'): return 1
    if not stair(w, 1, 1, '2F(1,1)->1F'): return 1

    print('\n- 1F 段2（回）')
    if not run_segs(w, 1, S['1b'], '1F回'): return 1

    print('\n- 1F 拿飛行のオーブ【提前】（原 1c 段前移）')
    # ✅ 2026-11-14 把 1F 西区（含 obj26 飛行のオーブ）从第 3 次 1F 访（'1c'，Toy~1637）
    #    前移到第 2 次访末尾（'1b' 后，Toy~1053，英雄 A24/D28、HP97、黄钥 3）。
    #    目的：orb 提前 ~600 步到手，供 1019 之后的空爬楼换 fly() 跳层（省步主体）。
    #    首访检查：1F 西区(x1-4)在 '1' 首访/'1b' 二访均未触及（'1' 注释明示"飞行之珠留到 1c"），
    #    此处在西区首访，血瓶/骷髅/orb/钥匙全部在位。代价：骷髅C/B 在 A24/D28 打（-28/-96，
    #    原 1637 时 A26/D30 -24/-66），HP97+50(血瓶1,3)-28-96+100=123，全程不掉负。
    #    '1c' 原位置（Toy~1590）同步移除。
    if not run_segs(w, 1, S['1c'], '1F拿orb'): return 1
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

    print('\n- 1F 段3（回）：1c（含 orb）已前移到段2末，本处直接上 2F')
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

    print('\n--- 4F→7F 右数第3列（7F补血提前到 8F 門番Ｃ 之前）---')
    # ✅ 2026-11-14 修复 orb 前移 -20 HP 赤字：把 7F补血（青薬+200）提前到 8F补血
    #    （2 只門番Ｃ -306）之前，使进 8F 时 HP≥306 满足。地理上 7F 在 4F→8F 途中，
    #    步数净 0，仅调整补血顺序。
    if not stair(w, 1, 11, '4F(1,11)->5F'): return 1
    if not stair(w, 1, 1, '5F(1,1)->6F'): return 1
    if not stair(w, 11, 11, '6F(11,11)->7F'): return 1
    if not run_segs(w, 7, H['7d'], '7F补血'): return 1

    print('\n--- 7F→8F 右中（門番Ｃ 口袋）---')
    if not stair(w, 1, 1, '7F(1,1)->8F'): return 1
    if not run_segs(w, 8, H['8c'], '8F补血'): return 1

    print('\n--- 8F→7F→1F 右下（7F补血已提前完成，本处直接穿行下 1F）---')
    if not stair(w, 1, 1, '8F(1,1)->7F'): return 1
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

    if os.environ.get('MOTA_STOP_11F') == '1':
        return 0

# ⚠️ 2026-11-13：原 11F→47F 旧版路线（16F 绕行/17F 宝库等）整体移除。
#   成品链 = z2_route.py（V1~V2x 忠实重译），只复用本文件的 1F→11F 重放（MOTA_STOP_11F 截断）。
#   旧版 run_segs_bak.py 已随死代码清理删除（2026-11-13）。



if __name__ == '__main__':
    sys.exit(main())
