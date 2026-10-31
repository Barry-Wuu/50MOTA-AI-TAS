# -*- coding: utf-8 -*-
"""扫描 1-11F 全部 水晶/药/钥匙 位置与属性（新鲜世界，初始状态）。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
w = M.World.new()
CAT = {13: '红晶', 14: '蓝晶', 11: '红药+50', 12: '蓝药+200',
       1: '黄钥', 3: '蓝钥', 28: '红钥'}
for f in range(1, 12):
    items = []
    for y in range(13):
        for x in range(13):
            o = w.at(f, x, y)
            if o in CAT:
                items.append((x, y, CAT[o], o))
    if items:
        print('%2dF: %s' % (f, ' | '.join('(%d,%d)%s' % (x, y, n) for (x, y, n, o) in items)))
