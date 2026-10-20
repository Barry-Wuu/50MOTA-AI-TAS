# 魔塔（50MOTA-AI-TAS）发行版「魔法の塔」去重与版本核查

> 仓库：Barry_Wu_/50MOTA-AI-TAS ｜ 发行版：名称「魔法の塔」/ tag「魔塔」/ prerelease=true
> 核查方式：GitCode v5 API 拉清单 + 8 个文件全量下载 + 二进制/资源级分析 + **真实安装运行 + 第 1 层实机截图**
> **最终状态：8/8 全部解包、安装/启动、实机跑通、第 1 层截图完成（2026-10-20）**

## 0. 凭据：已解开，token 有效（2026-10-20 修正）

- sojson/CryptoJS + **空字符串密钥** 解密成功，明文为：
  `tokenis<REDACTED-TOKEN>`
- **前 7 个字符 `tokenis` 是人话前缀（= "token is"）**，不是 token 的一部分。此前 401 是误把整串当前凭据所致。
- 真正 token 本体：`<REDACTED-TOKEN>`，用 **`Authorization: Bearer`** 鉴权：
  - `GET /api/v5/user` → **200，login=Barry_Wu_**（即仓库 owner 本人）
- **结论：删除操作已解除凭据阻断**，只待确认删除目标即可执行。

## 1. 资源清单（asset id 来自 v5 API）

| # | 文件名 | 类型 | asset id |
|---|--------|------|----------|
| 01 | 01_PC98原版_mtower.fdi | attach | 257750 |
| 02 | 02_Windows_mtw16a.exe | attach | 257749 |
| 03 | 03_Windows_TSW_tsw12.exe | attach | 257748 |
| 04 | 04_Windows_3D_Mtw3Dp_Optmedia122_Setup.exe | attach | 257747 |
| 05 | 05_Windows_3D_Tsw3Dp_Optmedia120_Setup.exe | attach | 257746 |
| 06 | 06_Jr1_mtjr1.lzh | attach | 257745 |
| 07 | 07_Jr3D_mtjr3d13.exe | attach | 257744 |
| 08 | 08_Java_MTower08a.zip | attach | 257743 |
| — | 魔塔.zip / .tar.gz / .tar.bz2 / .tar | source（平台自动生成） | 无 |

## 2. 实机运行结果（**8/8 全部跑通**）

工具链：wine 9.0（win32 前缀跑 Win16；**全新独立 WINEPREFIX 跑 Turbo Delphi 游戏**）、unshield/innoextract、OpenJDK 20、**自编译 np2kai（SDL2，真实 PC-98 BIOS ROM）**、ImageMagick 截屏。

| # | 版本真身 | 安装/运行 | 第1层截图 | 结论 |
|---|----------|-----------|-----------|------|
| 01 | **魔法の塔 Ver1.1（1996 PC-98 原版）** | ✅ FDI 软盘直接引导 MS-DOS 5.00A（IO.SYS 是隐藏系统文件，AUTOEXEC.BAT 自动跑 MTE.EXE）；np2kai + 真实 BIOS ROM | ✅ `floor1_01_MTE.png`（+ after_move 验证可操作） | MTE.EXE 101303B，MZ 格式；PC-9801VX+ 及 98 兼容机 + MS-DOS 3.1+；50 层，HUD 1000/100/100 |
| 02 | **魔法の塔 for Windows [オプトメディア]** | ✅ LHa→IS3 安装器在 win32 前缀跑通，装出 `Program Files/MTW16/Mtw.exe` | ✅ `floor1_02_MTW16.png` | Mtw.exe 2000-04-28 |
| 03 | **Tower of the Sorcerer Ver.2** | ✅ InstallShield 向导装出 `Tower of the Sorcerer/TSW.exe` | ✅ `floor1_03_TSW.png` | © 1996-2000 Oz & Kenichi |
| 04 | **魔法の塔 for Windows(3DVersion) Ver1.82** | ✅ InstallShield 10.5 二级安装器（MTW3D17.exe→Mtw3Dp.exe，Enter 驱动向导 4 步装成）；**全新 WINEPREFIX=/root/.wine04 下正常运行** | ✅ `floor1_04_MTW.png`（+ after_move） | Mtw3Dp.exe 1961472B，Turbo Delphi (Oz3D 引擎)，窗口 802x491，开局 1000/100/100 |
| 05 | **Tower of the Sorcerer(3DVersion) Ver1.1** | ✅ 同款安装器（TSW3D10.exe→tsw3Dp.exe）；WINEPREFIX=/root/.wine05 | ✅ `floor1_05_TSW.png` | tsw3Dp.exe 1940992B，HUD 显示 "Tower 1 F"，武器/盾 "Sacred" |
| 06 | **MTJr. 魔法の塔 小学生版 Ver1.0** | ✅ lha 解出 mtjr.com（富林野健一作的 MTE.EXE 补丁器）；**在 01 的 DOS 环境运行 MTJR.COM 生成 MTJR.EXE 并实跑** | ✅ `floor1_06_MTJr.png`（+ after_move） | 布局同原版但新增阶梯状特殊道具（小学生版特色：拔け穴多数、初期神剑） |
| 07 | **魔法の塔Jr. for Windows(3DVersion) Ver1.3** | ✅ innoextract 完整解包（Mtw3DJrp.exe 1977856B，必要 DLL 已齐）；WINEPREFIX=/root/.wine07 | ✅ `floor1_07_Jr3D.png` | Turbo Delphi 2006 (Oz3D 引擎) |
| 08 | **Java 版 Magic Tower** | ✅ 写 AppletStub wrapper 空调起 Applet（820×520） | ✅ `floor1_08_Java.png` | "Tower 1F"，© 2000 Oz，Internet RPG "Magic Tower" |

### 2.1 曾被误判"跑不了"的三组，如何全部跑通

| # | 旧结论（误判） | 根因 | 正解 |
|---|----------------|------|------|
| 04/05 | OPTMEDIA 网络安装器卡死下载、cab 内 0 文件 | 只解包了第一层安装器，没发现**二级安装器**（MTW3D17.exe/TSW3D10.exe 内嵌 isrt.dll + 完整 payload） | 跑二级安装器，Enter 键驱动向导即装成 |
| 07 | Wine 0x0eedfade 栈溢出崩溃（Delphi 2006 不兼容） | **脏 WINEPREFIX + 挂死进程**的环境问题，非兼容性问题 | 用**全新独立 WINEPREFIX**（.wine04/.wine05/.wine07），三个 Delphi 游戏全部正常 |
| 01/06 | 需 PC-98 BIOS ROM、DOSBox 是 IBM-PC 模拟器跑不了 | 方向正确但过度悲观：**np2kai 可自编译 + BIOS ROM 可从公开仓获取**；且误以为 FDI 无 IO.SYS | np2kai 打 usebios 补丁 + 真实 BIOS ROM；IO.SYS 是隐藏系统文件（mtools 默认不显示），**原盘可直接 DOS 启动** |

### 2.2 PC-98 运行环境搭建记录（np2kai，2026-10-20）

- **源码**：np2kai master，`cmake .. -DUSE_SDL=2 -DUSE_SDL2_TTF=ON -DBUILD_WX=OFF`（SDL2 版，Ubuntu 22.04）
- **补丁 1（必需）**：`sdl/np2.c` 的 `initload()` 前强制 `np2cfg.usebios = 1`——SDL 端 ini.c 无 usebios 项，默认 0 导致 bios.rom 永不加载（只用内置 nosyscode 桩，表现为"IPL 后黑屏/无 DOS"）
- **BIOS ROM**：archtaurus/RetroPieBIOS 仓（bios.rom 98304B + font.rom 288768B + itf.rom 32768B + sound.rom 16384B），放 `~/.config/sdlnp21kai/`；md5 与该仓文档一致
- **字体**：SDL2_TTF 需要 `~/.config/sdlnp21kai/default.ttf`，软链 NotoSansCJK-Regular.ttc
- **PC-98 引导链**（反汇编 bios.rom 0xFD800 reset stub 确认）：复位 → BIOS init → IPL 读软盘 CHS(0,0,1) 启动扇区（**要求 0x1FE 处有 0xAA55 签名**，否则进 ROM 监视器）→ 加载到段 0x1FE0 并跳转执行
- **键盘**：小键盘 2/4/6/8 或光标键移动；Return/Space 开菜单；**Pause 键 = PC-98 STOP**（MTE.EXE 里退出回 DOS）；菜单内确认键为小键盘回车
- **DOS 磁盘映像操作**：FDI = 4096B 头 + 1.44MB 原始盘（80 柱×2 头×18 扇区×512B）；用 mtools 时先 `dd skip=4096` 剥头，操作完再拼回

## 3. 第 1 层实机画面对比（决定性证据）

| 画面 | 观察 |
|------|------|
| `floor1_02_MTW16.png` vs `floor1_03_TSW.png` | **像素级完全一致**：同窗口布局、同 UI（WEAPON/SHIELD 面板、方向键垫）、同地图、同美术。唯一区别是菜单语言（日/英）。**02 与 03 是同一个程序的两个语言发行版**（TSW = Tower of the Sorcerer = 魔法の塔 for Windows 的英文名） |
| `floor1_08_Java.png` vs 上两者 | **地图布局完全相同**（左上楼梯、顶部 3 史莱姆、钥匙/药水/蝙蝠位置一一对应），但**美术皮肤是 Java 版自有一套**。同作者（Oz）的同一地图数据、第三个呈现 |
| `floor1_01_MTE.png` vs `floor1_06_MTJr.png` | **同一地图数据**（PC-98 原版 vs 其小学生版补丁），06 左下物品栏多一个阶梯状特殊道具；HUD 完全一致（塔1階/1000/100/100/神剑神盾） |
| 04 vs 05 vs 07 | 三款 Oz3D 引擎（Turbo Delphi）等距 3D 迷宫，各自独立地图与数值（04/05 开局 1000/100/100；05 武器显示 Sacred），互不重复 |

附带美术证据：08 的 `title.gif` 写明 "Magic Tower © 2001 Oz & Kenichi / © 1996 N.W"；06 的 `ZENO.ICO` 是独立画风红甲骑士头像。

## 4. 关于"重复"的最终结论

- **字节级**：8 文件 sha256 各不相同 → 无文件级重复。
- **程序级（实锤）**：**02 = 03**（同一游戏「魔法の塔 for Windows / Tower of the Sorcerer」的日文原版与英文版，运行画面像素级一致）→ **这是发行版里唯一真正的重复对**。
- **内容级**：08 Java 与 02/03 **地图相同、美术与平台不同**（同作者官方 Java 移植）→ 算"同内容跨平台版"，是否算重复取决于口径。
- **内容级（PC-98 线）**：01 与 06 是**同一游戏的两个难度变体**（06 = 01 的补丁产物），地图数据同源但 06 有额外道具与事件文本，属"修改版"而非字节/程序重复。
- **独立分支**：04/05（真 3D，Mtw3D/Tsw3D）、07（Jr3D）均不与任何其它文件重复。
- 修正前轮两处误判：① 03 TSW 并非"另一引擎"，与 02 同程序；② 06 Jr1 是 **2D** PC-98 版（"小学生版"），不是伪 3D；Jr 系只有 07 是 3D。

## 5. 去重删除方案（凭据已就绪，待确认目标）

**最小去重**：02/03 二选一删除（建议留 02 日文原版 Mtw.exe、删 03 英文版，或按你偏好）：

| 删除候选 | asset id | 理由 |
|----------|----------|------|
| 03 TSW（英） | 257748 | 与 02 像素级同画面，仅菜单语言不同 |
| 或 02 MTW16（日） | 257749 | 若你更想留英文版 |

**进一步瘦身（可选，口径由你定）**：08 Java（257743）与 02/03 同地图，若"同内容即重复"则三选一。

**同源变体（可选）**：06（257745）是 01（257750）的小学生版补丁，若"同源只留原版"可删 06。

**无法归入重复集**：01（PC-98 原版源头，1996 历史地位）、04/05/07（3D 独立分支）。

> 待你点名删除目标（asset id 列表），二次确认后调用删除接口执行。
> 4 个 source 源码包为平台自动生成、无 asset id，不单独处理。

## 6. 截图资产索引（/workspace/mota_art/）

| 文件 | 版本 | 说明 |
|------|------|------|
| `floor1_01_MTE.png` / `floor1_01_MTE_after_move.png` | 01 PC-98 Ver1.1 | np2kai + 真实 BIOS + DOS 5.00A 实跑；after_move 为按小键盘 2 后对比（923 像素差异，骑士已移动） |
| `floor1_02_MTW16.png` | 02 Win16 日文 | wine 实跑 |
| `floor1_03_TSW.png` | 03 Win16 英文 | wine 实跑 |
| `floor1_04_MTW.png` / `floor1_04_MTW_after_move.png` | 04 3D Ver1.82 | 二级安装器安装 + .wine04 前缀实跑 |
| `floor1_05_TSW.png` | 05 3D Ver1.1 | .wine05 前缀实跑 |
| `floor1_06_MTJr.png` / `floor1_06_MTJr_after_move.png` | 06 小学生版 | MTJR.COM 现场生成 MTJR.EXE 后实跑（1110 像素差异验证可操作） |
| `floor1_07_Jr3D.png` | 07 Jr3D Ver1.3 | .wine07 前缀实跑 |
| `floor1_08_Java.png` | 08 Java | AppletStub wrapper 实跑 |
