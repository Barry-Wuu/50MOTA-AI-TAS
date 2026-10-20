# 07_Jr3D_mtjr3d13

> 发行版 asset：`07_Jr3D_mtjr3d13.exe`（attach id 257744）

## 版本真身

**魔法の塔Jr. for Windows(3DVersion) Ver1.3**（Turbo Delphi 2006，Oz3D 引擎）——Jr 系列的真 3D 版，等距迷宫。

| 项 | 值 |
|---|---|
| 主程序 | `game/Mtw3DJrp.exe`（1977856 B） |
| 引擎 | Turbo Delphi 2006（Oz3D） |
| 安装器 | Inno Setup（`unins000.exe`/`unins000.dat` 在列） |
| 数据 | `DATA/`、`data2/`、`help/`、`MIDI/`、`WAV/`、`savedat/` |
| 文档 | `MtJr3D.txt`（SJIS 日文）、`Readme.txt`、`修正事項.txt` |

## 目录内容

```
07_Jr3D_mtjr3d13/
├── 07_Jr3D_mtjr3d13.exe     # 原始安装包（Inno Setup）
├── game/                    # innoextract 完整解包（app/ 内容平铺）
│   ├── Mtw3DJrp.exe
│   ├── DATA/ data2/ help/ MIDI/ WAV/ savedat/
│   └── MtJr3D.txt / Readme.txt / 修正事項.txt
├── floor1_07_Jr3D.png       # 第 1 层实机截图
└── README.md
```

## 运行方式

```bash
# 解包（已解好，game/ 即结果）
innoextract 07_Jr3D_mtjr3d13.exe

# 运行（必要 DLL 已齐）
WINEPREFIX=<全新 win32 前缀> wine game/Mtw3DJrp.exe
```

实测：wine 9.0，全新独立 WINEPREFIX（.wine07），第 1 层正常。

## 备注

- 本版曾被误判"Wine 栈溢出崩溃（Delphi 2006 不兼容）"——实为**脏 WINEPREFIX + 挂死进程**的环境问题；换全新前缀后与 04/05 一样正常。
- 注意区分：**Jr 系只有本版（07）是 3D**；06 的 Jr1 是 2D PC-98 修改版。
