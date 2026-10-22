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
├── magic_tower1_rows.csv        # 大表逐行标记（S 暗墙 / T 隐形块 / E 实体 / B BOSS）
├── magic_tower1_walkroute.md    # 走法路线、危险格、00 层通达方式、隐藏物体说明
├── hidden_floor_band5.png / floor_00.png / MTower_sheet.gif
└── README.md
```

## 怪物战力表

数据源：`magic_tower1_monsters.csv`（战力四维） + `magic_tower1_entities.csv`（布点）。
「只数 / 出现层」只统计常规楼层（1–50F 与 00F），图鉴块 `catalog` 与变量块 `stage_flags` 里的重复登记已剔除。

| id | 怪物 | HP | ATK | DEF | GOLD | 只数 | 出现层 |
|---:|---|---:|---:|---:|---:|---:|---|
| 5 | Green Slime | 35 | 18 | 1 | 1 | 27 | 1,3-9,30,34 |
| 7 | Bat | 35 | 38 | 3 | 3 | 31 | 1,3-9,11-12,15,19-20,34 |
| 6 | Red Slime | 45 | 20 | 2 | 2 | 22 | 1,3-9,30,34,46 |
| 9 | Skeleton C | 50 | 42 | 6 | 6 | 23 | 1,3-4,6-10,46 |
| 10 | Skeleton B | 55 | 52 | 12 | 8 | 16 | 1,4-10 |
| 8 | Priest | 60 | 32 | 8 | 5 | 17 | 1,3-10 |
| 15 | Gate-Keeper B | 100 | 180 | 110 | 100 | 6 | 2,32,38 |
| 29 | Gate-Keeper C | 50 | 48 | 22 | 12 | 6 | 8,17 |
| 16 | Skeleton A | 100 | 65 | 15 | 30 | 1 | 10 |
| 47 | Big Bat | 60 | 100 | 8 | 12 | 40 | 11-12,14-20,46 |
| 46 | Superion Priest | 100 | 95 | 30 | 22 | 20 | 11-12,14-20 |
| 45 | Big Slime | 130 | 60 | 3 | 8 | 27 | 11-12,14-19,30,34 |
| 48 | Zombie | 260 | 85 | 5 | 18 | 19 | 11-12,14-19,38,46 |
| 56 | Rock | 20 | 100 | 68 | 28 | 9 | 14,16,18-20 |
| 49 | Zombie Knight | 320 | 120 | 15 | 30 | 23 | 14-19,31,33,36 |
| 50 | some of Giant Octopus | 1200 | 180 | 20 | 50 | 1 | 15 |
| 51 | some of Giant Octopus | 1200 | 180 | 20 | 50 | 1 | 15 |
| 52 | some of Giant Octopus | 1200 | 180 | 20 | 50 | 1 | 15 |
| 60 | some of Giant Octopus | 1200 | 180 | 20 | 50 | 1 | 15 |
| 61 | some of Giant Octopus | 1200 | 180 | 20 | 50 | 1 | 15 |
| 62 | some of Giant Octopus | 1200 | 180 | 20 | 50 | 1 | 15 |
| 70 | some of Giant Octopus | 1200 | 180 | 20 | 50 | 1 | 15 |
| 71 | Giant Octopus | 1200 | 180 | 20 | 100 | 1 | 15 |
| 72 | some of Giant Octopus | 1200 | 180 | 20 | 50 | 1 | 15 |
| 95 | Slime Man | 320 | 140 | 20 | 30 | 23 | 16,31-34,36-40 |
| 96 | Great Magic Master | 4500 | 560 | 310 | 1000 | 1 | 25 |
| 92 | Swordsman | 100 | 680 | 50 | 55 | 16 | 31,33-34,36-40,46 |
| 91 | Knight | 160 | 230 | 105 | 65 | 19 | 31-32,34,36-40,46 |
| 93 | Soldier | 210 | 200 | 65 | 45 | 23 | 31-34,36-40,46 |
| 94 | Ghost Soldier | 220 | 180 | 30 | 35 | 25 | 31-34,36-40 |
| 74 | Dragon | 1500 | 600 | 250 | 800 | 1 | 35 |
| 90 | Golden Knight | 120 | 150 | 50 | 100 | 1 | 40 |
| 97 | Vampire Bat | 200 | 390 | 90 | 50 | 14 | 41-43,45-48 |
| 99 | Magician A | 200 | 380 | 130 | 90 | 14 | 41-43,45-49 |
| 100 | Magician B | 220 | 370 | 110 | 80 | 16 | 41-43,45-48 |
| 58 | Magic Sergeant | 230 | 450 | 100 | 100 | 11 | 41-43,45,48 |
| 98 | SlimeLord | 360 | 310 | 20 | 40 | 13 | 41-43,45-48 |
| 101 | Dark Knight | 180 | 430 | 210 | 120 | 11 | 42-43,45,48-49 |
| 102 | Gate-Keeper A | 180 | 460 | 360 | 200 | 2 | 44 |
| 59 | Vampire（仅图鉴，关卡无布点） | 444 | 199 | 66 | 144 | 0 | — |
| 57 | Magic Serg（仅图鉴，关卡无布点） | 8000 | 5000 | 1000 | 500 | 0 | — |


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

- **id 71 大ダコ 不是一只怪，而是一只 9 格的怪**：15F 的大乌贼由中央 `71` + 八块躯体
  `50/51/52/60/61/62/70/72` 组成，**九格全部是独立战斗单位**（均 1200/180/20，躯体各给 50 GOLD、中央给 100），
  所以表里 9 行同值、各 1 只，合计一只。
- **id 74 ドラゴン 的九宫格不同**：35F 的中央可战斗格是 `(x=6, y=7)`，1500/600/250/800；
  环绕它的 `53/54/55/63/64/65/73/75` 是躯体装饰格（kind 0、HP/ATK/DEF/GOLD 全为 0）——
  **不可战斗也不能通过**，打龙只需打中央那一格。
- **id 57 魔導師ゼノ 与 id 59 バンパイア 在关卡布点表里没有战斗位**：
  id 59 由 `banpaia` 事件在 20F `(6,6)` 现场生成；id 57 只登记于图鉴块，
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
