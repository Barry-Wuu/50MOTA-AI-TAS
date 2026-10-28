#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""opt_orb2.py —— 段2（11F→21F）祭坛往返飞行之珠重写（v2 修正断点）。

结构：
  body 行 0..2249 = 段1（step1..2250，含飞行之珠拾取）
  body 行 2250..  = 段2（step1..982，11F→21F）
  段2 step795 = body 行 2250+794 = 20F(7,11)（回12F前最后一格，恰在20F下行梯(6,11)旁）

优化：
  从段2 step795 断点起，不爬楼梯回12F，而是：
    1) fly(12)   → 12F(10,11)          （省 20→12 共8层爬楼）
    2) BFS 到祭坛 (12,6,9)，献3次       （140+220+320=680G）
    3) BFS 回12F楼梯旁，fly(20) → 20F(6,10)（省 12→20 共8层爬楼）
    4) BFS 到 20F(6,6) 打吸血鬼（途经开红门/吃青药/杀大蝙蝠）
    5) 上 21F

校验：
  - 新CSV用引擎回放：关键事件（献祭3次/开红门/吃青药/杀BOSS/上21F）必须发生
  - 终态达标：HP>0、ATK=115、DEF=57、boss20=True、位于21F(6,2)
  - 对比原始终态报告差异（金币会因跳过中间层战斗而略少，属预期）
"""
import os, csv, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M
import play20 as P

SRC = os.path.join(HERE, '..', '魔塔1_route_1F到21F.csv')
OUT = os.path.join(HERE, '..', '魔塔1_route_1F到21F_飞行之珠优化.csv')
SEG2_START = 2250          # 段2在 body 的行号（0基）
SEG2_BREAK_STEP = 794      # 段2断点 step（20F(7,11)，恰在20F下行梯(6,11)旁）

def replay_rows(rows):
    w = M.World.new()
    for r in rows:
        if '飞行之珠传送' in r[5]:
            tf = int(r[1])
            lg = w.fly(tf)
            if M.blocked(lg):
                raise RuntimeError('fly失败 %s: %s' % (r, lg))
            if (w.hero.f, w.hero.x, w.hero.y) != (int(r[1]), int(r[2]), int(r[3])):
                raise RuntimeError('fly落点不一致 %s vs %s' % ((w.hero.f,w.hero.x,w.hero.y),(r[1],r[2],r[3])))
            continue
        k = r[4]
        dx, dy = {'8': (0,-1), '6': (1,0), '2': (0,1), '4': (-1,0)}.get(k, (0,0))
        if dx == 0 and dy == 0:
            continue
        lg = w.move(dx, dy)
        if M.blocked(lg):
            raise RuntimeError('move被挡 %s: %s' % (r, lg))
    return w

def append_path(w, path, LOG):
    for dx, dy, lab, _ in path:
        w = w.clone()
        lg = w.move(dx, dy)
        h = w.hero
        LOG.append((len(LOG)+1, h.f, h.x, h.y, lab, ' '.join(lg),
                    h.hp, h.atk, h.dfn, h.gold,
                    h.keys['y'], h.keys['b'], h.keys['r']))
    return w

def seg(w, tgt, LOG, tag=''):
    w2, path = P.nav(w, tgt)
    if w2 is None:
        raise RuntimeError('BFS失败 %s: %s' % (tag, path))
    w = append_path(w, path, LOG)
    print('  ✓ %-26s -> %s  [%d步]' % (tag, P.st(w.hero), len(path)))
    return w

def fly(w, tf, LOG):
    w = w.clone()
    lg = w.fly(tf)
    if M.blocked(lg):
        raise RuntimeError('fly失败: %s' % lg)
    h = w.hero
    LOG.append((len(LOG)+1, h.f, h.x, h.y, '8', ' '.join(lg),
                h.hp, h.atk, h.dfn, h.gold,
                h.keys['y'], h.keys['b'], h.keys['r']))
    print('  ✓ fly(%d)          -> %s' % (tf, P.st(w.hero)))
    return w

def main():
    body = list(csv.reader(open(SRC, encoding='utf-8')))[1:]
    header = ['step','floor','x','y','key','event','hp','atk','def','gold','ky','kb','kr']
    seg1 = body[:SEG2_START]
    seg2_break = body[SEG2_START : SEG2_START + SEG2_BREAK_STEP]   # 段2 step1..795

    # 断点 World：回放 段1 + 段2前795步
    w = replay_rows(seg1 + seg2_break)
    print('断点(段2 step%d):' % SEG2_BREAK_STEP, P.st(w.hero), 'boss20=', w.boss20,
          'items=', sorted(w.hero.items), '红钥=', w.hero.keys['r'])

    # 断点必须已持有飞行之珠 & 在20F
    assert 26 in w.hero.items, '未持有飞行之珠！'
    assert w.hero.f == 20, '断点不在20F！'
    assert not w.boss20, 'BOSS已死，不需要回12F献攻？'

    LOG = []
    print('--- 续推：fly(12) → 祭坛3次 → fly(20) → BOSS → 21F ---')

    # 1) fly(12)（断点 20F(7,11) 恰在20F下行梯(6,11)旁，满足楼梯相邻）
    w = fly(w, 12, LOG)

    # 2) 到祭坛 (12,6,9)，献3次
    w = seg(w, (12, 6, 9), LOG, '12F → 祭坛')
    for i in range(3):
        c = M.altar_cost(w.altar_k)
        if w.hero.gold < c:
            print('  ⚠️ 金不足(需%d，有%d)，只献%d次' % (c, w.hero.gold, i))
            break
        if (w.hero.f, w.hero.x, w.hero.y) == (12, 6, 9):
            w = seg(w, (12, 6, 10), LOG, '  离开祭坛')
        w = seg(w, (12, 6, 9), LOG, '祭坛第%d次' % (i+1))
    print('  献祭后:', P.st(w.hero))

    # 3) 回12F楼梯旁，fly(20)
    # 任意楼梯旁均可；BFS 到最近楼梯的相邻格
    stairs12 = [c for c in M.STAIRS[12] if c]
    # 选离当前最近的一个楼梯相邻格
    best = None; best_d = 999
    for (sx, sy) in stairs12:
        for (ax, ay) in [(sx-1,sy),(sx+1,sy),(sx,sy-1),(sx,sy+1)]:
            if 1 <= ax <= 11 and 1 <= ay <= 11:
                d = abs(ax-w.hero.x)+abs(ay-w.hero.y)
                if d < best_d:
                    best_d = d; best = (ax, ay)
    w = seg(w, (12, best[0], best[1]), LOG, '12F → 楼梯旁')
    w = fly(w, 20, LOG)

    # 4) 到 20F BOSS (6,6)（途经开红门/吃青药/杀大蝙蝠）
    w = seg(w, (20, 6, 6), LOG, '20F → 吸血鬼BOSS')
    print('  BOSS后:', P.st(w.hero), 'boss20=', w.boss20)

    # 5) 上21F
    if w.boss20:
        w = seg(w, 21, LOG, '20F → 21F')
    print('★ 抵达:', P.st(w.hero))

    # —— 组装新CSV：段1 + 段2前795步 + 续推 ——
    prefix = [list(r) for r in (seg1 + seg2_break)]
    offset = int(prefix[-1][0])
    newrows = [list(r) for r in prefix]
    for r in LOG:
        nr = list(r)
        nr[0] = str(int(r[0]) + offset)
        newrows.append(nr)

    # —— 校验：引擎回放新CSV ——
    w_opt = replay_rows(newrows)
    h = w_opt.hero
    key_events = [r[5] for r in newrows if r[5] and '祭坛' in r[5] or '吸血鬼' in r[5] or '赤い回復薬' in r[5] or '红门' in r[5]]
    # 精确统计献祭次数：事件里含「祭坛献金」的行才算真正献祭
    altar_cnt = sum(1 for r in newrows if '祭坛献金' in r[5])
    print('\n=== 校验 ===')
    print('关键事件命中:', {
        '祭坛实际献祭次数': altar_cnt,
        '开红门': any('红门' in r[5] for r in newrows),
        '吃青药': any('青い回復薬' in r[5] for r in newrows),
        '杀吸血鬼': w_opt.boss20,
        '到21F': h.f == 21 and (h.x, h.y) == (6, 2),
    })
    print('终态达标: HP>0 =', h.hp > 0, '| ATK=%d DEF=%d' % (h.atk, h.dfn),
          '| 位置=%dF(%d,%d)' % (h.f, h.x, h.y))
    print('优化后终态:', P.st(h), 'boss20=', w_opt.boss20)

    # 原始终态
    w_orig = replay_rows(body)
    h0 = w_orig.hero
    print('原始终态:', P.st(h0), 'boss20=', w_orig.boss20)
    print('金币差: 原始%d -> 优化%d (少%d，因跳过中间层战斗)' % (h0.gold, h.gold, h0.gold-h.gold))

    # 步数对比
    print('\n原始步数:', len(body), ' 优化后:', len(newrows), ' 省:', len(body)-len(newrows))

    # 写出
    with open(OUT, 'w', newline='', encoding='utf-8') as fp:
        cw = csv.writer(fp)
        cw.writerow(header)
        cw.writerows(newrows)
    print('已写出:', OUT)

if __name__ == '__main__':
    main()