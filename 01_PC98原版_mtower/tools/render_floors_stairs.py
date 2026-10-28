#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「战利品楼梯（隐藏上梯）」与「楼梯落点」直接叠进主渲染图 floors/floor_XX.png。

底图取自提交 2efaf1f —— 该提交已把 BOSS/事件层的隐藏上行梯按战利品画法（α≈0.55 幽灵化）
画入楼层图。本脚本在其上再叠加：
  · 楼梯落点（绿圈 + 十字）—— 从下层上来，落在本层的坐标
  · 上行梯踏步格（红角标）/ 下行梯踏步格（蓝角标）
  · 隐藏上梯「战利品楼梯」橙标（与底图幽灵楼梯位置对应，做图例指认）
并在图下方扩展一条图例带，写明本层上下梯与落点。

特性：每次从固定底图 BASE_COMMIT 重算，可反复运行而不累积叠画（幂等）。
数据源：mota_core.terrain()/stair_up()/warp_to() + WARP（全部由 PC-98 二进制解出）
        + HIDDEN_UP / SECRET_DOOR / FLY_IN（引擎 UP_PATCH / eventMT / 飞行道具配对）。
"""
import io
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # 01_PC98原版_mtower/
REPO = ROOT.parent                      # 仓库根
sys.path.insert(0, str(HERE))
import mota_core as M                   # noqa: E402

BASE_COMMIT = '2efaf1f'                 # 隐藏上梯已画入的版本，作为幂等底图
FLOORS_REL = '01_PC98原版_mtower/floors'
FONT_PATH = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'

CELL, N = 40, 13                        # 520×520，cell(x,y) 像素 = (x*40, y*40)
LEGEND_H = 86

C_UP   = (208, 48, 48)
C_DN   = (36, 96, 200)
C_IN   = (24, 150, 88)
C_HID  = (232, 138, 22)
C_FLY  = (146, 84, 196)
C_TXT  = (58, 58, 68)
C_BG   = (251, 250, 247)

# 隐藏上梯：杀 BOSS/事件后生成 (层, 踏步格, 目标层, 落点)
HIDDEN_UP = {
    10: ((6, 11), 11, (6, 10)),
    20: ((6, 1),  21, (6, 2)),
    30: ((6, 1),  31, (6, 2)),
    40: ((6, 1),  41, (5, 1)),
    49: ((6, 3),  50, (6, 5)),
}
SECRET_DOOR = {24: ((6, 0), 50, (6, 5))}
# 飞行之珠/幻之阶落点：0F 由 1F 楼梯旁飞来；44F 只能飞行道具进
FLY_IN = {0: (1, 2, '1F 楼梯旁·飞行之珠下来'), 44: (1, 2, '幻之阶·只能飞行道具进入')}

_fc = {}


def font(sz):
    sz = max(7, int(sz))
    if sz not in _fc:
        _fc[sz] = ImageFont.truetype(FONT_PATH, sz)
    return _fc[sz]


def build_tables():
    """stairs[f]=[(x,y,'UP'/'DN',tf,tx,ty)]；arrive[f]=[(from_floor,x,y)]"""
    stairs = {f: [] for f in range(51)}
    arrive = defaultdict(list)
    for f in range(51):
        for y in range(N):
            for x in range(N):
                if M.terrain(f, x, y) != 2:
                    continue
                up = M.stair_up(f, x, y)
                w = M.warp_to(f, x, y)
                if w:
                    stairs[f].append((x, y, 'UP' if up else 'DN', w[0], w[1], w[2]))
                    arrive[w[0]].append((f, w[1], w[2]))
                else:
                    stairs[f].append((x, y, 'UP' if up else 'DN', None, None, None))
    for f, ((hx, hy), tf, (tx, ty)) in HIDDEN_UP.items():
        arrive[tf].append((f, tx, ty))
    arrive[50].append((24, 6, 5))
    arrive[0].append((1, 1, 2))
    arrive[44].append((45, 1, 2))
    return stairs, arrive


STAIRS, ARRIVE = build_tables()


def base_image(fl):
    """从 BASE_COMMIT 取该层底图（含战利品与幽灵隐藏上梯），保证幂等。"""
    rel = '%s/floor_%02d.png' % (FLOORS_REL, fl)
    data = subprocess.run(['git', 'show', '%s:%s' % (BASE_COMMIT, rel)],
                          cwd=str(REPO), capture_output=True)
    if data.returncode != 0 or not data.stdout:
        # 回退：读工作区当前文件
        return Image.open(ROOT / 'floors' / ('floor_%02d.png' % fl)).convert('RGB')
    return Image.open(io.BytesIO(data.stdout)).convert('RGB')


def annotate(fl):
    img = base_image(fl)
    W0, H0 = img.size
    canvas = Image.new('RGB', (W0, H0 + LEGEND_H), C_BG)
    canvas.paste(img, (0, 0))
    dr = ImageDraw.Draw(canvas, 'RGBA')

    # 1) 楼梯落点：绿圈 + 十字
    for (ff, x, y) in ARRIVE.get(fl, []):
        px, py = x * CELL, y * CELL
        pad = 6
        dr.ellipse([px + pad, py + pad, px + CELL - 1 - pad, py + CELL - 1 - pad],
                   outline=C_IN + (235,), width=3)
        cx, cy = px + CELL // 2, py + CELL // 2
        dr.line([cx - 6, cy, cx + 6, cy], fill=C_IN + (235,), width=2)
        dr.line([cx, cy - 6, cx, cy + 6], fill=C_IN + (235,), width=2)

    # 2) 上/下梯踏步格：左上角实心小方块
    for (x, y, kind, tf, tx, ty) in STAIRS.get(fl, []):
        px, py = x * CELL, y * CELL
        col = C_UP if kind == 'UP' else C_DN
        dr.rectangle([px + 2, py + 2, px + 13, py + 13], fill=col + (255,),
                     outline=(255, 255, 255, 255))

    # 3) 隐藏上梯「战利品楼梯」：左上角橙标 + 小三角
    if fl in HIDDEN_UP:
        (hx, hy), tf, (tx, ty) = HIDDEN_UP[fl]
        px, py = hx * CELL, hy * CELL
        dr.rectangle([px + 2, py + 2, px + 13, py + 13], fill=C_HID + (255,),
                     outline=(255, 255, 255, 255))
        dr.polygon([(px + CELL - 12, py + 4), (px + CELL - 4, py + 4), (px + CELL - 8, py + 12)],
                   fill=C_HID + (255,))
    if fl in SECRET_DOOR:
        (dx, dy), tf, (tx, ty) = SECRET_DOOR[fl]
        px, py = dx * CELL, dy * CELL
        dr.rectangle([px + 2, py + 2, px + 13, py + 13], fill=C_IN + (255,),
                     outline=(255, 255, 255, 255))

    # 4) 底部图例带
    ly = H0 + 6
    fn_s = font(11)
    # 第一行：色块图例（短标签，避免超宽）
    items = [(C_UP, '上行梯'), (C_DN, '下行梯'), (C_IN, '落点'),
             (C_HID, '隐藏上梯(战利品楼梯)')]
    if fl in FLY_IN:
        items.append((C_FLY, '飞行落点'))
    x = 12
    for col, lab in items:
        dr.ellipse([x, ly + 3, x + 10, ly + 13], fill=col)
        dr.text((x + 14, ly + 1), lab, font=fn_s, fill=C_TXT)
        x += 14 + int(dr.textlength(lab, font=fn_s)) + 16

    # 第二行：本层楼梯/隐藏上梯/暗门 坐标→目标
    rows = []
    for (sx, sy, kind, tf, tx, ty) in STAIRS.get(fl, []):
        if tf is None:
            continue
        tag = '上' if kind == 'UP' else '下'
        rows.append(('%s(%d,%d)→%dF(%d,%d)' % (tag, sx, sy, tf, tx, ty),
                     C_UP if kind == 'UP' else C_DN))
    if fl in HIDDEN_UP:
        (hx, hy), tf, (tx, ty) = HIDDEN_UP[fl]
        rows.append(('隐藏上(%d,%d)→%dF(%d,%d)' % (hx, hy, tf, tx, ty), C_HID))
    if fl in SECRET_DOOR:
        (dx, dy), tf, (tx, ty) = SECRET_DOOR[fl]
        rows.append(('暗门(%d,%d)→%dF(%d,%d)' % (dx, dy, tf, tx, ty), C_IN))
    yy = ly + 20
    xx = 12
    for txt, col in rows:
        piece = txt + '  '
        wpx = int(dr.textlength(piece, font=fn_s))
        if xx + wpx > W0 - 12:
            break
        dr.text((xx, yy), piece, font=fn_s, fill=col)
        xx += wpx
    # 第三行：落点列表
    ar = ARRIVE.get(fl, [])
    if ar:
        s = '落点：' + '、'.join('%dF→(%d,%d)' % a for a in ar[:4])
        if len(ar) > 4:
            s += ' 等%d处' % len(ar)
        while dr.textlength(s, font=fn_s) > W0 - 24 and len(s) > 6:
            s = s[:-2]
        dr.text((12, yy + 20), s, font=fn_s, fill=C_IN)
    return canvas


def main():
    out_dir = ROOT / 'floors'
    out_dir.mkdir(exist_ok=True)
    for fl in range(1, 51):                 # 渲染库存为 floor_01..floor_50（无 0F）
        annotate(fl).save(out_dir / ('floor_%02d.png' % fl))
        print('  叠加落点 %dF' % fl, flush=True)
    # 单独一张图例
    lg = Image.new('RGB', (560, 96), C_BG)
    d = ImageDraw.Draw(lg)
    d.text((12, 8), '魔塔1 渲染图图例', font=font(17), fill=(28, 28, 38))
    items = [(C_UP, '上行梯踏步格(红角标)'), (C_DN, '下行梯踏步格(蓝角标)'),
             (C_IN, '楼梯落点(绿圈+十字)'), (C_HID, '战利品楼梯=隐藏上梯(橙标)'),
             (C_FLY, '飞行之珠/幻之阶落点(紫)')]
    for i, (col, lab) in enumerate(items):
        yy = 40 + i * 11
        d.ellipse([14, yy, 24, yy + 10], fill=col)
        d.text((30, yy - 2), lab, font=font(12), fill=C_TXT)
    lg.save(ROOT / 'floors_legend.png')
    print('done: floors/*.png + floors_legend.png')


if __name__ == '__main__':
    main()
