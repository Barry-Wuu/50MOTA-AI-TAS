#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""walk_seq.py —— 回放 route_plan.csv 后，按命令行给出的目标序列依次走，打印每段账。

目标写法:
   "12"           走到 12F（踩楼梯即跨层，用谓词目标）
   "12(5,10)"     走到 12F 的 (5,10) 格子
   "@10F(11,4)"   同 "10(11,4)"

例:
  python3 walk_seq.py 12 "12(5,10)" "12(7,10)" 11 10 "10(11,4)" 11
"""
import sys
import state as S
import plan as P


def parse(g):
    g = g.strip().lstrip('@')
    if '(' in g:
        head, rest = g.split('(', 1)
        xy = rest.rstrip(')').split(',')
        return (int(head), int(xy[0]), int(xy[1]))
    return int(g)


def main():
    goals = [parse(a) for a in sys.argv[1:]]
    w = S.replay()
    print('起点  ' + P.st(w.hero))
    total = 0
    for g in goals:
        if isinstance(g, int):
            tag = '→ %dF' % g
            w2, path = P.walk(w, g, 600000)
        else:
            tag = '→ %dF(%d,%d)' % g
            w2, path = P.walk(w, g, 600000)
        if w2 is None:
            print('  ✗ %-18s 失败：%s   [%s]' % (tag, path, P.st(w.hero)))
            return
        h0, h1 = w.hero, w2.hero
        d = h1.hp - h0.hp
        note = ''
        if h1.atk != h0.atk:
            note += ' ATK%+d' % (h1.atk - h0.atk)
        if h1.dfn != h0.dfn:
            note += ' DEF%+d' % (h1.dfn - h0.dfn)
        dk = ''.join('%s%+d' % (k, h1.keys[k] - h0.keys[k]) for k in ('y', 'b', 'r')
                     if h1.keys[k] != h0.keys[k])
        print('  ✓ %-18s %-46s [%3d 步] HP%+d%s%s' % (tag, P.st(h1), len(path), d, note, dk))
        total += len(path)
        w = w2
    print('合计 %d 步；终态 %s' % (total, P.st(w.hero)))


if __name__ == '__main__':
    main()
