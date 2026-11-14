"""Scan merged_route_full.json for all idle closed loops."""
import json, sys

d = json.load(open("merged_route_full.json", encoding="utf-8"))
s = d["steps"]
N = len(s)

def sig(x):
    return (x.get("f"), x.get("hp"), x.get("a"), x.get("df"), x.get("g"),
            x.get("ky"), x.get("kb"), x.get("kr"), tuple(x.get("it", [])))

# Single pass: track "last visit to (floor,x,y) with same state sig"
# Build run segments: consecutive steps with no event, no item change, no stat change
runs = []  # (start_idx, end_idx) inclusive, maximal idle run
i = 0
while i < N:
    if s[i].get("e") or s[i].get("it"):
        i += 1
        continue
    sig0 = sig(s[i])
    j = i + 1
    while j < N and not s[j].get("e") and not s[j].get("it") and sig(s[j]) == sig0:
        j += 1
    runs.append((i, j - 1))  # j-1 = last idle step
    i = j

# Within each run, find closed loops: start_pos == some later pos in run
loops = []
for (a, b) in runs:
    if b - a < 3:
        continue
    # Find maximal closed sub-loops within this run
    pos_seen = {}  # (x,y) -> first index in run
    k = a
    while k <= b:
        pos = (s[k]["x"], s[k]["y"])
        if pos in pos_seen:
            start_k = pos_seen[pos]
            loop_len = k - start_k + 1
            if loop_len >= 4:  # at least 4 steps forming a loop
                loops.append((s[start_k]["i"], s[k]["i"], s[start_k]["f"], loop_len, pos))
                # Don't advance past k; reset pos_seen from k
                pos_seen = {}
                pos_seen[pos] = k
            # else: small loop (back-and-forth), skip
        else:
            pos_seen[pos] = k
        k += 1

print(f"Found {len(loops)} idle loops (>=4 steps):")
total_saved = 0
for l in loops:
    saved = l[3] - 1  # remove all but the return step
    total_saved += saved
    print(f"  steps {l[0]}-{l[1]} (floor {l[2]}, {l[3]} steps, save {saved}, returns to {l[4]})")
print(f"Total steps to remove: {total_saved}")
print(f"Current total: {d['total']['steps']}, after: {d['total']['steps'] - total_saved}")
