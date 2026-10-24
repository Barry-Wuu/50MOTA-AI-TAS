import java.applet.Applet;
import java.applet.AppletContext;
import java.applet.AppletStub;
import java.applet.AudioClip;
import java.awt.Event;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.lang.reflect.Array;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.URL;
import java.util.Enumeration;
import java.util.Iterator;

/** 探针：dump 空房间(band5/slot0) 的 map/mapObject/mapAttribute，确认事件后勇者如何离开 */
public class Probe8 {
  static Applet app;
  static class Stub implements AppletStub, AppletContext {
    public boolean isActive() { return true; }
    public URL getDocumentBase() { try { return new URL("file:."); } catch (Exception e) { return null; } }
    public URL getCodeBase() { try { return new URL("file:."); } catch (Exception e) { return null; } }
    public String getParameter(String n) { return null; }
    public AppletContext getAppletContext() { return this; }
    public void appletResize(int w, int h) {}
    public AudioClip getAudioClip(URL u) { return new AudioClip() { public void play() {} public void loop() {} public void stop() {} }; }
    public Image getImage(URL u) { return new BufferedImage(32, 32, BufferedImage.TYPE_INT_RGB); }
    public Applet getApplet(String n) { return null; }
    public Enumeration<Applet> getApplets() { return new Enumeration<Applet>() { public boolean hasMoreElements() { return false; } public Applet nextElement() { return null; } }; }
    public void showDocument(URL u) {}
    public void showDocument(URL u, String t) {}
    public void showStatus(String s) {}
    public void setStream(String k, java.io.InputStream s) {}
    public java.io.InputStream getStream(String k) { return null; }
    public Iterator<String> getStreamKeys() { return new Iterator<String>() { public boolean hasNext() { return false; } public String next() { return null; } public void remove() {} }; }
  }
  static Field f(String n) { try { Field x = app.getClass().getDeclaredField(n); x.setAccessible(true); return x; } catch (Throwable t) { return null; } }
  static int arrA(String fld, int r, int c) {
    try { Field x = f(fld); Object row = Array.get(x.get(app), r); Object e = Array.get(row, c);
      return (e instanceof Character) ? (int) (char) (Character) e : ((Number) e).intValue(); } catch (Throwable t) { return -1; }
  }
  static int gi(String n) {
    try { Field x = f(n); Object v = x.get(app);
      if (v instanceof Character) return (int) (char) (Character) v;
      if (v instanceof Boolean) return ((Boolean) v) ? 1 : 0;
      return ((Number) v).intValue(); } catch (Throwable t) { return 0; }
  }

  public static void main(String[] a) throws Exception {
    app = (Applet) Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new Stub());
    Method KEYDOWN = app.getClass().getMethod("keyDown", Event.class, int.class);
    Method PAINT = app.getClass().getMethod("paint", Graphics.class);
    Event EV = new Event(app, System.currentTimeMillis(), Event.KEY_PRESS, 0, 0, 0, 0);
    Graphics DUMMY = new BufferedImage(820, 520, BufferedImage.TYPE_INT_RGB).getGraphics();
    app.init();
    // 复刻 start() 标志
    String[] zeros = {"yesnoNumber","yesnoJudge","mapFlagErase","messageFlag","messageFlag2","messageFlag3",
        "yusyaFlag","openningFlag","saidanFlag","menuFlag","itemKeyFlag","attackFlag","scoreFlag",
        "saveFlag","popupFlag","UpKey","DownKey","LeftKey","RightKey","focusFlag","countRepaint",
        "movingSkip","paintSkip","repaintSkip","currentKey"};
    for (String n : zeros) { Field x = f(n); if (x != null) { if (x.getType() == boolean.class) x.setBoolean(app, false); else x.setInt(app, 0); } }
    String[] ones = {"inputKey","mapFlagAll","configFlag","animaFlag"};
    for (String n : ones) { Field x = f(n); if (x != null) { if (x.getType() == boolean.class) x.setBoolean(app, true); else x.setInt(app, 1); } }
    for (Field x : app.getClass().getDeclaredFields()) {
      if (Image.class.isAssignableFrom(x.getType()) && !x.getType().isArray()) {
        x.setAccessible(true);
        int w = 820, h = 520; String n = x.getName();
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
    // 过加载：paint 第一帧加载数据
    for (int i = 0; i < 5; i++) PAINT.invoke(app, DUMMY);
    System.out.println("HP=" + arrA("mapObject",66,118) + " mapX=" + gi("mapX") + " mapY=" + gi("mapY"));

    // ===== dump 空房间 band5/slot0：全局 rows 65-77, cols 0-12 =====
    System.out.println("=== 空房间 map（全局 rows 65-77 × cols 0-12）===");
    for (int r = 65; r <= 77; r++) {
      StringBuilder sb = new StringBuilder();
      for (int c = 0; c <= 12; c++) sb.append(String.format("%5d", arrA("map", r, c)));
      System.out.println(sb);
    }
    System.out.println("=== 空房间 mapObject ===");
    for (int r = 65; r <= 77; r++) {
      StringBuilder sb = new StringBuilder();
      for (int c = 0; c <= 12; c++) sb.append(String.format("%5d", arrA("mapObject", r, c)));
      System.out.println(sb);
    }
    // 对每个不同 tile 打印其属性（重点 [3] 地形分类、[16][17] warp）
    System.out.println("=== 空房间 tile 属性（非0 tile）===");
    java.util.TreeSet<Integer> tiles = new java.util.TreeSet<>();
    for (int r = 65; r <= 77; r++) for (int c = 0; c <= 12; c++) tiles.add(arrA("map", r, c));
    for (int t : tiles) {
      if (t <= 0) continue;
      StringBuilder sb = new StringBuilder("tile " + t + ": ");
      for (int k = 0; k < 20; k++) {
        try { Field x = f("mapAttribute"); Object row = Array.get(x.get(app), t); Object e = Array.get(row, k);
          sb.append(k + "=" + ((e instanceof Character) ? (int)(char)(Character)e : ((Number)e).intValue()) + " "); } catch (Throwable ex) { sb.append(k + "=? "); }
      }
      System.out.println(sb);
    }
    // mapAttribute[116] 详细（3F(5,9) 的 warp 瓦片）
    System.out.println("=== mapAttribute[116]（3F(5,9) 事件瓦片）===");
    for (int k = 0; k < 20; k++) System.out.print("[" + k + "]=" + arrA("mapAttribute", 116, k) + " ");
    System.out.println();
    // 2F(2,7)/2F(3,7)/2F(3,8) 当前 tile
    System.out.println("2F(2,7) tile=" + arrA("map", 7, 15) + " obj=" + arrA("mapObject", 7, 15));
    System.out.println("2F(3,7) tile=" + arrA("map", 7, 16) + " obj=" + arrA("mapObject", 7, 16));
    System.out.println("2F(3,8) tile=" + arrA("map", 8, 16) + " obj=" + arrA("mapObject", 8, 16));
    System.out.println("3F(5,9) tile=" + arrA("map", 9, 31) + " obj=" + arrA("mapObject", 9, 31));
    System.exit(0);
  }
}
