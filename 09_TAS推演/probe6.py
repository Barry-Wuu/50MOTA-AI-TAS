# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools")
import mota_core as M

for f in (6,7,8,9):
    print("="*20, f, "F", "stairs", M.STAIRS[f])
    for y in range(13):
        row=[]
        for x in range(13):
            t=M.terrain(f,x,y)
            o=M.obj_raw(f,x,y)
            if t==1: ch='#'
            elif t==2: ch='S' if M.stair_up(f,x,y) else 's'
            elif o==0: ch='.'
            else:
                ty=M.TYPE.get(M.oatr(o,3),'?')
                if ty=='MONSTER':
                    hp,atk,dfn,g=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12),M.oatr(o,13)
                    ch='%02d'%o
                elif ty=='DOOR': ch='D%d'%o
                elif ty=='ITEM': ch='I%d'%o
                elif ty=='STATUS': ch='T%d'%o
                elif ty=='KEY': ch='K%d'%o
                elif ty=='MESSAGE': ch='N%d'%o
                elif ty=='BUY': ch='B%d'%o
                else: ch='o%d'%o
            row.append(ch.rjust(3))
        print('y%2d '%y+''.join(row))
    # list monsters
    print("monsters:")
    for y in range(13):
        for x in range(13):
            o=M.obj_raw(f,x,y)
            if o and M.TYPE.get(M.oatr(o,3))=='MONSTER':
                print("   (%d,%d) obj%d %s HP%d ATK%d DEF%d G%d"%(x,y,o,M.oname(o)[:12],M.oatr(o,10),M.oatr(o,11),M.oatr(o,12),M.oatr(o,13)))
    print("items:")
    for y in range(13):
        for x in range(13):
            o=M.obj_raw(f,x,y)
            if o and M.TYPE.get(M.oatr(o,3)) in ('ITEM','STATUS','KEY'):
                print("   (%d,%d) obj%d %s type=%s HP+%d ATK+%d DEF+%d"%(x,y,o,M.oname(o)[:12],M.TYPE.get(M.oatr(o,3)),M.oatr(o,10),M.oatr(o,11),M.oatr(o,12)))
    print("doors:")
    for y in range(13):
        for x in range(13):
            o=M.obj_raw(f,x,y)
            if o and M.TYPE.get(M.oatr(o,3))=='DOOR':
                print("   (%d,%d) obj%d %s color=%s"%(x,y,o,M.oname(o)[:12],M.DOOR_OF.get(o)))
