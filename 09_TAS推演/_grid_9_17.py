# -*- coding: utf-8 -*-
import sys
TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
sys.path.insert(0, TOOLS)
import mota_core as M

def sym(f, x, y):
    t = M.terrain(f, x, y)
    if t == 1: return '##'
    if t == 2: return 'UP' if M.stair_up(f, x, y) else 'DN'
    o = M.obj_raw(f, x, y)
    if not o: return ' .'
    ty = M.TYPE.get(M.oatr(o, 3))
    if o in M.KEY_OF: return ' K' + ('Y' if o == 1 else 'B' if o == 3 else 'R')
    if ty == 'DOOR':
        return ' dY' if o == 2 else ' dB' if o == 4 else ' dR' if o == 27 else ' d?'
    if ty == 'MONSTER': return ' M '
    if ty == 'STATUS': return ' S '
    if ty == 'SAIDAN': return ' A '
    if o == 89: return ' sW'
    return ' ? '

for f in (9, 10, 11, 12, 14, 15, 16, 17):
    print('==== %dF ====' % f)
    print('    ' + ''.join('%2d' % x for x in range(13)))
    for y in range(13):
        print('y%2d ' % y + ''.join(sym(f, x, y) for x in range(13)))
    print()
