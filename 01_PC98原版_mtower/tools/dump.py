# -*- coding: utf-8 -*-
import mota_core as M
w = M.World.new()
LEG={0:'.',1:'#',2:'S'}
def cell(f,x,y):
    o=w.at(f,x,y); t=w.terrain_at(f,x,y)
    if o:
        ty=M.TYPE.get(M.oatr(o,3),'?')
        if ty=='DOOR': return {'y':'y','b':'b','r':'r'}.get(M.DOOR_OF.get(o),'D')
        if ty=='KEY': return {'y':'Y','b':'B','r':'R'}.get(M.KEY_OF.get(o),'K')
        if ty=='MONSTER': return 'm'
        if ty=='ITEM': return 'i'
        if ty=='STATUS': return 's'
        if ty=='SELL': return 'S'
        if ty=='BUY': return 'S'
        if ty=='SCORE': return 'c'
        if ty=='MESSAGE': return 'm'
        if ty=='SAIDAN': return 'A'
        if ty=='NORMAL': return '.'
        return '?'
    return LEG[t]
for f in range(6,12):
    print("="*70)
    print("FLOOR",f)
    print("    " + " ".join("x%-2d"%x for x in range(1,12)))
    for y in range(1,12):
        print("y%-2d "%y + " ".join("%-3s"%cell(f,x,y) for x in range(1,12)))
    print("  --- objects ---")
    for y in range(1,12):
        for x in range(1,12):
            o=w.at(f,x,y)
            if o:
                ty=M.TYPE.get(M.oatr(o,3),'?')
                nm=M.oname(o)
                extra=''
                if ty=='MONSTER':
                    extra="HP=%s ATK=%s DEF=%s GOLD=%s"%(M.oatr(o,6),M.oatr(o,7),M.oatr(o,8),M.oatr(o,9))
                elif ty=='KEY': extra="keycolor=%s"%M.KEY_OF.get(o)
                elif ty=='DOOR': extra="doorcolor=%s"%M.DOOR_OF.get(o)
                elif ty=='ITEM': extra="attrs=%s"%(M.OA[o][1:14],)
                elif ty=='STATUS': extra="attrs=%s"%(M.OA[o][1:14],)
                print("   (%2d,%2d) obj%-4d %-8s %-14s %s"%(x,y,o,ty,nm,extra))
