# -*- coding: utf-8 -*-
"""11F→38F 最终路线：绕门优先（蓝门权重 60000）+ 剧情事件格放行 + 钥匙账结算。

与旧版（Dijkstra 门权重 20000、步数最优）的根本差别：
  旧版挑「步数最少」的门，14F 就开掉 2 道蓝门，一路欠账到 38F 欠 4 把；
  本版把蓝门代价抬到 60000（≈绕 60 步），逼它绕路，结果主线几乎不用蓝钥匙。

事件/动态格按源码结论手工放行（静态地图里它们看着是墙或不存在）：
  15F (6,6) 大乌贼本体 / (6,5) 镐      —— 杀本体后 9 格清空才生成镐
  20F (6,9) 红门 → (6,6) 吸血鬼 → (6,1) 上梯（BOSS 死后生成）
  29F (6,3) 墙                        —— 需先上 29F 再下楼才开
  35F (4,9) 盗贼暗道（(5,10) 触发）
  38F (2,5) 落穴                      —— 踩 (2,6) 后生成，回程该缝即断
"""
import sys, csv, heapq
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

W_Y, W_B, W_R = 60, 60000, 40000
W_MON, W_LAVA = 8, 25

# 事件放行格：静态地图判为墙/无，实为可走
EXTRA = {
    15: {(6, 6), (6, 5), (6, 3), (6, 9), (8, 1)},   # 杀本体后 9 格清空 + 两条落穴消失
    20: {(6, 9), (6, 8), (6, 6), (6, 3), (6, 1)},   # BOSS 死后双封印 (6,3)(6,9) 解除
    29: {(6, 3)},
    35: {(4, 9), (5, 10)},
    30: {(6, 6), (6, 1)},
    37: {(2, 4), (6, 4), (2, 7), (6, 7), (2, 8)},   # 四座库：用镐（15F 大乌贼掉落）破墙进入
}

JOBS = [
    (11, (6, 11), (11, 11)), (12, (10, 11), (1, 11)), (13, (2, 11), (11, 11)),
    (14, (10, 11), (6, 11)), (15, (6, 10), (6, 1)),   (16, (6, 2),  (6, 11)),
    (17, (6, 10), (6, 1)),   (18, (6, 2),  (1, 1)),   (19, (1, 2),  (6, 11)),
    (20, (6, 10), (6, 1)),   (21, (6, 2),  (6, 11)),  (22, (6, 10), (6, 6)),
    (23, (1, 2),  (11, 1)),  (24, (2, 11), (2, 10)),  (25, (2, 11), (1, 11)),
    (26, (2, 11), (2, 10)),  (27, (2, 11), (11, 11)), (28, (10, 11), (1, 11)),
    (29, (1, 10), (6, 11)),  (30, (6, 10), (6, 1)),   (31, (6, 2),  (6, 11)),
    (32, (6, 10), (11, 1)),  (33, (10, 1), (1, 1)),   (34, (2, 1),  (6, 11)),
    (35, (6, 10), (11, 1)),  (36, (11, 2), (11, 11)), (37, (11, 10), (1, 1)),
]
# 每层额外要去的点（道具/剧情），在落点之后、上梯之前
MUST = {
    13: [(6, 5)],                       # 神剣（穿熔岩 4 格）
    14: [(1, 3)],                       # 暗墙后的红钥匙 ← 20F 红门的唯一来源
    15: [(6, 6), (6, 5)],               # 大乌贼本体 + 镐
    19: [(6, 3)],                       # 十字架
    20: [(6, 9), (6, 6)],               # 红门 + 吸血鬼 BOSS
    29: [],                             # 29F 由 28F 折返开墙，见 SPECIAL
    35: [(5, 10), (4, 9)],              # 盗贼 + 暗道
    32: [(11, 7)],                       # 蓝钥匙（(4,8) 在祭坛区另一侧，绕路代价大，跳过）
    37: [(7, 5), (4, 9), (5, 9)],       # 红钥匙 + 两把蓝钥匙
    31: [(4, 4)],                       # 蓝钥匙
}
# 38F 特殊：去程走 (2,4)-(2,5)-(2,6) 缝取盾，回程缝已断，必须蓝门链
F38_GO = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
          (10, 1), (10, 2), (10, 3), (10, 4), (9, 4), (8, 4), (7, 4), (6, 4),
          (5, 4), (4, 4), (3, 4), (2, 4), (2, 5), (2, 6), (2, 7)]
F38_BACK = [(2, 7), (2, 6), (3, 6), (4, 6), (5, 6), (5, 5), (5, 4), (4, 4),
            (3, 4), (2, 4), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1), (5, 1),
            (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1)]


def cell_cost(f, x, y):
    if (x, y) in EXTRA.get(f, set()):
        return 1, '事件'
    t = M.terrain(f, x, y)
    if t == 1:
        return (2, '暗墙') if (f, x, y) in M.DARKWALL_CELLS else None
    o = M.obj_raw(f, x, y)
    if o == 89:
        return 2, '暗墙'
    if o == 115:
        return 2, '隐形块'
    if o == 79:
        return W_LAVA, '熔岩'
    if o in (2, 4, 27):
        return {2: W_Y, 4: W_B, 27: W_R}[o], {2: '黄门', 4: '蓝门', 27: '红门'}[o]
    if o == 20:
        return None
    if o and M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
        return W_MON, '怪'
    return 1, ''


def dijkstra(f, s, g):
    dist, pre, h = {s: 0}, {s: None}, [(0, s)]
    while h:
        d, c = heapq.heappop(h)
        if c == g:
            break
        if d > dist.get(c, 1 << 60):
            continue
        x, y = c
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if not (0 <= n[0] < 13 and 0 <= n[1] < 13):
                continue
            cc = cell_cost(f, n[0], n[1])
            if cc is None:
                continue
            nd = d + cc[0]
            if nd < dist.get(n, 1 << 60):
                dist[n] = nd; pre[n] = c; heapq.heappush(h, (nd, n))
    if g not in pre:
        return None
    p, c = [], g
    while c is not None:
        p.append(c); c = pre[c]
    return p[::-1]


def scan(f, full):
    """统计一条路径上的门/钥匙/战斗"""
    d = {'黄门': [], '蓝门': [], '红门': []}
    k = {'黄': [], '蓝': [], '红': []}
    m = []
    for (x, y) in full:
        o = M.obj_raw(f, x, y)
        if o == 2:
            d['黄门'].append((x, y))
        elif o == 4:
            d['蓝门'].append((x, y))
        elif o == 27:
            d['红门'].append((x, y))
        elif o == 1:
            k['黄'].append((x, y))
        elif o == 3:
            k['蓝'].append((x, y))
        elif o == 28:
            k['红'].append((x, y))
        elif o == 79:
            m.append('熔岩(%d,%d)' % (x, y))
        elif o and M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
            m.append('%s(%d,%d)' % (M.oname(o)[:6], x, y))
    return d, k, m


def auto_keys(f):
    """本层所有钥匙格（obj1 黄 / obj3 蓝 / obj28 红）"""
    return [(x, y) for y in range(13) for x in range(13)
            if M.obj_raw(f, x, y) in (1, 3, 28)]


def main():
    bal = {'黄': 0, '蓝': 0, '红': 0}
    rows = []
    for f, s, g in JOBS:
        cand = list(dict.fromkeys(MUST.get(f, []) + auto_keys(f)))
        cand = [c for c in cand if c != s and c != g]
        chain, cur = [s], s
        while cand:
            best, bp = None, None
            for c in cand:
                p = dijkstra(f, cur, c)
                if p and (best is None or len(p) < best):
                    best, bp, bc = len(p), p, c
            if bp is None:
                break
            chain += bp[1:]
            cur = bc
            cand.remove(bc)
        chain.append(g)
        full, ok = [], True
        for a, b in zip(chain, chain[1:]):
            p = dijkstra(f, a, b)
            if p is None:
                ok = False
                continue
            full += p if not full else p[1:]
        if not ok:
            print('%2dF ✗ 有断段' % f)
            continue
        d, k, m = scan(f, full)
        # 同一道门在去/回程会经过两次，只扣一次
        for c in ('黄', '蓝', '红'):
            bal[c] += len(set(k[c])) - len(set(d[c + '门']))
        rows.append((f, s, g, len(full) - 1, d, k, m))
        print('%2dF %s→%s %3d步  开 黄%d/蓝%d/红%d  拾 黄%d/蓝%d/红%d  余 %+d/%+d/%+d' % (
            f, s, g, len(full) - 1,
            len(set(d['黄门'])), len(set(d['蓝门'])), len(set(d['红门'])),
            len(set(k['黄'])), len(set(k['蓝'])), len(set(k['红'])),
            bal['黄'], bal['蓝'], bal['红']))
        for c in ('黄', '蓝', '红'):
            if d[c + '门']:
                print('       开%s门 %s' % (c, sorted(set(d[c + '门']))))
            if k[c]:
                print('       拾%s钥 %s' % (c, sorted(set(k[c]))))

    # 38F：去程 + 回程合成一条序列，scan 一次（set 天然去掉重复经过的门）
    seq38 = F38_GO + F38_BACK[1:]
    for tag, seq in (('38F 去程取盾', F38_GO), ('38F 回程出层', F38_BACK)):
        d, k, m = scan(38, seq)
        print('%s %d步  途经门 黄%s 蓝%s 红%s  拾 %s' % (
            tag, len(seq) - 1, sorted(set(d['黄门'])), sorted(set(d['蓝门'])),
            sorted(set(d['红门'])),
            ' '.join('%s钥%s' % (c, sorted(set(k[c]))) for c in ('黄', '蓝', '红') if k[c]) or '无'))
        print('       战/险 %s' % (' '.join(m) or '无'))
    d, k, m = scan(38, seq38)
    for c in ('黄', '蓝', '红'):
        bal[c] += len(set(k[c])) - len(set(d[c + '门']))
    print('38F 合计 %d 步  实开门 黄%s 蓝%s 红%s' % (
        len(seq38) - 1, sorted(set(d['黄门'])), sorted(set(d['蓝门'])), sorted(set(d['红门']))))
    # 14F (1,3) 是暗墙，撞开后底下才是红钥匙 obj28，obj_raw 里看不到，手工 +1
    bal['红'] += 1
    print('＋14F(1,3) 暗墙后红钥匙 obj28（obj_raw 看不到，手工补 +1）')
    print()
    print('11F→38F 净收支（不含 1F–10F 存量）：', bal)

    with open(r'D:/B++/WorkBuddy/mota_tas_tmp2/魔塔1_钥匙账_11F到38F_绕门版.csv',
              'w', newline='', encoding='utf-8-sig') as fp:
        cw = csv.writer(fp)
        cw.writerow(['楼层', '落点', '上梯', '步数', '开黄门', '开蓝门', '开红门',
                     '拾黄钥匙', '拾蓝钥匙', '拾红钥匙', '结余黄', '结余蓝', '结余红'])
        b = {'黄': 0, '蓝': 0, '红': 0}
        for (f, s, g, n, d, k, m) in rows:
            for c in ('黄', '蓝', '红'):
                b[c] += len(set(k[c])) - len(set(d[c + '门']))
            cw.writerow(['%dF' % f, '%d,%d' % s, '%d,%d' % g, n,
                         len(set(d['黄门'])), len(set(d['蓝门'])), len(set(d['红门'])),
                         len(set(k['黄'])), len(set(k['蓝'])), len(set(k['红'])),
                         b['黄'], b['蓝'], b['红']])
        d, k, m = scan(38, F38_GO + F38_BACK[1:])
        for c in ('黄', '蓝', '红'):
            b[c] += len(set(k[c])) - len(set(d[c + '门']))
        b['红'] += 1                       # 14F(1,3) 暗墙后的红钥匙
        cw.writerow(['38F', '%d,%d' % F38_GO[0], '%d,%d' % F38_BACK[-1],
                     len(F38_GO) + len(F38_BACK) - 2,
                     len(set(d['黄门'])), len(set(d['蓝门'])), len(set(d['红门'])),
                     len(set(k['黄'])), len(set(k['蓝'])), len(set(k['红'])) + 1,
                     b['黄'], b['蓝'], b['红']])
        cw.writerow(['合计', '', '', sum(r[3] for r in rows) + len(F38_GO) + len(F38_BACK) - 2,
                     '', '', '', '', '', '', b['黄'], b['蓝'], b['红']])


if __name__ == '__main__':
    main()
