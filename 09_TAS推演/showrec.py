# -*- coding: utf-8 -*-
import csv, io
p=r"D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/魔塔1_route_1F到21F.csv"
rows=list(csv.DictReader(io.open(p,encoding="utf-8-sig")))
print("cols", rows[0].keys())
for i,r in enumerate(rows[:80],1):
    print(i, r.get("floor"), r.get("x"), r.get("y"), "HP"+r.get("hp",""), "A"+r.get("atk",""), "D"+r.get("def",""), "G"+r.get("gold",""), "K%s/%s/%s"%(r.get("ky"),r.get("kb"),r.get("kr")), (r.get("event") or "")[:70])
