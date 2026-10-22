"""把两只运行时放置的魔王登记进数据与渲染表。

依据（均为 MTower.class 指令流事实）：
  - public void Zeno(Graphics,int,int) / Zeno2(...) 方法体内含 `... bipush 57; castore; displayCharacter(...)`
  - 调用点：eventMT 中 `bipush 110; bipush 55; invokevirtual Zeno`  → 49F (x=6,y=3)
                eventMT 中 `bipush 123; bipush 57; invokevirtual Zeno2` → 50F (x=6,y=5)
    （参数为大表 col/row：x=col-13*(col//13)，y=row-13*(row//13)，层号=13*(row//13)//13*10+col//13+1）
  - objectAttribute[57] = 8000/5000/1000/500；封印后 eventMT 改写为 800/500/100
"""输入：<大表根目录>（含 crops/live.json、javamap.json、dynamic_canonical.json），
     会改写本目录的 magic_tower1_map_50f.json 与 dynamic_canonical.json。
用法：python3 tools/register_boss.py ../..
"""
import json, os, sys

A = sys.argv[1]
D = A + '/r/01_PC98原版_mtower'
live = json.load(open(A + '/crops/live.json'))
mp, mo, ma, oa = live['map'], live['mapObject'], live['mapAttribute'], live['objectAttribute']
SMX = json.load(open(A + '/javamap.json'))['strMessage']
BOSS = 57
PLACES = [('49', 6, 3, 'Zeno', 110, 55), ('50', 6, 5, 'Zeno2', 123, 57)]

def sheet(fl, x, y):
    if fl == '0F':
        return 5 * 13 + y, 1 * 13 + x
    f = int(fl)
    return (f - 1) // 10 * 13 + y, (f - 1) % 10 * 13 + x

can = json.load(open(A + '/dynamic_canonical.json'))
for fl, x, y, mth, col, row in PLACES:
    R, C = sheet(fl, x, y)
    assert (row, col) == (R, C), (fl, x, y, (R, C), (row, col))   # 换算与调用点常量必须一致
    cur, t = mo[R][C], mp[R][C]
    ent = {
        'floor': fl, 'x': x, 'y': y, 'draw_obj': BOSS,
        'variants': [{'obj': BOSS, 'type': 'MONSTER',
                      'name_jp': (SMX['1'].get(str(oa[BOSS][5])) or '').replace('\n', ' '),
                      'method': mth}],
        'cell_now': {'terrain': t, 'terrain_kind': ma[t][3], 'object': cur,
                     'object_type': '空' if not cur else '?'},
        'note': mth + '(Graphics,col,row) 运行时放置；大表坐标 (' + str(col) + ',' + str(row) + ')',
    }
    can['objects'] = [o for o in can['objects'] if not (o['floor'] == fl and o['x'] == x and o['y'] == y)] + [ent]
can['objects'].sort(key=lambda o: (len(o['floor']), o['floor'], o['x'], o['y']))
json.dump(can, open(A + '/dynamic_canonical.json', 'w'), ensure_ascii=False)

d = json.load(open(D + '/magic_tower1_map_50f.json'))
for fl, x, y, mth, col, row in PLACES:
    d[fl]['runtime_boss'] = [{
        'x': x, 'y': y, 'obj': BOSS, 'placed_by': mth + '(Graphics,col,row)',
        'big_table_coord': [col, row],
        'stats': oa[BOSS][10:14],
        'after_seal': [800, 500, 100, oa[BOSS][13]],
    }]
d['_dynamic_spawns']['runtime_placed_bosses'] = {
    'obj': BOSS, 'name_jp': (SMX['1'].get(str(oa[BOSS][5])) or ''), 'stats': oa[BOSS][10:14],
    'cells': [{'floor': f, 'x': x, 'y': y, 'placed_by': m + '(g,' + str(c) + ',' + str(r) + ')'}
              for f, x, y, m, c, r in PLACES],
    'seal': '完成“骰子五点”封印后 eventMT 执行 objectAttribute[57][10]=800 / [11]=500 / [12]=100（原值的 1/10）',
    'proof': 'Zeno/Zeno2 方法体内为 `... bipush 57; castore; displayCharacter(...)`；两个调用点的常量参数即大表 col/row',
    'note': '静态 map/mapObject 数组里这两格都是空的，图鉴块也只有这一行魔王数据；'
            'class 内不存在 ATK 1580 / DEF 190 的对象（该常量 0 次出现），'
            '故百科表“魔王(50层) 8000/1580/190/50”不属于本版数据。',
}
json.dump(d, open(D + '/magic_tower1_map_50f.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('登记完成：49F(6,3) Zeno / 50F(6,5) Zeno2；坐标换算断言全部通过')
