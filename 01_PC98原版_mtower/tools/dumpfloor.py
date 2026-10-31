# -*- coding: utf-8 -*-
"""dumpfloor.py —— 楼层精确布局导出（用于把攻略方位词换成坐标）

输出：
  1. ASCII 地形图（# 墙 / S 楼梯 / . 地板）
  2. 物件编号矩阵
  3. 逐格物件清单（含名称、属性），按类别分组
用法：python tools/dumpfloor.py 4 5 6
"""
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M

SHORT = {
    1: 'y', 2: 'Y', 3: 'b', 4: 'B', 27: 'R', 28: 'r',
    5: 'G', 6: 'R', 7: 'b', 8: 'p', 9: 'K', 10: 'K', 11: 'I', 12: 'I',
    13: 'r', 14: 'c', 15: 'd', 16: 'g', 17: 'w', 18: 'k', 19: '~',
    20: 'O', 21: '-', 22: 'A', 23: '-', 24: '%', 25: '$', 26: '?',
    29: '$', 30: '$', 31: '$', 32: '$', 33: 'S', 34: 'S', 35: 'D',
    45: 'm', 46: 'm', 47: 'M', 48: 'z', 49: 'Z', 50: 'v', 51: 'V',
    52: 'l', 53: 'L', 54: 'n', 55: 'N', 56: 'R', 57: 'g', 58: 'h',
    59: 'P', 60: 'X', 61: 'x', 62: 'W', 63: 'q', 64: 'Q', 65: 'j',
    66: 'I', 67: 'I', 68: 'i', 69: 'e', 70: 'E', 71: 't', 72: 'T',
    73: 'o', 74: 'D', 75: 'A', 76: 'I', 77: 'I', 78: 'I', 79: '~',
    80: '?', 81: '?', 82: '?', 83: '?', 84: '?', 85: '?', 86: '?',
    87: '?', 88: 'T', 89: '#', 90: 'G', 91: '?', 92: '?', 93: '?',
    94: '?', 95: '?', 96: '?', 97: '?', 98: '?', 99: '?',
    100: '?', 101: '?', 102: '?', 103: 'C', 104: '?', 105: '?',
    106: '?', 107: '?', 108: '?', 109: '?', 110: '?', 111: '?',
    112: 'P', 113: 'g', 114: 'P', 115: '?',
}


def dump(f):
    print('=' * 78)
    print('%dF   STAIRS up=%s down=%s' % (f, M.STAIRS[f][0], M.STAIRS[f][1]))
    print('=' * 78)
    print('   ' + ''.join('%d' % (x % 10) for x in range(13)))
    for y in range(13):
        row = ''
        for x in range(13):
            t = M.terrain(f, x, y)
            o = M.obj_raw(f, x, y)
            if t == 1:
                row += '#'
            elif t == 2:
                row += 'S'
            elif o:
                row += SHORT.get(o, '*')
            else:
                row += '.'
        print('%2d %s' % (y, row))
    print()
    # 分组清单
    groups = {'KEY': [], 'DOOR': [], 'MONSTER': [], 'ITEM': [], 'OTHER': []}
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            nm = M.oname(o)
            if o in M.KEY_OF:
                g = 'KEY'
            elif ty == 'DOOR':
                g = 'DOOR'
            elif ty == 'MONSTER':
                g = 'MONSTER'
            elif ty in ('STATUS', 'ITEM'):
                g = 'ITEM'
            else:
                g = 'OTHER'
            if g == 'MONSTER':
                desc = '%-14s %d/%d/%d g%d' % (nm, M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13))
            elif g == 'ITEM':
                desc = '%-16s hp%+d atk%+d def%+d' % (nm, M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12))
            else:
                desc = nm
            groups[g].append('(%2d,%2d) obj%-3d %s' % (x, y, o, desc))
    for g in ('KEY', 'DOOR', 'MONSTER', 'ITEM', 'OTHER'):
        if groups[g]:
            print('-- %s --' % g)
            for line in groups[g]:
                print('  ' + line)
    print()


if __name__ == '__main__':
    for a in sys.argv[1:]:
        dump(int(a))
