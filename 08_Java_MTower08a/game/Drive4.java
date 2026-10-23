import java.applet.Applet;
import java.awt.BorderLayout;
import java.awt.Event;
import java.awt.Frame;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.lang.reflect.Array;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * 实机驱动 v2：进入游戏 → 按文件里的按键串（8上/2下/4左/6/r=开门再按一次）逐步走，
 * 每步回读 (层, 格, HP/ATK/DEF/GOLD, 钥匙变量格)，并在指定层抓取整层 mapObject/terrain 快照。
 * 目的：用真引擎判定 route_sword_1f_to_5f.csv，并回答「2F 牢房怎么出来」这类问题。
 */
public class Drive4 {
  static Applet app; static PrintWriter LOG; static Method KEYDOWN, KEYUP; static Event EV;
  static String OUT;

  static Field f(String n) { try { return app.getClass().getDeclaredField(n); } catch (Throwable t) { return null; } }
  static int gi(String n) {
    try { Field x = f(n); x.setAccessible(true); Object v = x.get(app);
      if (v instanceof Character) return (int) (char) (Character) v; return ((Number) v).intValue(); }
    catch (Throwable t) { return -9999; }
  }
  static int arr(String fld, int r, int c) {
    try { Field x = f(fld); x.setAccessible(true); Object row = Array.get(x.get(app), r); Object e = Array.get(row, c);
      return (e instanceof Character) ? (int) (char) (Character) e : ((Number) e).intValue(); }
    catch (Throwable t) { return -1; }
  }
  static void log(String m) { LOG.println(m); LOG.flush(); }
  static int fl() { return gi("mapY") * 10 + gi("mapX") + 1; }
  static int cx() { return gi("charaX") / 5; }
  static int cy() { return gi("charaY") / 5; }
  static String state() {
    return fl() + "," + cx() + "," + cy() + "," + arr("mapObject", 66, 118) + "," + arr("mapObject", 67, 118) + ","
        + arr("mapObject", 68, 118) + "," + arr("mapObject", 69, 118) + ",str=" + gi("strNumber")
        + ",msg=" + gi("messageFlag") + "/" + gi("messageFlag2") + "/" + gi("messageFlag3")
        + ",flag3F=" + gi("flag3F");
  }
  static void snap(String tag, int F) {
    int b = (F - 1) / 10, s = (F - 1) % 10;
    StringBuilder so = new StringBuilder(), sk = new StringBuilder();
    for (int y = 0; y < 13; y++) {
      for (int x = 0; x < 13; x++) {
        so.append(String.format("%4d", arr("mapObject", b * 13 + y, s * 13 + x)));
        int t = arr("map", b * 13 + y, s * 13 + x);
        sk.append(String.format("%4d", t < 200 ? arr("mapAttribute", t, 3) : -1));
      }
      so.append('\n'); sk.append('\n');
    }
    log("### " + tag + " floor" + F + " kinds:\n" + sk + "objects:\n" + so);
  }
  static void press(int code, int ms) {
    try { KEYDOWN.invoke(app, EV, code); } catch (Throwable t) { log("keyDown 异常 " + t); }
    try { Thread.sleep(ms); } catch (InterruptedException e) { }
    if (KEYUP != null) { try { KEYUP.invoke(app, EV, code); } catch (Throwable t) { } }
    try { Thread.sleep(320); } catch (InterruptedException e) { }
  }

  public static void main(String[] a) throws Exception {
    OUT = a[0];
    LOG = new PrintWriter(new OutputStreamWriter(new FileOutputStream(OUT), "UTF-8"));
    String keyfile = a[1];
    String snaps = a.length > 2 ? a[2] : "";           // 例如 "2,5"：在这些层抓快照
    app = (Applet) Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new RunApplet.Stub());
    KEYDOWN = app.getClass().getMethod("keyDown", Event.class, int.class);
    try { KEYUP = app.getClass().getMethod("keyUp", Event.class, int.class); } catch (Throwable t) { KEYUP = null; }
    EV = new Event(app, System.currentTimeMillis(), Event.KEY_PRESS, 0, 0, 0, 0);
    Frame fr = new Frame("mota"); fr.setLayout(new BorderLayout()); fr.add(app, BorderLayout.CENTER);
    fr.setSize(820, 540); fr.setVisible(true);
    app.init(); app.start();
    Field cf = f("imgCrop"); cf.setAccessible(true);
    long t0 = System.currentTimeMillis();
    while (System.currentTimeMillis() - t0 < 200000) {          // 只等贴图
      if (Array.get(cf.get(app), 100) != null) break;
      Thread.sleep(400);
    }
    log("贴图就绪 " + ((System.currentTimeMillis() - t0) / 1000) + "s");
    for (int i = 0; i < 30; i++) {                              // 反复试进入游戏
      if (arr("mapObject", 66, 118) > 0 && (cx() + cy()) > 0) break;
      if (i % 4 == 0) press(32, 260);                            // Space
      press(13, 320);                                            // Enter
      press(56, 300);                                            // 上：有时要点一下才开局
      Thread.sleep(1100);
      if (i % 5 == 4) log("  进场尝试 #" + i + " " + state());
    }
    log("进入 " + state());
    if (arr("mapObject", 66, 118) <= 0 || (cx() == 0 && cy() == 0)) {
      log("进场失败，退出码 3 让外层重来");
      LOG.close();
      System.exit(3);
    }
    snap("开局", 1);
    String keys = new String(Files.readAllBytes(Paths.get(keyfile)), "UTF-8").trim();
    int[] codes = new int[keys.length()];
    for (int i = 0; i < keys.length(); i++) {
      char ch = keys.charAt(i);
      int v;                                                   // 实测码位：8=上56 2=下52 4=左50 6=右54
      // 实测：56=上 52=左 54=右 50=下（即小键盘 8/4/6/2 的 ASCII）
      switch (ch) { case '8': v = 56; break; case '2': v = 50; break; case '4': v = 52; break;
                    case '6': v = 54; break; default: v = 13; }
      codes[i] = v;
    }
    int lastf = fl();
    for (int i = 0; i < codes.length; i++) {
      press(codes[i], 420);                             // 与 CSV 1:1：撞门步就是原地撞
      log(String.format("%3d k=%d %s", i, codes[i], state()));
      int nf = fl();
      if (nf != lastf) {
        log("  ~ 换层 " + lastf + " -> " + nf);
        try { if (java.util.Arrays.asList(snaps.split(",")).contains(String.valueOf(nf))) snap("刚到层时", nf); } catch (Exception e) {}
        lastf = nf;
      }
    }
    if (snaps.contains(String.valueOf(fl()))) snap("结束前", fl());
    log("结束 " + state());
    LOG.close(); System.exit(0);
  }
}
