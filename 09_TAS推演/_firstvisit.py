import json

d = json.load(open(r"D:\B++\WorkBuddy\mota_tas_tmp2\repo\09_TAS推演\merged_route_full.json", encoding="utf-8"))
s = d["steps"]
first = {}
for x in s:
    first.setdefault(x["f"], x["i"])
for f in sorted(first):
    print("F%-2d first visit @ step %d" % (f, first[f]))
