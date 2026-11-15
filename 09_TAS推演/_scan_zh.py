# -*- coding: utf-8 -*-
"""扫 Toy 包里的非简体字（繁体 / 日文汉字 / 假名）。

判据：
  · t2s(片段) != 片段  → 含繁体字
  · 含平假名/片假名    → 未翻译的日文
  · 含 jp2t 能转的日文新字体（壊/薬/鍵…） → 日文汉字
输出每个字所在的最小上下文字符串 + 出现次数。
"""
import json
import os
import re
import collections

import opencc

HERE = os.path.dirname(os.path.abspath(__file__))
T2S = opencc.OpenCC('t2s')
try:
    JP2T = opencc.OpenCC('jp2t')
except Exception:
    JP2T = None

FILES = ['toy_final/data.js', 'toy_final/steps1.js', 'toy_final/steps2.js',
         'toy_final/steps3.js', 'toy_final/index.html']

CJK = re.compile(r'[\u3000-\u303f\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]+')
KANA = re.compile(r'[\u3040-\u309f\u30a0-\u30ff]')

bad = collections.Counter()      # 字符串 -> 次数
badchar = collections.Counter()  # 单字 -> 次数

for fn in FILES:
    p = os.path.join(HERE, fn)
    if not os.path.exists(p):
        continue
    txt = open(p, encoding='utf-8', errors='ignore').read()
    # 去掉 base64 图片块，避免误判
    txt = re.sub(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', '', txt)
    for m in CJK.finditer(txt):
        seg = m.group(0)
        if not seg.strip():
            continue
        flags = []
        if KANA.search(seg):
            flags.append('假名')
        s2 = T2S.convert(seg)
        if s2 != seg:
            flags.append('繁体')
        if JP2T is not None:
            j2 = JP2T.convert(seg)
            if j2 != seg and '繁体' not in flags:
                flags.append('日文新字体')
        if flags:
            bad[(seg, ','.join(flags))] += 1
            for ch in seg:
                if KANA.match(ch) or T2S.convert(ch) != ch or (JP2T and JP2T.convert(ch) != ch):
                    badchar[ch] += 1

print('=== 含非简体字的字符串 %d 条 ===' % len(bad))
for (seg, flags), n in bad.most_common(60):
    print('  [%s] x%-3d %s' % (flags, n, seg[:70]))
print()
print('=== 涉及的单字（字: 次数）===')
print(' '.join('%s:%d' % (c, n) for c, n in badchar.most_common(80)))
