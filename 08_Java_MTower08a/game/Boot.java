import java.applet.Applet;
import java.awt.AWTEvent;
import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Event;
import java.awt.Frame;
import java.awt.image.PixelGrabber;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.lang.reflect.Array;
import java.lang.reflect.Field;
import java.lang.reflect.Method;

/** 真跑 08 Java 版：反射调用旧式 keyDown(Event,int) 驱动主角，逐步打印状态。 */
public class Boot {
  static Applet app;
  static PrintWriter LOG;
  static Method KEYDOWN;
  static Event EV;

  static Field f(String n) {
    try { return app.getClass().getDeclaredField(n); } catch (Throwable t) { return null; }
  }
  static String g(String n) {
    try {
      Field x = f(n); x.setAccessible(true);
      Object v = x.get(app);
      if (v == null) return "null";
      if (x.getType() == boolean.class) return ((Boolean) v) ? "1" : "0";
      if (v instanceof Character) return String.valueOf((int) (char) (Character) v);
      return String.valueOf(v);
    } catch (Throwable t) { return "?"; }
  }
  static int gi(String n) { try { return Integer.parseInt(g(n)); } catch (Exception e) { return 0; } }
  static int arr(String fld, int r, int c) {
    try {
      Field x = f(fld); x.setAccessible(true);
      Object row = Array.get(x.get(app), r);
      Object e = Array.get(row, c);
      return (e instanceof Character) ? (int) (char) (Character) e : Integer.parseInt(String.valueOf(e));
    } catch (Throwable t) { return -1; }
  }
  static void log(String m) { LOG.println(m); LOG.flush(); System.out.println(m); }
  static int cellX() { return gi("charaX") / 5; }
  static int cellY() { return gi("charaY") / 5; }
  static int band() { return gi("mapY"); }
  static int slot() { return gi("mapX"); }
  static int floor() { return band() * 10 + slot() + 1; }

  static void dump(String tag) {
    int r = band() * 13 + cellY(), c = slot() * 13 + cellX();
    log(String.format("%-16s floor=%d mapX=%d mapY=%d cell=(%d,%d) charaX=%d charaY=%d "
        + "tile=%d/%d obj=%d strNumber=%d msg=%d/%d/%d open=%d item=%d menu=%d FileNo=%d sai=%s/%s "
        + "flags[66..69,118]=%d/%d/%d/%d",
        tag, floor(), slot(), band(), cellX(), cellY(), gi("charaX"), gi("charaY"),
        arr("map", r, c), arr("mapAttribute", arr("map", r, c), 1), arr("mapObject", r, c),
        gi("strNumber"), gi("messageFlag"), gi("messageFlag2"), gi("messageFlag3"),
        gi("openningFlag"), gi("itemFlag"), gi("menuFlag"), gi("FileNo"),
        g("sai"), g("sai2"),
        arr("mapObject", 66, 118), arr("mapObject", 67, 118),
        arr("mapObject", 68, 118), arr("mapObject", 69, 118)));
  }

  static void press(int code) {
    try {
      Object r = KEYDOWN.invoke(app, EV, code);
    } catch (Throwable t) { log("keyDown(" + code + ") 异常: " + t); }
    try { Thread.sleep(420); } catch (InterruptedException e) {}
    try { KEYDOWN.invoke(app, EV, -code); } catch (Throwable t) {}   // keyUp 由同类方法处理，忽略失败
    try { Thread.sleep(220); } catch (InterruptedException e) {}
  }

  public static void main(String[] args) throws Exception {
    LOG = new PrintWriter(new OutputStreamWriter(new FileOutputStream(args[0]), "UTF-8"));
    app = (Applet) Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new RunApplet.Stub());
    KEYDOWN = app.getClass().getMethod("keyDown", Event.class, int.class);
    EV = new Event(app, System.currentTimeMillis(), Event.KEY_PRESS, 0, 0, 0, 0);
    Frame fr = new Frame("mota");
    fr.setLayout(new BorderLayout());
    fr.add(app, BorderLayout.CENTER);
    fr.setSize(820, 540);
    fr.setVisible(true);
    app.init();
    app.start();
    Field cf = f("imgCrop"); cf.setAccessible(true);
    long t0 = System.currentTimeMillis();
    while (System.currentTimeMillis() - t0 < 45000) {
      if (Array.get(cf.get(app), 100) != null) break;
      Thread.sleep(300);
    }
    Thread.sleep(2500);
    dump("boot");
    int[] script = {13, 13, 32, 13, 50, 56, 52, 54, 50, 50, 52, 52, 56, 56, 54, 54};
    for (int i = 0; i < script.length; i++) {
      press(script[i]);
      dump("k" + i + "(=" + script[i] + ")");
    }
    log("end"); LOG.close(); System.exit(0);
  }
}
