# -*- coding: utf-8 -*-
"""v9 补丁：把 steps*.js 步进日志里的日文（obj 名引用）也换成中文标准译文。

steps 日志形如 `击败 obj48 ゾンビ 损失0 +金18`——日文来自 mota_core.oname()
返回的原文。按 csv 对照表把出现的日文片段替换为中文（前缀/子串匹配）。
"""
import csv
import glob
import io
import os
import re
import sys

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '01_PC98原版_mtower', 'magic_tower1_texts.csv')

rows = list(csv.DictReader(io.open(CSV_PATH, encoding='utf-8-sig')))
jp2zh = {r['text_jp']: r['text_zh'] for r in rows if r['text_jp'] and r['text_zh']}
# 按长度降序替换，避免短名先替换破坏长名匹配
pairs = sorted(jp2zh.items(), key=lambda kv: -len(kv[0]))


def main():
    d = sys.argv[1]
    for fn in sorted(glob.glob(os.path.join(d, 'steps*.js'))):
        s = io.open(fn, encoding='utf-8').read()
        n0 = 0
        for jp, zh in pairs:
            if jp in s:
                n0 += s.count(jp)
                s = s.replace(jp, zh)
        io.open(fn, 'w', encoding='utf-8').write(s)
        kana = len(re.findall(r'[\u3040-\u30ff\uff66-\uff9f]', s))
        print('%s: 替换 %d 处，残留假名 %d' % (os.path.basename(fn), n0, kana))


if __name__ == '__main__':
    main()
