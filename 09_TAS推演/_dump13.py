import json, sys

d = json.load(open(r"D:\B++\WorkBuddy\mota_tas_tmp2\repo\09_TAS推演\merged_route_full.json", encoding="utf-8"))
s = d["steps"]

ranges = [(1955, 2045), (2085, 2155), (2640, 2690), (6695, 6765)]
if len(sys.argv) > 1:
    ranges = [tuple(int(v) for v in sys.argv[1].split("-"))]

for a, b in ranges:
    print("==== %d..%d" % (a, b))
    for x in s:
        if a <= x["i"] <= b:
            ev = x.get("e")
            evs = ""
            if ev:
                evs = " EV:" + str(ev)
            dh, da, dd, dg = x.get("dh"), x.get("da"), x.get("dd"), x.get("dg")
            st = ""
            if dh or da or dd or dg:
                st = " dHP%s dA%s dD%s dG%s" % (dh, da, dd, dg)
            print("  %5d F%2d (%d,%d)%s%s" % (x["i"], x["f"], x["x"], x["y"], st, evs))
