"""
mota_core —— 《魔法の塔》(01 PC-98 / 08 Java 同源数据) 的无头游玩内核。

只保留状态与函数，不做任何绘制：地图、怪物、战斗、门与钥匙、拾取、商店/祭坛、
以及运行时改写地图的事件脚本，全部用数据 + 纯函数复现，供寻路/速通分析使用。

每条规则都标注来源：
  ✅ = 从 08_Java_MTower08a/game/MTower.class 指令流读到的算式（mtower.jvm 复核）
  📝 = 物件自带文案（objectAttribute[][5] → strMessage）里明说的数值
  ⚠️ = 推断，尚未逐条追溯到写回语句（用时会被打印成 caveat，不当结论）

坐标约定（全部用“格”单位，不再有像素）：
  层 f ∈ 1..50 → band=(f-1)//10, slot=(f-1)%10；格 (x,y) 对应大表 row=band*13+y, col=slot*13+x
  00 层 = (band 5, slot 1)；图鉴块 (5,8)、变量块 (5,9) 不作为可行走楼层。
"""

from __future__ import annotations
import json, math, os, collections, dataclasses, typing
from typing import Set, List, Tuple, Dict

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.environ.get('MOTA_ART', HERE)          # .artifacts 根目录（含 crops/、javamap.json、dyn_raw.json）

LIVE = json.load(open(os.path.join(ART, 'crops', 'live.json')))
MAPT, MAPO, MA, OA = LIVE['map'], LIVE['mapObject'], LIVE['mapAttribute'], LIVE['objectAttribute']
SMX = json.load(open(os.path.join(ART, 'javamap.json')))['strMessage']
TEXT_JP = {int(k): v for k, v in SMX['1'].items() if isinstance(v, str)}
TEXT_EN = {int(k): v for k, v in SMX['0'].items() if isinstance(v, str)}
DYNEV = json.load(open(os.path.join(ART, 'dyn_raw.json'))) if os.path.exists(os.path.join(ART, 'dyn_raw.json')) else {'obj': [], 'ter': []}

KIND = {0: 'floor', 1: 'wall', 2: 'stair'}
TYPE = {0: 'NORMAL', 1: 'MESSAGE', 3: 'STATUS', 4: 'ITEM', 5: 'DOOR', 6: 'MONSTER',
        7: 'SAIDAN', 8: 'KEY', 11: 'SCORE', 14: 'SELL', 15: 'BUY'}

# ---- 地图访问 ---------------------------------------------------------------
BAND_SLOT = {}                                  # 层号 -> (band, slot)
for _f in range(1, 51):
    BAND_SLOT[_f] = ((_f - 1) // 10, (_f - 1) % 10)
BAND_SLOT[0] = (5, 1)                           # 00 层


def rc(f, x, y):
    b, s = BAND_SLOT[f]
    return b * 13 + y, s * 13 + x


def terrain(f, x, y):
    r, c = rc(f, x, y)
    return MA[MAPT[r][c]][3] if 0 <= r < 78 and 0 <= c < 130 and MAPT[r][c] < len(MA) else 1


def stair_up(f, x, y):
    """kind==2 的地形：crop 34=上行、35=下行 ✅（楼梯链 49/49 已验证）"""
    r, c = rc(f, x, y)
    return MA[MAPT[r][c]][1] == 34


def obj_raw(f, x, y):
    r, c = rc(f, x, y)
    return MAPO[r][c] if 0 <= r < 78 and 0 <= c < 130 else 0


def oatr(o, col):
    r = OA[o] if o < len(OA) else None
    return (r[col] if r and len(r) > col else 0) or 0


def oname(o):
    return TEXT_JP.get(oatr(o, 5), '')


def stairs_of(f):
    up = dn = None
    for y in range(13):
        for x in range(13):
            if terrain(f, x, y) == 2:
                (up := (x, y)) if stair_up(f, x, y) else (dn := (x, y))
    return up, dn


STAIRS = {f: stairs_of(f) for f in BAND_SLOT}
# 49F 没有 crop35 的下行梯：其"入口格"就是 eventMT 放 obj57（假魔王/魔导师ゼノ）的 (6,3)
# （写入点 `bipush 110; bipush 55; Zeno(g,col,row)` → slot8 x=6、band4 y=3 ✅）
if STAIRS[49][1] is None:
    STAIRS[49] = (STAIRS[49][0], (6, 3))

# ---------------------------------------------------------------------------
# 物件语义（默认按类型；个别 obj 有特例）
# ---------------------------------------------------------------------------
KEY_OF = {1: 'y', 3: 'b', 28: 'r'}                  # 📝 黄/蓝/红钥匙
DOOR_OF = {2: 'y', 4: 'b', 27: 'r'}                 # ⚠️ 门色按 id 顺序推断，尚未从指令流确认
SOLID_TYPES = {5, 7, 11, 14, 15}                   # DOOR/SAIDAN/SCORE/SELL/BUY：撞上而非穿过
DECOR_PASS = {21, 23}                             # 饰件：可踩；obj19 实机验证不可踩（np2kai 实测 2026-10，撞击无位移）

# ---- 商店（BUY/SELL 物件按 id 直接建模，避免 type14/15 命名歧义） ----------
# 依据：yesnoJudge 中 mdataBuff==id 分支（mtower.jvm 行 25143 起）+ OA[id][13]=价格。
#   41 → 7F 商人「鍵を５個セットで５０ＧＯＬＤ」= 5 把黄钥（✅ 指令流 [74][118]+=5）
#   18 → 6F 紫钥店（实际给蓝钥 [75][118]+=1，✅ 指令流）
#   156/159/162/164/166/168/170 为其它楼层商店（本路线只用到 41）
SHOP = {41, 18, 156, 159, 162, 164, 166, 168, 170}
SHOP_PRICE = {}                                     # obj -> 价格（从 OA 读，下面填）
SHOP_GRANT = {                                      # obj -> (资源, 数量) 列表
    41: [('y', 5)],
    18: [('b', 1)],
    156: [('r', 1)],
    159: [('b', 1)],
    162: [('y', 4), ('b', 1)],
    164: [('y', 3)],
    166: [('b', 3)],
    168: [('hp', 2000)],
    170: [('item', 170)],
}
for _o in SHOP:
    SHOP_PRICE[_o] = oatr(_o, 13)
PICKUP_TYPES = {3, 4, 8}                            # STATUS/ITEM/KEY：踏入即拾取
MONSTER_TYPE = 6

MAGIC_HALF_ATK = {58, 96}       # ⚠️ 魔导师/大魔导师战斗前削减主角 HP（我从未在指令流里逐条确认）
# 📝 盗贼凿墙事件（dynamic.csv 实证：触发格 obj88 MESSAGE「…大ダコが道をふさいでいて…抜け穴が…」，
#    目标格 directCheck 墙→地板；35F(5,10)→35F 暗道同机制）。键=被挖开的墙格，值=盗贼触发格
DIG_WALLS = {(15, 8, 1): (15, 9, 1),
             (35, 4, 9): (35, 5, 10)}                # 35F 同机制（dynamic.csv L137 / L68 盗贼）
DIG_TRIG = {v: k for k, v in DIG_WALLS.items()}   # 触发格 → 被挖开的墙格
# 📝 祭坛（README「祭壇」节：4 座 4F/12F/32F/46F，obj22 type=7）
#    4 项菜单：生命力 / 攻击力 / 防御力 / 取消（yesnoNumber=9，文案 206/207-）
ALTAR_CELLS = {(4, 6, 1), (12, 6, 9), (32, 10, 10), (46, 6, 1)}   # ✅ 引擎 obj_raw 实测坐标
ALTAR_GAIN = {'hp': 200, 'atk': 10, 'dfn': 10}    # 档位常量（saidan 绘制数值）


def altar_cost(k):
    """代价按本存档累计已祭次数 k 递增：((k+1)^2-(k+1)+2)*10 → 20/40/80/140/220/320…
    ⚠︎ k 自增的那一步未逐条追到语句（README 原注），按 k=已祭次数推断。"""
    return ((k + 1) ** 2 - (k + 1) + 2) * 10


# 📝 双倍伤害（MAP_NOTES §：持有十字架 obj103 → 对 id 48/49/59 翻倍；屠龙匕 obj109 → 对 id 74 翻倍）
DOUBLE_DMG_ITEM = {103: {48, 49, 59}, 109: {74}}
ATK_DOUBLE_IF = {(103,): {48, 49, 59}, (109,): {74}}   # 📝 十字架对ゾンビ系、屠龙匕对ドラゴン：我方伤害×2（attackDouble）
# 📝 MESSAGE（挡路 NPC）交互：谈完即从地图上消失，效果取自其文案括号内的明示数值
MSG_EFFECT = {
    152: ('pct3', None),      # 「攻撃力と防御力を３％だけあげてやろう」
    153: ('item', 24),        # 授けるのは 勇者のオーブ（obj24：鑑定器）
    174: ('gold', 1000),      # 「１０００ＧＯＬＤもらった!」
    87:  ('none', None),      # 盗贼脱走：同事件把 2F(2,7) 的墙挖通（已在 TRAP 里做）
    88:  ('none', None), 151: ('none', None), 173: ('none', None), 175: ('none', None),
    44:  ('none', None),      # 勇者「人形だっ！」
}

LUCKY_GOLD = 113                                      # 📝 幸运金币：击杀 GOLD×2
SEAL_TARGET = 57                                      # ✅ 封印后 objectAttribute[57][10/11/12] 改写 800/500/100


@dataclasses.dataclass
class Hero:
    hp: int = 0
    atk: int = 0
    dfn: int = 0
    gold: int = 0
    keys: typing.Counter = dataclasses.field(default_factory=collections.Counter)
    items: Set = dataclasses.field(default_factory=set)
    f: int = 1
    x: int = 6
    y: int = 11

    @staticmethod
    def initial():
        # ✅ 实机读取：mapObject[66..69][118] = 1000/100/100/0；1F 起点格 (6,11)
        h = Hero(hp=1000, atk=100, dfn=100, gold=0, f=1, x=6, y=11)
        return h

# ---------------------------------------------------------------------------
# 楼梯落点（权威）：每一格楼梯 tile 在其 MA 条目里直接存着目的地——
#   MA[idx][16] = 大表全局列(col)，MA[idx][17] = 大表全局行(row)。
#   解码 (col,row) → (目标层,x,y) 即得到"踩上去之后的落点"。
#   关键修正：原始数据里落点与"相邻层的另一道楼梯"相差一格
#   （如 1F 上梯落在 2F(1,2) 而非 2F(1,1)，2F 上梯落在 3F(2,11) 而非 3F(1,11)）。
#   所以"踩上楼就落到另一道楼梯"的旧约定是错的，必须用本 warp 表。
#   交叉验证：mk_enter.py 旧注释的 2F(1,2)/3F(2,11)/4F(11,10) 正是来自本表，与解码值完全一致。
# ---------------------------------------------------------------------------
def _decode_global(col, row):
    band, slot = row // 13, col // 13
    return band * 10 + slot + 1, col % 13, row % 13


WARP = {}                       # (f, x, y) -> (目标层, x, y)，来自 MA[16]/MA[17]
for _f in BAND_SLOT:
    for _y in range(13):
        for _x in range(13):
            if terrain(_f, _x, _y) == 2:
                _r, _c = rc(_f, _x, _y)
                _idx = MAPT[_r][_c]
                _col, _row = MA[_idx][16], MA[_idx][17]
                if _col == 0 and _row == 0:
                    continue
                WARP[(_f, _x, _y)] = _decode_global(_col, _row)


# 仅保留"无楼梯 tile、靠事件触发"的特殊过渡：49F 击败假魔王后入 50F。
UP_PATCH = {
    49: ((6, 3), 50, (6, 5)),       # 49F 无上楼梯格；(6,3) 是 eventMT 放 obj57 假魔王的格
                                    #    `bipush 110; bipush 55; Zeno(...)`；50F 无楼梯格，
                                    #    真魔王落在 (6,5)：`bipush 123; bipush 57; Zeno2(...)`
}


def warp_to(f, x, y):
    """站在楼梯格 (f,x,y) → (目标层, 落点x, 落点y)；非楼梯或无法通行返回 None。"""
    if (f, x, y) in WARP:
        return WARP[(f, x, y)]
    if f in UP_PATCH and (x, y) == UP_PATCH[f][0]:
        return UP_PATCH[f][1], UP_PATCH[f][2]
    return None


# ---------------------------------------------------------------------------
# 事件脚本：数据写入 + 3F 扒装丢牢（唯一有完整指令证据的剧本）
# ---------------------------------------------------------------------------
FLOOR_WRITES = collections.defaultdict(list)          # 层 -> [(x,y,obj)] 静态之外的常量写入
for e in DYNEV.get('obj', []):
    if e['floor'].isdigit():
        FLOOR_WRITES[int(e['floor'])].append((e['x'], e['y'], e['obj']))
TERR_WRITES = collections.defaultdict(list)
for e in DYNEV.get('ter', []):
    if e['floor'].isdigit():
        TERR_WRITES[int(e['floor'])].append((e['x'], e['y'], e['to']))

_TRAP_GUARD_CELLS = set()          # 由剧本自己放置的格，不进"进层即写入"集合（在下面填）

TRAP_3F = dict(                                        # ✅ 指令行 31937/32084/32094/32107/32325..32404
    trigger=(5, 9),                                    #    中央格＝勇者所站处
    set_hp=400, set_atk=10, set_dfn=10,
    guards=[(5, 8), (4, 9), (6, 9), (5, 10)],           #    四只 obj58 魔导师
    guard_obj=58,
    texts=[222, 223],
    # 落点：loadMapData2 静态把 mapAttribute[116][16/17]=1/66 → mapX=0,mapY=5 → 大表块(band5,slot0) 的 (1,1)
    # 该块是 13×13 全空房间；剧本后续阶段再把勇者接回 2F（这段我没跟完 ⚠️），故默认不做位移。
    drop_floor=2, drop_cell=(4, 8),   # ✅ 实测（Java 版 Headless8 无头驱动）：过场结束后英雄落在 2F(4,8)
    #   （先前推测 (3,8)「盗贼正下方邻格」有误；盗贼 obj87 在 (3,7)，(4,8) 才是接人点）
    # 空块 (band5,slot0)(1,1) 只是演出用的空白，不再当落点用
)

# ---------------------------------------------------------------------------
# World：可复制的游玩状态。move() 是唯一的"按键"，返回动作记录。
# ---------------------------------------------------------------------------
WALKABLE = set(range(0, 51))


def base_cells():
    d = {}
    for f in WALKABLE:
        for y in range(13):
            for x in range(13):
                o = obj_raw(f, x, y)
                if o:
                    d[(f, x, y)] = o
    return d


@dataclasses.dataclass
class World:
    hero: Hero = None
    cells: Dict = None           # 只读底图（一次构造）
    over: Dict = None            # 稀疏覆盖：被击杀/开门/拾取后的变化
    ter_over: Dict = None        # 稀疏地形覆盖：(f,x,y)->新地形id（剧本造/拆墙）
    cleared: Set = None
    applied_events: Set = None
    trap_done: bool = False
    flag3F: int = 0
    event_mode: str = 'on_entry'
    trap_mode: str = 'apply'          # apply=踩中央即吃剧本 / avoid=把中央格当禁行（反事实）
    caveats: Set = None
    bought: Set = None                # 已购物的商人格子（防重复购买）
    boss10: bool = False             # 10F BOSS（obj16 スケルトンＡ）已击败 → (6,11) 生上行梯
    boss20: bool = False             # 20F BOSS（obj59 バンパイア/吸血鬼）已击败 → (20,6,1) 现出上行梯
    altar_k: int = 0                  # 📝 本存档累计祭坛已使用次数（决定下一次代价）
    altar_policy: str = 'atk'         # 📝 祭坛菜单选择：hp / atk / dfn（A* 无法处理菜单，按策略预设）

    @classmethod
    def new(cls, event_mode='on_entry', hero=None, trap_mode='apply'):
        w = cls(hero=hero or Hero.initial(), cells=base_cells(), over={}, ter_over={}, cleared=set(),
                applied_events=set(), event_mode=event_mode, trap_mode=trap_mode, caveats=set(),
                bought=set(), boss10=False, boss20=False)
        w.apply_floor_events(w.hero.f)
        return w

    # -- 事件写入 ----------------------------------------------------------
    def apply_floor_events(self, f):
        if self.event_mode != 'on_entry' or f in self.applied_events:
            return
        self.applied_events.add(f)
        for x, y, o in FLOOR_WRITES.get(f, []):
            if (f, x, y) in _TRAP_GUARD_CELLS:
                continue                                  # 属于 3F 剧本，触发时才放
            base = self.cells.get((f, x, y), 0)
            if base and TYPE.get(oatr(base, 3)) == 'MONSTER':
                continue                                  # ✅ 该格静态是怪/BOSS，事件写入不得覆盖（否则 BOSS 消失、怪免打）
            if o:
                self.set_at(f, x, y, o)

    # -- 查询 --------------------------------------------------------------
    def at(self, f, x, y):
        k = (f, x, y)
        if k in self.cleared:
            return 0
        if k in self.over:
            return self.over[k]
        return self.cells.get(k, 0)

    def set_at(self, f, x, y, o):
        self.over[(f, x, y)] = o

    def terrain_at(self, f, x, y):
        t = self.ter_over.get((f, x, y))
        if t is not None:
            return MA[t][3] if t < len(MA) else 1
        return terrain(f, x, y)

    def battle(self, o):
        """返回 (我方掉血, 得到GOLD) 或 None（打不动）✅ 已验证算式"""
        h = self.hero
        hp, atk, dfn, gold = oatr(o, 10), oatr(o, 11), oatr(o, 12), oatr(o, 13)
        mult = 2 if (o in {48, 49, 59} and 103 in h.items) or (o == 74 and 109 in h.items) else 1
        per = h.atk * mult - dfn
        if hp <= 0 or per <= 0:
            return None
        turns = math.ceil(hp / per)
        loss = max(atk - h.dfn, 0) * (turns - 1)
        return loss, gold * (2 if LUCKY_GOLD in h.items else 1)

    # -- 动作：朝 (dx,dy) 走一步 -------------------------------------------
    def move(self, dx, dy):
        h = self.hero
        f, x, y = h.f, h.x, h.y
        nx, ny = x + dx, y + dy
        if self.terrain_at(f, nx, ny) == 1:
            # 📝 盗贼凿墙：触发格(盗贼)交谈后进 cleared，对应墙格即变成可通行的暗道
            if DIG_WALLS.get((f, nx, ny)) not in self.cleared:
                return ['blocked:墙']               # 未触发=普通墙；触发后直接放行（log 由落格时带出）
        o = self.at(f, nx, ny)
        # ✅ 修正（此处原为死锁 bug）：20F 的「进入」与「离开」是两套独立机制，不能混为一谈。
        #    · 进入：玩家踏上触发点 (6,8) 后，由剧情自动开门 —— 见 Java 源码
        #      MTower.java:3080：displayDoor(123,22,4)（开门动画）→ mapObject[22][123]=20
        #      （(6,9) 变为可通行装饰）→ banpaia()（吸血鬼登场）→ strNumber=19。
        #      门既不消耗红钥匙，也不要求 boss20。
        #    · 离开：击败 (6,6) 吸血鬼后置 boss20=True，(20,6,1) 才现出上行梯（下方 warp 逻辑，原本正确）。
        #    旧代码把「进入」误绑到 boss20 上，造成「要杀 BOSS 才开门、而 BOSS 就在门后 (6,6)」
        #    的死锁，20F BOSS 永远打不到。现按源码语义移除该判断。
        log = []
        ty = TYPE.get(oatr(o, 3), '?') if o else '空'
        if o:
            if o == 89:                                   # 📝 暗墙：撞了就塌
                self.cleared.add((f, nx, ny)); log.append('撞塌暗墙 obj89'); o = 0; ty = '空'
                if (f, nx, ny) in ((19, 6, 3), (19, 6, 4)):   # 📝 19F 十字暗墙：撞开获得十字架 obj103
                    h.items.add(103); log.append('获得十字架 obj103（对吸血鬼等伤害翻倍）')
            elif o == 79:                                # ⚠️ 熔岩：非战斗危险格，每步 -200 HP
                if h.hp <= 200:                          #    （MAP_NOTES §4 实证：13F 80 格 / 26F 18 格）
                    return ['熔岩烫死（HP%d ≤ 200，进不去了）' % h.hp]
                h.hp -= 200
                self.cleared.add((f, nx, ny)); log.append('踩熔岩 obj79 掉血200'); o = 0; ty = '空'
            elif o == 115:                                # ⚠️ 隐形块（GO 0F 字形等）按可走处理
                log.append('隐形块 obj115 视为可走(caveat)'); self.caveats.add('obj115 可通行未指令流确认'); o = 0
            elif ty == 'MONSTER':
                r = self.battle(o)
                if r is None:
                    return [f'打不动 obj{o} {oname(o)[:10]}']
                loss, gold = r
                if o in MAGIC_HALF_ATK:
                    h.hp = math.ceil(h.hp / 2); log.append(f'{oname(o)[:6]} 半血(⚠️未证)'); self.caveats.add('MAGIC_HALF_ATK 未指令流确认')
                if h.hp - loss <= 0:
                    return [f'打不过 obj{o}（需掉血 {loss}，剩 {h.hp}）']
                h.hp -= loss; h.gold += gold; self.cleared.add((f, nx, ny))
                log.append(f'击杀 obj{o} {oname(o)[:8]} 掉血{loss} +金{gold}')
                if f == 49:
                    self.after_49(log)
                if f == 10 and o == 16:
                    self.boss10 = True
                    log.append('★击败10F BOSS(スケルトンＡ) → 10F(6,11) 将生上行梯')
                if f == 20 and o == 59:
                    self.boss20 = True
                    log.append('★击败20F BOSS(バンパイア/吸血鬼) → 20F(6,1) 现出上行梯')
                o = 0
            elif ty == 'DOOR':
                col = DOOR_OF.get(o)
                if col is None:
                    self.cleared.add((f, nx, ny)); log.append(f'未知门 obj{o} 视为已开(⚠️)'); self.caveats.add('DOOR 颜色未确认')
                elif h.keys[col] <= 0:
                    return [f'无{ {"y":"黄","b":"蓝","r":"红"}[col] }钥匙，门 obj{o} 开不了']
                else:
                    h.keys[col] -= 1; self.cleared.add((f, nx, ny))
                    log.append(f'开{ {"y":"黄","b":"蓝","r":"红"}[col] }门 obj{o}'); return log
            elif o in KEY_OF:
                h.keys[KEY_OF[o]] += 1; self.cleared.add((f, nx, ny)); log.append(f'拾 {oname(o)[:10]}'); o = 0
            elif ty in ('STATUS', 'ITEM'):
                self.pick(o, log); self.cleared.add((f, nx, ny)); o = 0
            elif o in DECOR_PASS:
                log.append(f'踩过装饰 obj{o}'); o = 0
            elif o in SHOP:
                price = SHOP_PRICE.get(o, 0)
                if (f, nx, ny) in self.bought:
                    self.cleared.add((f, nx, ny)); log.append(f'已过商店 obj{o}'); o = 0
                elif h.gold < price:
                    return [f'买不起 obj{o}（需{price}G，仅{h.gold}G）']
                else:
                    h.gold -= price
                    for res, n in SHOP_GRANT.get(o, []):
                        if res == 'y': h.keys['y'] += n
                        elif res == 'b': h.keys['b'] += n
                        elif res == 'r': h.keys['r'] += n
                        elif res == 'hp': h.hp += n
                        elif res == 'item': h.items.add(n)
                    self.bought.add((f, nx, ny))
                    self.cleared.add((f, nx, ny))   # 买后该格变可走（obj155 占位）
                    log.append(f'购物 obj{o} 花{price}G -> {SHOP_GRANT.get(o)}')
                    return log                       # 英雄不移动（对话确认后仍在原格）
            elif ty == 'MESSAGE':
                kind, val = MSG_EFFECT.get(o, ('none', None))
                if kind == 'pct3':
                    b_a, b_d = h.atk, h.dfn
                    h.atk, h.dfn = int(h.atk * 1.03) or 1, int(h.dfn * 1.03) or 1
                    log.append(f'NPC obj{o} 交谈后消失：攻{b_a}→{h.atk} 防{b_d}→{h.dfn}（+3%，取整）')
                elif kind == 'gold':
                    h.gold += val; log.append(f'NPC obj{o} 交谈后消失：+{val} GOLD')
                elif kind == 'item':
                    h.items.add(val); log.append(f'NPC obj{o} 交谈后消失：获得 obj{val}')
                else:
                    log.append(f'NPC obj{o} 交谈后消失')
                self.cleared.add((f, nx, ny))                 # 📝 谈完让路 ✅ 老人/盗贼不常驻
            elif ty == 'SCORE':
                # 📝 仙女评分(obj69)：可交谈通过，不是墙。写死成不可通行会把 10F(6,4) 这一竖道封死、BOSS 到不了
                log.append(f'评分 NPC obj{o}（交谈通过）'); self.cleared.add((f, nx, ny)); o = 0
            elif ty == 'SAIDAN':
                # 📝 祭坛：4 项菜单在 A* 里无法表达，按 altar_policy 预设选择；代价随累计次数递增
                if (f, nx, ny) in ALTAR_CELLS:      # 可反复献祭，只受金币与递增代价限制
                    c = altar_cost(self.altar_k)
                    if h.gold < c:
                        return ['祭坛金币不足（需%d，有%d）' % (c, h.gold)]
                    h.gold -= c
                    pol = self.altar_policy if self.altar_policy in ALTAR_GAIN else 'atk'
                    if pol == 'hp':
                        h.hp += ALTAR_GAIN['hp']
                    elif pol == 'atk':
                        h.atk += ALTAR_GAIN['atk']
                    else:
                        h.dfn += ALTAR_GAIN['dfn']
                    self.altar_k += 1
                    log.append('祭坛献金%dG → %s+%d（第%d次，下次%dG）'
                               % (c, pol, ALTAR_GAIN[pol], self.altar_k, altar_cost(self.altar_k)))
                else:
                    return [f'不可通行 obj{o}（{ty}）']
            elif ty == 'NORMAL':
                log.append(f'踩过 type0 装饰 obj{o}'); o = 0   # ✅ type0=NORMAL 地板装饰，可踩（obj20 等）
        # 落格
        h.x, h.y = nx, ny
        if (f, nx, ny) in DIG_TRIG:                   # 📝 盗贼格是 eventMT 动态生成（静态表 obj=0），
            self.cleared.add((f, nx, ny))             #    踩到即交谈，凿开对应墙格
            log.append('盗賊「…大ダコの抜け穴がようやく…」→ 凿开暗道 %s' % (DIG_TRIG[(f, nx, ny)],))
        if self.terrain_at(f, nx, ny) == 2:
            w = warp_to(f, nx, ny)
            if w:
                h.f, h.x, h.y = w
                log.append(f'楼梯 → {h.f}F')
                self.apply_floor_events(h.f)
        elif f == 10 and self.boss10 and (nx, ny) == (6, 11):
            # ✅ 10F BOSS 死后 eventMT 把 map[11][123]=22（10F(6,11) 上行梯）→ MA[22] warp=(11,6,10)
            # 该格静态地形是地板(0)，故必须放在 terrain==2 分支之外判断，否则永不触发
            h.f, h.x, h.y = (11, 6, 10)
            log.append('楼梯 → 11F（BOSS 死后上行梯）')
            self.apply_floor_events(11)
        elif f == 20 and self.boss20 and (nx, ny) == (6, 1):
            # ✅ 20F 同构：杀吸血鬼后 (6,1) 封印解除现出上行梯 → 21F(6,2)。
            # 证据：21F(6,1) 静态下梯 warp=(20,6,2)，按 10F↔11F 同坐标配对规则，
            # 20F 的上行梯就在 (6,1)（即顶部花纹封印格，dynamic_terrain to:[50]）。
            # 该格静态地形是地板(1)，与 10F 一样必须放在 terrain==2 分支之外。
            h.f, h.x, h.y = (21, 6, 2)
            log.append('楼梯 → 21F（吸血鬼死后上行梯）')
            self.apply_floor_events(21)
        if h.f == 3 and (nx, ny) == TRAP_3F['trigger'] and not self.trap_done:
            h.x, h.y = nx, ny
            return self.do_trap3F(log)
        # 剧本收尾后的通路：盗贼挖开的 2F(2,7) 由 ter_over 生效，这里只把「四角撤走」标清楚
        
        if h.f == 3 and self.trap_mode == 'avoid' and (nx, ny) == TRAP_3F['trigger']:
            return ['避开3F中央(反事实)']
        return log

    def pick(self, o, log):
        h = self.hero
        hp, atk, dfn = oatr(o, 10), oatr(o, 11), oatr(o, 12)
        if hp: h.hp += hp
        if atk: h.atk += atk
        if dfn: h.dfn += dfn
        if TYPE.get(oatr(o, 3)) == 'ITEM':
            h.items.add(o)
        log.append(f'拾取 obj{o} {oname(o)[:14]} (HP+{hp} ATK+{atk} DEF+{dfn})')

    def do_trap3F(self, log):
        h, t = self.hero, TRAP_3F
        if self.trap_mode == 'avoid':
            h.x, h.y = h.x, h.y
            return ['3F 中央被禁行(反事实)']
        self.trap_done = True; self.flag3F = 1
        h.hp, h.atk, h.dfn = t['set_hp'], t['set_atk'], t['set_dfn']
        for gx, gy in t['guards']:
            self.set_at(3, gx, gy, t['guard_obj'])
        if t['drop_cell']:
            h.f, (h.x, h.y) = t['drop_floor'], t['drop_cell']
        # —— 剧本收尾（同一函数内一次做完，实测三段写入见下行说明）——
        for gx, gy in t['guards']:
            self.set_at(3, gx, gy, 0)                      # 四只魔导师撤走
        self.ter_over[(3, 5, 9)] = 1                       # ✅ line23394 传送门复成普通地板
        self.ter_over[(2, 2, 7)] = 1                       # ✅ line23316 盗贼挖开牢房墙
        h.f, (h.x, h.y) = t['drop_floor'], t['drop_cell']
        log.append(f'★3F 剧本：HP→400、ATK/DEF→10（神装被收）→ 丢到 {h.f}F 盗贼牢房 '
                   f'→ 四角撤走、3F(5,9) 复原、2F(2,7) 被挖通')
        return log

    def after_49(self, log):
        guards = [(x, y) for x, y, o in FLOOR_WRITES.get(49, []) if o == 58]
        left = [g for g in guards if self.at(49, g[0], g[1]) == 58]
        if not left and not self.at(49, 6, 3):
            self.set_at(49, 6, 3, SEAL_TARGET)
            globals()['OA'][SEAL_TARGET][10:13] = [800, 500, 100]       # ✅ 封印改写
            log.append('★49F 封印完成：四周围杀尽 → (6,3) 出现 obj57，其四维改写为 800/500/100')

# ---------------------------------------------------------------------------
# 规划：Dijkstra，代价 = (累计掉血, 步数)；状态含已拾取格子的掩码（防"重复捡"作弊），
# 怪物/门不做掩码（重访会重复付费 ⇒ 只会偏保守，不会偏乐观）。
# ---------------------------------------------------------------------------
import heapq as _hq
from collections import deque
_TIE = iter(range(10 ** 9))


def _key(w):
    return (w.hero.f, w.hero.x, w.hero.y, w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
            w.hero.atk if False else w.hero.keys['y'], frozenset(sorted(w.cleared & ITEMISH)))


BLOCK_WORDS = ('blocked', '打不动', '打不过', '不可通行', '无黄', '无蓝', '无红')

def blocked(log):
    return bool(log) and any(t in log[0] for t in BLOCK_WORDS)

_HST = {}


def heuristic(goal_cell):
    """下界：忽略怪物/门/剧情、只把墙当障碍的最短格数（跨层用楼梯连通）。可采纳。"""
    key = goal_cell
    if key in _HST:
        return _HST[key]
    import collections as C
    dist = {}
    gq = deque([goal_cell]); dist[goal_cell] = 0
    while gq:
        f, x, y = gq.popleft(); d = dist[(f, x, y)]
        nb = []
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 13 and 0 <= ny < 13 and terrain(f, nx, ny) != 1:
                nb.append((f, nx, ny))
        if terrain(f, x, y) == 2:
            w = WARP.get((f, x, y))
            if w and terrain(w[0], w[1], w[2]) != 1:
                nb.append(w)
        for c in nb:
            if c not in dist:
                dist[c] = d + 1; gq.append(c)
    _HST[key] = dist
    return dist


def plan(goal, event_mode='on_entry', max_states=400000, beam=None, trap_mode='apply', goal_cell=None, start=None):
    """goal(f,x,y)->bool 命中即停。返回 (世界, 路径) 或 None 或 ('cap',...)。
    start：外传起点世界（如铁剑路线终态），None 则按 Hero.initial() 新建。"""
    start = start if start is not None else World.new(event_mode=event_mode, trap_mode=trap_mode)
    start._par = None                      # 切断外传起点的父链，路径只含本段
    H = heuristic(goal_cell) if goal_cell else None
    h0 = (H or {}).get((start.hero.f, start.hero.x, start.hero.y), 0)
    pq = [(h0, 0, 0, start)]
    seen = {}
    n = 0
    while pq:
        loss, steps, _, w = _hq.heappop(pq)
        if goal(w.hero.f, w.hero.x, w.hero.y):
            path = []
            cur = w
            while cur is not None:
                path.append((cur.hero.f, cur.hero.x, cur.hero.y, cur.hero.hp))
                cur = getattr(cur, '_par', None)
            return w, list(reversed(path))
        n += 1
        # atk/dfn/gold 都由「已拾取掩码」唯一决定，放进键里只会让状态数爆炸，故不放
        k = (w.hero.f, w.hero.x, w.hero.y, w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'],
             frozenset(c for c in w.cleared if c in PICKUP_CELLS), frozenset(w.bought))
        if k in seen and seen[k][0] <= loss and seen[k][1] <= steps:
            continue
        seen[k] = (loss, steps)
        if n > max_states:
            return ('cap', n)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            before = (w.hero.hp, w.hero.f, w.hero.x, w.hero.y)
            w2 = w.clone()
            log = w2.move(dx, dy)
            if blocked(log):
                continue
            add = before[0] - w2.hero.hp
            w2._par = w
            ns = steps + 1
            nh = (H or {}).get((w2.hero.f, w2.hero.x, w2.hero.y), 0)
            _hq.heappush(pq, (loss + max(add, 0) + nh * 1000000, ns, next(_TIE), w2))
    return None            # 队列自然耗尽 = 图不可达（与撞上限区分）


def PICKUP_CELLS_FN():
    cs = set()
    for (f, x, y), o in base_cells().items():
        if TYPE.get(oatr(o, 3)) in ('STATUS', 'ITEM') or o in KEY_OF:
            cs.add((f, x, y))
    return frozenset(cs)


PICKUP_CELLS = PICKUP_CELLS_FN()


def _clone(self):
    import copy as _c
    w = World.__new__(World)
    w.hero = _c.copy(self.hero); w.hero.keys = collections.Counter(self.hero.keys)
    w.hero.items = set(self.hero.items)
    w.cells = self.cells                            # 底图共享（只读）
    w.over = dict(self.over)
    w.cleared = set(self.cleared); w.applied_events = set(self.applied_events)
    w.trap_done = self.trap_done; w.flag3F = self.flag3F
    w.ter_over = dict(self.ter_over)
    w.event_mode = self.event_mode; w.trap_mode = self.trap_mode; w.caveats = set(self.caveats)
    w.bought = set(self.bought); w.boss10 = self.boss10; w.boss20 = self.boss20
    w.altar_k = self.altar_k; w.altar_policy = self.altar_policy
    return w


World.clone = _clone


def make_goal(spec):
    """spec: 'sword'(5F 铁剑) / 'f<N>' / 'N:x,y'"""
    if spec == 'sword':
        for y in range(13):
            for x in range(13):
                if obj_raw(5, x, y) == 30:
                    tx, ty = x, y
        return (5, tx, ty)
    if spec.startswith('f'):
        return (int(spec[1:]), None, None)
    f, x, y = spec.split(':')
    return (int(f), int(x), int(y))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='魔塔无头内核')
    ap.add_argument('cmd', choices=['selftest', 'route', 'probe'])
    ap.add_argument('--to', default='sword')
    ap.add_argument('--events', default='on_entry', choices=['on_entry', 'static'])
    ap.add_argument('--trap', default='apply', choices=['apply', 'avoid'])
    a = ap.parse_args()
    if a.cmd == 'selftest':
        assert World.new(trap_mode='avoid').clone().trap_mode == 'avoid', 'clone 丢字段'
        assert World.new().event_mode == 'on_entry'
        w = World.new()
        print('起点', w.hero.f, (w.hero.x, w.hero.y), 'HP/ATK/DEF', w.hero.hp, w.hero.atk, w.hero.dfn)
        print('可拾取格数', len(PICKUP_CELLS), ' 事件写入涉及层', len(FLOOR_WRITES))
        for d in ((0, -1), (-1, 0), (1, 0), (1, 0)):
            print(' move', d, w.move(*d), '->', (w.hero.f, w.hero.x, w.hero.y), dict(w.hero.keys))
    else:
        g = make_goal(a.to)
        print('目标', g, '事件模式', a.events)
        r = plan(lambda f, x, y, g=g: (f == g[0] and (g[1] is None or (x, y) == (g[1], g[2]))),
                 event_mode=a.events, trap_mode=a.trap, goal_cell=g)
        if not r or (isinstance(r, tuple) and r and r[0] == 'cap'):
            print('未搜到（状态上限）' if r else '图不可达（无解）'); raise SystemExit(1)
        else:
            w, path = r
            print('路径长度', len(path) - 1, ' 余血', w.hero.hp, 'ATK/DEF', w.hero.atk, w.hero.dfn,
                  '钥匙', dict(w.hero.keys), 'GOLD', w.hero.gold)
            print('caveats', w.caveats)
            for p in path[:6]:
                print('   ', p)
            print('    …')


_TRAP_GUARD_CELLS |= {(3, x, y) for x, y in TRAP_3F['guards']}


# ---- 数据源切换：08 Java 版本体权威数据（DumpAll8.java 从 MTower.class 运行时导出） ----
def use_java8(path):
    """把 MAPT/MAPO/MA/OA 切换为 08 Java 版导出数据，并重建 WARP。

    依据：DumpAll8.java 反射读取 MTower.map/mapObject/mapAttribute/objectAttribute
    （loadMapData 加载后的运行时真值）。obj 表已与 PC98 live.json 全量对比 0 差异。
    """
    global MAPT, MAPO, MA, OA, WARP
    d = json.load(open(path))
    MAPT2 = [row[:] for row in MAPT]
    MAPO2 = [row[:] for row in MAPO]
    for _f in range(1, 51):
        _b, _s = (_f - 1) // 10, (_f - 1) % 10
        _J = d['floors'][str(_f)]
        for _y in range(13):
            for _x in range(13):
                MAPT2[_b * 13 + _y][_s * 13 + _x] = _J['map'][_y][_x]
                MAPO2[_b * 13 + _y][_s * 13 + _x] = _J['obj'][_y][_x]
    MAPT, MAPO, MA, OA = MAPT2, MAPO2, d['mapAttribute'], d['objectAttribute']
    W2 = {}
    for _f in BAND_SLOT:
        for _y in range(13):
            for _x in range(13):
                if terrain(_f, _x, _y) == 2:
                    _r, _c = rc(_f, _x, _y)
                    _idx = MAPT[_r][_c]
                    _col, _row = MA[_idx][16], MA[_idx][17]
                    if _col == 0 and _row == 0:
                        continue
                    W2[(_f, _x, _y)] = _decode_global(_col, _row)
    WARP.clear(); WARP.update(W2)
    return len(WARP)


_J8 = os.environ.get('MOTA_JAVA8')
if _J8 and os.path.exists(_J8):
    use_java8(_J8)
