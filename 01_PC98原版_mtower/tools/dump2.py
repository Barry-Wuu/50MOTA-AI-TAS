# -*- coding: utf-8 -*-
import mota_core as M
w = M.World.new()
for f in range(6,12):
    print("="*72); print("FLOOR",f)
    print("    " + " ".join("x%-2d"%x for x in range(1,12)))
    for y in range(1,12):
        row=[]
        for x in range(1,12):
            o=w.at(f,x,y); t=w.terrain_at(f,x,y)
            if o:
                ty=M.TYPE.get(M.oatr(o,3),'?')
                if ty=='DOOR': row.append('?' if o==89 else {'y':'y','b':'b','r':'r'}[M.DOOR_OF[o]])
                elif ty=='KEY': row.append({'y':'Y','b':'B','r':'R'}[M.KEY_OF[o]])
                elif ty=='MONSTER': row.append('m')
                elif ty=='ITEM': row.append('i')
                elif ty=='STATUS': row.append('s')
                elif ty in ('SELL','BUY'): row.append('$')
                elif ty=='SCORE': row.append('c')
                elif ty=='MESSAGE': row.append('M')
                elif ty=='SAIDAN': row.append('A')
                else: row.append('.')
            else: row.append({0:'.',1:'#',2:'S'}[t])
        print("y%-2d "%y + " ".join("%-3s"%c for c in row))
    print("  -- objects --")
    for y in range(1,12):
        for x in range(1,12):
            o=w.at(f,x,y)
            if not o: continue
            ty=M.TYPE.get(M.oatr(o,3),'?'); nm=M.oname(o)
            if ty=='MONSTER':
                hp,atk,dfn,gold=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12),M.oatr(o,13)
                per=20-dfn; extra="HP%-4d ATK%-4d DEF%-3d G%-3d per=%d loss=%s"%(hp,atk,dfn,gold,per,((atk-10)*((hp+per-1)//per-1) if per>0 else 'X'))
            elif ty=='KEY': extra="color=%s"%M.KEY_OF[o]
            elif ty=='DOOR': extra=('暗墙 obj89' if o==89 else 'color=%s'%M.DOOR_OF[o])
            elif ty=='ITEM': extra="OA=%s"%M.OA[o][1:14]
            elif ty=='STATUS': extra="OA=%s  text=%s"%(M.OA[o][1:14],nm)
            elif ty in ('SELL','BUY'): extra="price=%s grant=%s"%(M.oatr(o,13),M.SHOP_GRANT.get(o))
            else: extra=""
            print("   (%2d,%2d) obj%-4d %-8s %-16s %s"%(x,y,o,ty,nm[:16],extra))
