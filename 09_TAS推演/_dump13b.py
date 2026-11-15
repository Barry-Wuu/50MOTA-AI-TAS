import json, sys

d = json.load(open(r"D:\B++\WorkBuddy\mota_tas_tmp2\repo\09_TAS推演\merged_route_full.json", encoding="utf-8"))
s = d["steps"]
a, b = (int(v) for v in sys.argv[1].split("-"))
for x in s:
    if a <= x["i"] <= b:
        print("%5d F%2d (%2d,%2d) %-3s %-40s %s" % (
            x["i"], x["f"], x["x"], x["y"], x.get("d", ""), (x.get("l") or "")[:40], x.get("e") or ""))
