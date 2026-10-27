# 魔塔1 塔内全部对话 / 提示文案

按**出现楼层**编排：0F–50F 共 51 章，另加 1 章「无楼层归属」。机读版见 `magic_tower1_texts.csv`（保留原始 `floors` 字符串与 `group` 字段，共 309 行）。

**编排规则**

- 章题即楼层，条目本身不写「出现层」；
- 同层条目按 `[n]` 编号升序；
- 一条文案若在多层出现（怪物名、地形提示等多为此类），在每个对应楼层章各写一遍，内容完全相同；因此本文实际条目数（609）大于文案表行数（309）。
- 不挂地图数据、没有楼层概念的统一放在最后的「无楼层归属」章，同样按编号升序。

每条内容为两段：日文原文（`>` 引用块）与 `EN:` 英文译文。编号左侧是**引用方式**：

- `objN（数据引用）` / `地形N（数据引用）`——由对象表 / 地形表的 `ATR_STRING` 列挂上；
- `代码 strNumber=N ← 函数名`——由指令流里 `sipush N; putfield strNumber` 直接指定（开场与战后台词、钥匙不足、菜单确认等），这类文案不挂在地图数据上；
- `运行时按计算下标引用`——文案确实会在游戏里显示，但引用处的下标是算出来的（按楼层、分支、序号偏移），未能静态定位到引用点，故不猜楼层；

少数条目（怪物名、钥匙与道具取得提示等）的楼层除地图布点外，还依据「怪物图鉴登记」与「关卡旗标表」两路数据交叉核对，原始 `floors` 字段（含 `catalog` / `stage_flags` / `00F` 标记）见 `magic_tower1_texts.csv`。

原文的 12 个分组在正文里不再分章，编号索引如下（编号是文本表下标，与阅读顺序无关）：

- **无名提示与谜面（石板/老人语气，未具名）**（35）：2、3、18、22、53、55、56、61、62、64、65、66、67、69、71、72、73、75、76、78、79、80、81、82、83、84、85、91、98、208、215、266、280、283、296
- **盗贼（脱出屋）对白**（15）：4、5、6、7、16、17、24、25、26、29、30、44、59、68、99
- **具名人物台词（ゼノ・スケルトンＡ・バンパイア・大魔導師・老人・妖精・勇者…）**（35）：10、11、13、14、15、19、20、21、23、27、28、31、32、33、34、35、36、37、38、39、40、41、42、43、45、46、47、48、49、50、51、52、54、222、223
- **战斗与道具使用反馈提示**（30）：57、74、154、155、190、191、192、193、194、195、196、197、198、199、200、201、203、214、221、226、227、228、229、230、231、241、242、243、247、269
- **界面 · 系统文案（状态窗、情報、音、得分、称号）**（26）：58、77、185、186、187、188、189、207、209、211、212、213、216、217、218、219、220、225、233、234、235、236、237、238、239、240
- **道具 / 装备 / 钥匙：拾取与使用**（51）：60、133、134、135、142、147、148、149、151、152、153、156、157、158、159、160、161、162、163、164、165、166、167、168、169、171、172、173、174、175、176、177、178、179、180、181、182、205、252、254、255、256、257、258、259、260、261、262、263、264、265
- **地形与调查提示（门、楼梯、暗墙、熔岩、人物）**（17）：63、70、136、137、138、139、140、141、143、144、145、146、150、183、202、245、267
- **商人 · 祭坛 · 积分石 · 智慧之戒问答**（16）：86、87、88、89、90、92、93、94、95、96、204、206、210、224、297、298
- **存档 · 音效 · 版本等系统提示**（24）：97、184、246、248、249、250、251、253、268、281、282、284、285、286、287、288、289、290、291、292、293、294、295、314
- **怪物与 BOSS 名称**（34）：100、101、102、103、104、105、106、107、108、109、110、111、112、113、114、115、116、117、118、119、120、121、122、123、124、125、126、127、128、129、130、131、132、244
- **其它未归类文案**（1）：232
- **装备与道具名称（菜单用的短名）**（25）：270、271、272、273、274、275、276、277、278、279、299、300、301、302、303、304、305、306、307、308、309、310、311、312、313


### 0F

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[182]** obj113（数据引用）

> 幸運の金貨を手に入れた！敵が持っているＧＯＬＤ数が２倍になる。
>
EN: Got the Lucky Gold! You can get twice gold which monster has from now.

**[313]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 幸運の金貨
>
EN: The Lucky Gold

### 1F

**[100]** obj5（数据引用）

> Ｇスライム
>
EN: Green Slime

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[104]** obj8（数据引用）

> 僧　侶
>
EN: Priest

**[108]** obj9（数据引用）

> スケルトンＣ
>
EN: Skeleton C

**[109]** obj10（数据引用）

> スケルトンＢ
>
EN: Skeleton B

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[152]** obj26（数据引用）

> 飛翔のオーブを手に入れた！
>
EN: Got the orb of flying.

**[166]** obj11（数据引用）

> 赤い回復薬を手に入れた。生命力が５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 50 points up!

**[167]** obj12（数据引用）

> 青い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 200 points up!

**[168]** obj13（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が１ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 1 point up!

**[169]** obj14（数据引用）

> 青のクリスタルを手に入れた。防御力が１ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 1 point up!

**[301]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 飛翔のオーブ
>
EN: The orb of flying

### 2F

**[2]** 代码 `strNumber=2` ← eventMT

> 「・・・・・おい・・・」
>
EN: "------ Hey!"

**[3]** 代码 `strNumber=3` ← eventMT

> 「・・・・・おいっ！起きろ！」
>
EN: "------ Hey! Wake up!"

**[4]** obj87（数据引用）

> 盗賊「おお無事か！おまえ、ここの魔導師に捕まってこの牢屋に入れられてたんだよ。で、今まで気を失っていた訳だ。にしても、おまえ運がいいぜ。ちょうど抜け穴が完成したときに来るんだからな。そういう訳で俺は今から脱走するところだ。おまえもついてこい。」
>
EN: The thief says "What a relief you're okay!
　　 You were caught and thrown into this prison by the Magic Sergeant.
　　 You were unconscious when you got here.
　　 Nevertheless, you are so lucky that you just woke up.
　　 I've finished the escape tunnel. Let's break out."

**[5]** 代码 `strNumber=5` ← attackMonster/directCheck/pointCheck

> 盗賊「よし、じゃあ俺は先に行かせてもらうぜ。ああ、それからおまえの剣と盾、あいつらに取り上げられちまったみたいだな。この塔の中を丸腰で歩き回るのはやめた方がいい。確か５階に剣、９階に盾があったはずだから、まずそれを手に入れることを考えるんだな。じゃあ、またなっ！」
>
EN: The thief says "O.K. Well, excuse my going first. Your weapon and shield were stolen by the guards. It's not wise to wander about without them. I heard that there is a sword on the 5th floor and a shield on the 9th. You had better get them. See you!"

**[79]** obj151（数据引用）

> 「もう、話は終わりじゃ。」
>
EN: "I have done what I can. Good luck!"

**[80]** obj152（数据引用）

> 「おお、助けてくれてありがとうよ。お礼に、そなたの攻撃力と防御力を３％だけあげてやろう」（攻撃力と防御力が上がった!）
>
EN: "Oh, thank you for your help. I will raise your offensive and defensive power 3 percent as a token of my gratitude. [You begin feeling stronger]"

**[84]** obj173（数据引用）

> 「有効に使ってね!」
>
EN: "Please, use it wisely."

**[85]** obj174（数据引用）

> 「やあ、助けてくれてありがとう。少ないけれど、お礼にとっておいてくれ！」（１０００ＧＯＬＤもらった!）
>
EN: "Thank you for your help. Please accept money as a small token of my gratitude. (Got 1000 Gold.)"

**[107]** obj15（数据引用）

> 門番Ｂ
>
EN: Gate-Keeper B

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[167]** obj12（数据引用）

> 青い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 200 points up!

**[266]** 代码 `strNumber=266` ← eventMT

> 「・・・」
>
EN: "------"

### 3F

**[10]** obj177（数据引用）

> 魔導師ゼノ「ようこそ、『魔法の塔』へ。おまえがちょうど１００人目の侵入者だ。本来なら手下共に相手をさせるところだが、特別にこの私が自ら相手になってやろう。己の不運を呪うのだな。」
>
EN: The Magic Serg. Zeno says "Welcome to 'The Magic Tower'. You are the hundredth man who dared to enter my tower. You will now face my guards. Should you happen to survive, I will fight with you in person specially. You should accept your fate."

**[11]** obj178（数据引用）

> 勇者「なんだっ！？　うわ～っ！？」
>
EN: The brave man says "What? Oh!"

**[81]** obj153（数据引用）

> 「おぬしにこの勇者のオーブをさずけよう。これを持っていれば今いる階のモンスターの能力を調べてダメージを予測してくれるじゃろう。有効に使うのじゃ」
>
EN: "I will grant you the orb of the hero. It will forecast the results of fighting monsters on the current floor. Use it often."

**[100]** obj5（数据引用）

> Ｇスライム
>
EN: Green Slime

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[104]** obj8（数据引用）

> 僧　侶
>
EN: Priest

**[108]** obj9（数据引用）

> スケルトンＣ
>
EN: Skeleton C

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[166]** obj11（数据引用）

> 赤い回復薬を手に入れた。生命力が５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 50 points up!

**[167]** obj12（数据引用）

> 青い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 200 points up!

**[168]** obj13（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が１ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 1 point up!

**[169]** obj14（数据引用）

> 青のクリスタルを手に入れた。防御力が１ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 1 point up!

**[222]** 代码 `strNumber=222` ← eventMT

> 勇者「なんだと～！」
>
EN: The brave man says "What?"

**[223]** 代码 `strNumber=223` ← eventMT

> 勇者「あ～っ」
>
EN: The brave man says "Hey!"

**[299]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 勇者のオーブ
>
EN: The orb of the hero

### 4F

**[55]** obj175（数据引用）

> 「この塔には鍵で開けられる扉のほかに ”門” というものがあって、これはその門を守っているモンスターを倒さなければあかないじゃろう。」
>
EN: "There are doors which cannot be openned by a key. You can open these doors by beating the monsters which guard them."

**[100]** obj5（数据引用）

> Ｇスライム
>
EN: Green Slime

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[104]** obj8（数据引用）

> 僧　侶
>
EN: Priest

**[108]** obj9（数据引用）

> スケルトンＣ
>
EN: Skeleton C

**[109]** obj10（数据引用）

> スケルトンＢ
>
EN: Skeleton B

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[166]** obj11（数据引用）

> 赤い回復薬を手に入れた。生命力が５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 50 points up!

**[167]** obj12（数据引用）

> 青い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 200 points up!

**[168]** obj13（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が１ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 1 point up!

**[206]** obj22（数据引用）

> 「この祭壇に
>
EN: "If you offer me

### 5F

**[100]** obj5（数据引用）

> Ｇスライム
>
EN: Green Slime

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[104]** obj8（数据引用）

> 僧　侶
>
EN: Priest

**[109]** obj10（数据引用）

> スケルトンＢ
>
EN: Skeleton B

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[141]** obj89（数据引用）

> 壁がくずれた！
>
EN: The wall collapsed!

**[153]** obj25（数据引用）

> 知恵のオーブを手に入れた！
>
EN: Got the orb of wisdom.

**[156]** obj30（数据引用）

> 鉄の剣を手に入れた。攻撃力が１０ポイントアップ！
>
EN: Got an Iron Sword! Your offensive power was 10 points up!

**[166]** obj11（数据引用）

> 赤い回復薬を手に入れた。生命力が５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 50 points up!

**[169]** obj14（数据引用）

> 青のクリスタルを手に入れた。防御力が１ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 1 point up!

**[270]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 鉄の剣
>
EN: Iron

**[300]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 知恵のオーブ
>
EN: The orb of wisdom

### 6F

**[56]** obj42（数据引用）

> 「商人から物を買うと、あとで重要な情報を聞くことができるじゃろう。」
>
EN: "If you buy goods from merchants, you will be able to hear important information later."

**[86]** obj18（数据引用）

> 「紫の鍵を大特価の５０ＧＯＬＤで売るよ! 買わないかい?」
>
EN: "I will sell a blue key at very special price (50 gold)! Will you buy it?"

**[100]** obj5（数据引用）

> Ｇスライム
>
EN: Green Slime

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[104]** obj8（数据引用）

> 僧　侶
>
EN: Priest

**[108]** obj9（数据引用）

> スケルトンＣ
>
EN: Skeleton C

**[109]** obj10（数据引用）

> スケルトンＢ
>
EN: Skeleton B

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[166]** obj11（数据引用）

> 赤い回復薬を手に入れた。生命力が５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 50 points up!

**[169]** obj14（数据引用）

> 青のクリスタルを手に入れた。防御力が１ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 1 point up!

### 7F

**[87]** obj41（数据引用）

> 「鍵を５個セットで５０ＧＯＬＤで売るよ! 買わないかい?」
>
EN: "I will sell five keys for 50 Gold! Will you buy them?"

**[100]** obj5（数据引用）

> Ｇスライム
>
EN: Green Slime

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[104]** obj8（数据引用）

> 僧　侶
>
EN: Priest

**[108]** obj9（数据引用）

> スケルトンＣ
>
EN: Skeleton C

**[109]** obj10（数据引用）

> スケルトンＢ
>
EN: Skeleton B

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[166]** obj11（数据引用）

> 赤い回復薬を手に入れた。生命力が５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 50 points up!

**[167]** obj12（数据引用）

> 青い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 200 points up!

**[168]** obj13（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が１ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 1 point up!

### 8F

**[100]** obj5（数据引用）

> Ｇスライム
>
EN: Green Slime

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[104]** obj8（数据引用）

> 僧　侶
>
EN: Priest

**[106]** obj29（数据引用）

> 門番Ｃ
>
EN: Gate-Keeper C

**[108]** obj9（数据引用）

> スケルトンＣ
>
EN: Skeleton C

**[109]** obj10（数据引用）

> スケルトンＢ
>
EN: Skeleton B

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[135]** obj28（数据引用）

> 赤色の扉の鍵を手に入れた。
>
EN: Got a red key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[166]** obj11（数据引用）

> 赤い回復薬を手に入れた。生命力が５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 50 points up!

**[167]** obj12（数据引用）

> 青い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 200 points up!

**[168]** obj13（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が１ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 1 point up!

**[169]** obj14（数据引用）

> 青のクリスタルを手に入れた。防御力が１ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 1 point up!

### 9F

**[100]** obj5（数据引用）

> Ｇスライム
>
EN: Green Slime

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[104]** obj8（数据引用）

> 僧　侶
>
EN: Priest

**[108]** obj9（数据引用）

> スケルトンＣ
>
EN: Skeleton C

**[109]** obj10（数据引用）

> スケルトンＢ
>
EN: Skeleton B

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[141]** obj89（数据引用）

> 壁がくずれた！
>
EN: The wall collapsed!

**[161]** obj35（数据引用）

> 鉄の盾を手に入れた。防御力が１０ポイントアップ！
>
EN: Got an Iron Shield! Your defensive power was 10 points up!

**[166]** obj11（数据引用）

> 赤い回復薬を手に入れた。生命力が５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 50 points up!

**[168]** obj13（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が１ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 1 point up!

**[169]** obj14（数据引用）

> 青のクリスタルを手に入れた。防御力が１ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 1 point up!

**[275]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 鉄の盾
>
EN: Iron

### 10F

**[6]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 盗賊「ようっ！また会ったな。ここの門番を倒してくれて助かったぜ、ドジってまた捕まっちまってな。今度は、こんな奥の牢に閉じ込められちまった。まあ、それはそれとして、３５階にいるドラゴンの手前まで抜け穴を掘っといたんだ。開通させとくから先に行っててくれ。」
>
EN: The thief says "Ah, we meet again! Thank you. You beat the Gate-Keeper of this area. I was defeated and imprisoned again. Such a small prison this time. I'm making a secret tunnel in front of the Dragon. Go up to 35th floor and wait for me, while I complete the tunnel."

**[13]** 代码 `strNumber=13` ← eventMT

> スケルトンＡ「ふふふ、よくここまできたな。かくなる上はこの俺様がじきじき相手になってやる・・・といいたいところだが、まずは貴様の力を見せてもらうぞ！出会え！スケルトン兵士たちよ！」
>
EN: Skeleton A "Ha ha ha, You are lucky to have gotten so far. Since it has come to this, I shall fight with you personally, but first I must test your strength. Go and fight! Skeleton Soldiers!"

**[14]** 代码 `strNumber=14` ← eventMT

> スケルトンＡ「ほほう、なかなか・・・。だが、ここから先へは行かせん！ここで葬ってくれるわっ！さあ、こいっ！！！」
>
EN: Skeleton A "How considerably you do. But I will never let you pass. Here, you will die. Fight me!"

**[15]** 代码 `strNumber=15` ← eventMT

> スケルトンＡ「ううう・・・よくぞこの俺様を倒せたものだ・・・。しかし、これから先の階はこれまでとは比べものにならんほど強力な敵とワナが待っているぞ、せいぜい気を付けることだな・・・」
>
EN: Skeleton A "No, It's not possible! You may have defeated me, but beyond this point you must meet some enemies and snares that are powerful beyond anything you've seen. If careless, you will die!"

**[104]** obj8（数据引用）

> 僧　侶
>
EN: Priest

**[108]** obj9（数据引用）

> スケルトンＣ
>
EN: Skeleton C

**[109]** obj10（数据引用）

> スケルトンＢ
>
EN: Skeleton B

**[110]** obj16（数据引用）

> スケルトンＡ
>
EN: Skeleton A

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[167]** obj12（数据引用）

> 青い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 200 points up!

**[168]** obj13（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が１ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 1 point up!

**[169]** obj14（数据引用）

> 青のクリスタルを手に入れた。防御力が１ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 1 point up!

### 11F

**[102]** obj45（数据引用）

> Ｂスライム
>
EN: Big Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[105]** obj46（数据引用）

> 上級僧侶
>
EN: Superion Priest

**[111]** obj47（数据引用）

> 大バット
>
EN: Big Bat

**[112]** obj48（数据引用）

> ゾンビ
>
EN: Zombie

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[162]** obj36（数据引用）

> 銀の盾を手に入れた。防御力が２０ポイントアップ！
>
EN: Got a Silver Shield! Your defensive power was 20 points up!

**[254]** obj66（数据引用）

> 赤い回復薬を手に入れた。生命力が１００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 100 points up!

**[257]** obj76（数据引用）

> 青い回復薬を手に入れた。生命力が４００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 400 points up!

**[260]** obj80（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が２ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 2 points up!

**[276]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 銀の盾
>
EN: Silver

### 12F

**[59]** obj157（数据引用）

> 「９階と１６階と１８階の抜け穴には気が付いたかい？」
>
EN: "Did you notice the secret passages on the 9th, 16th, and 18th floors?"

**[88]** obj156（数据引用）

> 「希少品の赤い鍵を８００ＧＯＬＤで売るよ！買わないかい？」
>
EN: "I will sell the rare red key for 800 Gold! Will you buy it?"

**[102]** obj45（数据引用）

> Ｂスライム
>
EN: Big Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[105]** obj46（数据引用）

> 上級僧侶
>
EN: Superion Priest

**[111]** obj47（数据引用）

> 大バット
>
EN: Big Bat

**[112]** obj48（数据引用）

> ゾンビ
>
EN: Zombie

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[141]** obj89（数据引用）

> 壁がくずれた！
>
EN: The wall collapsed!

**[206]** obj22（数据引用）

> 「この祭壇に
>
EN: "If you offer me

**[254]** obj66（数据引用）

> 赤い回復薬を手に入れた。生命力が１００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 100 points up!

**[257]** obj76（数据引用）

> 青い回復薬を手に入れた。生命力が４００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 400 points up!

**[260]** obj80（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が２ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 2 points up!

**[263]** obj83（数据引用）

> 青のクリスタルを手に入れた。防御力が２ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 2 points up!

### 13F

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[160]** obj34（数据引用）

> 神　剣を手に入れた。攻撃力が１００ポイントアップ！
>
EN: Got a Sacred Sword! Your offensive power was 100 points up!

**[183]** obj79（数据引用）

> 溶岩が流れている。
>
EN: The lava is really hot.

**[274]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 神　剣
>
EN: Sacred

### 14F

**[102]** obj45（数据引用）

> Ｂスライム
>
EN: Big Slime

**[105]** obj46（数据引用）

> 上級僧侶
>
EN: Superion Priest

**[111]** obj47（数据引用）

> 大バット
>
EN: Big Bat

**[112]** obj48（数据引用）

> ゾンビ
>
EN: Zombie

**[113]** obj49（数据引用）

> ゾンビナイト
>
EN: Zombie Knight

**[114]** obj56（数据引用）

> ロック
>
EN: Rock

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[141]** obj89（数据引用）

> 壁がくずれた！
>
EN: The wall collapsed!

**[254]** obj66（数据引用）

> 赤い回復薬を手に入れた。生命力が１００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 100 points up!

**[263]** obj83（数据引用）

> 青のクリスタルを手に入れた。防御力が２ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 2 points up!

### 15F

**[7]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 盗賊「後でちゃんと行くから３５階まで先に行っておいてくれ。」
>
EN: The thief says "Don't worry, I'll be there."

**[17]** obj88（数据引用）

> 盗賊「よおっ！無事だったか？ここの大ダコが道をふさいでいて困っていたんだが今ようやく抜け穴が完成したんだ。おまえも、ここの大ダコを倒すのは後回しにした方がいいぜ。じゃあ、またなっ！」
>
EN: The thief says "Ah! Are you all right? The Big Octopus which lives in here was blocking my progress. Now a loophole has completed at last. You had better put off beating him. See you later!"

**[60]** obj160（数据引用）

> 「十字架を持っていれば、ゾンビやバンパイアに対する攻撃力が２倍になる。特にバンパイアは十字架を持っていないと倒せないだろう。これより上の階のどこかにあるらしいが……。」
>
EN: "If you carry a cross, the strength of Zombies and Vampires will be cut in half. It is near impossible to defeat them without a cross, especially Vampires. A cross is on a floor higher than this one."

**[90]** obj159（数据引用）

> 「紫の鍵を２００ＧＯＬＤで売るよ！買わないかい？」
>
EN: "I will sell a blue key for 200 Gold! Will you buy it?"

**[102]** obj45（数据引用）

> Ｂスライム
>
EN: Big Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[105]** obj46（数据引用）

> 上級僧侶
>
EN: Superion Priest

**[111]** obj47（数据引用）

> 大バット
>
EN: Big Bat

**[112]** obj48（数据引用）

> ゾンビ
>
EN: Zombie

**[113]** obj49（数据引用）

> ゾンビナイト
>
EN: Zombie Knight

**[118]** obj71（数据引用）

> 大ダコ
>
EN: Giant Octopus

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[244]** obj50、obj51、obj52 等5项（数据引用）

> 大ダコの一部
>
EN: some of Giant Octopus

**[257]** obj76（数据引用）

> 青い回復薬を手に入れた。生命力が４００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 400 points up!

**[263]** obj83（数据引用）

> 青のクリスタルを手に入れた。防御力が２ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 2 points up!

**[304]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> マトック
>
EN: The Magic Mattock

### 16F

**[16]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 盗賊「よっ！またあったな。すげえじゃねえか。ここのブロックのボスを倒すとはよ。俺もこれ以上、先の階へ行けなくて困ってたんだ。ああ、あと聞いた話だが、１１階に盾、１７階に剣があるそうだ。盾よりも剣の方を先に取りに行った方がいいそうだから、うまく敵をかわして剣を先に取りに行くんだな。じゃ、お先に！」
>
EN: The thief says "Hey! We meet again! How greatly you beat the boss of this area. It troubled me that I couldn't go upstairs any more. After I heard that there is a shield on the 11th floor and a sword on the 17th. You had better get a sword first and then a shield. Please excuse my going first!"

**[24]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 盗賊「あっ！まだ抜け穴、完成してなかったのに・・・もう少し待ってればアイテムを使わずにすんだはずだぞ。予定が狂っちまうな・・・いや、気にしないでくれ。」
>
EN: The thief says "The tunnel has not been completed yet. You should have waited a little longer, and you should not have used items. I had a bug in the program. There! Don't worry!"

**[25]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 盗賊「ああ、やっと抜け穴が完成した。あれ？またお前か。いいタイミングできたな。また抜け穴作っといたぜ。自由に使ってくれ。」
>
EN: The thief says "Oh, I have finished the tunnel. What? It's you again. You came at a good time. I have openned a tunnel, and you may use it freely."

**[61]** obj43（数据引用）

> 「このブロックでは赤い鍵は２ヶ所で手に入るそうじゃ。」
>
EN: "I heard that you can find a red key at two places in this area."

**[79]** obj151（数据引用）

> 「もう、話は終わりじゃ。」
>
EN: "I have done what I can. Good luck!"

**[82]** obj154（数据引用）

> 「やれやれ、見つかってしもうたか。褒美におぬしに”エリクサー”をやろう。この薬を使えば、その時の攻撃力と防御力に応じた値だけ生命力が回復するじゃろう。じゃから、当然、後の方で使う方が効果は大きいぞ。」
>
EN: "Thank goodness, you found me. I will give you an elixir as a symbol of my gratitude. Using this medicine will cause you to gain life according to your offensive and defensive power. So naturally, the later you use, the more it will have an effect on you."

**[102]** obj45（数据引用）

> Ｂスライム
>
EN: Big Slime

**[105]** obj46（数据引用）

> 上級僧侶
>
EN: Superion Priest

**[111]** obj47（数据引用）

> 大バット
>
EN: Big Bat

**[112]** obj48（数据引用）

> ゾンビ
>
EN: Zombie

**[113]** obj49（数据引用）

> ゾンビナイト
>
EN: Zombie Knight

**[114]** obj56（数据引用）

> ロック
>
EN: Rock

**[125]** obj95（数据引用）

> スライムマン
>
EN: Slime Man

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[141]** obj89（数据引用）

> 壁がくずれた！
>
EN: The wall collapsed!

**[254]** obj66（数据引用）

> 赤い回復薬を手に入れた。生命力が１００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 100 points up!

**[260]** obj80（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が２ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 2 points up!

**[263]** obj83（数据引用）

> 青のクリスタルを手に入れた。防御力が２ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 2 points up!

**[303]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> エリクサー
>
EN: The Magic Elixir

### 17F

**[102]** obj45（数据引用）

> Ｂスライム
>
EN: Big Slime

**[105]** obj46（数据引用）

> 上級僧侶
>
EN: Superion Priest

**[106]** obj29（数据引用）

> 門番Ｃ
>
EN: Gate-Keeper C

**[111]** obj47（数据引用）

> 大バット
>
EN: Big Bat

**[112]** obj48（数据引用）

> ゾンビ
>
EN: Zombie

**[113]** obj49（数据引用）

> ゾンビナイト
>
EN: Zombie Knight

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[157]** obj31（数据引用）

> 銀の剣を手に入れた。攻撃力が２０ポイントアップ！
>
EN: Got a Silver Sword! Your offensive power was 20 points up!

**[254]** obj66（数据引用）

> 赤い回復薬を手に入れた。生命力が１００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 100 points up!

**[257]** obj76（数据引用）

> 青い回復薬を手に入れた。生命力が４００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 400 points up!

**[260]** obj80（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が２ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 2 points up!

**[263]** obj83（数据引用）

> 青のクリスタルを手に入れた。防御力が２ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 2 points up!

**[271]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 銀の剣
>
EN: Silver

### 18F

**[62]** obj139（数据引用）

> 「このブロックでは、祭壇で攻撃力を何回か上げてもらわないとロックというモンスターが倒せなくなってしまうかもしれん。注意するのじゃ。」
>
EN: "In this area, if you don't raise your offensive power at an altar a few times, you may not be able to beat 'Rock' monsters. Be careful!"

**[102]** obj45（数据引用）

> Ｂスライム
>
EN: Big Slime

**[105]** obj46（数据引用）

> 上級僧侶
>
EN: Superion Priest

**[111]** obj47（数据引用）

> 大バット
>
EN: Big Bat

**[112]** obj48（数据引用）

> ゾンビ
>
EN: Zombie

**[113]** obj49（数据引用）

> ゾンビナイト
>
EN: Zombie Knight

**[114]** obj56（数据引用）

> ロック
>
EN: Rock

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[254]** obj66（数据引用）

> 赤い回復薬を手に入れた。生命力が１００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 100 points up!

**[260]** obj80（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が２ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 2 points up!

**[263]** obj83（数据引用）

> 青のクリスタルを手に入れた。防御力が２ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 2 points up!

### 19F

**[102]** obj45（数据引用）

> Ｂスライム
>
EN: Big Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[105]** obj46（数据引用）

> 上級僧侶
>
EN: Superion Priest

**[111]** obj47（数据引用）

> 大バット
>
EN: Big Bat

**[112]** obj48（数据引用）

> ゾンビ
>
EN: Zombie

**[113]** obj49（数据引用）

> ゾンビナイト
>
EN: Zombie Knight

**[114]** obj56（数据引用）

> ロック
>
EN: Rock

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[141]** obj89（数据引用）

> 壁がくずれた！
>
EN: The wall collapsed!

**[254]** obj66（数据引用）

> 赤い回復薬を手に入れた。生命力が１００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 100 points up!

**[260]** obj80（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が２ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 2 points up!

**[302]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 十字架
>
EN: A cross

### 20F

**[19]** 代码 `strNumber=19` ← eventMT

> バンパイア「ほほう、貴様か、スケルトンを倒して侵入してきた勇者というのは・・・だがこの私をスケルトン共のようなザコと一緒にするなよ。不死に等しいこの私の力を見せてやろう。さあ、こいっ！」
>
EN: Vampire "Well, You beat the skeletons and invaded. Never regard me as small like a skeleton. I will show you that I am as immortal as god. Hey, come on!"

**[20]** 代码 `strNumber=20` ← eventMT

> バンパイア「ううう・・・よもや、この私までもが敗れるとは・・・どうやら貴様の力は本物のようだな・・・だが、その程度では大魔導師様には絶対にかなわんぞ、せいぜい束の間勝利に酔いしれているがいい・・・」
>
EN: Vampire "Good god! I've never dreamed I'd be defeated. There is no doubt of your strength. But you will never win against the Great Magic Master as weak as you are. You shall only celebrate fleeting victory at most."

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[105]** obj46（数据引用）

> 上級僧侶
>
EN: Superion Priest

**[111]** obj47（数据引用）

> 大バット
>
EN: Big Bat

**[114]** obj56（数据引用）

> ロック
>
EN: Rock

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[166]** obj11（数据引用）

> 赤い回復薬を手に入れた。生命力が５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 50 points up!

**[257]** obj76（数据引用）

> 青い回復薬を手に入れた。生命力が４００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 400 points up!

**[260]** obj80（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が２ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 2 points up!

**[263]** obj83（数据引用）

> 青のクリスタルを手に入れた。防御力が２ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 2 points up!

### 21F

**[63]** obj140（数据引用）

> 「このブロックに、この魔法の塔の主である大魔導師がいるが、今のおまえさんでは戦っても死にに行くようなものじゃろう。とりあえず、うまくやりすごして上のブロックに行くのが正解じゃ。」
>
EN: "The Great Magic Master is in this area. He is a proprietor of this magic tower. At your strenght, to attack him means death. It stands to reason that you should not face him, but rather, get items on higher levels first."

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

### 22F

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

### 23F

**[53]** obj138（数据引用）

> 「わしが言うことは何もない。この階に、あるメッセージが隠されているじゃろう。」
>
EN: "I have nothing to say. A certain message may be hidden in this room."

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

### 24F

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

### 25F

**[21]** 代码 `strNumber=21` ← eventMT

> 大魔導師「・・・ジ・・・ユウシャ・・・・・コロス・・・」
>
EN: Great Magic Master "-K-I-L-L- -A-N- -I-N-V-A-D-E-R- "

**[126]** obj96（数据引用）

> 大魔導師
>
EN: Great Magic Master

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

### 26F

**[22]** 代码 `strNumber=22` ← eventMT

> 「・・・ジ・・・トキハキタレリ・・・エラバレシモノヨ、シヲオソレヌナラバジクウノモンヲクグリテ、ワガモトヘクルガヨイ・・・」
>
EN: "Now is the time. You were chosen. If you aren't afraid of Death, you should go through the gate of Time and Space, and come to me."

**[23]** obj44（数据引用）

> 勇者「これはっ……！人形だっ！」
>
EN: The brave man says "Oh! What? This is a doll!"

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[183]** obj79（数据引用）

> 溶岩が流れている。
>
EN: The lava is really hot.

### 27F

**[64]** obj141（数据引用）

> 「この階まで来た段階で、生命力１５００、攻撃力８０、防御力９８、鍵５個、紫の鍵が１個あれば、ほぼ理想的と言えるじゃろう。」
>
EN: "In the stage of this floor, if your strength is 1500, offensive power is 80, defensive power is 98, you have five keys, and one blue key, you are almost ideal."

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

### 28F

**[91]** obj161（数据引用）

> 「鍵１個を１００ＧＯＬＤで買うよ。鍵を売るかい？」
>
EN: "I will buy your keys at 100 Gold a piece. Will you sell me keys?"

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

### 29F

**[26]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 盗賊「このブロックに最後のボスと捕まったプリンセスがいるはずだが、今はまだ戦うのは早すぎるだろうな。」
>
EN: The thief says "The last boss and the captured princess must be in this area. Hmm, I wonder if we should wait before fighting him."

**[29]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 盗賊「おお、来たか。ちゃんと、抜け穴を開通させておいたぜ、この抜け穴を通ればドラゴンの後ろに出られるから、そこから上の階に行くんだな。」
>
EN: The thief says "There you are. I have just finished the tunnel. As you go through it, you will get to the Dragon. And then you should go up."

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

### 30F

**[100]** obj5（数据引用）

> Ｇスライム
>
EN: Green Slime

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[102]** obj45（数据引用）

> Ｂスライム
>
EN: Big Slime

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

### 31F

**[65]** obj142（数据引用）

> 「二刀流の剣士は攻撃力がものすごく高い。まともに戦えば大きなダメージを受けるだろう。一撃で倒せるようになるまで、戦わない方がよかろう。」
>
EN: "The offensive power of the swordsman who uses two swords is too high. He can use two swords at the same time. You will lose much strength if you fight him normally. You should never fight him before your attacks are stronger than his."

**[66]** obj163（数据引用）

> 「この塔は５０階建てだが、実際には４９階までしか行けないようだ。」
>
EN: "This tower is 50 stories high, but in reality it seems that you cannot go up to the 50th floor."

**[92]** obj162（数据引用）

> 「鍵を４個と紫の鍵をセットにして１０００ＧＯＬＤだ！買うかい？」
>
EN: "I will sell four keys and a blue key for 1000 Gold! Will you buy them?"

**[113]** obj49（数据引用）

> ゾンビナイト
>
EN: Zombie Knight

**[121]** obj91（数据引用）

> 騎　士
>
EN: Knight

**[122]** obj92（数据引用）

> 剣　士
>
EN: Swordsman

**[123]** obj93（数据引用）

> 兵　士
>
EN: Soldier

**[124]** obj94（数据引用）

> 死霊兵士
>
EN: Ghost Soldier

**[125]** obj95（数据引用）

> スライムマン
>
EN: Slime Man

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[255]** obj67（数据引用）

> 赤い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 200 points up!

**[258]** obj77（数据引用）

> 青い回復薬を手に入れた。生命力が８００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 800 points up!

**[261]** obj81（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が４ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 4 points up!

**[264]** obj84（数据引用）

> 青のクリスタルを手に入れた。防御力が４ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 4 points up!

### 32F

**[27]** 代码 `strNumber=27` ← eventMT

> 金騎士「貴様だな、第１、第２ブロックのボスを倒し登ってきた勇者というのは。だがそれも、ここで終わりだ！ここのブロックのボスである私が自ら貴様の首を上げてやるわっ！覚悟しろっ！」
>
EN: The Golden Knight says "You are a brave man beating the bosses of the first and second areas, and ascending the tower. But the game is over now. Here and Now, I will beat you for myself! Give up!"

**[28]** 代码 `strNumber=28` ← eventMT

> 金騎士「ううう……今回はこのぐらいにしておいてやる……４０階まで登ってこれたら今度は本気で相手をしてやるからなっ！覚えておけっ！」"
>
EN: The Golden Knight says "You think you're pretty strong, huh? If you can make it to the 40th floor, I shall fight with you again. There, you will die!

**[107]** obj15（数据引用）

> 門番Ｂ
>
EN: Gate-Keeper B

**[121]** obj91（数据引用）

> 騎　士
>
EN: Knight

**[123]** obj93（数据引用）

> 兵　士
>
EN: Soldier

**[124]** obj94（数据引用）

> 死霊兵士
>
EN: Ghost Soldier

**[125]** obj95（数据引用）

> スライムマン
>
EN: Slime Man

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[206]** obj22（数据引用）

> 「この祭壇に
>
EN: "If you offer me

**[258]** obj77（数据引用）

> 青い回復薬を手に入れた。生命力が８００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 800 points up!

**[261]** obj81（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が４ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 4 points up!

**[264]** obj84（数据引用）

> 青のクリスタルを手に入れた。防御力が４ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 4 points up!

### 33F

**[67]** obj143（数据引用）

> 「急がば回れじゃ。」
>
EN: "More haste, less speed."

**[113]** obj49（数据引用）

> ゾンビナイト
>
EN: Zombie Knight

**[122]** obj92（数据引用）

> 剣　士
>
EN: Swordsman

**[123]** obj93（数据引用）

> 兵　士
>
EN: Soldier

**[124]** obj94（数据引用）

> 死霊兵士
>
EN: Ghost Soldier

**[125]** obj95（数据引用）

> スライムマン
>
EN: Slime Man

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[158]** obj32（数据引用）

> 騎士の剣を手に入れた。攻撃力が４０ポイントアップ！
>
EN: Got a Sword of Knight! Your offensive power was 40 points up!

**[255]** obj67（数据引用）

> 赤い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 200 points up!

**[258]** obj77（数据引用）

> 青い回復薬を手に入れた。生命力が８００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 800 points up!

**[272]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 騎士の剣
>
EN: Knight

### 34F

**[100]** obj5（数据引用）

> Ｇスライム
>
EN: Green Slime

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[102]** obj45（数据引用）

> Ｂスライム
>
EN: Big Slime

**[103]** obj7（数据引用）

> バット
>
EN: Bat

**[121]** obj91（数据引用）

> 騎　士
>
EN: Knight

**[122]** obj92（数据引用）

> 剣　士
>
EN: Swordsman

**[123]** obj93（数据引用）

> 兵　士
>
EN: Soldier

**[124]** obj94（数据引用）

> 死霊兵士
>
EN: Ghost Soldier

**[125]** obj95（数据引用）

> スライムマン
>
EN: Slime Man

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[255]** obj67（数据引用）

> 赤い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 200 points up!

**[258]** obj77（数据引用）

> 青い回復薬を手に入れた。生命力が８００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 800 points up!

**[261]** obj81（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が４ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 4 points up!

**[264]** obj84（数据引用）

> 青のクリスタルを手に入れた。防御力が４ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 4 points up!

### 35F

**[30]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 盗賊「このブロックのボスの金騎士は弱いくせに態度だけはでかいから、この塔の副将格の魔導師ゼノには嫌われているらしい。」
>
EN: The thief says "The Golden Knight (who is the boss of this area) has a strong attitude in spite of being weak. It is for this reason that he is disliked by the Magic Serg. Zeno, who is the sub commander of this tower."

**[99]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 盗賊「ようまたあったな！無事だったか？これは聞いた話なんだが、２５階のボスを倒すと『時空の門』がどこかにできるらしいぞ。」
>
EN: The thief says "Ah!, we meet again! Thank goodness you're alive! I heard that if you beat the boss of 25th floor, 'the gate of time and space' will appear somewhere."

**[119]** obj74（数据引用）

> ドラゴン
>
EN: Dragon

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[141]** obj89（数据引用）

> 壁がくずれた！
>
EN: The wall collapsed!

**[310]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 雪の結晶
>
EN: The snow crystal

### 36F

**[68]** obj144（数据引用）

> 「この階の４つの抜け穴をうまく使えば、強い敵とは戦わずに上の階に行けるじゃろう。」
>
EN: "You may be able to go upstairs without fighting strong enemies, if you could use four tunnels skillfully in this floor."

**[113]** obj49（数据引用）

> ゾンビナイト
>
EN: Zombie Knight

**[121]** obj91（数据引用）

> 騎　士
>
EN: Knight

**[122]** obj92（数据引用）

> 剣　士
>
EN: Swordsman

**[123]** obj93（数据引用）

> 兵　士
>
EN: Soldier

**[124]** obj94（数据引用）

> 死霊兵士
>
EN: Ghost Soldier

**[125]** obj95（数据引用）

> スライムマン
>
EN: Slime Man

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[141]** obj89（数据引用）

> 壁がくずれた！
>
EN: The wall collapsed!

**[258]** obj77（数据引用）

> 青い回復薬を手に入れた。生命力が８００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 800 points up!

### 37F

**[69]** obj145（数据引用）

> 「この階の宝物庫にある宝を取るためにはマトックが必要じゃ。」
>
EN: "You need the mattock in order to get the treasure which is in the item warehouse on this floor."

**[121]** obj91（数据引用）

> 騎　士
>
EN: Knight

**[122]** obj92（数据引用）

> 剣　士
>
EN: Swordsman

**[123]** obj93（数据引用）

> 兵　士
>
EN: Soldier

**[124]** obj94（数据引用）

> 死霊兵士
>
EN: Ghost Soldier

**[125]** obj95（数据引用）

> スライムマン
>
EN: Slime Man

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[135]** obj28（数据引用）

> 赤色の扉の鍵を手に入れた。
>
EN: Got a red key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[174]** obj105（数据引用）

> 破壊の玉を手に入れた！
>
EN: Got the Destructible Ball!

**[255]** obj67（数据引用）

> 赤い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 200 points up!

**[258]** obj77（数据引用）

> 青い回復薬を手に入れた。生命力が８００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 800 points up!

**[261]** obj81（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が４ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 4 points up!

**[264]** obj84（数据引用）

> 青のクリスタルを手に入れた。防御力が４ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 4 points up!

**[305]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 破壊の玉
>
EN: The Destructible Ball

### 38F

**[70]** obj165（数据引用）

> 「門番のいる所には必ず門があるよ。逆に門のある階には、それを守っている敵がいるよ。だから……。」
>
EN: "There is never a gate without a Gate-Keeper. Conversely there are always enemies who keep the gate on floors that have gates. So,"

**[93]** obj164（数据引用）

> 「鍵３個を大サービスの２００ＧＯＬＤで売るよ！早い者勝ちだよ！」
>
EN: "I will sell three keys at special price (200 gold). First come, first served."

**[107]** obj15（数据引用）

> 門番Ｂ
>
EN: Gate-Keeper B

**[112]** obj48（数据引用）

> ゾンビ
>
EN: Zombie

**[121]** obj91（数据引用）

> 騎　士
>
EN: Knight

**[122]** obj92（数据引用）

> 剣　士
>
EN: Swordsman

**[123]** obj93（数据引用）

> 兵　士
>
EN: Soldier

**[124]** obj94（数据引用）

> 死霊兵士
>
EN: Ghost Soldier

**[125]** obj95（数据引用）

> スライムマン
>
EN: Slime Man

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[163]** obj37（数据引用）

> 騎士の盾を手に入れた。防御力４０がポイントアップ！
>
EN: Got a Shield of Knight! Your defensive power was 40 points up!

**[255]** obj67（数据引用）

> 赤い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 200 points up!

**[258]** obj77（数据引用）

> 青い回復薬を手に入れた。生命力が８００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 800 points up!

**[264]** obj84（数据引用）

> 青のクリスタルを手に入れた。防御力が４ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 4 points up!

**[277]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 騎士の盾
>
EN: Knight

### 39F

**[71]** obj146（数据引用）

> 「３時になれば空間移動の秘宝が現れるじゃろう。」
>
EN: "At three o'clock, the secret treasure that lets one travel in space will appear."

**[75]** obj169（数据引用）

> 「神盾は、魔法使いたちの魔法攻撃を防ぐ力があるらしい。……しかし、この盾は幻の階に隠されているそうだ。」
>
EN: "The sacred shield can defend you against magic attacks. But I heard this shield is hidden on a floor that doesn't exist."

**[94]** obj166（数据引用）

> 「紫の鍵が３個で２０００ＧＯＬＤだが、買うかい？」
>
EN: "2000 Golds for three blue keys. Deal?"

**[121]** obj91（数据引用）

> 騎　士
>
EN: Knight

**[122]** obj92（数据引用）

> 剣　士
>
EN: Swordsman

**[123]** obj93（数据引用）

> 兵　士
>
EN: Soldier

**[124]** obj94（数据引用）

> 死霊兵士
>
EN: Ghost Soldier

**[125]** obj95（数据引用）

> スライムマン
>
EN: Slime Man

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[255]** obj67（数据引用）

> 赤い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 200 points up!

**[261]** obj81（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が４ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 4 points up!

**[264]** obj84（数据引用）

> 青のクリスタルを手に入れた。防御力が４ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 4 points up!

**[306]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 空間転移の秘宝
>
EN: The Warp Staff

**[307]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 昇華の翼
>
EN: Wings to fly up

### 40F

**[31]** 代码 `strNumber=31` ← eventMT

> 金騎士「よくきたな。今度はさっきの様な訳にはいかんぞ！この屈辱は１０倍にして返してくれるわっ！死霊兵士突撃！」
>
EN: The Golden Knight says "I wonder how you were able to come so far. I will make sure you go no further. I will humiliate you 10 times as much as you've disgraced this tower. Ghost Soldiers, charge!"

**[32]** 代码 `strNumber=32` ← eventMT

> 金騎士「ふふん、こんなのは小手調べだっ！兵士突撃！」
>
EN: The Golden Knight says "Humph, that was nothing! Soldiers, charge!"

**[33]** 代码 `strNumber=33` ← eventMT

> 金騎士「まだまだ、これからっ！剣士突撃！」
>
EN: The Golden Knight says "We are only beginning. Let's fight from now on. Swordsmen, charge!"

**[34]** 代码 `strNumber=34` ← eventMT

> 金騎士「うぬぬ……だが、これはどうだっ！騎士突撃！」
>
EN: The Golden Knight says "Heck! How about this attack? Knights, charge!"

**[35]** 代码 `strNumber=35` ← eventMT

> 金騎士「うう……私の部下達を……許さんっ！許さんぞ！今度は手加減はしてやらんっ！覚悟しろ！」
>
EN: The Golden Knight says "How dare you defeat my followers? Never shall I forgive you! Now I won't use discretion. Give up!"

**[36]** 代码 `strNumber=36` ← eventMT

> 金騎士「ごほっ……今回はこのへんで……はあはあ……許しておいてやる……。だが次にやる時は今度こそ本当に本気で相手をしてやるからなっ！覚悟しておけっ！」
>
EN: The Golden Knight says "I will unwillingly forgive you this time. But we shall quarrel seriously when we meet again. You had better give up!"

**[37]** 代码 `strNumber=37` ← eventMT

> 金騎士「あっ……！ゼノ様……。あと一歩という所で、勇者を取り逃がしてしまいました。どうか、お許しを……。」
>
EN: The Golden Knight says "Oh! Sir Magic Serg. Zeno. I was not able to catch the brave man. Please forgive me."

**[38]** 代码 `strNumber=38` ← eventMT

> 魔導師ゼノ「取り逃がしただと……？逃げてきたのは貴様の方ではないかっ！この恥知らずめがっ！貴様のような臆病者はこの塔には不要だっ！ここで、死ねっ！」
>
EN: The Magic Serg. Zeno replies "You weren't? I dare you to say that again. You come running up here like a coward and tell me you couldn't do your job. What shame! This tower has no need for the likes of you! You've failed me for the last time. You shall now die."

**[39]** 代码 `strNumber=39` ← eventMT

> 金騎士「ああ、どうか、お許し……ぎゃあ～～～っ！！！」
>
EN: The Golden Knight says "Oh God, please forgive me! Ah!"

**[40]** 代码 `strNumber=40` ← eventMT

> 魔導師ゼノ「お見苦しいところをお見せしたな……。だが、安心してもらおう。私はこのようなゴミとはわけが違う。もし、お前が上まで登ってこれたなら今度は、私が直々にお相手しよう。待っているぞ……。」
>
EN: The Magic Serg. Zeno says "I behaved unbecomingly. But don't worry. I quite different from such a fellow. If you should come up to me, I would fight with you directly. I'm waiting for you."

**[120]** obj90（数据引用）

> 金騎士
>
EN: Golden Knight

**[121]** obj91（数据引用）

> 騎　士
>
EN: Knight

**[122]** obj92（数据引用）

> 剣　士
>
EN: Swordsman

**[123]** obj93（数据引用）

> 兵　士
>
EN: Soldier

**[124]** obj94（数据引用）

> 死霊兵士
>
EN: Ghost Soldier

**[125]** obj95（数据引用）

> スライムマン
>
EN: Slime Man

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[255]** obj67（数据引用）

> 赤い回復薬を手に入れた。生命力が２００ポイントアップ！
>
EN: Got a red elixir. Your vital power was 200 points up!

**[258]** obj77（数据引用）

> 青い回復薬を手に入れた。生命力が８００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 800 points up!

**[261]** obj81（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が４ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 4 points up!

**[264]** obj84（数据引用）

> 青のクリスタルを手に入れた。防御力が４ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 4 points up!

### 41F

**[116]** obj58（数据引用）

> 魔導師
>
EN: Magic Sergeant

**[127]** obj97（数据引用）

> 吸血コウモリ
>
EN: Vampire Bat

**[128]** obj98（数据引用）

> Ｋスライム
>
EN: SlimeLord

**[129]** obj99（数据引用）

> 魔術師Ａ
>
EN: Magician A

**[130]** obj100（数据引用）

> 魔術師Ｂ
>
EN: Magician B

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[141]** obj89（数据引用）

> 壁がくずれた！
>
EN: The wall collapsed!

**[256]** obj68（数据引用）

> 赤い回復薬を手に入れた。生命力が２５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 250 points up!

**[259]** obj78（数据引用）

> 青い回復薬を手に入れた。生命力が１０００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 1000 points up!

**[262]** obj82（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が５ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 5 points up!

**[265]** obj85（数据引用）

> 青のクリスタルを手に入れた。防御力が５ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 5 points up!

**[308]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 降臨の翼
>
EN: Wings to fly down

### 42F

**[73]** obj147（数据引用）

> 「魔術師は隣接すると魔法攻撃をしてくる。魔導師ははさまれると生命力を半分にする攻撃をしてくる。魔導師のはさみ攻撃は自分の生命力が高いほど受けるダメージが大きいはずじゃから気をつけてな。」
>
EN: "A Magician will attack using magic when he is next to you. The Magic Sergeants will attack and divide the vital power in half when you are caught between two. As for an attack on both sides from the Magic Sergeant, the stronger you are, the more damage you take. So, please be careful."

**[116]** obj58（数据引用）

> 魔導師
>
EN: Magic Sergeant

**[127]** obj97（数据引用）

> 吸血コウモリ
>
EN: Vampire Bat

**[128]** obj98（数据引用）

> Ｋスライム
>
EN: SlimeLord

**[129]** obj99（数据引用）

> 魔術師Ａ
>
EN: Magician A

**[130]** obj100（数据引用）

> 魔術師Ｂ
>
EN: Magician B

**[131]** obj101（数据引用）

> 黒騎士
>
EN: Dark Knight

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[135]** obj28（数据引用）

> 赤色の扉の鍵を手に入れた。
>
EN: Got a red key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[259]** obj78（数据引用）

> 青い回復薬を手に入れた。生命力が１０００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 1000 points up!

**[265]** obj85（数据引用）

> 青のクリスタルを手に入れた。防御力が５ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 5 points up!

### 43F

**[116]** obj58（数据引用）

> 魔導師
>
EN: Magic Sergeant

**[127]** obj97（数据引用）

> 吸血コウモリ
>
EN: Vampire Bat

**[128]** obj98（数据引用）

> Ｋスライム
>
EN: SlimeLord

**[129]** obj99（数据引用）

> 魔術師Ａ
>
EN: Magician A

**[130]** obj100（数据引用）

> 魔術師Ｂ
>
EN: Magician B

**[131]** obj101（数据引用）

> 黒騎士
>
EN: Dark Knight

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[164]** obj38（数据引用）

> 聖　盾を手に入れた。防御力が５０ポイントアップ！
>
EN: Got a Holy Shield! Your defensive power was 50 points up!

**[256]** obj68（数据引用）

> 赤い回復薬を手に入れた。生命力が２５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 250 points up!

**[259]** obj78（数据引用）

> 青い回復薬を手に入れた。生命力が１０００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 1000 points up!

**[278]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 聖　盾
>
EN: Holy

### 44F

**[132]** obj102（数据引用）

> 門番Ａ
>
EN: Gate-Keeper A

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[165]** obj39（数据引用）

> 神　盾を手に入れた。防御力が１００ポイントアップ！
>
EN: Got a Sacred Shield! Your defensive power was 100 points up!

**[256]** obj68（数据引用）

> 赤い回復薬を手に入れた。生命力が２５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 250 points up!

**[279]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 神　盾
>
EN: Sacred

### 45F

**[74]** obj148（数据引用）

> 「この塔の４４階は幻の階じゃ。普通の階段を登り降りしたのでは行くことができないらしい。ワープでもしないかぎり行くことは不可能じゃろう。」
>
EN: "The 44th floor in this tower is an illusion. It seems that we cannot go to there even if we use the stairs. I think that it is impossible to get there without teleporting."

**[75]** obj169（数据引用）

> 「神盾は、魔法使いたちの魔法攻撃を防ぐ力があるらしい。……しかし、この盾は幻の階に隠されているそうだ。」
>
EN: "The sacred shield can defend you against magic attacks. But I heard this shield is hidden on a floor that doesn't exist."

**[95]** obj168（数据引用）

> 「１０００ＧＯＬＤで生命力を２０００ポイント回復してあげるよ。」
>
EN: "I will increase your life 2000 points at 1000 Gold."

**[116]** obj58（数据引用）

> 魔導師
>
EN: Magic Sergeant

**[127]** obj97（数据引用）

> 吸血コウモリ
>
EN: Vampire Bat

**[128]** obj98（数据引用）

> Ｋスライム
>
EN: SlimeLord

**[129]** obj99（数据引用）

> 魔術師Ａ
>
EN: Magician A

**[130]** obj100（数据引用）

> 魔術師Ｂ
>
EN: Magician B

**[131]** obj101（数据引用）

> 黒騎士
>
EN: Dark Knight

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[176]** obj107（数据引用）

> 昇華の翼を手に入れた！
>
EN: Got wings to fly up!

**[259]** obj78（数据引用）

> 青い回復薬を手に入れた。生命力が１０００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 1000 points up!

**[262]** obj82（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が５ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 5 points up!

**[265]** obj85（数据引用）

> 青のクリスタルを手に入れた。防御力が５ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 5 points up!

**[307]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 昇華の翼
>
EN: Wings to fly up

### 46F

**[76]** obj149（数据引用）

> 「４１階は完全に左右対称になっておる。だから……。」
>
EN: "The 41st floor is perfectly symmetrical, and therefore,"

**[101]** obj6（数据引用）

> Ｒスライム
>
EN: Red Slime

**[108]** obj9（数据引用）

> スケルトンＣ
>
EN: Skeleton C

**[111]** obj47（数据引用）

> 大バット
>
EN: Big Bat

**[112]** obj48（数据引用）

> ゾンビ
>
EN: Zombie

**[121]** obj91（数据引用）

> 騎　士
>
EN: Knight

**[122]** obj92（数据引用）

> 剣　士
>
EN: Swordsman

**[123]** obj93（数据引用）

> 兵　士
>
EN: Soldier

**[127]** obj97（数据引用）

> 吸血コウモリ
>
EN: Vampire Bat

**[128]** obj98（数据引用）

> Ｋスライム
>
EN: SlimeLord

**[129]** obj99（数据引用）

> 魔術師Ａ
>
EN: Magician A

**[130]** obj100（数据引用）

> 魔術師Ｂ
>
EN: Magician B

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[180]** obj111（数据引用）

> 魔法の鍵を手に入れた！
>
EN: Got the magic key!

**[206]** obj22（数据引用）

> 「この祭壇に
>
EN: "If you offer me

**[256]** obj68（数据引用）

> 赤い回復薬を手に入れた。生命力が２５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 250 points up!

**[262]** obj82（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が５ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 5 points up!

**[311]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 魔法の鍵
>
EN: The magic key

### 47F

**[77]** obj171（数据引用）

> 「ドラゴンを倒す気なら、聖剣と聖盾、それにドラゴンスレーヤーを持って、なおかつレベルが高くなければならないだろう。」
>
EN: "If you want to beat the Dragon, you must have a holy sword, a holy shield, and a Dragon slayer, and also you must be high level."

**[96]** obj170（数据引用）

> 「超希少品のスーパーマトックを４０００ＧＯＬＤで買わないかい？」
>
EN: "Would you like to buy a super mattock (it's very rare) for 4000 Gold?"

**[127]** obj97（数据引用）

> 吸血コウモリ
>
EN: Vampire Bat

**[128]** obj98（数据引用）

> Ｋスライム
>
EN: SlimeLord

**[129]** obj99（数据引用）

> 魔術師Ａ
>
EN: Magician A

**[130]** obj100（数据引用）

> 魔術師Ｂ
>
EN: Magician B

**[133]** obj1（数据引用）

> 扉の鍵を手に入れた。
>
EN: Got a key.

**[134]** obj3（数据引用）

> 青色の扉の鍵を手に入れた。
>
EN: Got a blue key.

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[256]** obj68（数据引用）

> 赤い回復薬を手に入れた。生命力が２５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 250 points up!

**[262]** obj82（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が５ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 5 points up!

**[265]** obj85（数据引用）

> 青のクリスタルを手に入れた。防御力が５ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 5 points up!

**[312]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> スーパーマトック
>
EN: The Super Magic Mattock

### 48F

**[78]** obj150（数据引用）

> 「サイコロの５の目の形には、魔を封じ込める力があるという。このブロックのボスと戦う時には、このことを頭にいれておきなされ。」
>
EN: "It is said that the symbol of 5 on a pair of dice has the force of sealing magic. You had better memorize it till you fight the boss of this area."

**[116]** obj58（数据引用）

> 魔導師
>
EN: Magic Sergeant

**[127]** obj97（数据引用）

> 吸血コウモリ
>
EN: Vampire Bat

**[128]** obj98（数据引用）

> Ｋスライム
>
EN: SlimeLord

**[129]** obj99（数据引用）

> 魔術師Ａ
>
EN: Magician A

**[130]** obj100（数据引用）

> 魔術師Ｂ
>
EN: Magician B

**[131]** obj101（数据引用）

> 黒騎士
>
EN: Dark Knight

**[139]** 地形4、地形6、地形8 等47项（数据引用）

> 階段を上った。
>
EN: Went up the stairs.

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[159]** obj33（数据引用）

> 聖　剣を手に入れた。攻撃力が５０ポイントアップ！
>
EN: Got a Holy Sword! Your offensive power was 50 points up!

**[256]** obj68（数据引用）

> 赤い回復薬を手に入れた。生命力が２５０ポイントアップ！
>
EN: Got a red elixir. Your vital power was 250 points up!

**[259]** obj78（数据引用）

> 青い回復薬を手に入れた。生命力が１０００ポイントアップ！
>
EN: Got a blue elixir. Your vital power was 1000 points up!

**[262]** obj82（数据引用）

> 赤のクリスタルを手に入れた。攻撃力が５ポイントアップ！
>
EN: Got a red crystal. Your offensive power was 5 points up!

**[265]** obj85（数据引用）

> 青のクリスタルを手に入れた。防御力が５ポイントアップ！
>
EN: Got a blue crystal. Your defensive power was 5 points up!

**[273]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 聖　剣
>
EN: Holy

### 49F

**[129]** obj99（数据引用）

> 魔術師Ａ
>
EN: Magician A

**[131]** obj101（数据引用）

> 黒騎士
>
EN: Dark Knight

**[140]** 地形5、地形7、地形9 等46项（数据引用）

> 階段を下った。
>
EN: Went down the stairs.

**[309]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ドラゴンスレーヤー
>
EN: The Dragon Slayer

### 50F

**[41]** 代码 `strNumber=41` ← eventMT

> 魔導師ゼノ「よくぞ、ここまで、たどりついたものだ。誉めてやろう。約束どおり、この私が直々に相手をしよう。さあ、来るがいい。」
>
EN: The Magic Serg. Zeno "It's amazing that you found your way here at last. I compliment you. Now, as promised, I'll fight with you, man to man!"

**[42]** 代码 `strNumber=42` ← eventMT

> 魔導師ゼノ「うっ……この陣形は……まずいっ！」
>
EN: The Magic Serg. Zeno "Alas..."

**[43]** 代码 `strNumber=43` ← eventMT

> 勇者「おまえはっ……！どうしてこんな所に！」
>
EN: The brave man says "Who? It's you! Why are you in such a place ?"

**[44]** 代码 `strNumber=44` ← eventMT

> 盗賊「ふふふ……ここにいるという事は、答えは１つしかあるまい。こういう事だっ！」
>
EN: The thief says "Humph. There is only one reason why I'm here. And this is it!"

**[45]** 代码 `strNumber=45` ← eventMT

> 勇者「あっ！おまえはゼノッ！生きていたのか！？」
>
EN: The brave man says "Huh? Hey! You're Zeno! Were you still alive ?"

**[46]** 代码 `strNumber=46` ← eventMT

> 魔導師ゼノ「あんなことで倒されるものか。あれは、おまえの戦士としての知性を試したにすぎん。」
>
EN: The Magic Serg. Zeno says "I will never die. I merely tested your intelligence as a soldier."

**[47]** 代码 `strNumber=47` ← eventMT

> 勇者「なにっ！？……どういうことだっ！どうして、こんな事を……！？」
>
EN: The brave man says "Huh? What do you mean? Why did you do such a thing ?"

**[48]** 代码 `strNumber=48` ← eventMT

> 魔導師ゼノ「おまえの持つ神剣ウェポナー、そして私の持つ全能の杖インテリオン。この２つの力が合わさる時、偉大なる知恵を手に入れる事ができるという……。しかし、それには、その剣の力を十分に発揮できる能力を持った戦士が必要となるのだ。」
>
EN: The Magic Serg. Zeno says "The Sacred Sword 'Weaponer' which you have and The Omniscient Staff 'Intellion' which I have, Legend says that whoever unites the two will recieve great wisdom. But to this end, it must be assured that the soldier who does so can handle the the power of that sword."

**[49]** 代码 `strNumber=49` ← eventMT

> 勇者「その戦士が俺だというのか……！？」
>
EN: The brave man says "What are you saying... Am I the soldier ?"

**[50]** 代码 `strNumber=50` ← eventMT

> 魔導師ゼノ「そうだ……しかし、おまえの技量はその神剣ウェポナーを使いこなすには十分ではなかった。だから、私は偽りの情報を流し、様々なワナをこの塔にしかけ、おまえが来るのを待っていたのだ。そして、予定通り、おまえは神剣を扱うのに十分な力を身につけてここまで来た。」
>
EN: The Magic Serg. Zeno says "Yes. But when you came here, your ability wasn't sufficient to master the sacred sword 'Weaponer'."For that reason, I gave false information, set various traps in this tower, and waited for you to come. You came to here master the power enough to using the sacred sword as arranged beforehand.

**[51]** 代码 `strNumber=51` ← eventMT

> 勇者「では、姫がさらわれたという情報も、俺をここまで、おびき寄せる為のワナだったというのかっ！？」
>
EN: The brave man replies "Well, this means that the rumour that a princess was trapped here... was actually a lie in order to get me here, wasn't it ?"

**[52]** 代码 `strNumber=52` ← eventMT

> 魔導師ゼノ「その通りだ。そして、後は私がおまえの力を取りこめば、この茶番劇も終わりとなる……。時は来たれり……我全能なる力を用いて、神剣を砕き偉大なる知恵を手に入れん……。ゆくぞっ！神剣の戦士よ！」
>
EN: The Magic Serg. Zeno says "Yes, that's right. And now, if we can work together, this farce will end. Now is the time to act. Using omniscient power, We shall break the sacred sword and recieve great enlightenment. Soldier of the Sacred Sword! Let's finish this!"

**[54]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 魔導師ゼノ「ゴホッ！おのれ、この私が倒されるとは……、しかしこれぐらいで死ぬような私ではない！おぬしともう一度、戦う日が来ることを楽しみに待っているぞ！」
>
EN: The Magic Serg. Zeno says "You villain. Little did I expect to be beaten. But I would never die in such a way. I'll be looking forward to fighting with you again."

### 无楼层归属

余下这些条目没有楼层归属，按编号升序，共 122 条。原因分两类：

- 纯系统反馈——开关门、梯子/人物存在提示、钥匙不足、道具使用与伤害结算、存读档、音效开关、界面标签、评语与称号等，任何楼层都可能出现，没有「本层专属」的含义（含购买时余额不足的 [18]）；
- 挂在 obj40 / obj155 / obj167 / obj172 / obj17 上的 5 条（[57] [58] [72] [83] [89]）：这五个对象在 0F–50F 全部地图里没有任何落点（静态布点、`FLOOR_WRITES` 事件写入、`DYNEV` 动态投放三路都查过），文本在游戏里不会出现，属未使用条目。

**[18]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 「お金が足りないよ！」
>
EN: "You don't have enough money."

**[57]** obj40（数据引用）

> 「この塔は全部で５０階建てで、１０階ごとに１つのブロックを形成している。塔の内部には、各ブロックを統括するボスが配置されていて、そいつらを倒さないことには、それより上の階に行くことはできないだろう。」
>
EN: "This tower has fifty floor. Every ten floor form one area. The boss who controls each area, are posted in this tower. You cannot ascend from there if you don't beat them."

**[58]** obj155（数据引用）

> 「祭壇に寄進したときは、攻撃力よりも防御力を主に上げてもらった方がいいでしょう。ただし、攻撃力をまったく上げないと、あとで倒せない敵がでてくるかもしれないよ。」
>
EN: "When you offer gold at an alter, you may as well have your defensive power risen rather than your offensive power. The enemy whom you cannot beat may appear, provided you won't raise your offensive power."

**[72]** obj167（数据引用）

> 「この塔のどこかに、幸運の金貨というものがあって、それを持っていると敵を倒したときに得られるお金が２倍になるそうだ。」
>
EN: "There is a Lucky Gold somewhere in this tower. If you have it, you can get twice as much money when you beat an enemy."

**[83]** obj172（数据引用）

> 「もう、話す事はないよ。」
>
EN: "Be careful. I have nothing more to say."

**[89]** obj17（数据引用）

> 「うちの店は鍵をいくらでも売るよ。１つ１０００ＧＯＬＤだが買うかい？」
>
EN: "My store will sell as many keys as you need. They are 1000 Gold each. Will you buy them?"

**[97]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 表示する情報がありません。
>
EN: You don't have an informations any more.

**[98]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 「まいどーっ！」
>
EN: "Thank you very much."

**[115]** obj57（数据引用）

> 魔導師ゼノ
>
EN: Magic Serg. Zeno

**[117]** obj59（数据引用）

> バンパイア
>
EN: Vampire

**[136]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 扉が開いた。
>
EN: The door has opened.

**[137]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 青色の扉が開いた。
>
EN: The blue door has opened.

**[138]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 赤色の扉が開いた。
>
EN: The red door has opened.

**[142]** obj24（数据引用）

> 勇者のオーブを手に入れた！
>
EN: Got the orb of the hero.

**[143]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 老人がいる。
>
EN: You see an old man.

**[144]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 商人がいる。
>
EN: You see a merchant.

**[145]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 妖精がいる。
>
EN: You see a fairy.

**[146]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 盗賊がいる。
>
EN: You see a thief.

**[147]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 扉の鍵がない！
>
EN: Don't have the key.

**[148]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 青色の鍵がない！
>
EN: Don't have the blue key.

**[149]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 赤色の鍵がない！
>
EN: Don't have the red key.

**[150]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 階段がある。
>
EN: You see stairs.

**[151]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 飛翔のオーブは階段のとなりでなくては使えない！
>
EN: You must be near the stairs to use the orb of flying!

**[154]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 飛翔のオーブを使った！
>
EN: Used the orb of flying!

**[155]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 祭壇がある。
>
EN: You see an altar.

**[171]** obj103（数据引用）

> 十字架を手に入れた！バンパイア、ゾンビに対する攻撃力が２倍になった！
>
EN: Got a cross! Your offensive power against Vampires and Zombies has doubled.

**[172]** obj104（数据引用）

> エリクサーを手に入れた！
>
EN: Recieved the Magic Elixir.

**[173]** obj114（数据引用）

> マトックを手に入れた！
>
EN: Got the Magic Mattock.

**[175]** obj106（数据引用）

> 空間転移の秘宝を手に入れた！
>
EN: Got the Warp Staff!

**[177]** obj108（数据引用）

> 降臨の翼を手に入れた！
>
EN: Got wings to fly down!

**[178]** obj109（数据引用）

> ドラゴンスレーヤーを手に入れた！ドラゴンに対する攻撃力が２倍になった！
>
EN: Got the Dragon Slayer! Your attack power against the Dragon has doubled!

**[179]** obj110（数据引用）

> 雪の結晶を手に入れた！
>
EN: Got the snow crystal!

**[181]** obj112（数据引用）

> スーパーマトックを手に入れた！
>
EN: Got the Super Magic Mattock!

**[184]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> この階にいるモンスターの生命力、攻撃力、防御力、プレーヤーの受けるダメージを検索
>
EN: Looking up the results of battling these monsters.

**[185]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 命
>
EN: Vital power:

**[186]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 攻
>
EN: Offensive power:

**[187]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 防
>
EN: Defensive power:

**[188]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 予想ダメージ
>
EN: Expected damage:

**[189]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 攻撃不可能
>
EN: Attack is impossible!

**[190]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> エリクサーを使った！生命力が
>
EN: Used the Magic Elixir. Your vital power was

**[191]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> マトックを使った！四方の壁が崩れた！
>
EN: Used the Magic Mattock! The walls fell down!

**[192]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 破壊の玉を使った！四方の敵が倒れた！
>
EN: Used The Destructible Ball! Enemies on all sides died!

**[193]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 空間転移した！
>
EN: Warped!

**[194]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 昇華の翼を使った！
>
EN: Used the wing to fly up!

**[195]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 降臨の翼を使った！
>
EN: Used the wing to fly down!

**[196]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 雪の結晶を使った！
>
EN: Used the snow crystal!

**[197]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 魔法の鍵を使った！この階の扉がすべて開いた！
>
EN: Used the Magic Key! All these doors opened on this floor.

**[198]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> スーパーマトックを使った！この階の壁がすべて崩れた！
>
EN: Used the Super Magic Mattock! All the walls fell down on this floor!

**[199]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 転送先に障害物があって空間転移ができない！
>
EN: Can't warp (There's an object in the way).

**[200]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 上の階に障害物があって転移ができない！
>
EN: Can't go upstairs (it's blocked)!

**[201]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 下の階に障害物があって転移ができない！
>
EN: Can't go downstairs (it's blocked)!

**[202]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 溶岩が固まって道ができた！
>
EN: The lava cooled and turned to stone.

**[203]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> をたおした！
>
EN: You've beat

**[204]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ＧＯＬＤを
>
EN: . Recieved

**[205]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 枚手に入れた！
>
EN: Gold.

**[207]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ＧＯＬＤ寄進すれば望みをかなえてやろう。寄進するか？」
>
EN: Gold, I will grant your request. Will you?"

**[208]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 「どの望みをかなえて欲しいのだ？」
>
EN: "What option shall you choose?"

**[209]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ・生命力を
>
EN: Your life recovers by

**[210]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ポイント回復
>
EN: points.

**[211]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ・攻撃力を
>
EN: The offensive power is raised

**[212]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ポイントアップ
>
EN: points.

**[213]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ・防御力を
>
EN: The defensive power is raised

**[214]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ・やっぱりやめる
>
EN: Then I won't do it after all.

**[215]** 代码 `strNumber=215` ← saidan

> 「金がたらん！」
>
EN: "You don't have enough money!"

**[216]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 塔
>
EN: Tower

**[217]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 階
>
EN: F

**[218]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 生命力
>
EN: Life

**[219]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 攻撃力
>
EN: Offense

**[220]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 防御力
>
EN: Defense

**[221]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 相手の防御力が高すぎて攻撃ができない！
>
EN: You can't battle him. Because his defensive power is too high!

**[224]** obj69（数据引用）

> 「この階までのあなたの生命力、防御力、攻撃力、鍵の個数からあなたの実力を評価すると・・・
>
EN: "Judging by your vital power, offensive power, defensive power, and number of keys, you have

**[225]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 点です。
>
EN: points.

**[226]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> うーん、この点数だとこれから先へ進むのは、かなり無理があるでしょう。」
>
EN: If you have that many points, you might want to reconsider going higher..."

**[227]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> いまひとつですね。これから先はかなり苦戦するでしょう。」
>
EN: A bit below average. Maybe you should try harder."

**[228]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> まあまあですね。この点数ならこれから先もなんとかなるでしょう。」
>
EN: You are ordinary. You might get by okay!"

**[229]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> なかなかのものです。もう少し頑張れば称号を差し上げましょう。」
>
EN: Doing fine! If you wish to continue, I will give you a special rank..."

**[230]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> おめでとう！満点です。
>
EN: Congratulations! Your score is GREAT!

**[231]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> よくがんばりましたね。
>
EN: Do you wish to go on?

**[232]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> あなたには
>
EN: I give you the special rank of

**[233]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 『戦士』
>
EN: FIGHTER

**[234]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 『勇者』
>
EN: BRAVE MAN

**[235]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 『英雄』
>
EN: HERO

**[236]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 『剣帝』
>
EN: SWORD EMPEROR

**[237]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 『闘神』
>
EN: FIGHTER GOD

**[238]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> の称号を差し上げましょう。
>
EN: .

**[239]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> これから先もこの調子でね。」
>
EN: You may as well play as good as you have from this point on."

**[240]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ここまでおつかれさまでした。」
>
EN: It was nice fight so far."

**[241]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 魔術師Ａの魔法攻撃だ！生命力が２００ポイント減少！
>
EN: Your vital power decreased 200 points by magic attack of Magician A!

**[242]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 魔術師Ｂの魔法攻撃だ！生命力が１００ポイント減少！
>
EN: Your vital power decreased 100 points by magic attack of Magician B!

**[243]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 魔導師の魔法攻撃だ！生命力が半減！
>
EN: Your vital power decreased in half by the magic attack of Magic Master!

**[245]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 道が壁に変わった！
>
EN: The road changed to the wall!

**[246]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> セーブデータがありません。
>
EN: Nobody saved that game yet.

**[247]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 階段を移動中
>
EN: You are using the stairs.

**[248]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> おめでとう！得点が第
>
EN: Congratulations! You win the

**[249]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 位の成績でした。
>
EN: place with the points which you got.

**[250]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> データをロード(読み込み)しました。
>
EN: Loaded the Game.

**[251]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> データをセーブ(保存)しました。
>
EN: Saved the Game.

**[252]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 鍵を持ってないよ！
>
EN: You don't have a key!

**[253]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> このデータはロードできません。
>
EN: This Game can't load.

**[267]** 地形116、地形117（数据引用）

> 0
>
EN: 0

**[268]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> Magic Tower Ver0.8a

**[269]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ドラゴンが火を吹いた！生命力が１０００ポイント減少！
>
EN: Dragon blew on the fire! Your vital power decreased 1000 points.

**[280]** 代码 `strNumber=280` ← eventMT

> 「生命力がなくなりました。再挑戦してください。」
>
EN: "You have perished in Magic Tower. Please try again!"

**[281]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 上書きします。よろしいですか？
>
EN: Over write. Is it true ?

**[282]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 情報番号
>
EN: Information No.

**[283]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 「願いをかなえたぞ！」
>
EN: "Your wish came true."

**[284]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 実行中...
>
EN: Executing...

**[285]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> セーブできません。ポリシーツールで入出力の設定をして下さい。
>
EN: Can't save this game. Please set by policytool.

**[286]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ランキングデータを初期化しました。
>
EN: Initialized Ranking data.

**[287]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ランキングデータを初期化できません。ポリシーツールで入出力の設定をして下さい。
>
EN: Can't initialize this raning data. Please set by policytool.

**[288]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> このデータはロードできません。
>
EN: This data can't load.

**[289]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> Wav サウンドオン！
>
EN: Wav sound on.

**[290]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> Midiバックグラウンドミュージックオン！
>
EN: Midi Background music on.

**[291]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> サウンドオフ！　ＢＧＭオフ！
>
EN: Sound and Background music off.

**[292]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> サウンドオフ！
>
EN: Sound off.

**[293]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> バックグラウンドミュージックオフ！
>
EN: Background music off.

**[294]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> Au サウンドオン！
>
EN: Au sound on.

**[295]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> Auバックグラウンドミュージックオン！
>
EN: Au Background music on.

**[296]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> 「遊んでくれてありがとう！　まだ完成できていません。　楽しみに待っていてね！」
>
EN: "Thank you for playing this game. Please wait for completing."

**[297]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ポイント回復
>
EN: points up!

**[298]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> ＧＯＬＤを
>
EN: Got

**[314]** 运行时按计算下标引用（未在静态数据/常量赋值中定位）

> アイテムを使用します。よろしいですか？
>
EN: Do you use this item?
