# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools")
import mota_core as M

print("SHOP_PRICE", {k:M.SHOP_PRICE[k] for k in M.SHOP})
print("altar costs", [M.altar_cost(k) for k in range(9)])
for f in (10,11):
    print("="*20,f,"F stairs",M.STAIRS[f])
    for y in range(13):
        row=[]
        for x in range(13):
            t=M.terrain(f,x,y); o=M.obj_raw(f,x,y)
            if t==1: ch='#'
            elif t==2: ch='S' if M.stair_up(f,x,y) else 's'
            elif o==0: ch='.'
            else:
                ty=M.TYPE.get(M.oatr(o,3),'?')
                if ty=='MONSTER': ch='%02d'%o
                elif ty=='DOOR': ch='D%d'%o
                elif ty=='ITEM': ch='I%d'%o
                elif ty=='STATUS': ch='T%d'%o
                elif ty=='KEY': ch='K%d'%o
                elif ty=='MESSAGE': ch='N%d'%o
                elif ty=='BUY': ch='B%d'%o
                elif ty=='SAIDAN': ch='A%d'%o
                else: ch='o%d'%o
            row.append(ch.rjust(3))
        print('y%2d '%y+''.join(row))
    print("monsters:")
    for y in range(13):
        for x in range(13):
            o=M.obj_raw(f,x,y)
            if o and M.TYPE.get(M.oatr(o,3))=='MONSTER':
                print("   (%d,%d) obj%d %s HP%d ATK%d DEF%d G%d"%(x,y,o,M.oname(o)[:12],M.oatr(o,10),M.oatr(o,11),M.oatr(o,12),M.oatr(o,13)))
print("WARP 2F/3F/4F/5F/6F/7F/8F/9F/10F stair landings:")
for f in range(1,12):
    for (x,y),dst in M.WARP.items():
        if x==0: pass
print("2F", [(k,v) for k,v in M.WARP.items() if k[0]==2])
print("3F", [(k,v) for k,v in M.WARP.items() if k[0]==3])
print("4F", [(k,v) for k,v in M.WARP.items() if k[0]==4])
print("5F", [(k,v) for k,v in M.WARP.items() if k[0]==5])
print("10F", [(k,v) for k,v in M.WARP.items() if k[0]==10])
