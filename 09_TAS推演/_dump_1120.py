# -*- coding: utf-8 -*-
"""渲染 11F-20F 地图：地形+物件。
用法: python _dump_1120.py [f1] [f2] ...
"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

def sym(f, x, y):
    t = M.terrain(f, x, y)
    if t == 1:
        return '█'
    if t == 2:
        return 'S'
    o = M.obj_raw(f, x, y)
    if o == 0:
        return '·'
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if o in M.KEY_OF:
        return {'y': 'y', 'b': 'b', 'r': 'r'}[M.KEY_OF[o]]
    if o in M.DOOR_OF:
        return {'y': 'Y', 'b': 'B', 'r': 'R'}[M.DOOR_OF[o]]
    if o == 22:
        return 'A'          # 祭坛
    if o == 20:
        return 'o'          # 落穴装饰
    if o == 21 or o == 23:
        return '='
    if o == 89:
        return '?'          # 假墙
    if o == 88:
        return 'D'          # 盗贼
    if o == 90:
        return 'G'          # 楼梯守卫
    if o == 79:
        return '~'          # 熔岩
    if ty == 'MONSTER':
        nm = M.oname(o)
        # 用怪物名首字符（日文/英文）
        if 'スライム' in nm:
            return 'S' if 'Ｇ' in nm or 'G' in nm else 's'
        if 'バット' in nm or '蝙蝠' in nm:
            return 'B' if '大' in nm else 'b'
        if '僧侶' in nm:
            return 'P' if '上級' in nm else 'p'
        if 'ゾンビナイト' in nm:
            return 'Z'
        if 'ゾンビ' in nm:
            return 'z'
        if 'ロック' in nm:
            return 'R'
        if 'バンパイア' in nm:
            return 'V'
        if 'ダコ' in nm:
            return 'O'
        if 'スケルトン' in nm:
            return 'K'
        if '魔導師' in nm:
            return 'W'
        return 'M'
    if ty in ('STATUS', 'ITEM'):
        return 'I'
    if ty in ('NORMAL', 'SCORE', 'MESSAGE'):
        return 'N'
    if ty in ('SELL', 'BUY'):
        return '$'
    return '#'

def dump(f):
    print('======== %dF ========' % f)
    for y in range(13):
        line = '%2d ' % y
        for x in range(13):
            line += sym(f, x, y)
        print(line)
    print('    ' + ''.join((str(x // 10) if x >= 10 else ' ') for x in range(13)))
    print('    ' + ''.join(str(x % 10) for x in range(13)))
    # 物件清单
    print('  物件:')
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if o:
                print('    (%2d,%2d) obj%-3d %-12s hp%-5s atk%-4s def%-4s' % (
                    x, y, o, M.oname(o)[:12], M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12)))
    print()

if __name__ == '__main__':
    floors = [int(a) for a in sys.argv[1:]] or list(range(11, 21))
    for f in floors:
        dump(f)