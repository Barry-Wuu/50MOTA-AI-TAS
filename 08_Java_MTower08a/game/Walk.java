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

/** 逐键执行按键串（u/d/l/r，大写=连按两次用于开门），记录 HP/攻防/金币/层号/提示号。 */
public class Walk {
  static Applet app; static PrintWriter LOG; static Method KEYDOWN, KEYUP; static Event EV;
  static Field f(String n) { try { return app.getClass().getDeclaredField(n); } catch (Throwable t) { return null; } }
  static int gi(String n) { try { Field x = f(n); x.setAccessible(true); Object v = x.get(app);
      if (v instanceof Character) return (int) (char) (Character) v; return ((Number) v).intValue(); } catch (Throwable t) { return 0; } }
  static int arrA(String fld, int r, int c) { try { Field x = f(fld); x.setAccessible(true);
      Object row = Array.get(x.get(app), r); Object e = Array.get(row, c);
      return (e instanceof Character) ? (int) (char) (Character) e : ((Number) e).intValue(); } catch (Throwable t) { return -1; } }
  static int cx() { return gi("charaX") / 5; }
  static int cy() { return gi("charaY") / 5; }
  static int floorf() { return gi("mapY") * 10 + gi("mapX") + 1; }
  static void log(String m) { LOG.println(m); LOG.flush(); }
  static String stats() {
    return "f" + floorf() + " (" + cx() + "," + cy() + ") HP=" + arrA("mapObject", 66, 118)
        + " ATK=" + arrA("mapObject", 67, 118) + " DEF=" + arrA("mapObject", 68, 118)
        + " G=" + arrA("mapObject", 69, 118) + " keys(y,b,r)=" + arrA("mapObject", 70, 118) + ","
        + arrA("mapObject", 71, 118) + "," + arrA("mapObject", 72, 118)
        + " strNum=" + gi("strNumber");
  }
  static void press(int code) {
    try { KEYDOWN.invoke(app, EV, code); } catch (Throwable t) { log("down " + t); }
    try { Thread.sleep(520); } catch (InterruptedException e) {}
    try { if (KEYUP != null) KEYUP.invoke(app, EV, code); } catch (Throwable t) {}
    try { Thread.sleep(260); } catch (InterruptedException e) {} }
  static void dumpFloor(int fl) {
    int b = (fl - 1) / 10, s = (fl - 1) % 10; StringBuilder sb = new StringBuilder("  mapObject " + fl + "F\n");
    for (int y = 0; y < 13; y++) { for (int x = 0; x < 13; x++) sb.append(String.format("%4d", arrA("mapObject", b * 13 + y, s * 13 + x))); sb.append('\n'); }
    log(sb.toString());
  }
  public static void main(String[] a) throws Exception {
    LOG = new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]), "UTF-8"));
    app = (Applet) Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new RunApplet.Stub());
    KEYDOWN = app.getClass().getMethod("keyDown", Event.class, int.class);
    try { KEYUP = app.getClass().getMethod("keyUp", Event.class, int.class); } catch (Throwable t) { KEYUP = null; }
    EV = new Event(app, System.currentTimeMillis(), Event.KEY_PRESS, 0, 0, 0, 0);
    Frame fr = new Frame("mota"); fr.setLayout(new BorderLayout()); fr.add(app, BorderLayout.CENTER);
    fr.setSize(820, 540); fr.setVisible(true); app.init(); app.start();
    Field cf = f("imgCrop"); cf.setAccessible(true);
    long t0 = System.currentTimeMillis();
    while (System.currentTimeMillis() - t0 < 180000) { if (Array.get(cf.get(app), 100) != null) break; Thread.sleep(300); }
    log("贴图就绪 " + ((System.currentTimeMillis() - t0) / 1000) + "s");
    Thread.sleep(4000);
    for (int i = 0; i < 8; i++) {                       // 进游戏：最多按 5 次 Enter，每次确认 HP
      press(13); Thread.sleep(1200);
      log("enter" + i + " → " + stats());
      if (arrA("mapObject", 66, 118) > 0 && cx() + cy() > 0) break;
    }
    Thread.sleep(1500);
    log("起点 " + stats());
    int lastFloor = floorf(); int lastHp = arrA("mapObject", 66, 118);
    String keys = a[1];
    for (int i = 0; i < keys.length(); i++) {
      char c = keys.charAt(i); boolean twice = Character.isUpperCase(c);
      // 实测映射：56=上 54=右 52=下 50=左（与 keyDown 分支常量顺序不同，以实机为准）
      int code = new java.util.HashMap<Character,Integer>() {{ put('U',56); put('D',52); put('L',50); put('R',54); }}
          .getOrDefault(Character.toUpperCase(c), 0);
      if (code == 0) continue;
      press(code); if (twice) press(code);
      log(String.format("%3d %c  %s", i, c, stats()));
      if (floorf() != lastFloor) { log("!! 换层 " + lastFloor + " -> " + floorf()); dumpFloor(floorf()); lastFloor = floorf(); }
      int hp = arrA("mapObject", 66, 118);
      if (hp <= 0 && lastHp > 0) { log("!! 主角死亡，停止"); break; }
      if (hp > 0) lastHp = hp;
    }
    dumpFloor(floorf());
    log("结束 " + stats()); LOG.close(); System.exit(0);
  }
}
