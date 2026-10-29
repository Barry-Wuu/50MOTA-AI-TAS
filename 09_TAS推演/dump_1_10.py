# -*- coding: utf-8 -*-
"""一次性 dump 1F-10F 全数据，供手工排路线用（不做任何搜索）"""
import sys, io
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

out = io.StringIO()
def w(s=''):
    out.write(s + '\n')

DOOR = {2: '黄门', 4: '蓝门', 27: '红门'}
KEY = {1: '黄钥', 3: '蓝钥', 28: '红钥'}

for f in range(1, 11):
    w('=' * 70)
    w('%dF   stairs up/down = %s' % (f, M.stairs_of(f)))
    w('=' * 70)
    w('--- terrain (#=墙 .=地板 S=楼梯) ---')
    for y in range(1, 13):
        row = []
        for x in range(1, 13):
            t = M.terrain(f, x, y)
            if t == 1:
                row.append('  #')
            elif t == 2:
                row.append('  S')
            else:
                row.append('  .')
        w('y%-2d%s' % (y, ''.join(row)))
    w('--- obj 编号 ---')
    for y in range(1, 13):
        row = []
        for x in range(1, 13):
            o = M.obj_raw(f, x, y)
            row.append('%3d' % o if o else '  .')
        w('y%-2d%s' % (y, ''.join(row)))
    w('--- obj 明细 ---')
    for y in range(1, 13):
        for x in range(1, 13):
            o = M.obj_raw(f, x, y)
            if not o:
                continue
            a = [M.oatr(o, i) for i in range(14)]
            ty = M.TYPE.get(a[3], '?')
            tag = ''
            if o in DOOR:
                tag = 'DOOR/' + DOOR[o]
            elif o in KEY:
                tag = 'KEY/' + KEY[o]
            elif ty == 'MONSTER':
                tag = 'MON hp%d atk%d def%d g%d' % (a[10], a[11], a[12], a[13])
            w('  (%2d,%2d) obj%-4d %-14s type=%-6s %s' % (x, y, o, M.oname(o)[:14], ty, tag))
    w()

open(r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/dump_1_10.txt', 'w', encoding='utf-8').write(out.getvalue())
print('written', len(out.getvalue()))
