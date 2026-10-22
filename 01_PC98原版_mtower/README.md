# 01_PC98原版_mtower

> 发行版 asset：`01_PC98原版_mtower.fdi`（attach id 257750）

## 版本真身

**魔法の塔 Ver1.1**（1996，N.W / Oz & Kenichi 前身作品）——PC-9801VX 及 98 兼容机 + MS-DOS 3.1+ 的 PC-98 原版，50 层，开局 HP 1000 / 攻击 100 / 防御 100（神剑神盾）。

| 项 | 值 |
|---|---|
| 主程序 | `game/MTE.EXE`（101303 B，MZ 格式） |
| 文档 | `game/MTE.DOC`（键位与玩法说明） |
| 地图/数据 | `MTOWER1.P58` / `MTOWER2.P58` / `MONSTER.P58` / `ITEM.P58` / `WEAPON.P58` / `GROUND.P58` 等 |
| 磁盘系统 | MS-DOS 5.00A（IO.SYS 为隐藏系统文件），`AUTOEXEC.BAT` 自动运行 `MTE.EXE` |
| 介质 | `01_PC98原版_mtower.fdi`——FDI 映像（4096 B 头 + 1.44 MB 原始盘，80 柱×2 头×18 扇区×512 B） |

## 目录内容

```
01_PC98原版_mtower/
├── 01_PC98原版_mtower.fdi   # 原始发行介质（FDI 软盘映像）
├── game/                    # 从 FDI 提取的全部文件（23 个）
│   ├── MTE.EXE              # 游戏本体
│   ├── COMMAND.COM / IO.SYS(隐藏) / MSDOS.SYS(隐藏)
│   ├── AUTOEXEC.BAT         # 内容：MTE.EXE
│   ├── CONFIG.SYS           # files=20, buffers=30
│   ├── MT.GTX / *.P58       # 地图、怪物、物品、武器等数据
│   ├── INITIAL.DAT          # 游戏存档
│   └── MTE.DOC              # 说明书
├── floor1_01_MTE.png        # 第 1 层实机截图
├── floor1_01_MTE_after_move.png  # 按小键盘 2 后的对比图（923 像素差异，验证可操作）
├── map_50f.png              # 50 层总览（实贴图渲染，顶行第 1 列为 00 层）
├── floors/                  # 单层实贴图渲染 floor_01..50.png + floor_00.png + 23/35 标注图
├── tiles/                   # 189 块 imgCrop 实体贴图的切片
├── magic_tower1_map_50f.json    # 逐层地形/物体/暗墙/隐藏层/实体 + 事件动态写入数据
├── magic_tower1_entities.csv    # 全部实体布点（层,y,x,obj,kind,role,名称,HP/ATK/DEF/GOLD）
├── magic_tower1_monsters.csv    # 怪物与道具战力总表
├── magic_tower1_dynamic.csv     # 事件后才出现的隐藏物体 / 动态地形
├── magic_tower1_texts.csv         # 全部塔内文案（日/英 + 引用处 + 出现层），正文见本文件附录
├── magic_tower1_rows.csv        # 大表逐行标记（S 暗墙 / T 隐形块 / E 实体 / B BOSS）
├── magic_tower1_walkroute.md    # 走法路线、危险格、00 层通达方式、隐藏物体说明
├── hidden_floor_band5.png / floor_00.png / MTower_sheet.gif
├── tools/dynscan.py             # 提取“事件动态写入格子”的脚本
├── tools/gen_texts.py           # 生成本文件文案附录与 magic_tower1_texts.csv
└── README.md
```

## 怪物战力表

数据源：`magic_tower1_monsters.csv`（战力四维与 `name_cn` 经典译名）。「怪物译名」为经典中文版叫法，「怪物原名」为游戏内日文原名，
依据[百度百科「50层魔塔」词条](https://baike.baidu.com/item/50%E5%B1%82%E9%AD%94%E5%A1%94/4446423)的“敌人资料”表，按 HP/ATK/DEF 与出现楼层逐条比对得到（金币列个别行该表与原数据有小差异，故只用于对名字，不改数值）。
表内顺序即爬塔顺序（按各怪首次出现层排序）。部分怪在原版里被拆成多个 ID（如大乌贼），因此会有同名多行。

| id | 怪物译名 | 怪物原名 | HP | ATK | DEF | GOLD |
|---:|---|---|---:|---:|---:|---:|
| 5 | 绿色史莱姆 | Ｇスライム | 35 | 18 | 1 | 1 |
| 7 | 小蝙蝠 | バット | 35 | 38 | 3 | 3 |
| 6 | 红色史莱姆 | Ｒスライム | 45 | 20 | 2 | 2 |
| 9 | 骷髅人 | スケルトンＣ | 50 | 42 | 6 | 6 |
| 10 | 骷髅士兵 | スケルトンＢ | 55 | 52 | 12 | 8 |
| 8 | 初级法师 | 僧侶 | 60 | 32 | 8 | 5 |
| 15 | 中级卫兵 | 門番Ｂ | 100 | 180 | 110 | 100 |
| 29 | 初级卫兵 | 門番Ｃ | 50 | 48 | 22 | 12 |
| 16 | 骷髅队长 | スケルトンＡ | 100 | 65 | 15 | 30 |
| 47 | 大蝙蝠 | 大バット | 60 | 100 | 8 | 12 |
| 46 | 高级法师 | 上級僧侶 | 100 | 95 | 30 | 22 |
| 45 | 大史莱姆 | Ｂスライム | 130 | 60 | 3 | 8 |
| 48 | 兽人 | ゾンビ | 260 | 85 | 5 | 18 |
| 56 | 石头人 | ロック | 20 | 100 | 68 | 28 |
| 49 | 兽人武士 | ゾンビナイト | 320 | 120 | 15 | 30 |
| 50 | 大乌贼 | 大ダコの一部 | 1200 | 180 | 20 | 50 |
| 51 | 大乌贼 | 大ダコの一部 | 1200 | 180 | 20 | 50 |
| 52 | 大乌贼 | 大ダコの一部 | 1200 | 180 | 20 | 50 |
| 60 | 大乌贼 | 大ダコの一部 | 1200 | 180 | 20 | 50 |
| 61 | 大乌贼 | 大ダコの一部 | 1200 | 180 | 20 | 50 |
| 62 | 大乌贼 | 大ダコの一部 | 1200 | 180 | 20 | 50 |
| 70 | 大乌贼 | 大ダコの一部 | 1200 | 180 | 20 | 50 |
| 71 | 大乌贼 | 大ダコ | 1200 | 180 | 20 | 100 |
| 72 | 大乌贼 | 大ダコの一部 | 1200 | 180 | 20 | 50 |
| 95 | 幽灵 | スライムマン | 320 | 140 | 20 | 30 |
| 96 | 大法师 | 大魔導師 | 4500 | 560 | 310 | 1000 |
| 92 | 双手剑士 | 剣士 | 100 | 680 | 50 | 55 |
| 91 | 骑士 | 騎士 | 160 | 230 | 105 | 65 |
| 93 | 战士 | 兵士 | 210 | 200 | 65 | 45 |
| 94 | 鬼战士 | 死霊兵士 | 220 | 180 | 30 | 35 |
| 74 | 魔龙 | ドラゴン | 1500 | 600 | 250 | 800 |
| 90 | 骑士队长 | 金騎士 | 120 | 150 | 50 | 100 |
| 97 | 吸血蝙蝠 | 吸血コウモリ | 200 | 390 | 90 | 50 |
| 99 | 高级巫师 | 魔術師Ａ | 200 | 380 | 130 | 90 |
| 100 | 初级巫师 | 魔術師Ｂ | 220 | 370 | 110 | 80 |
| 58 | 魔法警卫 | 魔導師 | 230 | 450 | 100 | 100 |
| 98 | 史莱姆王 | Ｋスライム | 360 | 310 | 20 | 40 |
| 101 | 黑暗骑士 | 黒騎士 | 180 | 430 | 210 | 120 |
| 102 | 高级卫兵 | 門番Ａ | 180 | 460 | 360 | 200 |
| 59 | 吸血鬼 | バンパイア | 444 | 199 | 66 | 144 |
| 57 | 魔王（假魔王） | 魔導師ゼノ | 8000 | 5000 | 1000 | 500 |

### 战斗结算规则（读自 `MTower.class` 的 `attackMonster` / `monsStatus`，非推测）

- 我方单次伤害 = `ATK × attackDouble − 怪DEF`；当 `ATK × attackDouble ≤ 怪DEF` 时无法造成伤害。
- `attackDouble` 默认为 1，`monsStatus` 里按怪物 id 判定两处翻倍：
  - 持有 **十字架** 且怪物为 id 48 / 49 / 59（ゾンビ / ゾンビナイト / バンパイア）→ 翻倍；
  - 持有 **ドラゴンスレーヤー** 且怪物为 id 74（ドラゴン）→ 翻倍。
- 我方损失 = `(怪ATK − 我DEF) × (出手回合数 − 1)`，即打死对手的那最后一击不掉血。
- 上述标记与主角四维都不在普通变量里，而是写在 `mapObject` 数组的 stage_flags 块格子上（下表为数组下标 `[row][col]`）：
  十字架持有 `mapObject[74][119] == 1`、屠龙剑持有 `mapObject[70][120] == 1`；
  主角 HP `mapObject[66][118]`、ATK `mapObject[67][118]`、DEF `mapObject[68][118]`、GOLD `mapObject[69][118]`。

### 三点提醒

- **id 71 大乌贼不是一只怪，而是一只 9 格的怪**：15F 的大乌贼由中央 `71` + 八块躯体
  `50/51/52/60/61/62/70/72` 组成，**九格全部是独立战斗单位**（均 1200/180/20，躯体各给 50 GOLD、中央给 100），
  所以表里出现 9 行同值记录，它们是**同一只**大乌贼的九格（该词条“汉化缺陷”一节亦提到原版可打 9 次、共得 500 金币）。
- **id 74 魔龙 的九宫格不同**：35F 的中央可战斗格是 `(x=6, y=7)`，1500/600/250/800；
  环绕它的 `53/54/55/63/64/65/73/75` 是躯体装饰格（kind 0、HP/ATK/DEF/GOLD 全为 0）——
  **不可战斗也不能通过**，打龙只需打中央那一格。
- **id 57 魔王（假魔王）与 id 59 吸血鬼 在关卡布点表里没有战斗位**：
  id 59 吸血鬼由 `banpaia` 事件在 20F `(6,6)` 现场生成；id 57 魔王只登记于图鉴块，
  但 `loadMapData` 另有一处把它写到 24F `(1,11)`，而运行时 dump 的那格已不是 57（被后续流程覆盖）——
  这个不一致我没有替它下结论，TAS 若要精确复现需另行确认。

## 运行方式

PC-98 环境（np2kai 模拟器 + 真实 BIOS ROM）：

```bash
np2kai 01_PC98原版_mtower.fdi
```

启动后 MS-DOS 5.00A 自动通过 AUTOEXEC.BAT 运行 MTE.EXE，直接进游戏。

**键位**（据 `MTE.DOC`）：

- 小键盘 **2/4/6/8**（或方向键）：移动
- **Return / Space**：打开菜单
- **小键盘回车**：菜单内确认
- **Pause 键 = PC-98 STOP**：退出游戏回 DOS

环境搭建要点见仓库根目录 README「PC-98 运行环境」一节。

## 备注

- 本版是整个「魔法の塔」系列的 **PC-98 原版源头**（1996），历史地位最重要。
- 06 版（小学生版）即在本版磁盘环境里运行 `MTJR.COM` 补丁生成 `MTJR.EXE` 得到，二者地图数据同源。

## 附录：塔内全部对话 / 提示文案

来源：`MTower.class` 运行时的 `strMessage[2][400]`（`[1]` 日文、`[0]` 英文），实际有效 **309** 条，索引即引擎里的 `strNumber`。机读版同内容见 `magic_tower1_texts.csv`。

分组一览：怪物与 BOSS 名称 34 · 装备与道具名称 25 · 战斗与道具使用反馈提示 30 · 存档 · 音效 · 版本等系统提示 24 · 盗贼 15 · 具名人物台词 35 · 无名提示与谜面 35 · 道具 / 装备 / 钥匙：拾取与使用 51 · 商人 · 祭坛 · 积分石 · 智慧之戒问答 16 · 地形与调查提示 17 · 界面 · 系统文案 26 · 其它未归类文案 1

每条标题行的**引用方式**有四类：

- `objN（数据引用）` / `地形N（数据引用）`——由对象表 / 地形表的 `ATR_STRING` 列挂上，「出现层」即该对象（地形）实际铺在的楼层；
- `代码 strNumber=N ← 函数名`——由指令流里 `sipush N; putfield strNumber` 直接指定（开场与战后台词、钥匙不足、菜单确认等），这类文案不挂在地图数据上；
- `运行时按计算下标引用`——文案确实会在游戏里显示，但引用处的下标是算出来的（按楼层、分支、序号偏移，如盗贼台词与状态窗标签），我没能静态定位到具体引用点，所以直说"未定位"而不猜归属；
- 出现层为 `—` 表示它不来自地图数据，因此没有楼层概念。

### 怪物与 BOSS 名称（34 条）

**[100]** 　obj5（数据引用） 　·  出现层：1,3-9,30,34 catalog

> Ｇスライム
>
EN: Green Slime

**[101]** 　obj6（数据引用） 　·  出现层：1,3-9,30,34,46 catalog stage_flags

> Ｒスライム
>
EN: Red Slime

**[102]** 　obj45（数据引用） 　·  出现层：11-12,14-19,30,34 catalog

> Ｂスライム
>
EN: Big Slime

**[103]** 　obj7（数据引用） 　·  出现层：1,3-9,11-12,15,19-20,34 catalog

> バット
>
EN: Bat

**[104]** 　obj8（数据引用） 　·  出现层：1,3-10 catalog stage_flags

> 僧　侶
>
EN: Priest

**[105]** 　obj46（数据引用） 　·  出现层：11-12,14-20 catalog

> 上級僧侶
>
EN: Superion Priest

**[106]** 　obj29（数据引用） 　·  出现层：8,17 catalog

> 門番Ｃ
>
EN: Gate-Keeper C

**[107]** 　obj15（数据引用） 　·  出现层：2,32,38 catalog

> 門番Ｂ
>
EN: Gate-Keeper B

**[108]** 　obj9（数据引用） 　·  出现层：1,3-4,6-10,46 catalog

> スケルトンＣ
>
EN: Skeleton C

**[109]** 　obj10（数据引用） 　·  出现层：1,4-10 catalog

> スケルトンＢ
>
EN: Skeleton B

**[110]** 　obj16（数据引用） 　·  出现层：10 catalog stage_flags

> スケルトンＡ
>
EN: Skeleton A

**[111]** 　obj47（数据引用） 　·  出现层：11-12,14-20,46 catalog

> 大バット
>
EN: Big Bat

**[112]** 　obj48（数据引用） 　·  出现层：11-12,14-19,38,46 catalog

> ゾンビ
>
EN: Zombie

**[113]** 　obj49（数据引用） 　·  出现层：14-19,31,33,36 catalog

> ゾンビナイト
>
EN: Zombie Knight

**[114]** 　obj56（数据引用） 　·  出现层：14,16,18-20 catalog

> ロック
>
EN: Rock

**[115]** 　obj57（数据引用） 　·  出现层：catalog

> 魔導師ゼノ
>
EN: Magic Serg. Zeno

**[116]** 　obj58（数据引用） 　·  出现层：41-43,45,48 catalog

> 魔導師
>
EN: Magic Sergeant

**[117]** 　obj59（数据引用） 　·  出现层：catalog

> バンパイア
>
EN: Vampire

**[118]** 　obj71（数据引用） 　·  出现层：15 catalog

> 大ダコ
>
EN: Giant Octopus

**[119]** 　obj74（数据引用） 　·  出现层：35 catalog

> ドラゴン
>
EN: Dragon

**[120]** 　obj90（数据引用） 　·  出现层：40 catalog

> 金騎士
>
EN: Golden Knight

**[121]** 　obj91（数据引用） 　·  出现层：31-32,34,36-40,46 catalog

> 騎　士
>
EN: Knight

**[122]** 　obj92（数据引用） 　·  出现层：31,33-34,36-40,46 catalog

> 剣　士
>
EN: Swordsman

**[123]** 　obj93（数据引用） 　·  出现层：31-34,36-40,46 catalog

> 兵　士
>
EN: Soldier

**[124]** 　obj94（数据引用） 　·  出现层：31-34,36-40 catalog

> 死霊兵士
>
EN: Ghost Soldier

**[125]** 　obj95（数据引用） 　·  出现层：16,31-34,36-40 catalog

> スライムマン
>
EN: Slime Man

**[126]** 　obj96（数据引用） 　·  出现层：25 catalog

> 大魔導師
>
EN: Great Magic Master

**[127]** 　obj97（数据引用） 　·  出现层：41-43,45-48 catalog

> 吸血コウモリ
>
EN: Vampire Bat

**[128]** 　obj98（数据引用） 　·  出现层：41-43,45-48 catalog

> Ｋスライム
>
EN: SlimeLord

**[129]** 　obj99（数据引用） 　·  出现层：41-43,45-49 catalog

> 魔術師Ａ
>
EN: Magician A

**[130]** 　obj100（数据引用） 　·  出现层：41-43,45-48 catalog stage_flags

> 魔術師Ｂ
>
EN: Magician B

**[131]** 　obj101（数据引用） 　·  出现层：42-43,45,48-49 catalog

> 黒騎士
>
EN: Dark Knight

**[132]** 　obj102（数据引用） 　·  出现层：44 catalog

> 門番Ａ
>
EN: Gate-Keeper A

**[244]** 　obj50、obj51、obj52 等5项（数据引用） 　·  出现层：15 catalog

> 大ダコの一部
>
EN: some of Giant Octopus

### 装备与道具名称（菜单用的短名）（25 条）

**[270]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 鉄の剣
>
EN: Iron

**[271]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 銀の剣
>
EN: Silver

**[272]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 騎士の剣
>
EN: Knight

**[273]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 聖　剣
>
EN: Holy

**[274]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 神　剣
>
EN: Sacred

**[275]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 鉄の盾
>
EN: Iron

**[276]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 銀の盾
>
EN: Silver

**[277]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 騎士の盾
>
EN: Knight

**[278]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 聖　盾
>
EN: Holy

**[279]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 神　盾
>
EN: Sacred

**[299]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 勇者のオーブ
>
EN: The orb of the hero

**[300]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 知恵のオーブ
>
EN: The orb of wisdom

**[301]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 飛翔のオーブ
>
EN: The orb of flying

**[302]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 十字架
>
EN: A cross

**[303]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> エリクサー
>
EN: The Magic Elixir

**[304]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> マトック
>
EN: The Magic Mattock

**[305]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 破壊の玉
>
EN: The Destructible Ball

**[306]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 空間転移の秘宝
>
EN: The Warp Staff

**[307]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 昇華の翼
>
EN: Wings to fly up

**[308]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 降臨の翼
>
EN: Wings to fly down

**[309]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ドラゴンスレーヤー
>
EN: The Dragon Slayer

**[310]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 雪の結晶
>
EN: The snow crystal

**[311]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 魔法の鍵
>
EN: The magic key

**[312]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> スーパーマトック
>
EN: The Super Magic Mattock

**[313]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 幸運の金貨
>
EN: The Lucky Gold

### 战斗与道具使用反馈提示（30 条）

**[57]** 　obj40（数据引用） 　·  出现层：catalog

> 「この塔は全部で５０階建てで、１０階ごとに１つのブロックを形成している。塔の内部には、各ブロックを統括するボスが配置されていて、そいつらを倒さないことには、それより上の階に行くことはできないだろう。」
>
EN: "This tower has fifty floor. Every ten floor form one area. The boss who controls each area, are posted in this tower. You cannot ascend from there if you don't beat them."

**[74]** 　obj148（数据引用） 　·  出现层：45

> 「この塔の４４階は幻の階じゃ。普通の階段を登り降りしたのでは行くことができないらしい。ワープでもしないかぎり行くことは不可能じゃろう。」
>
EN: "The 44th floor in this tower is an illusion. It seems that we cannot go to there even if we use the stairs. I think that it is impossible to get there without teleporting."

**[154]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 飛翔のオーブを使った！
>
EN: Used the orb of flying!

**[155]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 祭壇がある。
>
EN: You see an altar.

**[190]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> エリクサーを使った！生命力が
>
EN: Used the Magic Elixir. Your vital power was

**[191]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> マトックを使った！四方の壁が崩れた！
>
EN: Used the Magic Mattock! The walls fell down!

**[192]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 破壊の玉を使った！四方の敵が倒れた！
>
EN: Used The Destructible Ball! Enemies on all sides died!

**[193]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 空間転移した！
>
EN: Warped!

**[194]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 昇華の翼を使った！
>
EN: Used the wing to fly up!

**[195]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 降臨の翼を使った！
>
EN: Used the wing to fly down!

**[196]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 雪の結晶を使った！
>
EN: Used the snow crystal!

**[197]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 魔法の鍵を使った！この階の扉がすべて開いた！
>
EN: Used the Magic Key! All these doors opened on this floor.

**[198]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> スーパーマトックを使った！この階の壁がすべて崩れた！
>
EN: Used the Super Magic Mattock! All the walls fell down on this floor!

**[199]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 転送先に障害物があって空間転移ができない！
>
EN: Can't warp (There's an object in the way).

**[200]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 上の階に障害物があって転移ができない！
>
EN: Can't go upstairs (it's blocked)!

**[201]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 下の階に障害物があって転移ができない！
>
EN: Can't go downstairs (it's blocked)!

**[203]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> をたおした！
>
EN: You've beat

**[214]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ・やっぱりやめる
>
EN: Then I won't do it after all.

**[221]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 相手の防御力が高すぎて攻撃ができない！
>
EN: You can't battle him. Because his defensive power is too high!

**[226]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> うーん、この点数だとこれから先へ進むのは、かなり無理があるでしょう。」
>
EN: If you have that many points, you might want to reconsider going higher..."

**[227]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> いまひとつですね。これから先はかなり苦戦するでしょう。」
>
EN: A bit below average. Maybe you should try harder."

**[228]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> まあまあですね。この点数ならこれから先もなんとかなるでしょう。」
>
EN: You are ordinary. You might get by okay!"

**[229]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> なかなかのものです。もう少し頑張れば称号を差し上げましょう。」
>
EN: Doing fine! If you wish to continue, I will give you a special rank..."

**[230]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> おめでとう！満点です。
>
EN: Congratulations! Your score is GREAT!

**[231]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> よくがんばりましたね。
>
EN: Do you wish to go on?

**[241]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 魔術師Ａの魔法攻撃だ！生命力が２００ポイント減少！
>
EN: Your vital power decreased 200 points by magic attack of Magician A!

**[242]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 魔術師Ｂの魔法攻撃だ！生命力が１００ポイント減少！
>
EN: Your vital power decreased 100 points by magic attack of Magician B!

**[243]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 魔導師の魔法攻撃だ！生命力が半減！
>
EN: Your vital power decreased in half by the magic attack of Magic Master!

**[247]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 階段を移動中
>
EN: You are using the stairs.

**[269]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ドラゴンが火を吹いた！生命力が１０００ポイント減少！
>
EN: Dragon blew on the fire! Your vital power decreased 1000 points.

### 存档 · 音效 · 版本等系统提示（24 条）

**[97]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 表示する情報がありません。
>
EN: You don't have an informations any more.

**[184]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> この階にいるモンスターの生命力、攻撃力、防御力、プレーヤーの受けるダメージを検索
>
EN: Looking up the results of battling these monsters.

**[246]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> セーブデータがありません。
>
EN: Nobody saved that game yet.

**[248]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> おめでとう！得点が第
>
EN: Congratulations! You win the

**[249]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 位の成績でした。
>
EN: place with the points which you got.

**[250]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> データをロード(読み込み)しました。
>
EN: Loaded the Game.

**[251]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> データをセーブ(保存)しました。
>
EN: Saved the Game.

**[253]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> このデータはロードできません。
>
EN: This Game can't load.

**[268]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> Magic Tower Ver0.8a

**[281]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 上書きします。よろしいですか？
>
EN: Over write. Is it true ?

**[282]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 情報番号
>
EN: Information No.

**[284]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 実行中...
>
EN: Executing...

**[285]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> セーブできません。ポリシーツールで入出力の設定をして下さい。
>
EN: Can't save this game. Please set by policytool.

**[286]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ランキングデータを初期化しました。
>
EN: Initialized Ranking data.

**[287]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ランキングデータを初期化できません。ポリシーツールで入出力の設定をして下さい。
>
EN: Can't initialize this raning data. Please set by policytool.

**[288]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> このデータはロードできません。
>
EN: This data can't load.

**[289]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> Wav サウンドオン！
>
EN: Wav sound on.

**[290]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> Midiバックグラウンドミュージックオン！
>
EN: Midi Background music on.

**[291]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> サウンドオフ！　ＢＧＭオフ！
>
EN: Sound and Background music off.

**[292]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> サウンドオフ！
>
EN: Sound off.

**[293]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> バックグラウンドミュージックオフ！
>
EN: Background music off.

**[294]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> Au サウンドオン！
>
EN: Au sound on.

**[295]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> Auバックグラウンドミュージックオン！
>
EN: Au Background music on.

**[314]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> アイテムを使用します。よろしいですか？
>
EN: Do you use this item?

### 盗贼（脱出屋）对白（15 条）

**[4]** 　obj87（数据引用） 　·  出现层：2 catalog

> 盗賊「おお無事か！おまえ、ここの魔導師に捕まってこの牢屋に入れられてたんだよ。で、今まで気を失っていた訳だ。にしても、おまえ運がいいぜ。ちょうど抜け穴が完成したときに来るんだからな。そういう訳で俺は今から脱走するところだ。おまえもついてこい。」
>
EN: The thief says "What a relief you're okay!
　　 You were caught and thrown into this prison by the Magic Sergeant.
　　 You were unconscious when you got here.
　　 Nevertheless, you are so lucky that you just woke up.
　　 I've finished the escape tunnel. Let's break out."

**[5]** 　代码 `strNumber=5` ← attackMonster/directCheck/pointCheck 　·  出现层：—

> 盗賊「よし、じゃあ俺は先に行かせてもらうぜ。ああ、それからおまえの剣と盾、あいつらに取り上げられちまったみたいだな。この塔の中を丸腰で歩き回るのはやめた方がいい。確か５階に剣、９階に盾があったはずだから、まずそれを手に入れることを考えるんだな。じゃあ、またなっ！」
>
EN: The thief says "O.K. Well, excuse my going first. Your weapon and shield were stolen by the guards. It's not wise to wander about without them. I heard that there is a sword on the 5th floor and a shield on the 9th. You had better get them. See you!"

**[6]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 盗賊「ようっ！また会ったな。ここの門番を倒してくれて助かったぜ、ドジってまた捕まっちまってな。今度は、こんな奥の牢に閉じ込められちまった。まあ、それはそれとして、３５階にいるドラゴンの手前まで抜け穴を掘っといたんだ。開通させとくから先に行っててくれ。」
>
EN: The thief says "Ah, we meet again! Thank you. You beat the Gate-Keeper of this area. I was defeated and imprisoned again. Such a small prison this time. I'm making a secret tunnel in front of the Dragon. Go up to 35th floor and wait for me, while I complete the tunnel."

**[7]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 盗賊「後でちゃんと行くから３５階まで先に行っておいてくれ。」
>
EN: The thief says "Don't worry, I'll be there."

**[16]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 盗賊「よっ！またあったな。すげえじゃねえか。ここのブロックのボスを倒すとはよ。俺もこれ以上、先の階へ行けなくて困ってたんだ。ああ、あと聞いた話だが、１１階に盾、１７階に剣があるそうだ。盾よりも剣の方を先に取りに行った方がいいそうだから、うまく敵をかわして剣を先に取りに行くんだな。じゃ、お先に！」
>
EN: The thief says "Hey! We meet again! How greatly you beat the boss of this area. It troubled me that I couldn't go upstairs any more. After I heard that there is a shield on the 11th floor and a sword on the 17th. You had better get a sword first and then a shield. Please excuse my going first!"

**[17]** 　obj88（数据引用） 　·  出现层：catalog

> 盗賊「よおっ！無事だったか？ここの大ダコが道をふさいでいて困っていたんだが今ようやく抜け穴が完成したんだ。おまえも、ここの大ダコを倒すのは後回しにした方がいいぜ。じゃあ、またなっ！」
>
EN: The thief says "Ah! Are you all right? The Big Octopus which lives in here was blocking my progress. Now a loophole has completed at last. You had better put off beating him. See you later!"

**[24]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 盗賊「あっ！まだ抜け穴、完成してなかったのに・・・もう少し待ってればアイテムを使わずにすんだはずだぞ。予定が狂っちまうな・・・いや、気にしないでくれ。」
>
EN: The thief says "The tunnel has not been completed yet. You should have waited a little longer, and you should not have used items. I had a bug in the program. There! Don't worry!"

**[25]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 盗賊「ああ、やっと抜け穴が完成した。あれ？またお前か。いいタイミングできたな。また抜け穴作っといたぜ。自由に使ってくれ。」
>
EN: The thief says "Oh, I have finished the tunnel. What? It's you again. You came at a good time. I have openned a tunnel, and you may use it freely."

**[26]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 盗賊「このブロックに最後のボスと捕まったプリンセスがいるはずだが、今はまだ戦うのは早すぎるだろうな。」
>
EN: The thief says "The last boss and the captured princess must be in this area. Hmm, I wonder if we should wait before fighting him."

**[29]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 盗賊「おお、来たか。ちゃんと、抜け穴を開通させておいたぜ、この抜け穴を通ればドラゴンの後ろに出られるから、そこから上の階に行くんだな。」
>
EN: The thief says "There you are. I have just finished the tunnel. As you go through it, you will get to the Dragon. And then you should go up."

**[30]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 盗賊「このブロックのボスの金騎士は弱いくせに態度だけはでかいから、この塔の副将格の魔導師ゼノには嫌われているらしい。」
>
EN: The thief says "The Golden Knight (who is the boss of this area) has a strong attitude in spite of being weak. It is for this reason that he is disliked by the Magic Serg. Zeno, who is the sub commander of this tower."

**[44]** 　代码 `strNumber=44` ← eventMT 　·  出现层：—

> 盗賊「ふふふ……ここにいるという事は、答えは１つしかあるまい。こういう事だっ！」
>
EN: The thief says "Humph. There is only one reason why I'm here. And this is it!"

**[59]** 　obj157（数据引用） 　·  出现层：—

> 「９階と１６階と１８階の抜け穴には気が付いたかい？」
>
EN: "Did you notice the secret passages on the 9th, 16th, and 18th floors?"

**[68]** 　obj144（数据引用） 　·  出现层：36

> 「この階の４つの抜け穴をうまく使えば、強い敵とは戦わずに上の階に行けるじゃろう。」
>
EN: "You may be able to go upstairs without fighting strong enemies, if you could use four tunnels skillfully in this floor."

**[99]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 盗賊「ようまたあったな！無事だったか？これは聞いた話なんだが、２５階のボスを倒すと『時空の門』がどこかにできるらしいぞ。」
>
EN: The thief says "Ah!, we meet again! Thank goodness you're alive! I heard that if you beat the boss of 25th floor, 'the gate of time and space' will appear somewhere."

### 具名人物台词（ゼノ・スケルトンＡ・バンパイア・大魔導師・老人・妖精・勇者…）（35 条）

**[10]** 　obj177（数据引用） 　·  出现层：—

> 魔導師ゼノ「ようこそ、『魔法の塔』へ。おまえがちょうど１００人目の侵入者だ。本来なら手下共に相手をさせるところだが、特別にこの私が自ら相手になってやろう。己の不運を呪うのだな。」
>
EN: The Magic Serg. Zeno says "Welcome to 'The Magic Tower'. You are the hundredth man who dared to enter my tower. You will now face my guards. Should you happen to survive, I will fight with you in person specially. You should accept your fate."

**[11]** 　obj178（数据引用） 　·  出现层：—

> 勇者「なんだっ！？　うわ～っ！？」
>
EN: The brave man says "What? Oh!"

**[13]** 　代码 `strNumber=13` ← eventMT 　·  出现层：—

> スケルトンＡ「ふふふ、よくここまできたな。かくなる上はこの俺様がじきじき相手になってやる・・・といいたいところだが、まずは貴様の力を見せてもらうぞ！出会え！スケルトン兵士たちよ！」
>
EN: Skeleton A "Ha ha ha, You are lucky to have gotten so far. Since it has come to this, I shall fight with you personally, but first I must test your strength. Go and fight! Skeleton Soldiers!"

**[14]** 　代码 `strNumber=14` ← eventMT 　·  出现层：—

> スケルトンＡ「ほほう、なかなか・・・。だが、ここから先へは行かせん！ここで葬ってくれるわっ！さあ、こいっ！！！」
>
EN: Skeleton A "How considerably you do. But I will never let you pass. Here, you will die. Fight me!"

**[15]** 　代码 `strNumber=15` ← eventMT 　·  出现层：—

> スケルトンＡ「ううう・・・よくぞこの俺様を倒せたものだ・・・。しかし、これから先の階はこれまでとは比べものにならんほど強力な敵とワナが待っているぞ、せいぜい気を付けることだな・・・」
>
EN: Skeleton A "No, It's not possible! You may have defeated me, but beyond this point you must meet some enemies and snares that are powerful beyond anything you've seen. If careless, you will die!"

**[19]** 　代码 `strNumber=19` ← eventMT 　·  出现层：—

> バンパイア「ほほう、貴様か、スケルトンを倒して侵入してきた勇者というのは・・・だがこの私をスケルトン共のようなザコと一緒にするなよ。不死に等しいこの私の力を見せてやろう。さあ、こいっ！」
>
EN: Vampire "Well, You beat the skeletons and invaded. Never regard me as small like a skeleton. I will show you that I am as immortal as god. Hey, come on!"

**[20]** 　代码 `strNumber=20` ← eventMT 　·  出现层：—

> バンパイア「ううう・・・よもや、この私までもが敗れるとは・・・どうやら貴様の力は本物のようだな・・・だが、その程度では大魔導師様には絶対にかなわんぞ、せいぜい束の間勝利に酔いしれているがいい・・・」
>
EN: Vampire "Good god! I've never dreamed I'd be defeated. There is no doubt of your strength. But you will never win against the Great Magic Master as weak as you are. You shall only celebrate fleeting victory at most."

**[21]** 　代码 `strNumber=21` ← eventMT 　·  出现层：—

> 大魔導師「・・・ジ・・・ユウシャ・・・・・コロス・・・」
>
EN: Great Magic Master "-K-I-L-L- -A-N- -I-N-V-A-D-E-R- "

**[23]** 　obj44（数据引用） 　·  出现层：26 catalog

> 勇者「これはっ……！人形だっ！」
>
EN: The brave man says "Oh! What? This is a doll!"

**[27]** 　代码 `strNumber=27` ← eventMT 　·  出现层：—

> 金騎士「貴様だな、第１、第２ブロックのボスを倒し登ってきた勇者というのは。だがそれも、ここで終わりだ！ここのブロックのボスである私が自ら貴様の首を上げてやるわっ！覚悟しろっ！」
>
EN: The Golden Knight says "You are a brave man beating the bosses of the first and second areas, and ascending the tower. But the game is over now. Here and Now, I will beat you for myself! Give up!"

**[28]** 　代码 `strNumber=28` ← eventMT 　·  出现层：—

> 金騎士「ううう……今回はこのぐらいにしておいてやる……４０階まで登ってこれたら今度は本気で相手をしてやるからなっ！覚えておけっ！」"
>
EN: The Golden Knight says "You think you're pretty strong, huh? If you can make it to the 40th floor, I shall fight with you again. There, you will die!

**[31]** 　代码 `strNumber=31` ← eventMT 　·  出现层：—

> 金騎士「よくきたな。今度はさっきの様な訳にはいかんぞ！この屈辱は１０倍にして返してくれるわっ！死霊兵士突撃！」
>
EN: The Golden Knight says "I wonder how you were able to come so far. I will make sure you go no further. I will humiliate you 10 times as much as you've disgraced this tower. Ghost Soldiers, charge!"

**[32]** 　代码 `strNumber=32` ← eventMT 　·  出现层：—

> 金騎士「ふふん、こんなのは小手調べだっ！兵士突撃！」
>
EN: The Golden Knight says "Humph, that was nothing! Soldiers, charge!"

**[33]** 　代码 `strNumber=33` ← eventMT 　·  出现层：—

> 金騎士「まだまだ、これからっ！剣士突撃！」
>
EN: The Golden Knight says "We are only beginning. Let's fight from now on. Swordsmen, charge!"

**[34]** 　代码 `strNumber=34` ← eventMT 　·  出现层：—

> 金騎士「うぬぬ……だが、これはどうだっ！騎士突撃！」
>
EN: The Golden Knight says "Heck! How about this attack? Knights, charge!"

**[35]** 　代码 `strNumber=35` ← eventMT 　·  出现层：—

> 金騎士「うう……私の部下達を……許さんっ！許さんぞ！今度は手加減はしてやらんっ！覚悟しろ！」
>
EN: The Golden Knight says "How dare you defeat my followers? Never shall I forgive you! Now I won't use discretion. Give up!"

**[36]** 　代码 `strNumber=36` ← eventMT 　·  出现层：—

> 金騎士「ごほっ……今回はこのへんで……はあはあ……許しておいてやる……。だが次にやる時は今度こそ本当に本気で相手をしてやるからなっ！覚悟しておけっ！」
>
EN: The Golden Knight says "I will unwillingly forgive you this time. But we shall quarrel seriously when we meet again. You had better give up!"

**[37]** 　代码 `strNumber=37` ← eventMT 　·  出现层：—

> 金騎士「あっ……！ゼノ様……。あと一歩という所で、勇者を取り逃がしてしまいました。どうか、お許しを……。」
>
EN: The Golden Knight says "Oh! Sir Magic Serg. Zeno. I was not able to catch the brave man. Please forgive me."

**[38]** 　代码 `strNumber=38` ← eventMT 　·  出现层：—

> 魔導師ゼノ「取り逃がしただと……？逃げてきたのは貴様の方ではないかっ！この恥知らずめがっ！貴様のような臆病者はこの塔には不要だっ！ここで、死ねっ！」
>
EN: The Magic Serg. Zeno replies "You weren't? I dare you to say that again. You come running up here like a coward and tell me you couldn't do your job. What shame! This tower has no need for the likes of you! You've failed me for the last time. You shall now die."

**[39]** 　代码 `strNumber=39` ← eventMT 　·  出现层：—

> 金騎士「ああ、どうか、お許し……ぎゃあ～～～っ！！！」
>
EN: The Golden Knight says "Oh God, please forgive me! Ah!"

**[40]** 　代码 `strNumber=40` ← eventMT 　·  出现层：—

> 魔導師ゼノ「お見苦しいところをお見せしたな……。だが、安心してもらおう。私はこのようなゴミとはわけが違う。もし、お前が上まで登ってこれたなら今度は、私が直々にお相手しよう。待っているぞ……。」
>
EN: The Magic Serg. Zeno says "I behaved unbecomingly. But don't worry. I quite different from such a fellow. If you should come up to me, I would fight with you directly. I'm waiting for you."

**[41]** 　代码 `strNumber=41` ← eventMT 　·  出现层：—

> 魔導師ゼノ「よくぞ、ここまで、たどりついたものだ。誉めてやろう。約束どおり、この私が直々に相手をしよう。さあ、来るがいい。」
>
EN: The Magic Serg. Zeno "It's amazing that you found your way here at last. I compliment you. Now, as promised, I'll fight with you, man to man!"

**[42]** 　代码 `strNumber=42` ← eventMT 　·  出现层：—

> 魔導師ゼノ「うっ……この陣形は……まずいっ！」
>
EN: The Magic Serg. Zeno "Alas..."

**[43]** 　代码 `strNumber=43` ← eventMT 　·  出现层：—

> 勇者「おまえはっ……！どうしてこんな所に！」
>
EN: The brave man says "Who? It's you! Why are you in such a place ?"

**[45]** 　代码 `strNumber=45` ← eventMT 　·  出现层：—

> 勇者「あっ！おまえはゼノッ！生きていたのか！？」
>
EN: The brave man says "Huh? Hey! You're Zeno! Were you still alive ?"

**[46]** 　代码 `strNumber=46` ← eventMT 　·  出现层：—

> 魔導師ゼノ「あんなことで倒されるものか。あれは、おまえの戦士としての知性を試したにすぎん。」
>
EN: The Magic Serg. Zeno says "I will never die. I merely tested your intelligence as a soldier."

**[47]** 　代码 `strNumber=47` ← eventMT 　·  出现层：—

> 勇者「なにっ！？……どういうことだっ！どうして、こんな事を……！？」
>
EN: The brave man says "Huh? What do you mean? Why did you do such a thing ?"

**[48]** 　代码 `strNumber=48` ← eventMT 　·  出现层：—

> 魔導師ゼノ「おまえの持つ神剣ウェポナー、そして私の持つ全能の杖インテリオン。この２つの力が合わさる時、偉大なる知恵を手に入れる事ができるという……。しかし、それには、その剣の力を十分に発揮できる能力を持った戦士が必要となるのだ。」
>
EN: The Magic Serg. Zeno says "The Sacred Sword 'Weaponer' which you have and The Omniscient Staff 'Intellion' which I have, Legend says that whoever unites the two will recieve great wisdom. But to this end, it must be assured that the soldier who does so can handle the the power of that sword."

**[49]** 　代码 `strNumber=49` ← eventMT 　·  出现层：—

> 勇者「その戦士が俺だというのか……！？」
>
EN: The brave man says "What are you saying... Am I the soldier ?"

**[50]** 　代码 `strNumber=50` ← eventMT 　·  出现层：—

> 魔導師ゼノ「そうだ……しかし、おまえの技量はその神剣ウェポナーを使いこなすには十分ではなかった。だから、私は偽りの情報を流し、様々なワナをこの塔にしかけ、おまえが来るのを待っていたのだ。そして、予定通り、おまえは神剣を扱うのに十分な力を身につけてここまで来た。」
>
EN: The Magic Serg. Zeno says "Yes. But when you came here, your ability wasn't sufficient to master the sacred sword 'Weaponer'."For that reason, I gave false information, set various traps in this tower, and waited for you to come. You came to here master the power enough to using the sacred sword as arranged beforehand.

**[51]** 　代码 `strNumber=51` ← eventMT 　·  出现层：—

> 勇者「では、姫がさらわれたという情報も、俺をここまで、おびき寄せる為のワナだったというのかっ！？」
>
EN: The brave man replies "Well, this means that the rumour that a princess was trapped here... was actually a lie in order to get me here, wasn't it ?"

**[52]** 　代码 `strNumber=52` ← eventMT 　·  出现层：—

> 魔導師ゼノ「その通りだ。そして、後は私がおまえの力を取りこめば、この茶番劇も終わりとなる……。時は来たれり……我全能なる力を用いて、神剣を砕き偉大なる知恵を手に入れん……。ゆくぞっ！神剣の戦士よ！」
>
EN: The Magic Serg. Zeno says "Yes, that's right. And now, if we can work together, this farce will end. Now is the time to act. Using omniscient power, We shall break the sacred sword and recieve great enlightenment. Soldier of the Sacred Sword! Let's finish this!"

**[54]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 魔導師ゼノ「ゴホッ！おのれ、この私が倒されるとは……、しかしこれぐらいで死ぬような私ではない！おぬしともう一度、戦う日が来ることを楽しみに待っているぞ！」
>
EN: The Magic Serg. Zeno says "You villain. Little did I expect to be beaten. But I would never die in such a way. I'll be looking forward to fighting with you again."

**[222]** 　代码 `strNumber=222` ← eventMT 　·  出现层：—

> 勇者「なんだと～！」
>
EN: The brave man says "What?"

**[223]** 　代码 `strNumber=223` ← eventMT 　·  出现层：—

> 勇者「あ～っ」
>
EN: The brave man says "Hey!"

### 无名提示与谜面（石板/老人语气，未具名）（35 条）

**[2]** 　代码 `strNumber=2` ← eventMT 　·  出现层：—

> 「・・・・・おい・・・」
>
EN: "------ Hey!"

**[3]** 　代码 `strNumber=3` ← eventMT 　·  出现层：—

> 「・・・・・おいっ！起きろ！」
>
EN: "------ Hey! Wake up!"

**[18]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 「お金が足りないよ！」
>
EN: "You don't have enough money."

**[22]** 　代码 `strNumber=22` ← eventMT 　·  出现层：—

> 「・・・ジ・・・トキハキタレリ・・・エラバレシモノヨ、シヲオソレヌナラバジクウノモンヲクグリテ、ワガモトヘクルガヨイ・・・」
>
EN: "Now is the time. You were chosen. If you aren't afraid of Death, you should go through the gate of Time and Space, and come to me."

**[53]** 　obj138（数据引用） 　·  出现层：23

> 「わしが言うことは何もない。この階に、あるメッセージが隠されているじゃろう。」
>
EN: "I have nothing to say. A certain message may be hidden in this room."

**[55]** 　obj175（数据引用） 　·  出现层：4

> 「この塔には鍵で開けられる扉のほかに ”門” というものがあって、これはその門を守っているモンスターを倒さなければあかないじゃろう。」
>
EN: "There are doors which cannot be openned by a key. You can open these doors by beating the monsters which guard them."

**[56]** 　obj42（数据引用） 　·  出现层：6 catalog

> 「商人から物を買うと、あとで重要な情報を聞くことができるじゃろう。」
>
EN: "If you buy goods from merchants, you will be able to hear important information later."

**[61]** 　obj43（数据引用） 　·  出现层：16 catalog

> 「このブロックでは赤い鍵は２ヶ所で手に入るそうじゃ。」
>
EN: "I heard that you can find a red key at two places in this area."

**[62]** 　obj139（数据引用） 　·  出现层：18

> 「このブロックでは、祭壇で攻撃力を何回か上げてもらわないとロックというモンスターが倒せなくなってしまうかもしれん。注意するのじゃ。」
>
EN: "In this area, if you don't raise your offensive power at an altar a few times, you may not be able to beat 'Rock' monsters. Be careful!"

**[64]** 　obj141（数据引用） 　·  出现层：27

> 「この階まで来た段階で、生命力１５００、攻撃力８０、防御力９８、鍵５個、紫の鍵が１個あれば、ほぼ理想的と言えるじゃろう。」
>
EN: "In the stage of this floor, if your strength is 1500, offensive power is 80, defensive power is 98, you have five keys, and one blue key, you are almost ideal."

**[65]** 　obj142（数据引用） 　·  出现层：31

> 「二刀流の剣士は攻撃力がものすごく高い。まともに戦えば大きなダメージを受けるだろう。一撃で倒せるようになるまで、戦わない方がよかろう。」
>
EN: "The offensive power of the swordsman who uses two swords is too high. He can use two swords at the same time. You will lose much strength if you fight him normally. You should never fight him before your attacks are stronger than his."

**[66]** 　obj163（数据引用） 　·  出现层：—

> 「この塔は５０階建てだが、実際には４９階までしか行けないようだ。」
>
EN: "This tower is 50 stories high, but in reality it seems that you cannot go up to the 50th floor."

**[67]** 　obj143（数据引用） 　·  出现层：33

> 「急がば回れじゃ。」
>
EN: "More haste, less speed."

**[69]** 　obj145（数据引用） 　·  出现层：37

> 「この階の宝物庫にある宝を取るためにはマトックが必要じゃ。」
>
EN: "You need the mattock in order to get the treasure which is in the item warehouse on this floor."

**[71]** 　obj146（数据引用） 　·  出现层：39

> 「３時になれば空間移動の秘宝が現れるじゃろう。」
>
EN: "At three o'clock, the secret treasure that lets one travel in space will appear."

**[72]** 　obj167（数据引用） 　·  出现层：—

> 「この塔のどこかに、幸運の金貨というものがあって、それを持っていると敵を倒したときに得られるお金が２倍になるそうだ。」
>
EN: "There is a Lucky Gold somewhere in this tower. If you have it, you can get twice as much money when you beat an enemy."

**[73]** 　obj147（数据引用） 　·  出现层：42

> 「魔術師は隣接すると魔法攻撃をしてくる。魔導師ははさまれると生命力を半分にする攻撃をしてくる。魔導師のはさみ攻撃は自分の生命力が高いほど受けるダメージが大きいはずじゃから気をつけてな。」
>
EN: "A Magician will attack using magic when he is next to you. The Magic Sergeants will attack and divide the vital power in half when you are caught between two. As for an attack on both sides from the Magic Sergeant, the stronger you are, the more damage you take. So, please be careful."

**[75]** 　obj169（数据引用） 　·  出现层：—

> 「神盾は、魔法使いたちの魔法攻撃を防ぐ力があるらしい。……しかし、この盾は幻の階に隠されているそうだ。」
>
EN: "The sacred shield can defend you against magic attacks. But I heard this shield is hidden on a floor that doesn't exist."

**[76]** 　obj149（数据引用） 　·  出现层：46

> 「４１階は完全に左右対称になっておる。だから……。」
>
EN: "The 41st floor is perfectly symmetrical, and therefore,"

**[78]** 　obj150（数据引用） 　·  出现层：48

> 「サイコロの５の目の形には、魔を封じ込める力があるという。このブロックのボスと戦う時には、このことを頭にいれておきなされ。」
>
EN: "It is said that the symbol of 5 on a pair of dice has the force of sealing magic. You had better memorize it till you fight the boss of this area."

**[79]** 　obj151（数据引用） 　·  出现层：—

> 「もう、話は終わりじゃ。」
>
EN: "I have done what I can. Good luck!"

**[80]** 　obj152（数据引用） 　·  出现层：2

> 「おお、助けてくれてありがとうよ。お礼に、そなたの攻撃力と防御力を３％だけあげてやろう」（攻撃力と防御力が上がった!）
>
EN: "Oh, thank you for your help. I will raise your offensive and defensive power 3 percent as a token of my gratitude. [You begin feeling stronger]"

**[81]** 　obj153（数据引用） 　·  出现层：3

> 「おぬしにこの勇者のオーブをさずけよう。これを持っていれば今いる階のモンスターの能力を調べてダメージを予測してくれるじゃろう。有効に使うのじゃ」
>
EN: "I will grant you the orb of the hero. It will forecast the results of fighting monsters on the current floor. Use it often."

**[82]** 　obj154（数据引用） 　·  出现层：—

> 「やれやれ、見つかってしもうたか。褒美におぬしに”エリクサー”をやろう。この薬を使えば、その時の攻撃力と防御力に応じた値だけ生命力が回復するじゃろう。じゃから、当然、後の方で使う方が効果は大きいぞ。」
>
EN: "Thank goodness, you found me. I will give you an elixir as a symbol of my gratitude. Using this medicine will cause you to gain life according to your offensive and defensive power. So naturally, the later you use, the more it will have an effect on you."

**[83]** 　obj172（数据引用） 　·  出现层：—

> 「もう、話す事はないよ。」
>
EN: "Be careful. I have nothing more to say."

**[84]** 　obj173（数据引用） 　·  出现层：—

> 「有効に使ってね!」
>
EN: "Please, use it wisely."

**[85]** 　obj174（数据引用） 　·  出现层：2

> 「やあ、助けてくれてありがとう。少ないけれど、お礼にとっておいてくれ！」（１０００ＧＯＬＤもらった!）
>
EN: "Thank you for your help. Please accept money as a small token of my gratitude. (Got 1000 Gold.)"

**[91]** 　obj161（数据引用） 　·  出现层：28

> 「鍵１個を１００ＧＯＬＤで買うよ。鍵を売るかい？」
>
EN: "I will buy your keys at 100 Gold a piece. Will you sell me keys?"

**[98]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 「まいどーっ！」
>
EN: "Thank you very much."

**[208]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 「どの望みをかなえて欲しいのだ？」
>
EN: "What option shall you choose?"

**[215]** 　代码 `strNumber=215` ← saidan 　·  出现层：—

> 「金がたらん！」
>
EN: "You don't have enough money!"

**[266]** 　代码 `strNumber=266` ← eventMT 　·  出现层：—

> 「・・・」
>
EN: "------"

**[280]** 　代码 `strNumber=280` ← eventMT 　·  出现层：—

> 「生命力がなくなりました。再挑戦してください。」
>
EN: "You have perished in Magic Tower. Please try again!"

**[283]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 「願いをかなえたぞ！」
>
EN: "Your wish came true."

**[296]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 「遊んでくれてありがとう！　まだ完成できていません。　楽しみに待っていてね！」
>
EN: "Thank you for playing this game. Please wait for completing."

### 道具 / 装备 / 钥匙：拾取与使用（51 条）

**[60]** 　obj160（数据引用） 　·  出现层：—

> 「十字架を持っていれば、ゾンビやバンパイアに対する攻撃力が２倍になる。特にバンパイアは十字架を持っていないと倒せないだろう。これより上の階のどこかにあるらしいが……。」
>
EN: "If you carry a cross, the strength of Zombies and Vampires will be cut in half. It is near impossible to defeat them without a cross, especially Vampires. A cross is on a floor higher than this one."

**[133]** 　obj1（数据引用） 　·  出现层：1-9,11-12,14-20,31-34,36-43,45,47 catalog stage_flags

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** 　obj3（数据引用） 　·  出现层：3-4,8,12,14-16,18-19,31-32,37,41-43,47 catalog

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[135]** 　obj28（数据引用） 　·  出现层：8,37,42 catalog

> 赤色の扉の鍵を手に入れた。
>
EN: Got a red key.

**[142]** 　obj24（数据引用） 　·  出现层：catalog

> 勇者のオーブを手に入れた！
>
EN: Got the orb of the hero.

**[147]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 扉の鍵がない！
>
EN: Don't have the key.

**[148]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 青色の鍵がない！
>
EN: Don't have the blue key.

**[149]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 赤色の鍵がない！
>
EN: Don't have the red key.

**[151]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 飛翔のオーブは階段のとなりでなくては使えない！
>
EN: You must be near the stairs to use the orb of flying!

**[152]** 　obj26（数据引用） 　·  出现层：1 catalog

> 飛翔のオーブを手に入れた！
>
EN: Got the orb of flying.

**[153]** 　obj25（数据引用） 　·  出现层：5 catalog

> 知恵のオーブを手に入れた！
>
EN: Got the orb of wisdom.

**[156]** 　obj30（数据引用） 　·  出现层：5 catalog

> 鉄の剣を手に入れた。攻撃力が１０ポイントアップ！
>
EN: Got an Iron Sword! Your offensive power was 10 points up!

**[157]** 　obj31（数据引用） 　·  出现层：17 catalog

> 銀の剣を手に入れた。攻撃力が２０ポイントアップ！
>
EN: Got a Silver Sword! Your offensive power was 20 points up!

**[158]** 　obj32（数据引用） 　·  出现层：33 catalog

> 騎士の剣を手に入れた。攻撃力が４０ポイントアップ！
>
EN: Got a Sword of Knight! Your offensive power was 40 points up!

**[159]** 　obj33（数据引用） 　·  出现层：48 catalog

> 聖　剣を手に入れた。攻撃力が５０ポイントアップ！
>
EN: Got a Holy Sword! Your offensive power was 50 points up!

**[160]** 　obj34（数据引用） 　·  出现层：13 catalog stage_flags

> 神　剣を手に入れた。攻撃力が１００ポイントアップ！
>
EN: Got a Sacred Sword! Your offensive power was 100 points up!

**[161]** 　obj35（数据引用） 　·  出现层：9 catalog

> 鉄の盾を手に入れた。防御力が１０ポイントアップ！
>
EN: Got an Iron Shield! Your defensive power was 10 points up!

**[162]** 　obj36（数据引用） 　·  出现层：11 catalog

> 銀の盾を手に入れた。防御力が２０ポイントアップ！
>
EN: Got a Silver Shield! Your defensive power was 20 points up!

**[163]** 　obj37（数据引用） 　·  出现层：38 catalog

> 騎士の盾を手に入れた。防御力４０がポイントアップ！
>
EN: Got a Shield of Knight! Your defensive power was 40 points up!

**[164]** 　obj38（数据引用） 　·  出现层：43 catalog

> 聖　盾を手に入れた。防御力が５０ポイントアップ！
>
EN: Got a Holy Shield! Your defensive power was 50 points up!

**[165]** 　obj39（数据引用） 　·  出现层：44 catalog stage_flags

> 神　盾を手に入れた。防御力が１００ポイントアップ！
>
EN: Got a Sacred Shield! Your defensive power was 100 points up!

**[166]** 　obj11（数据引用） 　·  出现层：1,3-9,20 catalog stage_flags

> 赤い回復薬を手に入れた。生命力が５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 50 points up!

**[167]** 　obj12（数据引用） 　·  出现层：1-4,7-8,10 catalog

> 青い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 200 points up!

**[168]** 　obj13（数据引用） 　·  出现层：1,3-4,7-10 catalog

> 赤のクリスタルを手に入れた。攻撃力が１ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 1 point up!

**[169]** 　obj14（数据引用） 　·  出现层：1,3,5-6,8-10 catalog

> 青のクリスタルを手に入れた。防御力が１ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 1 point up!

**[171]** 　obj103（数据引用） 　·  出现层：catalog

> 十字架を手に入れた！バンパイア、ゾンビに対する攻撃力が２倍になった！
>
EN: Got a cross! Your offensive power against Vampires and Zombies has doubled.

**[172]** 　obj104（数据引用） 　·  出现层：catalog

> エリクサーを手に入れた！
>
EN: Recieved the Magic Elixir.

**[173]** 　obj114（数据引用） 　·  出现层：catalog

> マトックを手に入れた！
>
EN: Got the Magic Mattock.

**[174]** 　obj105（数据引用） 　·  出现层：37 catalog

> 破壊の玉を手に入れた！
>
EN: Got the Destructible Ball!

**[175]** 　obj106（数据引用） 　·  出现层：catalog

> 空間転移の秘宝を手に入れた！
>
EN: Got the Warp Staff!

**[176]** 　obj107（数据引用） 　·  出现层：45 catalog

> 昇華の翼を手に入れた！
>
EN: Got wings to fly up!

**[177]** 　obj108（数据引用） 　·  出现层：catalog

> 降臨の翼を手に入れた！
>
EN: Got wings to fly down!

**[178]** 　obj109（数据引用） 　·  出现层：catalog

> ドラゴンスレーヤーを手に入れた！ドラゴンに対する攻撃力が２倍になった！
>
EN: Got the Dragon Slayer! Your attack power against the Dragon has doubled!

**[179]** 　obj110（数据引用） 　·  出现层：catalog

> 雪の結晶を手に入れた！
>
EN: Got the snow crystal!

**[180]** 　obj111（数据引用） 　·  出现层：46 catalog

> 魔法の鍵を手に入れた！
>
EN: Got the magic key!

**[181]** 　obj112（数据引用） 　·  出现层：catalog

> スーパーマトックを手に入れた！
>
EN: Got the Super Magic Mattock!

**[182]** 　obj113（数据引用） 　·  出现层：00F catalog

> 幸運の金貨を手に入れた！敵が持っているＧＯＬＤ数が２倍になる。
>
EN: Got the Lucky Gold! You can get twice gold which monster has from now.

**[205]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 枚手に入れた！
>
EN: Gold.

**[252]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 鍵を持ってないよ！
>
EN: You don't have a key!

**[254]** 　obj66（数据引用） 　·  出现层：11-12,14,16-19 catalog

> 赤い回復薬を手に入れた。生命力が１００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 100 points up!

**[255]** 　obj67（数据引用） 　·  出现层：31,33-34,37-40 catalog

> 赤い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 200 points up!

**[256]** 　obj68（数据引用） 　·  出现层：41,43-44,46-48 catalog

> 赤い回復薬を手に入れた。生命力が２５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 250 points up!

**[257]** 　obj76（数据引用） 　·  出现层：11-12,15,17,20 catalog

> 青い回復薬を手に入れた。生命力が４００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 400 points up!

**[258]** 　obj77（数据引用） 　·  出现层：31-34,36-38,40 catalog

> 青い回復薬を手に入れた。生命力が８００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 800 points up!

**[259]** 　obj78（数据引用） 　·  出现层：41-43,45,48 catalog

> 青い回復薬を手に入れた。生命力が１０００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 1000 points up!

**[260]** 　obj80（数据引用） 　·  出现层：11-12,16-20 catalog

> 赤のクリスタルを手に入れた。攻撃力が２ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 2 points up!

**[261]** 　obj81（数据引用） 　·  出现层：31-32,34,37,39-40 catalog

> 赤のクリスタルを手に入れた。攻撃力が４ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 4 points up!

**[262]** 　obj82（数据引用） 　·  出现层：41,45-48 catalog

> 赤のクリスタルを手に入れた。攻撃力が５ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 5 points up!

**[263]** 　obj83（数据引用） 　·  出现层：12,14-18,20 catalog

> 青のクリスタルを手に入れた。防御力が２ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 2 points up!

**[264]** 　obj84（数据引用） 　·  出现层：31-32,34,37-40 catalog

> 青のクリスタルを手に入れた。防御力が４ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 4 points up!

**[265]** 　obj85（数据引用） 　·  出现层：41-42,45,47-48 catalog

> 青のクリスタルを手に入れた。防御力が５ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 5 points up!

### 商人 · 祭坛 · 积分石 · 智慧之戒问答（16 条）

**[86]** 　obj18（数据引用） 　·  出现层：6 catalog

> 「紫の鍵を大特価の５０ＧＯＬＤで売るよ! 買わないかい?」
>
EN: "I will sell a blue key at very special price (50 gold)! Will you buy it?"

**[87]** 　obj41（数据引用） 　·  出现层：7 catalog

> 「鍵を５個セットで５０ＧＯＬＤで売るよ! 買わないかい?」
>
EN: "I will sell five keys for 50 Gold! Will you buy them?"

**[88]** 　obj156（数据引用） 　·  出现层：12

> 「希少品の赤い鍵を８００ＧＯＬＤで売るよ！買わないかい？」
>
EN: "I will sell the rare red key for 800 Gold! Will you buy it?"

**[89]** 　obj17（数据引用） 　·  出现层：catalog

> 「うちの店は鍵をいくらでも売るよ。１つ１０００ＧＯＬＤだが買うかい？」
>
EN: "My store will sell as many keys as you need. They are 1000 Gold each. Will you buy them?"

**[90]** 　obj159（数据引用） 　·  出现层：15

> 「紫の鍵を２００ＧＯＬＤで売るよ！買わないかい？」
>
EN: "I will sell a blue key for 200 Gold! Will you buy it?"

**[92]** 　obj162（数据引用） 　·  出现层：31

> 「鍵を４個と紫の鍵をセットにして１０００ＧＯＬＤだ！買うかい？」
>
EN: "I will sell four keys and a blue key for 1000 Gold! Will you buy them?"

**[93]** 　obj164（数据引用） 　·  出现层：38

> 「鍵３個を大サービスの２００ＧＯＬＤで売るよ！早い者勝ちだよ！」
>
EN: "I will sell three keys at special price (200 gold). First come, first served."

**[94]** 　obj166（数据引用） 　·  出现层：39

> 「紫の鍵が３個で２０００ＧＯＬＤだが、買うかい？」
>
EN: "2000 Golds for three blue keys. Deal?"

**[95]** 　obj168（数据引用） 　·  出现层：45

> 「１０００ＧＯＬＤで生命力を２０００ポイント回復してあげるよ。」
>
EN: "I will increase your life 2000 points at 1000 Gold."

**[96]** 　obj170（数据引用） 　·  出现层：47

> 「超希少品のスーパーマトックを４０００ＧＯＬＤで買わないかい？」
>
EN: "Would you like to buy a super mattock (it's very rare) for 4000 Gold?"

**[204]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ＧＯＬＤを
>
EN: . Recieved

**[206]** 　obj22（数据引用） 　·  出现层：4,12,32,46 catalog

> 「この祭壇に
>
EN: "If you offer me

**[210]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ポイント回復
>
EN: points.

**[224]** 　obj69（数据引用） 　·  出现层：catalog

> 「この階までのあなたの生命力、防御力、攻撃力、鍵の個数からあなたの実力を評価すると・・・
>
EN: "Judging by your vital power, offensive power, defensive power, and number of keys, you have

**[297]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ポイント回復
>
EN: points up!

**[298]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ＧＯＬＤを
>
EN: Got

### 地形与调查提示（门、楼梯、暗墙、熔岩、人物）（17 条）

**[63]** 　obj140（数据引用） 　·  出现层：21

> 「このブロックに、この魔法の塔の主である大魔導師がいるが、今のおまえさんでは戦っても死にに行くようなものじゃろう。とりあえず、うまくやりすごして上のブロックに行くのが正解じゃ。」
>
EN: "The Great Magic Master is in this area. He is a proprietor of this magic tower. At your strenght, to attack him means death. It stands to reason that you should not face him, but rather, get items on higher levels first."

**[70]** 　obj165（数据引用） 　·  出现层：—

> 「門番のいる所には必ず門があるよ。逆に門のある階には、それを守っている敵がいるよ。だから……。」
>
EN: "There is never a gate without a Gate-Keeper. Conversely there are always enemies who keep the gate on floors that have gates. So,"

**[136]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 扉が開いた。
>
EN: The door has opened.

**[137]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 青色の扉が開いた。
>
EN: The blue door has opened.

**[138]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 赤色の扉が開いた。
>
EN: The red door has opened.

**[139]** 　地形4、地形6、地形8 等47项（数据引用） 　·  出现层：1-9,11-19,21-29,31-39,41-48 00F

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 　地形5、地形7、地形9 等46项（数据引用） 　·  出现层：2-43,45-49

> 階段を下った。
>
EN: Went down the stairs.

**[141]** 　obj89（数据引用） 　·  出现层：5,9,12,14,16,19,35-36,41 catalog

> 壁がくずれた！
>
EN: The wall collapsed!

**[143]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 老人がいる。
>
EN: You see an old man.

**[144]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 商人がいる。
>
EN: You see a merchant.

**[145]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 妖精がいる。
>
EN: You see a fairy.

**[146]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 盗賊がいる。
>
EN: You see a thief.

**[150]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 階段がある。
>
EN: You see stairs.

**[183]** 　obj79（数据引用） 　·  出现层：13,26 catalog

> 溶岩が流れている。
>
EN: The lava is really hot.

**[202]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 溶岩が固まって道ができた！
>
EN: The lava cooled and turned to stone.

**[245]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 道が壁に変わった！
>
EN: The road changed to the wall!

**[267]** 　地形116、地形117（数据引用） 　·  出现层：—

> 0
>
EN: 0

### 界面 · 系统文案（状态窗、情報、音、得分、称号）（26 条）

**[58]** 　obj155（数据引用） 　·  出现层：—

> 「祭壇に寄進したときは、攻撃力よりも防御力を主に上げてもらった方がいいでしょう。ただし、攻撃力をまったく上げないと、あとで倒せない敵がでてくるかもしれないよ。」
>
EN: "When you offer gold at an alter, you may as well have your defensive power risen rather than your offensive power. The enemy whom you cannot beat may appear, provided you won't raise your offensive power."

**[77]** 　obj171（数据引用） 　·  出现层：—

> 「ドラゴンを倒す気なら、聖剣と聖盾、それにドラゴンスレーヤーを持って、なおかつレベルが高くなければならないだろう。」
>
EN: "If you want to beat the Dragon, you must have a holy sword, a holy shield, and a Dragon slayer, and also you must be high level."

**[185]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 命
>
EN: Vital power:

**[186]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 攻
>
EN: Offensive power:

**[187]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 防
>
EN: Defensive power:

**[188]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 予想ダメージ
>
EN: Expected damage:

**[189]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 攻撃不可能
>
EN: Attack is impossible!

**[207]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ＧＯＬＤ寄進すれば望みをかなえてやろう。寄進するか？」
>
EN: Gold, I will grant your request. Will you?"

**[209]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ・生命力を
>
EN: Your life recovers by

**[211]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ・攻撃力を
>
EN: The offensive power is raised

**[212]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ポイントアップ
>
EN: points.

**[213]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ・防御力を
>
EN: The defensive power is raised

**[216]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 塔
>
EN: Tower

**[217]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 階
>
EN: F

**[218]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 生命力
>
EN: Life

**[219]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 攻撃力
>
EN: Offense

**[220]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 防御力
>
EN: Defense

**[225]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 点です。
>
EN: points.

**[233]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 『戦士』
>
EN: FIGHTER

**[234]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 『勇者』
>
EN: BRAVE MAN

**[235]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 『英雄』
>
EN: HERO

**[236]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 『剣帝』
>
EN: SWORD EMPEROR

**[237]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> 『闘神』
>
EN: FIGHTER GOD

**[238]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> の称号を差し上げましょう。
>
EN: .

**[239]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> これから先もこの調子でね。」
>
EN: You may as well play as good as you have from this point on."

**[240]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> ここまでおつかれさまでした。」
>
EN: It was nice fight so far."

### 其它未归类文案（1 条）

**[232]** 　运行时按计算下标引用（未在静态数据/常量赋值中定位） 　·  出现层：—

> あなたには
>
EN: I give you the special rank of
