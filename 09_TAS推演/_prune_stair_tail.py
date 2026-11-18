"""剪除「贴梯后又走空步才 fly/stair」的冗余步。

判据（全部满足）：
  1. 触发步 t 是 fly（l 含"飞行之珠传送"）或 stair（l 含"楼梯 →"）
  2. 从 t-1 往前回溯的连续同层空步段（无 l、无 e）里
  3. 段内最早贴梯格 a 与最晚贴梯格 b 贴的是【同一个梯】
  4. b - a >= 2（中间至少 2 步纯走位）
删除 a+1 .. b（保留 a 作为停靠点）：fly 只需贴梯、落点固定；
stair 从最近邻格踏上、落点也固定 —— 故从 a 触发与从 b 触发完全等价。

安全保护：
  · 被删步无 l/e 且属性增量 dh/da/dd/dg 全 0（空步）
  · 被删步的 i 不出现在 cons/dyn 的 step 引用里（否则有隐藏状态变化，跳过）
  · 接缝校验：a 与 trigger 前一格的关系由 fly/stair 本身保证（贴梯）

沿用 _prune_loops.py 的 old->new 步号重映射，同步修 cons/dyn/floors/total。
"""
import json, copy, sys, os

INP = OUT = sys.argv[1] if len(sys.argv) > 1 else "merged_route_full.json"
d = json.load(open(INP, encoding="utf-8"))
s = d["steps"]

# mota_core 提供 STAIRS 表
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "01_PC98原版_mtower", "tools")))
import mota_core as M


def stair_cells(f, x, y):
    st = M.STAIRS.get(f) or ()
    out = []
    for c in st:
        if c and abs(c[0] - x) + abs(c[1] - y) == 1:
            out.append(tuple(c))
    return out


def ev(x):
    return bool(x.get("l")) or bool(x.get("e"))


# cons/dyn 引用的步号集合（保护：被删步不得参与任何状态变化引用）
refsteps = set()
for key in ("cons", "dyn"):
    for fl, lst in (d.get(key) or {}).items():
        for c in lst:
            try:
                refsteps.add(int(c[2]))
            except Exception:
                pass

REMOVE = set()
segs = []
skipped = []
for t, x in enumerate(s):
    lg = x.get("l", "") or ""
    if ("飞行之珠传送" not in lg) and ("楼梯 →" not in lg):
        continue
    if t == 0:
        continue
    f = s[t - 1]["f"]
    # 回溯尾部连续同层空步段
    j = t - 1
    seg = []
    while j >= 0 and s[j]["f"] == f and not ev(s[j]):
        seg.append(s[j])
        j -= 1
    seg = seg[::-1]
    if len(seg) < 3:
        continue
    ws = [(k, stair_cells(f, ss["x"], ss["y"])) for k, ss in enumerate(seg)
          if stair_cells(f, ss["x"], ss["y"])]
    if len(ws) < 2:
        continue
    a, ca = ws[0]
    b, cb = ws[-1]
    common = set(ca) & set(cb)
    if not common or (b - a) < 2:
        continue
    todel = [seg[k]["i"] for k in range(a + 1, b + 1)]
    # 保护1：无属性变化
    bad = [s[k] for k in range(a + 1, b + 1)
           if s[k].get("dh") or s[k].get("da") or s[k].get("dd") or s[k].get("dg")]
    if bad:
        skipped.append((t, f, "stat-delta"))
        continue
    # 保护2：不被 cons/dyn 引用
    if any(ii in refsteps for ii in todel):
        skipped.append((t, f, "cons/dyn-ref"))
        continue
    # 保护3：不与已删集合重叠
    if REMOVE & set(todel):
        skipped.append((t, f, "overlap"))
        continue
    REMOVE.update(todel)
    segs.append((seg[a]["i"], seg[b]["i"], f, b - a,
                 (seg[a]["x"], seg[a]["y"]), (seg[b]["x"], seg[b]["y"]), sorted(common)))

print("Found %d stair-tail redundancies:" % len(segs))
for sg in segs:
    print("  %dF steps %d-%d len=%d pos=%s->%s stair=%s" % (
        sg[2], sg[0], sg[1], sg[3], sg[4], sg[5], sg[6]))
print("Skipped:", skipped)
print("Steps to remove:", len(REMOVE))

if not REMOVE:
    print("nothing to do")
    sys.exit(0)

# 重映射
old_to_new = {}
new_i = 0
for x in s:
    if x["i"] in REMOVE:
        continue
    new_i += 1
    old_to_new[x["i"]] = new_i

new_steps = []
for x in s:
    if x["i"] in REMOVE:
        continue
    x2 = copy.deepcopy(x)
    x2["i"] = old_to_new[x["i"]]
    new_steps.append(x2)

# 接缝校验：保留停靠步 a 与触发步 t 之间，a 必须贴同一个梯
for (ai, bi, f, ln, pa, pb, common) in segs:
    a_step = next((z for z in new_steps if z["i"] == old_to_new[ai]), None)
    if a_step and abs(a_step["x"] - common[0][0]) + abs(a_step["y"] - common[0][1]) != 1:
        print("  !! seam check FAIL step a=%d" % ai)
        sys.exit(1)

d["steps"] = new_steps

# 修 cons/dyn 引用
for key in ("cons", "dyn"):
    if isinstance(d.get(key), dict):
        for fl, lst in d[key].items():
            fixed = []
            for c in lst:
                if int(c[2]) in REMOVE:
                    print("  %s[%s]: drop %s" % (key, fl, c))
                    continue
                c2 = list(c)
                c2[2] = old_to_new.get(int(c[2]), c[2])
                fixed.append(c2)
            d[key][fl] = fixed

# 重算 floors
for fl_key, fl_data in d.get("floors", {}).items():
    fl = int(fl_key)
    fl_steps = [x for x in new_steps if x["f"] == fl]
    fl_data["steps"] = len(fl_steps)
    path = []
    for x in fl_steps:
        p = [x["x"], x["y"]]
        if not path or path[-1] != p:
            path.append(p)
    fl_data["path"] = path

old_total = d["total"]["steps"]
d["total"]["steps"] = len(new_steps)
print("total.steps: %d -> %d" % (old_total, d["total"]["steps"]))

json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("saved", OUT)
