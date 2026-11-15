import json
d = json.load(open('merged_route_full.json', encoding='utf-8'))
s = d['steps']


def empty(x):
    return (not x.get('e')) and not (x.get('dh') or x.get('da') or x.get('dd') or x.get('dg'))


segs = []
cur = None
for x in s:
    if cur and cur['f'] == x['f']:
        cur['b'] = x['i']; cur['n'] += 1
        if not empty(x):
            cur['busy'] += 1
    else:
        cur = {'f': x['f'], 'a': x['i'], 'b': x['i'], 'n': 1, 'busy': 0 if empty(x) else 1}
        segs.append(cur)
print('纯过路段（长度>=8，无任何事件/属性变化）：')
for g in segs:
    if g['n'] >= 8 and g['busy'] == 0:
        a = next(z for z in s if z['i'] == g['a'])
        b = next(z for z in s if z['i'] == g['b'])
        print('  F%02d  i%d-%d  len%-3d  (%d,%d)->(%d,%d)' % (g['f'], g['a'], g['b'], g['n'], a['x'], a['y'], b['x'], b['y']))
print()
print('分段总览（len>=8）：')
for g in segs:
    if g['n'] >= 8:
        print('  F%02d i%d-%d len%-3d busy%d' % (g['f'], g['a'], g['b'], g['n'], g['busy']))