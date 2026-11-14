"""Scan merged_route_full.json for ALL idle detours (not just closed loops).
An idle detour = a maximal run of consecutive steps with no event, no item change,
no stat change, where the hero leaves a position and returns to it (or passes through
a previously visited position on the same floor with same state).

Also detect "redundant A-B-A back-and-forth" and "redundant rectangular loops".
"""
import json

d = json.load(open("merged_route_full.json", encoding="utf-8"))
s = d["steps"]
N = len(s)

def sig(x):
    return (x.get("f"), x.get("hp"), x.get("a"), x.get("df"), x.get("g"),
            x.get("ky"), x.get("kb"), x.get("kr"), tuple(x.get("it", [])))

# Find maximal idle runs (consecutive steps with no event/item/stat change)
runs = []
i = 0
while i < N:
    if s[i].get("e") or s[i].get("it"):
        i += 1
        continue
    sig0 = sig(s[i])
    j = i + 1
    while j < N and not s[j].get("e") and not s[j].get("it") and sig(s[j]) == sig0:
        j += 1
    if j - i >= 3:  # at least 3 idle steps
        runs.append((i, j - 1))
    i = j

print(f"Found {len(runs)} idle runs (>=3 steps):")
for (a, b) in runs:
    fl = s[a]["f"]
    positions = [(s[k]["x"], s[k]["y"]) for k in range(a, b+1)]
    start = positions[0]
    end = positions[-1]
    loop_closed = start == end
    # Find first position that repeats (indicating a detour)
    pos_first = {}
    detour_info = None
    for k, p in enumerate(positions):
        if p in pos_first:
            detour_info = (pos_first[p], k, p)
            break
        pos_first[p] = k

    length = b - a + 1
    print(f"  steps {s[a]['i']}-{s[b]['i']} (floor {fl}, {length} steps, "
          f"start={start} end={end}, closed={loop_closed}")
    if detour_info:
        dk = detour_info
        print(f"    first repeat: pos {dk[2]} first at step {s[a+dk[0]]['i']}, "
              f"repeated at step {s[a+dk[1]]['i']}, detour={dk[1]-dk[0]} steps")
    # Print full position trace for runs >= 10
    if length >= 10:
        print(f"    trace: {positions}")
