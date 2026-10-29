# -*- coding: utf-8 -*-
"""地形连通域分析：把门/怪物当"边界"，求纯地板连通域，列出每域边界门/怪与域内道具。
   只用于查地形，不做路线搜索。口径与 dump_1_10.py 一致。"""
import sys
from collections import deque

sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

N = 12
DOOR = {2: '黄门', 4: '蓝门', 27: '红门'}
KEY = {1: '黄钥', 3: '蓝钥', 28: '红钥'}


def classify(f, x, y):
    """返回 (可通行?, 边界标签 or 域内标签)"""
    t = M.terrain(f, x, y)
    if t == 1:
        return False, '', ''
    o = M.obj_raw(f, x, y)
    if o == 0:
        return True, '', ''
    a = [M.oatr(o, i) for i in range(14)]
    ty = M.TYPE.get(a[3], '?')
    if o in DOOR:
        return False, '门' + DOOR[o], ''
    if o in KEY:
        return True, '', '钥' + KEY[o]
    if ty == 'MONSTER':
        return False, '怪%s(%d/%d/%d)' % (M.oname(o).strip(), a[10], a[11], a[12]), ''
    if t == 2:
        return True, '', '楼梯'
    nm = M.oname(o).strip().replace('\n', ' ')
    return True, '', '%s' % nm[:16]


def analyze(f, verbose=True):
    reg = {}
    rid = 0
    for y in range(1, N):
        for x in range(1, N):
            if (x, y) in reg:
                continue
            ok, _, _ = classify(f, x, y)
            if not ok:
                continue
            rid += 1
            reg[(x, y)] = rid
            q = deque([(x, y)])
            while q:
                cx, cy = q.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if not (1 <= nx < N and 1 <= ny < N):
                        continue
                    if (nx, ny) in reg:
                        continue
                    ok2, _, _ = classify(f, nx, ny)
                    if not ok2:
                        continue
                    reg[(nx, ny)] = rid
                    q.append((nx, ny))
    out = {}
    for (x, y), r in reg.items():
        out.setdefault(r, []).append((x, y))
    res = []
    for r, cells in out.items():
        cells.sort(key=lambda c: (c[1], c[0]))
        gates, items = {}, {}
        for (x, y) in cells:
            _, _, lab = classify(f, x, y)
            if lab:
                items[(x, y)] = lab
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if not (1 <= nx < N and 1 <= ny < N) or (nx, ny) in reg:
                    continue
                _, glab, _ = classify(f, nx, ny)
                if glab:
                    gates[(nx, ny)] = glab
        res.append((r, cells, gates, items))
    res.sort(key=lambda t: -len(t[1]))
    if verbose:
        print('=' * 74)
        print('%dF  楼梯 上%s 下%s' % (f, M.stairs_of(f)[0], M.stairs_of(f)[1]))
        for r, cells, gates, items in res:
            print('-- 域#%d  %d格' % (r, len(cells)))
            print('   格: ' + ' '.join('(%d,%d)' % c for c in cells))
            if items:
                print('   物: ' + ' | '.join('(%d,%d)%s' % (k[0], k[1], v) for k, v in sorted(items.items())))
            if gates:
                print('   界: ' + ' | '.join('(%d,%d)%s' % (k[0], k[1], v) for k, v in sorted(gates.items())))
    return res


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            analyze(int(a))
    else:
        for f in (7, 8, 9, 10):
            analyze(f)
