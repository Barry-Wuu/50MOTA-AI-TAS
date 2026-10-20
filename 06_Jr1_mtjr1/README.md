# 06_Jr1_mtjr1

> 发行版 asset：`06_Jr1_mtjr1.lzh`（attach id 257745）

## 版本真身

**MTJr. 魔法の塔 小学生版 Ver1.0**——PC-98 原版（01 版）的小学生难度修改版。本体是**补丁器**：在 MS-DOS 下运行 `MTJR.COM` 打补丁生成 `MTJR.EXE`，再运行生成的 EXE 进游戏。

| 项 | 值 |
|---|---|
| 补丁器 | `game/mtjr.com`（14290 B，1997-08-21，富林野健一 作） |
| 说明 | `game/mtjr.doc`（3544 B） |
| 图标 | `game/zeno.ico`（766 B，独立画风红甲骑士头像） |
| 生成产物 | `game/MTJR.EXE`（101199 B）——**本次在 01 版 DOS 环境里现场运行 MTJR.COM 生成**（原版 MTE.EXE 为 101303 B，补丁版小 104 B） |
| 封包 | LHa (lh5)，`lha`/`lhasa` 可解 |

## 目录内容

```
06_Jr1_mtjr1/
├── 06_Jr1_mtjr1.lzh        # 原始发行封包（LHa）
├── game/                   # lha 解包内容 + 现场生成的运行产物
│   ├── mtjr.com            # 补丁器（给 MTE.EXE 打补丁）
│   ├── mtjr.doc            # 使用说明
│   ├── zeno.ico            # 图标
│   └── MTJR.EXE            # 运行产物（01 的 DOS 环境里生成）
├── floor1_06_MTJr.png      # 第 1 层实机截图
├── floor1_06_MTJr_after_move.png  # 按小键盘 2 后的对比图（1110 像素差异，验证可操作）
└── README.md
```

## 运行方式

本版无独立数据文件，**依赖 01 版（PC-98 原版）的磁盘环境**：

```text
1. 用 np2kai 启动 01_PC98原版_mtower.fdi（或把 mtjr.com 拷入该盘）
2. DOS 提示符下运行：MTJR.COM
   输出 "WSP self update 1.50 / MTJr.EXE 完了！"
3. 运行生成的：MTJR.EXE
4. 标题画面 "迷宮RPG『魔法の塔』 Hit any key!" → 按任意键进剧情 → 进第 1 层
```

`game/MTJR.EXE` 即第 3 步的产物，可直接拷回 01 的磁盘运行。

## 备注

- 布局与 01 原版同源，但**左下物品栏多一个阶梯状特殊道具**（小学生版特色：拔け穴多数、初期神剑），事件文本亦有差异。
- 与 01 属"同一游戏的两个难度变体"（修改版而非字节/程序重复）。
- 键位同 01：小键盘 2/4/6/8 移动，Return/Space 菜单，Pause = STOP。
