# 魔塔（50MOTA-AI-TAS）发行版「魔法の塔」8 版本仓库

> 来源：GitCode 仓库 `Barry_Wu_/50MOTA-AI-TAS` ｜ 发行版「魔法の塔」（tag「魔塔」，prerelease）
> 核查方式：v5 API 拉清单 + 8 个文件全量下载 + 二进制/资源级分析 + **真实安装运行 + 第 1 层实机截图**
> **状态：8/8 全部解包、安装/启动、实机跑通、第 1 层截图完成**

每个发行版一个文件夹，目录名 = 发行版 asset 文件名（去扩展名）。各文件夹内含：原始安装包/介质、解出/安装后的完整游戏目录（`game/`）、该版第 1 层实机截图、版本 README。

## 版本总览

| # | 文件夹 | 版本真身 | 平台/引擎 | 主程序 | 运行方式 |
|---|--------|----------|-----------|--------|----------|
| 01 | [`01_PC98原版_mtower/`](01_PC98原版_mtower/) | 魔法の塔 Ver1.1（1996 PC-98 原版） | PC-98 + MS-DOS 5.00A | MTE.EXE（101303 B） | np2kai + 真实 BIOS，AUTOEXEC 自动进游戏 |
| 02 | [`02_Windows_mtw16a/`](02_Windows_mtw16a/) | 魔法の塔 for Windows［オプトメディア］ | Win16 | Mtw.exe（1107456 B） | wine（win32 前缀） |
| 03 | [`03_Windows_TSW_tsw12/`](03_Windows_TSW_tsw12/) | Tower of the Sorcerer Ver.2（英） | Win16 | TSW.exe（1237504 B） | wine（win32 前缀） |
| 04 | [`04_Windows_3D_Mtw3Dp_Optmedia122_Setup/`](04_Windows_3D_Mtw3Dp_Optmedia122_Setup/) | 魔法の塔 for Windows(3DVersion) Ver1.82 | Turbo Delphi（Oz3D） | Mtw3Dp.exe（1961472 B） | wine（全新前缀） |
| 05 | [`05_Windows_3D_Tsw3Dp_Optmedia120_Setup/`](05_Windows_3D_Tsw3Dp_Optmedia120_Setup/) | Tower of the Sorcerer(3DVersion) Ver1.1 | Turbo Delphi（Oz3D） | tsw3Dp.exe（1940992 B） | wine（全新前缀） |
| 06 | [`06_Jr1_mtjr1/`](06_Jr1_mtjr1/) | MTJr. 魔法の塔 小学生版 Ver1.0 | PC-98（补丁修改版） | mtjr.com → MTJR.EXE（101199 B） | 01 的 DOS 环境跑 MTJR.COM 生成 |
| 07 | [`07_Jr3D_mtjr3d13/`](07_Jr3D_mtjr3d13/) | 魔法の塔Jr. for Windows(3DVersion) Ver1.3 | Turbo Delphi 2006（Oz3D） | Mtw3DJrp.exe（1977856 B） | wine（全新前缀） |
| 08 | [`08_Java_MTower08a/`](08_Java_MTower08a/) | Magic Tower 0.8a（Java Applet） | Java | MTower.class（270616 B） | `java RunApplet` |

## 去重结论（摘要）

完整分析见 [`mota_release_dedup.md`](mota_release_dedup.md)。

- **字节级**：8 文件 sha256 各不相同，无文件级重复。
- **程序级（唯一实锤重复对）**：**02 = 03**——同一游戏「魔法の塔 for Windows / Tower of the Sorcerer」的日文原版与英文版，第 1 层画面像素级一致，仅菜单语言不同。
- **内容级**：08 Java 与 02/03 地图相同、美术与平台不同（同作者官方 Java 移植）——算不算重复取决于口径。
- **同源变体**：06 是 01 的补丁产物（小学生版），地图数据同源但 06 有额外道具与事件文本，属"修改版"而非重复。
- **独立分支**：01（PC-98 原版源头）、04/05（3D 日/英）、07（Jr3D）均不与任何其它文件重复。

## 第 1 层截图索引

每个文件夹内直接附该版截图；集中索引在 [`mota_art/`](mota_art/)：

| 文件 | 版本 | 说明 |
|------|------|------|
| `floor1_01_MTE.png` / `floor1_01_MTE_after_move.png` | 01 | np2kai + 真实 BIOS + DOS 5.00A；after_move 为按小键盘 2 后对比（923 像素差异） |
| `floor1_02_MTW16.png` | 02 | wine 实跑 |
| `floor1_03_TSW.png` | 03 | wine 实跑 |
| `floor1_04_MTW.png` / `floor1_04_MTW_after_move.png` | 04 | 二级安装器安装 + 全新前缀实跑（738 像素差异） |
| `floor1_05_TSW.png` | 05 | 全新前缀实跑 |
| `floor1_06_MTJr.png` / `floor1_06_MTJr_after_move.png` | 06 | MTJR.COM 现场生成 MTJR.EXE 后实跑（1110 像素差异） |
| `floor1_07_Jr3D.png` | 07 | 全新前缀实跑 |
| `floor1_08_Java.png` | 08 | AppletStub wrapper 实跑 |

## 运行环境要点

- **Windows 版（02/03/04/05/07）**：wine 9.0。Win16（02/03）用 win32 前缀；三款 Turbo Delphi 游戏（04/05/07）**必须用全新独立 WINEPREFIX**（脏前缀 + 挂死进程会被误判为"栈溢出不兼容"）。
- **04/05 安装**：一级安装器只是网络安装器，真正 payload 在内嵌的**二级安装器**（各目录 `level2_installer/`），Enter 键驱动向导即可装成。
- **PC-98 版（01/06）**：np2kai（自编译，SDL2）+ 真实 PC-98 BIOS ROM。
  - 关键补丁：`sdl/np2.c` 的 `initload()` 前强制 `np2cfg.usebios = 1`（SDL 端默认 0，导致 bios.rom 永不加载，表现为"IPL 后黑屏/无 DOS"）
  - BIOS ROM 放 `~/.config/sdlnp21kai/`（bios.rom/font.rom/itf.rom/sound.rom + default.ttf 软链）
  - 01.fdi 可直接引导 MS-DOS 5.00A（IO.SYS 是隐藏系统文件，mtools 默认不显示，勿被误导）
  - 键位：小键盘 2/4/6/8 移动；Return/Space 菜单；**Pause = PC-98 STOP**（退出回 DOS）
  - FDI = 4096 B 头 + 1.44 MB 原始盘；用 mtools 操作前先 `dd skip=4096` 剥头、用完拼回
- **Java 版（08）**：OpenJDK 20，`java RunApplet`（仓库内附 AppletStub wrapper 源码）。

## 曾被误判"跑不了"的三组（已全部跑通）

| # | 旧结论（误判） | 正解 |
|---|----------------|------|
| 04/05 | OPTMEDIA 网络安装器卡死下载、cab 内 0 文件 | 只解了第一层；**二级安装器**（MTW3D17.exe/TSW3D10.exe）内嵌完整 payload |
| 07 | Wine 0x0eedfade 栈溢出（Delphi 2006 不兼容） | 脏 WINEPREFIX + 挂死进程的环境问题；换全新前缀即正常 |
| 01/06 | 需 PC-98 BIOS ROM、DOSBox 是 IBM-PC 模拟器跑不了 | np2kai 可自编译 + BIOS ROM 公开仓可获取；且原盘可直接 DOS 启动 |

---
*本仓库为游戏考古/逆向研究用途，所有 ROM/磁盘映像版权归原权利人（Oz & Kenichi / N.W）所有。*
