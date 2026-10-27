# -*- coding: utf-8 -*-
import mota_core as M
w=M.World.new()
f=10
print("10F 楼梯/传送:")
for y in range(1,12):
    for x in range(1,12):
        if w.terrain_at(f,x,y)==2:
            print("  梯 (%d,%d) warp->%s"%(x,y,M.warp_to(f,x,y)))
print("入口落点: 9F(6,1) -> ", M.warp_to(9,6,1))
print("9F 梯:", [(x,y) for y in range(1,12) for x in range(1,12) if w.terrain_at(9,x,y)==2])
print()
print("10F 全表 (x,y): terrain, obj, name")
for y in range(1,12):
    for x in range(1,12):
        t=w.terrain_at(f,x,y); o=w.at(f,x,y)
        if t==1: continue
        s="%2d,%2d t%d"%(x,y,t)
        if o:
            ty=M.TYPE.get(M.oatr(o,3),'?')
            if ty=='MONSTER':
                s+=" obj%d %s hp%d atk%d def%d g%d"%(o,M.oname(o),M.oatr(o,10),M.oatr(o,11),M.oatr(o,12),M.oatr(o,13))
            elif ty=='DOOR': s+=(" obj%d 暗墙"%o) if o==89 else (" obj%d 门%s"%(o,M.DOOR_OF[o]))
            elif ty=='KEY': s+=" obj%d 钥%s"%(o,M.KEY_OF[o])
            elif ty=='STATUS':
                hp,atk,dfn=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12)
                s+=" obj%d %s hp%d atk%d def%d"%(o,M.oname(o),hp,atk,dfn)
            elif ty in ('SELL','BUY'): s+=" obj%d 商店价%d grant%s"%(o,M.oatr(o,13),M.SHOP_GRANT.get(o))
            else: s+=" obj%d %s %s"%(o,ty,M.oname(o))
        print(s)
