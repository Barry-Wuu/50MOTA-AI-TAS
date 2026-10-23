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
import java.util.ArrayList;
import java.util.List;

/**
 * 闭环跟随实机验证：以内核路线 plan.txt（每行 "层 x y"）为目标序列，
 * 逐步短按方向键并等动画停住；换层时在所在格试四个方向直到真的换层。
 * 日志 = 引擎真实轨迹 + 每帧资源，用来逐帧对比内核复验 CSV。
 */
public class Drive5 {
  static Applet app;
  static PrintWriter LOG;
  static Method KEYDOWN, KEYUP;
  static Event EV;

  static Field f(String n) { try { return app.getClass().getDeclaredField(n); } catch (Throwable t) { return null; } }

  static int gi(String n) {
    try {
      Field x = f(n); x.setAccessible(true); Object v = x.get(app);
      if (v instanceof Character) return (char) (Character) v;
      if (v instanceof Boolean) return ((Boolean) v) ? 1 : 0;
      return ((Number) v).intValue();
    } catch (Throwable t) { return 0; }
  }

  static int arr(String fld, int r, int c) {
    try {
      Field x = f(fld); x.setAccessible(true);
      Object row = Array.get(x.get(app), r); Object e = Array.get(row, c);
      return (e instanceof Character) ? (char) (Character) e : ((Number) e).intValue();
    } catch (Throwable t) { return -1; }
  }

  static void log(String m) { LOG.println(m); LOG.flush(); }
  static int fl() { return gi("mapX") + 10 * gi("mapY") + 1; }
  static int cx() { return gi("charaX") / 5; }
  static int cy() { return gi("charaY") / 5; }

  static String st() {
    return fl() + "," + cx() + "," + cy()
        + " HP=" + arr("mapObject", 66, 118) + " ATK=" + arr("mapObject", 67, 118)
        + " DEF=" + arr("mapObject", 68, 118) + " G=" + arr("mapObject", 69, 118)
        + " v70/71/72=" + arr("mapObject", 70, 118) + "," + arr("mapObject", 71, 118) + "," + arr("mapObject", 72, 118)
        + " str=" + gi("strNumber") + " msg=" + gi("messageFlag") + "/" + gi("messageFlag2")
        + " msg3=" + gi("messageFlag3")
        + " flag3F=" + gi("flag3F");
  }

  static int CODE(char c) {
    switch (c) { case 'u': return 56; case 'd': return 50; case 'l': return 52; case 'r': return 54; }
    return 13;
  }

  /** Walk.java 实测有效的按键：down -> 520ms -> up -> 260ms（标题/对话只认这种节奏） */
  static void enterKey(int code) {
    try { KEYDOWN.invoke(app, EV, code); } catch (Throwable t) { }
    try { Thread.sleep(520); } catch (InterruptedException e) { }
    try { if (KEYUP != null) KEYUP.invoke(app, EV, code); } catch (Throwable t) { }
    try { Thread.sleep(260); } catch (InterruptedException e) { }
  }

  /** 移动键：极短按，然后轮询到画面停住，返回这一键是否真的动了 */
  static boolean press(char dir) {
    int x0 = cx(), y0 = cy(), f0 = fl();
    int code = CODE(dir);
    try { KEYDOWN.invoke(app, EV, code); } catch (Throwable t) { }
    try { Thread.sleep(70); } catch (InterruptedException e) { }
    try { if (KEYUP != null) KEYUP.invoke(app, EV, code); } catch (Throwable t) { }
    int px = -1, py = -1, pf = -1, stable = 0;
    for (int i = 0; i < 40; i++) {
      try { Thread.sleep(110); } catch (InterruptedException e) { }
      int x = cx(), y = cy(), ff = fl();
      if (x == px && y == py && ff == pf) { if (++stable >= 2) break; } else { stable = 0; }
      px = x; py = y; pf = ff;
    }
    try { Thread.sleep(140); } catch (InterruptedException e) { }
    return !(cx() == x0 && cy() == y0 && fl() == f0);
  }

  public static void main(String[] a) throws Exception {
    LOG = new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]), "UTF-8"));
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
    while (System.currentTimeMillis() - t0 < 200000) {
      if (Array.get(cf.get(app), 100) != null) break;
      Thread.sleep(300);
    }
    log("贴图就绪 " + ((System.currentTimeMillis() - t0) / 1000) + "s");
    Thread.sleep(4000);                                            // 关键：再等 4s 才吃键
    for (int round = 0; round < 6; round++) {
      for (int i = 0; i < 8; i++) {
        if (arr("mapObject", 66, 118) > 0 && (cx() + cy()) > 0) break;
        enterKey(13);
        Thread.sleep(1200);
      }
      if (arr("mapObject", 66, 118) > 0 && (cx() + cy()) > 0) break;
      log("  第" + round + "轮未进场 str=" + gi("strNumber") + " " + st());
      for (int i = 0; i < 3; i++) { enterKey(32); enterKey(13); Thread.sleep(400); }
      Thread.sleep(5000);
    }
    log("起点 " + st());
    if (arr("mapObject", 66, 118) <= 0 || (cx() == 0 && cy() == 0)) { log("进场失败"); LOG.close(); System.exit(3); }

    List<int[]> plan = new ArrayList<>();
    for (String line : Files.readAllLines(Paths.get(a[1]))) {
      String[] p = line.trim().split("\\s+");
      if (p.length >= 3) plan.add(new int[]{Integer.parseInt(p[0]), Integer.parseInt(p[1]), Integer.parseInt(p[2])});
    }
    log("计划点数 " + plan.size());

    int si = 0, stuck = 0;
    while (si < plan.size()) {
      while (si < plan.size()) {
        int[] q = plan.get(si);
        if (fl() == q[0] && cx() == q[1] && cy() == q[2]) { si++; } else { break; }
      }
      if (si >= plan.size()) break;
      int[] t = plan.get(si);
      int f0 = fl(), x = cx(), y = cy();

      if (f0 != t[0]) {                                             // 需要换层：在当前格试到真的换层
        boolean ok = false;
        char[] order = (t[0] > f0) ? new char[]{'l', 'u', 'r', 'd'} : new char[]{'l', 'd', 'r', 'u'};
        for (char c : order) {
          int before = f0;
          boolean mv = press(c);
          if (fl() != before) { ok = true; log(String.format("  [%d/%d] 换层 dir=%c -> %s", si, plan.size(), c, st())); break; }
          log(String.format("  [%d/%d] 换层试 %c 失败(动了=%s) %s", si, plan.size(), c, mv, st()));
        }
        if (!ok) {
          log("!! 楼梯无反应 当前" + st() + " 目标" + t[0] + "," + t[1] + "," + t[2]);
          for (int z = 0; z < 4; z++) { enterKey(13); }               // 先清掉可能的对话再试
          log("  清对话后 " + st());
          int before2 = fl();
          for (int k2 = 0; k2 < 8; k2++) {                        // 同一方向连按，看是否需要"撞两下"
            press('l');
            log(String.format("  重试l#%d -> %s", k2 + 1, st()));
            if (fl() != before2) { ok = true; break; }
            int[] nn = new int[]{arr("map", y, x - 1), arr("mapObject", y, x - 1)};
            log(String.format("      左邻格 map=%d obj=%d (row=%d col=%d)", nn[0], nn[1], y, x - 1));
          }
          if (!ok) { for (char c : new char[]{'u', 'r', 'd'}) { if (fl() == before2) press(c); log("  再试 " + c + " -> " + st()); if (fl() != before2) { ok = true; break; } } }
          if (!ok) break;
        }
        stuck = 0;
        continue;
      }

      char dir = (t[1] > x) ? 'r' : (t[1] < x) ? 'l' : (t[2] > y) ? 'd' : 'u';
      boolean mv = press(dir);
      log(String.format("  [%d/%d] 追 %c (%d,%d,%d)->(%d,%d,%d) 动了=%s | %s", si, plan.size(), dir, f0, x, y, t[0], t[1], t[2], mv, st()));
      if (fl() == t[0] && cx() == t[1] && cy() == t[2]) { stuck = 0; continue; }
      if (fl() != f0) { log("  ~ 意外换层 -> " + st()); stuck = 0; continue; }
      if (!mv && ++stuck >= 10) {
        log("!! 连按无效 当前" + st() + " 目标" + t[0] + "," + t[1] + "," + t[2]);
        int b = (f0 - 1) / 10, s = (f0 - 1) % 10;
        for (int dy = -2; dy <= 2 && stuck > 0; dy++) {                 // 打印邻域 map/attr/obj，直接看是谁挡的
          StringBuilder sb1 = new StringBuilder(), sb2 = new StringBuilder(), sb3 = new StringBuilder();
          for (int dx = -3; dx <= 3; dx++) {
            int r = b * 13 + y + dy, c2 = s * 13 + x + dx;
            sb1.append(String.format("%4d", arr("map", r, c2)));
            sb2.append(String.format("%4d", arr("mapAttribute", r, c2)));
            sb3.append(String.format("%4d", arr("mapObject", r, c2)));
          }
          log(String.format("  y%+d map:%s attr:%s obj:%s", dy, sb1, sb2, sb3));
        }
        break;
      }
      if (mv) { stuck = 0; }
    }
    log("终 [" + si + "/" + plan.size() + "] " + st());
    LOG.close();
    System.exit(0);
  }
}
