# -*- coding: utf-8 -*-
"""追踪每一步属于哪个 V 段。用法: python _tagtrace.py <floor> <x> <y>"""
import os, sys

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
os.chdir(TOOLS)
sys.path.insert(0, TOOLS)
import mota_core as M
import z2_route as Z
import run_segs

CUR = {'tag': ''}
TAGS = []


def _mk(fn, kind):
    def f(*a, **k):
        if kind == 'run':
            t = a[2] if len(a) > 2 else k.get('tag', '')
        else:
            t = a[3] if len(a) > 3 else k.get('label', '')
        if t:
            CUR['tag'] = t
        return fn(*a, **k)
    return f


Z.run = _mk(Z.run, 'run')
Z.goto = _mk(Z.goto, 'goto')
if hasattr(run_segs, 'goto'):
    run_segs.goto = _mk(run_segs.goto, 'goto')
if hasattr(run_segs, 'run_segs'):
    _orig_rs = run_segs.run_segs

    def _rs(*a, **k):
        t = k.get('tag', '')
        if t:
            CUR['tag'] = 'RS:' + t
        return _orig_rs(*a, **k)
    run_segs.run_segs = _rs

_om = M.World.move


def move_rec(self, dx, dy):
    lg = _om(self, dx, dy)
    TAGS.append((self.hero.f, self.hero.x, self.hero.y, CUR['tag']))
    return lg


M.World.move = move_rec

rc = Z.main()
print('rc=', rc, 'steps=', len(TAGS))

f = int(sys.argv[1]) if len(sys.argv) > 1 else 5
x = int(sys.argv[2]) if len(sys.argv) > 2 else 1
y = int(sys.argv[3]) if len(sys.argv) > 3 else 6
hits = [(i, t) for i, t in enumerate(TAGS) if t[0] == f and t[1] == x and t[2] == y]
print('hits on %dF(%d,%d):' % (f, x, y))
for i, h in hits[:40]:
    print('   idx%-5d %s' % (i, h))
