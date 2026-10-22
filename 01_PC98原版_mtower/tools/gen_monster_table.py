"""从 magic_tower1_monsters.csv + magic_tower1_entities.csv 重建 README 的「怪物战力表」。

用法：python3 tools/gen_monster_table.py        （只重写表体与表下那行注，不动其他章节）
规则（与 README 现况一致）：
  - 列：怪物译名 / 怪物原名 / HP / ATK / DEF / GOLD，不含内部 id；
  - 同名合并成一行（目前只有「大乌贼」——原版把一只拆成中央+八块躯体，四维相同、GOLD 中央 100 躯体 50）；
  - 原名去掉「の一部」并把全角空格归一；
  - 排序 = 各怪首次出现层，其次 HP。
"""
import csv, collections, os, re, sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(D, 'magic_tower1_monsters.csv'), encoding='utf8')))
ent = list(csv.DictReader(open(os.path.join(D, 'magic_tower1_entities.csv'), encoding='utf8')))
first = {}
for e in ent:
    try: f = int(e['floor'])
    except ValueError: continue
    if e['obj'] not in first or f < first[e['obj']]: first[e['obj']] = f
mons = [r for r in rows if r['role'] == 'monster']
for m in mons:
    m['jp'] = m['name_jp'].replace('\u3000', '').replace('の一部', '')
grp = collections.OrderedDict()
for m in sorted(mons, key=lambda m: (first.get(m['id'], 99), int(m['hp']), int(m['id']))):
    grp.setdefault(m['name_cn'], []).append(m)
tbl = ['| 怪物译名 | 怪物原名 | HP | ATK | DEF | GOLD |', '|---|---|---:|---:|---:|---:|']
for k, ms in grp.items():
    stat = collections.Counter((m['hp'], m['atk'], m['dfn']) for m in ms).most_common(1)[0][0]
    cand = [m for m in ms if (m['hp'], m['atk'], m['dfn']) == stat]
    gold = ([m for m in cand if m['id'] == '71'] or cand)[0]['gold']
    jps = list(dict.fromkeys(m['jp'] for m in ms))
    tbl.append('| {} | {} | {} | {} | {} | {} |'.format(k, ' / '.join(jps), *stat, gold))
body = '\n'.join(tbl) + '\n\n> 注：这一行同时是 **49F 与 50F 的 BOSS**（引擎运行时放置，见下方「提醒」）；表内数值为封印前。' \
    if False else '\n'.join(tbl)
p = os.path.join(D, 'README.md'); s = open(p, encoding='utf8').read()
i0 = s.index('| 怪物译名 | 怪物原名 |')
i1 = s.index('\n\n> 注：', i0) if '\n\n> 注：' in s[i0:i0+6000] else s.index('\n\n### ', i0)
new = s[:i0] + body + s[i1:]
open(p, 'w', encoding='utf8').write(new)
print('表体重建：', len(grp), '行（同名合并后）')
