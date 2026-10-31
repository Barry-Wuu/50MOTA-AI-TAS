# -*- coding: utf-8 -*-
import sys, time
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

t = time.time()
res = M.plan(lambda f, x, y: f == 11, max_states=250000)
dt = time.time() - t
if res is None:
    print('seg1 UNREACHABLE (%.1fs)' % dt)
elif isinstance(res, tuple) and res[0] == 'cap':
    print('seg1 CAP %s (%.1fs)' % (res[1], dt))
else:
    w, path = res
    h = w.hero
    print('seg1 OK  steps=%d  HP=%d ATK=%d DEF=%d G=%d 钥%d/%d/%d  (%.1fs)' % (
        len(path) - 1, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], dt))
    print('  终位 11F(%d,%d)  items=%s' % (h.x, h.y, sorted(h.items)))
    # 打印路径头尾
    print('  路径首3:', path[:3])
    print('  路径末3:', path[-3:])
