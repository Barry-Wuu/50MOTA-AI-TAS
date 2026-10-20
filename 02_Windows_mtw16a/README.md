# 02_Windows_mtw16a

> 发行版 asset：`02_Windows_mtw16a.exe`（attach id 257749）

## 版本真身

**魔法の塔 for Windows［オプトメディア］**（Oz & Kenichi，2000-04-28）——Win16 平台的日文原版，50 层。

| 项 | 值 |
|---|---|
| 主程序 | `game/Mtw.exe`（1107456 B，2000-04-28） |
| 安装器 | LHa 自解压 + InstallShield 5 向导 |
| 数据 | `Data/` `Data2/` `data3/` `MIDI/` `WAV/` `SAVEDAT/` |
| 文档 | `MTW.TXT` / `README.TXT` / `Ranking.txt` / `修正事項.txt` / `MTW.HLP` |

## 目录内容

```
02_Windows_mtw16a/
├── 02_Windows_mtw16a.exe    # 原始安装包（LHa 自解压 → InstallShield 5）
├── game/                    # 安装后的完整游戏目录（Program Files\MTW16）
│   ├── Mtw.exe
│   ├── Data/ Data2/ data3/ MIDI/ WAV/ SAVEDAT/
│   └── MTW.TXT / README.TXT / Ranking.txt / 修正事項.txt
├── floor1_02_MTW16.png      # 第 1 层实机截图
└── README.md
```

## 运行方式

```bash
WINEPREFIX=<全新 win32 前缀> wine game/Mtw.exe
```

实测：wine 9.0，win32 前缀，第 1 层正常（塔 1 阶、1000/100/100、神剑神盾）。

## 备注

- **与 03 是同一个程序的两个语言发行版**：第 1 层画面与 `03_Windows_TSW_tsw12` 像素级一致，仅菜单语言不同（TSW = Tower of the Sorcerer = 魔法の塔 for Windows 的英文名）。这是整个发行版清单里**唯一真正的程序级重复对**。
- 去重方案见根目录 README 与 `mota_release_dedup.md`。
