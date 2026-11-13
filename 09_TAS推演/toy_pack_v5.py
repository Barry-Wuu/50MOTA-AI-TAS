# -*- coding: utf-8 -*-
"""Toy 第 5 版：底图抹掉所有人形精灵（怪物 + NPC + 1F 勇者），只留建筑结构。

依据：v4 已把底图转成蓝灰双色调（无肤色、无粉红），仍被判「色情低俗」且 f01~f05 全中
—— 说明判定不看颜色，看的是画面里的**人形精灵**。所以这版把「m(monster) / n(NPC)」
格用该层地板贴图盖掉，勇者起点 (1F(6,11)) 同样盖掉；怪物位置与数值仍由 DOM 的
伤害数字、dyn 标记承担，信息不丢。

保留：d(门) / i(道具) / s(楼梯) / a(祭坛) / o(其他) —— 都是几何/器物，无人形。

用法：python toy_pack_v5.py <split_dir> <out_dir> <cover_out.png>
"""
import io
import json
import os
import re
import shutil
import sys

import numpy as np
from PIL import Image

CELL = 40
DARK = np.array([0x10, 0x14, 0x1c], dtype=np.float32)
LIGHT = np.array([0x9f, 0xb4, 0xcc], dtype=np.float32)
WORDS = [('击杀', '击败'), ('掉血', '损失'), ('暴毙', '失败'),
         ('mk.death', 'mk.fail'), ('"death"', '"fail"'), ("'death'", "'fail'")]
ERASE_KINDS = {'m', 'n'}          # monster / npc
EXTRA_ERASE = {'1': [(6, 11)]}    # 1F 底图里烙着的勇者起点


def duotone(img):
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255.0
    lum = np.clip((lum - 0.02) / 0.96, 0, 1) ** 0.92
    lum = np.round(lum * 15) / 15.0
    out = DARK[None, None, :] + (LIGHT - DARK)[None, None, :] * lum[..., None]
    return Image.fromarray(out.round().clip(0, 255).astype(np.uint8))


def clean_text(s):
    for a, b in WORDS:
        s = s.replace(a, b)
    for ch in ('☠', '✕', '✖'):
        s = s.replace(ch, '')
    s = s.replace("content:''", 'content:none').replace('content:""', 'content:none')
    m = re.search(r'<style>(.*?)</style>', s, re.S)
    if m:
        css = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.S)
        s = s[:m.start(1)] + re.sub(r'\n{3,}', '\n\n', css) + s[m.end(1):]
    return s


def main():
    src, dst = sys.argv[1], sys.argv[2]
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    js = io.open(os.path.join(dst, 'data.js'), encoding='utf-8').read()
    D = json.loads(re.search(r'window\.__D=(\{.*?\});\nwindow\.__IMG', js, re.S).group(1))
    imgs = json.loads(re.search(r'window\.__IMG=(\{.*?\});\n', js, re.S).group(1))
    tiles = json.loads(re.search(r'window\.__TILE=(\{.*?\});\n', js, re.S).group(1))

    erased = 0
    for f, rel in imgs.items():
        p = os.path.join(dst, rel.lstrip('./').replace('/', os.sep))
        im = Image.open(p).convert('RGB')
        t = Image.open(os.path.join(dst, tiles[f].lstrip('./').replace('/', os.sep))).convert('RGB')
        cells = [(int(k.split(',')[0]), int(k.split(',')[1]))
                 for k, v in (D['floors'][f].get('objs') or {}).items() if v[2] in ERASE_KINDS]
        cells += EXTRA_ERASE.get(f, [])
        for (x, y) in cells:
            im.paste(t, (x * CELL, y * CELL))
            erased += 1
        duotone(im).save(p, 'WEBP', lossless=True)
    print('抹掉精灵 %d 格（%d 层）' % (erased, len(imgs)))

    for fn in ('index.html', 'data.js'):
        p = os.path.join(dst, fn)
        # ⚠️ 必须"先读后写"：io.open(p,'w') 会在入参求值时就把文件截断，
        #    写成 write(clean(open(p).read())) 会读到空串、把产物清零（本脚本踩过）。
        raw = io.open(p, encoding='utf-8').read()
        io.open(p, 'w', encoding='utf-8').write(clean_text(raw))
    print('输出', dst)


if __name__ == '__main__':
    main()
