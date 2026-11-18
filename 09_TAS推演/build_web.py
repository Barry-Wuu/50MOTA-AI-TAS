# -*- coding: utf-8 -*-
"""把 merged_route.json + 原著贴图渲染成一个自包含的交互式网页。
- 楼层底图：01_PC98原版_mtower/floors/floor_XX.png（原版美术，无损 WebP 内嵌）
- 勇者标记：mota_art/MTower.gif 顶行勇者帧（col3,row0）
输出：1F到31F_推演全过程.html
"""
import io, os, sys, json, base64, csv, re
from PIL import Image

DED = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/'
FLOORS_DIR = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/floors/'
FLOORS_ALT = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'   # 0F 底图在根目录
SHEET = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/mota_art/MTower.gif'
HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, '..', '01_PC98原版_mtower', 'magic_tower1_texts.csv')


def floor_png(f):
    """楼层底图路径：floors/floor_XX.png；0F 等缺失时回退到 01_PC98原版_mtower/floor_XX.png。"""
    p = FLOORS_DIR + 'floor_%02d.png' % f
    if os.path.exists(p):
        return p
    q = FLOORS_ALT + 'floor_%02d.png' % f
    return q if os.path.exists(q) else p


TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
import mota_core as M

# ---- 对话台词（Toy 悬停 tooltip）：数据驱动，不再手写"有台词的人"名单。
# 权威源（仓库既有文件）：
#  - magic_tower1_texts.md        ：按楼层整理的具名对话正文（X「…」），供 盗賊/魔王 Zeno/勇者/骑士队长/吸血鬼/大法师/骷髅队长
#  - magic_tower1_entities.csv    ：NPC/gate 实体权威格点坐标（含 老人/商人 等"无名「…」"NPC 与具名 盗賊/勇者）
#  - magic_tower1_texts.csv       ：obj → 中文译文 / 分组，用于把实体台词译成中文、并归类 商人 / 老人
# 角色分类：具名前缀 X「 → X；无名「…」按内容/分组归为 商人 / 老人。 ----
CANON_ZH = {'盗賊': '盗贼', '魔導師ゼノ': '魔王 Zeno', '勇者': '勇者', 'バンパイア': '吸血鬼',
            '大魔導師': '大法师', '金騎士': '骑士队长', 'スケルトンＡ': '骷髅队长'}
ROUTE_NAMES = {
    '盗賊':      ['盗賊', '盗贼'],
    '魔導師ゼノ':['魔導師ゼノ', '魔王 Zeno', '魔王（假魔王）', '魔王', '假魔王', '真魔王'],
    '勇者':      ['勇者'],
    'バンパイア':['バンパイア', '吸血鬼'],
    '大魔導師':  ['大魔導師', '大法师'],
    '金騎士':    ['金騎士', '骑士队长'],
    'スケルトンＡ':['スケルトンＡ', '骷髅队长'],
}
MD_PATH  = os.path.join(HERE, '..', '01_PC98原版_mtower', 'magic_tower1_texts.md')
CSV_PATH = os.path.join(HERE, '..', '01_PC98原版_mtower', 'magic_tower1_texts.csv')
ENT_PATH = os.path.join(HERE, '..', '01_PC98原版_mtower', 'magic_tower1_entities.csv')
MCH_GRP  = '商人 · 祭坛 · 积分石 · 智慧之戒问答'
# 商人判定：分组为 商人·祭坛，或台词含买卖/店铺/回血/超级镐 关键词（覆盖 obj161 等被误归"无名提示"者）
_MERCHANT_KW = ('売る', '買う', '回復してあげる', 'マトック', '店')


def _is_npc_entity(_r):
    """实体是否是「有台词的 NPC」。
    ✅ 2026-11-15：原来只认 role 含 NPC，漏掉 role=event 的台词 NPC——最典型是 28F(8,4) obj161
       「鍵１個を１００ＧＯＬＤで買うよ」（回收钥匙的商人），导致 28F 全层没有悬停 tooltip。
       补判据：role=event 但 name_jp 是「…」台词，同样算 NPC（道具/门的 event 台词不以「开头）。"""
    _role = _r.get('role') or ''
    if 'NPC' in _role:
        return True
    return _role.strip() == 'event' and (_r.get('name_jp') or '').startswith('「')

# 1) md 解析：具名说话者台词（按 JP 前缀）
_by_jp = {}
try:
    _md_lines = io.open(MD_PATH, encoding='utf-8').read().split('\n')
    _floor = None; _cur = None; _entries = []
    _JP_RE = re.compile(r'([^「\n]{1,14})「([^」]*)」')
    for _ln in _md_lines:
        _m = re.match(r'^###\s*(\d+)F', _ln)
        if _m:
            _floor = int(_m.group(1)); _cur = None; continue
        _m = re.match(r'^\*\*\[(\d+)\]\*\*', _ln)
        if _m:
            _cur = {'floor': _floor, 'jp': [], 'zh': None}; _entries.append(_cur); continue
        if _cur is None:
            continue
        if _ln.startswith('>'):
            _cur['jp'].append(_ln[1:].strip())
        elif _ln.startswith('译文：') or _ln.startswith('译文:'):
            _cur['zh'] = _ln.split('：', 1)[-1].split(':', 1)[-1].strip()
    for _e in _entries:
        if not _e['zh']:
            continue
        _jp = ''.join(_e['jp'])
        _mj = _JP_RE.search(_jp)
        if not _mj or _mj.group(1).strip() not in CANON_ZH:
            continue
        _sp = _mj.group(1).strip()
        _mz = _JP_RE.search(_e['zh'])
        _dz = _mz.group(2).strip() if _mz else _e['zh']
        _by_jp.setdefault(_sp, []).append((_e['floor'], _dz))
except Exception:
    pass

# 2) csv：obj → (中文译文, 分组)，供实体台词翻译 + 商人/老人归类
_OBJ_ZH = {}; _OBJ_GRP = {}
try:
    for _r in csv.DictReader(io.open(CSV_PATH, encoding='utf-8-sig')):
        _m = re.search(r'obj(\d+)', _r.get('referenced_by', '') or '')
        if _m:
            _o = int(_m.group(1))
            _OBJ_ZH.setdefault(_o, _r.get('text_zh', '') or '')
            _OBJ_GRP.setdefault(_o, _r.get('group', '') or '')
except Exception:
    pass

# 3) NPC_DLG：具名角色（md）+ 商人/老人（从实体台词按楼层归类）
NPC_DLG = {}
for _jp, _names in ROUTE_NAMES.items():
    _rec = {'jp': _jp, 'zh': CANON_ZH[_jp],
            'lines': [{'f': f, 'zh': z} for f, z in sorted(_by_jp.get(_jp, []))]}
    for _n in _names + [_jp, CANON_ZH[_jp]]:
        NPC_DLG.setdefault(_n, _rec)
# 商人 / 老人：遍历实体 NPC，按楼层聚合中文台词
_merch = {}; _old = {}
try:
    for _r in csv.DictReader(io.open(ENT_PATH, encoding='utf-8-sig')):
        if not _is_npc_entity(_r):
            continue
        _f = _r.get('floor')
        if _f in (None, 'catalog'):
            continue
        try:
            _fi = int(_f)
        except Exception:
            continue
        try:
            _obj = int(_r['obj']) if _r.get('obj') else -1
        except Exception:
            _obj = -1
        _zh = _OBJ_ZH.get(_obj, '')
        if not _zh:
            continue
        _nj = _r.get('name_jp') or ''
        _is_m = (_OBJ_GRP.get(_obj) == MCH_GRP) or any(k in _nj for k in _MERCHANT_KW)
        (_merch if _is_m else _old).setdefault(_fi, []).append(_zh)
except Exception:
    pass
NPC_DLG['商人'] = {'jp': '商人', 'zh': '商人',
                  'lines': [{'f': f, 'zh': z} for f in sorted(_merch) for z in _merch[f]]}
NPC_DLG['老人'] = {'jp': '老人', 'zh': '老人',
                  'lines': [{'f': f, 'zh': z} for f in sorted(_old) for z in _old[f]]}
NPC_DLG_JSON = json.dumps(NPC_DLG, ensure_ascii=False)
# 名称按长度降序，避免短名被长名前缀误匹配（如 假魔王 早于 魔王）
NPC_NAMES = sorted(NPC_DLG.keys(), key=len, reverse=True)
NPC_RE_SRC = '(' + '|'.join(re.escape(_n) for _n in NPC_NAMES) + ')(「)?'

import sys as _sys
DATA_F = _sys.argv[1] if len(_sys.argv) > 1 else 'merged_route_full.json'
OUT_HTML = _sys.argv[2] if len(_sys.argv) > 2 else '1F到50F_全塔通关.html'
MAXF = int(_sys.argv[3]) if len(_sys.argv) > 3 else 50
# 第 4 个参数 = 外链输出目录（Toy 等平台的入口 index.html 有 1MB 硬上限，
# 单文件内嵌版 3MB 会被 307000 拒；给目录则把图/data 拆成 assets/ + data.js）
SPLIT_DIR = _sys.argv[4] if len(_sys.argv) > 4 else None
ASSET_DIR = os.path.join(SPLIT_DIR, 'assets') if SPLIT_DIR else None
if SPLIT_DIR:
    os.makedirs(ASSET_DIR, exist_ok=True)
data = json.load(io.open(DED + DATA_F, encoding='utf-8'))

# 底图里烙死的原勇者：1F(6,11) 与 MTower.gif 正面帧逐像素完全一致（diff 0.00）。
# 路线第 1 步时勇者已在 (6,10)，所以该格从第一步起就应还原成地面（步序 -1 = 永远覆盖）。
data.setdefault('cons', {}).setdefault('1', []).insert(0, [6, 11, -1, 'f'])

# ---- 地图 NPC 标记：合并「路线 BOSS 标记」与「实体 NPC 标记（权威格点）」
# 实体 NPC 覆盖 老人/商人/盗賊/勇者 等全部有台词角色（magic_tower1_entities.csv）；
# 路线 BOSS 标记覆盖 吸血鬼/骑士队长/大法师/魔王 Zeno 等战斗对话 NPC（entities 不含的怪物 BOSS）；
# 同一格多角色合并到一个标记。 ----
_DISP_TO_JP = {}
for _jp, _names in ROUTE_NAMES.items():
    for _n in _names:
        _DISP_TO_JP.setdefault(_n, _jp)
_NM_RE = re.compile('(' + '|'.join(re.escape(_n) for _n in sorted(_DISP_TO_JP, key=len, reverse=True)) + ')')
_MARK_CELLS = {}
try:
    _steps = data.get('steps', [])
    for _s in _steps:
        _txt = ' '.join(str(_s.get(_k) or '') for _k in ('e', 'l', 'note', 'mm'))
        _f = _s.get('f'); _x = _s.get('x'); _y = _s.get('y')
        if _f is None or _x is None or _y is None:
            continue
        for _m in _NM_RE.finditer(_txt):
            _MARK_CELLS.setdefault((_f, _x, _y), set()).add(_DISP_TO_JP[_m.group(1)])
except Exception:
    pass
# 实体 NPC（authoritative）：覆盖 老人/商人/盗賊/勇者 等所有有台词角色
try:
    for _r in csv.DictReader(io.open(ENT_PATH, encoding='utf-8-sig')):
        if not _is_npc_entity(_r):
            continue
        _f = _r.get('floor')
        if _f in (None, 'catalog'):
            continue
        try:
            _fi = int(_f)
        except Exception:
            continue
        try:
            _x = int(_r['x']); _y = int(_r['y'])
        except Exception:
            continue
        try:
            _obj = int(_r['obj']) if _r.get('obj') else -1
        except Exception:
            _obj = -1
        _nj = _r.get('name_jp') or ''
        _mm = re.match(r'^([^「\n]{1,12})「', _nj)
        if _mm and _mm.group(1).strip() in CANON_ZH:
            _role = _mm.group(1).strip()          # 盗賊 / 勇者（具名实体）
        else:
            _is_m = (_OBJ_GRP.get(_obj) == MCH_GRP) or any(k in _nj for k in _MERCHANT_KW)
            _role = '商人' if _is_m else '老人'
        _MARK_CELLS.setdefault((_fi, _x, _y), set()).add(_role)
except Exception:
    pass
NPC_MARKS = {}
for (_f, _x, _y), _set in _MARK_CELLS.items():
    NPC_MARKS.setdefault(_f, []).append({'x': _x, 'y': _y, 'n': sorted(_set)})
NPC_MARKS_JSON = json.dumps(NPC_MARKS, ensure_ascii=False)

js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def data_uri(img, **kw):
    b = io.BytesIO()
    img.save(b, 'WEBP', **kw)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


def emit(img, name):
    """内嵌模式 → data URI；外链模式 → 写 assets/<name>.webp 并返回相对路径。"""
    if SPLIT_DIR:
        img.save(os.path.join(ASSET_DIR, name + '.webp'), 'WEBP', lossless=True, method=6)
        return './assets/' + name + '.webp'
    return data_uri(img, lossless=True)


imgs = {}
for f in sorted(int(k) for k in data['floors']):
    p = floor_png(f)
    if os.path.exists(p):
        imgs[str(f)] = emit(Image.open(p).convert('RGBA'), 'f%02d' % f)


# ---- 每层的"地板贴图"：从该层纯地板格（地形0且无物件）里取最接近中位样板的一格 ----
import numpy as np


def floor_tile(f):
    fl = data['floors'][str(f)]
    ter, objs = fl['terrain'], fl['objs']
    # ⚠️ 2026-11-15 修 bug：这里的 ter 是**运行时最终口径**（破墙/暗墙/秘道都已生效），
    #   而底图 floor_XX.png 是**静态（未改动）**的。37F 被超级镐破掉 45 格墙后，
    #   这 45 格 ter==0 会被当成"纯地板"候选，可它们在底图上仍是**咖啡色墙砖**
    #   （PC-98 贴图：terrain=1 平均 RGB(139,88,56) 咖啡色，terrain=0 是深灰(108,99,101)），
    #   取中位样板时命中墙砖 → 拿去覆盖破墙格，覆盖完**还是墙**。
    #   ⇒ 剔除 dyn 里地形被改过的格，只从"底图上本来就是地板"的格里取样。
    tchg = {(d[0], d[1]) for d in (data.get('dyn') or {}).get(str(f), [])
            if isinstance(d[3], str) and d[3][:1] == 'T'}
    cands = [(x, y) for y in range(13) for x in range(13)
             if ter[y][x] == 0 and ('%d,%d' % (x, y)) not in objs
             and (x, y) not in tchg]
    if not cands:
        cands = [(x, y) for y in range(13) for x in range(13)
                 if ter[y][x] == 0 and (x, y) not in tchg]
    if not cands:
        cands = [(x, y) for y in range(13) for x in range(13) if ter[y][x] == 0]
    im = Image.open(floor_png(f)).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    tiles = np.stack([a[y * 40:y * 40 + 40, x * 40:x * 40 + 40] for x, y in cands])
    med = np.median(tiles, axis=0)
    diffs = np.abs(tiles - med).mean(axis=(1, 2, 3))
    best = int(np.argmin(diffs))
    return Image.fromarray(tiles[best].astype(np.uint8))


tiles = {}
for f in sorted(int(k) for k in data['floors']):
    if not os.path.exists(floor_png(f)):
        continue
    try:
        tiles[str(f)] = emit(floor_tile(f), 't%02d' % f)
    except Exception:
        pass
tile_js = json.dumps(tiles, ensure_ascii=False, separators=(',', ':'))

sheet = Image.open(SHEET).convert('RGBA')
# 顶行 40×40 勇者帧（c0 黑底、c1 空，角色从 c2 起）：c2 背面=上，c4 正面=下，c6 朝左，c8 朝右
HERO_COL = {'↑': 2, '↓': 4, '←': 6, '→': 8}
hero_js = json.dumps({k: emit(sheet.crop((c * 40, 0, c * 40 + 40, 40)), 'hero%d' % i)
                      for i, (k, c) in enumerate(HERO_COL.items())}, ensure_ascii=False)

# 楼梯贴图（与 11F(11,11) 静态上梯格逐像素一致，diff 0.00）：上行 (280,160)、下行 (320,160)
STAIR_XY = {'u': (280, 160), 'd': (320, 160)}
stair_js = json.dumps({k: emit(sheet.crop((x, y, x + 40, y + 40)), 'stair_' + k)
                       for k, (x, y) in STAIR_XY.items()}, ensure_ascii=False)

# ---- 道具图标：从贴图集按 Java 权威坐标裁剪（col=OA[obj][6]//40, row=OA[obj][7]//40，40px/格）----
# 权威来源：08_Java_MTower08a/decompiled/MTower.java CropImageFilter(objectAttribute[n3][6],[7],40,40)
# 与 mota_core.OA 读取一致，且已逐格掩码复核 diff=0（2026-11 定稿）。
ITEM_OBJS = [25, 26, 39, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114]
_item = {}
for _o in ITEM_OBJS:
    try:
        _c, _r = M.OA[_o][6] // 40, M.OA[_o][7] // 40
        _item[str(_o)] = emit(sheet.crop((_c * 40, _r * 40, _c * 40 + 40, _r * 40 + 40)), 'item%03d' % _o)
    except Exception:
        _item[str(_o)] = ''
item_js = json.dumps(_item, ensure_ascii=False, separators=(',', ':'))

img_js = json.dumps(imgs, ensure_ascii=False, separators=(',', ':'))

HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>魔塔1 · 1F→50F 全塔通关逐格校验（z2_route · 剩余怪伤害）</title>
<style>
:root{
  --bg:#0d1017; --panel:#161a24; --panel2:#1c2130; --line:#293040;
  --txt:#dfe6f2; --dim:#8b97ad; --accent:#4cc9f0; --gold:#f5c542;
  --red:#ff5d5d; --green:#3ecf8e; --blue:#4d8dff; --purple:#b07cff; --orange:#ff9f43;
  --mapsize:min(520px, calc(100vh - 350px));
}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--bg);color:var(--txt);font:13px/1.5 "Segoe UI","Microsoft YaHei",system-ui,sans-serif;
  display:flex;flex-direction:column;overflow:hidden}
header{flex:0 0 auto;display:flex;align-items:center;gap:18px;padding:8px 14px;
  background:linear-gradient(90deg,#11151f,#151a26);border-bottom:1px solid var(--line)}
header h1{font-size:16px;margin:0;font-weight:600;letter-spacing:.5px;white-space:nowrap}
header h1 em{color:var(--accent);font-style:normal}
.chips{display:flex;gap:8px;flex-wrap:wrap;align-items:center;flex:1}
.chip{background:var(--panel2);border:1px solid var(--line);border-radius:20px;padding:3px 10px;
  font-size:11.5px;color:var(--dim);white-space:nowrap}
.chip b{color:var(--txt);font-weight:600}
.chip.ok{border-color:#1f6b4f;color:#9fe8c8}
.chip.warn{border-color:#7a5a1c;color:#ffd98a}
a.chip{color:var(--dim);text-decoration:none;cursor:pointer}
a.chip:hover{border-color:var(--accent);color:var(--accent)}
main{flex:1;min-height:0;display:grid;grid-template-columns:404px minmax(0,1fr);gap:12px;padding:12px;overflow:hidden}
.leftcol{display:flex;flex-direction:column;gap:12px;min-height:0;overflow:hidden}
.rightcol{display:flex;flex-direction:column;gap:12px;min-height:0;overflow:auto;padding-right:2px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px}
.cardhead{display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:1px solid var(--line)}
.cardhead h2{font-size:13px;margin:0;font-weight:600;letter-spacing:.4px}
.cardhead .sub{color:var(--dim);font-size:11.5px}
.cardhead .sp{flex:1}

/* ---------- 地图（原著贴图） ---------- */
.mapcard{padding:10px 12px 12px}
.maprow{display:flex;gap:16px;align-items:flex-start}
#mapbox{position:relative;flex:0 0 auto;width:var(--mapsize);aspect-ratio:1/1;
  border:2px solid #3a3f52;border-radius:6px;background:#000 center/100% 100% no-repeat;
  image-rendering:pixelated;box-shadow:0 4px 18px rgba(0,0,0,.5)}
#psvg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:2}
#consumeLayer,#patchLayer,#dynLayer{position:absolute;inset:0;pointer-events:none;z-index:1}
.cons{position:absolute;width:7.6923%;height:7.6923%;transform:translate(-50%,-50%);
  background-image:var(--tile);background-size:100% 100%;background-repeat:no-repeat;
  image-rendering:pixelated}
.cons.ku{background-image:var(--up)}
.cons.kd{background-image:var(--down)}
#consumeLayer.hint .cons{outline:1px dashed rgba(62,207,142,.9);outline-offset:-1px}
.patch{position:absolute;width:7.6923%;height:7.6923%;transform:translate(-50%,-50%);
  border:2px dashed #ff9f43;border-radius:4px;background:rgba(255,159,67,.10);
  display:flex;align-items:flex-end;justify-content:center}
.patch span{font-size:9px;color:#ffd9a8;background:rgba(30,18,6,.85);padding:0 3px;border-radius:3px;
  transform:translateY(6px);white-space:nowrap}
/* 变动格：该步起新出现的物件（10F 战利品/落穴/楼梯、41F 魔術師Ａ+暗墙+降臨翼…） */
.dynmk{position:absolute;width:7.6923%;height:7.6923%;transform:translate(-50%,-50%);
  border:2px solid #4cc9f0;border-radius:4px;background:rgba(76,201,240,.13);
  display:flex;align-items:center;justify-content:center;overflow:hidden}
.dynmk span{font-size:8.5px;color:#c8f0ff;background:rgba(6,24,32,.88);padding:0 2px;border-radius:3px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.dynmk.t{background:rgba(176,124,255,.14);border-color:#b07cff}
.dynmk.t span{color:#e6d4ff}
.dynmk.s{background:rgba(62,207,142,.16);border-color:#3ecf8e}
.dynmk.s span{color:#b6f5d8}
#marker{position:absolute;width:7.6923%;height:7.6923%;transform:translate(-50%,-50%);z-index:3;
  pointer-events:none}
#heroImg{width:100%;height:100%;image-rendering:pixelated}
/* ✅ 2026-11-18（用户要求）：去掉勇者身上的蓝色发光与右上角朝向角标箭头 */
/* 楼层信息卡片（原 #mapside 内容，现移到右栏顶部） */
.floorbody{padding:10px 12px;display:flex;flex-direction:column;gap:10px}
/* 地图右侧的「本步状态」卡片 */
#mapside{flex:1 1 340px;min-width:280px;display:flex;flex-direction:column;gap:10px}
#mapside .statecard{display:flex;flex-direction:column;min-height:0}
#mapside .statebody{overflow:auto}
.floorname{font-size:20px;font-weight:700;letter-spacing:1px}
.floorname span{font-size:12px;color:var(--dim);font-weight:400;margin-left:6px}
.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}
.stat{background:var(--panel2);border:1px solid var(--line);border-radius:7px;padding:6px 8px}
.stat i{display:block;font-style:normal;color:var(--dim);font-size:11px}
.stat b{font-size:14px;color:var(--txt)}
.legend{display:flex;flex-wrap:wrap;gap:6px 10px;font-size:11px;color:var(--dim)}
.legend span{display:flex;align-items:center;gap:4px}
.dot{width:11px;height:11px;border-radius:3px;display:inline-block;border:1px solid #000}
.toggle{display:flex;align-items:center;gap:6px;font-size:11.5px;color:var(--dim);cursor:pointer}

/* ---------- 控制条 ---------- */
.controls{display:flex;align-items:center;gap:8px;margin-top:10px;flex-wrap:wrap}
.btn{background:var(--panel2);border:1px solid var(--line);color:var(--txt);border-radius:7px;
  padding:5px 10px;font-size:12px;cursor:pointer;white-space:nowrap}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn.primary{background:#12384a;border-color:#1d6d8f;color:#bfeeff}
.btn.primary:hover{background:#164a63}
#slider{flex:1;min-width:120px;accent-color:var(--accent)}
#stepno{width:64px;background:#0f131c;border:1px solid var(--line);color:var(--txt);border-radius:6px;
  padding:4px 6px;font-size:12px;text-align:center}
.ctrllabel{font-size:11.5px;color:var(--dim);white-space:nowrap}

/* ---------- 步骤表 ---------- */
.stepcard{flex:1;min-height:150px;display:flex;flex-direction:column;overflow:hidden}
.stepcard .cardhead{padding:7px 12px}
.tablewrap{flex:1;overflow:auto}
table{border-collapse:collapse;width:100%;font-size:12px}
thead th{position:sticky;top:0;background:#141926;z-index:2;text-align:left;font-weight:600;
  color:var(--dim);padding:5px 7px;border-bottom:1px solid var(--line);white-space:nowrap;font-size:11.5px}
tbody td{padding:3px 7px;border-bottom:1px solid #1e2431;white-space:nowrap;vertical-align:middle}
tbody tr{cursor:pointer}
tbody tr:hover{background:#1a2030}
tbody tr.sel{background:#12303f;box-shadow:inset 3px 0 0 var(--accent)}
tbody tr.mmrow{box-shadow:inset 3px 0 0 var(--gold)}
tbody tr.mmrow.sel{box-shadow:inset 3px 0 0 var(--gold),inset 0 0 0 1px #1d6d8f}
tbody tr.blk{box-shadow:inset 3px 0 0 var(--red)}
tbody tr.invrow{box-shadow:inset 3px 0 0 var(--orange);background:#241a0e}
tbody tr.deadrow{box-shadow:inset 3px 0 0 var(--red);background:#2a1212}
tbody tr.unrow td{color:#5f6b80;opacity:.72}
tbody tr.noterow td{color:var(--dim)}
td.num{color:var(--dim);text-align:right;font-variant-numeric:tabular-nums}
td.dir{text-align:center;color:var(--accent);font-weight:700}
td.ev{max-width:340px;white-space:normal;word-break:break-all}
td.ev .tag{display:inline-block;font-size:10px;padding:0 4px;border-radius:3px;margin-right:4px;background:#233047;color:#9db4d8}
td.ev .tag.b{background:#3a2020;color:#ffb0b0}
td.note{color:var(--gold);font-size:11px;max-width:200px;overflow:hidden;text-overflow:ellipsis}
td.keys{font-variant-numeric:tabular-nums;color:#c9d2e2}
.dpos{color:var(--green)} .dneg{color:var(--red)} .d0{color:#55617a}

/* ---------- 右侧 ---------- */
.rightcol .card{padding:0}
.statebody{padding:10px 12px;display:flex;flex-direction:column;gap:9px}
.stephead{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.stephead .no{font-size:20px;font-weight:700;letter-spacing:.5px}
.pill{font-size:11px;padding:2px 7px;border-radius:20px;border:1px solid var(--line);color:var(--dim)}
.pill.ok{border-color:#1f6b4f;color:#9fe8c8;background:#0e2a20}
.pill.note{border-color:#7a5a1c;color:#ffd98a;background:#2a2110}
.pill.blocked{background:#3a1414;border-color:#7a2020;color:#ffb0b0}
.pill.invalid{background:#3a2410;border-color:#8a5a1b;color:#ffc078}
.pill.dead{background:#3a1414;border-color:#ff2d2d;color:#ffc9c9;font-weight:700}
.pill.unreachable{background:#20242f;border-color:#39404f;color:#8b97ad}
.pill.skip{background:#2a2110;border-color:#7a5a1c;color:#ffd98a}
.evline{font-size:13px;color:var(--txt);word-break:break-all}
.logline{font-size:11.5px;color:var(--dim);word-break:break-all}
.posline{font-size:12px;color:var(--dim)}
.posline b{color:var(--txt)}
.statgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:7px}
.sbox{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:7px 9px}
.sbox i{display:block;font-style:normal;color:var(--dim);font-size:10.5px;letter-spacing:.5px}
.sbox .val{font-size:15px;font-weight:600;font-variant-numeric:tabular-nums}
.sbox .from{font-size:11px;color:#6d7891}
.sbox .dl{font-size:11.5px;margin-left:4px}
.keyrow{display:flex;gap:8px}
.keyrow .kk{flex:1;text-align:center;background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:5px}
.keyrow .kk i{font-style:normal;font-size:10.5px;color:var(--dim);display:block}
.keyrow .kk b{font-size:15px}
.itemrow{display:flex;flex-wrap:wrap;gap:5px;align-items:center;
  background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:6px 8px}
.itemrow .ihead{font-size:10.5px;color:var(--dim);margin-right:2px}
.itemicon{width:30px;height:30px;image-rendering:pixelated;display:block}
.warnbox{background:#2a2110;border:1px solid #7a5a1c;border-radius:8px;padding:7px 9px;font-size:11.5px;color:#ffd98a}
.warnbox b{color:#ffe6a8}
.okbox{background:#0e2a20;border:1px solid #1f6b4f;border-radius:8px;padding:7px 9px;font-size:11.5px;color:#9fe8c8}

.floorchips{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:10px 12px}
.fchip{background:var(--panel2);border:1px solid var(--line);border-radius:7px;padding:5px 6px;cursor:pointer;text-align:center}
.fchip:hover{border-color:var(--accent)}
.fchip b{display:block;font-size:13px}
.fchip i{font-style:normal;font-size:10px;color:var(--dim)}
.fchip.active{border-color:var(--accent);background:#12303f;box-shadow:0 0 0 1px rgba(76,201,240,.3)}
.fchip.warnf{border-color:#6d4f1c}
.fchip.A b{color:#7fc3e8}.fchip.B b{color:#c3a3ff}.fchip.C b{color:#ffc078}

.issueitem{padding:8px 12px;border-bottom:1px solid #1e2431;cursor:pointer}
.issueitem:last-child{border-bottom:none}
.issueitem:hover{background:#1a2030}
.issueitem .ih{display:flex;gap:7px;align-items:center;margin-bottom:2px}
.issueitem .ln{font-size:11px;color:var(--dim)}
.issueitem .msg{font-size:11.5px;color:#c9d2e2;line-height:1.45}
.kindbadge{font-size:10px;padding:1px 6px;border-radius:10px;font-weight:600}
.kindbadge.coord{background:#2a2110;color:#ffd98a}
.kindbadge.patch{background:#2a1a35;color:#d7a6ff}
.kindbadge.mismatch{background:#3a1414;color:#ffb0b0}
.kindbadge.blocked{background:#3a1414;color:#ffb0b0}
.kindbadge.gate{background:#3a2410;color:#ffc078}
.kindbadge.dead{background:#3a1414;color:#ffc9c9}

/* ---------- 标记层：栅栏门 / 不可得 / 暴毙 ---------- */
#markLayer{position:absolute;inset:0;pointer-events:none;z-index:2}
#dmgLayer{position:absolute;inset:0;pointer-events:none;z-index:4}
/* 扣血角标：对齐主流 HTML5 魔塔（mota-js 样板）的伤害文字生成方式——
   canvas 侧是 `strokeText()`（黑描边）再 `fillText()`（彩色填充），无衬线粗体、**字号固定**
   （不按位数缩放；格子 40px、14px 字号下 5 位数 ≈39px，正好压满一格）。
   DOM 里用 -webkit-text-stroke + paint-order 等价实现：描边先画、填充后盖（= fill 在上），
   描边宽用 em 跟随字号缩放，不再依赖模糊 text-shadow。 */
#dmgLayer .dmg{position:absolute;line-height:1;white-space:nowrap;
  font-family:Arial,"Helvetica Neue","Microsoft YaHei","PingFang SC",sans-serif;
  font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:-.2px;
  font-size:calc(var(--mapsize)/37);
  -webkit-text-stroke:.085em #000;paint-order:stroke fill;
  text-shadow:0 1px 1px rgba(0,0,0,.45);
  transform:translate(-1px,-100%);padding:0 1px}
.mk{position:absolute;width:7.6923%;height:7.6923%;transform:translate(-50%,-50%);
  display:flex;align-items:center;justify-content:center;font-weight:700}
.mk.gate{background:rgba(255,93,93,.22);border:2px solid #ff5d5d;border-radius:4px}
.mk.gate::after{content:'✕';color:#ff8a8a;font-size:15px;text-shadow:0 0 4px #000}
.mk.loot{background:rgba(139,151,173,.16);border:2px dashed #8b97ad;border-radius:4px}
.mk.loot::after{content:'✕';color:#aab6cc;font-size:14px;text-shadow:0 0 4px #000}
.mk.death{background:rgba(255,45,45,.28);border:2px solid #ff2d2d;border-radius:50%;
  animation:mkpulse 1.2s infinite}
.mk.death::after{content:'☠';color:#fff;font-size:16px;text-shadow:0 0 6px #ff2d2d}
@keyframes mkpulse{0%,100%{box-shadow:0 0 0 0 rgba(255,45,45,.65)}50%{box-shadow:0 0 0 8px rgba(255,45,45,0)}}
.verify{padding:10px 12px;display:flex;flex-direction:column;gap:7px;font-size:11.5px;color:var(--dim)}
.verify b{color:var(--txt)}
.hl{cursor:pointer;border-bottom:1px dashed #4a5568}
.hl:hover{color:var(--accent);border-color:var(--accent)}
.npc{cursor:help;border-bottom:1px dotted #7e8aa3;color:#c9d2e2}
.npc:hover{color:var(--accent);border-color:var(--accent)}
/* 对话悬浮面板：显示该角色在 magic_tower1_texts.md 中的全部台词（按楼层分组） */
.npctip{position:absolute;display:none;z-index:9999;max-width:380px;
  background:#0f1420;border:1px solid var(--accent);border-radius:8px;padding:8px 10px;
  box-shadow:0 6px 24px rgba(0,0,0,.6);font-size:12px;line-height:1.55;color:var(--txt);pointer-events:none}
.npctip .npch{font-weight:700;color:var(--accent);margin-bottom:5px;
  border-bottom:1px solid var(--line);padding-bottom:4px;white-space:nowrap}
.npctip .npcl{color:var(--txt);white-space:pre-wrap;word-break:break-word}
/* 地图 NPC 标记：默认透明不干扰底图，悬停显示虚线框 + 触发对话面板 */
#npcMarkLayer{position:absolute;inset:0;pointer-events:none;z-index:2}
.npcmark{position:absolute;width:7.6923%;height:7.6923%;transform:translate(-50%,-50%);
  border-radius:5px;cursor:help;pointer-events:auto}
.npcmark:hover{outline:2px solid var(--accent);outline-offset:-2px;
  background:rgba(124,201,240,.20);box-shadow:0 0 10px rgba(124,201,240,.5)}

#psvg .full{fill:none;stroke:#2f3a4f;stroke-width:1.1;stroke-dasharray:3 3}
#psvg .vis{fill:none;stroke:#4cc9f0;stroke-width:2;stroke-linejoin:round;
  filter:drop-shadow(0 0 2px rgba(76,201,240,.9))}
#psvg .visn{fill:none;stroke:#ffd98a;stroke-width:2;stroke-dasharray:4 3}

/* ===== 平板/窄屏：单列纵向堆叠 ===== */
@media (max-width:1080px){
  /* 关键：body 原为 flex 列 + main flex:1，高度锁死在视口内 → 单列堆叠后内容超长
     会被裁切并与相邻块重叠。窄屏改回普通文档流。 */
  html,body{height:auto;min-height:100%}
  body{display:block;overflow-y:auto;overflow-x:hidden}
  main{grid-template-columns:1fr;overflow:visible;height:auto;min-height:0}
  .rightcol{overflow:visible;order:2;height:auto}
  .leftcol{overflow:visible;order:1;height:auto}
  .stepcard{height:auto;min-height:300px}
  /* 平板/横屏：表格限高纵向滚动，避免整页被 6000+ 步撑到 7000px */
  .stepcard{display:flex;flex-direction:column}
  .tablewrap{overflow:auto;max-height:70vh}
  :root{--mapsize:min(520px, 92vw)}
  /* 地图与其右侧卡片在窄屏改为上下堆叠，避免侧栏被压成 0 宽 */
  .maprow{flex-wrap:wrap;gap:12px}
  #mapbox{width:100%;max-width:var(--mapsize);margin:0 auto}
  #mapside{flex:1 1 100%;min-width:0;width:100%}
  #mapside .statebody{overflow:visible}
}

/* ===== 手机：压缩留白、修横向溢出与表格塌陷 ===== */
@media (max-width:720px){
  html,body{max-width:100%;overflow-x:hidden}
  header{flex-wrap:wrap;gap:8px;padding:8px 10px}
  header h1{font-size:14px;white-space:normal;line-height:1.35}
  .chips{gap:6px;flex:1 1 100%}
  .chip{font-size:11px;padding:2px 8px}
  main{padding:8px;gap:8px}
  /* 关键：栅格子项默认 min-width:auto，会被内部 min-width:560px 的表格撑开 */
  main>aside,main>section{min-width:0}
  .rightcol,.leftcol{min-width:0;width:100%}
  .mapcard{padding:8px}
  .maprow{gap:8px}
  :root{--mapsize:min(520px, calc(100vw - 40px))}
  .controls{gap:6px;margin-top:8px}
  .controls .btn{font-size:12px;padding:6px 9px;flex:0 0 auto}
  #slider{flex:1 1 100%;min-width:0;order:10}
  .controls #stepLabel{order:11}
  .controls #stepno{order:12;width:72px;flex:0 0 auto}
  .controls #btnGo{order:13}
  /* 表格：横向滚动 + 限高，避免整页被撑到几千像素 */
  .stepcard{display:flex;flex-direction:column}
  .tablewrap{overflow:auto;-webkit-overflow-scrolling:touch;max-height:60vh}
  .tablewrap table{min-width:560px}
  .cardhead{flex-wrap:wrap;gap:6px;padding:8px 10px}
  .cardhead h2{font-size:12.5px;white-space:nowrap}
  .statebody,.floorbody{padding:8px 10px}
  .stephead .no{font-size:17px}
  .statgrid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
  .keyrow{gap:6px}
}
</style>
</head>
<body>
<header>
  <h1>魔塔1 <em>1F→50F</em> 全塔通关逐格校验</h1>
  <div class="chips" id="chips"></div>
</header>

<main>
  <aside class="rightcol">
    <div class="card">
      <div class="cardhead"><h2>楼层信息</h2><span class="sp"></span><span class="sub">当前层与图例</span></div>
      <div class="floorbody">
        <div>
          <div class="floorname" id="floorname">1F</div>
          <div class="posline" id="posline"></div>
        </div>
        <div class="stats" id="floostats"></div>
        <div class="legend" id="legend"></div>
        <label class="toggle"><input type="checkbox" id="consToggle"> 给已消耗格描边（默认已还原成地面）</label>
      </div>
    </div>

    <div class="card">
      <div class="cardhead"><h2>校验结论 / 问题清单</h2><span class="sp"></span><span class="sub" id="issueSub"></span></div>
      <div class="verify" id="verifyBox"></div>
      <div id="issueList"></div>
    </div>

    <div class="card">
      <div class="cardhead"><h2>楼层导航</h2><span class="sp"></span><span class="sub">点击跳到该层第一步</span></div>
      <div class="floorchips" id="floorchips"></div>
    </div>
  </aside>

  <section class="leftcol">
    <div class="card mapcard">
      <div class="maprow">
        <div id="mapbox">
          <svg id="psvg" viewBox="0 0 520 520" preserveAspectRatio="none"></svg>
          <div id="consumeLayer"></div>
          <div id="patchLayer"></div>
          <div id="dynLayer"></div>
          <div id="markLayer"></div>
          <div id="npcMarkLayer"></div>
          <div id="dmgLayer"></div>
          <div id="marker"><img id="heroImg" alt="勇者"></div>
        </div>
        <div id="mapside">
          <div class="card statecard">
            <div class="cardhead"><h2>本步状态（引擎实算）</h2><span class="sp"></span><span class="sub" id="stateSub"></span></div>
            <div class="statebody" id="stateBody"></div>
          </div>
        </div>
      </div>
      <div class="controls">
        <button class="btn" id="btnFirst" title="首步">⏮</button>
        <button class="btn" id="btnPrev" title="上一步">◀</button>
        <button class="btn primary" id="btnNext" title="下一步">下一步 ▶</button>
        <button class="btn" id="btnLast" title="末步">⏭</button>
        <button class="btn" id="btnPrevEv" title="上一个事件">↑ 上一事件</button>
        <button class="btn" id="btnNextEv" title="下一个事件">↓ 下一事件</button>
        <button class="btn" id="btnPlay" title="自动播放">▶ 播放</button>
        <input id="slider" type="range" min="1" max="__TOTAL__" value="1">
        <span class="ctrllabel" id="stepLabel">1 / __TOTAL__</span>
        <input id="stepno" type="number" min="1" max="__TOTAL__" value="1">
        <button class="btn" id="btnGo">跳转</button>
      </div>
    </div>

    <div class="card stepcard">
      <div class="cardhead">
        <h2 id="tblTitle">本层步骤</h2>
        <span class="sub" id="tblSub"></span>
        <span class="sp"></span>
        <label class="ctrllabel"><input type="checkbox" id="keyonly"> 只看关键步（事件 / 战斗 / 开门 / 拾取 / 异常）</label>
      </div>
      <div class="tablewrap">
        <table>
          <thead>
            <tr>
              <th>步</th><th>楼层 (x,y)</th><th>方向</th><th>事件 / 日志</th>
              <th>HP</th><th>ATK</th><th>DEF</th><th>G</th><th>钥匙</th><th>Δ</th>
            </tr>
          </thead>
          <tbody id="tbody"></tbody>
        </table>
      </div>
    </div>
  </section>
</main>

<div id="npctip" class="npctip"></div>
__DATASCRIPT__<script>
const D = __DATA__;
const IMG = __IMG__;
const TILE = __TILE__;
const STAIR = __STAIR__;
const CONS = D.cons || {};
const HERO = __HERO_JSON__;
const ITEM = __ITEMICON__;
(function(){
'use strict';
const ST = D.steps, FL = D.floors, ISSUES = D.issues || [];
const TOTAL = ST.length;
// 到每一步为止已访问的最大楼层（MAXF[i] = max(ST[0..i].f)）
const MAXF = (function(){var a=new Array(ST.length);var m=0;for(var i=0;i<ST.length;i++){var v=ST[i].f||1;if(v>m)m=v;a[i]=m;}return a;})();
const byFloor = {}, firstOf = {};
ST.forEach(function(s,i){
  (byFloor[s.f] = byFloor[s.f] || []).push(i);
  if(firstOf[s.f] === undefined) firstOf[s.f] = i;
});

const CELL=40, N=13, MAPW=CELL*N;
const PATCHES = [{f:29,x:6,y:3,label:'暗道补丁'},{f:30,x:6,y:1,label:'清场生成梯'}];

const svgEl = document.getElementById('psvg');
const markerEl = document.getElementById('marker');
const mapbox = document.getElementById('mapbox');
const consumeLayer = document.getElementById('consumeLayer');
const patchLayer = document.getElementById('patchLayer');
const dynLayer = document.getElementById('dynLayer');
const dmgLayer = document.getElementById('dmgLayer');
const tbody = document.getElementById('tbody');
// 步骤明细：点击某行自动跳转到该步（事件委托，2026-11-14）
tbody.addEventListener('click', function(e){
  const tr = e.target.closest ? e.target.closest('tr[data-i]') : null;
  if(tr){ select(+tr.dataset.i); }
});
const slider = document.getElementById('slider');
const stepno = document.getElementById('stepno');

let sel = 0, tableFloor = -1, keyOnly = false, lastKeyOnly = false, playTimer = null, showCons = false;

const DIRV = {'↑':[0,-1],'↓':[0,1],'←':[-1,0],'→':[1,0],'·':[0,0],'':[0,0]};
const STLABEL = {ok:'正常',note:'标注行',blocked:'无法执行',skip:'未执行',
  invalid:'违规未执行',dead:'暴毙',unreachable:'未执行'};
const EXEC = {ok:1,note:1,dead:1};

function esc(t){ return String(t==null?'':t).replace(/[&<>"']/g, function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
}); }
/* 对话 / 角色名：路线里凡出现具名台词角色（盗贼 / 骑士队长 / 吸血鬼 / 魔王 / 勇者…
   等），无论是否带「引号」，都包成 .npc 并带 data-npc 属性；悬停由下方自定义面板
   显示该角色在本层的台词（按 data-floor 过滤，只显示当前层，不跨层）。
   仅当「角色名「」紧跟时走对话排版：角色名：<换行>台词，多句各成行。 */
const NPC_DLG = __NPC_DLG__;
const NPC_MARKS = __NPC_MARKS__;
const NPC_RE = /__NPC_RE__/g;
function fmtEv(t, floor){
  if(!t) return '';
  let s = esc(t);
  s = s.replace(NPC_RE, function(_, name, q){
    const d = NPC_DLG[name];
    if(!d) return name;
    const fa = (floor!=null && floor!==undefined) ? ' data-floor="'+floor+'"' : '';
    if(q){  // 对话形式 角色名「台词」 → 角色名：<换行>台词
      return '<span class="npc" data-npc="'+esc(name)+'"'+fa+'>'+name+'：</span><br>';
    }
    return '<span class="npc" data-npc="'+esc(name)+'"'+fa+'>'+name+'</span>';
  });
  s = s.replace(/」/g, '<br>');
  return s;
}
function posOf(s){ return s.p ? s.p : [s.f,s.x,s.y]; }
function actualFloor(){ return posOf(ST[sel])[0]; }
function pct(v){ return ((v*CELL+CELL/2)/MAPW*100).toFixed(4)+'%'; }
function cx(x){ return x*CELL+CELL/2; }
function cy(y){ return y*CELL+CELL/2; }
/* 剩余怪物伤害：m=[hp,atk,def,name]，heroA/heroD 为当前步英雄攻防。
   返回 {txt,color}：打不过=红???；loss0=绿；越高越偏红（线性 hue 120→0，封顶 300）。 */
function dmgInfo(m, heroA, heroD, items, oid){
  const hp=m[0], atk=m[1], def=m[2];
  // ✅ 2026-11-16（用户指出：怪左下角伤害未计倍率）：
  //   与引擎 mota_core.battle() 保持一致 ——
  //   十字架 obj103 对 obj48/49/59（ゾンビ/ゾンビナイト/バンパイア）攻击翻倍；
  //   屠龙匕 obj109 对 obj74（ドラゴン）攻击翻倍。缺这两条会显著高估伤害。
  const IT = items || [];
  const mult = (((oid===48||oid===49||oid===59) && IT.indexOf(103)>=0) ||
                (oid===74 && IT.indexOf(109)>=0)) ? 2 : 1;
  const per = heroA * mult - def;
  if(per <= 0) return {txt:'???', color:'#ff5b5b', cant:true};
  const turns = Math.ceil(hp/per);
  const loss = Math.max(atk - heroD, 0) * (turns - 1);
  const t = Math.min(loss/300, 1);
  const h = 120 - 120*t;
  return {txt:String(loss), color:'hsl('+h+',92%,56%)', cant:false, loss:loss};
}
function renderDmg(f, heroA, heroD, items){
  const ITEMS_NOW = items || [];
  const fl = FL[f];
  if(!fl){ dmgLayer.innerHTML=''; return; }
  const cons = CONS[String(f)] || [];
  const done = {};
  cons.forEach(function(c){ if(c[2]<=sel) done[c[0]+','+c[1]]=1; });
  const objs = fl.objs || {}, MS = D.monstats || {};
  let h='';
  for(const k in objs){
    const v = objs[k], oid = String(v[0]);
    if(v[2]!=='m' || done[k]) continue;               // 只画未打的怪
    const ms = MS[oid];
    if(!ms) continue;
    const xy = k.split(',');
      const info = dmgInfo(ms, heroA, heroD, ITEMS_NOW, +oid);
    const x = +xy[0], y = +xy[1];
    const left = (x*CELL/MAPW*100).toFixed(3)+'%';
    const top  = ((y+1)*CELL/MAPW*100).toFixed(3)+'%';
    // 字号固定（与主流 H5 魔塔一致：canvas 侧就是一个固定的 `bold 12px`，
    // 不按位数缩放；格子 40px、14px 字号下 5 位数 ≈39px，刚好压满一格）。
    // ???（打不动）同字号，只换成红色。
    h += '<span class="dmg" style="left:'+left+';top:'+top+';color:'+info.color+'">'
         + info.txt + '</span>';
  }
  dmgLayer.innerHTML = h;
}
function dspan(v){
  if(!v) return '<span class="d0">0</span>';
  return '<span class="'+(v>0?'dpos':'dneg')+'">'+(v>0?'+':'')+v+'</span>';
}
function deltaText(s){
  const a=[];
  if(s.dh) a.push('HP'+(s.dh>0?'+':'')+s.dh);
  if(s.da) a.push('A'+(s.da>0?'+':'')+s.da);
  if(s.dd) a.push('D'+(s.dd>0?'+':'')+s.dd);
  if(s.dg) a.push('G'+(s.dg>0?'+':'')+s.dg);
  return a.length?a.join(' '):'—';
}
function isKeyStep(s){
  return !!(s.l) || !!(s.mm) || s.st!=='ok' || s.st==='note';
}

/* ---------------- 地图（原著贴图 + 路径 + 勇者） ---------------- */
function renderMap(){
  const f = actualFloor();
  const fl = FL[f];
  if(!fl) return;
  mapbox.style.backgroundImage = 'url("'+(IMG[String(f)]||'')+'")';

  // 已消耗格（击杀/拾取/开门/撞暗墙/交谈NPC…）→ 还原成地面；楼梯格上的人走了则还原成楼梯
  const cons = CONS[String(f)] || [];
  // 截至当前步已消耗的格（如盗贼交谈后消失、镐拾取后消失）→ 该格起按空地处理
  const consumed = {};
  cons.forEach(function(c){ if(c[2] <= sel) consumed[c[0]+','+c[1]]=1; });
  // ✅ 2026-11-15：值到 "T0"（地形变地面）的格也**直接贴本层地板贴图**，不再只挂紫框标记。
  //   37F 超级镐破整层真墙 / 24F 秘道 / 29F 暗道 / 41F 揭示格都走这条路：
  //   原图里那格是墙的像素，不覆盖就会一直显示成墙 ← 用户指出的 bug。
  const tfloor = [];
  ((D.dyn||{})[String(f)] || []).forEach(function(d){
    if(d[2] <= sel && d[3] === 'T0') tfloor.push([d[0], d[1]]);
  });
  consumeLayer.style.setProperty('--tile', 'url("' + (TILE[String(f)] || '') + '")');
  consumeLayer.style.setProperty('--up', 'url("' + (STAIR.u || '') + '")');
  consumeLayer.style.setProperty('--down', 'url("' + (STAIR.d || '') + '")');
  consumeLayer.innerHTML = cons.filter(function(c){ return c[2] <= sel; }).map(function(c){
    // ⚠️ 2026-11-15 修 bug：_tile() 返回 'ku'/'kd'/'f'，旧代码一律拼成 'k'+值 →
    //   class 变成 "cons kku"，而 CSS 只有 `.cons.ku` / `.cons.kd`，永远匹配不上，
    //   于是**所有楼梯格都被当普通地板画**（32F(11,1) 上行梯不显示就是这么来的）。
    //   现在只在 ku/kd 时追加该类，其余走基础 .cons（即 --tile 地板）。
    return '<div class="cons'+(c[3]==='ku'?' ku':(c[3]==='kd'?' kd':''))+'" style="left:'+pct(c[0])+';top:'+pct(c[1])+'"></div>';
  }).join('') + tfloor.map(function(p){
    return '<div class="cons" style="left:'+pct(p[0])+';top:'+pct(p[1])+'"></div>';
  }).join('');

  // 补丁格
  patchLayer.innerHTML = PATCHES.filter(function(p){return p.f===f;}).map(function(p){
    return '<div class="patch" style="left:'+pct(p.x)+';top:'+pct(p.y)+'"><span>'+esc(p.label)+'</span></div>';
  }).join('');

  // 变动格：该步起「新出现/变化」的物件与地形（10F 战利品/落穴/楼梯、41F 魔術師Ａ+暗墙+降臨翼…）
  const dynArr = (D.dyn||{})[String(f)] || [];
  const OBJN = D.objnames || {};
  const TLAB = {'0':'地面','1':'墙','2':'楼梯','3':'暗墙'};
  // ✅ 2026-11-16：同一格可能有先后多条 dyn（如 10F (4,4)：步1478 出现落穴 obj20 →
  //   步1791 被 BOSS 战后拆除变地面 T0）。旧逻辑只看「该条自身是否为 T0」，
  //   于是 obj20 那条仍然挂标记，画面在 BOSS 后仍显示落穴 ← 用户指出的地面渲染错误。
  //   现预扫一遍：凡该格已有 ≤sel 的 T0，则跳过它的物件标记。
  const dynCleared = {};   // key -> 已被清成地面
  dynArr.forEach(function(d){
    if(d[2] > sel) return;
    if(d[3] === 'T0') dynCleared[d[0]+','+d[1]] = 1;
  });
  const dynSeen = {};
  let dynH = '';
  dynArr.forEach(function(d){
    if(d[2] > sel) return;                      // 尚未出现
    if(d[3] === 'T0') return;                   // 变地面：已由 consumeLayer 贴地板贴图，不再挂标记
    const key = d[0]+','+d[1];
    const v = d[3];
    if(dynCleared[key]) return;                 // 该格后来已被清成地面 → 旧物件标记不再显示
    // 物件已被拾取/击杀/交谈（该格已还原成地面）→ 不再显示；地形变化 T* 保留
    if(typeof v !== 'string' && consumed[key]) return;
    const stat = (fl.objs||{})[key];
    if(typeof v !== 'string' && stat && String(stat[0]) === String(v)) return;  // 与静态一致，无变化
    let lab, cls='dynmk';
    if(v === 'STAIR'){ lab='上行梯'; cls+=' s'; }
    else if(typeof v === 'string' && v.charAt(0)==='T'){
      const tv=v.slice(1); lab=TLAB[tv]||('T'+tv); cls+=' t';
    } else { lab=OBJN[String(v)]||('obj'+v); }
    const dk = key+'|'+String(v);
    if(dynSeen[dk]) return;
    dynSeen[dk]=1;
    dynH += '<div class="'+cls+'" style="left:'+pct(d[0])+';top:'+pct(d[1])+'" title="步'+d[2]+' 出现：'+esc(lab)+'"><span>'+esc(lab)+'</span></div>';
  });
  dynLayer.innerHTML = dynH;

  // 标记层：2F 栅栏门 / 门后不可得战利品 / 暴毙点
  const MK = (D.markers||{})[String(f)] || [];
  document.getElementById('markLayer').innerHTML = MK.map(function(m){
    return '<div class="mk '+m.t+'" style="left:'+pct(m.x)+';top:'+pct(m.y)+'" title="'+esc(m.label)+'"></div>';
  }).join('');

  // NPC 标记层：该层所有具名 NPC 所在格（默认透明，悬停触发 #npctip 对话面板）
  // 已交谈的 NPC 会从地图消失 → 该格起不再挂悬停标记，按空地处理
  const NM = (NPC_MARKS[String(f)] || []).filter(function(m){ return !consumed[m.x+','+m.y]; });
  document.getElementById('npcMarkLayer').innerHTML = NM.map(function(m){
    return '<div class="npcmark" data-npc="'+esc(m.n.join('|'))+'" data-floor="'+f+'" style="left:'+pct(m.x)+';top:'+pct(m.y)+'"></div>';
  }).join('');

  // 路径
  const full = (fl.path||[]);
  const vis=[];
  for(let i=0;i<=sel;i++){
    const s=ST[i], p=posOf(s);
    if(p[0]!==f || !EXEC[s.st]) continue;
    const pt=[p[1],p[2]];
    if(!vis.length || vis[vis.length-1][0]!==pt[0] || vis[vis.length-1][1]!==pt[1]) vis.push(pt);
  }
  function poly(pts, cls){
    // 同一层可能多次进出：相邻点不相邻（跨越楼梯/传送）时断开，避免画出穿墙直线
    const segs=[]; let cur=[];
    for(let i=0;i<pts.length;i++){
      if(i>0){
        const d=Math.abs(pts[i][0]-pts[i-1][0])+Math.abs(pts[i][1]-pts[i-1][1]);
        if(d>1){ if(cur.length>1) segs.push(cur); cur=[]; }
      }
      cur.push(pts[i]);
    }
    if(cur.length>1) segs.push(cur);
    return segs.map(function(a){
      return '<polyline class="'+cls+'" points="'+a.map(function(p){ return cx(p[0])+','+cy(p[1]); }).join(' ')+'"/>';
    }).join('');
  }
  // 只画已走过的青色路线（去掉"待经路线"黑虚线 full）
  svgEl.innerHTML = poly(vis,'vis');

  // 勇者
  const cur=ST[sel], p=posOf(cur);
  markerEl.style.left = pct(p[1]);
  markerEl.style.top  = pct(p[2]);
  document.getElementById('heroImg').src = HERO[cur.d] || HERO['↓'];

  // 剩余怪物伤害（当前层，按本步攻防算）
  renderDmg(f, cur.a, cur.df, cur.it);

  // 地图侧栏
  document.getElementById('floorname').innerHTML = f+'F <span>第 '+cur.i+' 步的实际位置</span>';
  let pos='';
  if(cur.p && (cur.p[0]!==cur.f || cur.p[1]!==cur.x || cur.p[2]!==cur.y)){
    pos='路线标注 '+cur.f+'F('+cur.x+','+cur.y+') → 引擎落点 <b>'+cur.p[0]+'F('+cur.p[1]+','+cur.p[2]+')</b>';
  }else{
    pos='坐标 <b>'+cur.f+'F('+cur.x+','+cur.y+')</b>　方向 '+(cur.d||'·');
  }
  document.getElementById('posline').innerHTML = pos;

  const st=fl;
  const entry = st.entry ? ('HP '+st.entry.hp+' / A '+st.entry.atk+' / D '+st.entry.dfn) : '—';
  const exit  = st.exit  ? ('HP '+st.exit.hp +' / A '+st.exit.atk +' / D '+st.exit.dfn) : '—';
  document.getElementById('floostats').innerHTML =
    '<div class="stat"><i>本层步数</i><b>'+st.steps+'</b></div>'+
    '<div class="stat"><i>战损</i><b>'+st.loss+'</b></div>'+
    '<div class="stat"><i>击杀</i><b>'+st.kills+'</b></div>'+
    '<div class="stat"><i>最大已访问楼层</i><b>'+MAXF[sel]+'</b></div>'+
    '<div class="stat"><i>首次进入</i><b style="font-size:11px;font-weight:400">'+entry+'</b></div>'+
    '<div class="stat"><i>最后离开</i><b style="font-size:11px;font-weight:400">'+exit+'</b></div>';
}

/* ---------------- 状态面板 ---------------- */
function renderState(){
  const s=ST[sel];
  const prev = sel>0 ? ST[sel-1] : null;
  const b = prev
    ? {hp:prev.hp, a:prev.a, df:prev.df, g:prev.g, ky:prev.ky, kb:prev.kb, kr:prev.kr}
    : {hp:s.hp-s.dh, a:s.a-s.da, df:s.df-s.dd, g:s.g-s.dg, ky:0, kb:0, kr:0};
  const DIRTXT = {'←':'⬅️向左移动','→':'➡️向右移动','↑':'⬆️向上移动','↓':'⬇️向下移动'};
  const ev = s.e || s.l || (DIRTXT[s.d] || '（纯移动）');
  let h='';
  h += '<div class="stephead">'+
       '<span class="no">#'+s.i+'</span>'+
       '<span class="pill '+s.st+'">'+(STLABEL[s.st]||s.st)+'</span>'+
       (s.rs?('<span class="pill">录制行 #'+s.rs+'</span>'):'')+
       '</div>';
  h += '<div class="evline">'+fmtEv(ev, s.f)+'</div>';
  const p=posOf(s);
  h += '<div class="posline">位置：<b>'+s.f+'F('+s.x+','+s.y+')</b>　方向 <b>'+(s.d||'·')+'</b>'+
       ((p[0]!==s.f||p[1]!==s.x||p[2]!==s.y) ? '　<span style="color:var(--gold)">引擎落点 '+p[0]+'F('+p[1]+','+p[2]+')</span>' : '')+
       '</div>';
  // ⚠️ 变量名别叫 src：Toy 的预检脚本用 `src\s*=\s*['"]...` 正则找本地资源引用，
  //    会把这个 JS 字符串当成 href 而误报 "referenced local resource not found"。
  let srcline='';
  if(s.rs){
    srcline = '来源：录制路线 CSV 第 '+s.rs+' 行 · 逐行重放与录制状态一致';
  }else{
    srcline = '来源：segs_route.py 人工翻译 · mota_core 逐格实算';
  }
  if(srcline) h += '<div class="logline">'+esc(srcline)+'</div>';
  h += '<div class="statgrid">'+
       '<div class="sbox"><i>HP 生命</i><span class="val">'+s.hp+'</span><span class="dl">'+dspan(s.dh)+'</span><div class="from">'+b.hp+' → '+s.hp+'</div></div>'+
       '<div class="sbox"><i>ATK 攻击</i><span class="val">'+s.a+'</span><span class="dl">'+dspan(s.da)+'</span><div class="from">'+b.a+' → '+s.a+'</div></div>'+
       '<div class="sbox"><i>DEF 防御</i><span class="val">'+s.df+'</span><span class="dl">'+dspan(s.dd)+'</span><div class="from">'+b.df+' → '+s.df+'</div></div>'+
       '<div class="sbox"><i>GOLD 金币</i><span class="val">'+s.g+'</span><span class="dl">'+dspan(s.dg)+'</span><div class="from">'+b.g+' → '+s.g+'</div></div>'+
       '</div>';
  h += '<div class="keyrow">'+
       '<div class="kk"><i>黄钥匙</i><b>'+s.ky+'</b><div class="from">'+b.ky+' → '+s.ky+'</div></div>'+
       '<div class="kk"><i>蓝钥匙</i><b>'+s.kb+'</b><div class="from">'+b.kb+' → '+s.kb+'</div></div>'+
       '<div class="kk"><i>红钥匙</i><b>'+s.kr+'</b><div class="from">'+b.kr+' → '+s.kr+'</div></div>'+
       '</div>';
  // 已获得道具：每道具一个图标，拿到才显示、用完即隐。
  // obj106 中心飞行器：显示剩余次数 s.cw 个（刚吃 3 个，用一次减一，减到 0 消失）。
  if(s.it && s.it.length){
    h += '<div class="itemrow"><span class="ihead">道具</span>'+ s.it.map(function(o){
      var n = (o===106) ? (s.cw||0) : 1;
      if(n<1) return '';
      var u = ITEM[o]||'';
      var nm = (D.objnames||{})[o]||('道具#'+o);
      return Array(n).fill('<img src="'+u+'" class="itemicon" title="'+esc(nm)+'">').join('');
    }).join('') + '</div>';
  }
  if(s.mm && s.mm.length){
    h += '<div class="warnbox"><b>⚠ 坐标/落点差异</b><br>'+s.mm.map(esc).join('<br>')+'</div>';
  }
  if(s.st==='ok' && !(s.mm&&s.mm.length)){
    h += '<div class="okbox">✓ 本步状态由 mota_core 实算，与路线无冲突</div>';
  }
  document.getElementById('stateBody').innerHTML = h;
  document.getElementById('stateSub').textContent = '第'+s.i+'/'+TOTAL+'步';
}

/* ---------------- 步骤表 ---------------- */
function buildTable(f){
  const list = (byFloor[f]||[]).filter(function(i){ return !keyOnly || isKeyStep(ST[i]); });
  let h='';
  for(const i of list){
    const s=ST[i];
    let cls='';
    if(s.mm && s.mm.length) cls+=' mmrow';
    if(s.st==='blocked') cls+=' blk';
    if(s.st==='invalid') cls+=' invrow';
    if(s.st==='dead') cls+=' deadrow';
    if(s.st==='unreachable') cls+=' unrow';
    if(s.st==='note'||s.st==='skip') cls+=' noterow';
    const ev = s.e || s.l || '';
    let note = '';
    if(s.mm && s.mm.length) note = s.mm.join('；');
    else if(s.st==='note') note = '标注行（无实际移动）';
    else if(s.st==='invalid') note = '2F 栅栏门未开，原路线违规，未执行';
    else if(s.st==='dead') note = 'HP 不足，路线在此暴毙';
    else if(s.st==='unreachable') note = '前段已无法继续，未执行';
    // 备注并入「事件 / 日志」列（2026-11-14）
    const evText = note ? (ev ? ev+'　['+note+']' : note) : ev;
    const tag = s.st==='note'?'<span class="tag">标注</span>'
      : s.st==='blocked'?'<span class="tag b">失败</span>'
      : s.st==='invalid'?'<span class="tag" style="background:#4a2f12;color:#ffc078">违规</span>'
      : s.st==='dead'?'<span class="tag b">暴毙</span>'
      : s.st==='unreachable'?'<span class="tag" style="background:#2a3040;color:#8b97ad">未执行</span>'
      : '';
    h += '<tr class="'+cls.trim()+'" data-i="'+i+'">'+
         '<td class="num">'+s.i+'</td>'+
         '<td>'+s.f+'F ('+s.x+','+s.y+')</td>'+
         '<td class="dir">'+(s.d||'·')+'</td>'+
         '<td class="ev" title="'+esc(evText)+'">'+tag+fmtEv(evText, s.f)+'</td>'+
         '<td>'+s.hp+'</td><td>'+s.a+'</td><td>'+s.df+'</td><td>'+s.g+'</td>'+
         '<td class="keys">'+s.ky+'/'+s.kb+'/'+s.kr+'</td>'+
         '<td>'+deltaText(s)+'</td>'+
         '</tr>';
  }
  tbody.innerHTML=h;
  tableFloor=f; lastKeyOnly=keyOnly;
  document.getElementById('tblTitle').textContent = f+'F 步骤明细';
  document.getElementById('tblSub').textContent = list.length+' / '+(byFloor[f]||[]).length+' 行';
}

function highlightRow(){
  tbody.querySelectorAll('tr.sel').forEach(function(el){el.classList.remove('sel');});
  const row = tbody.querySelector('tr[data-i="'+sel+'"]');
  if(row){
    row.classList.add('sel');
    row.scrollIntoView({block:'nearest'});
  }
}

/* ---------------- 楼层导航 ---------------- */
function renderFloors(){
  let h='';
  for(let f=0;f<=50;f++){
    const st=FL[f];
    if(!st) continue;
    const warn = ISSUES.some(function(it){return it.floor===f;});
    h += '<div class="fchip'+(warn?' warnf':'')+'" data-f="'+f+'" title="'+esc(
        f+'F  步'+st.steps+'  战损'+st.loss+'  击杀'+st.kills+'  开门'+st.doors+'  拾取'+st.pickups+
        '  最低HP'+(st.minhp==null?'-':st.minhp))+'">'+
      '<b>'+f+'F</b><i>'+st.steps+'步 · 损'+st.loss+'</i></div>';
  }
  const box=document.getElementById('floorchips');
  box.innerHTML=h;
  box.querySelectorAll('.fchip').forEach(function(el){
    el.addEventListener('click', function(){ select(firstOf[+el.dataset.f]||0); });
  });
}
function updateFloorActive(){
  const f=ST[sel].f;
  document.querySelectorAll('.fchip').forEach(function(el){
    el.classList.toggle('active', +el.dataset.f===f);
  });
}

/* ---------------- 问题清单 ---------------- */
function renderIssues(){
  const flags=[];
  const seen={};
  ISSUES.forEach(function(it){ flags.push(it); seen[it.line+'|'+(it.kind||'')]=1; });
  ST.forEach(function(s){
    if(s.mm && s.mm.length){
      const k=s.i+'|coord';
      if(!seen[k]){ seen[k]=1; flags.push({kind:'coord',line:s.i,floor:s.f,x:s.x,y:s.y,msg:s.mm.join('；')}); }
    }
  });
  flags.sort(function(a,b){return a.line-b.line;});
  const box=document.getElementById('issueList');
  if(!flags.length){ box.innerHTML='<div class="verify">无异常</div>'; }
  else{
    box.innerHTML = flags.map(function(it){
      return '<div class="issueitem" data-line="'+it.line+'">'+
        '<div class="ih"><span class="kindbadge '+(it.kind||'')+'">'+(it.kind||'issue')+'</span>'+
        '<span class="ln">第 '+it.line+' 步 · '+it.floor+'F('+it.x+','+it.y+')</span></div>'+
        '<div class="msg">'+esc(it.msg)+'</div></div>';
    }).join('');
    box.querySelectorAll('.issueitem').forEach(function(el){
      el.addEventListener('click', function(){
        const ln=+el.dataset.line;
        const idx=ST.findIndex(function(s){return s.i===ln;});
        if(idx>=0) select(idx);
      });
    });
  }
  document.getElementById('issueSub').textContent = flags.length+' 个标记点';
}

/* ---------------- 顶部摘要 ---------------- */
function renderHeader(){
  const t=D.total, f=D.final, m=D.minhp, dd=D.dead;
  let nExec=0, nInv=0, nUn=0;
  ST.forEach(function(s){ if(s.st==='ok'||s.st==='dead') nExec++; else if(s.st==='invalid') nInv++; else nUn++; });
  const chips=[
    '<span class="chip">总步数 <b>'+t.steps+'</b></span>',
    '<span class="chip ok">引擎实际执行 <b>'+nExec+'</b> 步</span>',
    '<span class="chip">累计战损 <b>'+t.loss+'</b> · 击杀 <b>'+t.kills+'</b> · 开门 <b>'+t.doors+'</b> · 拾取 <b>'+t.pickups+'</b></span>',
    (dd? '<span class="chip" style="border-color:#7a2020;color:#ffb0b0">暴毙点 <b>'+dd.floor+'F('+dd.x+','+dd.y+')</b> HP'+dd.hp+' / 需'+dd.need+'</span>' : ''),
    '<span class="chip hl" id="minhpChip">最低 HP <b>'+m[0]+'</b> @ '+m[1]+'F('+m[2]+','+m[3]+')</span>',
    // ⚠️ 2026-11-15：Toy 包内不放站外跳转链接（B站 Toy 安全扫描会判风险，审核驳回）。
    //   仓库出处改成纯文本展示，不带 href。
    '<span class="chip repo" title="源码仓库：gitcode.com/Barry_Wu_/50MOTA-AI-TAS">Gitcode 仓库</span>',
    '<span class="chip repo" title="镜像：github.com/Barry-Wuu/50MOTA-AI-TAS">Github 仓库</span>'
  ];
  document.getElementById('chips').innerHTML=chips.join('');
  document.getElementById('minhpChip').addEventListener('click', function(){
    const idx=ST.findIndex(function(s){return s.i===m[4];});
    if(idx>=0) select(idx);
  });

  document.getElementById('verifyBox').innerHTML =
    '<div><b>路线 = z2_route.py 程序化推演（1F→50F 全塔通关），mota_core 逐格实算</b>：共 <b>'+t.steps+'</b> 步，终点 50F(6,5) HP<b>'+f.hp+'</b> A<b>'+f.atk+'</b> D<b>'+f.dfn+'</b> G<b>'+f.gold+'</b> 钥 '+f.ky+'/'+f.kb+'/'+f.kr+'（真魔王已击破）。</div>'+
    '<div>关键节点：V94 大法师(A423/D402, 战损6162) → V95 26F假公主(4红门) → V96 24F竖井 ending → V97 真魔王(封印后800/500/100, 战损196)。</div>'+
    '<div style="color:#ffd98a">⚠ 变动格：<b style="color:#8fe3ff">蓝框</b>=该步起新出现的物件（10F 战利品/落穴/盗贼、41F 魔術師Ａ+降臨翼…）；<b style="color:#d7b0ff">紫框</b>=地形变化为墙/暗墙（41F 三个暗墙、24F 竖井复原）。<b>地形变地面</b>的格（37F 超级镐破整层墙、29/30F 暗道、24F 竖井）直接贴地板贴图，不再挂框。</div>'+
    '<div>剩余怪伤害 = 当前步攻防下与该怪战斗的总 HP 损失；0=绿色，越高越偏红，打不动（攻≤防）显示红色 ???。数字标在怪物格左下角。</div>';
}

/* ---------------- 选择与导航 ---------------- */
function select(i){
  i = Math.max(0, Math.min(TOTAL-1, i));
  sel = i;
  const f = ST[sel].f;
  if(f!==tableFloor || keyOnly!==lastKeyOnly) buildTable(f);
  renderState();
  renderMap();
  updateFloorActive();
  slider.value = sel+1;
  stepno.value = ST[sel].i;
  document.getElementById('stepLabel').textContent = ST[sel].i+' / '+TOTAL;
  highlightRow();
}
function nextEvent(dir){
  let i=sel+dir;
  while(i>=0 && i<TOTAL){
    if(isKeyStep(ST[i])){ select(i); return; }
    i+=dir;
  }
}
function stopPlay(){
  if(playTimer){ clearInterval(playTimer); playTimer=null; }
  document.getElementById('btnPlay').textContent='▶ 播放';
  document.getElementById('btnPlay').classList.remove('primary');
}
function togglePlay(){
  if(playTimer){ stopPlay(); return; }
  if(sel>=TOTAL-1) select(0);
  document.getElementById('btnPlay').textContent='❚❚ 暂停';
  document.getElementById('btnPlay').classList.add('primary');
  playTimer=setInterval(function(){
    if(sel>=TOTAL-1){ stopPlay(); return; }
    select(sel+1);
  }, 320);
}

document.getElementById('btnFirst').onclick=function(){ select(0); stopPlay(); };
document.getElementById('btnPrev').onclick=function(){ select(sel-1); stopPlay(); };
document.getElementById('btnNext').onclick=function(){ select(sel+1); stopPlay(); };
document.getElementById('btnLast').onclick=function(){ select(TOTAL-1); stopPlay(); };
document.getElementById('btnPrevEv').onclick=function(){ nextEvent(-1); stopPlay(); };
document.getElementById('btnNextEv').onclick=function(){ nextEvent(1); stopPlay(); };
document.getElementById('btnPlay').onclick=togglePlay;
slider.addEventListener('input', function(){ stopPlay(); select(+slider.value-1); });
document.getElementById('btnGo').onclick=function(){
  const n=parseInt(stepno.value,10);
  if(!isNaN(n)){ const idx=ST.findIndex(function(s){return s.i===n;}); if(idx>=0){ stopPlay(); select(idx); } }
};
stepno.addEventListener('keydown', function(e){ if(e.key==='Enter') document.getElementById('btnGo').click(); });
document.getElementById('keyonly').addEventListener('change', function(e){
  keyOnly=e.target.checked; buildTable(ST[sel].f); highlightRow();
});
document.getElementById('consToggle').addEventListener('change', function(e){
  showCons=e.target.checked; consumeLayer.classList.toggle('hint', showCons);
});
document.addEventListener('keydown', function(e){
  if(e.target.tagName==='INPUT' && e.target.type!=='range') return;
  if(e.key==='ArrowRight'){ e.preventDefault(); stopPlay(); select(sel+1); }
  else if(e.key==='ArrowLeft'){ e.preventDefault(); stopPlay(); select(sel-1); }
  else if(e.key==='PageDown'){ e.preventDefault(); stopPlay(); select(sel+20); }
  else if(e.key==='PageUp'){ e.preventDefault(); stopPlay(); select(sel-20); }
  else if(e.key==='Home'){ e.preventDefault(); stopPlay(); select(0); }
  else if(e.key==='End'){ e.preventDefault(); stopPlay(); select(TOTAL-1); }
});

/* ---------------- 图例 ---------------- */
document.getElementById('legend').innerHTML =
  '<span><i class="dot" style="background:#4cc9f0"></i>本层已走路径</span>'+
  '<span><i class="dot" style="background:#ff9f43;border-color:#ff9f43"></i>补丁格</span>'+
  '<span><i class="dot" style="background:#3ecf8e"></i>已消耗→地面</span>'+
  '<span><i class="dot" style="background:#3ecf8e"></i>剩余怪伤害：0=绿 · 越大越红</span>'+
  '<span>底图 = 原版贴图</span>';

/* ---------------- 对话悬浮面板 ---------------- */
const npctip = document.getElementById('npctip');
function showNpcTip(el){
  const raw = el.getAttribute('data-npc');
  if(!raw){ npctip.style.display='none'; return; }
  const flAttr = el.getAttribute('data-floor');
  const floor = (flAttr!=null && flAttr!=='') ? parseInt(flAttr,10) : null;
  const keys = raw.split('|');
  let html = '';
  keys.forEach(function(key){
    const d = NPC_DLG[key];
    if(!d) return;
    // 只显示本层台词（data-floor 提供时）；无 data-floor 则回退全部
    const ls = (floor!=null) ? d.lines.filter(function(l){ return l.f===floor; }) : d.lines;
    if(!ls.length) return;
    // 具名角色显示「日文 ⇒ 中文」；老人/商人等无日文异名的角色只显示中文名
    const head = (d.jp && d.jp !== d.zh) ? (esc(d.jp)+' ⇒ '+esc(d.zh)) : esc(d.zh);
    html += '<div class="npch">'+head+'</div>';
    ls.forEach(function(l){ html += '<div class="npcl">'+esc(l.zh)+'</div>'; });
  });
  if(!html){ npctip.style.display='none'; return; }
  npctip.innerHTML = html;
  npctip.style.display = 'block';
  const r = el.getBoundingClientRect();
  let left = window.scrollX + r.left;
  let top = window.scrollY + r.bottom + 6;
  npctip.style.left = left + 'px';
  npctip.style.top = top + 'px';
  // 防右/下溢出视口
  const tw = npctip.offsetWidth, th = npctip.offsetHeight;
  const vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;
  if(left + tw > window.scrollX + vw - 8){
    npctip.style.left = Math.max(8, window.scrollX + vw - tw - 8) + 'px';
  }
  if(top + th > window.scrollY + vh - 8){
    npctip.style.top = (window.scrollY + r.top - th - 6) + 'px';
  }
}
document.addEventListener('mouseover', function(e){
  const el = e.target.closest ? e.target.closest('[data-npc]') : null;
  if(el) showNpcTip(el);
});
document.addEventListener('mouseout', function(e){
  const el = e.target.closest ? e.target.closest('[data-npc]') : null;
  if(el) npctip.style.display = 'none';
});

/* ---------------- 初始化 ---------------- */
renderHeader();
renderIssues();
renderFloors();
/* 深链：?step=N（1 起）定位到第 N 步；?floor=F 定位到该层首次出现的那一步。
   部署到 Toy / 分享时可直接给出带参数的地址。 */
let initStep = 0;
try{
  const q = new URLSearchParams(location.search);
  const ss = q.get('step'), fs = q.get('floor');
  if(ss !== null && ss !== ''){
    const n = parseInt(ss, 10);
    if(n >= 1 && n <= TOTAL) initStep = n - 1;
  } else if(fs !== null && fs !== ''){
    const f = parseInt(fs, 10);
    for(let i = 0; i < ST.length; i++){ if(posOf(ST[i])[0] === f){ initStep = i; break; } }
  }
}catch(e){}
select(initStep);
})();
</script>
</body>
</html>
'''

if SPLIT_DIR:
    # 外链模式：data.js 装 D/IMG/TILE/STAIR/HERO/ITEMICON，index.html 只剩模板+CSS+JS
    _parts = ['window.__D=' + js, 'window.__IMG=' + img_js, 'window.__TILE=' + tile_js,
              'window.__STAIR=' + stair_js, 'window.__HERO_JSON=' + hero_js,
              'window.__ITEMICON=' + item_js]
    io.open(os.path.join(SPLIT_DIR, 'data.js'), 'w', encoding='utf-8').write(
        ';\n'.join(_parts) + ';\n')
    bind = ('window.__D', 'window.__IMG', 'window.__TILE', 'window.__STAIR',
            'window.__HERO_JSON', 'window.__ITEMICON')
    dscript = '<script src="./data.js"></script>'
    out = os.path.join(SPLIT_DIR, 'index.html')
else:
    bind = (js, img_js, tile_js, stair_js, hero_js, item_js)
    dscript = ''
    out = DED + OUT_HTML

html = (HTML.replace('__DATASCRIPT__', dscript)
            .replace('__DATA__', bind[0])
            .replace('__IMG__', bind[1])
            .replace('__TILE__', bind[2])
            .replace('__STAIR__', bind[3])
            .replace('__HERO_JSON__', bind[4])
            .replace('__ITEMICON__', bind[5])
            .replace('__TOTAL__', str(data['total']['steps']))
            .replace('__NPC_DLG__', NPC_DLG_JSON)
            .replace('__NPC_MARKS__', NPC_MARKS_JSON)
            .replace('__NPC_RE__', NPC_RE_SRC))
io.open(out, 'w', encoding='utf-8').write(html)
print('wrote', out, os.path.getsize(out), 'bytes')
