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
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;

/** 在运行时地图上自己寻路去 5F 拿铁剑：每步按键后轮询状态确认，失败换向。 */
public class Fetch {
  static Applet app; static PrintWriter LOG; static Method KEYDOWN, KEYUP; static Event EV;
  static final Set<String> DEAD = new HashSet<>();
  static int[] lastTry = null;
  static final int GF = 5, GX = 11, GY = 11;             // 铁剑所在层/格
  static Field f(String n) { try { return app.getClass().getDeclaredField(n); } catch (Throwable t) { return null; } }
  static int gi(String n) { try { Field x = f(n); x.setAccessible(true); Object v = x.get(app);
      if (v instanceof Character) return (int) (char) (Character) v; return ((Number) v).intValue(); } catch (Throwable t) { return -1; } }
  static int arr(String fld, int r, int c) { try { Field x = f(fld); x.setAccessible(true);
      Object row = Array.get(x.get(app), r); Object e = Array.get(row, c);
      return (e instanceof Character) ? (int) (char) (Character) e : ((Number) e).intValue(); } catch (Throwable t) { return -1; } }
  static void log(String m) { LOG.println(m); LOG.flush(); System.out.println(m); }
  static int fl() { return gi("mapY") * 10 + gi("mapX") + 1; }
  static int cx() { return gi("charaX") / 5; }
  static int cy() { return gi("charaY") / 5; }
  static int objAt(int q, int x, int y) { return arr("mapObject", (q - 1) / 10 * 13 + y, (q - 1) % 10 * 13 + x); }
  static boolean wallAt(int q, int x, int y) {
    if (x < 0 || y < 0 || x > 12 || y > 12) return true;
    int t = arr("map", (q - 1) / 10 * 13 + y, (q - 1) % 10 * 13 + x);
    return arr("mapAttribute", t, 3) == 1;
  }
  static int cropAt(int q, int x, int y) {
    int t = arr("map", (q - 1) / 10 * 13 + y, (q - 1) % 10 * 13 + x);
    return arr("mapAttribute", t, 1);
  }
  static int kindAt(int q, int x, int y) {
    int t = arr("map", (q - 1) / 10 * 13 + y, (q - 1) % 10 * 13 + x);
    return arr("mapAttribute", t, 3);
  }
  static String st() {
    return "f" + fl() + "(" + cx() + "," + cy() + ") HP=" + arr("mapObject", 66, 118) + " ATK=" + arr("mapObject", 67, 118)
        + " DEF=" + arr("mapObject", 68, 118) + " G=" + arr("mapObject", 69, 118) + " obj=" + objAt(fl(), cx(), cy());
  }
    static final int[] DCODE = {56, 50, 52, 54};             // 实机：上56 左50 下52 右54
  static final int[][] DD = {{0, -1}, {-1, 0}, {0, 1}, {1, 0}};

  static boolean tryDir(int d) {
    int bf = fl(), bx = cx(), by = cy();
    try { KEYDOWN.invoke(app, EV, DCODE[d]); } catch (Throwable t) {}
    for (int i = 0; i < 12; i++) {
      sleep(80);
      try { KEYUP.invoke(app, EV, DCODE[d]); } catch (Throwable t) {}
      if (fl() != bf || cx() != bx || cy() != by) return true;      // 位置变了＝走通/上楼
      sleep(40);
    }
    return false;
  }
  static void sleep(int ms) { try { Thread.sleep(ms); } catch (InterruptedException e) {} }

  /** BFS 于运行时地图：状态=(层,格x,格y,黄钥匙)。黄门耗钥匙，红门/門番B/魔导师＝墙。 */
  static List<Integer> pathDirs() {
    final int sq = fl(), sx = cx(), sy = cy();
    String start = sq + "," + sx + "," + sy + ",0";
    ArrayDeque<String> queue = new ArrayDeque<>();
    HashSet<String> seen = new HashSet<>();
    Set<String> dead = DEAD;
    Map<String, String> par = new HashMap<>();
    Map<String, Integer> pard = new HashMap<>();
    seen.add(start); queue.add(start);
    String found = null;
    while (!queue.isEmpty() && found == null) {
      String[] p = queue.poll().split(",");
      int q = Integer.parseInt(p[0]), x = Integer.parseInt(p[1]), y = Integer.parseInt(p[2]), k = Integer.parseInt(p[3]);
      for (int d = 0; d < 4; d++) {
        int nx = x + DD[d][0], ny = y + DD[d][1], nq = q, nk = k;
        if (nx < 0 || ny < 0 || nx > 12 || ny > 12) continue;
        if (wallAt(q, nx, ny)) continue;
        int o = objAt(q, nx, ny);
        if (o == 15 || o == 58 || o == 27) continue;
        if (dead.contains(nq + "," + nx + "," + ny)) continue;   // 撞不开的格＝墙
        int kind = kindAt(q, nx, ny);
        if (kind == 2) {
          int[] de = (cropAt(q, nx, ny) == 34) ? stairEntry(q + 1, 35) : stairEntry(q - 1, 34);
          if (de == null) continue;
          nq = (cropAt(q, nx, ny) == 34) ? q + 1 : q - 1;
          nx = de[0]; ny = de[1];
        }
        if (o == 1) nk = k + 1;
        if (nq < 1 || nq > 5) continue;
        String key = nq + "," + nx + "," + ny + "," + nk;
        if (seen.contains(key)) continue;
        seen.add(key); par.put(key, q + "," + x + "," + y + "," + k); pard.put(key, d);
        queue.add(key);
        if (nq == GF && nx == GX && ny == GY) { found = key; break; }
      }
    }
    List<Integer> out = new ArrayList<>();
    if (found == null) return out;
    String cur = found;
    while (cur != null && !cur.equals(start)) {
      Integer d = pard.get(cur);
      if (d == null) break;
      out.add(0, d);
      cur = par.get(cur);
    }
    return out;
  }
  static int[] stairEntry(int q, int wantCrop) {
    if (q < 1 || q > 8) return null;
    for (int y = 0; y < 13; y++) for (int x = 0; x < 13; x++)
      if (kindAt(q, x, y) == 2 && cropAt(q, x, y) == wantCrop) return new int[]{x, y};
    return null;
  }


  public static void main(String[] a) throws Exception {
    LOG = new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]), "UTF-8"));
    app = (Applet) Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new RunApplet.Stub());
    KEYDOWN = app.getClass().getMethod("keyDown", Event.class, int.class);
    KEYUP = app.getClass().getMethod("keyUp", Event.class, int.class);
    EV = new Event(app, System.currentTimeMillis(), Event.KEY_PRESS, 0, 0, 0, 0);
    Frame fr = new Frame("mota"); fr.setLayout(new BorderLayout()); fr.add(app, BorderLayout.CENTER);
    fr.setSize(820, 540); fr.setVisible(true);
    app.init(); app.start();
    Field cf = f("imgCrop"); cf.setAccessible(true);
    long t0 = System.currentTimeMillis();
    int lastPress = -10;
    while (System.currentTimeMillis() - t0 < 70000) {
      boolean ready = Array.get(cf.get(app), 100) != null && arr("mapObject", 66, 118) > 0;
      if (ready) break;
      long el = (System.currentTimeMillis() - t0) / 1000;
      if (el - lastPress >= 6) {                          // 每 4 秒稳按一次 Enter
        lastPress = (int) el;
        try { KEYDOWN.invoke(app, EV, 13); } catch (Throwable t) {}
        sleep(150);
        try { KEYUP.invoke(app, EV, 13); } catch (Throwable t) {}
      }
      if (false) log("  等待中 " + el + "s HP=" + arr("mapObject", 66, 118) + " obj[30@5F]=" + objAt(5, 11, 11));
      sleep(300);
    }
    if (arr("mapObject", 66, 118) <= 0) { log("进场失败(重载竞态) " + st()); LOG.close(); System.exit(2); }
    log("进入游戏 " + st());
    int steps = 0, stuck = 0, pi = 0;
    List<Integer> plan = pathDirs();
    log("初始计划长度 " + plan.size() + " 步；" + st());
    int expQ = fl(), expX = cx(), expY = cy();
    while (steps++ < 260) {
      if (fl() == GF && cx() == GX && cy() == GY) { log("\u2605 抵达铁剑格！" + st()); break; }
      if (plan.isEmpty()) { log("无路可走 " + st()); break; }
      if (pi >= plan.size() || fl() != expQ || cx() != expX || cy() != expY) {
        plan = pathDirs(); pi = 0;                       // 重新规划
        log("  第" + steps + " 步 重规划（" + st() + "）计划长 " + plan.size());
        if (plan.isEmpty()) { log("无路可走 " + st()); break; }
      }
      int d = plan.get(pi);
      int bfl = fl(), bx = cx(), by = cy();
      boolean moved = tryDir(d);
      pi++;
      expQ = fl(); expX = cx(); expY = cy();
      int tx = cx() + DD[d][0], ty = cy() + DD[d][1];
      if (!moved) {
        if (pi < plan.size() + 1 && plan.size() > pi) { }
        boolean same = lastTry != null && lastTry[0] == fl() && lastTry[1] == cx() && lastTry[2] == tx && lastTry[3] == ty;
        if (same) {
          DEAD.add((pi > 0 ? fl() : fl()) + "," + tx + "," + ty);
          log("  第" + steps + " 步 dir=" + d + " 两次不动 → 禁行 " + (pi > 0 ? fl() : fl()) + "(" + tx + "," + ty + ")" + " obj=" + objAt(fl(), tx, ty));
          lastTry = null; pi = plan.size();
        } else {
          lastTry = new int[]{fl(), cx(), tx, ty};
          pi--;                                            // 同方向再试一次（门被撞开的情况）
          log("  第" + steps + " 步 dir=" + d + " 未动，再试同方向（可能是撞门）" + st());
        }
        stuck++;
        if (stuck > 40) { log("连续卡死，停"); break; }
      } else {
        lastTry = null; stuck = 0;
        if (steps % 5 == 0) log("  第" + steps + " 步 " + st());
      }
    }
    log("最终 " + st());
    int sword = objAt(5, 11, 11);
    log("铁剑格现存 obj=" + sword + "（201？应为 0/空即已拾取；ATK=" + arr("mapObject", 67, 118) + "）");
    LOG.close(); System.exit(0);
  }
}
