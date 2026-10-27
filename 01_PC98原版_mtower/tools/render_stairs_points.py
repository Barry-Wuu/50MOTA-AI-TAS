#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把每层上下楼梯的落点直接画在楼层图上。
数据源：mota_core.terrain() / stair_up() / warp_to() / WARP（全部从游戏二进制解出，非推断）
图例：
  红点 = 本层上行梯踏步格（踩它上楼）
  蓝点 = 本层下行梯踏步格（踩它下楼）
  绿圈 = 落点：从下层上来，落在本层的这个坐标
  橙框 = 杀 BOSS 后生成的隐藏上梯（静态地图里没有这一格）
  绿框 = 24F 暗门 → 50F（不是楼梯，是 ending 事件 warp）
"""
import os, sys
sys.path.insert(0, '/tmp/motarepo2/01_PC98原版_mtower/tools')
import mota_core as M
from PIL import Image, ImageDraw, ImageFont

ART = '/tmp/motarepo2/08_Java_MTower08a/art'
OUT = '/workspace/魔塔_楼梯落点图'
os.makedirs(OUT, exist_ok=True)

FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
_fc = {}
def f(sz):
    sz = max(6, int(sz))
    if sz not in _fc:
        _fc[sz] = ImageFont.truetype(FONT, sz)
    return _fc[sz]

CELL, N = 40, 13
MARGIN, TOP, BOT = 30, 68, 140
W = N * CELL + MARGIN * 2
H = TOP + N * CELL + BOT

C_WALL    = (56, 56, 70)
C_WALL_HI = (76, 76, 94)
C_FLOOR   = (228, 220, 205)
C_GRID    = (200, 190, 174)
C_UP      = (208, 48, 48)
C_DN      = (36, 96, 200)
C_HID     = (232, 138, 22)
C_IN      = (24, 150, 88)
C_FLY     = (146, 84, 196)   # 紫：飞翔宝珠 / 幻之层传送

up_spr   = Image.open(os.path.join(ART, 'stair_up.png')).convert('RGBA')
down_spr = Image.open(os.path.join(ART, 'stair_down.png')).convert('RGBA')

HIDDEN_UP = {
    10: ((6, 11), 11, (6, 10)),
    20: ((6, 1),  21, (6, 2)),
    30: ((6, 1),  31, (6, 2)),
    40: ((6, 1),  41, (5, 1)),
}
SECRET_DOOR = {24: ((6, 0), 50, (6, 5))}
# 飞翔宝珠（obj26，1F(2,11) 拾取；规则：必须站在楼梯旁使用）
# 落点按实例反推的规律：楼梯格优先 (x, y+1)，不通则 (x+1, y)
#   2F/8F/18F 楼梯 (1,1) 且两侧皆地板 → 落 (1,2)；1F (1,2) 是墙 → 落 (2,1)
FLY_IN = {
    0:  (1, 2, '1F 楼梯旁用飞行之珠下来'),
    44: (1, 2, '幻之阶·只能飞行道具进入'),
}
FLY_ITEM = {1: (2, 11, '飞行之珠 飛翔のオーブ 拾取点')}
FLY_USE = {1: (2, 1, '楼梯旁·可在此起飞'), 44: (1, 2, '楼梯旁·可在此起飞')}


def terrain_grid(fl):
    return [[M.terrain(fl, x, y) for x in range(N)] for y in range(N)]


def build_tables():
    """stairs[f] = [(x,y,'UP'/'DN',tf,tx,ty)]；arrive[f] = [(from_floor, x, y)]"""
    stairs, arrive = {}, {}
    for fl in range(51):
        lst = []
        for y in range(N):
            for x in range(N):
                if M.terrain(fl, x, y) == 2:
                    up = M.stair_up(fl, x, y)
                    w = M.warp_to(fl, x, y)
                    if w:
                        lst.append((x, y, 'UP' if up else 'DN', w[0], w[1], w[2]))
                        arrive.setdefault(w[0], []).append((fl, w[1], w[2]))
                    else:
                        lst.append((x, y, 'UP' if up else 'DN', None, None, None))
        stairs[fl] = lst
    # 隐藏上梯的落点也要进 arrive（静态表里那格是空的，warp 查不到）
    for fl, ((hx, hy), tf, (tx, ty)) in HIDDEN_UP.items():
        arrive.setdefault(tf, []).append((fl, tx, ty))
    return stairs, arrive


STAIRS, ARRIVE = build_tables()
# 50F 的进入方式不是楼梯，是 24F(6,0) 暗门 ending-warp，落点 (6,5)（真魔王 Zeno2 所在）
ARRIVE.setdefault(50, []).append((24, 6, 5))
# 0F / 44F 的进入落点由 FLY_IN 单独渲染（飞翔宝珠），不重复计入 arrive


def diamond(dr, cx, cy, r, color, width=2):
    dr.line([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy), (cx, cy - r)],
            fill=color, width=width)


def render(fl, scale=1.0, detail=True):
    cs = int(round(CELL * scale))
    m, top = int(MARGIN * scale), int(TOP * scale)
    w = int(N * cs + m * 2)
    bot = BOT if detail else 10
    h = int(top + N * cs + bot * scale)
    img = Image.new('RGB', (w, h), (251, 250, 247))
    dr = ImageDraw.Draw(img)

    g = terrain_grid(fl)
    for y in range(N):
        for x in range(N):
            px, py = m + x * cs, top + y * cs
            if g[y][x] == 1:
                dr.rectangle([px, py, px + cs - 1, py + cs - 1], fill=C_WALL, outline=(40, 40, 52))
                dr.line([px + 1, py + 1, px + cs - 2, py + 1], fill=C_WALL_HI)
            else:
                dr.rectangle([px, py, px + cs - 1, py + cs - 1], fill=C_FLOOR, outline=C_GRID)

    # 楼梯踏步格：原著贴图 + 彩色描边 + 角落圆点
    for (x, y, kind, tf, tx, ty) in STAIRS[fl]:
        px, py = m + x * cs, top + y * cs
        spr = up_spr if kind == 'UP' else down_spr
        if scale != 1.0:
            ss = max(8, cs - 2)
            spr = spr.resize((ss, ss), Image.LANCZOS)
        img.paste(spr, (px + (cs - spr.width) // 2, py + (cs - spr.height) // 2), spr)
        col = C_UP if kind == 'UP' else C_DN
        lw = max(2, int(3 * scale))
        dr.rectangle([px + lw // 2, py + lw // 2, px + cs - 1 - lw // 2, py + cs - 1 - lw // 2],
                     outline=col, width=lw)
        rr = max(4, int(cs * 0.16))
        dr.ellipse([px + 3, py + 3, px + 3 + rr * 2, py + 3 + rr * 2], fill=col, outline=(255, 255, 255))

    # 落点（从下层上来落在这里）：绿色空心圈 + 十字
    _skip = {(FLY_IN[fl][0], FLY_IN[fl][1])} if fl in FLY_IN else set()
    for (ff, x, y) in ARRIVE.get(fl, []):
        if (x, y) in _skip:
            continue
        px, py = m + x * cs, top + y * cs
        pad = max(4, int(cs * 0.14))
        lw = max(2, int(3 * scale))
        for k in range(lw):
            dr.ellipse([px + pad + k, py + pad + k, px + cs - pad - k, py + cs - pad - k], outline=C_IN)
        cr = max(3, int(cs * 0.13))
        cx, cy = px + cs // 2, py + cs // 2
        dr.line([cx - cr, cy, cx + cr, cy], fill=C_IN, width=max(1, lw - 1))
        dr.line([cx, cy - cr, cx, cy + cr], fill=C_IN, width=max(1, lw - 1))

    # 隐藏上梯
    if fl in HIDDEN_UP:
        (hx, hy), tf, (tx, ty) = HIDDEN_UP[fl]
        px, py = m + hx * cs, top + hy * cs
        spr = up_spr if scale == 1.0 else up_spr.resize((max(8, cs - 2),) * 2, Image.LANCZOS)
        img.paste(spr, (px + (cs - spr.width) // 2, py + (cs - spr.height) // 2), spr)
        step = max(3, int(5 * scale))
        for i in range(0, cs, step * 2):
            dr.line([px + i, py, min(px + i + step, px + cs - 1), py], fill=C_HID, width=max(2, int(2 * scale)))
            dr.line([px + i, py + cs - 1, min(px + i + step, px + cs - 1), py + cs - 1], fill=C_HID, width=max(2, int(2 * scale)))
            dr.line([px, py + i, px, min(py + i + step, py + cs - 1)], fill=C_HID, width=max(2, int(2 * scale)))
            dr.line([px + cs - 1, py + i, px + cs - 1, min(py + i + step, py + cs - 1)], fill=C_HID, width=max(2, int(2 * scale)))
        if detail:
            lab = 'BOSS'
            dr.rectangle([px + 1, py + cs - 13, px + cs - 2, py + cs - 1], fill=C_HID)
            dr.text((px + 3, py + cs - 13), lab, font=f(cs * 0.30), fill=(255, 255, 255))

    # 24F 暗门
    if fl in SECRET_DOOR:
        (dx, dy), tf, (tx, ty) = SECRET_DOOR[fl]
        px, py = m + dx * cs, top + dy * cs
        dr.rectangle([px + 2, py + 2, px + cs - 3, py + cs - 3], outline=C_IN, width=max(2, int(3 * scale)))
        if detail:
            dr.rectangle([px + 2, py + cs - 14, px + cs - 3, py + cs - 2], fill=C_IN)
            dr.text((px + 4, py + cs - 14), '→50', font=f(cs * 0.33), fill=(255, 255, 255))

    # 飞翔宝珠：落点 / 拾取点 / 起飞点
    if fl in FLY_IN:
        fx, fy, _ = FLY_IN[fl]
        px, py = m + fx * cs, top + fy * cs
        diamond(dr, px + cs // 2, py + cs // 2, int(cs * 0.34), C_FLY, max(2, int(3 * scale)))
        if detail:
            dr.rectangle([px + 1, py + cs - 13, px + cs - 2, py + cs - 1], fill=C_FLY)
            dr.text((px + 4, py + cs - 13), 'FLY', font=f(cs * 0.30), fill=(255, 255, 255))
    if fl in FLY_ITEM:
        fx, fy, _ = FLY_ITEM[fl]
        px, py = m + fx * cs, top + fy * cs
        diamond(dr, px + cs // 2, py + cs // 2, int(cs * 0.32), C_FLY, max(2, int(2 * scale)))
        if detail:
            dr.rectangle([px + 1, py + cs - 13, px + cs - 2, py + cs - 1], fill=C_FLY)
            dr.text((px + 4, py + cs - 13), 'ORB', font=f(cs * 0.28), fill=(255, 255, 255))

    # 坐标刻度
    if detail and scale >= 0.75:
        fn = f(11 * scale if scale < 1 else 11)
        for i in range(N):
            lbl = str(i)
            tw = dr.textlength(lbl, font=fn)
            dr.text((m + i * cs + (cs - tw) / 2, top - 15), lbl, font=fn, fill=(126, 122, 116))
            dr.text((m - 17, top + i * cs + cs / 2 - 7), lbl, font=fn, fill=(126, 122, 116))

    # 标题
    dr.text((m, 12 * scale), '第 %d 层' % fl if fl else '地下 0 层', font=f(23 * scale), fill=(28, 28, 38))
    dr.text((w - m - 46 * scale, 14 * scale), 'F%d' % fl, font=f(17 * scale), fill=(158, 152, 144))

    # 底部文字：精确落点
    if not detail:
        return img
    ty0 = top + N * cs + 8 * scale
    fn = f(13 * scale)
    rows = []
    ups = [s for s in STAIRS[fl] if s[2] == 'UP']
    dns = [s for s in STAIRS[fl] if s[2] == 'DN']
    for s in ups:
        rows.append((C_UP, '上行 (%d,%d)' % (s[0], s[1]), '→ %dF (%d,%d)' % (s[3], s[4], s[5])))
    for s in dns:
        rows.append((C_DN, '下行 (%d,%d)' % (s[0], s[1]), '→ %dF (%d,%d)' % (s[3], s[4], s[5])))
    if fl in HIDDEN_UP:
        (hx, hy), tf, (tx, ty) = HIDDEN_UP[fl]
        rows.append((C_HID, '隐藏上梯 (%d,%d)' % (hx, hy), '→ %dF (%d,%d)' % (tf, tx, ty)))
    if fl in SECRET_DOOR:
        (dx, dy), tf, (tx, ty) = SECRET_DOOR[fl]
        rows.append((C_IN, '暗门 (%d,%d)' % (dx, dy), '→ %dF (%d,%d)' % (tf, tx, ty)))
    if fl in FLY_IN:
        fx, fy, why = FLY_IN[fl]
        rows.append((C_FLY, '飞行落点 (%d,%d)' % (fx, fy), why))
    if fl == 1:
        rows.append((C_FLY, '飞行之珠 (%d,%d)' % FLY_ITEM[1][:2], '飛翔のオーブ；须站楼梯旁用，可去 0F'))
    if not rows:
        rows.append(((150, 145, 138), '本层无楼梯格', '只能从 24F 暗门 warp 进' if fl == 50 else ''))
    for i, (col, s1, s2) in enumerate(rows[:5]):
        yy = ty0 + i * 22 * scale
        dr.rectangle([m, yy + 3 * scale, m + 9 * scale, yy + 15 * scale], fill=col)
        dr.text((m + 15 * scale, yy), s1, font=fn, fill=(58, 58, 68))
        dr.text((m + 132 * scale, yy), s2, font=fn, fill=col)

    # 落点行
    ar = ARRIVE.get(fl, [])
    if ar:
        yy = ty0 + max(len(rows[:5]), 1) * 22 * scale
        s = '落点：' + '、'.join('%dF→(%d,%d)' % (a[0], a[1], a[2]) for a in ar[:3])
        if len(ar) > 3:
            s += ' 等%d处' % len(ar)
        dr.text((m, yy), s, font=f(12 * scale), fill=C_IN)
    return img


def legend_strip(width):
    img = Image.new('RGB', (width, 46), (251, 250, 247))
    dr = ImageDraw.Draw(img)
    fn = f(14)
    items = [(C_UP, '上行梯踏步格'), (C_DN, '下行梯踏步格'), (C_IN, '落点（从下层上来落在本层的位置）'),
             (C_HID, '隐藏上梯：杀 BOSS 后出现'), (C_FLY, '飞行之珠 / 幻之阶落点')]
    x = 14
    for col, lab in items:
        dr.ellipse([x, 18, x + 12, 30], fill=col)
        dr.text((x + 18, 16), lab, font=fn, fill=(58, 58, 68))
        x += 18 + int(dr.textlength(lab, font=fn)) + 24
    return img


def main():
    for fl in range(51):
        render(fl).save(os.path.join(OUT, 'floor_%02d.png' % fl))
    groups = [(0, 9), (10, 19), (20, 29), (30, 39), (40, 49), (50, 50)]
    for a, b in groups:
        fls = list(range(a, b + 1))
        thumbs = [render(fl, scale=0.68, detail=False) for fl in fls]
        tw, th = thumbs[0].size
        cols, pad = 5, 10
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * tw + pad * (cols + 1), rows * th + pad * (rows + 1) + 52),
                          (251, 250, 247))
        d2 = ImageDraw.Draw(sheet)
        title = '魔塔1  第 %d–%d 层：上下楼梯落点' % (a, b) if a != b else '魔塔1  第 50 层（终战）'
        d2.text((pad + 4, 12), title, font=f(21), fill=(28, 28, 38))
        for i, t in enumerate(thumbs):
            r, c = i // cols, i % cols
            sheet.paste(t, (pad + c * (tw + pad), 46 + pad + r * (th + pad)))
        sheet.paste(legend_strip(sheet.width), (0, sheet.height - 46))
        sheet.save(os.path.join(OUT, 'overview_%02d-%02d.png' % (a, b)))
        print('overview', a, b, sheet.size)
    print('done floors 51')


if __name__ == '__main__':
    main()
