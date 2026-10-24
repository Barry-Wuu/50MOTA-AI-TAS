import java.applet.Applet;
import java.awt.BorderLayout;
import java.awt.Event;
import java.awt.Frame;
import java.awt.Rectangle;
import java.awt.Robot;
import java.awt.Toolkit;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.lang.reflect.Array;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * 08 Java 版实机验证：按模型路线逐键执行 + 每步强校验 (层,x,y) + 换层截图。
 * 用法: java Verify8 <logfile> <keys_udlr> <shotDir> <routeCsv>
 *   keys: u/d/l/r（大写=按两次开门），与模型步号一一对应
 *   csv : 模型路线 route_*.csv（step,floor,x,y,...），每步的目标坐标
 */
public class Verify8 {
  static Applet app; static PrintWriter LOG; static Method KEYDOWN, KEYUP; static Event EV; static Robot ROBOT;

  static Field f(String n) { try { Field x = app.getClass().getDeclaredField(n); x.setAccessible(true); return x; } catch (Throwable t) { return null; } }
  static int gi(String n) { try { Field x = f(n); Object v = x.get(app);
      if (v instanceof Character) return (int) (char) (Character) v;
      if (v instanceof Boolean) return ((Boolean) v) ? 1 : 0;
      return ((Number) v).intValue(); } catch (Throwable t) { return 0; } }
  static int arrA(String fld, int r, int c) { try { Field x = f(fld); Object row = Array.get(x.get(app), r); Object e = Array.get(row, c);
      return (e instanceof Character) ? (int) (char) (Character) e : ((Number) e).intValue(); } catch (Throwable t) { return -1; } }
  static int cx() { return gi("charaX") / 5; }
  static int cy() { return gi("charaY") / 5; }
  static int fl() { return gi("mapY") * 10 + gi("mapX") + 1; }
  static void log(String m) { LOG.println(m); LOG.flush(); System.out.println(m); }
  static String stats() {
    return "f" + fl() + " (" + cx() + "," + cy() + ") HP=" + arrA("mapObject", 66, 118)
        + " ATK=" + arrA("mapObject", 67, 118) + " DEF=" + arrA("mapObject", 68, 118)
        + " G=" + arrA("mapObject", 69, 118) + " keys(Y,B,R)=" + arrA("mapObject", 70, 118)
        + "," + arrA("mapObject", 71, 118) + "," + arrA("mapObject", 72, 118); }
  static void enter(int code) {
    try { KEYDOWN.invoke(app, EV, code); } catch (Throwable t) {}
    try { Thread.sleep(520); } catch (InterruptedException e) {}
    try { if (KEYUP != null) KEYUP.invoke(app, EV, code); } catch (Throwable t) {}
    try { Thread.sleep(260); } catch (InterruptedException e) {} }
  static int CODE(char c) { switch (c) { case 'u': case 'U': return 56; case 'd': case 'D': return 50; case 'l': case 'L': return 52; case 'r': case 'R': return 54; } return 13; }
  static boolean pressWait(char dir) {
    int x0 = cx(), y0 = cy(), f0 = fl(); int code = CODE(dir);
    try { KEYDOWN.invoke(app, EV, code); } catch (Throwable t) {}
    try { Thread.sleep(70); } catch (InterruptedException e) {}
    try { if (KEYUP != null) KEYUP.invoke(app, EV, code); } catch (Throwable t) {}
    int px = -1, py = -1, pf = -1, stable = 0;
    for (int i = 0; i < 45; i++) {
      try { Thread.sleep(110); } catch (InterruptedException e) {}
      int x = cx(), y = cy(), ff = fl();
      if (x == px && y == py && ff == pf) { if (++stable >= 2) break; } else stable = 0;
      px = x; py = y; pf = ff; }
    try { Thread.sleep(140); } catch (InterruptedException e) {}
    return !(cx() == x0 && cy() == y0 && fl() == f0); }
  static void shot(String path) {
    try { Rectangle scr = new Rectangle(Toolkit.getDefaultToolkit().getScreenSize());
      BufferedImage img = ROBOT.createScreenCapture(scr);
      javax.imageio.ImageIO.write(img, "png", new File(path));
      log("  截图 -> " + path); } catch (Throwable t) { log("  截图失败 " + t); } }
  static boolean at(int tf, int tx, int ty) { return fl() == tf && cx() == tx && cy() == ty; }

  public static void main(String[] a) throws Exception {
    LOG = new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]), "UTF-8"));
    String keys = a[1], shotDir = a[2], csv = a[3];
    ROBOT = new Robot();
    app = (Applet) Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new RunApplet.Stub());
    KEYDOWN = app.getClass().getMethod("keyDown", Event.class, int.class);
    try { KEYUP = app.getClass().getMethod("keyUp", Event.class, int.class); } catch (Throwable t) { KEYUP = null; }
    EV = new Event(app, System.currentTimeMillis(), Event.KEY_PRESS, 0, 0, 0, 0);
    Frame fr = new Frame("mota"); fr.setLayout(new BorderLayout()); fr.add(app, BorderLayout.CENTER);
    fr.setBounds(0, 0, 820, 540); fr.setVisible(true); app.init(); app.start();
    Field cf = f("imgCrop"); cf.setAccessible(true);
    long t0 = System.currentTimeMillis();
    while (System.currentTimeMillis() - t0 < 180000) { if (Array.get(cf.get(app), 100) != null) break; Thread.sleep(300); }
    log("贴图就绪 " + ((System.currentTimeMillis() - t0) / 1000) + "s");
    Thread.sleep(4000);
    for (int i = 0; i < 8; i++) { enter(13); Thread.sleep(1200); if (arrA("mapObject", 66, 118) > 0 && cx() + cy() > 0) break; }
    log("起点 " + stats());
    if (!(fl() == 1 && cx() == 6 && cy() == 11)) { log("!! 起点异常，应为 1F(6,11)"); shot(shotDir + "/ERROR_start.png"); LOG.close(); System.exit(3); }
    List<int[]> rows = new ArrayList<>();
    for (String line : Files.readAllLines(Paths.get(csv))) {
      String[] p = line.split(",", -1);
      if (p.length > 3 && p[0].matches("\\d+")) rows.add(new int[]{Integer.parseInt(p[1]), Integer.parseInt(p[2]), Integer.parseInt(p[3])}); }
    log("csv 目标点数 " + rows.size() + "  按键数 " + keys.length());
    new File(shotDir).mkdirs();
    int lastF = 1;
    for (int i = 0; i < keys.length(); i++) {
      int step = i + 1;
      if (step > rows.size()) { log("按键多于csv步数，停"); break; }
      int[] t = rows.get(step - 1);
      char ch = keys.charAt(i), dir = Character.toLowerCase(ch);
      if (Character.isUpperCase(ch)) { pressWait(dir); }        // 开门第一下：开门不动
      pressWait(dir);
      boolean ok = at(t[0], t[1], t[2]);
      for (int tries = 0; !ok && tries < 10; tries++) {
        if (tries % 2 == 0) pressWait(dir); else enter(13);      // 补按方向 / 清消息·推对话
        try { Thread.sleep(400); } catch (InterruptedException e) {}
        ok = at(t[0], t[1], t[2]); }
      if (!ok) { log("!! 第" + step + "步未达 目标=" + Arrays.toString(t) + " 实际 " + stats());
        shot(shotDir + "/ERROR_step" + step + ".png"); break; }
      log(String.format("%3d %c -> (%d,%d,%d) %s", step, ch, fl(), cx(), cy(), stats().replaceFirst("^f\\d+ \\S+ ", "")));
      if (fl() != lastF) { Thread.sleep(800); shot(String.format("%s/f%02d_step%03d.png", shotDir, fl(), step)); lastF = fl(); }
    }
    log("终 " + stats());
    LOG.close(); System.exit(0);
  }
}
