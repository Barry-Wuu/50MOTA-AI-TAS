# flash/ — 魔塔50层 Flash 汉化原版

## 文件

| 文件 | 大小 | SHA-256 |
|---|---|---|
| `mota50.swf` | 237,139 B（0.226 MB） | `48b6d47f2b07c9d422cc42fbbee71ab7b8a6bd5368843a9008936f8cd70d76ea` |

## SWF 规格

| 项 | 值 |
|---|---|
| 格式 | CWS（zlib 压缩） |
| SWF 版本 | 6（Flash 6，2004 年） |
| 解压后体积 | 532,439 B |
| Stage | 640 × 420 |
| 帧率 | 18 FPS |
| Tag 总数 | 3,460 |
| 主要 Tag | DefineShape ×164、DefineSprite ×142、DefineBitsLossless2 ×142、DefineSound ×7、DefineEditText ×34、DefineButton2 ×18 |

关键内部符号（证明为魔塔本体）：`FloorNo`、`DownFloorNo`、`EndFloorNo`、`KeyYellow`、`KeyBlue`、`KeyRed`、`KeyMagic`、`CowryKeyMagic_mc`、`HP`、`Defense`、`EnemyDefense_txt`、`Def_Enemy_array`。

## 来源

### 为什么不是 4399

4399 页面 `https://www.4399.com/flash/19783_1.htm` 的 `_strGamePath` 指向 `/upload_swf/ftp/20091114wen/12.swf`，实际 HTTP 抓取该文件得 **23,832 B**，不足页面标注 “0.23M” 的十分之一。

解析其 SWF tag 结构后确认该文件是**下架占位壳**：只有 2 个 `DefineButton2` + 2 个 `DefineEditText` + 1 个 `SymbolClass`，零 `DefineSound`；AS3 符号表内仅有 `homeBtn`、`getURLHandle`、`getBrowserName`、`http://www.4399.com/`、`window.open`——点击即跳回 4399 首页。4399 已将该游戏下架并替换 SWF，同期魔塔 50 层的其他页面（`82578` 改进版、`82589` 无敌版、`19764`、`19765`）现全部 404。

### 实际来源

采用 2004 年 Flash 作者发布站的历史原始地址（新浪游戏大厅）：

```
http://image2.sina.com.cn/gm/downgames/littlegame/U153P115T33D775F646DT20041125152518.swf
```

HTTP 200，`Content-Length: 237139`，`Content-Type: application/x-shockwave-flash`。

**与 4399 标注的吻合度**：237,139 / 1024 / 1024 = 0.226 MB，即 4399 页面显示的 “0.23M”。同一款文件，4399 只是把它换掉了。

## 版本定位（无魔改）

按 HTML5 魔塔广场（h5mota.com）社区对【50层魔塔原版】的主流定义，2004 年 50 层魔塔 Flash 汉化版即公认原版基线（该定义依据为复刻版累计游玩量约 75 万人次，断崖式领先）。

本文件为该原版本身，未做任何修改：

- 保留原版三大远古特性：对话穿墙、破墙偷雪花、圣水复活
- 不含 36 层暗道与 48 层魔法警卫（原版即无，非删减）
- 自带疯狂加血模式（原版内置，非外挂改版）

未发现无敌、加血上限、金币 99999、改地图、改怪物数值等任何魔改痕迹。

## 运行验证

Ruffle 0.7.1-stable 实测：

```
ruffle.exe -g gl --no-gui --width 640 --height 420 --storage memory mota50.swf
```

日志：`Loaded SWF version 6, resolution 640x420 @ 18 FPS`，无错误。唯一警告是 `Unknown device font "宋体"`，Ruffle 自动 fallback，不影响显示。

## 校验方式

```bash
curl -s -H "private-token: <token>" \
  "https://gitcode.com/api/v5/repos/Barry_Wu_/50MOTA-AI-TAS/contents/flash/mota50.swf?ref=main" \
  | python -c "import sys,json,base64;print(len(base64.b64decode(json.load(sys.stdin)['content'])))"
# 应输出 237139
```
