#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成《魔塔1 资料笔记》——把散在各处的机制结论与可机器校验的表合成一份。

用法：
    cd 01_PC98原版_mtower/tools && python gen_notes.py

产出：01_PC98原版_mtower/魔塔1_资料笔记.md
表格部分（物件表/特殊格/事件写入/门钥/楼梯/各层速查/怪物）全部由数据自动生成，
机制定论部分是手工维护的常量（带源码或实测证据），改结论请改本文件的 MECH 常量。
所有坐标统一 (x, y)，层号 0..50。
"""
import os
import sys
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M  # noqa: E402

OUT = os.path.normpath(os.path.join(HERE, '..', '魔塔1_资料笔记.md'))
FLOORS = range(0, 51)


# ---------------------------------------------------------------- 手工常量
# 物件编号权威表：obj -> (名称, 分类, 说明)
OBJ_NOTE = {
    1: ('黄钥匙', '钥匙', '文本 133「扉の鍵を手に入れた」'),
    2: ('黄门', '门', '⚠️ 不是钥匙！开一扇消耗 1 黄钥匙'),
    3: ('蓝钥匙', '钥匙', '全塔唯一蓝钥匙来源；obj88 是盗贼，不是钥匙'),
    4: ('蓝门', '门', '消耗 1 蓝钥匙'),
    27: ('红门', '门', '源码 @5580：mdata==27 扣红钥匙'),
    28: ('红钥匙', '钥匙', '静态只有 3 把：8F/37F/42F'),
    11: ('红药 +50', '补给', ''),
    12: ('红药 +200', '补给', ''),
    66: ('红药 +100', '补给', ''),
    67: ('红药 +200', '补给', ''),
    68: ('红药 +250', '补给', ''),
    76: ('蓝药 +400', '补给', ''),
    77: ('蓝药 +800', '补给', ''),
    78: ('蓝药 +1000', '补给', ''),
    13: ('红晶 ATK+1', '增益', ''),
    14: ('蓝晶 DEF+1', '增益', ''),
    80: ('红晶 ATK+2', '增益', ''),
    81: ('红晶 ATK+4', '增益', ''),
    82: ('红晶 ATK+5', '增益', ''),
    83: ('蓝晶 DEF+2', '增益', ''),
    84: ('蓝晶 DEF+4', '增益', ''),
    85: ('蓝晶 DEF+5', '增益', ''),
    30: ('铁剑 ATK+10', '装备', '5F'),
    31: ('銀の剣 ATK+20', '装备', '17F'),
    32: ('骑士剑 ATK+40', '装备', ''),
    33: ('聖剣 ATK+50', '装备', '48F，打 35F 魔龙的前置'),
    34: ('神剣 ATK+100', '装备', '13F 熔岩中央 (6,5)，后期才能取'),
    35: ('铁盾 DEF+10', '装备', '9F'),
    36: ('銀の盾 DEF+20', '装备', '11F'),
    37: ('骑士盾 DEF+40', '装备', '38F'),
    38: ('聖盾 DEF+50', '装备', '43F，打魔龙前置'),
    39: ('神盾 DEF+100', '装备', '44F，打魔龙前置'),
    22: ('祭坛', '机关', '4座：4F/12F/32F/46F'),
    25: ('知恵のオーブ', '秘宝', '看怪物数值'),
    26: ('飛翔のオーブ', '秘宝', '飞行'),
    105: ('破壊の玉', '秘宝', '37F 上左库'),
    107: ('昇華の翼', '秘宝', '39F，上跳一层'),
    108: ('降臨の翼', '秘宝', '41F，下跳一层（回 0F 拿幸运金币靠它）'),
    109: ('屠龙匕', '秘宝', '49F (7,2) 打假魔王后给；对 obj74 伤害×2'),
    110: ('雪之结晶', '秘宝', '35F (6,5)；itemFlag 11，清四邻各 1 格熔岩，可反复用'),
    111: ('魔法の鍵', '秘宝', ''),
    113: ('幸运金币', '秘宝', '0F；杀怪 GOLD×2'),
    112: ('超级镐', '工具', '47F 商人 4000G，破整层 12×12 墙'),
    114: ('普通镐', '工具', '15F 杀大乌贼后掉 (6,5)，一次性，破脚下四方'),
    79: ('熔岩', '地形', '⚠️ 实心墙，不是伤害地砖；全塔 98 格（13F 80 + 26F 18）'),
    19: ('洞（落穴）', '地形', '2F 6 处，掉到下一层'),
    20: ('落穴', '地形', '实心不可穿（c3=0 c4=0）；多处是事件生成'),
    21: ('装饰（可踩）', '地形', '祭坛两侧，DECOR_PASS 可通行'),
    23: ('装饰（可踩）', '地形', '祭坛两侧，DECOR_PASS 可通行'),
    86: ('50F 背景格', '地形', '96 格，无交互'),
    89: ('隐形墙', '暗墙', '撞一次塌（文本 141「壁がくずれた！」），可通行'),
    115: ('隐形块', '暗墙', '撞了变墙（23F 44 格拼成 "GO 0F"）'),
    88: ('盗贼 NPC', 'NPC', '⚠️ 不是蓝钥匙！15F/35F 会凿墙；29F/50F 也会出现'),
    87: ('盗贼（2F 牢房）', 'NPC', '3F 扒装剧本后落到 2F(4,8)，到这里交谈拿回装备'),
    69: ('实力评价牌', '记分', '每 10 层一块（10F/20F/25F/30F…），按 HP/DEF/ATK/钥匙数评级'),
    151: ('提示牌', '信息', '「もう、話は終わりじゃ。」'),
    173: ('提示牌', '信息', '「有効に使ってね!」'),
    138: ('NPC 23F', 'NPC', '提示本层藏有信息'),
    139: ('NPC', 'NPC', '祭坛升 ATK 才能打「ロック」'),
    140: ('NPC 21F', 'NPC', '大魔导师 4500/560/310 警告'),
    141: ('NPC 27F', 'NPC', '提示 27F 门槛：HP1500 ATK80 DEF98'),
    142: ('NPC 31F', 'NPC', '二刀流剑士警告'),
    143: ('NPC 33F', 'NPC', '「急がば回れ」'),
    144: ('NPC 36F', 'NPC', '4 个抜け穴可绕强敌'),
    145: ('NPC', 'NPC', '宝物库需要マトック'),
    146: ('NPC', 'NPC', '「3 时空间移动秘宝」'),
    147: ('NPC', 'NPC', '魔术师相邻攻击、魔导师夹击削半血'),
    148: ('NPC', 'NPC', '44F 是幻之层'),
    149: ('NPC', 'NPC', '41F 左右对称'),
    150: ('NPC', 'NPC', '骰子 5 点形封印魔王'),
    152: ('NPC', 'NPC', '给 ATK/DEF +3%'),
    153: ('NPC', 'NPC', '勇者のオーブ'),
    161: ('收购商', '商店', '卖钥匙给他，100G/把'),
    174: ('NPC', 'NPC', '给 1000G'),
    175: ('NPC', 'NPC', '解释「門」的机制'),
}

SHOP_NOTE = {
    18: '黄＋1（50G）', 41: '黄＋5（50G）', 156: '红＋1（800G）', 159: '蓝＋1（200G）',
    162: '黄＋4 蓝＋1（1000G）', 164: '黄＋3（200G）', 166: '蓝＋3（2000G）',
    168: 'HP＋2000（1000G）', 170: '超级镐（4000G）',
}

# 机制定论：每条 (标题, 正文)
MECH = [
    ('通行判定（唯一权威）', '''
源码 `directCheck` @5456：`mapObject != 0` 即阻挡；只有 `c3(a[3])==0 && c4(a[4])==1` 才放行。
因此 **熔岩 obj79（c3=0 c4=0）、落穴 obj20、魔龙躯体 obj53-75 全是实心**，不要当装饰放行。
obj89 / obj115 属于 `c3=5` 的门类，由撞墙分支单独处理。
'''),
    ('熔岩不是伤害地砖', '''
`ichicheck` @785 对 `'O'`（=79）只做一件事：弹文本 183「溶岩が流れている。」——**不掉血、不清格**。
全源码搜 `'O'` 只有 5 处：1 处提示 + 4 处在雪之结晶分支。
⚠️ `mota_core.py` 早期版本写的「熔岩每步 −200」是无源码依据的猜测，已废弃。
'''),
    ('雪之结晶 obj110', '''
`itemFlag == 11`（不是 12）。@1322-1370：弹确认框 → 对角色**上下左右 4 邻格**逐格判 `=='O'`
→ 有则播 `displayDoor(...,9~12)` 动画并把该格改成地板。
**一次只清四邻各 1 格，持有旗标 `mapObject[71][120]` 不清零 → 可无限次重复使用。**
清 13F 那 80 格要站在边缘一格格往里啃。
'''),
    ('13F 神剣是后期道具', '''
13F 主线（下梯 (1,11) → 上梯 (11,11)）走 y=11 石廊，**10 步、0 格熔岩、0 战损**，根本不碰熔岩。
神剣 obj34 在熔岩正中的 (6,5)，从 (6,10) 黄门进要穿 4 格熔岩。
正确时序：**49F 假魔王 → 屠龙匕 → 35F 魔龙 → 雪之结晶 → 回 13F 清熔岩 → 神剣**。
所以 11F-20F 的 ATK 曲线里**没有** +100。
'''),
    ('15F 两条路线：直穿 vs 凿墙绕行', '''
落点 (6,10)，上梯 (6,1)。大乌贼 9 格占 (5..7, 4..6)，把 x=5..7 的纵向通道拦腰截断。

**A. 直穿**：10 步，但必须打本体 obj71 (6,6)。杀本体后 3×3 九格一次清空
（@3099-3129）+ 落穴 (6,3)(6,9) 消失 + **(6,5) 生成普通镐 obj114**。
战损随 ATK 曲线变化（1200/180/20）：

| 时机 | ATK/DEF | 回合 | 损失 |
|---|---|---|---|
| 进 11F 时 | 60/70 | 30 | 3190 |
| 12F 之后 | 64/74 | 28 | 2862 |
| **直进 15F** | **66/74** | **27** | **2756** |
| 绕行走完 16F+17F 再回来 | 88/76 | 18 | **1768** |
| 后期档 | 120/90 | 12 | 990 |

**B. 凿墙绕行**：15F (9,1) 有盗贼 obj88（eventMT 写入），对话后凿开 **(8,1)** 的墙。
凿开后 (8,1) 变地板，右上区 (9..11, 1) 与上梯 (6,1) 连通：
`(6,10)→(7,10)→(7,11)→[黄门](8,11)→(9,11)→(9,10)→(9,9)[黄门]→(9,8)→(9,7)→(9,6)[黄门]→(9,5)→(10,5)→(11,5)→(11,4)→(11,3)[黄门]→(11,2)→(10,2)→(9,2)→(9,1)盗贼→(8,1)凿开→(7,1)→(6,1)`
= **21 步 / 4 道黄门 / 3 场小战（バット (9,11)、大バット (10,5)、Ｂスライム (11,2)）**。
不凿墙时 (6,10)→(6,1) **怎么走都不通**（BFS 实测，x=4 与 x=8 两列都是半截断墙）。

**关键取舍**：绕行能上 16F/17F，但**拿不到镐**（镐是大乌贼掉落物）。
镐是 37F 破库拿红钥匙 → 38F 红门 的刚需，所以乌贼只能推迟、不能省。
绕行的实际价值：
1. 先上 17F 拿銀の剣（ATK+20）再回来打，**2756 → 1768，省 988 血**；
2. 顺路吃 15F **(11,8) 蓝药 +400**（在 x=11 竖井上，绕行路径正好路过）和 **(1,1) 青晶 DEF+2**
   （从上梯 (6,1) 往西走 y=1 走廊，(4,1) 一道黄门）；
3. 把「必吃的大战」推到 HP 更充裕的时候，避开 15F 作为 11F-20F 血线瓶颈。
'''),
    ('15F 盗贼与 37F/35F 是同一套凿墙机制', '''
`DIG_WALLS = {(15,8,1): (15,9,1), (35,4,9): (35,5,10)}` —— 键=被凿开的墙格，值=盗贼格。
35F (5,10) 盗贼开 (4,9) 暗道，让玩家绕开 3×3 魔龙。
两者都靠 `dynamic.csv` 的 `obj88:MESSAGE` 记录 + 目标格 directCheck 由墙变地板实证。
'''),
    ('obj2 是黄门，不是黄钥匙', '''
黄钥匙 obj1（169 个），黄门 obj2（239 个）。之前一度把 obj2 当钥匙，导致钥匙账全线错位。
同理 obj4 蓝门 / obj27 红门 / obj28 红钥匙。
全塔静态：**黄门 239 / 蓝门 39 / 红门 12**，而钥匙只有 **黄 169 / 蓝 20 / 红 3**。
⇒ 门永远开不完，**必须挑门走**。
'''),
    ('门的取舍策略决定钥匙账生死', '''
用「步数最优」（每道门权重 20000）排 11F-20F，会在 14F 开 2 道蓝门、18F 2 道、20F 2 道，
欠账滚到 38F 差 4 把蓝钥匙。
改成「绕门优先」（蓝门权重 60000 ≈ 绕 60 步也比开一道蓝门便宜）后，
11F→38F 净收支 **黄 +16 / 蓝 +2 / 红 0**，38F 三道蓝门稳开。
'''),
    ('20F 三段式（@2961）', '''
① `mapObject[74][127]==1 && map[14][123]=='2'`（上梯已生成）才刷新战利品；
② 杀 (6,6) 吸血鬼 → 双封印 (6,3)(6,9) 解除 + (6,1) 现上梯 + flag=1；
③ 踏入 (6,8) → 入口变 obj20 封印 + 吸血鬼出现。
进 (6,9) 是**红门**，必须持红钥匙。ATK+6/DEF+6/HP+1200 是**击杀后掉落**，不是战前补给。
'''),
    ('38F 是一次性盾', '''
踩到 (2,6) 时 @2528 执行 `mapObject[44][93]=20`，把层内 **(2,5)** 变成落穴，同时播「地板开洞」动画。
去程 (2,4)→(2,5)→(2,6)→盾(2,7) 走得通，**回程就断了**。
落穴生效后能走的只剩 9 格 {(1,6)(1,7)(1,8)(2,6)(2,7)(2,8)(3,6)(3,7)(3,8)}，
既到不了上梯也回不了下梯；唯一出口是蓝门链 (4,6)(5,6)(5,5) → 需 **3 把蓝钥匙**。
(2,9) 暗墙条件的 `mapObject[49][92]==0 && [49][94]==0` 要求先杀 (1,10)(3,10) 两只门番B，
而它们在被封的左侧 → **初始不可用，不是备选路线**。
'''),
    ('十字架 obj103', '''
在 **19F (6,3)**（源码 @5603：`n==110 && n2==16 ? 103`），撞的是 obj89 暗墙。19F 还有 (6,4) 一道。
持有旗标 `mapObject[74][119]`，对 obj48 / obj49 / obj59 **伤害 ×2**。
31F 之前不需要靠它（兽人系全部可绕），**唯一必经是 31F 的 2 只**（(6,8)(6,9)）。
'''),
    ('祭坛 obj22', '''
4 座：**4F (6,1)、12F (6,9)、32F (10,10)、46F (6,1)**。
`saidan()` @3872-3948，全塔共享次数 `mapObject[66][119]`。
奉献额 `(k²-k+2)*10`（k=已祭次数）→ 20/40/80/140/220…
收益与层行相关：HP +(n+1)×100、ATK +mapY×2+2、DEF +mapY×4+4。
31-40F（mapY=3）→ ATK+8 / DEF+16。45F 商店同价给 ATK+10/DEF+20，更划算。
'''),
    ('3F 扒装剧本', '''
触发格 (5,9)；四只魔導師 obj58 围 (5,8)(4,9)(6,9)(5,10)；HP/ATK/DEF 被重设为 400/10/10；
英雄被丢到 **2F (4,8)**；2F (3,7) 盗贼可交谈、2F (2,7) 被挖通。
（`TRAP_3F` 常量；h5 复刻版机制逐项对应，但坐标不同源）
'''),
    ('35F 魔龙', '''
本体 obj74 在 (6,5) 可战斗；环绕 8 格 obj53/54/55/63/64/65/73/75 是 kind 0、四维全 0 的装饰躯体。
进中央要走 35F (5,10) 盗贼凿开的 (4,9) 暗道（并撞 6 面 obj89）。
打它需要 聖剣 obj33(48F) + 聖盾 obj38(43F) + 神盾 obj39(44F) + 屠龙匕 obj109(49F)。
杀后 (6,5) 掉雪之结晶 obj110。
'''),
    ('49F/50F 魔王', '''
两只魔王共用一行数据且都是运行时放置：
`Zeno(g,110,55)` → **49F (6,3)**（外圈 8 格 obj58 魔法警卫成 3×3 环）；
`Zeno2(g,123,57)` → **50F (6,5)**（obj88 小偷先写在该格 → 小偷变身，同格两对象）。
封印后 `eventMT` 把 `objectAttribute[57][10/11/12]` 改写成 800/500/100。
'''),
    ('危险格（非战斗掉血）', '''
obj96 大魔導師：战斗**前**把主角 HP 减半。
魔術師 obj99/obj100：相邻 −200 / −100（聖盾可挡）。
魔龙吐息：−1000。
'''),
    ('开局的初始值', '''
HP 1000 / ATK 100 / DEF 100 / GOLD 0（`mapObject[66..69][118]`，实机确认）。
1F 起点 (6,11)。按键映射：上 56 / 右 54 / 下 52 / 左 50。
'''),
]

# 时序依赖链
CHAINS = [
    ('镐链（38F 红门）',
     '15F 杀大乌贼 → (6,5) 掉普通镐 obj114 → 37F (1,8) 破 (2,8) 开下左库 → 红钥匙 (7,5) → 38F 红门 (3,1)'),
    ('红钥匙链（20F 红门）',
     '14F (1,3) 撞暗墙 → 露出红钥匙 obj28 → 20F 红门 (6,9)。DARKWALL_CELLS 全塔只有这一个元素'),
    ('神剣链（ATK+100）',
     '49F 假魔王 → obj109 屠龙匕 (7,2) → 35F 魔龙 obj74 → obj110 雪之结晶 (6,5) → 回 13F 清熔岩 → obj34 神剣 ATK+100'),
    ('魔龙链',
     '聖剣 obj33(48F 8,10) + 聖盾 obj38(43F 9,4) + 神盾 obj39(44F 6,6) + 屠龙匕 obj109(49F) → 才能打 35F 魔龙'),
    ('幸运金币（0F）',
     '0F obj113 杀怪 GOLD×2；要等 41F 拿降臨の翼 obj108 才能下到 0F（1F↔0F 楼梯都在 (1,1)）'),
    ('38F 商店救不了 38F',
     'obj164 (5,2) 只卖黄钥匙 +3（200G）；卖蓝钥匙的 obj166 在 **39F (9,2)**，在 38F 上梯之后'),
]

# 已作废的旧结论
VOID = [
    ('熔岩每步 −200', '熔岩是实心墙，`ichicheck` 只弹提示。11F-20F 表里 13F 的「1600 血」整条作废'),
    ('13F 神剣是 11F-20F 的支柱', '神剣要等 35F 魔龙掉雪之结晶才能拿；主线走 y=11 石廊 10 步 0 熔岩'),
    ('obj2 是黄钥匙', 'obj2 是黄门，黄钥匙是 obj1'),
    ('obj88 是蓝钥匙', 'obj88 是盗贼 NPC；蓝钥匙只有 obj3'),
    ('obj21 / obj23 是落穴', '它们是祭坛两侧的可踩装饰（DECOR_PASS）；真正的落穴只有 obj20（obj19 是 2F 的洞）'),
    ('obj113 是超级镐', 'obj113 是幸运金币；obj112 超级镐（47F 商人）、obj114 普通镐（15F）'),
    ('十字架在 16F (8,2)', '十字架 obj103 在 19F (6,3)；16F (8,2) 是地形型暗墙，不是十字架'),
    ('20F 的 ATK+6/DEF+6/HP+1200 是战前补给', '是杀 (6,6) 吸血鬼后的掉落，且需红钥匙开 (6,9)'),
    ('38F (2,9) 暗墙是出层备选', '条件要求先杀 (1,10)(3,10) 门番B，而它们在被封的左侧 → 初始不可用'),
    ('15F 大乌贼无法绕过', '15F (9,1) 盗贼凿开 (8,1) 后可绕行 21 步上梯（但拿不到镐）'),
    ('`map_50f.json` 的 terrain 3=墙', '那只在那个 JSON 里成立；`mota_core.terrain()` 是 1=墙、2=楼梯，两套口径相反'),
]

# 怪物重点表（只列 BOSS 级与高威胁）；数值由程序从 objectAttribute 读，这里只写备注
MON_NOTE = [
    (71, '大乌贼', '15F (6,6)', '9 格同数据；杀本体后九格一次全清 + 掉普通镐'),
    (74, '魔龙', '35F (6,5)', '需屠龙匕×2 + 聖剣/聖盾/神盾'),
    (59, '吸血鬼', '20F (6,6)', '十字架×2；ATK≤66 时零伤害'),
    (96, '大魔導師', '21F', '**战斗前把主角 HP 减半**；4500 血打不动'),
    (90, '金騎士', '32F (6,9)(11,1) / 40F', '守卫格，32F 两处 obj90 是动态写入'),
    (56, 'ロック', '27F 一带', 'DEF68 高、HP20 低；需祭坛升 ATK 才破防'),
    (58, '魔導師', '3F 剧本 / 42F / 48F / 49F', '夹击削半血；3F 那 4 只是扒装剧本'),
    (15, '門番Ｂ', '10F/20F/40F 交界', 'DEF110，早期 ATK 不够打不动'),
    (102, '門番Ａ', '多处', 'DEF360，后期怪'),
    (29, '門番Ｃ', '多处', ''),
    (101, '黒騎士', '49F (5,8)(7,8)', ''),
    (99, '魔術師Ａ', '41F 起', '相邻 −200'),
    (100, '魔術師Ｂ', '41F 起', '相邻 −100'),
]


# ---------------------------------------------------------------- 数据工具
def floors_with(obj):
    return [f for f in FLOORS if any(
        M.obj_raw(f, x, y) == obj for y in range(13) for x in range(13))]


def count_obj(obj):
    return sum(1 for f in FLOORS for y in range(13) for x in range(13)
               if M.obj_raw(f, x, y) == obj)


def cells_of(obj):
    return [(f, x, y) for f in FLOORS for y in range(13) for x in range(13)
            if M.obj_raw(f, x, y) == obj]


def fmt_cells(cs, limit=12):
    s = ' '.join('%dF(%d,%d)' % c for c in cs[:limit])
    if len(cs) > limit:
        s += ' …共%d' % len(cs)
    return s


def stairs_of(f):
    ups, dns = [], []
    for y in range(13):
        for x in range(13):
            t = M.WARP.get((f, x, y))
            if not t:
                continue
            (ups if t[0] > f else dns).append(((x, y), t))
    return ups, dns


# ---------------------------------------------------------------- 章节生成
def sec_head():
    return '''# 魔塔1 资料笔记

> **本文件由 `tools/gen_notes.py` 生成**——表格（物件/特殊格/事件/门钥/楼梯/各层/怪物）全部读数据自动生成，
> 机制结论是手工维护的常量。改结论请改脚本里的 `MECH` / `CHAINS` / `VOID`，不要直接改这个 md。
>
> - 数据源：`magic_tower1_map_50f.json`（静态）、`tools/dyn_raw.json`（事件写入）、
>   `magic_tower1_texts.md`（文案）、`08_Java_MTower08a/decompiled/MTower.java`（源码）
> - 权威口径：`tools/mota_core.py`（PC-98/Java 运行时口径）
> - 重跑：`cd 01_PC98原版_mtower/tools && python gen_notes.py`

## 〇、先读这三条（以前全都栽在这上面）

1. **两套 terrain 口径相反**：`mota_core.terrain()` 是 **1=墙 / 2=楼梯 / 0=地板**；
   而 `magic_tower1_map_50f.json` 的 `terrain` 字段是 **3=墙 / 1=地板**。混用会全错。
2. **obj2 是黄门不是钥匙**；obj1 才是黄钥匙。obj88 是盗贼 NPC，不是蓝钥匙。
3. **熔岩 obj79 是实心墙，不是伤害地砖**。`ichicheck` 只弹一行提示，不掉血、不清格。

'''


def sec_obj():
    out = ['## 一、物件编号权威表\n',
           '数量列为全塔（0..50F）**静态**格子数；静态为 0 但 `dyn_raw` 里有写入的，'
           '标成「事件生成」并给出写入楼层。\n',
           '| obj | 名称 | 分类 | 全塔数量 | 出现楼层 | 备注 |',
           '|---|---|---|---|---|---|']
    for o, (name, kind, note) in sorted(OBJ_NOTE.items()):
        n = count_obj(o)
        fl = floors_with(o)
        if n == 0:
            dyn_fl = sorted({f for f, items in M.FLOOR_WRITES.items()
                             for (_, _, oo) in items if oo == o})
            cnt = '事件生成'
            fls = ','.join(str(v) for v in dyn_fl) if dyn_fl else '—'
        else:
            cnt = str(n)
            fls = ','.join(str(v) for v in fl[:16]) + ('…' if len(fl) > 16 else '')
        out.append('| %d | %s | %s | %s | %s | %s |' % (o, name, kind, cnt, fls, note))
    out.append('')
    out.append('> 怪物编号（5-10、15-16、29、45-49、56、58、71、74、90-102 等）见 §十。\n')
    return '\n'.join(out)


def sec_special():
    out = ['## 二、特殊格总表\n', '### 2.1 凿墙事件（盗贼）\n',
           '| 被凿开的墙 | 触发格（盗贼） | 效果 |', '|---|---|---|']
    for wall, trig in sorted(M.DIG_WALLS.items()):
        out.append('| %dF(%d,%d) | %dF(%d,%d) | 墙变地板，打通捷径 |' % (wall + trig))
    out.append('')
    out.append('### 2.2 暗墙（撞塌）\n')
    out.append('| 层 | 坐标 | 类型 | 效果 |')
    out.append('|---|---|---|---|')
    for (f, x, y) in sorted(M.DARKWALL_CELLS):
        out.append('| %dF | (%d,%d) | 地形型 | 撞塌后露出红钥匙 obj28 |' % (f, x, y))
    obj89 = cells_of(89)
    by_floor = collections.Counter(f for f, _, _ in obj89)
    out.append('| 多 | 见下 | obj89 | 撞一次塌，可通行 |')
    out.append('')
    out.append('obj89 全塔 %d 处，按层：%s\n' % (
        len(obj89), '、'.join('%dF×%d' % kv for kv in sorted(by_floor.items()))))
    obj115 = cells_of(115)
    by_floor = collections.Counter(f for f, _, _ in obj115)
    out.append('obj115 隐形块全塔 %d 处，按层：%s\n' % (
        len(obj115), '、'.join('%dF×%d' % kv for kv in sorted(by_floor.items()))))
    out.append('> ⚠️ obj115 在 **23F 撞了会变墙**（源码 @5599 仅 23F 生效）；其余层的 obj115 是可直接穿过的隐形块。')
    out.append('> 23F 那 44 格按 8-连通分成 4 个字形：G / O / 0 / F = **"GO 0F"**，提示回地下层。\n')
    out.append('### 2.3 祭坛\n')
    out.append('| 层 | 坐标 |')
    out.append('|---|---|')
    for (f, x, y) in sorted(M.ALTAR_CELLS):
        out.append('| %dF | (%d,%d) |' % (f, x, y))
    out.append('')
    out.append('奉献额 `(k²-k+2)*10`（k=全塔已祭次数）→ 20/40/80/140/220/320…\n')
    out.append('### 2.4 商店\n')
    out.append('| 层 | 坐标 | obj | 商品 | 价格 |')
    out.append('|---|---|---|---|---|')
    for o, price in sorted(M.SHOP_PRICE.items(), key=lambda kv: kv[1]):
        cs = cells_of(o)
        for (f, x, y) in cs:
            out.append('| %dF | (%d,%d) | %d | %s | %d G |' % (
                f, x, y, o, SHOP_NOTE.get(o, '?'), price))
    out.append('')
    out.append('### 2.5 NPC\n')
    out.append('| obj | 层 | 坐标 | 台词要点 |')
    out.append('|---|---|---|---|')
    for o in (87, 88, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 152, 153, 161, 174, 175):
        for (f, x, y) in cells_of(o):
            note = OBJ_NOTE.get(o, ('', '', M.oname(o)[:40]))[2] or M.oname(o)[:34]
            out.append('| %d | %dF | (%d,%d) | %s |' % (o, f, x, y, note))
    out.append('')
    out.append('### 2.6 落穴与熔岩\n')
    for o, nm in ((19, '洞（掉层）'), (20, '落穴（实心）'), (79, '熔岩（实心）')):
        cs = cells_of(o)
        by_floor = collections.Counter(f for f, _, _ in cs)
        out.append('- **obj%d %s**：%d 格 — %s' % (
            o, nm, len(cs), '、'.join('%dF×%d' % kv for kv in sorted(by_floor.items()))))
    out.append('')
    return '\n'.join(out)


def sec_writes():
    out = ['## 三、全塔事件写入表（22 层，静态地图上看不到的东西）\n',
           '来源 `tools/dyn_raw.json`；`M.FLOOR_WRITES` 是同一份数据的 (x,y,obj) 形式。\n']
    for f in sorted(M.FLOOR_WRITES):
        items = M.FLOOR_WRITES[f]
        dedup = list(dict.fromkeys(items))
        parts = []
        for (x, y, o) in dedup:
            parts.append('(%d,%d)=obj%d %s' % (x, y, o, (OBJ_NOTE.get(o, ('', '', ''))[0] or M.oname(o)[:14] or '?')))
        out.append('- **%dF**：%s' % (f, '，'.join(parts)))
    out.append('')
    out.append('> 用法：静态 JSON 里这些格是空的/是墙，**不要以为走不通**。')
    out.append('> 反过来，像 38F (2,5) 这种「事件后才变成障碍」的格，也不能当通路。\n')
    return '\n'.join(out)


def sec_keys():
    out = ['## 四、门与钥匙\n']
    tot = {1: count_obj(1), 3: count_obj(3), 28: count_obj(28),
           2: count_obj(2), 4: count_obj(4), 27: count_obj(27)}
    out.append('| 颜色 | 钥匙 | 门 | 缺口 |')
    out.append('|---|---|---|---|')
    for key, door, nm in ((1, 2, '黄'), (3, 4, '蓝'), (28, 27, '红')):
        out.append('| %s | %d | %d | %+d |' % (nm, tot[key], tot[door], tot[key] - tot[door]))
    out.append('')
    out.append('**门永远开不完，必须挑门走。** 蓝门尤其紧张（20 把钥匙 vs 39 道门）。\n')
    out.append('### 逐层分布\n')
    out.append('| 层 | 黄钥 | 蓝钥 | 红钥 | 黄门 | 蓝门 | 红门 |')
    out.append('|---|---|---|---|---|---|---|')
    for f in FLOORS:
        c = {o: 0 for o in (1, 3, 28, 2, 4, 27)}
        for y in range(13):
            for x in range(13):
                o = M.obj_raw(f, x, y)
                if o in c:
                    c[o] += 1
        if any(c.values()):
            out.append('| %dF | %d | %d | %d | %d | %d | %d |' % (
                f, c[1], c[3], c[28], c[2], c[4], c[27]))
    out.append('')
    return '\n'.join(out)


def sec_stairs():
    out = ['## 五、楼梯（层内坐标，x,y）\n',
           '| 层 | 上行梯 → 目标层 | 下行梯 → 目标层 |', '|---|---|---|']
    for f in FLOORS:
        ups, dns = stairs_of(f)
        u = ' '.join('(%d,%d)→%dF@(%d,%d)' % (c[0], c[1], t[0], t[1], t[2]) for c, t in ups) or '（无，事件生成）'
        d = ' '.join('(%d,%d)→%dF@(%d,%d)' % (c[0], c[1], t[0], t[1], t[2]) for c, t in dns) or '（无）'
        out.append('| %dF | %s | %s |' % (f, u, d))
    out.append('')
    out.append('> ⚠️ 楼梯编号不能按奇偶猜：31F/34F/37F 是反的。一律以本表为准。')
    out.append('> BOSS 层（10/20/30/40/49）的上行梯是杀掉 BOSS 后由 eventMT 写入的，静态表里没有。\n')
    return '\n'.join(out)


def sec_mech():
    out = ['## 六、机制定论\n']
    for i, (title, body) in enumerate(MECH, 1):
        out.append('### 6.%d %s\n' % (i, title))
        out.append(body.strip() + '\n')
    return '\n'.join(out)


def sec_chains():
    out = ['## 七、时序依赖链（顺序错了就卡死）\n']
    for title, body in CHAINS:
        out.append('- **%s**：%s' % (title, body))
    out.append('')
    return '\n'.join(out)


def sec_void():
    out = ['## 八、已作废的旧结论（别再用）\n',
           '| 旧结论 | 为什么错 |', '|---|---|']
    for a, b in VOID:
        out.append('| %s | %s |' % (a, b))
    out.append('')
    return '\n'.join(out)


KEY_ITEMS = {30: '铁剑', 31: '銀の剣', 32: '骑士剑', 33: '聖剣', 34: '神剣',
             35: '铁盾', 36: '銀の盾', 37: '骑士盾', 38: '聖盾', 39: '神盾',
             25: '知恵のオーブ', 26: '飛翔のオーブ', 105: '破壊の玉', 107: '昇華の翼',
             108: '降臨の翼', 109: '屠龙匕', 110: '雪之结晶', 111: '魔法の鍵', 113: '幸运金币'}


def sec_floors():
    out = ['## 九、各层速查\n',
           '| 层 | 楼梯（下→上） | 关键道具/机关 | 门 黄/蓝/红 | 钥 黄/蓝/红 | NPC/商店 | 兽人系 | 特殊 |',
           '|---|---|---|---|---|---|---|---|']
    for f in FLOORS:
        ups, dns = stairs_of(f)
        st = ''
        if dns:
            st += '(%d,%d)' % dns[0][0]
        else:
            st += '—'
        st += '→'
        if ups:
            st += '(%d,%d)' % ups[0][0]
        else:
            st += '事件生成'
        # 关键道具
        items = []
        for y in range(13):
            for x in range(13):
                o = M.obj_raw(f, x, y)
                if o in KEY_ITEMS:
                    items.append('%s(%d,%d)' % (KEY_ITEMS[o], x, y))
                elif o == 22:
                    items.append('祭坛(%d,%d)' % (x, y))
        for o in M.SHOP_PRICE:
            for y in range(13):
                for x in range(13):
                    if M.obj_raw(f, x, y) == o:
                        items.append('商店(%d,%d)' % (x, y))
        # 门钥
        c = collections.Counter(M.obj_raw(f, x, y) for y in range(13) for x in range(13))
        doors = '%d/%d/%d' % (c[2], c[4], c[27])
        keys = '%d/%d/%d' % (c[1], c[3], c[28])
        # NPC
        npcs = []
        for o in (87, 88, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 152, 153, 161, 174, 175):
            for y in range(13):
                for x in range(13):
                    if M.obj_raw(f, x, y) == o:
                        npcs.append('obj%d(%d,%d)' % (o, x, y))
        # 兽人系
        zombie = c[48] + c[49]
        # 特殊
        spec = []
        for (ff, x, y) in M.DARKWALL_CELLS:
            if ff == f:
                spec.append('暗墙(%d,%d)' % (x, y))
        for wall, trig in M.DIG_WALLS.items():
            if trig[0] == f:
                spec.append('盗贼凿墙(%d,%d)' % (trig[1], trig[2]))
        L = c[79]
        if L:
            spec.append('熔岩%d格' % L)
        if f in M.FLOOR_WRITES:
            spec.append('事件写入%d项' % len(M.FLOOR_WRITES[f]))
        out.append('| %dF | %s | %s | %s | %s | %s | %d | %s |' % (
            f, st, ' '.join(items) or '—', doors, keys,
            ' '.join(npcs) or '—', zombie, ' '.join(spec) or '—'))
    out.append('')
    return '\n'.join(out)


def sec_monsters():
    out = ['## 十、重点怪物\n',
           '| obj | 名称 | 位置 | HP/ATK/DEF/GOLD | 备注 |', '|---|---|---|---|---|']
    for o, name, pos, note in MON_NOTE:
        a = [M.oatr(o, i) for i in range(15)]
        out.append('| %d | %s | %s | %d/%d/%d/%d | %s |' % (
            o, name, pos, a[10], a[11], a[12], a[13], note))
    out.append('')
    out.append('全量怪物四维见 `magic_tower1_monsters.csv`（41 个怪物 ID + 译文名）。\n')
    out.append('战斗公式（`attackDouble` 见 @6106）：\n')
    out.append('```')
    out.append('回合 = ceil(怪HP / (我ATK × attackDouble − 怪DEF))   # 每击 ≤0 则打不动')
    out.append('扣血 = max(0, 怪ATK − 我DEF) × (回合 − 1)                   # 最后一击不掉血')
    out.append('attackDouble: 持十字架 且 怪 ∈ {48,49,59} → 2')
    out.append('              持屠龙匕 且 怪 == 74     → 2')
    out.append('```\n')
    return '\n'.join(out)


def sec_artifacts():
    return '''## 十一、路线产物索引

| 文件 | 内容 | 状态 |
|---|---|---|
| `../09_TAS推演/魔塔1_route_21F到30F_原版.csv` | 21F→30F 逐格路线（144 行 / 128 步 / 战损 0） | ✅ 数值与拓扑均可信 |
| `../09_TAS推演/魔塔1_route_31F到38F_取骑士盾.csv` | 31F→38F 逐格路线（170 行 / 154 步 / 990 HP @ATK186） | ⚠️ 拓扑可用，数值按 ATK164 起算需重算 |
| `../09_TAS推演/魔塔1_route_11F到20F.csv` | 11F→20F（Dijkstra 步数最优口径） | ❌ 挑门策略错，钥匙账崩；需按绕门重排 |
| `../09_TAS推演/魔塔1_钥匙账_11F到38F_绕门版.csv` | 绕门优先的钥匙账（净 黄+16/蓝+2/红 0） | ✅ 账已闭合 |
| `tools/魔塔1_route_1F到21F.csv` 等 | 早期人类玩法回放（983~3233 行），**含真实钥匙库存轨迹** | 📌 当基线参考，不经 `plan.py` |
| `tools/plan.py` / `state.py` | 带断点的 A* 求解器 | ⚠️ 基线质量差（1F-10F 会跑崩），暂不可用于端到端验证 |
| `tools/mota_core.py` | 无头游玩内核（地形/物件/战斗/事件规则） | ✅ 规则权威 |
| `tools/gen_notes.py` | 生成本文件 | ✅ |

> ⚠️ **产物必须落在 `repo/` 之内**（`repo/09_TAS推演/`），`repo/` 才是 git 仓库的自带根。
> 写在 `mota_tas_tmp2/` 根目录的东西永远推不上 GitCode。

'''


def main():
    parts = [sec_head(), sec_obj(), sec_special(), sec_writes(), sec_keys(),
             sec_stairs(), sec_mech(), sec_chains(), sec_void(), sec_floors(),
             sec_monsters(), sec_artifacts()]
    txt = '\n'.join(parts)
    with open(OUT, 'w', encoding='utf-8') as fp:
        fp.write(txt)
    print('written', OUT, len(txt), 'chars')
    return OUT


if __name__ == '__main__':
    main()
