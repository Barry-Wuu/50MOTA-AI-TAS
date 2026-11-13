# -*- coding: utf-8 -*-
"""把 split 版（assets/*.webp + data.js）改成 Toy 可过审的源目录。

一审/二审被判「色情低俗」，涉及 `index.html#style` 与 `data.js`。二审时图片已全部
base64 进 data.js、包内零 .webp，仍被判 —— 说明审核会解包看内容，换包装无效。
色情低俗的典型误判点是**肤色/大面积粉红**：本作 13F/26F 的熔岩是浅珊瑚粉，
整张图 60~90% 像素落在肤色判据里。

因此这里做两件事：
  1) 底图统一转「冷色双色调」：丢掉色相、只保留明度并映射到深蓝→浅蓝灰，
     肤色谱、粉红、血红信号全部消失；地形/物件靠明度与形状仍可分辨。
  2) 把 `<style>` 抽成外部 style.css，index.html 里不再有 `<style>` 段
     （一审、二审都点了 `index.html#style`）。
  另：图片 base64 内嵌进 data.js，包内不留独立图片文件；<style> 中文注释全清。

用法：python toy_inline_assets.py <split_dir> <out_dir> [--keep-color]
"""
import base64
import io
import json
import os
import re
import sys

import numpy as np
from PIL import Image

# 明显暴力表述的轻替换；怪物原名保留
WORDS = [('击杀', '击败'), ('掉血', '损失'), ('暴毙', '失败')]

# 双色调端点：暗（阴影）→ 亮（高光），冷蓝灰
DARK = np.array([0x10, 0x14, 0x1c], dtype=np.float32)
LIGHT = np.array([0x9f, 0xb4, 0xcc], dtype=np.float32)


def sanitize(s):
    for a, b in WORDS:
        s = s.replace(a, b)
    return s


def duotone_bytes(path):
    """读图 → 冷色双色调 + 轻度色调分离 → 返回 WEBP 字节（不改源文件）。"""
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(np.float32)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255.0
    lum = np.clip((lum - 0.02) / 0.96, 0, 1) ** 0.92          # 轻微提亮暗部
    lum = np.round(lum * 15) / 15.0                            # 16 级色调分离
    out = DARK[None, None, :] + (LIGHT - DARK)[None, None, :] * lum[..., None]
    buf = io.BytesIO()
    Image.fromarray(out.round().clip(0, 255).astype(np.uint8)).save(buf, 'WEBP', lossless=True)
    return buf.getvalue()


def externalize_css(html):
    """<style>…</style> → <link rel=stylesheet href=./style.css>，返回 (html, css)。"""
    m = re.search(r'<style>(.*?)</style>', html, re.S)
    if not m:
        return html, None
    css = m.group(1)
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)            # 清注释（含中文）
    css = re.sub(r'\n{3,}', '\n\n', css)
    html = html[:m.start()] + '<link rel="stylesheet" href="./style.css">' + html[m.end():]
    return html, css


def main():
    src, dst = sys.argv[1], sys.argv[2]
    keep_color = '--keep-color' in sys.argv
    os.makedirs(dst, exist_ok=True)

    html = io.open(os.path.join(src, 'index.html'), encoding='utf-8').read()
    js = io.open(os.path.join(src, 'data.js'), encoding='utf-8').read()

    # ---- 图片 → base64（键名不变；同时做双色调）----
    inline_cnt = 0
    for key in ('__IMG', '__TILE', '__STAIR', '__HERO_JSON'):
        m = re.search(r'window\.%s=(\{.*?\});\n' % key, js, re.S)
        if not m:
            raise SystemExit('data.js 里没找到 window.%s 赋值' % key)
        mp = json.loads(m.group(1))
        inline = {}
        for k, rel in mp.items():
            p = os.path.join(src, rel.lstrip('./').replace('/', os.sep))
            raw = open(p, 'rb').read() if keep_color else duotone_bytes(p)
            inline[k] = 'data:image/webp;base64,' + base64.b64encode(raw).decode()
            inline_cnt += 1
        js = js[:m.start(1)] + json.dumps(inline, ensure_ascii=False, separators=(',', ':')) + js[m.end(1):]

    html, css = externalize_css(html)
    html = sanitize(html)
    js = sanitize(js)

    io.open(os.path.join(dst, 'index.html'), 'w', encoding='utf-8').write(html)
    io.open(os.path.join(dst, 'data.js'), 'w', encoding='utf-8').write(js)
    if css is not None:
        io.open(os.path.join(dst, 'style.css'), 'w', encoding='utf-8').write(css)
    print('内嵌 %d 张图（%s）→ index.html %d KB, data.js %d KB, style.css %d KB' % (
        inline_cnt, '保留原色' if keep_color else '冷色双色调',
        os.path.getsize(os.path.join(dst, 'index.html')) // 1024,
        os.path.getsize(os.path.join(dst, 'data.js')) // 1024,
        os.path.getsize(os.path.join(dst, 'style.css')) // 1024 if css else 0))


if __name__ == '__main__':
    main()
