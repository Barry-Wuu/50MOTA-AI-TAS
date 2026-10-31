# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
w = M.World.new()
f=3
def ch(o):
    if not o: return '.'
    ty=M.TYPE.get(M.oatr(o,3),'?')
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
print('3F 上梯:', M.STAIRS[3])
# 触发格与守卫
print('TRAP trigger(3F):', M.TRAP_3F['trigger'], 'guards:', M.TRAP_3F['guards'])
