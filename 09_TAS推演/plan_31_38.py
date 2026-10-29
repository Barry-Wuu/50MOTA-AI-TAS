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

# 凿墙：目标格 -> 触发格（35F (5,10) 盗贼 obj88 → 凿开 (4,9)）
DIG = {(35, (4, 9)): [(5, 10)]}

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
    33: [('M', (10, 10)), ('M', (11, 3)), ('O', (5, 2)), ('O', (2, 4))],
    34: [('M', (5, 4)), ('M', (7, 4)), ('M', (9, 4)), ('M', (11, 4)),
         ('M', (5, 8)), ('M', (7, 8)), ('M', (9, 8)), ('M', (11, 8)),
         ('M', (11, 1)), ('M', (11, 11)), ('M', (1, 11)),
         ('O', (1, 5)), ('O', (3, 5)), ('O', (1, 7)), ('O', (3, 7)),
         ('O', (3, 1)), ('O', (11, 2)), ('O', (10, 11))],
    35: [('M', (5, 10))],
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
            return all((df,) + t2 in cleared for t2 in trig)
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
                if M.obj_raw(f, *c) in DOOR:
                    cleared.add(c)
                for (df, cell), trig in DIG.items():
                    if df == f and c in trig:
                        cleared.add((df,) + cell)
                        for t2 in trig:
                            cleared.add((df,) + t2)
                if (f, c) in TRAP:
                    dropped.add(TRAP[(f, c)])

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
                if a[11]: H.atk += a[11]
                if a[12]: H.dfn += a[12]
                if a[13]: H.gold += a[13]
                lines.append('拾%s%s' % (M.oname(o)[:16], c))
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
        # 35F 盗贼凿墙
        if f == 35 and (5, 10) in path_all:
            lines.append('★(5,10) 盗贼 → 凿开 (4,9)')
        # 38F 骑士盾
        if f == 38:
            lines.append('★骑士の盾 obj37 @(2,7)')
        H.steps += len(path_all) - 1
        out.append(dict(f=f, steps=len(path_all) - 1, lines=lines, hp=H.hp,
                        atk=H.atk, dfn=H.dfn, gold=H.gold, dmg=H.dmg - dmg0,
                        atk0=atk0, dfn0=dfn0, ky=H.keys['黄'], kb=H.keys['蓝'],
                        kr=H.keys['红']))
        if verbose:
            print('F%-2d %3d步 战损%-5d | ATK%-3d DEF%-3d 金%-5d 钥 黄%+d 蓝%+d 红%+d'
                  % (f, len(path_all) - 1, H.dmg - dmg0, H.atk, H.dfn, H.gold,
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
    st = dict(atk=H1.atk, dfn=H1.dfn, gold=H1.gold,
              ky=H1.keys['黄'], kb=H1.keys['蓝'], kr=H1.keys['红'], hp=H1.hp)
    print('20F 出口：ATK%d DEF%d 金%d 钥 黄%+d 蓝%+d 红%+d  (11F-20F 战损 %d / %d 步)'
          % (H1.atk, H1.dfn, H1.gold, H1.keys['黄'], H1.keys['蓝'], H1.keys['红'],
             H1.dmg, H1.steps))
    print()
    rows, H = run(2, 2, cnt0=3, start=st)
    export(rows, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/魔塔1_route_31F到38F_骑士盾_v2.csv')
    print('CSV 已写入 repo/09_TAS推演/')
