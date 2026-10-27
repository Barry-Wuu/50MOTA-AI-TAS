# -*- coding: utf-8 -*-
"""楼层模型（修正版）：应用 FLOOR_WRITES 事件写入后再建区域/边界图。

⚠️ 10F 有事件写入（FLOOR_WRITES[10]）：静态图与实际不同，
   例如 (9,4)/(11,4) 静态为空 → 事件写入黄钥匙；(1,4)/(3,4) 写入青药+200。
   但「静态是 MONSTER 的格」受保护不被覆盖（BOSS obj16 得以保留）。
"""
import collections
import mota_core as M

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
MONNAME = {}


class Floor:
    def __init__(self, f):
        self.f = f
        w = M.World.new()
        w.apply_floor_events(f)          # ✅ 关键：应用事件写入
        self.w = w
        self.blocker = {}                # (x,y) -> ('m', obj) | ('d', color) | ('w',) 暗墙
        self.stair = set()
        for y in range(1, 12):
            for x in range(1, 12):
                t = w.terrain_at(f, x, y)
                if t == 1:
                    continue
                if t == 2:
                    self.stair.add((x, y))
                o = w.at(f, x, y)
                if not o:
                    continue
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if ty == 'DOOR':
                    self.blocker[(x, y)] = ('d', '暗' if o == 89 else M.DOOR_OF[o])
                elif ty == 'MONSTER':
                    self.blocker[(x, y)] = ('m', o)
        # 区域
        self.reg = {}
        self.regcells = []
        for y in range(1, 12):
            for x in range(1, 12):
                if w.terrain_at(f, x, y) == 1 or (x, y) in self.blocker or (x, y) in self.reg:
                    continue
                rid = len(self.regcells)
                q = collections.deque([(x, y)])
                self.reg[(x, y)] = rid
                cells = []
                while q:
                    c = q.popleft()
                    cells.append(c)
                    for dx, dy in DIRS:
                        n = (c[0] + dx, c[1] + dy)
                        if not (1 <= n[0] <= 11 and 1 <= n[1] <= 11):
                            continue
                        if w.terrain_at(f, *n) == 1 or n in self.blocker or n in self.reg:
                            continue
                        self.reg[n] = rid
                        q.append(n)
                self.regcells.append(cells)
        self.adj = collections.defaultdict(list)
        for c, b in self.blocker.items():
            nb = set()
            for dx, dy in DIRS:
                n = (c[0] + dx, c[1] + dy)
                if n in self.reg:
                    nb.add(self.reg[n])
            for r in nb:
                for r2 in nb:
                    if r != r2:
                        self.adj[r].append((c, r2))
        # 每区收益
        self.gain = {}
        for rid, cells in enumerate(self.regcells):
            hp = atk = dfn = 0
            keys = {'y': 0, 'b': 0, 'r': 0}
            names = []
            for (x, y) in cells:
                o = w.at(f, x, y)
                if not o:
                    continue
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if ty == 'STATUS':
                    hp += M.oatr(o, 10)
                    atk += M.oatr(o, 11)
                    dfn += M.oatr(o, 12)
                    names.append((x, y, M.oname(o)))
                elif ty == 'KEY':
                    keys[M.KEY_OF[o]] += 1
                    names.append((x, y, M.oname(o)))
            self.gain[rid] = dict(hp=hp, atk=atk, dfn=dfn, keys=keys, names=names)
        # 商店
        self.shops = {}
        for y in range(1, 12):
            for x in range(1, 12):
                o = w.at(f, x, y)
                if o and o in M.SHOP:
                    self.shops[(x, y)] = (M.SHOP_PRICE.get(o, 0), M.SHOP_GRANT.get(o, []), o)

    def mon_loss(self, obj, atk, dfn):
        hp, eatk, edfn, gold = M.oatr(obj, 10), M.oatr(obj, 11), M.oatr(obj, 12), M.oatr(obj, 13)
        per = atk - edfn
        if per <= 0:
            return None
        turns = -(-hp // per)
        return max(eatk - dfn, 0) * (turns - 1), gold

    def info(self, obj):
        return dict(name=M.oname(obj), hp=M.oatr(obj, 10), atk=M.oatr(obj, 11),
                    df=M.oatr(obj, 12), gold=M.oatr(obj, 13))
