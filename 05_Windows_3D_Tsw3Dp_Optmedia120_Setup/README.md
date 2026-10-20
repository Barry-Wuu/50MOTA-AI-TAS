# 05_Windows_3D_Tsw3Dp_Optmedia120_Setup

> 发行版 asset：`05_Windows_3D_Tsw3Dp_Optmedia120_Setup.exe`（attach id 257746）

## 版本真身

**Tower of the Sorcerer(3DVersion) Ver1.1**（Oz3D 引擎，Turbo Delphi）——真 3D 等距迷宫英文版，HUD 显示 "Tower 1 F"，武器/盾显示 "Sacred"。

| 项 | 值 |
|---|---|
| 主程序 | `game/tsw3Dp.exe`（1940992 B） |
| 引擎 | Turbo Delphi（Oz3D） |
| 安装器 | **二级结构**：一级 `05_..._Setup.exe`（InstallShield 自解压）内嵌二级安装器 `level2_installer/TSW3D10.exe` |
| 数据 | `game/DATA/`、`data2/`、`help/`、`lang/`、`MIDI/`、`WAV/`、`savedat/` |

## 目录内容

```
05_Windows_3D_Tsw3Dp_Optmedia120_Setup/
├── 05_Windows_3D_Tsw3Dp_Optmedia120_Setup.exe  # 原始安装包（一级）
├── level2_installer/        # 二级安装器（含完整 payload）
│   ├── TSW3D10.exe
│   ├── isrt.dll / _IsRes.dll / _ISUser.dll
│   └── corecomp.ini / default.pal / FontData.ini
├── game/                    # 安装后的完整游戏目录（Program Files\TSW3D）
│   ├── tsw3Dp.exe
│   ├── DATA/ data2/ help/ lang/ MIDI/ WAV/ savedat/
│   └── tsw3D.txt / Readme.txt / 修正事項.txt / BGMPlayer.exe
├── floor1_05_TSW.png        # 第 1 层实机截图
└── README.md
```

## 运行方式

```bash
# 安装（或直接用已装好的 game/ 目录）
WINEPREFIX=<全新 win32 前缀> wine level2_installer/TSW3D10.exe
# 运行
WINEPREFIX=<同一前缀> wine game/tsw3Dp.exe
```

实测：wine 9.0，全新独立 WINEPREFIX（.wine05），第 1 层正常。

## 备注

- 与 04 同款二级安装器结构、同引擎，日/英两版，地图与数值独立，互不重复。
- 另排除项：`Magic Ball 2 New Worlds` 等重复续作不在本发行版清单内。
