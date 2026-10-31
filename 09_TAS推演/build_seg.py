# -*- coding: utf-8 -*-
"""8F(6,2)→11F 分段构建：从 manual 的 8F(6,2) 状态出发，用 plan2 单层逐段推进。"""
import sys, time
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import manual
import route_build as RB

W = M.World.new()
for d in manual.PREAMBLE_MOVES: W.move(*d)
_orig = W.move
pm = []
def rec(dx, dy):
    lg = _orig(dx, dy); pm.append((dx, dy)); return lg
W.move = rec
manual.W = W
manual.execute(verbose=False)
W.move = _orig
h = W.hero
print('起点 %dF(%d,%d) HP%d A%d D%d G%d 钥%d/%d/%d' % (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r']))

def seg(name, goal, start, max_states=200000, **kw):
    t = time.time()
    r = RB.plan2(goal, start=start, max_states=max_states, **kw)
    dt = time.time() - t
    if r is None: print('%s None (%.1fs)' % (name, dt)); return None
    if isinstance(r, tuple) and r[0] == 'cap': print('%s CAP %s (%.1fs)' % (name, r[1], dt)); return None
    w, mv = r; h = w.hero
    print('%s OK 步+%d → %dF(%d,%d) HP%d A%d D%d G%d 钥%d/%d/%d (%.1fs)' % (
        name, len(mv), h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], dt))
    return w, mv

# 段1: 8F 内 → 8F(4,10) 红晶
r1 = seg('seg1 8F红晶', lambda f, x, y: (f, x, y) == (8, 4, 10), W, stay_floor=8, goal_cell=(8, 4, 10))
