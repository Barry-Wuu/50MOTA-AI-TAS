# -*- coding: utf-8 -*-
import csv, io
p=r"D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/魔塔1_route_1F到11F_合法重排.csv"
rows=list(csv.DictReader(io.open(p,encoding="utf-8")))
for r in rows:
    if r["floor"] in ("5","6","7"):
        print(r["step"].rjust(3), r["floor"]+"F", "(%s,%s)"%(r["x"],r["y"]), "HP%-4s"%r["hp"], "A%s D%s"%(r["atk"],r["def"]), "K%s/%s/%s"%(r["ky"],r["kb"],r["kr"]), r["event"][:80])
