#!/usr/bin/env python3
"""把 BOSS/事件层"击杀后才出现"的隐藏上行梯，按战利品画法（半透明幽灵）
直接画进 01_PC98原版_mtower/floors/floor_XX.png。

美术来源：08_Java_MTower08a/game/image/MTower.gif（魔塔08 主精灵表，40×40 原生贴图）。
  - 上行梯 sprite @ (280,160)-(320,200)   —— 由 11F(11,11) 静态上梯格 dist=0.00 实证
  - 下行梯 sprite @ (320,160)-(360,200)   —— 由 12F(11,11)/20F(6,11) 下梯格 dist=0.00 实证

隐藏上梯清单（引擎 WARP/UP_PATCH 配对 + eventMT 实证）：
  10F(6,11)  杀 10F BOSS 后 → 11F(6,10)     [mota_core move() boss10 分支]
  20F(6,1)   杀吸血鬼后     → 21F(6,2)      [mota_core move() boss20 分支]
  30F(6,1)   eventMT to:[70] → 31F(6,2)     [JSON dynamic_terrain]
  40F(6,1)   杀 40F BOSS 后 → 41F           [41F(6,1) 下梯落 40F(5,1) 配对]
  49F(6,3)   杀假魔王(obj57)后 → 50F(6,5)   [UP_PATCH]

战利品画法实测（20F(5,8) 青回复药，residual=0.25/255）：
  C = 0.55·S + 0.45·F   —— 整块 40×40 精灵以 α≈0.55 叠加在地板上。
楼梯精灵底图是楼梯井格纹（非地板），故先按亮度提取梯级前景，再以同 α 幽灵化叠加，
保持底格地板/原内容不被格纹污染。
"""
import numpy as np
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # 01_PC98原版_mtower/
ART_DIR = ROOT.parent / '08_Java_MTower08a' / 'art'
SHEET = ART_DIR.parent / 'game' / 'image' / 'MTower.gif'

ALPHA = 0.55                 # 战利品实测透明度
STAIR_UP_XY = (280, 160)     # 上行梯 40×40 精灵左上角
CELL = 40

# 隐藏上梯出现处 (floor, x, y) —— 与 mota_core 的 boss10/boss20/UP_PATCH/eventMT 一致
TARGETS = [(10, 6, 11), (20, 6, 1), (30, 6, 1), (40, 6, 1), (49, 6, 3)]


def luminance(a):
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114


def main():
    ART_DIR.mkdir(exist_ok=True)

    # 1) 提取贴图入库（魔塔08 → 仓库 art/）
    sheet_img = Image.open(SHEET).convert('RGBA')
    sheet_img.save(ART_DIR / 'MTower_sheet.png')
    sx, sy = STAIR_UP_XY
    up = np.asarray(sheet_img.convert('RGB'))[sy:sy + CELL, sx:sx + CELL]
    Image.fromarray(up).save(ART_DIR / 'stair_up.png')
    Image.fromarray(np.asarray(sheet_img.convert('RGB'))[sy:sy + CELL, sx + CELL:sx + 2 * CELL]).save(
        ART_DIR / 'stair_down.png')

    # 2) 梯级前景蒙版：梯级亮(~200)、阶梯井底纹暗(~55-95)、梯级阴影中等
    L = luminance(up.astype(float))
    mask = np.clip((L - 100.0) / (175.0 - 100.0), 0.0, 1.0) * ALPHA   # 0~0.55

    # 3) 逐层幽灵叠加，原地写回
    for f, x, y in TARGETS:
        p = ROOT / 'floors' / ('floor_%02d.png' % f)
        im = np.asarray(Image.open(p).convert('RGB')).astype(float)
        cx, cy = x * CELL, y * CELL
        cell = im[cy:cy + CELL, cx:cx + CELL]
        im[cy:cy + CELL, cx:cx + CELL] = cell * (1 - mask[..., None]) + up * mask[..., None]
        Image.fromarray(im.round().astype('uint8')).save(p)
        print('  %dF(%d,%d) 已画隐藏上行梯' % (f, x, y))

    print('贴图入库: %s/{MTower_sheet,stair_up,stair_down}.png' % ART_DIR)


if __name__ == '__main__':
    main()
