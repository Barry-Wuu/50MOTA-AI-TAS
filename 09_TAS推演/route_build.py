# -*- coding: utf-8 -*-
"""连续合法路线构建器：补丁版 plan()，状态键含 atk/def/gold（修复 3F 扒装剪枝缺陷），
   链式推进 1F→11F→21F→31F→38F。输出每段终态与完整路径（可重放校验）。"""
import sys, time, heapq as _hq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

def plan2(goal, start=None, max_states=600000, goal_cell=None, trap_mode='apply', forbid=None, stay_floor=None):
    start = start if start is not None else M.World.new(trap_mode=trap_mode)
    forbid = forbid or set()                              # ✅ 禁踩格集合（f,x,y），用于「战利品 BOSS 后拿」
    start._par = None
    H = M.heuristic(goal_cell) if goal_cell else None
    h0 = (H or {}).get((start.hero.f, start.hero.x, start.hero.y), 0)
    pq = [(h0, 0, 0, start)]
    seen = {}
    n = 0
    while pq:
        loss, steps, _, w = _hq.heappop(pq)
        if goal(w.hero.f, w.hero.x, w.hero.y):
            mv = []
            cur = w
            while cur is not None:
                m = getattr(cur, '_mvd', None)
                if m is not None:
                    mv.append(m)
                cur = getattr(cur, '_par', None)
            return w, list(reversed(mv))
        n += 1
        if n > max_states:
            return ('cap', n)
        k = (w.hero.f, w.hero.x, w.hero.y,
             w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
             w.hero.atk, w.hero.dfn, w.hero.gold,          # ✅ 补丁：含 atk/dfn/gold
             frozenset(c for c in w.cleared if c in M.PICKUP_CELLS), frozenset(w.bought))
        if k in seen and seen[k][0] <= loss and seen[k][1] <= steps:
            continue
        seen[k] = (loss, steps)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            before = (w.hero.hp, w.hero.f, w.hero.x, w.hero.y)
            w2 = w.clone()
            log = w2.move(dx, dy)
            if M.blocked(log):
                continue
            if stay_floor is not None and w2.hero.f != stay_floor:   # ✅ 限制单层（防回溯爆炸）
                continue
            if (w2.hero.f, w2.hero.x, w2.hero.y) in forbid:   # ✅ 禁踩（战利品后拿）
                continue
            add = before[0] - w2.hero.hp
            w2._par = w
            w2._mvd = (dx, dy)                            # ✅ 记录真实动作（换层/商店时差分不可靠）
            ns = steps + 1
            nh = (H or {}).get((w2.hero.f, w2.hero.x, w2.hero.y), 0)
            _hq.heappush(pq, (loss + max(add, 0) + nh * 1000000, ns, next(M._TIE), w2))
    return None

if __name__ == '__main__':
    t = time.time()
    r = plan2(lambda f, x, y: f == 11, max_states=600000)
    dt = time.time() - t
    if r is None:
        print('seg1 None (%.1fs)' % dt)
    elif isinstance(r, tuple) and r[0] == 'cap':
        print('seg1 CAP %s (%.1fs)' % (r[1], dt))
    else:
        w, path = r
        h = w.hero
        print('seg1 OK steps=%d HP%d A%d D%d G%d 钥%d/%d/%d (%.1fs)' % (
            len(path) - 1, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], dt))
        print(' 终位 %dF(%d,%d) items=%s' % (h.f, h.x, h.y, sorted(h.items)))
