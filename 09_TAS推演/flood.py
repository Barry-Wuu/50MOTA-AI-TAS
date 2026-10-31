# -*- coding: utf-8 -*-
"""洪水式探索一层：开所有可达门、杀所有可达怪，打印每步清除内容与最终连通图。
用法: python flood.py <floor> <x> <y>
只用于弄清几何（BOSS 通路、门序），不做最终路线决策。
"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

w = M.World.new()
f = int(sys.argv[1]); sx = int(sys.argv[2]); sy = int(sys.argv[3])
w.hero.f, w.hero.x, w.hero.y = f, sx, sy
w.hero.keys = {'y': 999, 'b': 999, 'r': 999}
# 给足能力（只探几何，不关心战损）
w.hero.hp, w.hero.atk, w.hero.dfn = 99999, 999, 999

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def info(o):
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if ty == 'MONSTER':
        return '%s(%d/%d/%d)G%d' % (M.oname(o), M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13))
    return '%s obj%d' % (M.oname(o)[:12], o)

def bfs_reach():
    seen = {(w.hero.x, w.hero.y)}
    q = [(w.hero.x, w.hero.y)]
    frontier = {}
    while q:
        nq = []
        for (cx, cy) in q:
            for (dx, dy) in DIRS:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < 13 and 0 <= ny < 13) or (nx, ny) in seen:
                    continue
                c = w.clone()
                c.hero.x, c.hero.y = cx, cy
                lg = c.move(dx, dy)
                if lg and lg[0].startswith(('blocked', '打不动', '打不过', '无', '买不起', '熔岩烫死', '祭坛金币不足')):
                    o = w.at(f, nx, ny)
                    frontier[(nx, ny)] = (o, lg[0])
                else:
                    seen.add((nx, ny)); nq.append((nx, ny))
        q = nq
    return seen, frontier

step = 0
while True:
    seen, frontier = bfs_reach()
    cleared = False
    # 先把可达格里的免费拾取/楼梯走掉（走一遍即可，无需决策）
    # 找可达且能开/能杀的关口，按"门优先、怪按名"固定序，逐个执行
    for (nx, ny) in sorted(frontier):
        o, msg = frontier[(nx, ny)]
        ty = M.TYPE.get(M.oatr(o, 3), '?')
        if o in (2, 4, 27):          # 门
            step += 1
            print('%3d 开 %2dF(%2d,%2d) %s   [%s]' % (step, f, nx, ny, info(o), msg))
            w.move(nx - w.hero.x, ny - w.hero.y)
            cleared = True
            break
        elif ty == 'MONSTER':        # 怪
            step += 1
            print('%3d 杀 %2dF(%2d,%2d) %s   [%s]' % (step, f, nx, ny, info(o), msg))
            w.move(nx - w.hero.x, ny - w.hero.y)
            cleared = True
            break
    if not cleared:
        break

print()
print('==== 最终连通（%dF 可达 %d 格，残留关口）====' % (f, len(bfs_reach()[0])))
seen, frontier = bfs_reach()
print('  可达格: ' + ' '.join('(%d,%d)' % c for c in sorted(seen)))
for c in sorted(frontier):
    o, msg = frontier[c]
    print('    (%2d,%2d) %-30s %s' % (c[0], c[1], info(o), msg))
