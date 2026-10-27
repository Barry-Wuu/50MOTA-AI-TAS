# MTower.class 反编译源码（CFR）

`MTower.java` 由 `game/MTower.class` 反编译得到，用于查「某句文案在什么条件下、被写到哪一格」。

```bash
curl -sSL -o cfr.jar https://repo1.maven.org/maven2/org/benf/cfr/0.152/cfr-0.152.jar
java -jar cfr.jar game/MTower.class --outputdir decompiled
```

用途举例（都已在 `01_PC98原版_mtower/magic_tower1_texts.md` 里落实）：

- 商店成交后把所在格改写成后续 NPC：`mapObject[YpBuff][XpBuff] = 40 / 155 / 157 / 160 / 163 / 165 / 169 / 171`；
- 对话结束统一换成「もう話す事はないよ」的 `172`；
- 12F(11,1) 破墙后揭示的鍵屋 `17`；
- 余额不足时商店共用 `strMessage[..][18]`。

注意：源码里的 `char` 常量会以 `'\uXXXX'` 形式出现（如 `'\u009b'` = 155），查数值时容易漏。
