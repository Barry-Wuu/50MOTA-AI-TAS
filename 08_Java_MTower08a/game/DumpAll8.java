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
import java.util.Enumeration;
import java.util.Iterator;

/** 从 08 Java 版本体导出全部 50 层权威地图数据（map/mapObject/mapAttribute/mapFrame）→ map_java8.json */
public class DumpAll8 {
  static Applet app;
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

  static Field f(String n) throws Exception { Field x = app.getClass().getDeclaredField(n); x.setAccessible(true); return x; }
  static int cell(String fld, int r, int c) throws Exception {
    Object row = Array.get(f(fld).get(app), r); Object e = Array.get(row, c);
    return (e instanceof Character) ? (int) (char) (Character) e : ((Number) e).intValue();
  }
  static int dim0(String fld) throws Exception { return Array.getLength(f(fld).get(app)); }
  static int dim1(String fld) throws Exception { return Array.getLength(Array.get(f(fld).get(app), 0)); }

  public static void main(String[] a) throws Exception {
    PrintWriter out = new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]), "UTF-8"));
    app = (Applet) Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new Stub());
    KEYDOWN = app.getClass().getMethod("keyDown", Event.class, int.class);
    KEYUP = app.getClass().getMethod("keyUp", Event.class, int.class);
    PAINT = app.getClass().getMethod("paint", Graphics.class);
    EV = new Event(app, System.currentTimeMillis(), Event.KEY_PRESS, 0, 0, 0, 0);
    DUMMY = new BufferedImage(820, 520, BufferedImage.TYPE_INT_RGB).getGraphics();
    app.init();
    // 手动初始化缓冲（同 Headless8）
    for (Field x : app.getClass().getDeclaredFields()) {
      if (Image.class.isAssignableFrom(x.getType()) && !x.getType().isArray()) {
        x.setAccessible(true);
        int w = 820, h = 520; String n = x.getName();
        if (n.contains("Map")) { w = 40; h = 40; } else if (n.equals("imgBuffCharaX")) { w = 80; h = 40; }
        else if (n.equals("imgBuffCharaY")) { w = 40; h = 80; } else if (n.equals("imgBuff2")) { w = 120; h = 120; }
        else if (n.equals("imgBuff3")) { w = 40; h = 40; } else if (n.equals("imgBuffopen")) { w = 820; h = 520; }
        else if (n.contains("Status")) { w = 520; h = 520; }
        x.set(app, new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB));
      }
    }
    for (Field x : app.getClass().getDeclaredFields()) {
      if (Graphics.class.isAssignableFrom(x.getType())) {
        x.setAccessible(true);
        Field img = f(x.getName().equals("gBuffopen") ? "imgBuffopen" : "imgBuff" + x.getName().substring(5));
        x.set(app, (img != null && img.get(app) != null) ? ((Image) img.get(app)).getGraphics() : new BufferedImage(820, 520, BufferedImage.TYPE_INT_RGB).getGraphics());
      }
    }
    String[] ones = {"inputKey", "mapFlagAll", "configFlag", "animaFlag"};
    for (String n : ones) { Field x = f(n); if (x.getType() == boolean.class) x.setBoolean(app, true); else x.setInt(app, 1); }

    for (int i = 0; i < 5; i++) { PAINT.invoke(app, DUMMY); Thread.sleep(50); }   // 触发 loadMapData

    int mRows = dim0("map"), mCols = dim1("map");
    out.println("{");
    out.println("  \"_meta\": {\"source\": \"08_Java_MTower08a MTower.class 运行时字段\", \"mapRows\": " + mRows + ", \"mapCols\": " + mCols + "},");
    // mapFrame（楼层 -> map/mapObject 起始行列）
    out.println("  \"mapFrame\": [");
    int fr0 = dim0("mapFrame"), fr1 = dim1("mapFrame");
    for (int r = 0; r < fr0; r++) {
      out.print("    [");
      for (int c = 0; c < fr1; c++) out.print(cell("mapFrame", r, c) + (c < fr1 - 1 ? ", " : ""));
      out.println("]" + (r < fr0 - 1 ? "," : ""));
    }
    out.println("  ],");
    // 属性表：mapAttribute（地形属性，含 warp [16]/[17]）+ objectAttribute（物件属性）
    out.println("  \"mapAttribute\": [");
    for (int r = 0; r < 200; r++) {
      out.print("    [");
      for (int c = 0; c < 40; c++) {
        Field x = f("mapAttribute"); Object row = Array.get(x.get(app), r);
        out.print(Array.get(row, c) + (c < 39 ? ", " : ""));
      }
      out.println("]" + (r < 199 ? "," : ""));
    }
    out.println("  ],");
    out.println("  \"objectAttribute\": [");
    for (int r = 0; r < 200; r++) {
      out.print("    [");
      for (int c = 0; c < 40; c++) {
        Field x = f("objectAttribute"); Object row = Array.get(x.get(app), r);
        out.print(Array.get(row, c) + (c < 39 ? ", " : ""));
      }
      out.println("]" + (r < 199 ? "," : ""));
    }
    out.println("  ],");
    // mapFrame 是贴图裁剪表，与楼层无关；楼层定位 = band*13+y, slot*13+x
    out.println("  \"floors\": {");
    StringBuilder sb = new StringBuilder();
    for (int fl = 1; fl <= 50; fl++) {
      int band = (fl - 1) / 10, slot = (fl - 1) % 10;
      int rowBase = band * 13, colBase = slot * 13;
      sb.append("    \"").append(fl).append("\": {\"map\": [");
      for (int y = 0; y < 13; y++) {
        sb.append("[");
        for (int x = 0; x < 13; x++) sb.append(cell("map", rowBase + y, colBase + x)).append(x < 12 ? "," : "");
        sb.append("]").append(y < 12 ? ", " : "");
      }
      sb.append("], \"obj\": [");
      for (int y = 0; y < 13; y++) {
        sb.append("[");
        for (int x = 0; x < 13; x++) sb.append(cell("mapObject", rowBase + y, colBase + x)).append(x < 12 ? "," : "");
        sb.append("]").append(y < 12 ? ", " : "");
      }
      sb.append("]}").append(fl < 50 ? "," : "").append("\n");
    }
    out.print(sb);
    out.println("  }");
    out.println("}");
    out.close();
    System.out.println("dumped map " + mRows + "x" + mCols + " -> " + a[0]);
  }
}
