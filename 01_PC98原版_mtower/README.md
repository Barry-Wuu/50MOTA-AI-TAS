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
└── README.md
```

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
