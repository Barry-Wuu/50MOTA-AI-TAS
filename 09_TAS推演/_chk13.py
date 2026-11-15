import json, sys
d = json.load(open('merged_route_full.json', encoding='utf-8'))
steps = d['steps'] if isinstance(d, dict) and 'steps' in d else d
print('total', len(steps))
segs = []
cur = None
for s in steps:
    f = s['f']
    if segs and segs[-1][0] == f:
        segs[-1][2] = s['i']
    else:
        segs.append([f, s['i'], s['i']])
for f, a, b in segs:
    if f in (11, 12, 13, 14) and a <= 2760:
        print('F%02d i %d-%d len %d' % (f, a, b, b - a + 1))
print('---- 13F only ----')
for s in steps:
    if s['f'] == 13 and s['i'] <= 6800:
        print(s['i'], (s['x'], s['y']), s.get('l', ''), '|', s.get('e', ''))