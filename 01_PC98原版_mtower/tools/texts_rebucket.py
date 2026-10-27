#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 CSV 的 floors 重建 magic_tower1_texts.md 的楼层分章（正文内容零改动）。

用途：楼层归属修正后重排。FLOOR_FIX 为本轮从字节码新定的落点。
用法：python3.11 rebucket.py [--write]
"""
import re, os, csv, sys
from collections import defaultdict

BASE = '/tmp/motarepo2/01_PC98原版_mtower'
SRC = os.path.join(BASE, 'magic_tower1_texts.md')
CSVP = os.path.join(BASE, 'magic_tower1_texts.csv')

# 本轮用字节码定出的楼层（覆盖 CSV 里的 —）
FLOOR_FIX = {
    2: '2',    # 2F 牢房醒来：开场脚本 266「・・・」→2「…おい…」→3「…おいっ！起きろ！」，
               # 紧接 [4] obj87 盗賊「おまえ…牢屋に入れられてた…今まで気を失っていた」；
               # 塔门口的 [10]/[11] 是 1F，被打晕后才切到 2F
    3: '2',    # 同上
    17: '15',  # obj88 写在 15F(9,1)，同处 objectAttribute[88][5]=17；文中「大ダコ」在 15F
    22: '26',  # eventMT 22511-22573：勇者站在 26F(6,7) 才触发（26F(6,6) 是偽王女的人形 obj44）
}

NOFLOOR_NOTE = [
    '余下这些条目没有楼层归属，按编号升序，共 {n} 条。原因分两类：',
    '',
    '- 纯系统反馈——开关门、梯子/人物存在提示、钥匙不足、道具使用与伤害结算、存读档、音效开关、'
    '界面标签、评语与称号等，任何楼层都可能出现，没有「本层专属」的含义（含购买时余额不足的 [18]）；',
    '- 挂在 obj40 / obj155 / obj167 / obj172 / obj17 上的 5 条（[57] [58] [72] [83] [89]）：'
    '这五个对象在 0F–50F 全部地图里没有任何落点（静态布点、`FLOOR_WRITES` 事件写入、`DYNEV` 动态投放'
    '三路都查过），文本在游戏里不会出现，属未使用条目。',
]


def parse(text):
    lines = text.split('\n')
    chapters, i, n = [], 0, len(lines)
    while i < n and not lines[i].startswith('### '):
        i += 1
    while i < n and lines[i].startswith('### '):
        title = lines[i]; i += 1
        blocks, cur = [], None
        while i < n and not lines[i].startswith('### '):
            L = lines[i]
            if L.startswith('**['):
                if cur: blocks.append(cur)
                cur = [L]
            elif cur is None:
                if L.strip(): cur = [L]
            else:
                cur.append(L)
            i += 1
        if cur: blocks.append(cur)
        for b in blocks:
            while b and b[-1].strip() == '':
                b.pop()
        chapters.append((title, blocks))
    return chapters


HEAD = re.compile(r'^\*\*\[(\d+)\]\*\*(.*)$')


def split_head(h):
    m = HEAD.match(h)
    return int(m.group(1)), m.group(2).rstrip()


def expand(floors):
    fl = set()
    for t in re.split(r'[,\s\u3000]+', floors.strip()):
        if not t or t == '—':
            continue
        m = re.fullmatch(r'(\d+)(?:-(\d+))?', t)
        if m:
            a = int(m.group(1)); b = int(m.group(2) or a)
            fl.update(range(a, b + 1))
        elif t == '00F':
            fl.add(0)
        elif t in ('catalog', 'stage_flags'):
            pass
        else:
            raise ValueError('未知标记 ' + t)
    return fl


def main():
    entries = {}          # id -> (mid, body)
    for title, blocks in parse(open(SRC, encoding='utf-8').read()):
        for b in blocks:
            if not b[0].startswith('**['):
                continue
            idx, mid = split_head(b[0])
            if idx in entries:
                assert entries[idx] == (mid, b[1:]), '同一编号内容不一致 %d' % idx
                continue
            entries[idx] = (mid, b[1:])
    print('解析条目 %d' % len(entries))

    rows = list(csv.DictReader(open(CSVP, encoding='utf-8')))
    floors = {}
    group = {}
    for r in rows:
        i = int(r['strNumber'])
        floors[i] = FLOOR_FIX.get(i, r['floors'])
        group[i] = r['group']
    missing = set(entries) - set(floors)
    if missing:
        raise SystemExit('CSV 缺编号 %s' % sorted(missing))

    by_floor = defaultdict(list)
    nofloor = []
    for i in entries:
        fl = expand(floors[i])
        if fl:
            for f in fl:
                by_floor[f].append(i)
        else:
            nofloor.append(i)

    def block(i):
        mid, body = entries[i]
        return ['**[%d]**%s' % (i, mid)] + body

    cat = defaultdict(list)
    for i, g in group.items():
        cat[g].append(i)
    cats = sorted(cat.items(), key=lambda kv: min(kv[1]))
    total = sum(len(v) for v in by_floor.values())

    out = [
        '# 魔塔1 塔内全部对话 / 提示文案',
        '',
        '按**出现楼层**编排：0F–50F 共 51 章，另加 1 章「无楼层归属」。机读版见 '
        '`magic_tower1_texts.csv`（保留原始 `floors` 字符串与 `group` 字段，共 309 行）。',
        '',
        '**编排规则**',
        '',
        '- 章题即楼层，条目本身不写「出现层」；',
        '- 同层条目按 `[n]` 编号升序；',
        '- 一条文案若在多层出现（怪物名、地形提示等多为此类），在每个对应楼层章各写一遍，内容完全相同；'
        '因此本文实际条目数（%d）大于文案表行数（309）。' % total,
        '- 不挂地图数据、没有楼层概念的统一放在最后的「无楼层归属」章，同样按编号升序。',
        '',
        '每条内容为两段：日文原文（`>` 引用块）与 `EN:` 英文译文。编号左侧是**引用方式**：',
        '',
        '- `objN（数据引用）` / `地形N（数据引用）`——由对象表 / 地形表的 `ATR_STRING` 列挂上；',
        '- `代码 strNumber=N ← 函数名`——由指令流里 `sipush N; putfield strNumber` 直接指定'
        '（开场与战后台词、钥匙不足、菜单确认等），这类文案不挂在地图数据上；',
        '- `运行时按计算下标引用`——文案确实会在游戏里显示，但引用处的下标是算出来的'
        '（按楼层、分支、序号偏移），未能静态定位到引用点，故不猜楼层；',
        '',
        '少数条目（怪物名、钥匙与道具取得提示等）的楼层除地图布点外，还依据「怪物图鉴登记」与'
        '「关卡旗标表」两路数据交叉核对，原始 `floors` 字段（含 `catalog` / `stage_flags` / `00F` 标记）'
        '见 `magic_tower1_texts.csv`。',
        '',
        '原文的 12 个分组在正文里不再分章，编号索引如下（编号是文本表下标，与阅读顺序无关）：',
        '',
    ]
    for g, ids in cats:
        out.append('- **%s**（%d）：%s' % (g, len(ids), '、'.join(str(i) for i in sorted(ids))))
    out.append('')

    for f in range(51):
        ids = sorted(by_floor.get(f, []))
        out.append('')
        out.append('### %dF' % f)
        for i in ids:
            out.append('')
            out.extend(block(i))
    out.append('')
    out.append('### 无楼层归属')
    out.append('')
    for line in [x.replace('{n}', str(len(nofloor))) for x in NOFLOOR_NOTE]:
        out.append(line)
    for i in sorted(nofloor):
        out.append('')
        out.extend(block(i))
    out.append('')

    new = '\n'.join(out)
    print('条目块 %d，无楼层 %d，行数 %d' % (total, len(nofloor), new.count('\n')))
    if '--write' in sys.argv:
        open(SRC, 'w', encoding='utf-8').write(new)
        for r in rows:
            i = int(r['strNumber'])
            if i in FLOOR_FIX:
                r['floors'] = FLOOR_FIX[i]
        with open(CSVP, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=['strNumber', 'text_jp', 'text_en', 'referenced_by', 'floors', 'group'])
            w.writeheader(); w.writerows(rows)
        print('已写回 md + csv')
    else:
        open('/tmp/rebucket_preview.md', 'w', encoding='utf-8').write(new)
        print('预览 /tmp/rebucket_preview.md')


if __name__ == '__main__':
    main()
