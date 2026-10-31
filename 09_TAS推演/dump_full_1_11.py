# -*- coding: utf-8 -*-
"""1F-11F 全图（x0..12 / y0..12），供人工逐格推演。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

DOOR = {2: 'Y门', 4: 'B门', 27: 'R门'}
KEY = {1: 'Y钥', 3: 'B钥', 28: 'R钥'}
out = []
for f in range(1, 12):
    out.append('=' * 72)
    out.append('%dF  up/down=%s' % (f, M.STAIRS.get(f)))
    out.append('=' * 72)
    out.append('     ' + ''.join('%3d' % x for x in range(13)))
    for y in range(13):
        row = ''
        for x in range(13):
            t = M.terrain(f, x, y)
            o = M.obj_raw(f, x, y)
            if o:
                ch = '#'
                ty = M.TYPE.get(M.oatr(o, 3), '?')
                if o in DOOR:
                    ch = {'Y门': 'y', 'B门': 'b', 'R门': 'r'}[DOOR[o]]
                elif o in KEY:
                    ch = {'Y钥': 'k', 'B钥': 'K', 'R钥': 'R'}[KEY[o]]
                elif ty == 'MONSTER':
                    ch = {'obj5': 's', 'obj6': 'q', 'obj7': 'v', 'obj8': 'm',
                          'obj9': 'c', 'obj10': 'b', 'obj16': 'A', 'obj29': 'g',
                          'obj47': 'V', 'obj45': 'S', 'obj46': 'M', 'obj48': 'Z',
                          'obj15': 'G'}.get('obj%d' % o, 'X')
                elif ty == 'STATUS':
                    ch = {11: 'h', 12: 'H', 13: 'a', 14: 'd', 30: 'W', 35: 'D',
                          36: 'D', 80: 'a', 66: 'h', 76: 'H'}.get(o, 'i')
                elif ty == 'ITEM':
                    ch = 'o'
                elif ty == 'MESSAGE':
                    ch = 'n'
                elif ty == 'SAIDAN':
                    ch = 'T'
                elif ty == 'SELL':
                    ch = '$'
                else:
                    ch = '?'
            else:
                ch = {0: '.', 1: '#', 2: 'S'}.get(t, '?')
            row += '%3s' % ch
        out.append('y%-3d%s' % (y, row))
    out.append('--- detail ---')
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if o:
                out.append('  (%2d,%2d) obj%-4d %-12s %-8s hp=%s atk=%s def=%s g=%s' % (
                    x, y, o, M.oname(o)[:12], M.TYPE.get(M.oatr(o, 3), '?'),
                    M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13)))
    out.append('')
open(r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/map_1_11.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
