# -*- coding: utf-8 -*-
"""静态房间结构（纯读图）：
   节点 = 可走地板（含拾取物），不把门/怪算进连通；
   门/怪作为"边"，列出它们连接的两个房间。
"""
import sys, io, collections

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
sys.path.insert(0, TOOLS)
import mota_core as M

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
NAME = {'y': '黄门', 'b': '蓝门', 'r': '红门'}


def walkable(f, x, y):
    if M.terrain(f, x, y) not in (0, 2):
        return False
    o = M.obj_raw(f, x, y)
    if not o:
        return True
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    return ty in ('STATUS', 'ITEM', 'KEY', 'MESSAGE', 'NORMAL', 'SEAL', 'SCORE', 'SAIDAN')


def edge(f, x, y):
    o = M.obj_raw(f, x, y)
    if not o:
        return None
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if ty == 'DOOR':
        if o == 89:
            return ('wall89', '可撞塌墙')
        col = M.DOOR_OF.get(o)
        return ('door', NAME.get(col, '门%d' % o))
    if ty == 'MONSTER':
        return ('mon', '%s %d/%d/%d' % (M.oname(o)[:6], M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12)))
    return None


out = []
for f in range(1, 12):
    cells = [(x, y) for y in range(13) for x in range(13) if walkable(f, x, y)]
    cs = set(cells)
    comp = {}
    cid = 0
    for c in cells:
        if c in comp:
            continue
        cid += 1
        comp[c] = cid
        q = collections.deque([c])
        while q:
            u = q.popleft()
            for dx, dy in DIRS:
                v = (u[0] + dx, u[1] + dy)
                if v in cs and v not in comp:
                    comp[v] = cid
                    q.append(v)
    out.append('=' * 74)
    out.append('%dF  房间 %d 个' % (f, cid))
    out.append('=' * 74)
    groups = collections.defaultdict(list)
    for c in cells:
        groups[comp[c]].append(c)
    for g in sorted(groups, key=lambda k: -len(groups[k])):
        gc = groups[g]
        loot = []
        st = []
        for (x, y) in gc:
            o = M.obj_raw(f, x, y)
            if M.terrain(f, x, y) == 2:
                st.append('(%d,%d)' % (x, y))
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            tag = ''
            if ty == 'STATUS':
                tag = 'HP+%d/ATK+%d/DEF+%d' % (M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12))
            elif ty == 'KEY':
                tag = 'key'
            loot.append('(%d,%d)%s%s' % (x, y, M.oname(o)[:7], ('[' + tag + ']') if tag else ''))
        out.append(' R%d %d格 楼梯%s' % (g, len(gc), ','.join(st) or '无'))
        out.append('   物件: %s' % ('; '.join(loot) or '无'))
        out.append('   格: %s' % ' '.join('(%d,%d)' % c for c in sorted(gc, key=lambda t: (t[1], t[0])))
    # 边：每个门/怪格，看它四邻属于哪些房间
    out.append(' --- 关口 ---')
    for y in range(13):
        for x in range(13):
            e = edge(f, x, y)
            if not e:
                continue
            nb = set()
            for dx, dy in DIRS:
                v = (x + dx, y + dy)
                if v in comp:
                    nb.add(comp[v])
            out.append('  (%2d,%2d) %-4s %-22s 连接房间 %s' % (
                x, y, e[0], e[1], ','.join('R%d' % k for k in sorted(nb)) or '(无)'))
    out.append('')

io.open(r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/rooms_1_11.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
