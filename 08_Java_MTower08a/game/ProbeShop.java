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
 * 一次性探针：实测 7F(6,1) 商人 obj41「鍵を５個セットで５０ＧＯＬＤ」的购买交互。
 * 流程：1F→5F 铁剑(141步)→6F→7F(106步)，反射清零 7F 黄/蓝门（绕钥匙死锁），
 * 走到商人 (6,1) 面前撞上去，逐键试探（Enter/空格/ESC/y），每步 dump 状态区。
 * 目的：确定 ①购买按键 ②买到什么颜色的钥匙×几 ③钥匙计数槽位 ④金币扣哪个槽。
 */
public class ProbeShop {
  static Applet app;
  static PrintWriter LOG;
  static Method KEYDOWN, KEYUP, PAINT;
  static Event EV;
  static Graphics DUMMY;

  static class Stub implements AppletStub, AppletContext {
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
  static void setArr(String fld, int r, int c, int v) {
    try { Field x = f(fld); Object row = Array.get(x.get(app), r);
      if (row instanceof char[]) Array.setChar(row, c, (char) v);
      else Array.setInt(row, c, v); } catch (Throwable t) { log("  [setArr失败] " + t); }
  }
  static int cx() { return gi("charaX") / 5; }
  static int cy() { return gi("charaY") / 5; }
  static int fl() { return gi("mapY") * 10 + gi("mapX") + 1; }
  static void log(String m) { LOG.println(m); LOG.flush(); System.out.println(m); }

  static String stats() {
    return "f" + fl() + " (" + cx() + "," + cy() + ") HP=" + arrA("mapObject", 66, 118)
        + " ATK=" + arrA("mapObject", 67, 118) + " DEF=" + arrA("mapObject", 68, 118)
        + " G=" + arrA("mapObject", 69, 118) + " str=" + gi("strNumber");
  }

  static String flags() {
    return String.format("msg=%d/%d dlg=%d atk=%d op=%d yusya=%d saidan=%d item=%d/%d itemKey=%d yesno=%d/%d",
        gi("messageFlag"), gi("messageFlag2"), gi("dialogFlag"), gi("attackFlag"), gi("openningFlag"),
        gi("yusyaFlag"), gi("saidanFlag"), gi("itemFlag"), gi("itemNUM"), gi("itemKeyFlag"),
        gi("yesnoNumber"), gi("yesnoJudge"));
  }

  static String sig() {
    return gi("charaX") + "," + gi("charaY") + "," + gi("mapX") + "," + gi("mapY")
        + "," + gi("strNumber") + "," + gi("messageFlag") + "," + gi("messageFlag2") + "," + gi("dialogFlag")
        + "," + gi("itemFlag") + "," + gi("itemNUM") + "," + gi("yesnoNumber") + "," + gi("attackFlag")
        + "," + arrA("mapObject", 69, 118) + "," + arrA("mapObject", 70, 118) + "," + arrA("mapObject", 71, 118);
  }

  static int tickOk = 0, tickErr = 0;
  static void tick() {
    try { PAINT.invoke(app, DUMMY); tickOk++; }
    catch (Throwable t) {
      tickErr++;
      if (tickErr <= 8) {
        Throwable c = t;
        while (c instanceof java.lang.reflect.InvocationTargetException && c.getCause() != null) c = c.getCause();
        log("  [tick异常#" + tickErr + "] " + c);
      }
    }
  }

  static void settle(int maxFrames) {
    String prev = null; int stable = 0, n = 0;
    while (n < maxFrames) {
      tick(); n++;
      String s = sig();
      if (s.equals(prev)) { if (++stable >= 4) break; } else stable = 0;
      prev = s;
    }
  }

  static void key(int code) {
    try { KEYDOWN.invoke(app, EV, code); } catch (Throwable t) { log("  [keyDown异常] " + t); }
    tick();
    try { if (KEYUP != null) KEYUP.invoke(app, EV, code); } catch (Throwable t) {}
    settle(300);
  }

  static int CODE(char c) {
    switch (c) {
      case 'u': case 'U': case '8': return 56;
      case 'd': case 'D': case '2': return 50;
      case 'l': case 'L': case '4': return 52;
      case 'r': case 'R': case '6': return 54;
    }
    return 13;
  }

  static void clearMsg() {
    for (String n : new String[]{"messageFlag", "messageFlag2", "messageFlag3"}) {
      Field x = f(n);
      if (x != null && x.getType() == boolean.class) {
        try { x.setBoolean(app, false); } catch (Throwable t) {}
      }
    }
  }

  /** 按键驱动到目标格（含消息/过场/重按兜底，照抄 Headless8 主循环） */
  static boolean driveChecked(int tx, int ty, int tf, int dirCode, String tag) {
    boolean DBG = System.getenv("PROBE_DBG") != null;
    int escStreak = 0; String lastSig = null;
    for (int i = 0; i < 200; i++) {
      if (fl() == tf && cx() == tx && cy() == ty) return true;
      int msg = gi("messageFlag") | gi("messageFlag2");
      String s = sig();
      if (!s.equals(lastSig)) escStreak = 0;
      lastSig = s;
      if (DBG && i % 10 == 0) log(String.format("    [dbg]%s i=%d f%d (%d,%d) chX=%d chY=%d U%d D%d L%d R%d cur=%d msg=%d op=%d atk=%d",
          tag, i, fl(), cx(), cy(), gi("charaX"), gi("charaY"), gi("UpKey"), gi("DownKey"), gi("LeftKey"), gi("RightKey"),
          gi("currentKey"), msg, gi("openningFlag"), gi("attackFlag")));
      if (msg != 0) {
        key(27); escStreak++;
        if (escStreak >= 6) { clearMsg(); log("    [省流] 反射清零消息字段 (" + tag + ")"); escStreak = 0; }
      }
      else if (gi("openningFlag") != 0 || gi("dialogFlag") != 0) key(13);
      else if (gi("attackFlag") != 0) { settle(600); }     // 战斗动画：等待
      else key(dirCode);
    }
    log("  !! driveChecked(" + tf + "F," + tx + "," + ty + ") 超时 (" + tag + ") 现在 f" + fl() + " (" + cx() + "," + cy() + ") chX=" + gi("charaX") + " chY=" + gi("charaY") + " U=" + gi("UpKey") + " D=" + gi("DownKey") + " L=" + gi("LeftKey") + " R=" + gi("RightKey") + " cur=" + gi("currentKey") + " " + flags() + " focus=" + gi("focusFlag") + " cntRep=" + gi("countRepaint") + " menu=" + gi("menuFlag") + " inKey=" + gi("inputKey"));
    dumpFloor7();
    return false;
  }

  /** 按 CSV 目标序列驱动一段路程 */
  static boolean driveCsv(String csvPath, String keys) throws Exception {
    List<String> lines = Files.readAllLines(Paths.get(csvPath));
    List<int[]> rows = new java.util.ArrayList<>();
    for (String line : lines) {
      String[] p = line.split(",", -1);
      if (p.length > 3 && p[0].matches("\\d+")) rows.add(new int[]{Integer.parseInt(p[1]), Integer.parseInt(p[2]), Integer.parseInt(p[3])});
    }
    if (rows.size() != keys.length()) { log("!! CSV 行数 " + rows.size() + " != 按键数 " + keys.length() + " (" + csvPath + ")"); return false; }
    for (int i = 0; i < keys.length(); i++) {
      int[] t = rows.get(i);
      char ch = keys.charAt(i);
      if (!driveChecked(t[1], t[2], t[0], CODE(ch), csvPath + " 步" + (i + 1))) {
        log("!! " + csvPath + " 第" + (i + 1) + "步未达 f" + t[0] + "(" + t[1] + "," + t[2] + ")");
        return false;
      }
    }
    return true;
  }

  static void dumpFloor7() {
    int b = 0, s = 6;   // 7F
    StringBuilder sb = new StringBuilder("  mapObject 7F（obj）:\n");
    for (int y = 0; y < 13; y++) {
      for (int x = 0; x < 13; x++) sb.append(String.format("%5d", arrA("mapObject", b * 13 + y, s * 13 + x)));
      sb.append('\n');
    }
    log(sb.toString());
  }

  static void dumpState() {
    StringBuilder sb = new StringBuilder("  状态区 r66-77 c118-125:\n");
    for (int r = 66; r <= 77; r++) {
      sb.append(String.format("   r%02d:", r));
      for (int c = 118; c <= 125; c++) sb.append(String.format("%5d", arrA("mapObject", r, c)));
      sb.append('\n');
    }
    log(sb.toString());
  }

  static void realizeApplet() throws Exception {
    java.awt.Frame fr = new java.awt.Frame("mt8-probe");
    fr.setSize(640, 400);
    fr.add(app);
    Method an = java.awt.Component.class.getDeclaredMethod("addNotify");
    an.setAccessible(true);
    an.invoke(fr);
    an.invoke(app);
  }

  public static void main(String[] a) throws Exception {
    LOG = new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]), "UTF-8"));
    String sword = new String(Files.readAllBytes(Paths.get(a[1])), "UTF-8").trim();
    String to7 = new String(Files.readAllBytes(Paths.get(a[2])), "UTF-8").trim();
    String csvSword = a[3], csv7 = a[4];
    app = (Applet) Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new Stub());
    KEYDOWN = app.getClass().getMethod("keyDown", Event.class, int.class);
    try { KEYUP = app.getClass().getMethod("keyUp", Event.class, int.class); } catch (Throwable t) { KEYUP = null; }
    PAINT = app.getClass().getMethod("paint", Graphics.class);
    EV = new Event(app, System.currentTimeMillis(), Event.KEY_PRESS, 0, 0, 0, 0);

    app.init();
    realizeApplet();
    // 标志/缓冲/声音初始化（照抄 Headless8）
    String[] zeros = {"yesnoNumber", "yesnoJudge", "mapFlagErase", "messageFlag", "messageFlag2", "messageFlag3",
        "yusyaFlag", "openningFlag", "saidanFlag", "menuFlag", "itemKeyFlag", "attackFlag", "scoreFlag",
        "saveFlag", "popupFlag", "UpKey", "DownKey", "LeftKey", "RightKey", "focusFlag", "countRepaint",
        "movingSkip", "paintSkip", "repaintSkip", "currentKey"};
    for (String n : zeros) { Field x = f(n); if (x != null) { if (x.getType() == boolean.class) x.setBoolean(app, false); else x.setInt(app, 0); } }
    String[] ones = {"inputKey", "mapFlagAll", "configFlag", "animaFlag"};
    for (String n : ones) { Field x = f(n); if (x != null) { if (x.getType() == boolean.class) x.setBoolean(app, true); else x.setInt(app, 1); } }
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
        if (img != null && img.get(app) != null) x.set(app, ((Image) img.get(app)).getGraphics());
        else x.set(app, new BufferedImage(820, 520, BufferedImage.TYPE_INT_RGB).getGraphics());
      }
    }
    DUMMY = new BufferedImage(820, 520, BufferedImage.TYPE_INT_RGB).getGraphics();
    Field ax = f("audio");
    if (ax != null) {
      int len = Array.getLength(ax.get(app));
      AudioClip[] mute = new AudioClip[len];
      AudioClip m = new AudioClip() { public void play() {} public void loop() {} public void stop() {} };
      for (int i = 0; i < len; i++) mute[i] = m;
      ax.set(app, mute);
    }

    // 过开场
    for (int i = 0; i < 30; i++) {
      key(13); settle(200);
      if (arrA("mapObject", 66, 118) > 0 && fl() == 1 && cx() == 6 && cy() == 11) break;
    }
    log("[probe] 起点 " + stats());

    // 驱动 sword(141, CSV校验) + enter7(106, CSV校验)
    if (!driveCsv(csvSword, sword)) { LOG.close(); System.exit(2); }
    log("[probe] 铁剑路线终点 " + stats() + " " + flags());
    if (!driveCsv(csv7, to7)) { LOG.close(); System.exit(2); }
    log("[probe] 到达 " + stats() + " " + flags());
    if (!(fl() == 7 && cx() == 11 && cy() == 10)) { log("!! 未到 7F(11,10)，终止"); LOG.close(); System.exit(2); }

    // 反射清零 7F 黄门 obj2 / 蓝门 obj4（slot6: col 78-90, row 0-12）
    int cleared = 0;
    for (int r = 0; r < 13; r++) {
      for (int c = 78; c <= 90; c++) {
        int o = arrA("mapObject", r, c);
        if (o == 2 || o == 4) { setArr("mapObject", r, c, 0); cleared++; }
      }
    }
    log("[probe] 反射清零 7F 门 " + cleared + " 扇");

    // 基线 dump
    log("[probe] == 基线（商人前） ==");
    dumpState();

    // 向西 5 格到 (6,10)（路过 (7,10) 僧侣会打）
    if (System.getenv("PROBE_MIN") != null) {
      log("[probe] == 最小实验：清门后按左一次 ==");
      log("[probe] 按左前 chX=" + gi("charaX") + " chY=" + gi("charaY") + " L=" + gi("LeftKey") + " cur=" + gi("currentKey"));
      key(CODE('l'));
      log("[probe] 按左后(含settle300) chX=" + gi("charaX") + " chY=" + gi("charaY") + " L=" + gi("LeftKey") + " cur=" + gi("currentKey"));
      for (int i = 0; i < 12; i++) {
        tick();
        log(String.format("[probe]   tick%02d chX=%d chY=%d L=%d cur=%d cntRep=%d focus=%d inKey=%d", i, gi("charaX"), gi("charaY"), gi("LeftKey"), gi("currentKey"), gi("countRepaint"), gi("focusFlag"), gi("inputKey")));
      }
      LOG.close(); System.exit(0);
    }
    int[][] west = {{10,10},{9,10},{8,10},{7,10},{6,10}};
    for (int[] t : west) if (!driveChecked(t[0], t[1], 7, CODE('l'), "西")) { LOG.close(); System.exit(2); }
    log("[probe] 西段结束 " + stats() + " " + flags());
    // 向北 8 格到 (6,2)
    int[][] north = {{6,9},{6,8},{6,7},{6,6},{6,5},{6,4},{6,3},{6,2}};
    for (int[] t : north) if (!driveChecked(t[0], t[1], 7, CODE('u'), "北")) { LOG.close(); System.exit(2); }
    log("[probe] 就位 (6,2) " + stats() + " " + flags());
    dumpState();

    // 撞商人 (6,1)
    log("[probe] == 撞商人 obj41 ==");
    key(CODE('u'));
    log("[probe] 撞后 " + stats() + " " + flags());
    dumpFloor7();
    dumpState();

    // 逐键试探
    int[] tryKeys = {13, 32, 27, 121, 89, 13};
    String[] kn = {"Enter(13)", "空格(32)", "ESC(27)", "y(121)", "Y(89)", "Enter(13)再试"};
    for (int i = 0; i < tryKeys.length; i++) {
      log("[probe] -- 试键 " + kn[i] + " --");
      key(tryKeys[i]);
      log("[probe]   " + stats() + " " + flags());
      if (i == 0 || i == 5) { dumpState(); dumpFloor7(); }
    }

    log("[probe] tick 成功 " + tickOk + " 异常 " + tickErr);
    LOG.close();
    System.exit(0);
  }
}
