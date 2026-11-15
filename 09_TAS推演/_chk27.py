import json
d = json.load(open('merged_route_full.json', encoding='utf-8'))
s = d['steps']
# 找 27F 的 (6,1) 往返段
seg = [x for x in s if x['f'] == 27]
print('27F steps', len(seg), 'first i', seg[0]['i'], 'last i', seg[-1]['i'])
for x in seg:
    print(x['i'], (x['x'], x['y']), x.get('l', ''), '|', x.get('e', ''))