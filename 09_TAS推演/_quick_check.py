import json
d = json.load(open("merged_route_full.json", encoding="utf-8"))
s = d['steps']
print("1F steps:", sum(1 for x in s if x['f']==1))
print("27F steps:", sum(1 for x in s if x['f']==27))
# Quick: find long idle runs on 1F using 'l' field
f1 = [(i, x) for i, x in enumerate(s) if x['f']==1]
runs = []
i = 0
while i < len(f1):
    idx, x = f1[i]
    if x.get('l') or x.get('e'):
        i += 1; continue
    j = i+1
    while j < len(f1):
        _, y = f1[j]
        if y.get('l') or y.get('e'): break
        if (y['hp'],y['a'],y['df'],y['g']) != (x['hp'],x['a'],x['df'],x['g']): break
        j += 1
    if j - i >= 10:
        runs.append((f1[i][1]['i'], f1[j-1][1]['i'], j-i))
    i = j
print("1F idle runs >=10:", runs)
f27 = [x for x in s if x['f']==27]
print("27F positions:", [(x['i'], x['x'], x['y']) for x in f27])
