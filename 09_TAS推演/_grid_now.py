# -*- coding: utf-8 -*-
"""重放 z2_route 后，打印指定楼层的当前状态网格（含门色/楼梯/物件名）。"""
import sys, io
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import z2_route, run_segs, mota_core as M

buf = io.StringIO(); old = sys.stdout; sys.stdout = buf
rc = z2_route.main()
sys.stdout = old
w = run_segs.LAST_W
h = w.hero
print('rc=%d | HERO HP%d A%d D%d G%d keys %d/%d/%d %dF(%d,%d)' % (
    rc, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], h.f, h.x, h.y))

DOORC = {2: 'Y', 4: 'B', 27: 'R'}
KEYC = {1: 'k', 3: 'K', 28: 'Q'}

for f in [int(a) for a in sys.argv[1:]] or [16]:
    up, dn = M.STAIRS.get(f, (None, None))
    print('\n=== %dF  up%s dn%s ===' % (f, up, dn))
    print('     ' + ''.join('%4d' % x for x in range(1, 12)))
    for y in range(1, 12):
        row = '%3d  ' % y
        for x in range(1, 12):
            t = w.terrain_at(f, x, y)
            o = w.at(f, x, y)
            if t in (1, 2):
                ch = ' UU ' if (x, y) == up else (' DN ' if (x, y) == dn else ' ## ')
                if (x, y) == up or (x, y) == dn:
                    pass
            elif not o:
                ch = '  . '
            else:
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if ty == 'DOOR':
                    ch = '  ' + DOORC.get(o, 'd') + ' '
                elif o in KEYC:
                    ch = '  ' + KEYC[o] + ' '
                elif ty == 'MONSTER':
                    ch = '  M '
                elif ty == 'STATUS':
                    ch = '  s '
                elif ty == 'ITEM':
                    ch = '  I '
                elif ty == 'MESSAGE':
                    ch = '  T '
                elif ty == 'NORMAL':
                    ch = '  n '
                else:
                    ch = '  ? '
            row += ch
        print(row + ' %2d' % y)
    print('  U=上行梯 D=下行梯 Y/B/R=黄/蓝/红门 k/K/Q=黄/蓝/红钥 M=怪 s=药 I=道具 n=空物 T=对话')
    for y in range(1, 12):
        for x in range(1, 12):
            o = w.at(f, x, y)
            if o and M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
                r = w.battle(o)
                print('   (%2d,%2d) obj%-3d %-10s %s' % (x, y, o, M.oname(o)[:10],
                      ('损血%d +金%d' % (r[0], r[1])) if r else '打不过'))
