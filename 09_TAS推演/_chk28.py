import json, re, io, csv
d = json.load(open('merged_route_full.json', encoding='utf-8'))
s = d['steps']
print('--- 28F 步骤标签 ---')
for x in s:
    if x['f'] == 28:
        print(x['i'], (x['x'], x['y']), repr(x.get('l', '')), '|', repr(x.get('e', '')))

# NPC_DLG 块：从 data.js 里抠出来看有没有 28
try:
    txt = io.open('toy_final/data.js', encoding='utf-8').read()
    m = re.search(r'NPC_DLG\s*=\s*(\{.*?\});', txt, re.S)
    print('\n--- data.js NPC_DLG 命中:', bool(m))
    if m:
        obj = json.loads(m.group(1))
        print('键:', list(obj.keys()))
        for k, v in obj.items():
            fs = [l['f'] for l in v.get('lines', [])]
            print(' ', k, '楼层集合:', sorted(set(fs)))
except Exception as e:
    print('data.js 读取失败', e)