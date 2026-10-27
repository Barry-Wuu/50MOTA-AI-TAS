# -*- coding: utf-8 -*-
"""BOSS 门层渲染图标注：把「杀 BOSS 后才出现的上行梯」作为战利品画出来。

用户发现：BOSS 层渲染图画了半透明战利品，却漏掉最大的战利品——上行楼梯。
证据（mota_core 实测）：
  10F(6,11) 静态=地板，杀 obj16 后 eventMT 写入 22 号上行梯 → 11F(6,10)
  20F(6,1)  静态=地板(封印花纹)，杀 obj59 吸血鬼后 → 21F(6,2)（21F(6,1) 下梯落点 (20,6,2) 的同坐标配对）
  40F(6,1)  静态=地板，同构（41F(6,1) 下梯落点 (40,5,1) 为其邻格）
  49F(6,3)  静态=地板，杀 obj57 假魔王后 → 50F(6,5)（UP_PATCH）
"""
from PIL import Image, ImageDraw, ImageFont
import os

SRC = '/tmp/motarepo2/01_PC98原版_mtower/floors'
DST = '/workspace/魔塔_BOSS层_隐藏上行梯标注'
os.makedirs(DST, exist_ok=True)

FONT = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'

# (渲染图, 隐藏上梯格(x,y), 说明, 标签放上方还是下方)
TASKS = [
    ('floor_10.png', (6, 11), '杀10F BOSS后出现↑ → 11F(6,10)', 'below'),
    ('floor_20.png', (6, 1),  '杀吸血鬼后出现↑ → 21F(6,2)',    'below'),
    ('floor_40.png', (6, 1),  '杀40F BOSS后出现↑ → 41F',        'below'),
    ('floor_49.png', (6, 3),  '杀假魔王后出现↑ → 50F(6,5)',     'above'),
]

GOLD = (255, 200, 40)


def dashed_rect(d, x0, y0, x1, y1, color, width=4, dash=10):
    """画虚线矩形（四条边交替画短线）。"""
    def dashed_line(p0, p1):
        import math
        length = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        n = int(length // dash) + 1
        for i in range(0, n, 2):
            s = i / max(n - 1, 1)
            e = min((i + 1) / max(n - 1, 1), 1.0)
            a = (p0[0] + (p1[0] - p0[0]) * s, p0[1] + (p1[1] - p0[1]) * s)
            b = (p0[0] + (p1[0] - p0[0]) * e, p0[1] + (p1[1] - p0[1]) * e)
            d.line([a, b], fill=color, width=width)
    dashed_line((x0, y0), (x1, y0))
    dashed_line((x1, y0), (x1, y1))
    dashed_line((x1, y1), (x0, y1))
    dashed_line((x0, y1), (x0, y0))


for fname, (gx, gy), label, pos in TASKS:
    img = Image.open(os.path.join(SRC, fname)).convert('RGBA')
    W, H = img.size
    px, py = W / 13.0, H / 13.0          # 13×13 网格（0~12，含边框墙）
    x0, y0 = (gx - 1) * px, (gy - 1) * py
    x1, y1 = gx * px, gy * py

    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # 半透明金色底 + 虚线金框 + 上箭头
    d.rectangle([x0 + 2, y0 + 2, x1 - 2, y1 - 2], fill=(255, 200, 40, 70))
    dashed_rect(d, x0 + 2, y0 + 2, x1 - 2, y1 - 2, GOLD + (255,), width=4, dash=11)
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    a = 9
    d.line([(cx, cy - a), (cx, cy + a)], fill=GOLD + (255,), width=4)
    d.line([(cx - a * 0.7, cy), (cx, cy - a), (cx + a * 0.7, cy)], fill=GOLD + (255,), width=4, joint='curve')

    # 标签文字
    fs = max(15, int(px * 0.42))
    try:
        font = ImageFont.truetype(FONT, fs)
    except Exception:
        font = ImageFont.load_default()
    tw = d.textlength(label, font=font)
    th = fs + 6
    ty = y1 + 4 if pos == 'below' else y0 - th - 4
    if ty + th > H: ty = y0 - th - 4
    if ty < 0: ty = y1 + 4
    tx = min(max(cx - tw / 2, 2), W - tw - 2)
    d.rectangle([tx - 4, ty - 2, tx + tw + 4, ty + th], fill=(0, 0, 0, 190))
    d.text((tx, ty), label, font=font, fill=GOLD + (255,))

    out = Image.alpha_composite(img, ov).convert('RGB')
    dst = os.path.join(DST, fname.replace('.png', '_标注.png'))
    out.save(dst)
    print('✓', dst, '标记格 (%d,%d)' % (gx, gy))

print('完成')
