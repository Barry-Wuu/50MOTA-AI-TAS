#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trace.py —— 回放 CSV 后按目标序列走，打印每一步的 log。"""
import sys
import mota_core as M
import plan as P
from state import replay, parse_goal


def main():
    upto = None
    args = sys.argv[1:]
    if args and args[0] == '--at':
        upto = int(args[1]); args = args[2:]
    w = replay(upto=upto)
    print('起点 ' + P.st(w.hero))
    for a in args:
        tgt = parse_goal(a)
        w2, path = P.walk(w, tgt, 600000)
        if w2 is None:
            print('  ✗ %s -> %s [%s]' % (a, path, P.st(w.hero)))
            return
        cur = w
        print('  ── 目标 %s ──' % a)
        for (dx, dy, lab, lg) in path:
            cur = cur.clone()
            l2 = cur.move(dx, dy)
            h = cur.hero
            print('     %2d,%2d  %s' % (h.x, h.y, ' '.join(l2)))
        w = w2
        print('  ✓ %s → %s [%d 步]' % (a, P.st(w.hero), len(path)))


main()
