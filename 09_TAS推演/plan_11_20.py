# -*- coding: utf-8 -*-
"""11F→20F 重排（口径修正版 · 2026-10-29）

本轮三条硬口径（用户指定）
  1) 13F 神剣 obj34 **不拿**：熔岩不可穿，雪之结晶 obj110 才能清，而雪之结晶要 49F 假魔王→屠龙匕→35F 魔龙，
     时序在 35F 之后 → 13F 只走 y=11 长廊，0 战损。
  2) 熔岩 obj79：源码 c3=0/c4=0 → `directCheck` 判 bl=false（撞上去只弹 texts[183]「溶岩が流れている」）。
     雪の結晶走 itemFlag==11（@1322-1372）：把角色上下左右四格 `mapObject=='O'` 清成 0 并把 `map` 设 1，道具不消耗。
     ⚠️ 另有一说「每步 −200」：本版指令流里 a[9]=200 是第二帧裁剪坐标（@13224），未找到按步扣血分支；
     若按可踩版口径，13F 熔岩环到神剣约 4 格 = 800 血。本轮不踩熔岩，两种口径差值为 0。
  3) 15F 大ダコ obj71 **不打**：走 (9,1) 盗贼 → 凿开 (8,1) → (7,1) → 上梯 (6,1)。

源码核对到的事件规则
  A) 11F (2,4) 落穴 ← 11F (1,5)(3,5) 上級僧侶             @3796 [18][1]/[18][3] → [17][2]
  B) 17F (2,4) ← (1,5)(3,5) 門番Ｃ · (2,7) ← (1,8)(3,8) 門番Ｃ  @3809 / @3815 [21][79]
  C) 17F (10,4) ← (9,5)(11,5) ゾンビナイト · (10,7) ← (9,8)(11,8) ゾンビ @3821 / @3827
  D) 14F (1,3) 墙→红钥匙 obj28 ← 清 (1,1)(3,1)(2,2) 三只ゾンビナイト  @3802 [14][40]/[14][42]/[15][41]
  E) 15F (9,1) 盗贼 obj88（text 17）对话 → map[14][60]=1 即 (8,1) 变地板  @5786-5790
  F) 20F：红门(6,9)开 → 踏 (6,8) 放吸血鬼(6,6)+(6,9)复封(@3071)
          → 杀吸血鬼后 (6,6) 空 → (6,3)(6,9) 双封印消失 + (6,1) 生成上梯(@3043)
          → 随后 @2961 生成 (5..7,5) 黄钥匙×3、(6,8)(5,8)(7,8) 蓝药×3、
            (4,5..7) 赤晶×3、(8,5..7) 青晶×3
  G) 祭坛 obj22（12F (6,9)）：@3900-3928 四次使用代价 ((k+1)^2-(k+1)+2)*10 = 20/40/80/140/220/320…
        菜单：HP +(k+1)*100 ／ ATK +(mapY*2+2) ／ DEF +(mapY*4+4) ／ 取消
        12F mapY=1 → ATK+4 / DEF+8；16F 层行=1 同理；32F mapY=3 → ATK+8/DEF+16；46F mapY=4 → ATK+10/DEF+20
"""
import sys, csv, heapq, os
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W_Y, W_B, W_R = 60, 120, 600
W_MON = 12
DOOR = {2: ('黄', W_Y), 4: ('蓝', W_B), 27: ('红', W_R)}
KEY = {1: '黄', 3: '蓝', 28: '红'}

# ---- 本层事件未完成前不可通行 ----------------------------------------------
BLOCK = {15: {(x, y) for x in (5, 6, 7) for y in (4, 5, 6)}}   # 大乌贼 3×3 不打

# 落穴：守卫清空后才通
PIT_GUARD = {
    (11, (2, 4)): [(1, 5), (3, 5)],
    (17, (2, 4)): [(1, 5), (3, 5)],
    (17, (2, 7)): [(1, 8), (3, 8)],
    (17, (10, 4)): [(9, 5), (11, 5)],
    (17, (10, 7)): [(9, 8), (11, 8)],
}
F14_KEY_GUARDS = [(1, 1), (3, 1), (2, 2)]
F14_KEY_CELL = (1, 3)
# 凿墙：目标格 -> 触发格（走到触发格即凿开）
DIG = {(15, (8, 1)): [(9, 1)]}

# 禁开门（挑门策略：蓝门/红门只在必需时开）
FORBID_DOORS = {
    11: set(), 12: set(), 14: {(5, 4)},                # 14F (2,4) 蓝门是红钥匙唯一入口，(5,4) 无收益
    16: {(6, 4)}, 18: {(4, 1), (6, 6)}, 20: {(2, 6), (10, 6)},
}

# ---- 每层目标：'M'=可为它开门，'O'=只在不开新门时顺路取 ---------------------
TARGETS = {
    11: [('M',(1, 5)), ('M',(3, 5)), ('M',(2, 2)), ('M',(5, 1)),
         ('O',(1, 7)), ('O',(8, 11)), ('O',(9, 6)), ('O',(10, 1)),
         ('O',(1, 10)), ('O',(1, 11)), ('O',(2, 11)), ('O',(3, 11)), ('O',(4, 11)), ('O',(11, 1))],
    12: [('M',(2, 8)), ('M',(10, 6)), ('M',(6, 1)), ('M',(6, 7)),
         ('O',(9, 5)), ('O',(5, 10)), ('O',(7, 10)), ('O',(9, 7)), ('O',(1, 8)),
         ('M',(6, 9))],
    13: [],
    14: [('M',(1, 1)), ('M',(3, 1)), ('M',(2, 2)), ('M',(1, 3)), ('M',(5, 1)),
         ('O',(1, 5)), ('O',(5, 10)), ('O',(9, 6)), ('O',(6, 1)), ('O',(1, 11))],
    15: [('M',(9, 1)), ('M',(11, 8))],
    16: [('M',(11, 7)), ('O',(11, 3)), ('O',(1, 5)), ('O',(1, 7))],
    
    17: [('M',(1, 8)), ('M',(3, 8)), ('M',(1, 5)), ('M',(3, 5)), ('M',(2, 2)),
         ('M',(9, 8)), ('M',(11, 8)), ('M',(9, 5)), ('M',(11, 5)),
         ('M',(10, 3)), ('M',(9, 1)), ('M',(11, 1)), ('M',(10, 2)),
         ('O',(9, 3)), ('O',(11, 3)), ('O',(1, 11)), ('O',(11, 11))],
    18: [('M',(11, 3)), ('M',(5, 4)),
         ('O',(9, 1)), ('O',(10, 4)), ('O',(11, 4)), ('O',(2, 4))],
    19: [('M',(6, 3)), ('O',(11, 1)), ('O',(4, 1)), ('O',(7, 10)), ('O',(9, 9))],
    20: [('M',(6, 9)), ('M',(6, 8)), ('M',(6, 6))],
}

ALTAR_MUL = {12: (4, 8)}          # 层 → (ATK+, DEF+)


def passable(f, x, y, cleared):
    if not (0 <= x < 13 and 0 <= y < 13):
        return False
    if (x, y) in BLOCK.get(f, set()):
        return False
    t = M.terrain(f, x, y)
    o = M.obj_raw(f, x, y)
    if o == 79:                                  # 熔岩：未清不可穿
        return False
    for (df, cell), trig in DIG.items():
        if df == f and cell == (x, y):
            return all((df,) + t in cleared for t in trig)
    if o == 20:                                  # 落穴
        return (f, x, y) in cleared
    if o in DOOR:
        if (x, y) in cleared:
            return True
        if (x, y) in FORBID_DOORS.get(f, set()):
            return False
        return True
    if o in M.DECOR_PASS:
        return True
    if t == 1:
        if (f, x, y) == (f, *F14_KEY_CELL):
            return (f, x, y) in cleared          # 事件后才变地板
        return (f, x, y) in M.DARKWALL_CELLS
    return True


def cell_cost(f, x, y, cleared, atk, no_new=False):
    if not passable(f, x, y, cleared):
        return None
    o = M.obj_raw(f, x, y)
    if o in DOOR:
        if (x, y) in cleared:
            return 1
        if no_new:
            return None
        return DOOR[o][1]
    if o and M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
        if mstat(o)[2] >= atk:
            return None
        return W_MON
    return 1


def dijkstra(f, s, g, cleared, atk, no_new=False):
    dist, pre, h = {s: 0}, {s: None}, [(0, s)]
    while h:
        d, c = heapq.heappop(h)
        if c == g:
            break
        if d > dist.get(c, 1 << 60):
            continue
        x, y = c
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            cc = cell_cost(f, n[0], n[1], cleared, atk, no_new)
            if cc is None:
                continue
            nd = d + cc
            if nd < dist.get(n, 1 << 60):
                dist[n] = nd; pre[n] = c; heapq.heappush(h, (nd, n))
    if g not in pre:
        return None
    p, c = [], g
    while c is not None:
        p.append(c); c = pre[c]
    return p[::-1]


MON = {}


def mstat(o):
    if o not in MON:
        a = [M.oatr(o, i) for i in range(15)]
        MON[o] = (a[10], a[11], a[12], a[13])
    return MON[o]


def fight(o, atk, dfn, dbl=()):
    hp, ma, md, gold = mstat(o)
    per = atk * (2 if o in dbl else 1) - md
    if per <= 0:
        return None
    r = -(-hp // per)
    return r, max(0, ma - dfn) * (r - 1), gold


class Hero:
    def __init__(self):
        self.hp = 0
        self.atk = 60
        self.dfn = 50
        self.gold = 0
        self.keys = {'黄': 0, '蓝': 0, '红': 0}
        self.minhp = 0          # 进入 11F 所需最低 HP
        self.dmg = 0
        self.steps = 0
        self.log = []
        self.dbl = ()

    def take(self, d):
        self.dmg += d
        self.hp -= d
        self.minhp = max(self.minhp, -self.hp)


def run(altar_def=0, altar_atk=0, verbose=True, cnt0=0):
    H = Hero()
    out = []
    for f in range(11, 21):
        dmg0, step0, atk0, dfn0, gold0 = H.dmg, H.steps, H.atk, H.dfn, H.gold
        cleared = set()
        forbid = FORBID_DOORS.get(f, set())
        pos = M.FLY_LAND[f]
        up = M.STAIRS[f][0] or (6, 1)
        tgts = list(TARGETS.get(f, []))
        path_all = [pos]

        def after(path):
            """走完一段：开门入 cleared、触发事件"""
            for c in path:
                if M.obj_raw(f, *c) in DOOR:
                    cleared.add(c)
                for (df, cell), trig in DIG.items():
                    if df == f and c in trig:
                        cleared.add((df,) + cell)
                        for t in trig:
                            cleared.add((df,) + t)
            for (pf, pit), guards in PIT_GUARD.items():
                if pf == f and all(g in path_all for g in guards):
                    cleared.add((pf,) + pit)
            if f == 14 and all(g in path_all for g in F14_KEY_GUARDS):
                cleared.add((14,) + F14_KEY_CELL)

        while tgts:
            best = None
            for kind, t in tgts:
                for nn in ((True, False) if kind == 'O' else (False,)):
                    p = dijkstra(f, pos, t, cleared, H.atk, no_new=nn)
                    if p is not None:
                        cand = (len(p), 0 if kind == 'M' else 1, t, p, nn)
                        if best is None or cand[:2] < best[:2]:
                            best = cand
                        break
            if best is None:
                miss = [t for k, t in tgts]
                print('  !! F%d 从 %s 无可达目标，跳过 %s' % (f, pos, miss))
                break
            _, _, t, p, nn = best
            tgts = [(k, c) for k, c in tgts if c != t]
            path_all += p[1:]
            after(p)
            pos = t

        if f == 20:
            path_all.append(up)
        else:
            p = dijkstra(f, pos, up, cleared, H.atk)
            if p is None:
                print('  !! F%d %s→上梯%s 不通' % (f, pos, up))
            else:
                path_all += p[1:]
                for c in p:
                    if M.obj_raw(f, *c) in DOOR:
                        cleared.add(c)

        # ---- 逐格结算 ----
        lines, doors, keys, fights = [], [], [], []
        seen = set()
        seg = 0
        for c in path_all:
            o = M.obj_raw(f, *c)
            if not o or c in seen:
                continue
            seen.add(c)
            x, y = c
            if o in DOOR:
                n, _ = DOOR[o]
                H.keys[n] -= 1
                doors.append((c, o))
                lines.append('开%s门%s' % (n, c))
            elif o in KEY:
                n = KEY[o]
                H.keys[n] += 1
                keys.append((c, o))
                lines.append('拾%s钥%s' % (n, c))
            elif o == 89:                        # 可撞塌假墙（c3=5，免钥匙）
                cleared.add(c)
                if (f, (x, y)) == (19, (6, 3)):  # @5596 撞塌后原地生成 obj103
                    H.dbl = (48, 49, 59)
                    lines.append('★撞塌(6,3)假墙 → 十字架（对兽人/兽人武士/吸血鬼 ×2）')
                else:
                    lines.append('撞塌假墙%s' % (c,))
            elif M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
                r = fight(o, H.atk, H.dfn, H.dbl)
                if r is None:
                    lines.append('!!%s@%s 打不动' % (M.oname(o)[:8], c))
                    continue
                rd, d, g = r
                H.take(d); H.gold += g
                fights.append((c, o, rd, d))
                lines.append('%s@%s %d回合 -%d' % (M.oname(o)[:8], c, rd, d))
            elif M.oatr(o, 3) == 3:
                a = [M.oatr(o, i) for i in range(14)]
                if a[10]:
                    H.hp += a[10]
                if a[11]:
                    H.atk += a[11]
                if a[12]:
                    H.dfn += a[12]
                if a[13]:
                    H.gold += a[13]
                nm = M.oname(o)[:14]
                lines.append('拾%s%s' % (nm, c))
        # 14F 红钥匙
        if f == 14 and (14,) + F14_KEY_CELL in cleared:
            H.keys['红'] += 1
            lines.append('★(1,3) 暗墙→红钥匙')
        # 20F 吸血鬼
        if f == 20 and (6, 6) in [c for c in path_all]:
            r = fight(59, H.atk, H.dfn, H.dbl)
            if r:
                rd, d, g = r
                H.take(d); H.gold += g
                lines.append('バンパイア@(6,6) %d回合 -%d' % (rd, d))
                fights.append(((6, 6), 59, rd, d))
        # 12F 祭坛
        if f == 12 and altar_def + altar_atk > 0 and (6, 9) in path_all:
            ka, kd = ALTAR_MUL[12]
            cost = sum(M.altar_cost(k) for k in range(cnt0, cnt0 + altar_def + altar_atk))
            if H.gold >= cost:
                H.gold -= cost
                H.dfn += kd * altar_def
                H.atk += ka * altar_atk
                lines.append('★祭坛 ×%d 花%dG → ATK+%d DEF+%d'
                             % (altar_def + altar_atk, cost, ka * altar_atk, kd * altar_def))
            else:
                lines.append('★祭坛 金不足(%d<%d)' % (H.gold, cost))
        H.steps += len(path_all) - 1
        out.append(dict(f=f, steps=len(path_all) - 1, lines=lines, doors=doors,
                        keys=keys, hp=H.hp, atk=H.atk, dfn=H.dfn, gold=H.gold,
                        dmg=H.dmg - dmg0, atk0=atk0, dfn0=dfn0, gold0=gold0,
                        ky=H.keys['黄'], kb=H.keys['蓝'], kr=H.keys['红']))
        if verbose:
            print('F%-2d %3d步 | ATK%-3d DEF%-3d 金%-5d 钥黄%+d蓝%+d红%+d'
                  % (f, len(path_all) - 1, H.atk, H.dfn, H.gold,
                     H.keys['黄'], H.keys['蓝'], H.keys['红']))
            print('    ' + ' | '.join(lines))
    print()
    print('=== 11F→20F 合计：累计战损 %d，步数 %d，进入 11F 最低 HP %d ==='
          % (H.dmg, H.steps, H.minhp))
    print('    终态 ATK%d DEF%d 金%d 钥 黄%+d 蓝%+d 红%+d'
          % (H.atk, H.dfn, H.gold, H.keys['黄'], H.keys['蓝'], H.keys['红']))
    return out, H


def export(rows, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as fp:
        w = csv.writer(fp)
        w.writerow(['层', '层战损', '收尾ATK', '收尾DEF', '金币', '黄钥匙', '蓝钥匙', '红钥匙',
                    '步数', '步序', '动作'])
        for r in rows:
            w.writerow([r['f'], r['dmg'], r['atk'], r['dfn'], r['gold'],
                        r['ky'], r['kb'], r['kr'], r['steps'], '',
                        ' | '.join(r['lines'])])


if __name__ == '__main__':
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    rows, H = run(d, a)
    export(rows, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/魔塔1_route_11F到20F_v2.csv')
    print('CSV 已写入 repo/09_TAS推演/')
