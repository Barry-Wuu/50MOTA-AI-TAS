# -*- coding: utf-8 -*-
"""区域图（修正版）：正确处理「门挨着门 / 怪挨着怪」的阻断链。

上一版 routelib.Floor 的 adj 只在「阻断物两侧都是区域」时建边，
   于是「门(8,4)-门(9,4)」这种连续阻断链把 区5 与 区2 之间的通路整个丢掉。
本版改为：以区域为节点，对每个区域做「穿格 BFS」，
   进入阻断格视为『清掉它』（门→耗钥匙，怪→掉血），可继续从该格扩散，
   首次触达另一区域时得到一条『门链/阻断链』。

代价（与队伍状态无关的部分）：
   门链 → 需要对应颜色钥匙数（黄/蓝/红），暗墙 → 0
   怪链 → 各怪 hp/atk/def/gold
另外单列每个区域内的『必取物』。
"""
import collections
import mota_core as M

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Floor2:
    def __init__(self, f):
        self.f = f
        w = M.World.new()
        w.apply_floor_events(f)
        self.w = w
        self.blocker = {}
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
        # 区域（阻断格不计入）
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
        self.gates = self._gates()
        self.gain = self._gain()

    # -- 阻断链 ---------------------------------------------------------
    def _gates(self):
        """返回 {rid: [ (chain, other_rid) ]}，chain = [(cell, kind, payload)] 顺序即清障顺序"""
        gates = collections.defaultdict(list)
        for src in range(len(self.regcells)):
            # (当前格, 已清链)
            start = [(c, []) for c in self.regcells[src]]
            seen = {(c, ()) for c in self.regcells[src]}
            q = collections.deque(start)
            depth = 0
            while q:
                cell, chain = q.popleft()
                for dx, dy in DIRS:
                    n = (cell[0] + dx, cell[1] + dy)
                    if not (1 <= n[0] <= 11 and 1 <= n[1] <= 11):
                        continue
                    if self.w.terrain_at(self.f, *n) == 1:
                        continue
                    if n in self.reg:
                        r2 = self.reg[n]
                        if r2 != src and chain:
                            gates[src].append((tuple(chain), r2))
                        continue
                    if n not in self.blocker:
                        continue
                    if n in [c for c, _, _ in chain]:
                        continue
                    k, v = self.blocker[n]
                    nchain = chain + [(n, k, v)]
                    if (n, tuple(nchain)) in seen:
                        continue
                    seen.add((n, tuple(nchain)))
                    q.append((n, nchain))
        # 去重：同一 (other_rid) 保留最短链
        best = {}
        for src, lst in gates.items():
            d = {}
            for chain, r2 in lst:
                if r2 not in d or len(chain) < len(d[r2][0]):
                    d[r2] = (chain, r2)
            gates[src] = list(d.values())
        return gates

    def _gain(self):
        g = {}
        for rid, cells in enumerate(self.regcells):
            hp = atk = dfn = 0
            keys = {'y': 0, 'b': 0, 'r': 0}
            names = []
            for (x, y) in cells:
                o = self.w.at(self.f, x, y)
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
            g[rid] = dict(hp=hp, atk=atk, dfn=dfn, keys=keys, names=names)
        return g

    def chain_cost(self, chain, atk, dfn):
        """返回 (掉血, 获得金, 需要的钥匙计数 dict) 或 None（打不过）"""
        loss = 0
        gold = 0
        need = {'y': 0, 'b': 0, 'r': 0}
        for (cell, kind, v) in chain:
            if kind == 'd':
                if v == '暗':
                    continue
                need[v] += 1
            else:
                hp, eatk, edfn, g = M.oatr(v, 10), M.oatr(v, 11), M.oatr(v, 12), M.oatr(v, 13)
                per = atk - edfn
                if per <= 0:
                    return None
                turns = -(-hp // per)
                loss += max(eatk - dfn, 0) * (turns - 1)
                gold += g
        return loss, gold, need
