# 魔塔1 地图理解 · 会话交接

> 给下一个会话用。写于 2026-10-22 的长会话末尾（该会话工具输出多次异常，凡"看起来成功了"的结论都请按下文 §7 复核）。
> 范围：本目录 `01_PC98原版_mtower/`（PC-98 原版魔法の塔）的 50F+00 层地图数据、渲染图与文档。

## 0. 三分钟上手

- 仓库工作副本在沙箱持久目录：`…/work/.artifacts/r/`（含 01..08 各版；本目录=01）。
- 中间数据同样在 `.artifacts/`：`crops/live.json`（运行时要数据）、`crops/crop_NNN.png`（189 块 imgCrop）、
  `javamap.json`（strMessage）、`dyn_raw.json` / `dynamic_canonical.json`（事件写入表）、`mtower.jvm`（`javap -c -p MTower.class`）。
- 脚本在本目录 `tools/`：`dynscan.py`（扫常量写入站点）、`register_boss.py`（登记 49/50F 运行时魔王）、
  `gen_monster_table.py`（重建 README 战力表）、`gen_texts.py`（重建 README 文案附录）。
  渲染脚本 `sheet4.py` 与若干一次性脚本目前**只在 `.artifacts/`，未入库**。
- 跑 Java 版需要：`jd/*.deb` 解包出的 JDK 21（在 `.artifacts/`）+ Xvfb；注意 Debian 包里的
  `conf/security/java.security`、`lib/security/*` 是**指向不存在的绝对路径的符号链接**，必须换成
  `prefix/etc/java-21-openjdk/...` 的真实文件，否则 `java` 静默失败、`javac` 报 "Error loading java.security file"。
- 推送用一次性带 token 的 URL（token 曾被贴进聊天，**建议已在 GitCode 侧轮换**）；
  提交信息**一律用 `git commit -F - <<'MSG'`**，别用 `-m "…"`（本会话反引号把说明吃掉两次）。

## 1. 数据来历（重要：01 的地图不是从 01 的文件解出来的）

- `game/*.P58` 是 PC-98 位平面 RLE **图像**（含精灵图），`MT.GTX` 是带属性字节的**文本**，
  `INITIAL.DAT` = 46B 头 + 50×130×u16 的**进度状态**（不是二维地形）。所以 01 自身的文件里没有可直接
  读出的 50F 地形表。
- 实际地形/物体来自 **08 Java 版** `MTower.class`：先是 `loadMapData` 的字节码 + `jvmrun.py` 简易解释器还原，
  最终用 `Dump3`/`Drive` 反射启动 applet 后 dump `map / mapObject / mapAttribute / objectAttribute`
  → `crops/live.json`。楼层数、怪物四维、道具、文案同源。
- 因此：**数值与铺法是「08 运行时」口径**；与 01 的 PC-98 数值是否逐字相同，未做（要另解 `MONSTER.P58`）。

## 2. 大表坐标模型

- `map` 是 `char[78][130]`，`mapObject` 同形；每层 13×13，**行=带 band、列=槽 slot**：
  `row=band*13+y`，`col=slot*13+x`，`band=row//13`，`slot=col//13`，**层号 = band*10 + slot + 1**（1..50）。
- band5 的槽位是附加块：`slot1 → 序号 52 = 00 层`（幸运金币 (6,6)、上行楼梯 (1,1)），
  `slot8 = 图鉴 catalog`，`slot9 = stage_flags`。序号 51/53..58 未用。
- 引擎里 `mapX`=slot、`mapY`=band，楼层序号 = `mapY*10 + mapX + 1`；`eventMT` 里两处硬编码特例
  `index==1 ↔ index==52` 构成 **1F 与 00 层互连**（两块的楼梯都在 (1,1)）——所以 23F 的 "GO 0F" 只是提示，
  49F/50F 与 00 层无关。角色格 = `charaX/5 × charaY/5`（1F 起点 (6,10)）。
- 主角与道具状态也塞在 stage_flags 块里：HP/ATK/DEF/GOLD = `mapObject[66..69][118]`，
  「持有十字架」`mapObject[74][119]==1`（对 id 48/49/59 翻倍）、「持有屠龙匕」`mapObject[70][120]==1`（对 id 74 翻倍）。

## 3. 属性表列义（`mapAttribute[200][40]` / `objectAttribute[200][40]`）

`[1]` 主贴图索引、`[3]` 类型、`[5]` 文案号(strNumber)、地形用 `[6..9]` 备用；物体 `[10..13]` = HP/ATK/DEF/GOLD。
`mapAttribute[][3]`：0=通路 1=墙 2=门/楼梯（kind 2 即 `MAP_LOCALGATE`）。
`objectAttribute[][3]`：0 普通/障碍 1 消息 3 装备(增益存四维列) 4 道具 5 门 6 怪物 7 祭坛 8 钥匙 11 记分 14 收 keys 15 商店。
楼梯贴图 crop 34=上行、35=下行（每层各一处，除 1F 只有 (1,1) 门格外）。

## 4. 已验证事实（可信，已在 README/JSON/CSV 落地）

- 楼梯链 49/49 自洽；41F 左右对称、44F 为"幻之层"需密宝进入（老人文案+结构一致）。
- **暗墙三类**：① 地形型（墙图素+kind 0）2 处：16F(8,2)、18F(3,6)；② `obj 89` 撞塌式 52 处
  （5F、9F、12F×3、14F、16F×2、19F×2、35F×21、36F×20、41F、catalog）——这类格**地形是地板**、隐形墙靠物体实现；
  ③ `obj 115` 隐形块 46 处，**在 23F 的 44 格按 8-连通恰好分成 4 个字形 = "GO 0F"**
  （G@(2,1)-(5,5)14格、O@(8,3)-(10,5)8格、0@(2,7)-(5,10)12格、F@(7,7)-(10,11)10格）。
- **事件写入**（`tools/dynscan.py`，排除 `loadMapData*/Initdata*` 与 band5 两块）：115 格 / 22 层。
  例：35F 盗贼凿墙=`map[4][47]=1`（49F 之外唯一 directCheck 开墙，另一处 15F(8,1)）；
  34F 5 把隐藏钥匙；35F 雪的结晶；39F 升华之翼；41F 降临之翼（+15F 镐、49F 屠龙匕、40/49F 成批水晶回复药）；
  3F/42F/48F/49F 隐藏生成魔导师、32F/40F 金骑士、20F(6,6) 吸血鬼(`banpaia`)。
- **战力**：41 个怪物 ID / 经典译名 33 组；结算
  `单次伤害 = ATK×attackDouble − 怪DEF`（≤怪DEF 则打不动），
  `我方损失 = (怪ATK − 我DEF)×(⌈怪HP/(ATK×attackDouble−怪DEF)⌉ − 1)`（最后一击不掉血）。
- **两只魔王共用一行数据且都是运行时放置**：`Zeno(g,110,55)` → **49F (6,3)**（外圈 8 格 `obj58` 魔法警卫成 3×3 环）、
  `Zeno2(g,123,57)` → **50F (6,5)**（`obj88` 小偷先写在该格 → 小偷变身，同格两对象）。
  封印后 `eventMT` 把 `objectAttribute[57][10/11/12]` 改写为 **800/500/100**（原值 1/10）——
  百度百科敌人表"800×10/500×10/100×10"正是这次改写；class 内**没有** 1580/190 的对象，
  故百科"魔王(50层) 8000/1580/190"不属于本版。
- 大乌贼(15F) = 中央 `71` + 八块躯体共 9 格，**九格全是战斗单位**；魔龙(35F) 中央 `(6,5)` 可战斗，
  环绕 8 格 `53/54/55/63/64/65/73/75` 是 kind 0 且四维全 0 的**装饰躯体**（不可打、不可走）。
- 危险格（非战斗掉血）：熔岩 `obj79`（每步 −200，13F 80 格 / 26F 18 格）；`obj96` 大魔导师 HP 减半；
  魔術師 `99/100` 相邻 −200/−100（神圣盾可挡）；魔龙吐息 −1000；洞 `obj19/20` 位移。
- 文案：`strMessage[2][400]` 实际 308 条；133 条被 obj/地形引用，39 条由 `sipush N; putfield strNumber`
  直引（函数名已标），137 条经运行时计算下标（**未静态定位，README 里按原样标注，没猜**）。
  英文数组里 javap 残留的 `\"`、`\n` 已还原。

## 5. 渲染样式约定（改图前先看这条）

- `map_50f.png` = **5 列 × 11 行**：顶行只有第 1 列是 00 层，其下 10 行为 1..50 层。
- 暗墙/隐形块/事件开墙：一律**墙图素压暗到 40%**（同图素同系数；若该格自带别的墙图素则压暗其自身图素，
  如 24F(6,0) 的 crop 9）。`obj 115`（游戏内是地板）也按压暗砖墙标记。
- 楼层号：用 `work/uploads/magictower.png` 里提取的真数字 Tile（32×32 定长切、`alpha>50 且非品红键`，
  0..4 = idx 185..189，5..9 = idx 193..197，色 (255,95,0)），涂在每层 `(0,0)`、`(0,1)`；
  100 个编号位实测全是墙格，不遮信息。
- 隐藏物体（4 节事件写入）**同格多对象全部叠画**：主对象 55% 铺满整格，排序恒为
  **怪/BOSS > 门 > NPC/消息 > 战利品**（否则警卫会被战利品挤掉，本会话踩过）；
  第 2~4 个 80%、22px 贴在**本格内**的右下/左下/右上/左上（贴片偏移曾是 56px → 越界画进邻格，也踩过）；
  ≥5 个时左上叠数字贴片。

## 6. 未完成 / 待决（下一个会话从这里接）

1. **变长目标写入未定位**：`mapObject[变量][变量]=常量` 形式（如 49F 蓝钥匙 `obj3`）拿不到坐标。
   现在把蓝钥匙按用户口述（"第八只警卫格同格两把钥匙"）画在 `(5,2)` 作**示意**，JSON
   `overlay_cells`+`limits` 已注明证据强度。要做实：给 08 harness 注入真正的 AWT `KeyEvent`
   （写 `currentKey`+`LeftKey` 不足以驱动 `moveCharacter`，本会话试过没动起来），击杀后 dump `mapObject`。
2. 渲染脚本 `sheet4.py`/`build*.py` 未入库；`map_50f.png`、`floors/*.png` 目前**无法从仓库自身复现**。
3. 01 原版的 `.P58`/`MT.GTX` 仍未解码 → 数值/铺法与 Java 版的差异未知（06 小学生版同源可交叉验证）。
4. README 战力表译名取自**百度百科**（玩家整理，非官方汉化）：个别 GOLD 与我们的数据有 1 处出入，且
   百科里"50层魔王"那行本版不存在；若拿到官方汉化表，可直接改 `magic_tower1_monsters.csv` 的 `name_cn` 后
   跑 `tools/gen_monster_table.py`。
5. 23F "GO 0F" 的 0 与字母 O 无法区分（字形 2 行"GO / 0F"），若要与 00 层楼梯 (1,1) 建立更强联系，需先解 §6.2。

## 7. 本会话的工具故障（别让下一个会话上当）

- **工具输出多次被截断、显示成 JSON 残片**，个别命令的 stdout 里混进了像是"我的回复文本"的内容：
  所以任何"生成/写入成功"的自述都要**重新读文件或查远端**验证；不要相信中间一次显示。
- 已因此发生的真实错误（都已修，但记着）：`git commit -m` 里反引号被 shell 执行（提交说明丢行）、
  我的 JSON patch 用 `str.replace` 未命中却打印"成功"、`xvfb-run -f` 被当成 fontconfig 参数（它是 xauthority）、
  `sorted(set(...))` 破坏 rank、贴片偏移越界、登记 50F 魔王时覆盖了原有 obj88。
- 仓库 token 曾出现在聊天里：轮换后请把它放回 `~/.config`，别再写进任何提交或文件。

## 8. 本目录文件清单

| 文件 | 内容 |
|---|---|
| `README.md` | 版本真身、目录内容、**怪物战力表**（含战斗结算与提醒）、运行方式、备注、**附录：309 条塔内文案**（日/英+引用方式+出现层） |
| `magic_tower1_map_50f.json` | 每层 `terrain/objects/secret_walls/entities/bosses/dynamic_objects/dynamic_terrain/runtime_boss` + 顶层 `_obj115_invisible_marker_tiles`、`_dynamic_spawns`（含 `overlay_cells`、`corrections`、`limits`） |
| `magic_tower1_rows.csv` | 大表逐行标记 S 暗墙 / T 隐形块 / E 实体 / B BOSS |
| `magic_tower1_entities.csv` | 全部布点（floor,y,x,obj,kind,role,名称,HP,ATK,DEF,GOLD） |
| `magic_tower1_monsters.csv` | 41 怪物+道具有四维的行，含 `name_cn` 经典译名 |
| `magic_tower1_dynamic.csv` | 事件后才出现的物体 / 动态地形 |
| `magic_tower1_texts.csv` | 309 条文案（strNumber、日、英、引用方式、出现层、分组） |
| `magic_tower1_walkroute.md` | 走法路线、危险格、隐藏物体、00 层通达方式 |
| `map_50f.png` / `floors/` / `floor_00.png` / `hidden_floor_band5.png` / `tiles/` | 渲染产出与 189 块 imgCrop 切片 |
| `tools/` | `dynscan.py` `register_boss.py` `gen_monster_table.py` `gen_texts.py` |
| `01_PC98原版_mtower.fdi` / `game/` | 原始软盘映像与其内 23 个文件 |
