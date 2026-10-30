# -*- coding: utf-8 -*-
"""手推执行器（不做任何自动决策）：
  - 只沿"纯地板/拾取格"走（自动拾取途中的药/晶/钥匙，免费）
  - 战斗、开门、撞暗墙、祭坛、商店、上楼梯，全部由 PLAN 里逐条指定
  - 每条动作后打印 HP/ATK/DEF/G/钥匙/坐标，便于逐行核对
用法:
  python manual.py            执行 PLAN
  python manual.py reach      执行 PLAN 后列出"可达自由格邻接的怪物/门"（决策参考，不做选择）
"""
import sys, io, csv
from collections import deque

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
sys.path.insert(0, TOOLS)
import mota_core as M

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DNAME = {(1, 0): 'R', (-1, 0): 'L', (0, 1): 'D', (0, -1): 'U'}
FAIL = ('blocked', '打不动', '打不过', '无', '买不起', '熔岩烫死', '祭坛金币不足')
rows_rec = list(csv.DictReader(io.open(SRC + '魔塔1_route_1F到21F.csv', encoding='utf-8-sig')))
W = M.World.new()


def pick_move(r):
    tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
    rec = dict(atk=int(r['atk']), dfn=int(r['def']), gold=int(r['gold']),
               ky=int(r['ky']), kb=int(r['kb']), kr=int(r['kr']))
    h = W.hero
    same = (h.f, h.x, h.y) == (tf, tx, ty)
    best = None
    for d in DIRS:
        c = W.clone(); lg = c.move(*d)
        if lg and lg[0].startswith(FAIL): continue
        hh = c.hero; sc = 0
        if (hh.f, hh.x, hh.y) == (tf, tx, ty): sc += 8
        elif same and (hh.f, hh.x, hh.y) == (h.f, h.x, h.y) and lg: sc += 4
        else: continue
        for k, cur in (('atk', hh.atk), ('dfn', hh.dfn), ('gold', hh.gold)):
            if cur == rec[k]: sc += 1
        for k, kk in (('ky', 'y'), ('kb', 'b'), ('kr', 'r')):
            if hh.keys.get(kk, 0) == rec[k]: sc += 1
        if bool(lg) == bool((r['event'] or '').strip()): sc += 1
        if best is None or sc > best[0]: best = (sc, d)
    return best


# ---- 前奏（2026-10-30 重写）：不再重放含非法穿门的录制，改用已验证的扒装+越狱脚本。
#      从全新世界出发：plan2(avoid) 到 3F 落点 → 手工踩 (5,9) 触发扒装 → 越狱 → 2F(1,10)。
import route_build as _RB
_esc = _RB.plan2(lambda f, x, y: f == 3, goal_cell=(3, 2, 11), max_states=200000, trap_mode='avoid')
if not _esc or (isinstance(_esc, tuple) and _esc[0] == 'cap'):
    raise RuntimeError('到3F落点失败: %s' % (_esc,))
W, _pp = _esc
W.trap_mode = 'apply'
PREAMBLE_MOVES = list(_pp)                              # plan2(avoid) 1F→3F落点 的真实动作
for (a, b) in [(3, 11), (4, 11), (5, 11), (5, 10), (5, 9)]:
    dx, dy = a - W.hero.x, b - W.hero.y
    lg = W.move(dx, dy)
    PREAMBLE_MOVES.append((dx, dy))
    if lg and lg[0].startswith(FAIL):
        raise RuntimeError('触发扒装卡在 %dF(%d,%d): %s' % (W.hero.f, a, b, lg[:1]))
# 越狱：从扒装落点 2F(4,8) → (3,8) → (3,7) 盗贼 → (2,7)(1,7)(1,8)(1,9)(1,10)
# （2026-10-30 修复：原 (4,8)→(3,7) 是斜穿非法动作，改为合法 4 方向两步）
for (a, b) in [(3, 8), (3, 7), (2, 7), (1, 7), (1, 8), (1, 9), (1, 10)]:
    dx, dy = a - W.hero.x, b - W.hero.y
    lg = W.move(dx, dy)
    PREAMBLE_MOVES.append((dx, dy))
    if lg and lg[0].startswith(FAIL):
        raise RuntimeError('越狱卡在 2F(%d,%d): %s' % (a, b, lg[:1]))

STEPS = [0]
LOG = []


def st():
    h = W.hero
    return 'HP%-5d A%-3d D%-3d G%-4d 钥%d/%d/%d %dF(%d,%d)' % (
        h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y)


def free(f, x, y):
    if not (0 <= x < 13 and 0 <= y < 13):
        return False
    t = W.terrain_at(f, x, y)
    if t == 1 or t == 2:
        return False
    o = W.at(f, x, y)
    if o == 0:
        return True
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if o == 89 or o == 19 or o == 79:
        return False
    if o in M.KEY_OF:
        return True
    if ty in ('STATUS', 'ITEM'):
        return True
    if ty in ('NORMAL', 'SCORE', 'MESSAGE'):
        return True
    return False


def bfs(f, start, goal):
    if start == goal:
        return []
    prev = {start: None}
    q = deque([start])
    while q:
        c = q.popleft()
        for d in DIRS:
            n = (c[0] + d[0], c[1] + d[1])
            if n in prev:
                continue
            if not free(f, n[0], n[1]):
                continue
            prev[n] = (c, d)
            if n == goal:
                path = []
                while prev[n] is not None:
                    p, dd = prev[n]
                    path.append(dd)
                    n = p
                return list(reversed(path))
            q.append(n)
    return None


def walk(f, goal, quiet=False):
    h = W.hero
    path = bfs(f, (h.x, h.y), goal)
    if path is None:
        raise RuntimeError('不可达 %dF%s（当前 %s）' % (f, goal, (h.x, h.y)))
    for d in path:
        lg = W.move(*d)
        if lg and lg[0].startswith(FAIL):
            raise RuntimeError('行走失败 %s -> %s' % ((h.x, h.y), lg))
        STEPS[0] += 1
        for e in lg:
            if e.startswith(('拾取', '拾 ', 'NPC', '踩', '撞击', '撞塌', '隐形', '盗賊', '购物', '祭坛')):
                LOG.append('    · ' + e)


def adj_free(f, x, y):
    cand = []
    for d in DIRS:
        n = (x + d[0], y + d[1])
        if free(f, n[0], n[1]):
            cand.append(n)
    return cand


def approach(f, x, y):
    """走到目标格的可达自由邻格（选最近的那个）。"""
    h = W.hero
    best = None
    for c in adj_free(f, x, y):
        p = bfs(f, (h.x, h.y), c)
        if p is None:
            continue
        if best is None or len(p) < len(best[1]):
            best = (c, p)
    if best is None:
        raise RuntimeError('目标 %dF(%d,%d) 无可达邻格' % (f, x, y))
    walk(f, best[0])


def enter(f, x, y, label):
    """从当前格朝目标格走一步（战斗/开门/撞墙/祭坛/购物）。"""
    h = W.hero
    dx, dy = x - h.x, y - h.y
    if abs(dx) + abs(dy) != 1:
        raise RuntimeError('%s: 不在邻格 %s vs (%d,%d)' % (label, (h.x, h.y), x, y))
    o = W.at(f, x, y)
    lg = W.move(dx, dy)
    STEPS[0] += 1
    if lg and lg[0].startswith(FAIL):
        raise RuntimeError('%s 失败: %s' % (label, lg))
    return o, lg


def info(o):
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if ty == 'MONSTER':
        return '%s(%d/%d/%d)' % (M.oname(o), M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12))
    return '%s obj%d' % (M.oname(o)[:10], o)


# ---------------------------------------------------------------- PLAN
PLAN = [
    # ---- 3F：按人类攻略基线（400→1000 吃蓝瓶，打绿史莱姆→老头→红史莱姆→黄门→上楼）
    ('s', 2, 1, 11, '2F(1,11) 上行梯 → 3F'),
    # 上中房 3×3(x4-6,y1-3)：3 蓝瓶(+600) + 5 黄钥 + 1 蓝钥，全吃
    ('w', 3, 5, 3, '上中房：蓝钥匙'),
    ('w', 3, 4, 3, '黄钥匙'),
    ('w', 3, 4, 2, '蓝药 +200'),
    ('w', 3, 4, 1, '黄钥匙'),
    ('w', 3, 5, 1, '蓝药 +200'),
    ('w', 3, 6, 1, '黄钥匙'),
    ('w', 3, 6, 2, '蓝药 +200'),
    ('w', 3, 6, 3, '黄钥匙'),
    ('w', 3, 5, 2, '黄钥匙'),
    ('w', 3, 5, 5, '回中厅'),
    ('m', 3, 7, 5, 'G史莱姆（开右廊入口）'),
    ('w', 3, 8, 5, '进入右廊 x8'),
    ('w', 3, 11, 4, '老头：勇者のオーブ(鑑定器)'),
    ('w', 3, 8, 5, '回右廊'),
    ('w', 3, 8, 9, '下到右廊底'),
    ('m', 3, 8, 10, 'R史莱姆'),
    ('w', 3, 8, 11, ''),
    ('d', 3, 9, 11, '黄门'),
    ('w', 3, 10, 11, ''),
    ('s', 3, 11, 11, '上行梯 → 4F'),
    # ---- 4F：落点(11,10) → 黄门(10,7) → 左行 y7 → G史莱姆(3,7) → R史莱姆(1,7) → 黄门(1,8) → 上楼
    ('d', 4, 10, 7, '黄门(10,7) 出落点小间'),
    ('w', 4, 9, 7, ''),
    ('w', 4, 4, 7, '沿 y7 西行'),
    ('m', 4, 3, 7, 'G史莱姆'),
    ('w', 4, 2, 7, ''),
    ('m', 4, 1, 7, 'R史莱姆'),
    ('d', 4, 1, 8, '黄门(1,8)'),
    ('w', 4, 1, 9, ''),
    ('s', 4, 1, 11, '上行梯 → 5F'),
    # ---- 5F 首访：落点(2,11) → x6 竖廊北上 → G(6,8) → G(7,6) → R(11,7) → 右侧房 → 黄门(8,9)
    #      → 撞暗墙(9,11) → 铁剑(11,11) → 回头 R(11,2) → 中路蝙蝠(6,4) → 钥匙(6,2) → 下行梯(1,11)
    ('w', 5, 6, 11, '落点(2,11)→x6 底'),
    ('w', 5, 6, 9, 'x6 竖廊北上'),
    ('m', 5, 6, 8, 'G史莱姆（上）'),
    ('w', 5, 6, 6, '过 (6,7) 到中路 (6,6)'),
    ('m', 5, 7, 6, 'G史莱姆（右）'),
    ('w', 5, 11, 6, '沿 y6 东行'),
    ('m', 5, 11, 7, 'R史莱姆（下）'),
    ('w', 5, 11, 8, '进入右侧房'),
    ('w', 5, 8, 8, '沿 y8 西行'),
    ('d', 5, 8, 9, '黄门(8,9)'),
    ('w', 5, 8, 11, '下到 (8,11)'),
    ('b', 5, 9, 11, '撞暗墙(9,11)'),
    ('w', 5, 11, 11, '铁剑 ATK+10'),
    ('w', 5, 11, 8, '回右侧房'),
    ('m', 5, 11, 2, 'R史莱姆（右上，回头）'),
    ('w', 5, 6, 6, '回中路'),
    ('m', 5, 6, 4, '蝙蝠（中路）'),
    ('w', 5, 6, 2, '钥匙(6,2)'),
    ('s', 5, 1, 11, '下行梯 → 4F(1,10)'),
    # ---- 4F 回补：北上 (1,6)→(3,6)→(3,5) → 黄门(4,5) → R史莱姆(6,5) → 回上行梯
    #      （抉择1：不开 4F 祭坛，省下蓝钥匙）
    ('w', 4, 1, 6, '北上到 (1,6)（(1,8) 门已开）'),
    ('w', 4, 3, 6, ''),
    ('w', 4, 3, 5, '到 (3,5)'),
    ('d', 4, 4, 5, '黄门(4,5)'),
    ('w', 4, 5, 5, ''),
    ('m', 4, 6, 5, 'R史莱姆（4F 回补）'),
    ('s', 4, 1, 11, '上行梯 → 5F'),
    # ---- 5F 第二遍：落点→x6 中路→y6 东行→x11 北上(11,1)→黄门(10,1)→G(8,2)（只打一只）
    #      →取 4 黄钥匙→原路回→x6 北上(6,1)→黄门(5,1)→R(4,1)→蝙蝠(3,3)→黄门(2,3)→上行梯(1,1)
    ('w', 5, 6, 6, '落点→x6 中路'),
    ('w', 5, 11, 6, '沿 y6 东行'),
    ('w', 5, 11, 1, '上 x11 竖列到 (11,1)'),
    ('d', 5, 10, 1, '黄门(10,1)'),
    ('w', 5, 8, 1, '到 (8,1)'),
    ('m', 5, 8, 2, 'G史莱姆（右上，只打一只）'),
    ('w', 5, 9, 3, '取钥匙 (8,3)(9,3)'),
    ('w', 5, 8, 4, '取钥匙 (9,4)(8,4)'),
    ('w', 5, 9, 4, '补取 (9,4) 钥匙'),
    ('w', 5, 11, 6, '原路回 (11,6)'),
    ('w', 5, 6, 1, '沿 y6 西行 → x6 北上到 (6,1)'),
    ('d', 5, 5, 1, '黄门(5,1)'),
    ('m', 5, 4, 1, 'R史莱姆(4,1)'),
    ('w', 5, 4, 3, '到 (4,3)'),
    ('m', 5, 3, 3, '蝙蝠(3,3)'),
    ('d', 5, 2, 3, '黄门(2,3)'),
    ('w', 5, 1, 2, '到 (1,2)'),
    ('s', 5, 1, 1, '上行梯 → 6F(1,2)'),
    # ---- 6F：落点(1,2)→x1 南下(1,4)→黄门(2,4)(3,4)→R(4,3)→左上 4 钥匙→黄门(5,4)→x6 南下
    #      →钥匙(6,6)→(6,8)→黄门(7,8)(8,8)→R(9,9)→双红瓶(9,11)(8,11)→黄门(10,8)→R(11,9)→上行梯(11,11)
    #      （右上法师+蝙蝠只为 1 钥匙+1 红瓶，净耗约 94 血，跳过）
    ('w', 6, 1, 4, '落点(1,2) 南下到 (1,4)'),
    ('d', 6, 2, 4, '黄门(2,4)'),
    ('d', 6, 3, 4, '黄门(3,4)'),
    ('w', 6, 4, 4, '到 (4,4)'),
    ('m', 6, 4, 3, 'R史莱姆(4,3)'),
    ('w', 6, 4, 1, '取钥匙 (4,2)(4,1)'),
    ('w', 6, 3, 2, '取钥匙 (3,1)(3,2)'),
    ('d', 6, 5, 4, '黄门(5,4)'),
    ('w', 6, 6, 4, '到 (6,4)'),
    ('w', 6, 6, 6, 'x6 南下拿钥匙(6,6)'),
    ('w', 6, 6, 8, 'x6 继续南下到 (6,8)'),
    ('d', 6, 7, 8, '黄门(7,8)'),
    ('d', 6, 8, 8, '黄门(8,8)'),
    ('w', 6, 9, 8, '到 (9,8)'),
    ('m', 6, 9, 9, 'R史莱姆(9,9)'),
    ('w', 6, 9, 11, '取红瓶(9,11)'),
    ('w', 6, 8, 11, '取红瓶(8,11)'),
    ('w', 6, 9, 8, '回 (9,8)'),
    ('d', 6, 10, 8, '黄门(10,8)'),
    ('w', 6, 11, 8, '到 (11,8)'),
    ('m', 6, 11, 9, 'R史莱姆(11,9)'),
    ('s', 6, 11, 11, '上行梯 → 7F'),
    # ---- 7F：落点(11,10)→黄门(11,7)→y6 走廊→骷髅C(9,5)取 2 钥匙+红瓶→黄门(5,7)→蝙蝠(5,9)
    #      →钥匙(5,10)(5,11)→黄门(7,7)→R(7,9)→僧侶(7,10)→蓝瓶(7,11) +200→僧侶(4,6)→骷髅B(2,6)
    #      →黄门(1,5)→x1 北上→上行梯(1,1)
    #      （跳过 x9 下层骷髅B(+200蓝瓶/-252血) 与 x3 蝙蝠+ATK1，暂缓）
    ('d', 7, 11, 7, '黄门(11,7)'),
    ('w', 7, 9, 6, '到 (9,6)'),
    ('m', 7, 9, 5, '骷髅C(9,5)'),
    ('w', 7, 9, 1, '取红瓶(9,3)+钥匙(9,2)(9,1)'),
    ('w', 7, 5, 6, '回 y6 走廊 (5,6)'),
    ('d', 7, 5, 7, '黄门(5,7)'),
    ('w', 7, 5, 8, '到 (5,8)'),
    ('m', 7, 5, 9, '蝙蝠(5,9)'),
    ('w', 7, 5, 11, '取钥匙 (5,10)(5,11)'),
    ('w', 7, 7, 6, '回 (7,6)'),
    ('d', 7, 7, 7, '黄门(7,7)'),
    ('w', 7, 7, 8, '到 (7,8)'),
    ('m', 7, 7, 9, 'R史莱姆(7,9)'),
    ('m', 7, 7, 10, '僧侶(7,10)'),
    ('w', 7, 7, 11, '蓝瓶(7,11) +200'),
    ('w', 7, 5, 6, '回 (5,6)'),
    ('m', 7, 4, 6, '僧侶(4,6)'),
    # ---- 7F 商人 obj41：5 把黄钥匙 50G（解决 8F/9F 钥匙缺口）
    ('w', 7, 5, 6, '东移到 (5,6)'),
    ('d', 7, 5, 5, '蓝门(5,5)'),
    ('w', 7, 5, 4, '到 (5,4)'),
    ('m', 7, 5, 3, 'R史莱姆(5,3)'),
    ('w', 7, 5, 1, '到商人旁 (5,1)'),
    ('p', 7, 6, 1, '买 5 黄钥匙 50G'),
    ('w', 7, 5, 6, '回 (5,6)'),
    ('m', 7, 2, 6, '骷髅B(2,6)'),
    ('d', 7, 1, 5, '黄门(1,5)'),
    ('s', 7, 1, 1, '上行梯 → 8F'),
    # ---- 8F：落点(1,2) → 黄门(3,1) → 黄门(4,1) → (5,1) → 上行梯(6,1) → 9F
    ('d', 8, 3, 1, '黄门(3,1)'),
    ('d', 8, 4, 1, '黄门(4,1)'),
    ('w', 8, 5, 1, '到 (5,1)'),
    ('s', 8, 6, 1, '上行梯 → 9F'),
    # ---- 9F 右路：黄门(8,1) → G(9,1) → G(10,2) → 红药(11,1)(11,3) → (10,4)
    #      → 撞暗墙(10,5) → (10,6) → 铁盾(9,7) → 回(10,4) → 黄门(9,4)(8,4)
    #      → 钥匙(7,4) → ATK水晶(6,5) → 钥匙(5,4)
    ('d', 9, 8, 1, '黄门(8,1)'),
    ('m', 9, 9, 1, 'G史莱姆(9,1)'),
    ('w', 9, 9, 2, '到 (9,2)'),
    ('m', 9, 10, 2, 'G史莱姆(10,2)'),
    ('w', 9, 10, 1, '到 (10,1)'),
    ('w', 9, 11, 1, '红药(11,1) +50'),
    ('w', 9, 11, 3, '红药(11,3) +50'),
    ('w', 9, 10, 4, '到 (10,4)'),
    ('b', 9, 10, 5, '撞暗墙(10,5)'),
    ('w', 9, 10, 6, '到 (10,6)'),
    ('w', 9, 9, 6, '到 (9,6)'),
    ('w', 9, 9, 7, '铁盾 DEF+10'),
    ('w', 9, 10, 4, '回 (10,4)'),
    ('d', 9, 9, 4, '黄门(9,4)'),
    ('d', 9, 8, 4, '黄门(8,4)'),
    ('w', 9, 7, 4, '钥匙(7,4)'),
    ('w', 9, 6, 5, 'ATK水晶(6,5)'),
    ('w', 9, 5, 4, '钥匙(5,4)'),
    # ---- 9F 左上：黄门(4,5) → 蝙蝠(3,5) → 蓝水晶(1,5) DEF+1 → 钥匙(2,4)
    ('d', 9, 4, 5, '黄门(4,5)'),
    ('m', 9, 3, 5, '蝙蝠(3,5)'),
    ('w', 9, 1, 5, '蓝水晶(1,5) DEF+1'),
    ('w', 9, 2, 4, '钥匙(2,4)'),
    ('w', 9, 5, 5, '回中厅 (5,5)'),
    # ---- 回 8F：走右侧环 → (7,1) → (6,2) → 下行梯(6,1)
    ('s', 9, 6, 1, '下行梯 → 8F'),
]

def execute(plan=PLAN, verbose=True):
    if verbose:
        print('起始：' + st())
    for act in plan:
        kind = act[0]
        if kind == 'w':
            _, f, x, y, note = act
            walk(f, (x, y))
            tag = '走到'
        elif kind == 'm':
            _, f, x, y, note = act
            approach(f, x, y)
            o, lg = enter(f, x, y, '战斗')
            tag = '战 ' + info(o)
        elif kind == 'd':
            _, f, x, y, note = act
            approach(f, x, y)
            o, lg = enter(f, x, y, '开门')
            tag = '门 ' + info(o)
        elif kind == 'b':
            _, f, x, y, note = act
            approach(f, x, y)
            o, lg = enter(f, x, y, '撞墙')
            tag = '撞 ' + info(o)
        elif kind == 's':
            _, f, x, y, note = act
            approach(f, x, y)
            o, lg = enter(f, x, y, '楼梯')
            tag = '楼梯'
        elif kind == 'a':
            _, f, x, y, pol, note = act
            approach(f, x, y)
            W.altar_policy = pol
            o, lg = enter(f, x, y, '祭坛')
            tag = '祭坛' + pol
        elif kind == 'p':
            _, f, x, y, note = act
            approach(f, x, y)
            o, lg = enter(f, x, y, '购物')
            tag = '购物'
        elif kind == 'fly':
            _, f, note = act
            lg = W.fly(f)
            if lg and lg[0].startswith('飞行'): raise RuntimeError(lg)
            tag = '飞行'
        else:
            raise RuntimeError(kind)
        if verbose:
            for e in LOG:
                print(e)
            print('[%s] %-22s %s   %s' % (tag, note, st(), ('| ' + '; '.join(lg)) if lg else ''))
        LOG.clear()
    if verbose:
        print('总步数 %d' % STEPS[0])
        h = W.hero
        print('终态 HP%d ATK%d DEF%d GOLD%d 黄%d 蓝%d 红%d' % (h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r']))


def reach_report(f, verbose=True):
    """列出当前层可达自由格、以及贴边（一步可达）的怪物/门/物件。"""
    h = W.hero
    seen = {(h.x, h.y)}
    q = deque([(h.x, h.y)])
    frontier = []
    while q:
        c = q.popleft()
        for d in DIRS:
            n = (c[0] + d[0], c[1] + d[1])
            if not (0 <= n[0] < 13 and 0 <= n[1] < 13) or n in seen:
                continue
            if free(f, n[0], n[1]):
                seen.add(n); q.append(n)
            else:
                o = W.at(f, n[0], n[1])
                if o and n not in [x[1] for x in frontier]:
                    frontier.append((o, n))
    if verbose:
        print('%dF 可达 %d 格' % (f, len(seen)))
        print('  格: ' + ' '.join('(%d,%d)' % c for c in sorted(seen)))
        print('  贴边关口:')
        for o, c in frontier:
            print('    (%2d,%2d) %s' % (c[0], c[1], info(o)))
    return seen, frontier


if __name__ == '__main__':
    execute()
    if 'reach' in sys.argv:
        for f in [int(a) for a in sys.argv[sys.argv.index('reach') + 1:] if a.isdigit()]:
            reach_report(f)
