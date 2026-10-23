"""重建 mota_core 的数据依赖：
  tools/crops/live.json   = {map, mapObject, mapAttribute, objectAttribute}
  tools/javamap.json      = {strMessage: {0:EN, 1:JP}}

来源：
  1) 01_PC98原版_mtower/magic_tower1_rows.csv  -> 78x130 大表（50 层 + 00 层）
  2) 08_Java_MTower08a/game/MTower.class 的 javap -c 输出 -> 属性表常量赋值
  3) 01_PC98原版_mtower/magic_tower1_texts.csv -> strMessage
"""
import csv, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CLASS = os.path.join(os.path.dirname(ROOT), '08_Java_MTower08a', 'game', 'MTower.class')
ROWS = os.path.join(ROOT, 'magic_tower1_rows.csv')
TEXTS = os.path.join(ROOT, 'magic_tower1_texts.csv')

# ---------- 1) 大表 ----------
def build_tables():
    MAP = [[0]*130 for _ in range(78)]
    OBJ = [[0]*130 for _ in range(78)]
    seen = {}
    for r in csv.DictReader(open(ROWS, encoding='utf8')):
        b = r['block']
        y, x = int(r['y']), int(r['x'])
        if b == 'floor_0':
            band, slot = 5, 1
        elif b.isdigit():
            f = int(b)
            band, slot = (f-1)//10, (f-1)%10
        else:
            continue
        rr, cc = band*13 + y, slot*13 + x
        MAP[rr][cc] = int(r['terrain'])
        OBJ[rr][cc] = int(r['object'])
        seen[b] = seen.get(b, 0) + 1
    return MAP, OBJ, seen

# ---------- 2) 属性表（javap 常量赋值提取） ----------
def val(s):
    m = re.search(r'(?:bipush|sipush)\s+(-?\d+)', s)
    if m:
        return int(m.group(1))
    m = re.search(r'iconst_(\d)', s)
    if m:
        return int(m.group(1))
    m = re.search(r'iconst_m1', s)
    if m:
        return -1
    m = re.search(r'ldc(?:_w)?\s+#\d+\s+//\s*(?:int\s+)?(-?\d+)', s)
    if m:
        return int(m.group(1))
    return None

def javap():
    if not os.path.exists(CLASS):
        sys.exit('找不到 MTower.class: ' + CLASS)
    out = subprocess.run(['javap', '-c', '-p', CLASS], capture_output=True, text=True).stdout
    return out.split('\n')

def build_attrs(lines, field):
    """提取 `<field>[N][C] = V` 的常量赋值（N/C/V 均为立即数）"""
    tbl = {}
    for i in range(len(lines)-6):
        if field not in lines[i]:
            continue
        mm = re.search(r'(?:bipush|sipush)\s+(\d+)', lines[i+1])
        mi = re.search(r'iconst_(\d)', lines[i+1])
        if not (mm or mi) or 'aaload' not in lines[i+2]:
            continue
        n = int(mm.group(1)) if mm else int(mi.group(1))
        cv = val(lines[i+3])
        vv = val(lines[i+4])
        if cv is None or vv is None or 'iastore' not in lines[i+5]:
            continue
        tbl.setdefault(n, {})[cv] = vv
    # 补全为 200 x 40
    out = [[0]*40 for _ in range(200)]
    for n, d in tbl.items():
        if n < 200:
            for c, v in d.items():
                if 0 <= c < 40:
                    out[n][c] = v
    return out, tbl

# ---------- 3) strMessage ----------
def build_strmsg():
    jp, en = {}, {}
    for r in csv.DictReader(open(TEXTS, encoding='utf8')):
        k = r.get('strNumber')
        if not k or not k.strip().isdigit():
            continue
        k = int(k)
        if r.get('text_jp'):
            jp[str(k)] = r['text_jp']
        if r.get('text_en'):
            en[str(k)] = r['text_en']
    return {'0': en, '1': jp}

if __name__ == '__main__':
    MAP, OBJ, seen = build_tables()
    lines = javap()
    MA, ma_raw = build_attrs(lines, 'mapAttribute')
    OA, oa_raw = build_attrs(lines, 'objectAttribute')
    print('大表块数', len(seen), ' | mapAttribute 条目', len(ma_raw), ' objectAttribute 条目', len(oa_raw))
    os.makedirs(os.path.join(HERE, 'crops'), exist_ok=True)
    json.dump({'map': MAP, 'mapObject': OBJ, 'mapAttribute': MA, 'objectAttribute': OA},
              open(os.path.join(HERE, 'crops', 'live.json'), 'w'))
    json.dump({'strMessage': build_strmsg()}, open(os.path.join(HERE, 'javamap.json'), 'w'), ensure_ascii=False)
    print('写出 crops/live.json + javamap.json')
    # 抽查
    print('1F(1,1) terrain=', MAP[1][1], ' obj=', OBJ[1][1])
    print('mapAttribute[1]=', MA[1][:8])
    print('objectAttribute[8]=', OA[8][:14])
