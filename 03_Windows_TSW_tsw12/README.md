# 03_Windows_TSW_tsw12

> 发行版 asset：`03_Windows_TSW_tsw12.exe`（attach id 257748）

## 版本真身

**Tower of the Sorcerer Ver.2**（© 1996-2000 Oz & Kenichi）——Win16 平台的英文版，即 02 日文原版的英文本地化，50 层。

| 项 | 值 |
|---|---|
| 主程序 | `game/TSW.exe`（1237504 B，2000-04-28） |
| 安装器 | InstallShield 5 自解压向导（壳内确认 "This will install Tower of the Sorcerer"） |
| 数据 | `Data/` `Data2/` `Data3/` `Midi/` `Wav/` `Savedat/` |
| 文档 | `TSW.txt` / `Readme.txt` / `Ranking.txt` / `Tsw.hlp` / `Extra.gif` |

## 目录内容

```
03_Windows_TSW_tsw12/
├── 03_Windows_TSW_tsw12.exe  # 原始安装包
├── game/                     # 安装后的完整游戏目录（Program Files\Tower of the Sorcerer）
│   ├── TSW.exe
│   ├── Data/ Data2/ Data3/ Midi/ Wav/ Savedat/
│   └── TSW.txt / Readme.txt / Ranking.txt / Extra.gif
├── floor1_03_TSW.png         # 第 1 层实机截图
└── README.md
```

## 运行方式

```bash
WINEPREFIX=<全新 win32 前缀> wine game/TSW.exe
```

实测：wine 9.0，win32 前缀，第 1 层正常（Tower 1F、WEAPON/SHIELD 面板、方向键垫 UI）。

## 备注

- **与 02 是同一个程序**：第 1 层画面与 `02_Windows_mtw16a` 像素级一致（同窗口布局、同 UI、同地图、同美术），唯一区别是菜单语言（日/英）。
- 若按"同内容只留一版"去重，本版是删除候选（或反之留英删日，见根目录 README）。
