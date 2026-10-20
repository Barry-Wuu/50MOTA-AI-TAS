# 04_Windows_3D_Mtw3Dp_Optmedia122_Setup

> 发行版 asset：`04_Windows_3D_Mtw3Dp_Optmedia122_Setup.exe`（attach id 257747）

## 版本真身

**魔法の塔 for Windows(3DVersion) Ver1.82**（Oz3D 引擎，Turbo Delphi）——真 3D 等距迷宫版，50 层，开局 1000/100/100。

| 项 | 值 |
|---|---|
| 主程序 | `game/Mtw3Dp.exe`（1961472 B） |
| 引擎 | Turbo Delphi（Oz3D），窗口 802×491 |
| 安装器 | **二级结构**：`04_..._Setup.exe`（InstallShield 10.5 网络安装器）内嵌二级安装器 `level2_installer/MTW3D17.exe`，由它带完整 payload |
| 数据 | `game/DATA/`（CHT3D.OZ / KABE3D.OZ / KEY.OZ / Left3d*.bmp / Right3d*.bmp…）、`data2/`、`MIDI/`、`WAV/`、`savedat/`、`help/` |

## 目录内容

```
04_Windows_3D_Mtw3Dp_Optmedia122_Setup/
├── 04_Windows_3D_Mtw3Dp_Optmedia122_Setup.exe  # 原始安装包（一级网络安装器）
├── level2_installer/        # 从一级安装器内嵌提取的二级安装器
│   ├── MTW3D17.exe          # 真正带 payload 的安装器（Enter 驱动向导 4 步装成）
│   ├── isrt.dll / _IsRes.dll / _ISUser.dll
│   └── corecomp.ini / default.pal / FontData.ini
├── game/                    # 安装后的完整游戏目录（Program Files\MTW3D）
│   ├── Mtw3Dp.exe
│   ├── DATA/ data2/ help/ MIDI/ WAV/ savedat/
│   └── Mtw3D.txt / Readme.txt / 魔法の塔.txt / 修正事項.txt / BGMPlayer.exe
├── floor1_04_MTW.png        # 第 1 层实机截图
├── floor1_04_MTW_after_move.png  # 按 Up 后的对比图（738 像素差异，骑士上移一格）
└── README.md
```

## 运行方式

```bash
# 安装（也可直接使用已装好的 game/ 目录）
WINEPREFIX=<全新 win32 前缀> wine level2_installer/MTW3D17.exe   # Enter 驱动向导
# 运行
WINEPREFIX=<同一前缀> wine game/Mtw3Dp.exe
```

实测：wine 9.0，**全新独立 WINEPREFIX**（.wine04），第 1 层等距迷宫正常（骷髅、药水、钥匙，HUD 1000/100/100）。

## 备注

- 本版曾被误判"跑不了"：旧结论以为 OPTMEDIA 网络安装器无 payload、cab 内 0 文件。实际 payload 全在**二级安装器**里。
- 与 05 是同一引擎的日/英两个 3D 版本，地图与数值各自独立，**互不重复**。
