# -*- coding: utf-8 -*-
"""从已验证的 1F→21F 路线中切出 1F→11F 段，生成基线 CSV 与逐层汇总。
   前置：replay_csv.py 已确认整份 CSV 在新 World 里可 0 误差重放。"""
import csv
import io
import os
import re
import sys

sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/魔塔1_route_1F到21F.csv'
OUT = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/'
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def run():
    rows = list(csv.DictReader(io.open(SRC, encoding='utf-8', errors='replace')))
    w = M.World.new()
    h = w.hero
    first = {}
    seg = []
    stats = {'kill': 0, 'door': {}, 'key': {}, 'shop': 0, 'npc': 0}
    for i, r in enumerate(rows):
        tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
        ev = (r['event'] or '').strip()
        nxt = None
        if i + 1 < len(rows):
            nf, nx, ny = int(rows[i + 1]['floor']), int(rows[i + 1]['x']), int(rows[i + 1]['y'])
            if nf == tf:
                nxt = (nx - tx, ny - ty)
        cands = []
        for d in DIRS:
            c = w.clone()
            lg = c.move(*d)
            hh = c.hero
            if (hh.f, hh.x, hh.y) != (tf, tx, ty):
                continue
            sc = 0
            for k, cur in (('hp', hh.hp), ('atk', hh.atk), ('def', hh.dfn), ('gold', hh.gold)):
                if cur == int(r[k]):
                    sc += 1
            for k, kk in (('ky', 'y'), ('kb', 'b'), ('kr', 'r')):
                if hh.keys.get(kk, 0) == int(r[k]):
                    sc += 1
            if bool(ev) == bool(lg):
                sc += 1
            if nxt == d:
                sc += 2
            cands.append((sc, d))
        ok = max(cands)[1]
        log = w.move(*ok)
        txt = ''.join(log)
        seg.append((len(seg) + 1, h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
                    h.keys.get('y', 0), h.keys.get('b', 0), h.keys.get('r', 0), txt))
        if h.f not in first:
            first[h.f] = dict(step=len(seg), hp=h.hp, atk=h.atk, dfn=h.dfn, gold=h.gold,
                              ky=h.keys.get('y', 0), kb=h.keys.get('b', 0), kr=h.keys.get('r', 0))
        if '击杀' in txt:
            stats['kill'] += 1
        m = re.search(r'开(黄|蓝|红)门', txt)
        if m:
            stats['door'][m.group(1)] = stats['door'].get(m.group(1), 0) + 1
        if '购物' in txt:
            stats['shop'] += 1
        if 'NPC' in txt:
            stats['npc'] += 1
        if h.f == 11:
            break
    return rows, seg, first, stats, w


def leftover(w):
    """1F-10F 尚未拾取的道具/钥匙"""
    DOOR = {2: '黄门', 4: '蓝门', 27: '红门'}
    KEY = {1: '黄钥', 3: '蓝钥', 28: '红钥'}
    out = []
    for f in range(1, 11):
        got = []
        for y in range(1, 12):
            for x in range(1, 12):
                o = M.obj_raw(f, x, y)
                if not o or (f, x, y) in w.cleared:
                    continue
                a = [M.oatr(o, i) for i in range(14)]
                ty = M.TYPE.get(a[3], '?')
                if o in KEY:
                    got.append(((x, y), '钥' + KEY[o]))
                elif ty in ('STATUS', 'ITEM'):
                    got.append(((x, y), M.oname(o).strip().split('。')[0][:12]))
        if got:
            out.append((f, got))
    return out


def main():
    rows, seg, first, stats, w = run()
    print('1F→11F 共 %d 步' % len(seg))
    print('战斗 %d 场 / 开门 %s / 购物 %d 次 / NPC %d 次' % (stats['kill'], stats['door'], stats['shop'], stats['npc']))
    print('--- 首次到达各层 ---')
    for f in sorted(first):
        d = first[f]
        print('  %2dF step%-5d HP%-5d ATK%-3d DEF%-3d G%-5d 钥%d/%d/%d'
              % (f, d['step'], d['hp'], d['atk'], d['dfn'], d['gold'], d['ky'], d['kb'], d['kr']))

    with io.open(OUT + '魔塔1_route_1F到11F_基线.csv', 'w', encoding='utf-8', newline='') as fp:
        wr = csv.writer(fp)
        wr.writerow(['step', 'floor', 'x', 'y', 'hp', 'atk', 'def', 'gold', 'ky', 'kb', 'kr', 'event'])
        for s in seg:
            wr.writerow(s)
    print('已写 魔塔1_route_1F到11F_基线.csv')

    lines = ['# 魔塔1 1F→11F 基线（重放校验通过）', '',
             '- 来源：`01_PC98原版_mtower/魔塔1_route_1F到21F.csv` 前段，整份 CSV 在全新 World 中重放 **3232 行 0 误差**',
             '- 引擎：`tools/mota_core.py`（PC-98 原版口径）',
             '- 段长：**%d 步**；战斗 **%d** 场；开门 黄%d 蓝%d 红%d；购物 %d 次；NPC %d 次'
             % (len(seg), stats['kill'], stats['door'].get('黄', 0), stats['door'].get('蓝', 0),
                stats['door'].get('红', 0), stats['shop'], stats['npc']), '',
             '## 首次到达各层时的英雄状态', '',
             '| 层 | 步 | HP | ATK | DEF | GOLD | 黄 | 蓝 | 红 |', '|---|---|---|---|---|---|---|---|---|']
    for f in sorted(first):
        d = first[f]
        lines.append('| %dF | %d | %d | %d | %d | %d | %d | %d | %d |'
                     % (f, d['step'], d['hp'], d['atk'], d['dfn'], d['gold'], d['ky'], d['kb'], d['kr']))
    d = first[11]
    lines += ['', '## 进 11F 终态（本基线的关键修正）', '',
              '**HP %d / ATK %d / DEF %d / GOLD %d / 黄 %d 蓝 %d 红 %d**（第 %d 步）'
              % (d['hp'], d['atk'], d['dfn'], d['gold'], d['ky'], d['kb'], d['kr'], d['step']), '',
              '> 旧推演假设「进 11F 时 ATK 60 / DEF 50」不成立。实测 ATK 只有 **%d**、DEF **%d**。' % (d['atk'], d['dfn']),
              '> HP 仅剩 **%d**，也不足以直接进入 11F→20F 段——下游必须重排。' % d['hp'], '']
    lo = leftover(w)
    lines += ['## 走到 11F 时 1F–10F 剩余未拿的道具/钥匙', '',
              '（用于下游回补 HP / 钥匙；不含需先杀怪或开门的间接收益）', '']
    for f, got in lo:
        lines.append('- **%dF**：%s' % (f, ' '.join('(%d,%d)%s' % (c[0], c[1], nm) for c, nm in got)))
    lines += ['', '## 口径注意事项（两处引擎与源码可能不一致）', '',
              '1. **obj20「落穴」的通行性未定**。`objectAttribute` 里 obj19/20/21/23/79 全是 `a[3]=0`（NORMAL）；',
              '   `mota_core` 把 obj20/21/23 当可踩地板、把 obj79 当「掉血 200 的地砖」。',
              '   本项目早先记录过一条源码判据「c3==0 且 c4==1 才放行」，但现有属性表**所有物件 a[4] 全为 0**，该判据无法在数据上复现，',
              '   因此**不能拿它来判定 obj20**。本基线沿用 mota_core 口径（obj20 可踩），路线已完整跑通。',
              '2. 受影响的具体格：**8F(10,4)**（红钥匙 (10,2) 的必经格）、**10F(4,4)(8,4)**。',
              '   若日后确认 obj20 实心，8F 红钥匙须改走 9F/8F 的 **門番Ｃ 50/48/22**（需 ATK>22），8F/10F 走位要重排。',
              '3. **obj79 熔岩**在本段出现 **0 格**（全在 13F 80 格 / 26F 18 格），所以熔岩口径**不影响 1F→10F**。', '']
    io.open(OUT + '魔塔1_route_1F到11F_基线.md', 'w', encoding='utf-8').write('\n'.join(lines))
    print('已写 魔塔1_route_1F到11F_基线.md')
    print('--- 1F-10F 剩余 ---')
    for f, got in lo:
        print(' %2dF %s' % (f, ' '.join('(%d,%d)%s' % (c[0], c[1], nm) for c, nm in got)))


if __name__ == '__main__':
    main()
