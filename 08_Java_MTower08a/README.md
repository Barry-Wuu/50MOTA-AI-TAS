# 08_Java_MTower08a

> 发行版 asset：`08_Java_MTower08a.zip`（attach id 257743）

## 版本真身

**Magic Tower 0.8a**（© 2000 Oz & Kenichi / © 1996 N.W，Shigemasa Ozawa，Free Soft）——官方 Java Applet 移植版，Internet RPG "Magic Tower"，50 层。

| 项 | 值 |
|---|---|
| 主类 | `MTower.class`（270616 B） |
| Applet 壳 | `RunApplet.class` + `RunApplet.java`（本地实现的 AppletStub wrapper，空调起 Applet） |
| 依赖 | 仅需 JRE（`Required DLLs: None`） |
| 数据 | `data/`、`data2/`、`image/`、`himage/`、`midi/`、`wav/`、`au/`、`score/`、`savedat/` |
| 文档 | `MTower.txt`、`Readme.txt`、`HowtoSaveJPN.html`、`HowtoSaveENG.html`、`Autoexec.bat` |

## 目录内容

```
08_Java_MTower08a/
├── 08_Java_MTower08a.zip    # 原始发行封包（Zip，store 压缩）
├── game/                    # zip 解包内容（MagicTower/）
│   ├── MTower.class         # 游戏 Applet 主类
│   ├── RunApplet.class      # AppletStub wrapper（本地补全，用于无浏览器运行）
│   ├── RunApplet.java       # wrapper 源码
│   ├── MTower.html / MTower.txt / Readme.txt
│   ├── data/ data2/ image/ himage/ midi/ wav/ au/ score/ savedat/
│   └── HowtoSaveJPN.html / HowtoSaveENG.html / Autoexec.bat
├── floor1_08_Java.png       # 第 1 层实机截图
└── README.md
```

## 运行方式

```bash
cd game
java RunApplet        # 用本地 wrapper 直接跑 Applet（820×520）
```

或浏览器打开 `MTower.html` 需 Java 插件支持（现代浏览器已不可用，推荐上面的 wrapper 方式）。

实测：OpenJDK 20，第 1 层正常（"Tower 1F"）。

## 备注

- 与 02/03 **地图布局完全相同**（左上楼梯、顶部 3 史莱姆、钥匙/药水/蝙蝠位置一一对应），但美术皮肤是 Java 版自有一套——同作者的同一地图数据、第三个呈现。
- `title.gif` 写明 "Magic Tower © 2001 Oz & Kenichi / © 1996 N.W"。

## 无头逻辑验证器（game/Headless8.java）

在 `MTower.class` 基础上做的「无延迟 / 无显示 / 无声音」纯逻辑驱动，秒级验证 PC98 模型算出的速通路线（`../01_PC98原版_mtower/tools/` 的 route_*.csv / keys_*.txt）。

| 文件 | 说明 |
|---|---|
| `game/Headless8.java` | 主驱动器：自建 AppletStub（哑巴音频 / BufferedImage 贴图），同步循环调 `paint()` 推进逻辑，按 keys 逐键驱动、对照 route csv 逐步校验 |
| `game/patch_twait.py` | 字节码补丁：`MTower.twait(int)` 的 `Thread.sleep` 段 nop 化（其余字节码与异常表原样，过校验），零延迟 |
| `game/MTower.class` | 已打补丁；`MTower.class.orig` 为原版备份 |
| `game/Probe8.java` / `Verify8.java` / `DumpAll8.java` | 开发期探针：空房间/瓦片属性 dump、单层复验、全量地图导出（`map_java8.json`） |
| `game/emul_log/verify_*.log` | 三条路线无头验证原始日志（证据） |

重建与运行：

```bash
cd game
python3 patch_twait.py        # MTower.class -> 零延迟（幂等，自动备份 .orig）
javac Headless8.java          # Applet 弃用警告可忽略
Xvfb :77 -screen 0 1024x768x24 &
DISPLAY=:77 java Headless8 <log> <keys.txt> <route.csv>
```

- keys：`u/d/l/r` 串，与 csv 步号一一对应；`H8_DEBUG=1` 开逐 tick 跟踪
- 消息框自动处理：ESC(27) 清 messageFlag（keyDown 偏移 1588 实证）；连按 6 次无进展反射清零 messageFlag/2/3（省流模式，只跳 UI 阻塞）
- 关键技术结论（字节码/实测依据）：
  1. 逻辑推进链 `paint() -> moveCharacter() -> pointCheck()`，角色在格中心才调 pointCheck；同步调 paint 即可驱动，不需要 timer 线程
  2. `OpenningZeno` 的 `createImage(640,400)` 需要 peer：反射 `Component.addNotify()` + 一个**不可见** Frame 父容器（否则 Applet 无 graphicsConfig，X11 peer 构造 NPE）；Frame 不可见故 AWT 不会并发发 paint，保确定性
  3. **3F 扒装剧本**：踩 3F(5,9) -> 过场 -> 空房间 -> **HP=400/ATK=10/DEF=10** -> 消息队列 -> 完成时英雄落 **2F(4,8)**（实测；旧推测 (3,8) 已纠正）、盗贼 obj87 在 2F(3,7)、2F(2,7) 挖通
  4. `mapObject[72][118]/[73][118]` 是勇者初始全局坐标槽（loadMapData 偏移 43814 写死 6/11），不是红钥匙数（终态 dump：当前已在 4F(11,10)，两槽仍为 6/11）
  5. `mapObject[71][118]` = 最深到达楼层（pointCheck 偏移 314-366：warp 时 `if (current - V >= 0) V = current`；实测 1,2,3,4,5 与楼层一一吻合，终态值 4 对应进入 4F）
  6. 钥匙计数不在 stage_flags（band5 slot9）状态块内：拾蓝钥前后全状态区 diff 仅 [69][117] 0→8、[70][124] 4→3 两格；因 4F 路线全程不开门无法反查，stats() 不再显示钥匙字段（诚实缺失）

已验证路线（2026-10-24，exit 0 全过，模型与实机逐步位置/属性全一致）：

| 路线 | 步数 | 终点 | HP/ATK/DEF | 金 |
|---|---|---|---|---|
| 进 4F | 78 | 4F(11,10) | 326/10/10 | 7 |
| 进 5F | 107 | 5F(2,11) | 652/10/10 | 10 |
| 5F 铁剑 | 141 | 5F(11,11) | 418/20/10 | 18 |
