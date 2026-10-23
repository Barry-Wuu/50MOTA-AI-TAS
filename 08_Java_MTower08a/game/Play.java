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

/** 实机校验：1) 读运行时 1..5F 的 obj 网格；2) 传送到 3F 入口逐步走，看魔导师何时出现、掉多少血。 */
public class Play {
  static Applet app; static PrintWriter LOG; static Method KEYDOWN; static Event EV;
  static Field f(String n) { try { return app.getClass().getDeclaredField(n); } catch (Throwable t) { return null; } }
  static void set(String n, int v) { try { Field x = f(n); x.setAccessible(true);
      if (x.getType() == boolean.class) x.setBoolean(app, v != 0); else x.setInt(app, v); } catch (Throwable t) { log("set " + n + " 失败 " + t); } }
  static int gi(String n) { try { Field x = f(n); x.setAccessible(true); Object v = x.get(app);
      if (v instanceof Character) return (int) (char) (Character) v; return ((Number) v).intValue(); } catch (Throwable t) { return 0; } }
  static int arrA(String fld, int r, int c) { try { Field x = f(fld); x.setAccessible(true);
      Object row = Array.get(x.get(app), r); Object e = Array.get(row, c);
      return (e instanceof Character) ? (int) (char) (Character) e : ((Number) e).intValue(); } catch (Throwable t) { return -1; } }
  static int cellX() { return gi("charaX") / 5; }
  static int cellY() { return gi("charaY") / 5; }
  static int band() { return gi("mapY"); }
  static int slot() { return gi("mapX"); }
  static int floor() { return band() * 10 + slot() + 1; }
  static void log(String m) { LOG.println(m); LOG.flush(); System.out.println(m); }

  static void grids(int from, int to) {
    for (int fl = from; fl <= to; fl++) {
      int b = (fl - 1) / 10, s = (fl - 1) % 10;
      StringBuilder sb = new StringBuilder();
      for (int y = 0; y < 13; y++) {
        for (int x = 0; x < 13; x++) {
          int o = arrA("mapObject", b * 13 + y, s * 13 + x);
          sb.append(String.format("%4d", o));
        }
        sb.append('\n');
      }
      log("----- mapObject " + fl + "F ----- \n" + sb);
    }
  }
  static void hp() { log("HP/ATK/DEF/GOLD = " + arrA("mapObject", 66, 118) + "/" + arrA("mapObject", 67, 118)
      + "/" + arrA("mapObject", 68, 118) + "/" + arrA("mapObject", 69, 118) + "   cell=" + cellX() + "," + cellY()
      + " floor=" + floor() + " strNumber=" + gi("strNumber")); }
  static void press(int code) {
    try { KEYDOWN.invoke(app, EV, code); } catch (Throwable t) { log("keyDown " + t); }
    try { Thread.sleep(600); } catch (InterruptedException e) {}
  }
  static void goto_(String spec) { }
  public static void main(String[] a) throws Exception {
    LOG = new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]), "UTF-8"));
    app = (Applet) Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new RunApplet.Stub());
    KEYDOWN = app.getClass().getMethod("keyDown", Event.class, int.class);
    EV = new Event(app, System.currentTimeMillis(), Event.KEY_PRESS, 0, 0, 0, 0);
    Frame fr = new Frame("mota"); fr.setLayout(new BorderLayout()); fr.add(app, BorderLayout.CENTER);
    fr.setSize(820, 540); fr.setVisible(true);
    app.init(); app.start();
    Field cf = f("imgCrop"); cf.setAccessible(true);
    long t0 = System.currentTimeMillis();
    while (System.currentTimeMillis() - t0 < 45000) { if (Array.get(cf.get(app), 100) != null) break; Thread.sleep(300); }
    Thread.sleep(2500);
    press(13);   // 关掉开场
    log("起点: floor=" + floor() + " cell=" + cellX() + "," + cellY());
    hp();
    grids(1, 5);
    // 传送到 3F 的下行梯格 (1,11)
    set("mapX", 2); set("mapY", 0); set("charaX", 1 * 5); set("charaY", 11 * 5);
    set("charaXold", 5); set("charaYold", 55);
    log("=== 传送到 3F 后 ==="); hp();
    grids(3, 3);
    for (int i = 0; i < 6; i++) { press(56); }            // 连续向上，观察能否穿过 (5,9) 一带
    hp();
    log("=== 3F 再 dump ==="); grids(3, 3);
    log("end"); LOG.close(); System.exit(0);
  }
}
