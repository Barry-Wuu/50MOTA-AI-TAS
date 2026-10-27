#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 magic_tower1_texts.md 由「按分组分章」改为「按楼层分章」。

规则：
  1. 章题 = 0F…50F；同层条目按 [n] 编号升序；条目不再写出「出现层」。
  2. 无楼层归属（—）的条目合并到最后一章。
  3. 一条文案对应多层的，在每个对应楼层章各写一遍（内容完全相同）。

用法：python3.11 texts_by_floor.py [--write]
"""
import re, sys, os, csv
from collections import defaultdict, Counter

BASE = '/tmp/motarepo2/01_PC98原版_mtower'
SRC = os.path.join(BASE, 'magic_tower1_texts.md')
CSV = os.path.join(BASE, 'magic_tower1_texts.csv')

FLAG_TAG = {'catalog': '图鉴', 'stage_flags': '关卡旗标'}


def parse(text):
    lines = text.split('\n')
    prefix, chapters = [], []
    i, n = 0, len(lines)
    while i < n and not lines[i].startswith('### '):
        prefix.append(lines[i]); i += 1
    while i < n and lines[i].startswith('### '):
        title = lines[i]; i += 1
        blocks, cur = [], None
        while i < n and not lines[i].startswith('### '):
            L = lines[i]
            if L.startswith('**['):
                if cur is not None:
                    blocks.append(cur)
                cur = [L]
            elif cur is None:
                if L.strip():
                    cur = [L]
            else:
                cur.append(L)
            i += 1
        if cur is not None:
            blocks.append(cur)
        for b in blocks:
            while b and b[-1].strip() == '':
                b.pop()
        chapters.append((title, blocks))
    return prefix, chapters


HEAD_RE = re.compile(r'^\*\*\[(\d+)\]\*\*(.*)$')


def split_head(head):
    """→ (id, 引用方式描述(带前导全角空格), 出现层字符串)"""
    m = HEAD_RE.match(head)
    if not m:
        raise ValueError('无法解析标题行: ' + head)
    idx = int(m.group(1))
    mid = m.group(2)
    p = mid.find('出现层：')
    floors = ''
    if p >= 0:
        floors = mid[p + 4:].strip()
        mid = mid[:p]
    mid = re.sub(r'[\s\u3000·]+$', '', mid)
    if mid:
        mid = ' ' + mid.lstrip()
    return idx, mid, floors


def expand(floors):
    """出现层字符串 → (楼层集合, 佐证标记列表)"""
    fl, tags = set(), []
    for t in re.split(r'[,\s\u3000]+', floors.strip()):
        if not t or t == '—':
            continue
        m = re.fullmatch(r'(\d+)(?:-(\d+))?', t)
        if m:
            a = int(m.group(1)); b = int(m.group(2) or a)
            fl.update(range(a, b + 1))
        elif t == '00F':
            fl.add(0)
        elif t in FLAG_TAG:
            tags.append(FLAG_TAG[t])
        else:
            raise ValueError('未知出现层标记: ' + t)
    return fl, tags


def main():
    text = open(SRC, encoding='utf-8').read()
    prefix, chapters = parse(text)

    entries = {}          # id -> dict(mid, body_lines, floors, tags, group)
    group_of = {}
    for title, blocks in chapters:
        g = re.sub(r'^###\s*', '', title)
        g = re.sub(r'（\d+\s*条）$', '', g).strip()
        for b in blocks:
            idx, mid, floors = split_head(b[0])
            fl, tags = expand(floors)
            if idx in entries:
                raise ValueError('重复编号 %d' % idx)
            entries[idx] = dict(mid=mid, body=b[1:], floors=fl, tags=tags)
            group_of[idx] = g
    print('解析条目 %d' % len(entries))

    by_floor = defaultdict(list)
    nofloor = []
    for idx, e in entries.items():
        if e['floors']:
            for f in e['floors']:
                by_floor[f].append(idx)
        else:
            nofloor.append(idx)

    def block(idx):
        e = entries[idx]
        return ['**[%d]**%s' % (idx, e['mid'])] + e['body']

    # ---- 前言 ----
    cat_idx = defaultdict(list)
    for idx, g in group_of.items():
        cat_idx[g].append(idx)
    cats = sorted(cat_idx.items(), key=lambda kv: min(kv[1]))

    head_txt = [
        '# 魔塔1 塔内全部对话 / 提示文案',
        '',
        '按**出现楼层**编排：0F–50F 共 51 章，另加 1 章「无楼层归属」。机读版见 '
        '`magic_tower1_texts.csv`（保留原始 `floors` 字符串与 `group` 字段，共 309 行）。',
        '',
        '**编排规则**',
        '',
        '- 章题即楼层，条目本身不再写「出现层」；',
        '- 同层条目按 `[n]` 编号升序；',
        '- 一条文案若在多层出现（怪物名、地形提示等多为此类），在每个对应楼层章各写一遍，内容完全相同；'
        '因此本文实际条目数（%d）大于文案表行数（309）。' % sum(len(v) for v in by_floor.values()),
        '- 不挂地图数据、没有楼层概念的（开场/战后台词、菜单与系统提示、钥匙不足等）统一放在最后的'
        '「无楼层归属」章，同样按编号升序。',
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
        head_txt.append('- **%s**（%d）：%s' % (g, len(ids), '、'.join(str(i) for i in sorted(ids))))
    head_txt.append('')

    out = list(head_txt)
    for f in range(51):
        ids = sorted(by_floor.get(f, []))
        out.append('')
        out.append('### %dF' % f)
        if not ids:
            out.append('')
            out.append('（本层无专属文案，见相邻楼层与末章。）')
            continue
        for idx in ids:
            out.append('')
            out.extend(block(idx))
    out.append('')
    out.append('### 无楼层归属（—）')
    out.append('')
    out.append('这些文案不落在地图格上，或引用下标在运行时算出、无法静态定位到具体楼层；'
               '按编号升序，共 %d 条。' % len(nofloor))
    for idx in sorted(nofloor):
        out.append('')
        out.extend(block(idx))
    out.append('')

    new = '\n'.join(out)
    print('章数 %d，条目块 %d，无楼层 %d，行数 %d → %d' %
          (51 + 1, sum(len(v) for v in by_floor.values()), len(nofloor),
           text.count('\n'), new.count('\n')))
    if '--write' in sys.argv:
        open(SRC, 'w', encoding='utf-8').write(new)
        print('已写回', SRC)
    else:
        open('/tmp/texts_by_floor_preview.md', 'w', encoding='utf-8').write(new)
        print('预览写入 /tmp/texts_by_floor_preview.md')


if __name__ == '__main__':
    main()
