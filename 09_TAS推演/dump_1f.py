# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

w = M.World.new()
f=1
def ch(o):
    if o==0: return '.'
    ty = M.TYPE.get(M.oatr(o,3),'?')
    if ty=='DOOR': return {2:'y',4:'b',27:'r'}.get(o,'D')
    if ty=='MONSTER': return 'm'
    if ty in ('STATUS','ITEM'): return 'i'
    if ty=='MESSAGE': return 'N'
    if ty=='SAIDAN': return 'A'
    if ty in ('SHOP','BUY','SELL'): return '$'
    return str(o%10)
print('   '+''.join('%d'%(x%10) for x in range(13)))
for y in range(13):
    row=''
    for x in range(13):
        if w.terrain_at(f,x,y)==1: row+='#'
        else:
            o=w.at(f,x,y)
            row+=ch(o)
    print('%2d '%y+row)
# 可达区域（BFS 视怪物可打、门=需钥匙）
print('上梯格(1F):', M.STAIRS[1])
