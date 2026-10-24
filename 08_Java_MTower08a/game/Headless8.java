import java.applet.Applet;
import java.applet.AppletContext;
import java.applet.AppletStub;
import java.applet.AudioClip;
import java.awt.Event;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.lang.reflect.Array;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.List;

/**
 * 魔塔8(Java) 无延迟/无显示/无声音 纯逻辑验证器。
 *
 * 原理（读原著字节码得出）：
 *   - MTower implements Runnable，但 run() 只负责 repaint()；
 *     真正的逻辑推进在 paint() -> moveCharacter(gBuff) 链中。
 *   - moveCharacter 仅当 charaX/charaY %5==0（格中心静止）时才调 pointCheck(g)
 *     （拾取/开关门/剧本/战斗结算全在此），随后按 UpKey/currentKey 逐像素移动。
 *   => 不起窗口、不起 timer 线程，直接同步循环调 moveCharacter 即可零延迟驱动；
 *        声音经 AppletStub.getAudioClip 置空（哑巴 clip 防 NPE）；
 *        图像字段全部替换为离屏 BufferedImage（逻辑不依赖像素内容）。
 * 用法: java Headless8 <logfile> <keys_udlr> <routeCsv>
 *   keys: u/d/l/r（大写=按两次开门），与 csv 步号一一对应
 */
public class Headless8 {
  static Applet app;
  static PrintWriter LOG;
  static Method KEYDOWN, KEYUP, MOVECHARACTER, PAINT;
  static Event EV;
  static Graphics DUMMY;

  // ---------- AppletStub：零 X 依赖（图像返回 BufferedImage，声音返回哑巴 clip） ----------
  static class HeadlessStub implements AppletStub, AppletContext {
    public boolean isActive() { return true; }
    public URL getDocumentBase() { try { return new URL("file:."); } catch (Exception e) { return null; } }
    public URL getCodeBase() { try { return new URL("file:."); } catch (Exception e) { return null; } }
    public String getParameter(String n) { return null; }
    public AppletContext getAppletContext() { return this; }
    public void appletResize(int w, int h) {}
    public AudioClip getAudioClip(URL u) {
      return new AudioClip() { public void play() {} public void loop() {} public void stop() {} };
    }
    public Image getImage(URL u) { return new BufferedImage(32, 32, BufferedImage.TYPE_INT_RGB); }
    public Applet getApplet(String n) { return null; }
    public Enumeration<Applet> getApplets() {
      return new Enumeration<Applet>() { public boolean hasMoreElements() { return false; } public Applet nextElement() { return null; } };
    }
    public void showDocument(URL u) {}
    public void showDocument(URL u, String t) {}
    public void showStatus(String s) {}
    public void setStream(String k, java.io.InputStream s) {}
    public java.io.InputStream getStream(String k) { return null; }
    public Iterator<String> getStreamKeys() {
      return new Iterator<String>() { public boolean hasNext() { return false; } public String next() { return null; } public void remove() {} };
    }
  }

  // ---------- 字段访问 ----------
  static Field f(String n) { try { Field x = app.getClass().getDeclaredField(n); x.setAccessible(true); return x; } catch (Throwable t) { return null; } }
  static int gi(String n) {
    try { Field x = f(n); Object v = x.get(app);
      if (v instanceof Character) return (int) (char) (Character) v;
      if (v instanceof Boolean) return ((Boolean) v) ? 1 : 0;
      return ((Number) v).intValue(); } catch (Throwable t) { return 0; }
  }
  static int arrA(String fld, int r, int c) {
    try { Field x = f(fld); Object row = Array.get(x.get(app), r); Object e = Array.get(row, c);
      return (e instanceof Character) ? (int) (char) (Character) e : ((Number) e).intValue(); } catch (Throwable t) { return -1; }
  }
  static int cx() { return gi("charaX") / 5; }
  static int cy() { return gi("charaY") / 5; }
  static int fl() { return gi("mapY") * 10 + gi("mapX") + 1; }
  static void log(String m) { LOG.println(m); LOG.flush(); System.out.println(m); }

  static String stats() {
    return "f" + fl() + " (" + cx() + "," + cy() + ") HP=" + arrA("mapObject", 66, 118)
        + " ATK=" + arrA("mapObject", 67, 118) + " DEF=" + arrA("mapObject", 68, 118)
        + " G=" + arrA("mapObject", 69, 118)
        + " str=" + gi("strNumber");
  }

  /** 全量状态签名（稳定判据用） */
  static String sig() {
    return gi("charaX") + "," + gi("charaY") + "," + gi("mapX") + "," + gi("mapY")
        + "," + arrA("mapObject", 66, 118) + "," + arrA("mapObject", 67, 118) + "," + arrA("mapObject", 68, 118)
        + "," + arrA("mapObject", 69, 118) + "," + arrA("mapObject", 70, 118) + "," + arrA("mapObject", 71, 118) + "," + arrA("mapObject", 72, 118)
        + "," + gi("strNumber") + "," + gi("messageFlag") + "," + gi("messageFlag2") + "," + gi("dialogFlag")
        + "," + gi("attackFlag") + "," + gi("openningFlag") + "," + gi("yusyaFlag") + "," + gi("saidanFlag") + "," + gi("itemFlag");
  }

  /** 一帧逻辑推进（等价于 run() -> repaint() -> paint()：含加载/开场动画/moveCharacter） */
  static int tickOk = 0, tickErr = 0;
  static void tick() {
    try { PAINT.invoke(app, DUMMY); tickOk++; }
    catch (Throwable t) {
      tickErr++;
      if (tickErr <= 8) {
        Throwable c = t;
        while (c instanceof java.lang.reflect.InvocationTargetException && c.getCause() != null) c = c.getCause();
        log("  [tick异常#" + tickErr + "] " + c);
        StackTraceElement[] st = c.getStackTrace();
        for (int i = 0; i < Math.min(6, st.length); i++) log("      at " + st[i]);
      }
    }
  }

  /** 同步推进到状态稳定（连续 STABLE 帧签名不变） */
  static final int STABLE = 4;
  static int settle(int maxFrames) {
    String prev = null; int stable = 0, n = 0;
    while (n < maxFrames) {
      tick(); n++;
      String s = sig();
      if (DBG && n <= 14) log(String.format("      f%02d tick%02d cx=%d cy=%d chX=%d chY=%d R=%d cur=%d sv72=%d sv73=%d sig=%s",
          fl(), n, cx(), cy(), gi("charaX"), gi("charaY"), gi("RightKey"), gi("currentKey"),
          arrA("mapObject", 72, 118), arrA("mapObject", 73, 118), s));
      if (s.equals(prev)) { if (++stable >= STABLE) break; } else stable = 0;
      prev = s;
    }
    return n;
  }

  /** 有消息/对话/战斗动画在活动？（strNumber 常态>=0，不能作判据） */
  static boolean busy() {
    return gi("messageFlag") != 0 || gi("messageFlag2") != 0 || gi("dialogFlag") != 0
        || gi("attackFlag") != 0 || gi("openningFlag") != 0;
  }

  // ---------- 省流模式：剧情文案字段级跳过 ----------
  // 依据（读 keyDown 字节码）：ESC(27) 分支 offset 1588 `if(messageFlag) messageFlag=false`
  // 是消息框的正牌清除键；Enter(10) 在多数条件下也能清（offset 2170）。
  // 省流兜底：同一消息连按 ESC 无进展超过 SKIP_AFTER 次，直接反射清零消息字段
  // （与 ESC 的 putfield 效果等价，只跳 UI 阻塞，不动逻辑真值）。
  static final int SKIP_AFTER = 6;
  static int escStreak = 0;
  static void clearMessageFields() {
    for (String n : new String[]{"messageFlag", "messageFlag2", "messageFlag3"}) {
      Field x = f(n);
      if (x != null && x.getType() == boolean.class) {
        try { x.setBoolean(app, false); } catch (Throwable t) {}
      }
    }
  }

  static int CODE(char c) {
    switch (c) {
      case 'u': case 'U': case '8': return 56;   // 上
      case 'd': case 'D': case '2': return 50;   // 下
      case 'l': case 'L': case '4': return 52;   // 左
      case 'r': case 'R': case '6': return 54;   // 右
    }
    return 13;                                    // Enter
  }

  static boolean DBG = System.getenv("H8_DEBUG") != null;

  static void key(int code) {
    int rx0 = gi("RightKey"), lx0 = gi("LeftKey"), ux0 = gi("UpKey"), dx0 = gi("DownKey");
    try { KEYDOWN.invoke(app, EV, code); } catch (Throwable t) { log("  [keyDown异常] " + t); }
    tick();                                   // 至少推进一帧，让按键生效
    try { if (KEYUP != null) KEYUP.invoke(app, EV, code); } catch (Throwable t) { log("  [keyUp异常!] " + t); }
    if (DBG) log(String.format("    [key %d] 前(U%d D%d L%d R%d) 后(U%d D%d L%d R%d) cur=%d pos=(%d,%d)",
        code, ux0, dx0, lx0, rx0, gi("UpKey"), gi("DownKey"), gi("LeftKey"), gi("RightKey"), gi("currentKey"), cx(), cy()));
  }

  // ---------- 手动复刻 start() 的标志初始化（字节码 putfield 序列照抄） ----------
  static void initFlags() throws Exception {
    String[] zeros = {"yesnoNumber", "yesnoJudge", "mapFlagErase", "messageFlag", "messageFlag2", "messageFlag3",
        "yusyaFlag", "openningFlag", "saidanFlag", "menuFlag", "itemKeyFlag", "attackFlag", "scoreFlag",
        "saveFlag", "popupFlag", "UpKey", "DownKey", "LeftKey", "RightKey", "focusFlag", "countRepaint",
        "movingSkip", "paintSkip", "repaintSkip", "currentKey"};
    for (String n : zeros) { Field x = f(n); if (x != null) { if (x.getType() == boolean.class) x.setBoolean(app, false); else x.setInt(app, 0); } }
    String[] ones = {"inputKey", "mapFlagAll", "configFlag", "animaFlag"};
    for (String n : ones) { Field x = f(n); if (x != null) { if (x.getType() == boolean.class) x.setBoolean(app, true); else x.setInt(app, 1); } }
  }

  // ---------- 手动创建 start() 里的离屏缓冲（createImage 需要 peer，headless 下自建） ----------
  static void initBuffers() throws Exception {
    int[][][] sizes = { // {w,h} 按 start() 中的尺寸
        {}, {},
    };
    for (Field x : app.getClass().getDeclaredFields()) {
      if (Image.class.isAssignableFrom(x.getType()) && !x.getType().isArray()) {
        x.setAccessible(true);
        int w = 820, h = 520;
        String n = x.getName();
        if (n.contains("Map")) { w = 40; h = 40; }
        else if (n.equals("imgBuffCharaX")) { w = 80; h = 40; }
        else if (n.equals("imgBuffCharaY")) { w = 40; h = 80; }
        else if (n.equals("imgBuff2")) { w = 120; h = 120; }
        else if (n.equals("imgBuff3")) { w = 40; h = 40; }
        else if (n.equals("imgBuffopen")) { w = 820; h = 520; }
        else if (n.contains("Status")) { w = 520; h = 520; }
        x.set(app, new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB));
      }
    }
    for (Field x : app.getClass().getDeclaredFields()) {
      if (Graphics.class.isAssignableFrom(x.getType())) {
        x.setAccessible(true);
        Field img = f(x.getName().equals("gBuffopen") ? "imgBuffopen" : "imgBuff" + x.getName().substring(5));
        if (img != null && img.get(app) != null) {
          x.set(app, ((Image) img.get(app)).getGraphics());
        } else {
          x.set(app, new BufferedImage(820, 520, BufferedImage.TYPE_INT_RGB).getGraphics());
        }
      }
    }
    DUMMY = new BufferedImage(820, 520, BufferedImage.TYPE_INT_RGB).getGraphics();
  }

  // ---------- 声音静音（Stub 已返回哑巴 clip；此处兜底填 audio[]） ----------
  static void initAudio() throws Exception {
    Field x = f("audio");
    if (x == null) return;
    Object old = x.get(app);
    int len = old == null ? 8 : Array.getLength(old);
    AudioClip[] mute = new AudioClip[len];
    AudioClip m = new AudioClip() { public void play() {} public void loop() {} public void stop() {} };
    for (int i = 0; i < len; i++) mute[i] = m;
    x.set(app, mute);
  }

  static void dumpFloor(int flr) {
    int b = (flr - 1) / 10, s = (flr - 1) % 10;
    StringBuilder sb = new StringBuilder("  mapObject " + flr + "F\n");
    for (int y = 0; y < 13; y++) {
      for (int x = 0; x < 13; x++) sb.append(String.format("%5d", arrA("mapObject", b * 13 + y, s * 13 + x)));
      sb.append('\n');
    }
    log(sb.toString());
  }

  // ---------- 让 applet 获得 peer（createImage 的前提） ----------
  // 依据：OpenningZeno 偏移 7 `createImage(640,400)`，Component 无 peer 时返回 null
  // -> NPE（MTower.java:8154）。
  // 两步坑（实测）：
  //   1) JDK20 删了 Component.getPeer()，不能用它判活；
  //   2) Applet 无父容器时 getGraphicsConfiguration() 返回 null，X11 peer 构造直接 NPE
  //      （XWindow.initGraphicsConfiguration），必须先给它一个带 peer 的父容器。
  // 方案：建一个**不 setVisible** 的 Frame 作父（X11 窗口不映射，AWT 不会给 applet
  // 发 paint 事件，不干扰本驱动的同步 paint()），只反射调 addNotify 拿 peer。
  static void realizeApplet() throws Exception {
    java.awt.Frame fr = new java.awt.Frame("mt8-headless");
    fr.setSize(640, 400);
    fr.add(app);
    Method an = java.awt.Component.class.getDeclaredMethod("addNotify");
    an.setAccessible(true);
    an.invoke(fr);            // 父容器先拿 peer（不可见，不发重绘）
    an.invoke(app);           // applet 跟着拿 peer，graphicsConfig 从父继承
    log("[headless] applet displayable=" + app.isDisplayable() + "（createImage 可用前提）");
  }

  public static void main(String[] a) throws Exception {
    LOG = new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]), "UTF-8"));
    String keys = new String(Files.readAllBytes(Paths.get(a[1])), "UTF-8").trim();
    String csv = a[2];
    app = (Applet) Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new HeadlessStub());
    KEYDOWN = app.getClass().getMethod("keyDown", Event.class, int.class);
    try { KEYUP = app.getClass().getMethod("keyUp", Event.class, int.class); } catch (Throwable t) { KEYUP = null; }
    MOVECHARACTER = app.getClass().getMethod("moveCharacter", Graphics.class);
    PAINT = app.getClass().getMethod("paint", Graphics.class);
    EV = new Event(app, System.currentTimeMillis(), Event.KEY_PRESS, 0, 0, 0, 0);

    app.init();                 // 只加载数据（MediaTracker.waitForAll 对 BufferedImage 立即完成）
    realizeApplet();            // Xvfb 下获得 peer，使 OpenningZeno 的 createImage(640,400) 可用
    initFlags();
    initBuffers();
    initAudio();
    log("[headless] init 完成，贴图 imgCrop[100]=" + (f("imgCrop") != null && Array.get(f("imgCrop").get(app), 100) != null ? "就绪" : "缺失(不影响逻辑)"));

    // 过开场：按 Enter 直到 HP>0 且回到 1F(6,11)
    for (int i = 0; i < 30; i++) {
      key(13); settle(200);
      if (arrA("mapObject", 66, 118) > 0 && fl() == 1 && cx() == 6 && cy() == 11) break;
    }
    log("起点 " + stats());
    if (!(fl() == 1 && cx() == 6 && cy() == 11)) { log("!! 起点异常，应为 1F(6,11)"); LOG.close(); System.exit(3); }

    List<String> lines = Files.readAllLines(Paths.get(csv));
    List<int[]> rows = new java.util.ArrayList<>();
    for (String line : lines) {
      String[] p = line.split(",", -1);
      if (p.length > 3 && p[0].matches("\\d+")) rows.add(new int[]{Integer.parseInt(p[1]), Integer.parseInt(p[2]), Integer.parseInt(p[3])});
    }
    log("csv 目标点 " + rows.size() + " 按键数 " + keys.length());
    if (rows.size() != keys.length()) { log("!! 步数不一致"); LOG.close(); System.exit(4); }

    int lastF = 1;
    for (int i = 0; i < keys.length(); i++) {
      int step = i + 1;
      int[] t = rows.get(step - 1);
      char ch = keys.charAt(i), dir = Character.toLowerCase(ch);
      // 同步驱动：每步单按一次即完整走格/触发事件（开门 move 不移动、交谈 move 走上 NPC 格），
      // 不需要 np2kai 异步时代的"按两次"workaround。
      key(CODE(dir));
      settle(300);
      boolean ok = fl() == t[0] && cx() == t[1] && cy() == t[2];
      int tries = 0;
      String lastSig = sig();
      while (!ok && tries < 200) {
        // 消息框(messageFlag/2)：ESC(27) 是正牌清除键（keyDown offset 1588 实证）；
        // 过场(openningFlag)/对话框(dialogFlag)：Enter 推进；
        // 其余（战斗动画等）：方向键。
        int msg = gi("messageFlag") | gi("messageFlag2");
        if (msg != 0) {
          key(27);                                    // ESC 清消息
          escStreak++;
          if (escStreak >= SKIP_AFTER) {              // 省流兜底：字段级跳过剧情文案
            clearMessageFields();
            log("    [省流] 连按 ESC " + escStreak + " 次无进展，反射清零消息字段");
            escStreak = 0;
          }
        }
        else if (gi("openningFlag") != 0 || gi("dialogFlag") != 0) { key(13); escStreak = 0; }
        else { key(CODE(dir)); escStreak = 0; }
        settle(800);
        ok = fl() == t[0] && cx() == t[1] && cy() == t[2];
        tries++;
        String s = sig();
        if (!s.equals(lastSig)) escStreak = 0;        // 有进展就重置连击
        lastSig = s;
        if (DBG) log(String.format("    retry%d -> (%d,%d,%d) %s ev73=%d ev74=%d f3=%d op=%d str=%d msg=%d ok=%b",
            tries, fl(), cx(), cy(), stats(), arrA("mapObject", 73, 126), arrA("mapObject", 74, 126),
            gi("flag3F"), gi("openningFlag"), gi("strNumber"), gi("messageFlag"), ok));
      }
      if (!ok) {
        log("!! 第" + step + "步未达 目标=" + t[0] + "F(" + t[1] + "," + t[2] + ") 实际 " + stats());
        dumpFloor(fl());
        LOG.close(); System.exit(5);
      }
      String mark = (fl() != lastF) ? "  <<换层 " + lastF + "->" + fl() : "";
      log(String.format("%3d %c -> (%d,%d,%d) %s%s", step, ch, fl(), cx(), cy(), stats().replaceFirst("^f\\d+ \\S+ ", ""), mark));
      lastF = fl();
    }
    log("终 " + stats());
    // 状态区 dump（行 60-77 × 列 115-125）：用于核对钥匙等真实槽位
    {
      Field mo = f("mapObject");
      int moRows = mo == null ? 0 : Array.getLength(mo.get(app));
      Object row0 = moRows > 0 ? Array.get(mo.get(app), 0) : null;
      int cols = row0 == null ? 0 : Array.getLength(row0);
      log("  mapObject 维度 = " + moRows + "×" + cols);
      for (int r = 60; r < Math.min(moRows, 78); r++) {
        StringBuilder sb = new StringBuilder(String.format("  r%02d:", r));
        for (int c = 115; c <= 125; c++) sb.append(String.format("%4d", arrA("mapObject", r, c)));
        log(sb.toString());
      }
    }
    log("[headless] tick 成功 " + tickOk + " 异常 " + tickErr);
    LOG.close(); System.exit(0);
  }
}
