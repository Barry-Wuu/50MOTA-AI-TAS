# -*- coding: utf-8 -*-
"""分段运行：跑累计前缀，打印每层出口状态"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import exec_route as E
import route_1_10 as R


def st(h):
    return E.st(h)


SEGS = [
    ('A(1-3扒装前)', R.PLAN_A),
    ('B1(2F收尾)', R.PLAN_B1),
    ('B2(1F蓝药)', R.PLAN_B2),
    ('B3(3F钥匙组)', R.PLAN_B3),
    ('C4(4F)', R.PLAN_C4),
    ('C5(5F铁剑)', R.PLAN_C5),
    ('C6(6F)', R.PLAN_C6),
    ('C7(7F)', R.PLAN_C7),
    ('C8(8F)', R.PLAN_C8),
]


def main(upto=None):
    acc = []
    for name, seg in SEGS:
        acc = acc + seg
        try:
            w, log = E.run(acc, verbose=False)
        except Exception as ex:
            print('!! %s 失败: %s' % (name, ex))
            return
        print('%-14s -> %s' % (name, st(w.hero)))
        if upto and name.startswith(upto):
            break


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
