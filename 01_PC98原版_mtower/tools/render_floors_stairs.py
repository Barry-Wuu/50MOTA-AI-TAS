#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在渲染图上补「隐藏上梯（半透明战利品楼梯）」与「楼梯落点」。

两类产物：
  1) 单层图 floors/floor_01..50.png  —— 520×520，不含图例带
  2) 50 层全图 map_50f.png           —— 5 列×11 行整塔（0F 左上，1–50F 行优先）

绘制规则（按用户要求）：
  · 隐藏上梯**以半透明楼梯精灵**画出（C = (1-α)·底 + α·梯级前景，α≈0.55），
    而不是在角落打小方块。落点用绿圈+十字，不遮挡。
  · 隐藏上梯共 4 处 BOSS 层：10F(6,11)→11F、20F(6,1)→21F、30F(6,1)→31F、40F(6,1)→41F。
  · **49F 没有上行楼梯**（不画）；进入 50F 是从 **24F 上方 (6,0) 暗门**上行 → 50F(6,5)，
    故把 24F(6,0) 作为「上行至 50F」的半透明楼梯画出，50F 落点标 (6,5)。
  · 台阶/暗门一律不加左上角小方块。

幂等：单层底图取 18b96d4、全图底图取 18b96d4（均未画过隐藏上梯），可反复运行不累积。
数据源：mota_core.terrain()/stair_up()/warp_to()+WARP（二进制解出）。
"""
import io
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # 01_PC98原版_mtower/
REPO = ROOT.parent                      # 仓库根
sys.path.insert(0, str(HERE))
import mota_core as M                   # noqa: E402

BASE = '18b96d4'                        # 原始楼层底图（未画隐藏上梯），幂等基准
FLOORS_REL = '01_PC98原版_mtower/floors'
MAP50_REL = '01_PC98原版_mtower/map_50f.png'
ART = ROOT.parent / '08_Java_MTower08a' / 'art'
FONT_PATH = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'

CELL, N = 40, 13
MCELL, MGAP, MPAD = 520, 10, 10
ALPHA = 0.55

C_UP  = (208, 48, 48)
C_DN  = (36, 96, 200)
C_IN  = (24, 150, 88)
C_HID = (232, 138, 22)
C_FLY = (146, 84, 196)

# ---- 隐藏上梯（BOSS 层，杀 BOSS 后生成） ----
HIDDEN_UP = {
    10: ((6, 11), 11, (6, 10)),
    20: ((6, 1),  21, (6, 2)),
    30: ((6, 1),  31, (6, 2)),
    40: ((6, 1),  41, (5, 1)),
}
# ---- 24F 上方暗门 → 50F（ending warp，不是阶梯，但视觉上是“上行至 50F”） ----
SECRET_DOOR = {24: ((6, 0), 50, (6, 5))}
# 需要以半透明楼梯“补全”的格：4 个 BOSS 隐藏上梯 + 24F 顶部暗门
GHOST = {f: c for f, (c, _t, _l) in HIDDEN_UP.items()}
GHOST[24] = SECRET_DOOR[24][0]

FLY_IN = {0: (1, 2), 44: (1, 2)}

# ---- 半透明楼梯精灵（上行梯），前景蒙版按亮度提取 ----
_spr = Image.open(ART / 'stair_up.png').convert('RGB')
UP = np.asarray(_spr).astype(float)
_L = UP[..., 0] * 0.299 + UP[..., 1] * 0.587 + UP[..., 2] * 0.114
MASK = np.clip((_L - 100.0) / (175.0 - 100.0), 0.0, 1.0) * ALPHA

_fc = {}


def font(sz):
    sz = max(7, int(sz))
    if sz not in _fc:
        _fc[sz] = ImageFont.truetype(FONT_PATH, sz)
    return _fc[sz]


def build_arrive():
    arrive = defaultdict(list)
    for f in range(51):
        for y in range(N):
            for x in range(N):
                if M.terrain(f, x, y) != 2:
                    continue
                w = M.warp_to(f, x, y)
                if w:
                    arrive[w[0]].append((f, w[1], w[2]))
    for f, ((hx, hy), tf, (tx, ty)) in HIDDEN_UP.items():
        arrive[tf].append((f, tx, ty))
    for f, ((dx, dy), tf, (tx, ty)) in SECRET_DOOR.items():
        arrive[tf].append((f, tx, ty))
    arrive[0].append((1, 1, 2))
    arrive[44].append((45, 1, 2))
    return arrive


ARRIVE = build_arrive()


def ghost(arr, px, py):
    """把上行梯精灵以 α≈0.55 幽灵化叠加到 arr[py:py+40, px:px+40]。"""
    h, w = arr.shape[:2]
    if px < 0 or py < 0 or px + CELL > w or py + CELL > h:
        return
    cell = arr[py:py + CELL, px:px + CELL]
    arr[py:py + CELL, px:px + CELL] = cell * (1 - MASK[..., None]) + UP * MASK[..., None]


def draw_points(dr, ox, oy, fl):
    """只画落点绿圈 + 飞行紫钻；不在角落打任何小方块。"""
    skip = {(FLY_IN[fl][0], FLY_IN[fl][1])} if fl in FLY_IN else set()
    for (ff, x, y) in ARRIVE.get(fl, []):
        if (x, y) in skip:
            continue
        px, py = ox + x * CELL, oy + y * CELL
        pad = 6
        dr.ellipse([px + pad, py + pad, px + CELL - 1 - pad, py + CELL - 1 - pad],
                   outline=C_IN + (240,), width=3)
        cx, cy = px + CELL // 2, py + CELL // 2
        dr.line([cx - 6, cy, cx + 6, cy], fill=C_IN + (240,), width=2)
        dr.line([cx, cy - 6, cx, cy + 6], fill=C_IN + (240,), width=2)
    if fl in FLY_IN:
        fx, fy = FLY_IN[fl]
        px, py = ox + fx * CELL, oy + fy * CELL
        cx, cy, r = px + CELL // 2, py + CELL // 2, int(CELL * 0.34)
        dr.line([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy), (cx, cy - r)],
                fill=C_FLY + (255,), width=3)


def git_show(ref, rel):
    d = subprocess.run(['git', 'show', '%s:%s' % (ref, rel)], cwd=str(REPO),
                       capture_output=True)
    return d.stdout if d.returncode == 0 and d.stdout else None


def single_floor(fl):
    data = git_show(BASE, '%s/floor_%02d.png' % (FLOORS_REL, fl))
    if data:
        img = Image.open(io.BytesIO(data)).convert('RGB')
    else:
        img = Image.open(ROOT / 'floors' / ('floor_%02d.png' % fl)).convert('RGB')
    arr = np.asarray(img).astype(float)
    if fl in GHOST:
        hx, hy = GHOST[fl]
        ghost(arr, hx * CELL, hy * CELL)
    img = Image.fromarray(arr.round().clip(0, 255).astype('uint8'))
    draw_points(ImageDraw.Draw(img, 'RGBA'), 0, 0, fl)
    return img


def cell_origin(fl):
    if fl == 0:
        r, c = 0, 0
    else:
        r, c = 1 + (fl - 1) // 5, (fl - 1) % 5
    return MPAD + c * (MCELL + MGAP), MPAD + r * (MCELL + MGAP)


def render_map50():
    data = git_show(BASE, MAP50_REL)
    img = Image.open(io.BytesIO(data)).convert('RGB')
    arr = np.asarray(img).astype(float)
    for fl, (hx, hy) in GHOST.items():
        ox, oy = cell_origin(fl)
        ghost(arr, ox + hx * CELL, oy + hy * CELL)
    img = Image.fromarray(arr.round().clip(0, 255).astype('uint8'))
    dr = ImageDraw.Draw(img, 'RGBA')
    for fl in range(51):
        ox, oy = cell_origin(fl)
        draw_points(dr, ox, oy, fl)
    return img


def legend_image():
    lg = Image.new('RGB', (600, 118), (251, 250, 247))
    d = ImageDraw.Draw(lg)
    d.text((14, 8), '魔塔1 渲染图图例', font=font(17), fill=(28, 28, 38))
    # 半透明楼梯示意块
    yy = 38
    d.rectangle([16, yy, 52, yy + 36], fill=(150, 150, 158))
    d.text((60, yy + 2), '半透明楼梯 = 隐藏上梯（战利品楼梯）：', font=font(13), fill=(58, 58, 68))
    d.text((60, yy + 19), 'BOSS 层杀 BOSS 后出现（10/20/30/40F）；24F 顶部暗门→50F', font=font(12),
           fill=(120, 70, 20))
    yy2 = 84
    d.ellipse([18, yy2, 34, yy2 + 16], outline=C_IN, width=3)
    d.line([26 - 4, yy2 + 8, 26 + 4, yy2 + 8], fill=C_IN, width=2)
    d.line([26, yy2 + 4, 26, yy2 + 12], fill=C_IN, width=2)
    d.text((42, yy2 - 1), '绿圈+十字 = 楼梯落点（从下层上来落在本层坐标）', font=font(13),
           fill=(58, 58, 68))
    d.text((470, yy2 - 1), '紫钻 = 飞行落点(0F/44F)', font=font(12), fill=C_FLY)
    return lg


def main():
    out = ROOT / 'floors'
    out.mkdir(exist_ok=True)
    for fl in range(1, 51):
        single_floor(fl).save(out / ('floor_%02d.png' % fl))
    print('  floors/floor_01..50.png 已更新（520×520，半透明上梯+落点，无小方块）', flush=True)
    render_map50().save(ROOT / 'map_50f.png')
    print('  map_50f.png 已更新（整塔全图）', flush=True)
    legend_image().save(ROOT / 'floors_legend.png')
    print('  floors_legend.png 已更新', flush=True)


if __name__ == '__main__':
    main()
