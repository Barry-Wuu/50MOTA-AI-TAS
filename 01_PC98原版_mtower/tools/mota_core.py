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


# ⚠️ 2026-11-13 撤销 OPEN_WALLS：源数据 1F(4,11)(8,11) tile3 就是墙（截图逐格采样
#   确认棕砖墙色、secret_walls=[]），当年"飞行之珠不可达"判断是错的——
#   实际左下房经黄门 (2,8) 连中区，飞行之珠由 1c 第三次合法取得。
#   底排被两段墙截成三个房间正是原版设计。 terrain() 恢复纯真值。


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
# 飞行之珠（obj26）传送落点：到达目标层时落在该层「自下层上来的落点」（= 上行梯旁踏出格）。
# 数据来自 STAIRS_POINTS.md 的「落点（下层→本层）」第一列（自下方到达），已与 WARP 落地核对。
FLY_LAND = {1:(2,1),2:(1,2),3:(2,11),4:(11,10),5:(2,11),6:(1,2),7:(11,10),
            8:(1,2),9:(6,2),10:(1,10),11:(6,10),12:(10,11),13:(2,11),14:(10,11),
            15:(6,10),16:(6,2),17:(6,10),18:(6,2),19:(1,2),20:(6,10),21:(6,2),
            # 22F-49F 由 STAIRS_POINTS.md「落点（下层→本层）」列补齐（2026-10-29）
            # 例外：41F 原表记 (5,1)，但该格 terrain==1 是实墙，按落点规则改取 (6,2)（推断）
            22:(6,10),23:(1,2),24:(2,11),25:(2,11),26:(2,11),27:(2,11),28:(10,11),
            29:(1,10),30:(6,10),31:(6,2),32:(6,10),33:(10,1),34:(2,1),35:(6,10),
            36:(11,2),37:(11,10),38:(2,1),39:(11,2),40:(10,11),41:(6,2),42:(6,10),
            43:(1,2),44:(1,2),45:(2,1),46:(11,2),47:(10,11),48:(11,10),49:(2,11),
            # 50F 无楼梯，只能由 24F(6,0) 暗门 warp 进，落点 (6,5)；飞行不可直选，仅备查
            }
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
DECOR_PASS = set()                                # 饰件：可踩；obj19 实机验证不可踩（np2kai 实测 2026-10，撞击无位移）
# ✅ 祭坛本体由 3 格构成：中央 obj22(SAIDAN) + 左右 obj21/obj23（type0，但属于祭坛，不可踩）。
#    实机/用户确认：祭坛左右两格不能穿过。obj21/23 全塔只出现在 4F/12F/32F/46F 祭坛两侧。
ALTAR_SIDE = {21, 23}
# ✅ 2F 监狱栅栏门 obj19：Java MTower.java directCheck（a[3]==0 && a[4]==0 → 不放行）与 np2kai 实测
#    都表明不可通行；@3764 只在 (6,2)(8,2) 两只門番Ｂ obj15 清空后，一次性把 6 格全部清零（开门动画）。
GATE_2F = {(2, 5, 5), (2, 9, 5), (2, 5, 8), (2, 9, 8), (2, 5, 11), (2, 9, 11)}

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
    170: [('item', 112)],                               # ✅ obj170 商店卖超级镐 obj112（非 obj170 自身）
}
for _o in SHOP:
    SHOP_PRICE[_o] = oatr(_o, 13)
PICKUP_TYPES = {3, 4, 8}                            # STATUS/ITEM/KEY：踏入即拾取
MONSTER_TYPE = 6

MAGIC_HALF_ATK = {58, 96}       # ⚠️ 旧模型（战斗前半血）——已被 MAGIC_PASSBY 取代，见下；保留以免破坏引用
# ✅ 穿行魔法伤害（Java MTower.ichicheck2 L832-931 实证 + PC-98 42F(1,4) 消息互证）：
#   · 魔導師(58)「夹击」：当左右两格或上下两格**都是**魔導師 → 英雄 HP 减半（你血越多扣越多）
#   · 魔術師Ａ(99) 邻接 → -200；魔術師Ｂ(100) 邻接 → -100
#   · 神盾 obj39（44F 幻の階）在身 → 全部魔法攻击无效
MAGIC_SANDWICH = {58}                   # 夹击→半血
MAGIC_ADJ_DMG  = {99: 200, 100: 100}    # 邻接→固定伤害
# ✅ 2026-11-12 修正：魔法免疫属 **44F 神盾 obj39**，不是 43F 聖盾 obj38。
#   证据链（三方一致）：
#   ① 日文原文 MTower.java strMessage[1][75]：
#      「神盾は、魔法使いしたちの魔法攻撃を防ぐ力があるらしい。……しかし、この盾は幻の階に隠されているそうだ。」
#      （"The sacred shield can defend you against magic attacks... hidden on a floor that doesn't exist."）
#      「幻の階」= 44F（同段 strMessage[1][74] 明说 44 階は幻の階，普通楼梯上不去，只能 WARP）。
#   ② 物品名与属性：obj38 = 聖盾 +50DEF（43F 9,4）；obj39 = 神盾 +100DEF（44F 6,6）。
#   ③ 中文攻略（apkzu / 3DM / 9game / 百度知道 四源一致）：
#      「43F:圣盾(+50防御)；44F:神圣盾(+100防御,**忽视魔法攻击**)」。
#   ⚠️ Java 版未实现该免疫（mapObject[73][121] 全文件仅 11 处读取、0 处置位，
#      只在 init 清零），故引擎按 PC-98 原版语义与文档描述实现，比 08a Java 版更完整。
SACRED_SHIELD  = 39                     # 神盾（44F 幻の階）：魔法攻击全免疫
HOLY_SHIELD    = 38                     # 聖盾（43F）：纯 +50DEF，无魔法效果
# 📝 盗贼凿墙事件（dynamic.csv 实证：触发格 obj88 MESSAGE「…大ダコが道をふさいでいて…抜け穴が…」，
#    目标格 directCheck 墙→地板；35F(5,10)→35F 暗道同机制）。键=被挖开的墙格，值=盗贼触发格
DIG_WALLS = {(15, 8, 1): (15, 9, 1),
             (35, 4, 9): (35, 5, 10)}                # 35F 同机制（dynamic.csv L137 / L68 盗贼）
DIG_TRIG = {v: k for k, v in DIG_WALLS.items()}   # 触发格 → 被挖开的墙格
# 📝 29F 小偷暗道（dynamic.csv 实证：29F(6,4)(7,2) 均为 obj88 MESSAGE「この大ダコが道をふさいて…抜け穴が…」，
#    29F(6,3) 记作 `draw_obj=1 / variants:'3' / cell_now=eventMT` = 撞小偷偷完后该格变黄钥匙 obj1 且墙开）。
#    前提：23F 把 44 块 obj115 隐形砖全撞掉（"Go 0F" 字形）。两个触发格挖同一格。
DIG29_TRIG = {(29, 7, 2), (29, 6, 4)}
DIG29_WALL = (29, 6, 3)
DIG_TRIG.update({t: DIG29_WALL for t in DIG29_TRIG})
# 📝 祭坛（README「祭壇」节：4 座 4F/12F/32F/46F，obj22 type=7）
#    4 项菜单：生命力 / 攻击力 / 防御力 / 取消（yesnoNumber=9，文案 206/207-）
ALTAR_CELLS = {(4, 6, 1), (12, 6, 9), (32, 10, 10), (46, 6, 1)}   # ✅ 引擎 obj_raw 实测坐标
ALTAR_GAIN = {'hp': 200, 'atk': 10, 'dfn': 10}    # 兜底档位常量（saidan 绘制数值）
# ✅ 逐层档位（2026-10-31 修正）：原实现按全塔统一 +10，与攻略实录的 L 值序列对不上。
#    直接证据：
#      · §4.2「4F（回）…若选择开商店则蓝门加防（L≈658，D14）」→ 4F 加防 +4（DEF 10→14）
#      · §5.2「12F：升 2 次防 1 次攻（L≈316，A34/D50）」→ 12F 加攻 +4、加防 +8
#    间接证据：按 D14 复算 5F回/8F 的 8 处战损全部逐点吻合（G-4 / R-12 / 蝙蝠-48 /
#    スケルトンC-84 / 僧侶-72），而按 D10 全部偏大。
#    ⚠️ 4F 的 atk/hp 档位仍未验证（本路线只用加防），32F/46F 沿用既有研究结论。
# ✅ 2026-11-02 定论修正（用户质疑成立）：PC-98 祭坛收益**随楼层区域缩放**，非固定 +10。
#   真值来源：`08_Java_MTower08a/decompiled/MTower.java` saidan() 属性写回 @3915-3923——
#     HP 增益 = (k+1)×100（k=全存档已祭次数，mapObject[66][119]）
#     ATK 增益 = mapY×2+2；DEF 增益 = mapY×4+4（mapY=楼层区 = (floor-1)//10）
#   即 4F +2攻/+4防、12F +4攻/+8防、32F +8攻/+16防、46F +10攻/+20防。
#   ⚠️ 79c9434「恢复固定+10」是错误回退（误把 saidan 绘制显示常量当属性写回 + 引擎CSV循环论证）；
#     旧「固定+200HP/+10ATK/+10DEF」作废。与 `09_TAS推演/plan_11_20.py` @30-32 原口径一致。
ALTAR_GAIN_BY_FLOOR = {
    4:  {'atk': 2,  'dfn': 4},
    12: {'atk': 4,  'dfn': 8},
    32: {'atk': 8,  'dfn': 16},
    46: {'atk': 10, 'dfn': 20},
}


def altar_gain(f, pol, k=0):
    """取该层祭坛的单项收益。ATK/DEF 随楼层区缩放；HP 随累计已祭次数 k 递增（(k+1)×100）。"""
    if pol == 'hp':
        return (k + 1) * 100
    g = dict(ALTAR_GAIN)
    g.update(ALTAR_GAIN_BY_FLOOR.get(f, {}))
    return g[pol]


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
    154: ('item', 104),       # ✅ 「褒美におぬしに”エリクサー”をやろう」→ 圣水 obj104 入包
                              #    （16F(11,11)，MTower.java @3090-3092；越晚用收益越大）
    87:  ('none', None),      # 盗贼脱走：同事件把 2F(2,7) 的墙挖通（已在 TRAP 里做）
    88:  ('none', None), 151: ('none', None), 173: ('none', None), 175: ('none', None),
    44:  ('none', None),      # 勇者「人形だっ！」
}

LUCKY_GOLD = 113                                      # 📝 幸运金币：击杀 GOLD×2
SEAL_TARGET = 57                                      # ✅ 封印后 objectAttribute[57][10/11/12] 改写 800/500/100

# ---------------------------------------------------------------------------
# ✅ 50F 真·通关链（08 Java 实证；用户实机版本一致）
#   ① 26F(6,7) 假公主剧情（mapObject[67][126] 一次性旗）→ 挖开 24F 中央竖井
#      Java@2820-2825: map[26][45]=1; map[27][44]=3; map[27][46]=3; map[28..30][45]=1
#      坐标换算：row=band*13+y、col=slot*13+x → 24F(6,0)=1 / (5,1)(7,1)=3 / (6,2)(6,3)(6,4)=1
#   ② 24F(6,0) 踩上即 endFlag=true（Java@2934）→ ending()@14072 滚屏 24F→49F，
#      末帧把勇者放到 50F(6,7)（charaX=30/charaY=35 + mapX=9/mapY=4 ⇒ 全局 col123,row59），
#      并把 24F 竖井**全部还原**（一次性通道），置 mapObject[76][126]=1。
#   ③ 50F(6,7) 且 50F(6,5)==obj88 小偷 且 [76][126]==1 → 12 页对话；
#      计数到 2 时 Zeno2(graphics,123,57) 把小偷变身成 obj57（魔導師ゼノ）落在 50F(6,5)。
#   ④ 50F 中央 3×3 被墙包死，勇者是传送进 (6,7) 的；走到 (6,5) 开打。
SECRET24_DIG = {                                      # 26F 触发后：24F 竖井挖开
    (24, 6, 0): 1, (24, 6, 2): 1, (24, 6, 3): 1, (24, 6, 4): 1,
    (24, 5, 1): 3, (24, 7, 1): 3,
}
SECRET24_RESTORE = {                                  # ending() 末尾：24F 还原
    (24, 6, 0): 31, (24, 6, 2): 3, (24, 6, 3): 3, (24, 6, 4): 3,
    (24, 5, 1): 1, (24, 7, 1): 1,
}
TRIG_26F = (26, 6, 7)                                 # 假公主剧情触发格（红门后第一格）
TRIG_24F_END = (24, 6, 0)                             # endFlag 格
F50_LAND = (50, 6, 7)                                 # ending() 落点
ZENO2_CELL = (50, 6, 5)                               # 小偷/真魔王格

# ✅ 49F 魔王战的「战后演出写入」不是进层即写入：
#    Java@1581 触发条件是「(6,3) ゼノ已死」，然后才把 3 蓝药/3 红晶/3 蓝晶/红钥匙/屠龙匕摆出来。
#    dyn_raw 把这些常量写入混在一起，若照搬进层覆盖会白送 +3000HP/+15ATK/+15DEF，且 (5,2)/(7,2)
#    的钥匙/屠龙匕会被同格 obj58 警卫覆盖丢失。故这里全部排除，改由 after_49 在击败ゼノ后写入。
F49_CUTSCENE_CELLS = {
    (49, 5, 5), (49, 6, 5), (49, 7, 5),               # obj78 青い回復薬 +1000HP ×3
    (49, 2, 4), (49, 3, 4), (49, 4, 4),               # obj82 赤のクリスタル +5ATK ×3
    (49, 8, 4), (49, 9, 4), (49, 10, 4),              # obj85 青のクリスタル +5DEF ×3
    (49, 5, 2), (49, 7, 2),                           # obj28 红钥匙 / obj109 屠龙匕
}
F49_GUARD_CELLS = [(5, 2), (6, 2), (7, 2), (7, 3), (7, 4), (6, 4), (5, 4), (5, 3)]
# ✅ 49F 封印的真正判据（Java@1745 逐格比对，非「8 只全灭」）：
#    (5,2)(7,2)(5,4)(7,4) 四斜角仍是 obj58，而 (6,2)(5,3)(7,3)(6,4) 四正方向已清空，
#    且 (6,3) 仍是 obj57 ゼノ ⇒ 才把 objectAttribute[57] 改写 800/500/100。
#    攻略「先打上下左右 4 个魔法警卫（骰子 5）封印」正对应这 4 个正方向格。
F49_SEAL_EDGES = [(6, 2), (5, 3), (7, 3), (6, 4)]
F49_SEAL_CORNERS = [(5, 2), (7, 2), (5, 4), (7, 4)]
ZENO49_CELL = (49, 6, 3)
F50_THIEF_CELL = (50, 6, 5)



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


# ✅ 2026-11-11 修正：50F **没有楼梯入口**，也不从 49F 进。
#    真·入口是 26F(6,7) 假公主剧情挖开 24F 竖井 → 24F(6,0) 触发 ending() → 传送到 50F(6,7)。
#    （08 Java: eventMT@2809 / @2934 / ending()@14072；用户实机版本一致：24F 秘道、25F 大法师、26F 假公主）
UP_PATCH = {}


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
        fl = int(e['floor'])
        obj = e['obj']
        # ✅ 41F(6,5,108) 降臨の翼：dyn_raw 标 method=eventMT，Java @1930 实证
        #    只在暗墙事件完成（杀(2,2)+撞(10,2)+杀魔術師A）后才生成。
        #    不能静态写入——否则不触发事件也能直接拿。
        if fl == 41 and obj == 108:
            continue
        # ✅ 39F(4,4,107) 昇華の翼：dyn_raw 标 method=eventMT，Java @2517-2519 实证
        #    九门事件（开12点+3点两门）后才生成。
        #    但 mota_core 已有 check_39_doors() 动态生成 obj106（中心飞行器，原版正确），
        #    此 107 是 Java 复刻的错误（原版应为 106）。
        #    若静态写入会与 check_39_doors() 冲突，跳过。
        if fl == 39 and obj == 107:
            continue
        # ✅ 16F(11,11) 圣水 NPC：dyn_raw 记的是「谈话后」的 obj151（話は終わりじゃ），
        #    首访真值应是 obj154（エリクサーをくれる老人，立绘 55/56；真·盗贼 obj87/88 是 51/52）。MTower.java @3090-3092 实证：
        #    初始 obj154 → 对话后置 mapObject[75][119]=1（圣水 obj104 入包）+ 该格改 obj151。
        #    故把 dyn_raw 的 151 改写回 154，让首访就能拿到圣水。
        if fl == 16 and e['x'] == 11 and e['y'] == 11 and obj == 151:
            obj = 154
        FLOOR_WRITES[fl].append((e['x'], e['y'], obj))
TERR_WRITES = collections.defaultdict(list)
for e in DYNEV.get('ter', []):
    if e['floor'].isdigit():
        TERR_WRITES[int(e['floor'])].append((e['x'], e['y'], e['to']))

_TRAP_GUARD_CELLS = set()          # 由剧本自己放置的格，不进"进层即写入"集合（在下面填）

# ✅ 20F BOSS 间红门：静态底图 (20,6,9) 就是红门 obj27（DOOR_OF[27]='r'），
#    必须持红钥匙 obj28 才能开启 —— 这是「见 BOSS 的基本门槛」。
#    dyn_raw 里那条 (6,9,20) 记的是「门已开之后」的状态，不是进层即写入；
#    若照搬成进层覆盖，红门会凭空变成可通行装饰，红钥匙门槛被整个跳过。
#    ✅ 同理 40F 决战区红门 (40,6,8)：静态底图就是红门 obj27（probe_keys12 实测
#    obj_raw 视图 F40(6,8)=o27），而 dyn_raw 在 (6,8) 记的是 obj20「门已开」状态，
#    照搬进层覆盖会让红门变成可通行装饰 —— 红钥匙门槛（V68「过红门决战」）被跳过。
#    （2026-11-06 修复：新增 (40,6,8)，与 20F 同因同解。）
BOSS_DOOR_CELLS = {(20, 6, 9), (40, 6, 8)}

# ✅ 落穴（obj20）守卫清规则（资料笔记 @3780-3845「某两只怪清空 → 该格 obj20 归零」）：
#    键=(层,落穴x,落穴y)，值=[(守卫1x,守卫1y),(守卫2x,守卫2y)]。
#    守卫全部击杀/清除后，落穴格 obj20 从地图上消失（变可通行地板）。
#    注意：15F/30F 落穴由 OCTO/slime30 机制单独处理，不在此表。
PIT_GUARD_CLEAR = {
    (8, 10, 4):   [(9, 5), (11, 5)],
    (11, 2, 4):   [(1, 5), (3, 5)],
    (17, 2, 4):   [(1, 5), (3, 5)],
    (17, 2, 7):   [(1, 8), (3, 8)],
    (17, 10, 4):  [(9, 5), (11, 5)],
    (17, 10, 7):  [(9, 8), (11, 8)],
    (32, 2, 9):   [(1, 10), (3, 10)],
    (44, 6, 8):   [(5, 9), (7, 9)],
    (45, 7, 10):  [(8, 9), (8, 11)],
}
# 反向索引：守卫格 → 它守护的落穴列表
GUARD_TO_PITS = {}
for _pit, _guards in PIT_GUARD_CLEAR.items():
    for _gx, _gy in _guards:
        GUARD_TO_PITS.setdefault((_pit[0], _gx, _gy), []).append(_pit)

# ✅ 15F 大乌贼 = 单体多格 Boss（资料笔记 §十「9 格同数据；杀本体后九格一次全清 + 掉普通镐」）。
#    9 格占 (5..7, 4..6)：obj50/51/52（y4 行）、obj60/61/62（y5 行）、obj70/71/72（y6 行）。
#    本体 obj71 在 (6,6)，四维 1200/180/20/100；其余 8 格是「大ダコの一部」，四维 1200/180/20/50。
#    引擎旧模型把这 9 格当 9 只独立怪（每格 -301）→ 错；真相是 **1 场战斗**（对本体 obj71）。
#    杀本体后（@3099-3129）：3×3 九格一次清空 + 落穴 (6,3)(6,9) 消失 + (6,5) 生成普通镐 obj114。
OCTO_F = 15
OCTO_MAIN_OBJ = 71                                     # 本体 obj71（四维 1200/180/20/100）
OCTO_MAIN = (15, 6, 6)                                  # 本体格 (6,6)
OCTO_BODY = [(15, x, y) for x in (5, 6, 7) for y in (4, 5, 6)]   # 3×3 九格（含本体）
OCTO_OBJS = {50, 51, 52, 60, 61, 62, 70, 71, 72}        # 九格的对象 id（含本体 71）
OCTO_PITS = [(15, 6, 3), (15, 6, 9)]                    # 杀后消失的两道落穴
OCTO_PICK = (15, 6, 5)                                  # 杀后 (6,5) 生成普通镐 obj114
OCTO_TRIGGER = (15, 6, 8)                               # 📝 踩 (6,8) 且本体仍在 → (6,9) 变落穴（封出口）

# ✅ 2F 奖励 NPC：静态初始是 obj174(+1000G)/obj152(ATK/DEF×1.03)，
#    dyn_raw 里的 obj173/obj151 是「对话后」的替换（MTower.java @3751/@3761），
#    不是进层即写入。若照搬成进层覆盖，1000G 与 +3% 将永远拿不到。
#    cell_now 字段同样证实：cell_now=obj174/obj152，draw_obj=173/151。
KEEP_STATIC_NPC_CELLS = {(2, 11, 4), (2, 11, 7)}

# ✅ 34F 钥匙生成事件（MTower.java @2594 实证）：变量旗 mapObject[67][125]==0 且
#    8 个黄门后怪物格 (5,4)(7,4)(9,4)(11,4)(5,8)(7,8)(9,8)(11,8) 全部清空 →
#    置旗 + 落 (2,6)红钥匙 obj28、(1,5)(3,5)(1,7)(3,7)黄钥匙 obj1。
#    这 5 格静态全为空，dyn_raw 的写入是「条件触发」而非进层即写入；
#    照搬进层覆盖会让早段（V49）提前拿到本属 V66 的 1红+4黄。
KEY34_CELLS = {(34, 2, 6), (34, 1, 5), (34, 3, 5), (34, 1, 7), (34, 3, 7)}
KEY34_MONS = [(34, x, y) for x in (5, 7, 9, 11) for y in (4, 8)]

# ✅ 14F(1,3) 红钥匙（见 BOSS 的第二把钥匙，8F 那把已用于 10F 红门）
#    Java MTower.java:3801-3808 实证：该格原版地形值是 **3（暗墙）**，并非实墙。
#    进入 14F 且周围三格(mapObject[14][40/42]、[15][41])清空后执行：
#        map[16][40] = 1   （暗墙塌掉 → 变可通行地板）
#        mapObject[16][40] = 28  （落红钥匙）
#    displayDoor/displayCharacter 表明这是一次「暗墙裂开、露出红钥匙」的演出。
#    故本引擎按 **暗墙** 处理：撞塌后可踩入，露出 obj28 正常拾取（见 move 内 DARKWALL_CELLS 分支）。
#    原引擎把 terrain=1 当死墙直接 blocked，导致红钥匙永远拿不到、20F 红门开不了。
DARKWALL_CELLS = {(14, 1, 3),
                  (41, 5, 6), (41, 6, 6), (41, 7, 6)}  # ✅ 41F 事件墙：事件触发后变暗墙，可撞塌穿过

# ✅ OPEN_WALLS 定义已上移到 terrain() 之前（见函数上方注释），此处删除重复定义，
#   否则会在模块加载末尾把 OPEN_WALLS 重新赋值覆盖（虽然值相同，但保持单一真源）。
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
    slime30: bool = False            # 30F 六只史莱姆已清 → (30,6,4)(6,7) 落穴消失、(30,6,1) 现上行梯
    boss40: bool = False             # 40F BOSS（obj90 金騎士，(6,6)）已击败 → (40,6,1) 现出上行梯（ter[7]→to:90）
    altar_k: int = 0                  # 📝 本存档累计祭坛已使用次数（决定下一次代价）
    altar_policy: str = 'atk'         # 📝 祭坛菜单选择：hp / atk / dfn（A* 无法处理菜单，按策略预设）
    story42: bool = False             # ✅ 42F 剧情：骑士队长已逃（金騎士清场）
    story32: bool = False             # ✅ 32F 剧情：金騎士先手攻击（-300HP）→ 清场 + 2F 生成盗贼
    octo15: bool = False              # ✅ 15F 大乌贼（obj71 本体）已击败 → 3×3 九格清空 + (6,5) 生成镐
    event41_stage: int = 0            # ✅ 41F 暗墙事件阶段：0=未触发, 1=(2,2)杀+(10,2)撞墙刷怪, 2=事件完成(降臨の翼生成)
    pending_items: Dict = None        # ✅ 事件写在怪物脚下的道具：怪物被击杀后露出（10F 水晶/蓝药/黄钥）
    story26: bool = False             # ✅ 26F(6,7) 假公主剧情已触发 → 24F 竖井已挖开（一次性）
    story24_end: bool = False         # ✅ 24F(6,0) ending() 已执行 → 已传送到 50F(6,7)、24F 已还原
    seal49: bool = False              # ✅ 49F 十字封印成立（四正方向警卫全灭）→ obj57 改写 800/500/100
    zeno49_dead: bool = False         # ✅ 49F(6,3) ゼノ已击败 → 战后演出已摆出道具
    f50_talk: int = 0                 # ✅ 50F(6,7) 对话页计数：0→12，计数 2 时 Zeno2 变身
    won50: bool = False               # ✅ 50F(6,5) 真魔王已击败 = 通关
    center_warp_charges: int = 0      # ✅ 中心飞行器 obj106（空間転移の秘宝）剩余次数：拾取=3，每次 -1；0=不可用。
                                      #    依据 Java @1203-1206 mapObject[67][120] 计数（拾取=1，用后+1，>=4 归零=3 次）。

    @classmethod
    def new(cls, event_mode='on_entry', hero=None, trap_mode='apply'):
        w = cls(hero=hero or Hero.initial(), cells=base_cells(), over={}, ter_over={}, cleared=set(),
                applied_events=set(), event_mode=event_mode, trap_mode=trap_mode, caveats=set(),
                bought=set(), boss10=False, boss20=False, octo15=False, event41_stage=0, pending_items={})
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
            if (f, x, y) in BOSS_DOOR_CELLS:
                continue                                  # ✅ 红门保持 obj27，须红钥匙开启（见 BOSS 的门槛）
            if (f, x, y) in KEEP_STATIC_NPC_CELLS:
                continue                                  # ✅ 2F 奖励 NPC 保持静态 obj174/152（对话后才替换）
            if (f, x, y) in KEY34_CELLS:
                continue                                  # ✅ 34F 钥匙：8 门后怪物全灭才生成（@2594），非进层即写入
            if f == 49 and (f, x, y) in F49_CUTSCENE_CELLS and o != 58:
                continue                                  # ✅ 49F 战后演出才摆出（Java@1638-1740），进层不得白送
                                                          #    注意：同一格可能同时有警卫(58)与道具，只跳道具
            if f == 49 and (x, y) == (6, 3):
                continue                                  # ✅ 49F 中心是ゼノ obj57，不是 obj69 评分 NPC
            if f == 39 and (x, y) == (4, 4):
                continue                                  # ✅ 39F 昇華の翼：由 9门事件才生成，非进层即写入
            base = self.cells.get((f, x, y), 0)
            if base and TYPE.get(oatr(base, 3)) == 'MONSTER':
                # ✅ 该格静态是怪/BOSS，事件写入不得覆盖（否则 BOSS 消失、怪免打）。
                #    但事件确实在该格放道具（10F 水晶/蓝药/黄钥写在怪物脚下）：记下待怪物死后露出。
                if o in KEY_OF or TYPE.get(oatr(o, 3)) in ('STATUS', 'ITEM'):
                    self.pending_items[(f, x, y)] = o
                continue
            if o:
                self.set_at(f, x, y, o)
        if f == 49:
            # ✅ 进入 49F 触发ゼノ登场（Java@1779-1794：踩 (6,5) 播 Zeno(110,55)）+ 8 只 obj58 围成十字
            self.set_at(*ZENO49_CELL, SEAL_TARGET)
            self.cleared.discard(ZENO49_CELL)
        if f == 42:
            # ✅ 42F 剧情：金騎士（骑士队长）威胁→受伤逃走（strNumber 27/28），
            #    不实际战斗。与 3F 同型菱形：中央金騎士 (6,8) + 四角 4 只魔導師伏兵
            #    (6,7)(5,8)(7,8)(6,9) 全部随剧情清场（同 3F 四角撤走）。
            #    ✅ 依据：攻略 §8.2 行322 只提「2 初级巫师+2 魔法警卫扣血」——
            #    那 2 魔法警卫是右侧 (9,8)(11,8) 的静态魔導師，4 只伏兵不是战斗目标；
            #    且若不清场，42F 起点 (6,10) 会被 (6,9) 伏兵堵死，无法「右中过黄门」。
            for c in ((42, 6, 8), (42, 6, 7), (42, 5, 8), (42, 7, 8), (42, 6, 9)):
                self.cleared.add(c)
            self.story42 = True

    # -- 动作：飞行之珠传送（须站在楼梯旁） ---------------------------------
    def fly(self, target_f):
        """飞行之珠 obj26：站在当前层楼梯旁，传送到任意已到达楼层。
        落点取 FLY_LAND[target_f]（= 该层上行踏出格），等价于从下层走上来的落点。
        规则「飛翔のオーブは階段のとなりでなくては使えない！」已由 adjacency 校验。
        """
        h = self.hero
        if 26 not in h.items:
            return ['飞行之珠：尚未持有 obj26，无法传送']
        if target_f not in FLY_LAND:
            return ['飞行之珠：目标层 %d 不可达' % target_f]
        s = STAIRS.get(h.f)
        cells = [c for c in (s if s else (None, None)) if c]
        adj = any(abs(sx - h.x) + abs(sy - h.y) == 1 for (sx, sy) in cells)
        if not adj:
            return ['飞行之珠：须站在楼梯旁（当前 %dF(%d,%d) 附近无楼梯）' % (h.f, h.x, h.y)]
        h.f = target_f
        h.x, h.y = FLY_LAND[target_f]
        log = ['飞行之珠传送 → %dF（落点 %s）' % (target_f, FLY_LAND[target_f])]
        self.apply_floor_events(target_f)
        return log

    # -- 动作：同层飞行器（昇華の翼 obj107） ---------------------------------
    def wing_up(self, force_layer=False):
        """昇華の翼 obj107（向上飞行器，**一次性消耗**）。
        - force_layer=True 或无上行梯 → 向上飞一层 f+1（落点 FLY_LAND[f+1]）：用于 43F→44F 幻之阶。
        - 否则 → 同层瞬移到本层上行梯口旁（省路）：用于 42F 之类「同层飞行到楼梯口」。
        依据：秘宝表 107「上跳一层」；用户定：昇華の翼一次性，且写死用于进 44F（43F force_layer）。
        """
        h = self.hero
        if 107 not in h.items:
            return ['昇華の翼：尚未持有 obj107，无法传送']
        up = STAIRS.get(h.f)
        up_cell = up[0] if up else None
        # ① 强制上移一层（或无上行梯）→ f+1
        if force_layer or up_cell is None:
            if h.f + 1 in FLY_LAND:
                h.items.discard(107)                      # 一次性消耗
                old = h.f
                h.f = h.f + 1; h.x, h.y = FLY_LAND[h.f]
                self.apply_floor_events(h.f)
                return ['昇華の翼（一次性）：%dF→%dF 向上飞一层（落点 %s）'
                        % (old, h.f, FLY_LAND[h.f])]
            return ['昇華の翼：%dF 上方无可达楼层' % h.f]
        # ② 同层瞬移到上行梯口旁
        sx, sy = up_cell
        for d in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            ax, ay = sx + d[0], sy + d[1]
            if not (1 <= ax <= 11 and 1 <= ay <= 11):
                continue
            if self.terrain_at(h.f, ax, ay) == 1:
                continue                                  # 墙
            o = self.at(h.f, ax, ay)
            if o and TYPE.get(oatr(o, 3), '?') == 'MONSTER':
                continue                                  # 怪格不停留
            h.items.discard(107)                          # 一次性消耗
            h.x, h.y = ax, ay
            return ['昇華の翼（一次性）：同层瞬移到 %dF(%d,%d)（上行梯旁，已消耗）' % (h.f, ax, ay)]
        return ['昇華の翼：上行梯 %dF(%d,%d) 无可走邻格' % (h.f, sx, sy)]

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

    # ✅ 穿行魔法伤害（Java MTower.ichicheck2 L831-931 实证；PC-98 42F(1,4) 消息互证）：
    #   每步入新格后调用一次（Java 第 1038 行，仅换格时）。圣盾 obj38 在身则全部无效。
    def check_magic_passby(self, log):
        h = self.hero
        if SACRED_SHIELD in h.items:
            return None                                  # 聖盾：魔法攻击全免疫
        f, x, y = h.f, h.x, h.y
        # 1) 魔導師夹击：左右两格或上下两格都是魔導師 → HP 减半
        L = self.at(f, x - 1, y); R = self.at(f, x + 1, y)
        U = self.at(f, x, y - 1); D = self.at(f, x, y + 1)
        if (L in MAGIC_SANDWICH and R in MAGIC_SANDWICH) or (U in MAGIC_SANDWICH and D in MAGIC_SANDWICH):
            h.hp = math.ceil(h.hp / 2)
            log.append('★魔導師夹击 → HP减半（现 %d）' % h.hp)
            if h.hp <= 0:
                return ['被魔導師夹击夹死（HP≤0）']
        # 2) 魔術師邻接固定伤害
        for c in (L, R, U, D):
            dmg = MAGIC_ADJ_DMG.get(c)
            if dmg:
                h.hp -= dmg
                log.append('★魔術師邻接 → -%d（现 %d）' % (dmg, h.hp))
                if h.hp <= 0:
                    return ['被魔術師魔法打死（HP≤0）']
        return None

    # -- 动作：朝 (dx,dy) 走一步 -------------------------------------------
    def face_altar(self, ax, ay):
        """✅ 2026-11-13 Java 真值修正：面朝祭坛献祭（人物不移动，可原地连献）。
        Java MTower.java：directCheck(面前格) 判 obj type==7 → yesno 菜单（L5804）；
        连续确认 = 连续献祭，零位移。返回日志列表；失败返回含 '祭坛' 的错误。"""
        h = self.hero
        f, x, y = h.f, h.x, h.y
        if (f, ax, ay) not in ALTAR_CELLS:
            return [f'祭坛坐标错误：({f},{ax},{ay}) 不在 ALTAR_CELLS']
        if abs(ax - x) + abs(ay - y) != 1:
            return [f'祭坛：必须站在祭坛邻格面朝它（当前 ({x},{y}) → ({ax},{ay})）']
        c = altar_cost(self.altar_k)
        if h.gold < c:
            return ['祭坛金币不足（需%d，有%d）' % (c, h.gold)]
        h.gold -= c
        pol = self.altar_policy if self.altar_policy in ALTAR_GAIN else 'atk'
        gain = altar_gain(f, pol, self.altar_k)
        if pol == 'hp':
            h.hp += gain
        elif pol == 'atk':
            h.atk += gain
        else:
            h.dfn += gain
        self.altar_k += 1
        return ['祭坛献金%dG → %s+%d（第%d次，下次%dG）'
                % (c, pol, gain, self.altar_k, altar_cost(self.altar_k))]

    def move(self, dx, dy):
        h = self.hero
        # ✅ 2026-11-14 保真度修正：原版每次输入只走 **一格**。
        #   旧实现不校验 |dx|/|dy|，路径被落穴/暗墙挡住时，规划器算出的方向会是 (0,-2) 这类
        #   「跳两格」的位移，引擎照单全收 → 英雄直接跳过被挡的格（原版绝无可能）。
        #   实测曾出现 7 处非法跳穴（8F(10,4) / 17F 四处 / 32F(2,9) / 45F(7,10)）。
        if abs(dx) > 1 or abs(dy) > 1:
            return ['blocked:非法移动方向（%d,%d）——原版每次只走一格' % (dx, dy)]
        f, x, y = h.f, h.x, h.y
        nx, ny = x + dx, y + dy
        log = []
        if self.terrain_at(f, nx, ny) == 1:
            if (f, nx, ny) in DARKWALL_CELLS:
                # 📝 暗墙(原版地形值 3)：撞塌后露出底下物体，可踩入拾取。
                #    ✅ 2026-11-13 修复：DARKWALL 无论是否 cleared 都放行。
                #    旧逻辑写成 `in DARKWALL and not in cleared`，导致「已撞塌」时落进 elif
                #    → 因 terrain 仍为 1 而判 blocked，撞塌过的地形暗墙反而不可再通行
                #    （41F 中央十字 (5,6)(7,6) 被 V71 撞过后 V93 复现 blocked:墙）。
                if (f, nx, ny) not in self.cleared:
                    log.append('撞塌暗墙(14,1,3) → 露出红钥匙')
            elif DIG_WALLS.get((f, nx, ny)) not in self.cleared:
                return ['blocked:墙']               # 未触发=普通墙；触发后直接放行（log 由落格时带出）
        o = self.at(f, nx, ny)
        if o in ALTAR_SIDE:
            # ✅ 祭坛左右两格 obj21/obj23 属于祭坛本体，不可踩入
            return ['blocked:祭坛侧格 obj%d（祭坛本体不可踩）' % o]
        if o == 19 and (f, nx, ny) in GATE_2F:
            # ✅ 2F 监狱栅栏门：两只門番Ｂ清空前不可通行（Java directCheck / np2kai 实测）；
            #    清空后由下方击杀分支把 6 格一并 cleared，届时 at() 返回 0，不再进这里。
            return ['blocked:2F 监狱栅栏门 obj19（须先击败 (6,2)(8,2) 两只門番Ｂ）']
        # ✅ 修正（此处原为死锁 bug）：20F 的「进入」与「离开」是两套独立机制，不能混为一谈。
        #    · 进入：(20,6,9) 是红门 obj27，必须持红钥匙 obj28 开启 —— 见 BOSS 的基本门槛。
        #      开门由下方 ty == 'DOOR' 分支统一处理（无红钥匙挡路、有则消耗 1 把），
        #      故此处不再额外判断。开门后踏上 (6,8) 触发点，banpaia() 才放出吸血鬼
        #      （Java MTower.java:3080：displayDoor → mapObject[22][123]=20 → banpaia）。
        #    · 离开：击败 (6,6) 吸血鬼后置 boss20=True，(20,6,1) 才现上行梯（下方 warp 逻辑，正确）。
        #    旧代码把「进入」误绑到 boss20 上，既造出「要杀 BOSS 才开门、而 BOSS 在门后」的死锁，
        #    又让红钥匙这道门槛形同虚设。现已恢复红门、交由 DOOR 分支消耗红钥匙。
        ty = TYPE.get(oatr(o, 3), '?') if o else '空'
        if o:
            if o == 89:                                   # 📝 暗墙：撞了就塌
                if f == 41 and (nx, ny) == (10, 2) and (41, 2, 2) in self.cleared \
                        and self.event41_stage == 0:
                    # ✅ Java @13751-13753: (2,2)已杀 + 撞(10,2) → 设旗标 + 刷魔術師Ａ埋伏
                    self.event41_stage = 1
                    self.over[(41, 10, 2)] = 99       # 生成 obj99 魔術師Ａ
                    self.cleared.discard((41, 10, 2))  # 确保怪物可见（不被cleared覆盖）
                    log.append('★41F 撞塌暗墙(10,2) → 魔術師Ａ埋伏出现!')
                    return log                         # 不移动（怪挡路）
                self.cleared.add((f, nx, ny)); log.append('撞塌暗墙 obj89'); o = 0; ty = '空'
                if (f, nx, ny) in ((19, 6, 3), (19, 6, 4)):   # 📝 19F 十字暗墙：撞开获得十字架 obj103
                    h.items.add(103); log.append('获得十字架 obj103（对吸血鬼等伤害翻倍）')
            elif o == 79:                                # ✅ 熔岩：**不可通行**（不是掉血地砖）
                # 📝 依据：MTower.java @785 `directCheck` —— obj79 的 c3=0/c4=0 → 判 bl=false，
                #    撞上只弹 texts[183]「溶岩が流れている」，角色不动。
                #    （13F 80 格 / 26F 18 格，MAP_NOTES §4）
                # ⚠️ 旧实现误写成「可踩 −200HP/步」，会让 13F 神剣 obj34 不用雪之结晶就能拿 —— 与原版不符。
                #    清除唯一途径 = 雪之结晶 obj110（itemFlag==11，清四邻各 1 格，道具不消耗）。
                return ['blocked:熔岩 obj79（溶岩が流れている，不可通行；须雪之结晶 obj110 清除四邻）']
            elif o == 115:                                # ⚠️ 隐形块（GO 0F 字形等）按可走处理
                log.append('隐形块 obj115 视为可走(caveat)'); self.caveats.add('obj115 可通行未指令流确认'); o = 0
            elif ty == 'MONSTER':
                if f == OCTO_F and o in OCTO_OBJS:
                    # ✅ 大乌贼 = 单体多格 Boss（资料笔记 §十/6.5）：只对本体 obj71 打一场。
                    #    9 格四维 1200/180/20，本体金 100、其余「一部」金 50。
                    #    杀本体后 3×3 九格一次清空 + 落穴(6,3)(6,9)消失 + (6,5) 生成普通镐 obj114。
                    r = self.battle(OCTO_MAIN_OBJ)
                    if r is None:
                        return ['打不动大乌贼（obj71 本体）']
                    loss, gold = r
                    if h.hp - loss <= 0:
                        return [f'打不过大乌贼（需掉血 {loss}，剩 {h.hp}）']
                    h.hp -= loss; h.gold += gold
                    for c in OCTO_BODY:
                        self.cleared.add(c)                 # 九格一次全清
                    self.octo15 = True
                    self.cleared.discard(OCTO_PICK)         # (6,5) 不放进 cleared，否则 at() 会先命中 cleared 返回 0
                    self.set_at(*OCTO_PICK, 114)            # (6,5) 生成普通镐 obj114（覆盖拾取可见）
                    for p in OCTO_PITS:
                        self.cleared.add(p)                 # 两道落穴消失
                        self.ter_over.pop(p, None)
                    log.append(f'★击杀大乌贼（本体 obj71）掉血{loss} +金{gold} → 九格全清，(6,5) 生成镐 obj114')
                    o = 0
                else:
                    r = self.battle(o)
                    if r is None:
                        return [f'打不动 obj{o} {oname(o)[:10]}']
                    loss, gold = r
                    # ✅ 2026-11-11 移除旧的「攻击 obj58/96 前半血」：Java 里没有这条，
                    #    真正的半血只发生在 ichicheck2@833（左右/上下夹击魔導師）——已由 check_magic_passby 处理。
                    if h.hp - loss <= 0:
                        return [f'打不过 obj{o}（需掉血 {loss}，剩 {h.hp}）']
                    h.hp -= loss; h.gold += gold; self.cleared.add((f, nx, ny))
                    log.append(f'击杀 obj{o} {oname(o)[:8]} 掉血{loss} +金{gold}')
                    self._reveal_pending(f, nx, ny, log)
                    if f == 2 and o == 15 and self.at(2, 6, 2) == 0 and self.at(2, 8, 2) == 0:
                        # ✅ @3764：两只門番Ｂ清空 → 播 6 号开门动画，6 个 obj19 栅栏格一并清零
                        for gx, gy in ((5, 5), (9, 5), (5, 8), (9, 8), (5, 11), (9, 11)):
                            self.cleared.add((2, gx, gy))
                        log.append('★2F 两只門番Ｂ已清 → 6 扇监狱栅栏门 obj19 打开')
                    if f == 38 and o == 15 and self.at(38, 1, 10) == 0 and self.at(38, 3, 10) == 0 \
                            and (38, 2, 9) not in self.ter_over:
                        # ✅ MTower.java @2524 实证：mapObject[49][92]==0 && [49][94]==0 && map[48][93]==3
                        #    → mapObject[48][93]=89, map[48][93]=1 —— 两只門番Ｂ(1,10)(3,10)全死后，
                        #    (2,9) 暗墙「现形」为 obj89（撞塌即通 texts[141]），地形 tile3→tile1(MA[1][3]=0 地板)
                        self.ter_over[(38, 2, 9)] = 1
                        self.set_at(38, 2, 9, 89)
                        log.append('★38F 两只門番Ｂ已清 → (2,9) 暗墙现形 obj89（一撞即塌）')
                    if f == 34 and (34, nx, ny) in KEY34_MONS and all(c in self.cleared for c in KEY34_MONS):
                        # ✅ MTower.java @2594 实证：8 只门后怪物格全空 + 变量旗为 0 → 落 1红+4黄钥匙。
                        #    本检查只发生在击杀这 8 格之一时，全灭瞬间即第 8 次击杀 → 恰好触发一次。
                        for kx, ky, ko in ((2, 6, 28), (1, 5, 1), (3, 5, 1), (1, 7, 1), (3, 7, 1)):
                            self.set_at(34, kx, ky, ko)
                        log.append('★34F 8 道黄门后怪物全灭 → (2,6)红钥匙 + 4 黄钥匙生成')
                    if f == 49:
                        self.after_49(o, nx, ny, log)
                    if f == 50 and o == SEAL_TARGET and (nx, ny) == F50_THIEF_CELL[1:]:
                        self.won50 = True
                        log.append('★击败真魔王 obj57（50F(6,5)）→ 通关！')
                    if f == 10 and o == 16:
                        self.boss10 = True
                        log.append('★击败10F BOSS(スケルトンＡ) → 10F(6,11) 将生上行梯')
                    if f == 20 and o == 59:
                        self.boss20 = True
                        log.append('★击败20F BOSS(バンパイア/吸血鬼) → 20F(6,1) 现出上行梯')
                    if f == 40 and o == 90:
                        # ✅ dyn_raw.json obj[43]: (6,6)→obj90；ter[7]: (6,1)→to:90。
                        #    资料笔记:888 obj90=金騎士 120/150/50/100，同 10F/20F/30F 同构。
                        self.boss40 = True
                        log.append('★击败40F BOSS(金騎士 obj90) → 40F(6,1) 将现出上行梯')
                    # ✅ 守卫清落穴：击杀后检查是否触发了落穴消失（@3780-3845）
                    for pit in GUARD_TO_PITS.get((f, nx, ny), []):
                        guards = PIT_GUARD_CLEAR[pit]
                        if all((f, gx, gy) in self.cleared for gx, gy in guards) \
                                and pit not in self.cleared:
                            self.cleared.add(pit)
                            log.append(f'★守卫全清 → 落穴 {pit[0]}F({pit[1]},{pit[2]}) 消失')
                    # ✅ 41F 暗墙事件（Java @1901-1930）：杀(10,2)埋伏魔術師Ａ → 三条件满足 → 触发
                    if f == 41 and (nx, ny) == (10, 2) and self.event41_stage == 1 \
                            and (41, 2, 2) in self.cleared:
                        self.event41_stage = 2
                        for wx, wy in ((5, 6), (6, 6), (7, 6)):
                            self.ter_over[(41, wx, wy)] = 3      # tile 3 → MA[3][3]=1 → 暗墙
                            self.over[(41, wx, wy)] = 0          # 清蓝门/物件（不加 cleared，否则暗墙不可撞塌）
                        for fx, fy in ((5, 7), (7, 7)):
                            self.ter_over[(41, fx, fy)] = 0      # 变地板
                        self.set_at(41, 6, 5, 108)               # 生成降臨の翼
                        log.append('★41F 事件完成 → (5,6)(6,6)(7,6) 变暗墙；(5,7)(7,7) 变地板；(6,5) 生成降臨の翼')
                    o = 0
            elif ty == 'DOOR':
                col = DOOR_OF.get(o)
                if col is None:
                    # obj89 暗墙（隐形墙）：撞一次塌，可通行
                    if f == 41 and (nx, ny) == (10, 2) and (41, 2, 2) in self.cleared \
                            and self.event41_stage == 0:
                        # ✅ Java @13751-13753: (2,2)已杀 + 撞(10,2) → 设旗标 + 刷魔術師Ａ埋伏
                        self.event41_stage = 1
                        self.over[(41, 10, 2)] = 99       # 生成 obj99 魔術師Ａ
                        self.cleared.discard((41, 10, 2))  # 确保怪物可见（不被cleared覆盖）
                        log.append('★41F 撞塌暗墙(10,2) → 魔術師Ａ埋伏出现!')
                        return log                         # 不移动（怪挡路）
                    self.cleared.add((f, nx, ny))
                    log.append(f'撞塌暗墙 obj{o}'); o = 0
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
                # ✅ 2026-11-13 修正（Java 真值 MTower.java L6404-6431 + L5804）：
                #    directCheck(面前格) 判 obj type==7 → 弹 yesno 菜单，人物**不移动**。
                #    连续献祭 = 面朝祭坛反复确认，零位移。旧「踩上祭坛格」建模作废。
                #    现语义：面向祭坛（邻格）时调用 face_altar() 触发；走向祭坛格=blocked。
                if (f, nx, ny) in ALTAR_CELLS:
                    return ['blocked:祭坛本体不可踩（Java directCheck 面朝触发）']
                return [f'不可通行 obj{o}（{ty}）']
            elif ty == 'NORMAL':
                if o == 20 and (f, nx, ny) in PIT_GUARD_CLEAR:
                    # ✅ 落穴 obj20：守卫未清则挡路（资料笔记 @3780-3845）
                    guards = PIT_GUARD_CLEAR[(f, nx, ny)]
                    if not all((f, gx, gy) in self.cleared for gx, gy in guards):
                        return [f'落穴 obj20 @ {f}F({nx},{ny}) 挡路（守卫未清）']
                    self.cleared.add((f, nx, ny))
                    log.append(f'落穴 obj20 @ {f}F({nx},{ny}) 守卫已清 → 消失')
                o = 0   # 其余 type0=NORMAL 地板装饰可踩
        # 落格
        h.x, h.y = nx, ny
        # ✅ 穿行魔法伤害：每步入新格判定（夹击半血 / 魔術師邻接-200/-100，圣盾免）
        r = self.check_magic_passby(log)
        if r:
            return r
        if (f, nx, ny) in DIG_TRIG:
            # 📝 盗贼踩到即交谈、凿开对应墙格；交谈后 NPC 从地图消失，故只触发一次，
            #    之后再次经过该格按普通空地处理，不再重放台词/重复凿墙。
            #    判定「是否已凿」不能只看触发格是否 cleared：29F 触发格本身是 obj88 MESSAGE，
            #    会先被上面的 NPC 处理清掉，须改看目标墙状态。
            tg = DIG_TRIG[(f, nx, ny)]
            already = (tg in self.ter_over) if f == 29 else ((f, nx, ny) in self.cleared)
            if not already:
                self.cleared.add((f, nx, ny))
                log.append('盗賊「…大ダコの抜け穴がようやく…」→ 凿开暗道 %s' % (tg,))
                if f == 29:                            # 29F：挖开 (6,3)，该格同现黄钥匙 obj1
                    self.ter_over[DIG29_WALL] = 1      # MA[1][3]==0 → 地板
                    self.over[DIG29_WALL] = 1
                    log.append('29F(6,3) 暗道打通，现黄钥匙 obj1')
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
        elif f == 30 and self.slime30 and (nx, ny) == (6, 1):
            # 📝 30F 同构（资料笔记 §event 表：清掉 (3,5)(4,5)(5,5)(7,5)(8,5)(9,5) 六只后
            #    (6,4)(6,7) 落穴消失、(6,1) 出现上行楼梯 map=70）→ 落 31F(6,2)
            h.f, h.x, h.y = (31, 6, 2)
            log.append('楼梯 → 31F（六只史莱姆清空后上行梯）')
            self.apply_floor_events(31)
        elif f == 40 and self.boss40 and (nx, ny) == (6, 1):
            # ✅ 40F 同构：杀金騎士 obj90(6,6) 后，(6,1) 现出上行梯（dyn_raw ter[7]→to:90）
            #    → 落 41F(6,2)（41F 静态下梯 (6,1) warp=(40,5,1)，上行梯应落 41F(6,2) 邻格）。
            h.f, h.x, h.y = (41, 6, 2)
            log.append('楼梯 → 41F（40F BOSS 金騎士死后上行梯）')
            self.apply_floor_events(41)
        # ✅ 26F(6,7) 假公主剧情（Java@2809-2825，一次性）→ 挖开 24F 中央竖井
        #    该格本身是红门 obj27：先开门（消耗红钥匙），再踩上去才触发。
        if h.f == 26 and (nx, ny) == (6, 7) and not self.story26:
            self.story26 = True
            for (tf, tx, ty), tile in SECRET24_DIG.items():
                self.ter_over[(tf, tx, ty)] = tile
            log.append('★26F(6,7) 假公主剧情 → 24F 中央竖井挖开：(6,0) 通道现形')
        # ✅ 24F(6,0) 站上即 endFlag（Java@2934-2936）→ ending()@14072：
        #    滚屏 24F→49F 后把勇者放到 50F(6,7)，并把 24F 挖墙全部还原（一次性通道）。
        if h.f == 24 and (nx, ny) == (6, 0) and self.story26 and not self.story24_end:
            self.story24_end = True
            for (tf, tx, ty), tile in SECRET24_RESTORE.items():
                self.ter_over[(tf, tx, ty)] = tile
            h.f, h.x, h.y = F50_LAND
            self.apply_floor_events(50)
            log.append('★24F(6,0) 触发 ending() → 滚屏 24F→49F → 勇者被送到 50F(6,7)（24F 秘道已还原）')
        # ✅ 50F(6,7)：小偷 12 页对话；计数 2 时 Zeno2(123,57) 把小偷变成 obj57（Java@1518-1521）
        if h.f == 50 and (h.x, h.y) == (6, 7) and self.f50_talk == 0 \
                and self.at(*F50_THIEF_CELL) == 88:
            self.f50_talk = 12
            self.set_at(*F50_THIEF_CELL, SEAL_TARGET)
            log.append('★50F 小偷对话 12 页 → Zeno2 变身：50F(6,5) 出现 obj57 魔導師ゼノ'
                       '（四维 %d/%d/%d）'
                       % (oatr(SEAL_TARGET, 10), oatr(SEAL_TARGET, 11), oatr(SEAL_TARGET, 12)))
        # ✅ 32F 金騎士伏兵事件（@2666-2759 实证）：英雄 warp 到 32F(6,10) 后触发
        #    5 状态机：金騎士从 (11,1) 走到 (6,9) → 先手战斗（-300HP）→ 撤退 → 清场 + 2F 生成盗贼
        #    战斗算式：金騎士 150ATK vs DEF90 = 60/hit × 5 hits = 300（先手=怪物先攻）
        #    必须在 warp 之后检查，因为从 31F 上楼时 h.f 初始为 31，warp 后才变成 32
        if h.f == 32 and (h.x, h.y) == (6, 10) and not self.story32:
            h.hp -= 300
            if h.hp <= 0:
                return ['32F 金騎士先手攻击致死（-300HP，剩 %d）' % h.hp]
            self.cleared.add((32, 6, 9))
            self.cleared.add((32, 11, 1))
            self.set_at(2, 11, 11, 88)  # spawn 盗贼 obj88 at 2F(11,11)
            self.story32 = True
            log.append('★32F 金騎士先手攻击 → -300HP（现 %d）→ 清场 + 2F(11,11) 生成盗贼' % h.hp)
        # 📝 30F BOSS 层（六只史莱姆）：踩 (6,6) 触发 → (6,4)(6,7) 变落穴（ter_over=墙，封环）；
        #    六只全清后落穴消失、slime30=True，(6,1) 才现上行梯（见上方 elif f == 30 分支）。
        #    依据：资料笔记 §event「30F 踩(6,6)(环内) → (6,4)(6,7) 变落穴，把 6 只史莱姆和你一起封在环里」+
        #          「清掉六只 → 落穴消失；(6,1) 出现上行楼梯 map=70」。
        if h.f == 30:
            if (nx, ny) == (6, 6) and not self.slime30:
                self.ter_over[(30, 6, 4)] = 3
                self.ter_over[(30, 6, 7)] = 3
                log.append('30F 踩(6,6) → (6,4)(6,7) 变落穴，与六只史莱姆同封环内')
            if not self.slime30 and all(
                    (30, x, y) in self.cleared for (x, y) in
                    ((3, 5), (4, 5), (5, 5), (7, 5), (8, 5), (9, 5))):
                self.slime30 = True
                self.ter_over.pop((30, 6, 4), None)
                self.ter_over.pop((30, 6, 7), None)
                log.append('30F 六只史莱姆清空 → 落穴消失，(6,1) 现上行梯')
        # ✅ 15F 大乌贼陷阱（资料笔记 §event @3127）：踩 (6,8) 且本体 obj71 仍在 →
        #    (6,9) 变落穴 obj20 封住出口，逼你打完乌贼才能上 16F。
        #    杀本体后由 OCTO 分支把 (6,9) 一并清空，出口复通。
        if h.f == 15 and (nx, ny) == (6, 8) and not self.octo15:
            self.ter_over[(15, 6, 9)] = 3
            log.append('15F 踩(6,8) → (6,9) 变落穴，封住出口（须先打完大乌贼）')
        # ✅ 41F 暗墙事件（Java @1901-1930 实证）：
        #    阶段0→1: 杀(2,2)魔術師Ａ + 撞(10,2)obj89暗墙 → 刷(10,2)魔術師Ａ埋伏 + 设旗标
        #    阶段1→2: 杀(10,2)埋伏魔術師Ａ → 三条件全满足 → 生成暗墙+降臨の翼
        #    暗墙 (5,6)(6,6)(7,6) 用 tile 3（MA[3][3]=1=wall），在 DARKWALL_CELLS 中可撞塌。
        #    降臨の翼＝向下飞行器，1F 无下行梯时用它下到 0F 拿幸运金币。
        #    ⚠️ 顺序关键：必须先杀(2,2)再撞(10,2)，否则暗墙只塌不刷怪，事件永久错过！
        if h.f == 41 and self.event41_stage == 2 and not (41, 6, 5) in self.cleared:
            pass  # 事件已完成，(6,5) 的 obj108 由正常拾取处理
        if h.f == 3 and (nx, ny) == TRAP_3F['trigger'] and not self.trap_done:
            h.x, h.y = nx, ny
            return self.do_trap3F(log)
        # 剧本收尾后的通路：盗贼挖开的 2F(2,7) 由 ter_over 生效，这里只把「四角撤走」标清楚
        
        if h.f == 3 and self.trap_mode == 'avoid' and (nx, ny) == TRAP_3F['trigger']:
            return ['避开3F中央(反事实)']
        return log

    def _reveal_pending(self, f, x, y, log):
        """事件写在怪物脚下的道具：击杀后露出并立即取得（对应原版 itemFlag 拾取演出）。"""
        o = self.pending_items.pop((f, x, y), None)
        if not o:
            return
        if o in KEY_OF:
            self.hero.keys[KEY_OF[o]] += 1
            log.append(f'击破后露出 {oname(o)[:10]}')
        elif TYPE.get(oatr(o, 3)) in ('STATUS', 'ITEM'):
            self.pick(o, log)

    def pick(self, o, log):
        h = self.hero
        hp, atk, dfn = oatr(o, 10), oatr(o, 11), oatr(o, 12)
        if hp: h.hp += hp
        if atk: h.atk += atk
        if dfn: h.dfn += dfn
        if TYPE.get(oatr(o, 3)) == 'ITEM':
            h.items.add(o)
        if o == SACRED_SHIELD:
            h.items.add(SACRED_SHIELD)                # ✅ 神盾 obj39 是 STATUS 类，免疫判据查 h.items，必须显式登记
        if o == 106:
            self.center_warp_charges = 3              # ✅ 中心飞行器：拾取即 3 次（Java @5544 拾取=1，@1203-1206 起算）
            log.append('★拾取中心飞行器 obj106（空間転移の秘宝）：可用 3 次中心对称瞬移')
        log.append(f'拾取 obj{o} {oname(o)[:14]} (HP+{hp} ATK+{atk} DEF+{dfn})')

    def use_pick(self):
        """普通镐 obj114（itemFlag==5）：一次性，破角色上下左右四邻的 map==3 真墙 → 地板。

        依据 魔塔1_资料笔记.md「镐走 itemFlag==5：清四邻 map==3（真墙）→ 地板，一次性」（@1087-1126）。
        ⚠️ 引擎此前只把镐当道具收进 items，没有「使用」这一步；48F 圣剑库的 (10,10) 真墙
           只能靠它凿开（不可达圣剑），故在此补齐。纯增量方法：不调用则一切行为不变。
        """
        h = self.hero
        if 114 not in h.items:
            return False, ['没有普通镐 obj114，无法破墙']
        broken = []
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nx, ny = h.x + dx, h.y + dy
            if not (1 <= nx <= 11 and 1 <= ny <= 11):
                continue
            if self.terrain_at(h.f, nx, ny) != 1:
                continue
            if (h.f, nx, ny) in DARKWALL_CELLS:
                continue
            self.ter_over[(h.f, nx, ny)] = 1        # MA[1][3]==0 → 地板
            self.over.pop((h.f, nx, ny), None)
            broken.append((nx, ny))
        h.items.discard(114)
        if not broken:
            return True, ['镐 obj114 已使用（一次性）：四邻无真墙，白费']
        return True, ['★使用镐 obj114（一次性）：破开四邻真墙 %s' % broken]

    def use_bomb(self):
        """破壊の玉 obj105（资料笔记 §itemFlag: 清整层怪物）。
        使用后当前层全部怪物标记为 cleared（零战斗清除），并触发守卫清落穴事件。
        一次性消耗。
        """
        h = self.hero
        if 105 not in h.items:
            return False, ['没有破壊の玉 obj105']
        f = h.f
        cleared_mons = []
        for y in range(1, 12):
            for x in range(1, 12):
                o = self.at(f, x, y)
                if o and TYPE.get(oatr(o, 3)) == 'MONSTER':
                    self.cleared.add((f, x, y))
                    cleared_mons.append((x, y, o))
                    # 触发守卫清落穴
                    for pit in GUARD_TO_PITS.get((f, x, y), []):
                        guards = PIT_GUARD_CLEAR[pit]
                        if all((f, gx, gy) in self.cleared for gx, gy in guards) \
                                and pit not in self.cleared:
                            self.cleared.add(pit)
        h.items.discard(105)
        if not cleared_mons:
            return True, ['破壊の玉 obj105 已使用：本层无怪物']
        return True, ['★使用破壊の玉 obj105：清整层 %d 只怪物 %s' % (len(cleared_mons), cleared_mons)]

    def use_super_pick(self):
        """超级镐 obj112（itemFlag==13，资料笔记 §itemFlag: 破整层 12×12 墙）。
        使用后当前层全部真墙（map==3 / terrain==1）变地板，一次性消耗。
        """
        h = self.hero
        if 112 not in h.items:
            return False, ['没有超级镐 obj112']
        f = h.f
        broken = []
        for y in range(1, 12):
            for x in range(1, 12):
                if self.terrain_at(f, x, y) == 1:
                    if (f, x, y) in DARKWALL_CELLS:
                        continue
                    self.ter_over[(f, x, y)] = 1
                    self.over.pop((f, x, y), None)
                    broken.append((x, y))
        h.items.discard(112)
        if not broken:
            return True, ['超级镐 obj112 已使用：本层无真墙']
        return True, ['★使用超级镐 obj112：破整层 %d 格真墙' % len(broken)]

    def use_magic_key(self):
        """魔法钥匙 obj111（46F(3,8)）：一次性，**打开本层所有门**（黄/蓝/红），不耗钥匙。
        依据：texts line3554「可打开一层楼所有的门」、line4160「使用了魔法钥匙！本层所有的门都打开了！」。
        """
        h = self.hero
        if 111 not in h.items:
            return False, ['没有魔法钥匙 obj111']
        f = h.f
        opened = []
        for y in range(1, 12):
            for x in range(1, 12):
                o = self.at(f, x, y)
                if o in (2, 4, 27):                  # 黄门 obj2 / 蓝门 obj4 / 红门 obj27
                    self.cleared.add((f, x, y))
                    opened.append((x, y, o))
        h.items.discard(111)
        if not opened:
            return True, ['魔法钥匙 obj111 已使用：本层无门可开']
        return True, ['★使用魔法钥匙 obj111：%dF 打开全部 %d 扇门 %s' % (f, len(opened), opened)]

    def use_snow_crystal(self):
        """雪之结晶 obj110（itemFlag==11）：把角色**上下左右四邻**的熔岩 obj79 清成地板。

        依据 魔塔1_推演进度.md §一 / gen_notes.py『雪之结晶 obj110』：
          `MTower.java` @1322-1372 —— 弹确认框 → 对四邻逐格判 `=='O'` → 有则播
          displayDoor(...,9~12) 动画并把该格改成地板；持有旗标 `mapObject[71][120]` 不清零
          → **可无限次重复使用，不消耗**。
        ⚠️ 熔岩 obj79 本身是不可通行的（directCheck bl=false），故清除是拿到 13F 神剣 obj34
           的唯一途径：必须站在熔岩边缘一格格往里啃。
        """
        h = self.hero
        if 110 not in h.items:
            return False, ['没有雪之结晶 obj110，无法清除熔岩']
        f = h.f
        cleared_cells = []
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            nx, ny = h.x + dx, h.y + dy
            if not (1 <= nx <= 11 and 1 <= ny <= 11):
                continue
            if self.at(f, nx, ny) != 79:
                continue
            self.cleared.add((f, nx, ny))       # at() 命中 cleared 返回 0 → 变地板
            cleared_cells.append((nx, ny))
        if not cleared_cells:
            return True, ['雪之结晶 obj110：四邻无熔岩（道具不消耗）']
        return True, ['★使用雪之结晶 obj110：清除四邻熔岩 %s（道具不消耗，可反复用）'
                      % cleared_cells]

    def use_elixir(self):
        """圣水 obj104（エリクサー，由 16F 右下角 obj154 老人赠送）：HP += ATK×10 + DEF×5，
        一次性消耗。

        依据 MTower.java @1067-1086（itemFlag==4，槽位 mapObject[75][119]=obj104）：
            mapObject[66][118] += mapObject[67][118] * 10 + mapObject[68][118] * 5
        其中 66=HP、67=ATK、68=DEF —— 由状态栏 y=122/154/185 绘制顺序（@13408-13413）
        + 战斗估算 @6602/6612（67≤怪防→打不动、怪攻−68→每回合伤害）+ 祝福魔法 @3759-3760
        （67*=1.03、68*=1.03）三处互证。
        ⚠️ 文案「按攻击与防御总和加生命」是中文版意译，真实权重是 ATK×10 + DEF×5（ATK 双倍）。
        「越晚用越好」—— ATK/DEF 越高收益越大，路线应留到加点后再喝。
        """
        h = self.hero
        if 104 not in h.items:
            return False, ['没有圣水 obj104（须先在 16F 右下 (11,11) 与 obj154 老人对话）']
        gain = h.atk * 10 + h.dfn * 5
        h.hp += gain
        h.items.discard(104)
        return True, ['★饮用圣水 obj104：HP += ATK%d×10 + DEF%d×5 = +%d（现 HP=%d，已消耗）'
                      % (h.atk, h.dfn, gain, h.hp)]

    def wing_down(self):
        """降臨の翼 obj108（向下飞行器，**一次性消耗**）：站在本层任意处，瞬移到本层下行梯口旁。
        若本层无下行梯（如 1F），则视为「向下飞行一层」→ 降落至下一层（特殊：1F→0F）。
        依据：资料笔记「降臨の翼＝向下飞行器；0F 要等 41F 拿降臨の翼才能下到」。
        """
        h = self.hero
        if 108 not in h.items:
            return ['降臨の翼：尚未持有 obj108，无法传送']
        f = h.f
        s = STAIRS.get(f)
        dn = s[1] if s else None          # 下行梯
        if dn is not None:
            sx, sy = dn
            for d in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                ax, ay = sx + d[0], sy + d[1]
                if not (1 <= ax <= 11 and 1 <= ay <= 11):
                    continue
                if self.terrain_at(f, ax, ay) == 1:
                    continue
                o = self.at(f, ax, ay)
                if o and TYPE.get(oatr(o, 3)) == 'MONSTER':
                    continue
                h.items.discard(108)                  # 一次性消耗
                h.x, h.y = ax, ay
                return ['降臨の翼（一次性）：同层瞬移到 %dF(%d,%d)（下行梯旁，已消耗）' % (f, ax, ay)]
            return ['降臨の翼：下行梯 %dF(%d,%d) 无可走邻格' % (f, sx, sy)]
        # ✅ 本层无下行梯 → 向下飞行一层（特殊：1F→0F）
        if f == 1:
            h.items.discard(108)                      # 一次性消耗
            h.f = 0; h.x, h.y = 1, 2      # 0F(1,1)=上行梯，邻格 (1,2) 可走
            self.apply_floor_events(0)
            return ['降臨の翼（一次性）：1F 无下行梯 → 向下飞行至 0F（落点 (1,2)，已消耗）']
        if f - 1 in FLY_LAND:
            h.items.discard(108)                      # 一次性消耗
            h.f = f - 1; h.x, h.y = FLY_LAND[f - 1]
            self.apply_floor_events(f - 1)
            return ['降臨の翼（一次性）：向下飞行至 %dF（落点 %s，已消耗）' % (f - 1, FLY_LAND[f - 1])]
        return ['降臨の翼：%dF 下方无可达楼层' % f]

    # -- 动作：中心飞行器（空間転移の秘宝 obj106） -----------------------------
    def wing_center(self):
        """中心飞行器 obj106（空間転移の秘宝 / The Warp Staff）：可用 3 次，
        瞬移到本层「中心对称点」 (x,y) → (12-x, 12-y)（以 (6,6) 为中心 180° 旋转）。
        依据：texts line4052「你得到中心飞行器，可用 3 次到达中心对称的对应点」；
              Java MTower.java @1191-1202 `n4 = 12 - charaX/5 + mapX*13`、`charaX = (12 - charaX/5)*5`。
        失败条件（@1193）：目标格 mapObject!=0（有物体）或 map!=1（非地板）→「目标格有障碍物，无法中心飞行」。
        计数（@1203-1206）：拾取即 3 次，每次使用 -1，用完不可再飞。
        """
        h = self.hero
        if 106 not in h.items:
            return ['中心飞行器：尚未持有 obj106，无法传送']
        if self.center_warp_charges <= 0:
            return ['中心飞行器：已用完（共 3 次）']
        tx, ty = 12 - h.x, 12 - h.y
        if not (1 <= tx <= 11 and 1 <= ty <= 11):
            return ['中心飞行器：目标格 (%d,%d) 越界，无法中心飞行' % (tx, ty)]
        if self.terrain_at(h.f, tx, ty) == 1:              # mota_core: terrain 1 = 墙
            return ['中心飞行器：目标格 %dF(%d,%d) 是墙，无法中心飞行' % (h.f, tx, ty)]
        o = self.at(h.f, tx, ty)
        if o:                                              # 门/怪/道具/暗墙 等任何物体都算障碍
            return ['中心飞行器：目标格 %dF(%d,%d) 有障碍物 obj%d，无法中心飞行' % (h.f, tx, ty, o)]
        self.center_warp_charges -= 1
        fx, fy = h.x, h.y
        h.x, h.y = tx, ty
        return ['中心飞行器：%dF (%d,%d)→(%d,%d)（剩 %d 次）'
                % (h.f, fx, fy, tx, ty, self.center_warp_charges)]

    def check_39_doors(self):
        """39F 九门事件（Java @2517-2519 原版逻辑）：开 (4,2)12点 + (6,4)3点 两扇黄门，
        其余 7 门（(2,2)(6,2)(2,4)(4,4)(2,6)(4,6)(6,6)）仍是黄门 obj2
        → **(4,4) 生成「中心飞行器 obj106」（Warp Staff / 空間転移の秘宝）**。
        ⚠️ Java 复刻版 @2519 误写 107（昇華の翼）；原版渲染图 (4,4)=斜放长柄杖(Warp Staff)=obj106
           （用户实证 + floor_39.png 放大图）。昇華の翼 obj107 实际在 45F(2,10)。
        """
        if self.hero.f != 39:
            return []
        if self.at(39, 4, 4) == 106:
            return ['39F 九门事件已完成（(4,4) 已是中心飞行器）']
        if self.at(39, 4, 2) != 0 or self.at(39, 6, 4) != 0:
            return []                                  # 12点/3点尚未开
        keep = [(2, 2), (6, 2), (2, 4), (4, 4), (2, 6), (4, 6), (6, 6)]
        if any(self.at(39, x, y) != 2 for x, y in keep):
            return []                                  # 其余 7 门必须保持黄门
        self.over[(39, 4, 4)] = 106
        self.cleared.discard((39, 4, 4))
        return ['★39F 九门事件（12点+3点开、其余7门关）→ (4,4) 生成中心飞行器 obj106（Warp Staff）']

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

    def after_49(self, o, nx, ny, log):
        # ① 十字封印（Java@1745 逐格判据）：四正方向 obj58 全灭 + 四斜角仍在 + (6,3) ゼノ仍在
        if not self.seal49 \
                and all(self.at(49, x, y) == 0 for x, y in F49_SEAL_EDGES) \
                and all(self.at(49, x, y) == 58 for x, y in F49_SEAL_CORNERS) \
                and self.at(49, 6, 3) == SEAL_TARGET:
            self.seal49 = True
            globals()['OA'][SEAL_TARGET][10:13] = [800, 500, 100]       # ✅ 封印改写（全局）
            log.append('★49F 十字封印成立（上下左右 4 只魔法警卫已灭）→ obj57 四维改写 800/500/100')
        # ② 击败 (6,3) ゼノ → 战后演出摆出道具（Java@1638-1740）
        if not self.zeno49_dead and (nx, ny) == (6, 3) and o == SEAL_TARGET:
            self.zeno49_dead = True
            for fx, fy, fo in ((5, 5, 78), (6, 5, 78), (7, 5, 78),
                               (2, 4, 82), (3, 4, 82), (4, 4, 82),
                               (8, 4, 85), (9, 4, 85), (10, 4, 85),
                               (5, 2, 28), (7, 2, 109)):
                self.set_at(49, fx, fy, fo)
                self.cleared.discard((49, fx, fy))
            self.set_at(49, 6, 3, 69)                                   # 评分 NPC 立在原格
            self.cleared.discard((49, 6, 3))
            log.append('★49F ゼノ击败 → 战后演出：3 蓝药 + 3 红晶 + 3 蓝晶 + 红钥匙 + 屠龙匕，(6,3) 立评分 NPC')

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
    w.slime30 = self.slime30; w.boss40 = self.boss40
    w.altar_k = self.altar_k; w.altar_policy = self.altar_policy
    w.pending_items = dict(self.pending_items)
    w.story42 = self.story42; w.story32 = self.story32; w.octo15 = self.octo15
    w.event41_stage = self.event41_stage
    w.story26 = self.story26; w.story24_end = self.story24_end
    w.seal49 = self.seal49; w.zeno49_dead = self.zeno49_dead
    w.f50_talk = self.f50_talk; w.won50 = self.won50
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
