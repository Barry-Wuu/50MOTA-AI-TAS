"""生成 README「附录：塔内全部对话/提示文案」与 magic_tower1_texts.csv。

前置（与 dynscan.py 相同）：
  1) cd 08_Java_MTower08a/game && javap -c -p MTower.class > mtower.jvm
  2) 运行时导出 crops/live.json（map/mapAttribute/objectAttribute）与 javamap.json（strMessage）
用法：
  python3 tools/gen_texts.py
输出：
  texts_section.md（README 附录正文） + magic_tower1_texts.csv（309 行机读版）
"""
"""生成 01 版《魔法の塔》塔内全部文案（日/英）附录，按引用场景分组，输出 markdown 片段。

用法: python3 gen_texts.py            # 打印统计并把片段写到 texts_section.md
数据来源:
  javamap.json['strMessage']  —— '1' 日文 / '0' 英文（索引即 strNumber）
  crops/live.json            —— mapAttribute[][5] / objectAttribute[][5] 记录每条文案被谁引用
"""
import json, collections, csv, os

A = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(A, 'r', '01_PC98原版_mtower')
J = json.load(open(os.path.join(A, 'javamap.json')))['strMessage']
JP = {int(k): (v if isinstance(v, str) else str(v)) for k, v in J['1'].items()}
EN = {int(k): (v if isinstance(v, str) else str(v)) for k, v in J['0'].items()}
live = json.load(open(os.path.join(A, 'crops', 'live.json')))
ma, oa, mp, mo = live['mapAttribute'], live['objectAttribute'], live['map'], live['mapObject']
TN = {0: 'NORMAL', 1: 'MESSAGE', 3: 'STATUS', 4: 'ITEM', 5: 'DOOR', 6: 'MONSTER',
      7: 'SAIDAN', 8: 'KEY', 11: 'SCORE', 14: 'SELL', 15: 'BUY'}

# 索引 -> 引用者
refs = collections.defaultdict(lambda: {'obj': [], 'terrain': []})
for i, r in enumerate(oa):
    if r and len(r) > 5 and r[5]:
        refs[r[5]]['obj'].append(i)      # key 必须是文案索引 r[5]，不是行号
for i, r in enumerate(ma):
    if r and len(r) > 5 and r[5]:
        refs[r[5]]['terrain'].append(i)

# obj / terrain 出现在哪些层
def block_floors():
    fl = collections.defaultdict(set)
    for r in range(78):
        for c in range(130):
            band, y = divmod(r, 13); slot, x = divmod(c, 13)
            if band == 5 and slot == 9: tag = 'stage_flags'
            elif band == 5 and slot == 8: tag = 'catalog'
            elif band == 5 and slot == 1: tag = '00F'
            elif band < 5: tag = str(band * 10 + slot + 1)
            else: tag = f'b{band}s{slot}'
            o = mo[r][c]
            if o: fl['obj', o].add(tag)
            t = mp[r][c]
            if t is not None: fl['ter', t].add(tag)
    return fl
FLOORS = block_floors()

def comp(tags):
    nums = sorted({int(t) for t in tags if t.isdigit()})
    out = []
    for v in nums:
        if out and out[-1][1] + 1 == v: out[-1][1] = v
        else: out.append([v, v])
    s = ','.join(str(a) if a == b else f'{a}-{b}' for a, b in out)
    extra = sorted({t for t in tags if not t.isdigit()})
    return (s + ((' ' + ' '.join(extra)) if extra else '')) if s else ' '.join(extra)

CODE = {int(k): v for k, v in json.load(open(os.path.join(A, 'code_strnumber.json'))).items()}

def kinds_of(i):
    return {obj_kind(o) for o in refs[i]['obj']} if i in refs else set()

def obj_kind(i):
    r = oa[i] if i < len(oa) else None
    return TN.get(r[3], '?') if r and len(r) > 3 else '?'

def where(i):
    """该文案的使用位置（层列表）"""
    tags = set()
    for o in refs[i]['obj']: tags |= FLOORS.get(('obj', o), set())
    for t in refs[i]['terrain']: tags |= FLOORS.get(('ter', t), set())
    return comp(tags) if tags else '—'

def who(i):
    w = []
    for o in refs[i]['obj'][:3]: w.append(f'obj{o}')
    for t in refs[i]['terrain'][:3]: w.append(f'地形{t}')
    more = (len(refs[i]['obj']) + len(refs[i]['terrain'])) - len(w)
    return '、'.join(w) + (f' 等{more}项' if more > 0 else '')

import re
NAMED = re.compile(r'^(魔導師ゼノ|大魔導師|スケルトン[ＡＢＣ]?|バンパイア|金騎士|剣士|騎士|神|妖精|老人|勇者|プリンセス|門番|黒騎士|盗賊)「')
THIEF = re.compile(r'盗賊「|抜け穴')
ITEM  = re.compile(r'手に入れた|を使っ|がない！|を持ってない|持っていない|使えない')
SHOP  = re.compile(r'売るよ|買うか|買わな|この祭壇に|この階までの|答え|質問|情報番号|ポイント回復|ＧＯＬＤを')
TERR  = re.compile(r'が開いた|が開く|がいる|階段|壁がくずれた|溶岩|道が|通れない|入れない')
Gears = re.compile(r'^(鉄の剣|銀の剣|騎士の剣|聖\u3000剣|神\u3000剣|鉄の盾|銀の盾|騎士の盾|聖\u3000盾|神\u3000盾|勇者のオーブ|知恵のオーブ|飛翔のオーブ|十字架|エリクサー|マトック|スーパーマトック|破壊の玉|空間転移の秘宝|昇華の翼|降臨の翼|ドラゴンスレーヤー|雪の結晶|魔法の鍵|幸運の金貨)$')
FB    = re.compile(r'を使っ|できない|攻撃だ！|ポイント減少|生命力が半減|火を吹いた|をたおした|移動中|障害物')
SYS   = re.compile(r'セーブ|ロード|ランキング|Ｍ？idi|バックグラウンド|サウンド|Ver|よろしいですか|実行中|表示する情報|検索|^情報|得点|成績')
UI    = re.compile(r'^命$|^攻$|^防$|予想ダメージ|攻撃不可能|^塔$|^階$|^生命力$|^攻撃力$|^防御力$|・生命力を|・攻撃力を|・防御力を|ポイントアップ|^\u3000*ＧＯＬＤ|寄進|称号|満点|点です|レベル|^(戦士|勇者|英雄|剣帝|闘神)|^『|これから先も|おつかれ')
def classify(i):
    t = JP[i]
    if 'MONSTER' in kinds_of(i) and len(t) <= 14: return '怪物与 BOSS 名称'
    if THIEF.search(t): return '盗贼（脱出屋）对白'
    if NAMED.search(t): return '具名人物台词（ゼノ・スケルトンＡ・バンパイア・大魔導師・老人・妖精・勇者…）'
    if re.search(r'祭壇がある|空間転移した|やっぱりやめる|点数|無理がある|苦戦|なかなかの|満点です|よくがんばりました', t):
        return '战斗与道具使用反馈提示'
    if Gears.match(t): return '装备与道具名称（菜单用的短名）'
    if SYS.search(t): return '存档 · 音效 · 版本等系统提示'
    if FB.search(t): return '战斗与道具使用反馈提示'
    if ITEM.search(t): return '道具 / 装备 / 钥匙：拾取与使用'
    if SHOP.search(t): return '商人 · 祭坛 · 积分石 · 智慧之戒问答'
    if TERR.search(t): return '地形与调查提示（门、楼梯、暗墙、熔岩、人物）'
    if UI.search(t): return '界面 · 系统文案（状态窗、情報、音、得分、称号）'
    if t.startswith('「'): return '无名提示与谜面（石板/老人语气，未具名）'
    if i in refs and refs[i]['terrain']: return '地形与调查提示（门、楼梯、暗墙、熔岩、人物）'
    if i in refs and kinds_of(i) & {'SELL','BUY','SAIDAN','SCORE'}: return '商人 · 祭坛 · 积分石 · 智慧之戒问答'
    if i in refs and 'MESSAGE' in kinds_of(i): return '具名人物台词（ゼノ・スケルトンＡ・バンパイア・大魔導師・老人・妖精・勇者…）'
    if i in refs and refs[i]['obj']: return '道具与对象兜底文案（按对象类型归类）'
    return '其它未归类文案'
ORDER = ['怪物与 BOSS 名称', '装备与道具名称（菜单用的短名）', '战斗与道具使用反馈提示', '存档 · 音效 · 版本等系统提示', '盗贼（脱出屋）对白',
         '具名人物台词（ゼノ・スケルトンＡ・バンパイア・大魔導師・老人・妖精・勇者…）',
         '无名提示与谜面（石板/老人语气，未具名）',
         '道具 / 装备 / 钥匙：拾取与使用',
         '商人 · 祭坛 · 积分石 · 智慧之戒问答',
         '地形与调查提示（门、楼梯、暗墙、熔岩、人物）',
         '界面 · 系统文案（状态窗、情報、音、得分、称号）',
         '道具与对象兜底文案（按对象类型归类）', '其它未归类文案']
CATS = collections.defaultdict(list)
for i in sorted(JP): CATS[classify(i)].append(i)

def src_of(i):
    w = who(i)
    if w: return w + '（数据引用）'
    if i in CODE: return '代码 `strNumber=' + str(i) + '` ← ' + '/'.join(CODE[i])
    return '运行时按计算下标引用（未在静态数据/常量赋值中定位）'

def unesc(t):
    return t.replace(chr(92) + '"', '"').replace(chr(92) + "'", "'")

def entry(i):
    jp = unesc(JP.get(i, '')).strip(); en = unesc(EN.get(i, '')).strip()
    lines = [f'**[{i}]** 　{src_of(i)} 　·  出现层：{where(i)}', '']
    for ln in (jp or '（无）').split('\n'):
        lines.append(f'> {ln.strip()}')
    if en:
        lines.append('>')
        for n, ln in enumerate(en.split('\n')):
            lines.append(('EN: ' if n == 0 else '　　 ') + ln.strip())
    lines.append('')
    return '\n'.join(lines)

placed, cats, rows = set(), [], []
for title in ORDER:
    idxs = CATS.get(title, [])
    if not idxs: continue
    cats.append(f'### {title}（{len(idxs)} 条）\n')
    cats.append('\n'.join(entry(i) for i in idxs))
    placed |= set(idxs)
    for i in idxs:
        rows.append([i, unesc(JP.get(i, '')).replace('\n', '⏎'), unesc(EN.get(i, '')).replace('\n', '⏎'),
                     src_of(i), where(i), title])
missing = [i for i in sorted(EN) if i not in JP]
toc=' · '.join(f'{t.split("（")[0]} {len(CATS[t])}' for t in ORDER if CATS.get(t))
head = ['## 附录：塔内全部对话 / 提示文案', '',
        f'来源：`MTower.class` 运行时的 `strMessage[2][400]`（`[1]` 日文、`[0]` 英文），实际有效 **{len(JP)}** 条，'
        '索引即引擎里的 `strNumber`。机读版同内容见 `magic_tower1_texts.csv`。', '',
        '分组一览：' + toc, '',
        '每条标题行的**引用方式**有四类：', '',
        '- `objN（数据引用）` / `地形N（数据引用）`——由对象表 / 地形表的 `ATR_STRING` 列挂上，'
        '「出现层」即该对象（地形）实际铺在的楼层；',
        '- `代码 strNumber=N ← 函数名`——由指令流里 `sipush N; putfield strNumber` 直接指定'
        '（开场与战后台词、钥匙不足、菜单确认等），这类文案不挂在地图数据上；',
        '- `运行时按计算下标引用`——文案确实会在游戏里显示，但引用处的下标是算出来的'
        '（按楼层、分支、序号偏移，如盗贼台词与状态窗标签），我没能静态定位到具体引用点，'
        '所以直说"未定位"而不猜归属；',
        '- 出现层为 `—` 表示它不来自地图数据，因此没有楼层概念。', '']
if missing:
    head.append(f'注：英文数组另有 {len(missing)} 个索引没有对应日文（{missing[:8]}…），未列入正文。')
section = '\n'.join(head + cats).rstrip() + '\n'
open(os.path.join(A, 'texts_section.md'), 'w', encoding='utf8').write(section)
with open(os.path.join(D, 'magic_tower1_texts.csv'), 'w', newline='', encoding='utf8') as fh:
    w = csv.writer(fh); w.writerow(['strNumber', 'text_jp', 'text_en', 'referenced_by', 'floors', 'group'])
    w.writerows(rows)
print('条目:', len(placed), ' 片段字节:', len(section.encode()), ' CSV 行:', len(rows), ' 未覆盖:', [i for i in sorted(JP) if i not in placed][:10])
