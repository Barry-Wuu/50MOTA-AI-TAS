import json

d = json.load(open(r"D:\B++\WorkBuddy\mota_tas_tmp2\repo\09_TAS推演\merged_route_full.json", encoding="utf-8"))
segs = d["segs"]
for k, v in segs.items():
    if isinstance(v, dict):
        print(k, {kk: v[kk] for kk in list(v)[:8]})
    else:
        print(k, str(v)[:200])
print("total", d["total"], "floors", d.get("floors"))
