import java.applet.*; import java.awt.*; import java.io.*; import java.lang.reflect.*;
public class Drive3 {
  static Applet app; static PrintWriter LOG;
  static Field F(String n) throws Exception { Field f=app.getClass().getDeclaredField(n); f.setAccessible(true); return f; }
  static int g(String n) throws Exception { Object v=F(n).get(app); return v instanceof Character?(int)(char)(Character)v:((Number)v).intValue(); }
  static void p(String n,int v) throws Exception { Field f=F(n); if(f.getType()==boolean.class) f.setBoolean(app,v!=0); else f.setInt(app,v); }
  static int cellX() throws Exception { return g("charaX")/5; } static int cellY() throws Exception { return g("charaY")/5; }
  static int floor() throws Exception { return g("mapY")*10+g("mapX")+1; }
  static int mget(String fld,int r,int c) throws Exception { Object row=Array.get(F(fld).get(app),r); return (int)(char)Array.get(row,c); }
  static void log(String m){ LOG.println(m); LOG.flush(); }
  public static void main(String[] x) throws Exception {
    LOG=new PrintWriter(new OutputStreamWriter(new FileOutputStream(x[0]),"UTF-8"));
    app=(Applet)Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new RunApplet.Stub());
    Frame fr=new Frame("d"); fr.setSize(820,520); fr.add(app); fr.setVisible(true);
    app.init(); app.start();
    Object crops=F("imgCrop").get(app); long t0=System.currentTimeMillis();
    while(System.currentTimeMillis()-t0<25000){ if(Array.get(crops,100)!=null) break; Thread.sleep(300);} Thread.sleep(2500);
    p("mapX",0); p("mapY",0); p("charaX",10); p("charaY",5); p("charaXold",10); p("charaYold",5);
    log("boot: floor="+floor()+" cell=("+cellX()+","+cellY()+") strNumber="+g("strNumber"));
    for(int i=0;i<24;i++){
      p("currentKey",4); p("LeftKey",1); Thread.sleep(320); p("LeftKey",0); Thread.sleep(430);
      int r=g("mapY")*13+cellY(), c=g("mapX")*13+cellX();
      log("i="+i+" floor="+floor()+" cell=("+cellX()+","+cellY()+") charaX="+g("charaX")+" charaY="+g("charaY")
          +" map["+r+","+c+"]="+mget("map",r,c)+" obj="+mget("mapObject",r,c)+" strNumber="+g("strNumber")+" msg="+g("messageFlag"));
      if(floor()!=1){ log("!! 楼层序号变了 -> floor="+floor()+" (mapX="+g("mapX")+",mapY="+g("mapY")+") cell=("+cellX()+","+cellY()+")"); break; }
    }
    log("end"); LOG.close(); System.exit(0);
  }
}
