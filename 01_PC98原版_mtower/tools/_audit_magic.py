# -*- coding: utf-8 -*-
"""统计整条路线中「魔導師夹击(半血)」与「魔術師邻接固定伤害」的全部发生点。
monkey-patch check_magic_passby，对比每次调用前后的 HP 变化。
"""
import os, sys, io, contextlib
sys.path.insert(0, 'tools')
import mota_core as M

EVENTS = []

_orig = M.World.check_magic_passby

def patched(self, log):
    h = self.hero
    before = h.hp
    pos = (h.f, h.x, h.y)
    kind = None
    if M.SACRED_SHIELD not in h.items:
        f, x, y = h.f, h.x, h.y
        L = self.at(f, x - 1, y); R = self.at(f, x + 1, y)
        U = self.at(f, x, y - 1); D = self.at(f, x, y + 1)
        if (L in M.MAGIC_SANDWICH and R in M.MAGIC_SANDWICH) or \
           (U in M.MAGIC_SANDWICH and D in M.MAGIC_SANDWICH):
            kind = '夹击'
        else:
            for c in (L, R, U, D):
                if c in M.MAGIC_ADJ_DMG:
                    kind = '邻接%d' % c
                    break
    r = _orig(self, log)
    after = h.hp
    if after != before:
        EVENTS.append((kind, pos, before, after, before - after))
    return r

M.World.check_magic_passby = patched

import z2_route as Z
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        Z.main()
except SystemExit:
    pass

print('=== 魔法伤害事件全统计（整条路线）===')
print('%-10s %-14s %8s %8s %8s' % ('类型', '位置', '前HP', '后HP', '损失'))
t_j = t_adj = t_all = 0
for kind, pos, b, a, d in EVENTS:
    if a <= 0:
        tag = '【致死】'
    else:
        tag = ''
    print('%-10s %-14s %8d %8d %8d %s' % (kind or '?', '%dF(%d,%d)' % pos, b, a, d, tag))
    t_all += d
    if kind == '夹击':
        t_j += 1
    else:
        t_adj += 1
print()
print('夹击次数 = %d  夹击总损失 = %d' % (t_j, sum(d for k, _, _, _, d in EVENTS if k == '夹击')))
print('邻接伤害次数 = %d  邻接总损失 = %d' % (t_adj, sum(d for k, _, _, _, d in EVENTS if k != '夹击')))
print('魔法伤害总损失 = %d' % t_all)
print('总事件数 = %d' % len(EVENTS))
