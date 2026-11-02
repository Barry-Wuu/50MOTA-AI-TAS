# -*- coding: utf-8 -*-
"""两版 objectAttribute 逐项对比：PC-98 live.json vs Java map_java8.json
验证「原始魔塔1 与 Java 魔塔8 数值一致」假设（用户 2026-11-02 指令）。
用法: python _cmp_oa.py
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 01_PC98原版_mtower
pc = json.load(open(os.path.join(R, 'tools', 'crops', 'live.json'), encoding='utf-8'))['objectAttribute']
jv = json.load(open(os.path.join(R, '..', '08_Java_MTower08a', 'game', 'map_java8.json'), encoding='utf-8'))['objectAttribute']

diffs = []
for r in range(200):
    if list(pc[r]) != list(jv[r]):
        diffs.append((r, list(pc[r]), list(jv[r])))
print(f"rows: PC={len(pc)} Java={len(jv)}  differing={len(diffs)}")
for r, p, j in diffs:
    print(f"obj{r}: PC={p}")
    print(f"      JAVA={j}")
# 重点核对 obj22 祭坛 + 怪物四维
print("\nobj22 altar PC:", list(pc[22]), "  a[10..13]=", pc[22][10:14])
print("obj22 altar JV:", list(jv[22]), "  a[10..13]=", jv[22][10:14])
# 全部 a[10..13] 一致性
mismatch_stats = [r for r in range(200) if list(pc[r][10:14]) != list(jv[r][10:14])]
print("rows with a[10..13] mismatch:", mismatch_stats)
# 全部 a[3] 类型一致性
mismatch_type = [r for r in range(200) if pc[r][3] != jv[r][3]]
print("rows with a[3](type) mismatch:", mismatch_type)
