# -*- coding: utf-8 -*-
"""从指定层/坐标做引擎级可达性 BFS（clone+move，忠实 mota_core 判定）。
可选 --plan 先重放 manual.PLAN 到锚点 8F(6,2)，再探测（反映真实世界状态）。
用法: python reach.py [--plan] <floor> <x> <y>
输出: 可达自由格 + 贴边关口（怪物/门/物件）。
"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

args = sys.argv[1:]
if args and args[0] == '--plan':
    import manual
    manual.execute(verbose=False)
    w = manual.W
    args = args[1:]
else:
    w = M.World.new()

f = int(args[0]); sx = int(args[1]); sy = int(args[2])
w.hero.f, w.hero.x, w.hero.y = f, sx, sy

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def info(o):
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if ty == 'MONSTER':
        return '%s(%d/%d/%d)G%d' % (M.oname(o), M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13))
    return '%s obj%d' % (M.oname(o)[:12], o)

def try_move(cx, cy, dx, dy):
    c = w.clone()
    c.hero.x, c.hero.y = cx, cy
    lg = c.move(dx, dy)
    if lg and lg[0].startswith(('blocked', '打不动', '打不过', '无', '买不起', '熔岩烫死', '祭坛金币不足')):
        return None, lg
    return (c.hero.x, c.hero.y), lg

seen = {(sx, sy)}
q = [(sx, sy)]
frontier = {}
while q:
    nq = []
    for (cx, cy) in q:
        for (dx, dy) in DIRS:
            nx, ny = cx + dx, cy + dy
            if not (0 <= nx < 13 and 0 <= ny < 13) or (nx, ny) in seen:
                continue
            res, lg = try_move(cx, cy, dx, dy)
            if res:
                seen.add((nx, ny)); nq.append((nx, ny))
            else:
                o = w.at(f, nx, ny)
                frontier.setdefault((nx, ny), (o, lg))
    q = nq

print('%dF 从 (%d,%d) 可达 %d 格' % (f, sx, sy, len(seen)))
print('  可达格: ' + ' '.join('(%d,%d)' % c for c in sorted(seen)))
print('  贴边关口:')
for c in sorted(frontier):
    o, lg = frontier[c]
    print('    (%2d,%2d) %-30s %s' % (c[0], c[1], info(o), lg[0] if lg else ''))
