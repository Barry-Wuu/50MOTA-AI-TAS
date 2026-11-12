# -*- coding: utf-8 -*-
"""对比 manual 与 run_segs 的 1 区黄钥匙流水（只打印发生变化的那一步）。"""
import re, io

PAT = re.compile(r'钥(\d+)/(\d+)/(\d+)')


def flow(path, endline=None, skip=()):
    out = []
    last = None
    with io.open(path, encoding='utf-8-sig', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            if endline and i > endline:
                break
            m = PAT.search(line)
            if not m:
                continue
            k = tuple(int(v) for v in m.groups())
            if last is None or k != last:
                if not any(s in line for s in skip):
                    out.append((i, k, line.strip()))
                last = k
    return out


print('==== manual.py 黄钥匙流水 ====')
for i, k, line in flow(r'D:\B++\WorkBuddy\mota_tas_tmp2\repo\09_TAS推演\_manual.log'):
    print('%4d  %s' % (i, line[:130]))

print('\n==== run_segs 1 区黄钥匙流水（截至 11F 入口）====')
for i, k, line in flow(r'D:\B++\WorkBuddy\mota_tas_tmp2\repo\01_PC98原版_mtower\_run_segs_now.log', endline=777):
    print('%4d  %s' % (i, line[:130]))
