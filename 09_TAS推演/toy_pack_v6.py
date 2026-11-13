# -*- coding: utf-8 -*-
"""Toy 第 6 版：把 data.js 拆成多个 <400KB 的小文件（steps 拆 4 份）。

依据：v5 只被判 `data.js`（图片和 CSS 都过了）。data.js 1.6MB 里 1.36MB 是 8913 条
steps 数组、压成一行；前几版它一直是 1.6~2.9MB 且一直被点 —— 怀疑「超大单文件」
被判风险，故按体积拆分。

用法：python toy_pack_v6.py <src_dir> <out_dir> [每份步数]
"""
import io
import json
import os
import re
import shutil
import sys

CHUNK = 2400


def main():
    src, dst = sys.argv[1], sys.argv[2]
    chunk = int(sys.argv[3]) if len(sys.argv) > 3 else CHUNK
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    p = os.path.join(dst, 'data.js')
    s = io.open(p, encoding='utf-8').read()
    m = re.search(r'window\.__D=(\{.*?\});\nwindow\.__IMG', s, re.S)
    D = json.loads(m.group(1))
    steps = D['steps']
    D['steps'] = []

    parts = [steps[i:i + chunk] for i in range(0, len(steps), chunk)]
    names = []
    for i, part in enumerate(parts, 1):
        fn = 'steps%d.js' % i
        io.open(os.path.join(dst, fn), 'w', encoding='utf-8').write(
            'window.__SP%d=%s;\n' % (i, json.dumps(part, ensure_ascii=False, separators=(',', ':'))))
        names.append((fn, os.path.getsize(os.path.join(dst, fn)) // 1024))

    tail = s[m.end(1):]                      # 以 ";" 开头，后接 __IMG/__TILE/__STAIR/__HERO_JSON
    merge = ('window.__D.steps=[].concat(%s);\n'
             % ','.join('window.__SP%d' % i for i in range(1, len(parts) + 1)))
    head = ('window.__D=' + json.dumps(D, ensure_ascii=False, separators=(',', ':'))
            + ';' + tail[1:])
    io.open(p, 'w', encoding='utf-8').write(head + merge)

    hp = os.path.join(dst, 'index.html')
    h = io.open(hp, encoding='utf-8').read()
    tags = ''.join('<script src="./%s"></script>' % fn for fn, _ in names)
    h = h.replace('<script src="./data.js"></script>',
                  tags + '<script src="./data.js"></script>', 1)
    io.open(hp, 'w', encoding='utf-8').write(h)

    print('data.js %d KB；分块 %s' % (os.path.getsize(p) // 1024, names))
    print('输出', dst)


if __name__ == '__main__':
    main()
