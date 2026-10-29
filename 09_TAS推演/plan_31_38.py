# -*- coding: utf-8 -*-
"""31F→38F 重排（取 38F 骑士の盾 · 2026-10-29）

前置口径（承接 11F→20F 重排）
  · 出 20F 终态 ATK90 / DEF102（13F 神剣不拿、15F 乌贼不打）
  · 21F→30F 无任何属性道具（已核实：全段 0 个 c3==3 物件），只有 25F 大魔導師 4500/560/310 与 30F 六只小史莱姆
    → 进 31F 仍是 ATK90 / DEF102
本段口径
  · 33F (10,10) 騎士の剣 obj32 = ATK **+40**（旧推演写成水晶级 +2，错得离谱）
  · 38F (2,7) 騎士の盾 obj37 = DEF **+40**
  · 37F 中央两座库（含红钥匙 (7,5)）被 `map==3` 真墙封死，**只有镐 obj114 能破**；本轮没镐 → 放弃，只走 x=11 右通道上顶行
  · 35F 魔龙 3×3 (5..7, 5..7) 不打，走 (5,10) 盗贼 → 凿开 (4,9) → 撞 89 隐形墙绕到上梯
  · 38F (2,5) 初始是空地板，踩 (2,6) 才由 @2528 变落穴 → 拿盾后原路回不去，必须走 (4,6)(5,6)(5,5) 三道蓝门绕回
"""
import sys, csv, heapq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W_Y, W_B, W_R = 60, 120, 600
W_MON = 12
DOOR = {2: ('黄', W_Y), 4: ('蓝', W_B), 27: ('红', W_R)}
KEY = {1: '黄', 3: '蓝', 28: '红'}

# 35F 魔龙 3×3（obj53-55 / 63-65 / 73-75），不打
BLOCK = {35: {(x, y) for x in (5, 6, 7) for y in (5, 6, 7)}}

# 凿墙：目标格 -> 触发格（35F (4,9) 由 2F(11,11) 对话远程开好，空触发=恒可通行）
# 源码链：32F(6,10) 踩 5 次 → 2F(11,11) 生成盗贼 → 清 2F(6,2)(8,2) 門番Ｂ → 2F(11,11) 对话
#   → map[48][56]=1 把 35F(4,9) 从墙变地板（@5770）。所以本段不需要再走到 35F(5,10) 触发。
DIG = {(35, (4, 9)): []}

# 2F 支线路径（飞行落点 (1,2) → 打完两只門番Ｂ → (11,11) 对话）
# 去程：23 步，含蓝门 (3,1)、門番Ｂ(6,2)(8,2) 两战；洞 (9,11) 在两戰后清零可通行
F2_GO = [(1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 2), (6, 2), (7, 2), (8, 2),
         (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11),
         (8, 11), (9, 11), (10, 11), (11, 11)]
# 回程：从 (11,11) 回到 (1,10)（(1,11) 下行梯旁，满足飞行条件），BFS 实测 29 步，无消耗
F2_BACK = [(11, 11), (10, 11), (9, 11), (8, 11), (8, 10), (8, 9), (8, 8), (8, 7), (8, 6),
           (8, 5), (8, 4), (7, 4), (7, 3), (7, 2), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1),
           (2, 1), (2, 2), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
           (1, 10)]

# 静态落穴（初始就存在，不可踩）：35F (6,3)
PIT_FIXED = {(35, (6, 3))}

# 事件落穴：38F 踩 (2,6) 后 (2,5) 变落穴
TRAP = {(38, (2, 6)): (38, (2, 5))}

# 隐形墙 obj89 在三处：撞一次就塌，按可通行处理

ENTRY = {31: (6, 2), 32: (6, 10), 33: (10, 1), 34: (2, 1),
         35: (6, 10), 36: (11, 2), 37: (11, 10), 38: (2, 1)}
UPSTAIR = {31: (6, 11), 32: (11, 1), 33: (1, 1), 34: (6, 11),
           35: (11, 1), 36: (11, 11), 37: (1, 1), 38: (11, 1)}

F34_CLEAR = [(5, 4), (7, 4), (9, 4), (11, 4), (5, 8), (7, 8), (9, 8), (11, 8)]

FORBID_DOORS = {
    # 37F 右侧 (11,?) 无门；33F 有蓝门 (1,3)(3,11) 视收益决定
    33: set(), 34: set(), 37: set(), 38: set(),
}

# 'M'=可为它开门　'O'=只在不开新门时顺路取
TARGETS = {
    # 31F (4,8) 青晶4 放弃：唯一入口 (4,9) 黄门 → (4,10) 騎士 160/230/105，
    # 本层 ATK 只有 90/94（<105 打不动），要拿必须等 33F 騎剣后回头，收益仅 DEF+4
    31: [('M', (8, 4)), ('M', (8, 8)), ('M', (4, 4)), ('O', (10, 1)), ('O', (2, 11))],
    32: [('M', (1, 1)), ('M', (2, 2)), ('M', (11, 4)), ('M', (10, 10))],
    # 33F 先取 (11,3) 蓝药（让路径绕开剑士时已有高 ATK），再拿骑士剑
    33: [('M', (10, 10)), ('M', (11, 3)), ('O', (5, 2)), ('O', (2, 4))],
    34: [('M', (5, 4)), ('M', (7, 4)), ('M', (9, 4)), ('M', (11, 4)),
         ('M', (5, 8)), ('M', (7, 8)), ('M', (9, 8)), ('M', (11, 8)),
         ('M', (11, 1)), ('M', (11, 11)), ('M', (1, 11)),
         ('O', (1, 5)), ('O', (3, 5)), ('O', (1, 7)), ('O', (3, 7)),
         ('O', (3, 1)), ('O', (11, 2)), ('O', (10, 11))],
    35: [],
    36: [('M', (1, 11))],
    37: [('M', (11, 1))],
    38: [('M', (2, 7)), ('M', (5, 8)), ('O', (6, 8)), ('O', (11, 11))],
}

F12, F14 = 12, 14


def passable(f, x, y, cleared, dropped=()):
    if not (0 <= x < 13 and 0 <= y < 13):
        return False
    if (x, y) in BLOCK.get(f, set()):
        return False
    if (f, (x, y)) in PIT_FIXED or (f, (x, y)) in dropped:
        return False
    t = M.terrain(f, x, y)
    o = M.obj_raw(f, x, y)
    if o == 79:
        return False
    for (df, cell), trig in DIG.items():
        if df == f and cell == (x, y):
            return True          # 35F(4,9) 由 2F 对话远程开好，恒可通行
    if o == 20:
        return (f, x, y) in cleared
    if o in DOOR:
        if (x, y) in cleared:
            return True
        if (x, y) in FORBID_DOORS.get(f, set()):
            return False
        return True
    if o == 89:                                   # 隐形墙：撞一次塌
        return True
    if o in M.DECOR_PASS:
        return True
    if (x, y) in cleared and M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
        return True                                # 已击杀怪物 → 空地
    if t == 1:
        return (f, x, y) in M.DARKWALL_CELLS
    return True


def cell_cost(f, x, y, cleared, atk, no_new=False, dropped=()):
    if not passable(f, x, y, cleared, dropped):
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


def dijkstra(f, s, g, cleared, atk, no_new=False, dropped=()):
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
            cc = cell_cost(f, n[0], n[1], cleared, atk, no_new, dropped)
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
    def __init__(self, atk=90, dfn=102, gold=1063, ky=16, kb=1, kr=0, hp=0):
        self.hp = hp
        self.atk = atk
        self.dfn = dfn
        self.gold = gold
        self.keys = {'黄': ky, '蓝': kb, '红': kr}
        self.minhp = 0
        self.dmg = 0
        self.steps = 0
        self.dbl = ()

    def take(self, d):
        self.dmg += d
        self.hp -= d
        self.minhp = max(self.minhp, -self.hp)


def run(altar_atk=0, altar_def=0, verbose=True, cnt0=0, start=None):
    H = Hero(**(start or {}))
    out = []
    did_f2 = False          # 2F 凿墙支线是否已完成
    sword_granted = False   # 33F 骑士剑 +40 是否已提前结算
    for f in range(31, 39):
        dmg0, atk0, dfn0, gold0 = H.dmg, H.atk, H.dfn, H.gold
        cleared = set()
        dropped = set()
        pos = ENTRY[f]
        up = UPSTAIR[f]
        tgts = list(TARGETS.get(f, []))
        path_all = [pos]

        def after(path):
            for c in path:
                o = M.obj_raw(f, *c)
                if o in DOOR:
                    cleared.add(c)
                elif M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
                    cleared.add(c)          # 已击杀：后续再经过按空地计
                for (df, cell), trig in DIG.items():
                    if df == f and c in trig:
                        cleared.add((df,) + cell)
                        for t2 in trig:
                            cleared.add((df,) + t2)
                if (f, c) in TRAP:
                    dropped.add(TRAP[(f, c)])

        # ── 32F 触发链：进入即踩 (6,10)，原地反复触发 5 次（0 步）──
        if f == 32:
            r = fight(90, H.atk, H.dfn, H.dbl)     # obj90 金騎士 120/150/50/100（第 3 次强制战）
            if r is None:
                print('  !! 32F 金騎士打不动')
            else:
                rd, d, g = r
                H.take(d); H.gold += g
                lines_pre = ['金騎士@32F触发链 %d回合 -%d' % (rd, d)]

        while tgts:
            best = None
            for kind, t in tgts:
                for nn in ((True, False) if kind == 'O' else (False,)):
                    p = dijkstra(f, pos, t, cleared, H.atk, no_new=nn, dropped=dropped)
                    if p is not None:
                        cand = (len(p), 0 if kind == 'M' else 1, t, p, nn)
                        if best is None or cand[:2] < best[:2]:
                            best = cand
                        break
            if best is None:
                miss = [t for k, t in tgts]
                print('  !! F%d 从 %s 无可达目标：%s' % (f, pos, miss))
                break
            _, _, t, p, nn = best
            tgts = [(k, c) for k, c in tgts if c != t]
            path_all += p[1:]
            after(p)
            pos = t

        # ── 33F 拿完剑 → 2F 凿墙支线 → 飞回 33F ──
        if f == 33 and not did_f2:
            # 骑士剑 +40 提前结算（否则 2F 支线在 lines 结算前用旧 ATK 打門番Ｂ）
            if (10, 10) in path_all and not sword_granted:
                H.atk += 40
                sword_granted = True
            # 从剑的位置走到 33F 下行梯旁（(10,1) 是 (11,1) 邻格，可飞行）
            p = dijkstra(33, pos, (10, 1), cleared, H.atk, dropped=dropped)
            if p is None:
                print('  !! 33F 到楼梯旁不可达')
            else:
                path_all += p[1:]
                after(p)
                pos = (10, 1)
                f2_lines = ['★飞行→2F']

                # 飞行 → 2F（落 (1,2)），执行支线
                for c in F2_GO[1:]:
                    o = M.obj_raw(2, *c)
                    if o in DOOR:
                        n, _ = DOOR[o]
                        H.keys[n] -= 1
                        f2_lines.append('开%s门%s' % (n, c))
                    elif M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
                        r = fight(o, H.atk, H.dfn, H.dbl)
                        if r is None:
                            print('  !! 2F %s@%s 打不动' % (M.oname(o)[:8], c))
                            continue
                        rd, d, g = r
                        H.take(d); H.gold += g
                        f2_lines.append('%s@%s %d回合 -%d' % (M.oname(o)[:8], c, rd, d))
                H.steps += len(F2_GO) - 1
                f2_lines.append('★(11,11)对话 → 35F(4,9)凿开')
                # 回程（(11,11) → (1,10)，即 (1,11) 下行梯旁）
                H.steps += len(F2_BACK) - 1
                f2_lines.append('★飞回33F')
                did_f2 = True
                # 飞行回 33F（落点 (10,1)）
                pos = (10, 1)

        p = dijkstra(f, pos, up, cleared, H.atk, dropped=dropped)
        if p is None:
            print('  !! F%d %s→上梯%s 不通' % (f, pos, up))
        else:
            path_all += p[1:]
            after(p)

        lines, seen = [], set()
        for c in path_all:
            o = M.obj_raw(f, *c)
            if not o or c in seen:
                continue
            seen.add(c)
            if o in DOOR:
                n, _ = DOOR[o]
                H.keys[n] -= 1
                lines.append('开%s门%s' % (n, c))
            elif o in KEY:
                n = KEY[o]
                H.keys[n] += 1
                lines.append('拾%s钥%s' % (n, c))
            elif M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
                r = fight(o, H.atk, H.dfn, H.dbl)
                if r is None:
                    lines.append('!!%s@%s 打不动' % (M.oname(o)[:8], c))
                    continue
                rd, d, g = r
                H.take(d); H.gold += g
                lines.append('%s@%s %d回合 -%d' % (M.oname(o)[:8], c, rd, d))
            elif M.oatr(o, 3) == 3:
                a = [M.oatr(o, i) for i in range(14)]
                if a[10]: H.hp += a[10]
                if a[11]:
                    if f == 33 and o == 32 and sword_granted:
                        pass          # 骑士剑已在 2F 支线前结算
                    else:
                        H.atk += a[11]
                if a[12]: H.dfn += a[12]
                if a[13]: H.gold += a[13]
                lines.append('拾%s%s' % (M.oname(o)[:16], c))
        # 32F 触发链
        if f == 32:
            lines = lines_pre + lines
            lines.append('★32F触发链：踩(6,10)×5 → 2F(11,11) 生成盗贼')
        # 32F 祭坛：DEF 优先（本段君主伤害全看 DEF）
        if f == 32 and altar_atk + altar_def > 0 and (10, 10) in path_all:
            n = altar_atk + altar_def
            cost = sum(M.altar_cost(k) for k in range(cnt0, cnt0 + n))
            if H.gold >= cost:
                H.gold -= cost
                H.atk += 8 * altar_atk
                H.dfn += 16 * altar_def
                lines.append('★祭坛 ×%d 花%dG → ATK+%d DEF+%d'
                             % (n, cost, 8 * altar_atk, 16 * altar_def))
        # 34F 清场八只 → @2586 掉红钥匙 (2,6) + 黄钥匙×4
        if f == 34 and all(c in path_all for c in F34_CLEAR):
            H.keys['红'] += 1
            H.keys['黄'] += 4
            lines.append('★清场八只 → 红钥匙(2,6) + 黄钥匙(1,5)(3,5)(1,7)(3,7)')
        # 33F 2F 支线
        if f == 33 and did_f2:
            lines.append('★飞行→2F 清門番Ｂ×2 + (11,11)对话 → 凿开 35F(4,9) → 飞回33F')
            lines.extend(f2_lines)
        # 38F 骑士盾
        if f == 38:
            lines.append('★骑士の盾 obj37 @(2,7)')
        H.steps += len(path_all) - 1
        f_steps = len(path_all) - 1
        if f == 33 and did_f2:
            f_steps += len(F2_GO) - 1 + len(F2_BACK) - 1
        out.append(dict(f=f, steps=f_steps, lines=lines, hp=H.hp,
                        atk=H.atk, dfn=H.dfn, gold=H.gold, dmg=H.dmg - dmg0,
                        atk0=atk0, dfn0=dfn0, ky=H.keys['黄'], kb=H.keys['蓝'],
                        kr=H.keys['红']))
        if verbose:
            print('F%-2d %3d步 战损%-5d | ATK%-3d DEF%-3d 金%-5d 钥 黄%+d 蓝%+d 红%+d'
                  % (f, f_steps, H.dmg - dmg0, H.atk, H.dfn, H.gold,
                     H.keys['黄'], H.keys['蓝'], H.keys['红']))
            print('    ' + ' | '.join(lines))
    print()
    print('=== 31F→38F 合计：战损 %d，步数 %d，段内最低 HP %d（相对 11F 起点）==='
          % (H.dmg, H.steps, H.minhp))
    print('    终态 ATK%d DEF%d 金%d 钥 黄%+d 蓝%+d 红%+d'
          % (H.atk, H.dfn, H.gold, H.keys['黄'], H.keys['蓝'], H.keys['红']))
    return out, H


def export(rows, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as fp:
        w = csv.writer(fp)
        w.writerow(['层', '层战损', '收尾ATK', '收尾DEF', '金币', '黄钥匙', '蓝钥匙',
                    '红钥匙', '步数', '动作'])
        for r in rows:
            w.writerow([r['f'], r['dmg'], r['atk'], r['dfn'], r['gold'],
                        r['ky'], r['kb'], r['kr'], r['steps'], ' | '.join(r['lines'])])


if __name__ == '__main__':
    import plan_11_20 as A
    r1, H1 = A.run(3, 0, verbose=False)
    # 不传 hp：Hero 从 0 开始，minhp = 本段相对起点需带血量（与旧文档口径一致）
    st = dict(atk=H1.atk, dfn=H1.dfn, gold=H1.gold,
              ky=H1.keys['黄'], kb=H1.keys['蓝'], kr=H1.keys['红'])
    print('20F 出口：ATK%d DEF%d 金%d 钥 黄%+d 蓝%+d 红%+d  (11F-20F 战损 %d / %d 步)'
          % (H1.atk, H1.dfn, H1.gold, H1.keys['黄'], H1.keys['蓝'], H1.keys['红'],
             H1.dmg, H1.steps))
    print()
    rows, H = run(2, 2, cnt0=3, start=st)
    export(rows, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/魔塔1_route_31F到38F_骑士盾_v3.csv')
    print('CSV 已写入 repo/09_TAS推演/')
