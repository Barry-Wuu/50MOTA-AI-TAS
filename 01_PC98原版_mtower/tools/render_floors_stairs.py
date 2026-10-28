#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「战利品楼梯（隐藏上梯）」与「楼梯落点」叠进两层渲染图：

  1) 单层图  floors/floor_01..50.png  —— 保持 520×520 原尺寸，不画图例带（图例见说明图）
  2) 50 层全图 map_50f.png            —— 5 列×11 行整塔拼图（0F 在左上，1–50F 顺排），
                                         每格叠加同一套标记，并在左上角标层号便于定位

标记（不写进像素图例，只在 floors_legend.png 说明）：
  绿圈+十字 = 落点（从下层上来落在本层坐标）
  红/蓝角标 = 上/下梯踏步格
  橙角标   = 隐藏上梯（战利品楼梯，杀 BOSS/事件后生成）
  绿角标   = 24F 暗门 → 50F
  紫钻     = 飞行之珠 / 幻之阶落点

幂等：单层图取 2efaf1f 底图、全图取 18b96d4 底图重算，可反复运行不累积。
数据源：mota_core.terrain()/stair_up()/warp_to()+WARP（二进制解出）。
"""
import io
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

BASE_FLOORS = '2efaf1f'                 # 单层底图（隐藏上梯已画入），幂等
BASE_MAP50 = '18b96d4'                  # 50 层整塔底图，幂等
FLOORS_REL = '01_PC98原版_mtower/floors'
MAP50_REL = '01_PC98原版_mtower/map_50f.png'
FONT_PATH = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'

CELL, N = 40, 13                        # 单层 520×520
# 50 层全图几何：cell 520，间距 10，左上留 10
MCELL, MGAP, MPAD = 520, 10, 10

C_UP  = (208, 48, 48)
C_DN  = (36, 96, 200)
C_IN  = (24, 150, 88)
C_HID = (232, 138, 22)
C_FLY = (146, 84, 196)

HIDDEN_UP = {
    10: ((6, 11), 11, (6, 10)),
    20: ((6, 1),  21, (6, 2)),
    30: ((6, 1),  31, (6, 2)),
    40: ((6, 1),  41, (5, 1)),
    49: ((6, 3),  50, (6, 5)),
}
SECRET_DOOR = {24: ((6, 0), 50, (6, 5))}
FLY_IN = {0: (1, 2, '1F 楼梯旁·飞行之珠下来'), 44: (1, 2, '幻之阶·只能飞行道具进入')}

_fc = {}


def font(sz):
    sz = max(7, int(sz))
    if sz not in _fc:
        _fc[sz] = ImageFont.truetype(FONT_PATH, sz)
    return _fc[sz]


def build_tables():
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


def diamond(dr, cx, cy, r, color, width=2):
    dr.line([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy), (cx, cy - r)],
            fill=color, width=width)


def draw_marks(dr, ox, oy, fl):
    """在 (ox,oy) 为左上原点的该层上叠加 stairs/落点/隐藏上梯/暗门/飞行标记。"""
    skip = {(FLY_IN[fl][0], FLY_IN[fl][1])} if fl in FLY_IN else set()

    # 落点：绿圈+十字
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

    # 上/下梯踏步格：左上角实心方块
    for (x, y, kind, tf, tx, ty) in STAIRS.get(fl, []):
        px, py = ox + x * CELL, oy + y * CELL
        col = C_UP if kind == 'UP' else C_DN
        dr.rectangle([px + 2, py + 2, px + 13, py + 13], fill=col + (255,),
                     outline=(255, 255, 255, 255))

    # 隐藏上梯（战利品楼梯）：橙角标 + 右上小三角
    if fl in HIDDEN_UP:
        (hx, hy), tf, (tx, ty) = HIDDEN_UP[fl]
        px, py = ox + hx * CELL, oy + hy * CELL
        dr.rectangle([px + 2, py + 2, px + 13, py + 13], fill=C_HID + (255,),
                     outline=(255, 255, 255, 255))
        dr.polygon([(px + CELL - 12, py + 4), (px + CELL - 4, py + 4), (px + CELL - 8, py + 12)],
                   fill=C_HID + (255,))

    # 24F 暗门
    if fl in SECRET_DOOR:
        (dx, dy), tf, (tx, ty) = SECRET_DOOR[fl]
        px, py = ox + dx * CELL, oy + dy * CELL
        dr.rectangle([px + 2, py + 2, px + 13, py + 13], fill=C_IN + (255,),
                     outline=(255, 255, 255, 255))

    # 飞行落点：紫钻
    if fl in FLY_IN:
        fx, fy, _ = FLY_IN[fl]
        px, py = ox + fx * CELL, oy + fy * CELL
        diamond(dr, px + CELL // 2, py + CELL // 2, int(CELL * 0.34), C_FLY + (255,), 3)


def git_show(ref, rel):
    d = subprocess.run(['git', 'show', '%s:%s' % (ref, rel)], cwd=str(REPO),
                       capture_output=True)
    return d.stdout if d.returncode == 0 and d.stdout else None


def single_floor(fl):
    """单层图：520×520，仅叠加标记，不画图例带。"""
    data = git_show(BASE_FLOORS, '%s/floor_%02d.png' % (FLOORS_REL, fl))
    if data:
        img = Image.open(io.BytesIO(data)).convert('RGB')
    else:
        img = Image.open(ROOT / 'floors' / ('floor_%02d.png' % fl)).convert('RGB')
    dr = ImageDraw.Draw(img, 'RGBA')
    draw_marks(dr, 0, 0, fl)
    return img


def cell_origin(fl):
    """层号 → 整塔全图该格左上角像素。0F 在 (r0,c0)；1–50F 从 r1 起行优先。"""
    if fl == 0:
        r, c = 0, 0
    else:
        r, c = 1 + (fl - 1) // 5, (fl - 1) % 5
    return MPAD + c * (MCELL + MGAP), MPAD + r * (MCELL + MGAP)


def render_map50():
    data = git_show(BASE_MAP50, MAP50_REL)
    img = Image.open(io.BytesIO(data)).convert('RGB')
    dr = ImageDraw.Draw(img, 'RGBA')
    for fl in range(51):
        ox, oy = cell_origin(fl)
        draw_marks(dr, ox, oy, fl)
    # 底图每格左上角已自带层号，无需重复标注
    return img


def legend_image():
    lg = Image.new('RGB', (600, 128), (251, 250, 247))
    d = ImageDraw.Draw(lg)
    d.text((14, 8), '魔塔1 渲染图图例（楼梯落点 / 战利品楼梯）', font=font(17), fill=(28, 28, 38))
    items = [
        (C_UP,  '红角标 = 上行梯踏步格（踩它上楼）'),
        (C_DN,  '蓝角标 = 下行梯踏步格（踩它下楼）'),
        (C_IN,  '绿圈+十字 = 落点（从下层上来落在本层坐标）'),
        (C_HID, '橙角标 = 隐藏上梯（战利品楼梯，杀 BOSS/事件后生成）'),
        (C_FLY, '紫钻 = 飞行之珠 / 幻之阶落点（0F、44F）'),
    ]
    for i, (col, lab) in enumerate(items):
        yy = 40 + i * 16
        d.ellipse([16, yy, 28, yy + 12], fill=col)
        d.text((36, yy - 2), lab, font=font(13), fill=(58, 58, 68))
    return lg


def main():
    out = ROOT / 'floors'
    out.mkdir(exist_ok=True)
    for fl in range(1, 51):
        single_floor(fl).save(out / ('floor_%02d.png' % fl))
    print('  floors/floor_01..50.png 已更新（520×520，无图例带）', flush=True)
    render_map50().save(ROOT / 'map_50f.png')
    print('  map_50f.png 已叠加楼梯落点+隐藏上梯+层号', flush=True)
    legend_image().save(ROOT / 'floors_legend.png')
    print('  floors_legend.png（说明用）已更新', flush=True)


if __name__ == '__main__':
    main()
