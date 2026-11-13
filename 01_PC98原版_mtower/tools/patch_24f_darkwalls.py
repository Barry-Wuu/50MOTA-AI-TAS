# -*- coding: utf-8 -*-
"""补画 24F 第一行（y=1）的两格暗墙：(5,1)(7,1)。

依据（50F_CHAIN.md 行 12/20、魔塔1_资料笔记.md 行 221）：
  · 24F 初始 map：`map[26][45]=31; map[27][44]=1; map[27][46]=1; map[28..30][45]=3`
    → (6,0)=31、(5,1)=(7,1)=1（地板）、(6,2..4)=3（暗砖）
  · 26F(6,7) 剧情触发后（MTower.java @2820-2825）：
    (6,0)/(6,2..4) 31/3 → 1（**竖井挖开，变通路**）
    (5,1)/(7,1)   1     → 3（**把 row1 通道截断，逼你走中央竖井**）
  → 竖井段真正呈现的形态是「中央一列通路 + y=1 两侧各一块暗墙」，
    但 floors/floor_24.png 的底图只画了中央那列 3 格暗砖，**y=1 的两侧暗墙缺画**。

做法：暗墙图素 = 墙砖压暗 40%（MAP_NOTES §5 渲染约定），实测为 `#2e1a0e`，
      在 (6,2)(6,3)(6,4) 上是完全相同的 40×40 贴图（md5 一致），直接平移复制。

同时改：
  · 01_PC98原版_mtower/floors/floor_24.png   —— 单层图（已被 render_floors_stairs 烘焙过叠加层，只能原地补图素）
  · 01_PC98原版_mtower/map_50f.png           —— 5 列 × 11 行总图，24F 位于 r=5,c=3
    （origin = MPAD + c*(MCELL+MGAP), MPAD + r*(MCELL+MGAP) = (1600, 2660)，常量见 render_floors_stairs.py）

可重复执行（幂等：目标格已是暗墙则跳过）。
"""
import hashlib
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent          # 01_PC98原版_mtower/
CELL = 40                                              # 13 格 × 40px = 520
SRC = (6, 2)                                           # 暗墙样板格
TARGETS = [(5, 1), (7, 1)]                             # 要补的两格（row 1）
MCELL, MGAP, MPAD = 520, 10, 10                        # render_floors_stairs.py @43


def tile_md5(img, x, y):
    t = img.crop((x * CELL, y * CELL, x * CELL + CELL, y * CELL + CELL))
    return hashlib.md5(t.tobytes()).hexdigest()


def patch(img, ox, oy, label):
    """把 (SRC) 的 40×40 图素复制到目标格；ox/oy 为该层在整图中的原点（单层图=0,0）。"""
    src = img.crop(((ox + SRC[0] * CELL), (oy + SRC[1] * CELL),
                    (ox + SRC[0] * CELL + CELL), (oy + SRC[1] * CELL + CELL)))
    src_sum = tile_md5(img, *SRC)
    changed = 0
    for (x, y) in TARGETS:
        box = (ox + x * CELL, oy + y * CELL, ox + x * CELL + CELL, oy + y * CELL + CELL)
        cur = hashlib.md5(img.crop(box).tobytes()).hexdigest()
        if cur == src_sum:
            print('  · %s (%d,%d) 已是暗墙，跳过' % (label, x, y))
            continue
        img.paste(src, box[:2])
        print('  ✓ %s (%d,%d) 补暗墙图素' % (label, x, y))
        changed += 1
    return changed


def main():
    total = 0

    p1 = ROOT / 'floors' / 'floor_24.png'
    im1 = Image.open(p1).convert('RGB')
    total += patch(im1, 0, 0, 'floor_24.png')
    if total:
        im1.save(p1)
        print('  → 写回 %s (%dx%d)' % (p1.name, im1.size[0], im1.size[1]))

    p2 = ROOT / 'map_50f.png'
    if p2.exists():
        im2 = Image.open(p2).convert('RGB')
        r, c = 1 + (24 - 1) // 5, (24 - 1) % 5            # 24F → r=5, c=3
        ox = MPAD + c * (MCELL + MGAP)
        oy = MPAD + r * (MCELL + MGAP)
        n = patch(im2, ox, oy, 'map_50f.png')
        if n:
            im2.save(p2)
            print('  → 写回 map_50f.png (%dx%d)  24F 原点=(%d,%d)' %
                  (im2.size[0], im2.size[1], ox, oy))
        total += n

    print('完成，共补 %d 格。' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
