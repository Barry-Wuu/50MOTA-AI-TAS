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
