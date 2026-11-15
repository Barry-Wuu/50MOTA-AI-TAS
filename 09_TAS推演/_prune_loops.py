"""自动剪除所有空闲闭环（idle loop）。

判据（全部满足）：
  1. 同一层内连续 step
  2. 无 l（日志）、无 e（事件）
  3. HP/ATK/DEF/GOLD/钥匙 全部不变
  4. 段首位置 == 段尾位置（闭环）
  5. 长度 >= 6

剪除规则：删掉闭环内除首步外的全部步（首步保留 = 已在该格）。
这样前后衔接天然成立（后一步从同一格继续）。

用 pickle 保存旧步号 -> 新步号映射，供 cons/dyn 修引用。
"""
import json, copy, sys

INP = OUT = sys.argv[1] if len(sys.argv) > 1 else "merged_route_full.json"
d = json.load(open(INP, encoding="utf-8"))
s = d["steps"]

def sig(x):
    return (x.get("f"), x.get("hp"), x.get("a"), x.get("df"), x.get("g"),
            x.get("ky"), x.get("kb"), x.get("kr"))

REMOVE = set()
loops = []

i = 0
n = len(s)
while i < n:
    x = s[i]
    if x.get("l") or x.get("e"):
        i += 1
        continue
    start = sig(x)
    pos0 = (x["f"], x["x"], x["y"])
    # 找同层、同状态、回到同格的最近点
    j = i + 1
    hit = None
    while j < n:
        y = s[j]
        if y.get("l") or y.get("e"):
            break
        if sig(y) != start:
            break
        if (y["f"], y["x"], y["y"]) == pos0 and (j - i) >= 6:
            hit = j
            break
        j += 1
    if hit is None:
        i += 1
        continue
    # 闭环：删除 i+1 .. hit-1（保留 i 和 hit 中的 hit 作为到达步也行）
    # 更优：保留 i（起点），删除 i+1..hit 全部（hit 与 i 同格，重复）
    for k in range(i + 1, hit + 1):
        REMOVE.add(s[k]["i"])
    loops.append((s[i]["i"], s[hit]["i"], s[i]["f"], hit - i,
                  (s[i]["x"], s[i]["y"]), (s[hit]["x"], s[hit]["y"])))
    i = hit + 1

print(f"Found {len(loops)} idle closed loops:")
for lp in loops:
    print(f"  {lp[2]}F steps {lp[0]}-{lp[1]}  len={lp[3]}  pos={lp[4]}->{lp[5]}")
print(f"Steps to remove: {len(REMOVE)}")

if not REMOVE:
    print("nothing to do")
    sys.exit(0)

# 校验：被删步无事件/无属性变化/无日志
bad = [x for x in s if x["i"] in REMOVE and (x.get("l") or x.get("e") or x.get("dh") or x.get("da") or x.get("dd") or x.get("dg"))]
if bad:
    print(f"ERROR: {len(bad)} removal targets have events/log/stat-delta:")
    for b in bad[:10]:
        print(f"  step {b['i']} f{b['f']} l={b.get('l')!r} e={b.get('e')!r} dh={b.get('dh')} dg={b.get('dg')}")
    sys.exit(1)

# 映射
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

# 邻接校验（每个被剪段的接缝）
for lp in loops:
    prev_i = lp[0]
    next_i = lp[1] + 1
    a = next((z for z in s if z["i"] == prev_i), None)
    b = next((z for z in s if z["i"] == next_i), None)
    if a and b and a["f"] == b["f"]:
        dist = abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])
        flag = "OK" if dist == 1 else f"!! dist={dist}"
        print(f"  seam {prev_i}->{next_i}: {a['f']}F({a['x']},{a['y']})->({b['x']},{b['y']}) {flag}")

d["steps"] = new_steps

# 修 cons/dyn 引用
for key in ("cons", "dyn"):
    if isinstance(d.get(key), dict):
        for fl, lst in d[key].items():
            fixed = []
            for c in lst:
                if c[2] in REMOVE:
                    print(f"  {key}[{fl}]: drop {c}")
                    continue
                c2 = list(c)
                c2[2] = old_to_new.get(c[2], c[2])
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
print(f"total.steps: {old_total} -> {d['total']['steps']}")

json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"saved {OUT}")