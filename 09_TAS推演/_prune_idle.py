"""Remove two idle detours from merged_route_full.json:
1) 27F old-man visit: steps 3528-3547 (20 steps) — walk to (6,1) and back, 老人只念一句属性点评
   （obj141，无属性/道具收益；与基线口径一致：只保留 NPC 本体，不保留这次往返）
2) 1F rectangle loop: steps 1030-1077 (48 steps) — giant loop from (5,6) back to (5,6)

Then renumber all step indices, fix cons/dyn references, update floors/total counts.
"""
import json, copy, sys

INP = "merged_route_full.json"
OUT = "merged_route_full.json"

d = json.load(open(INP, encoding="utf-8"))
s = d["steps"]
N = len(s)

# Build index map: old_i -> new_i
# Steps to remove (by their .i field, 1-based as shown in UI):
REMOVE = set()
# 27F: remove steps with i in [3528, 3547]  (20 steps: (6,11)→(6,1)→back to (6,11))
#   Keep 3527 (6,11) and 3548 (7,11) as bridge — adjacent
#   ⚠️ 2026-11-15：13F 过路改飞 + V7 少绕 14F + V10/V11/V18/V20/V21 五段爬楼改飞
#   （原始步 7172→6904，省 268 步），原 3528-3547 整体前移 → 3260-3279
#   （27F 段首步 3255、末步 3283 已核对）
for i in range(3260, 3280):
    REMOVE.add(i)
# 1F: remove steps with i in [1030, 1077]  (48 steps, keep 1029 at (5,6) as bridge)
for i in range(1030, 1078):
    REMOVE.add(i)

print(f"Removing {len(REMOVE)} steps: "
      f"1F [{min(r for r in REMOVE if r < 2000)}..{max(r for r in REMOVE if r < 2000)}], "
      f"27F [{min(r for r in REMOVE if r >= 2000)}..{max(r for r in REMOVE if r >= 2000)}]")

# Verify removal targets are safe (no events on removed steps; it=list is carried state, not pickup)
# A real pickup shows as dh/da/dd/dg non-zero OR e contains "手に入れた"
bad = [x for x in s if x["i"] in REMOVE and x.get("e")]
if bad:
    print(f"ERROR: {len(bad)} steps to remove have events!")
    for b in bad:
        print(f"  step {b['i']} f{b['f']} e={b.get('e')!r}")
    sys.exit(1)
# Also check no stat deltas on removed steps
bad2 = [x for x in s if x["i"] in REMOVE and (x.get("dh") or x.get("da") or x.get("dd") or x.get("dg"))]
if bad2:
    print(f"WARNING: {len(bad2)} steps have stat deltas:")
    for b in bad2:
        print(f"  step {b['i']} f{b['f']} dh={b.get('dh')} da={b.get('da')} dd={b.get('dd')} dg={b.get('dg')}")
else:
    print("OK: all removal targets are idle (no events, no stat changes)")

# Verify adjacency after removal
# 1F: step 1029 (5,6) -> step 1078 (5,5)  — adjacent? yes (diff 1 in y)
s1029 = next(x for x in s if x["i"] == 1029)
s1078 = next(x for x in s if x["i"] == 1078)
d1 = abs(s1029["x"] - s1078["x"]) + abs(s1029["y"] - s1078["y"])
print(f"1F bridge: step 1029 ({s1029['x']},{s1029['y']}) -> step 1078 ({s1078['x']},{s1078['y']}) dist={d1}")
assert d1 == 1, f"1F bridge not adjacent! dist={d1}"

# 27F: step 3259 (6,11) -> step 3280 (7,11)  — adjacent? yes (diff 1 in x)
s3881 = next(x for x in s if x["i"] == 3259)
s3902 = next(x for x in s if x["i"] == 3280)
d2 = abs(s3881["x"] - s3902["x"]) + abs(s3881["y"] - s3902["y"])
print(f"27F bridge: step 3881 ({s3881['x']},{s3881['y']}) -> step 3902 ({s3902['x']},{s3902['y']}) dist={d2}")
assert d2 == 1, f"27F bridge not adjacent! dist={d2}"

# Build old_i -> new_i mapping
old_to_new = {}
new_i = 0
for x in s:
    if x["i"] in REMOVE:
        continue
    new_i += 1
    old_to_new[x["i"]] = new_i

print(f"Old steps: {N}, removed: {len(REMOVE)}, new steps: {new_i}")

# Filter steps and renumber
new_steps = []
for x in s:
    if x["i"] in REMOVE:
        continue
    x2 = copy.deepcopy(x)
    x2["i"] = old_to_new[x["i"]]
    new_steps.append(x2)

d["steps"] = new_steps

# Fix cons: {floor: [[x,y,stepIdx,type],...]}
if isinstance(d.get("cons"), dict):
    for fl, lst in d["cons"].items():
        fixed = []
        for c in lst:
            old_si = c[2]
            if old_si in REMOVE:
                # This consume was on a removed step — drop it
                print(f"  cons[{fl}]: dropping entry {c} (step {old_si} removed)")
                continue
            c2 = list(c)
            c2[2] = old_to_new.get(old_si, old_si)
            fixed.append(c2)
        d["cons"][fl] = fixed

# Fix dyn: {floor: [[x,y,stepIdx,objId],...]}
if isinstance(d.get("dyn"), dict):
    for fl, lst in d["dyn"].items():
        fixed = []
        for c in lst:
            old_si = c[2]
            if old_si in REMOVE:
                print(f"  dyn[{fl}]: dropping entry {c} (step {old_si} removed)")
                continue
            c2 = list(c)
            c2[2] = old_to_new.get(old_si, old_si)
            fixed.append(c2)
        d["dyn"][fl] = fixed

# Update floors: recompute steps count and path
if isinstance(d.get("floors"), dict):
    for fl_key, fl_data in d["floors"].items():
        fl = int(fl_key)
        # Count steps on this floor (by .f field)
        fl_steps = [x for x in new_steps if x["f"] == fl]
        old_count = fl_data.get("steps", 0)
        fl_data["steps"] = len(fl_steps)
        if old_count != fl_data["steps"]:
            print(f"  floors[{fl}].steps: {old_count} -> {fl_data['steps']}")

        # Rebuild path from steps (x,y pairs)
        path = []
        for x in fl_steps:
            pos = (x["x"], x["y"])
            if not path or path[-1] != list(pos):
                path.append(list(pos))
        fl_data["path"] = path

# Update total
old_total = d["total"]["steps"]
d["total"]["steps"] = len(new_steps)
print(f"total.steps: {old_total} -> {d['total']['steps']}")

# Save
json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"Saved {OUT} ({len(new_steps)} steps)")

# Verify: spot check
print("\n--- Verification ---")
for check_i in [1029, 1030 if 1030 not in REMOVE else 1078, 3881, 3882 if 3882 not in REMOVE else 3902]:
    ni = old_to_new.get(check_i)
    if ni:
        x = next(s for s in new_steps if s["i"] == ni)
        print(f"  old step {check_i} -> new step {ni}: f{x['f']} ({x['x']},{x['y']})")
