# -*- coding: utf-8 -*-
import mota_core as M
w = M.World.new()
for f in [6]:
    print("=== floor", f, "=== terrain map")
    print("    " + " ".join("x%-4d"%x for x in range(1,12)))
    for y in range(1,12):
        row=[]
        for x in range(1,12):
            o = w.at(f,x,y)
            t = w.terrain_at(f,x,y)
            if o:
                ty = M.TYPE.get(M.oatr(o,3),'?')
                row.append("%s%d"%(ty,o))
            else:
                row.append({0:'.',1:'#',2:'S'}[t])
        print("y%-3d"%y, " ".join("%-5s"%c for c in row))
