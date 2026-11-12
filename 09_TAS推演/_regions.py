# -*- coding: utf-8 -*-
"""按层输出「门/怪物/祭坛当墙」的连通域编号图，用于确认攻略方位词对应的房间。
用法：python _regions.py 8 11 12
"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
from collections import deque

BARRIER = ('DOOR', 'MONSTER', 'SAIDAN', 'SELL', 'BUY')


def region_map(f, open_monsters=False):
    reg = {}
    rid = 0
    for y in range(1, 12):
        for x in range(1, 12):
            if (x, y) in reg:
                continue
            t = M.terrain(f, x, y)
            o = M.obj_raw(f, x, y)
            ty = M.TYPE.get(M.oatr(o, 3)) if o else None
            if t in (1, 2) or (ty in BARRIER and not (open_monsters and ty == 'MONSTER')):
                reg[(x, y)] = 'X'
                continue
            rid += 1
            q = deque([(x, y)])
            reg[(x, y)] = rid
            while q:
                cx, cy = q.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if not (1 <= nx <= 11 and 1 <= ny <= 11):
                        continue
                    if (nx, ny) in reg:
                        continue
                    t2 = M.terrain(f, nx, ny)
                    o2 = M.obj_raw(f, nx, ny)
                    ty2 = M.TYPE.get(M.oatr(o2, 3)) if o2 else None
                    if t2 in (1, 2) or (ty2 in BARRIER and not (open_monsters and ty2 == 'MONSTER')):
                        reg[(nx, ny)] = 'X'
                        continue
                    reg[(nx, ny)] = rid
                    q.append((nx, ny))
    return reg


for a in sys.argv[1:]:
    f = int(a)
    reg = region_map(f)
    print('=' * 60)
    print('%dF 连通域（门/怪/祭坛=墙，X 为墙/障碍）' % f)
    print('    ' + ''.join('%2d' % x for x in range(1, 12)))
    for y in range(1, 12):
        row = '%2d  ' % y
        for x in range(1, 12):
            r = reg.get((x, y), 'X')
            row += (' X' if r == 'X' else '%2d' % r)
        print(row)
    print()
    # 每个区域里的物件
    zones = {}
    for (x, y), r in reg.items():
        if r == 'X':
            continue
        o = M.obj_raw(f, x, y)
        if o:
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            zones.setdefault(r, []).append('(%d,%d)obj%d %s %s' % (
                x, y, o, ty, M.oname(o)[:10]))
    for r in sorted(zones):
        print('-- 区域 %d --' % r)
        for s in zones[r]:
            print('   ' + s)
