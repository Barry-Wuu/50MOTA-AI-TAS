import java.applet.*; import java.awt.*; import java.io.*; import java.lang.reflect.*;
public class Drive2 {
  static Applet app; static Field F(String n) throws Exception { Field f=app.getClass().getDeclaredField(n); f.setAccessible(true); return f; }
  static int g(String n) throws Exception { Object v=F(n).get(app); return v instanceof Character?(int)(char)(Character)v:((Number)v).intValue(); }
  static void p(String n,int v) throws Exception { Field f=F(n); if(f.getType()==boolean.class) f.setBoolean(app,v!=0); else f.setInt(app,v); }
  static void key(int ck,String flag) throws Exception { p("currentKey",ck); p(flag,1); Thread.sleep(450); p(flag,0); Thread.sleep(650); }
  static PrintWriter LOG;
  static void log(String m){ LOG.println(m); LOG.flush(); log(m); }
  public static void main(String[] x) throws Exception {
    LOG=new PrintWriter(new OutputStreamWriter(new FileOutputStream(a.length>0?a[0]:"drive2_run.log"),"UTF-8"));
    app=(Applet)Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new RunApplet.Stub());
    Frame fr=new Frame("d"); fr.setSize(820,520); fr.add(app); fr.setVisible(true);
    app.init(); app.start();
    Object crops=F("imgCrop").get(app); long t0=System.currentTimeMillis();
    while(System.currentTimeMillis()-t0<25000){ if(Array.get(crops,100)!=null) break; Thread.sleep(300);} Thread.sleep(2500);
    p("messageFlag",0); p("dialogFlag",0); p("inputKey",1);
    // 放到 1F：block(mapX=0,mapY=0)，角色格 (2,1) 单位=px/8 → charaX=10,charaY=5
    p("mapX",0); p("mapY",0); p("charaX",10); p("charaY",5);
    p("charaXold",10); p("charaYold",5);
    log("start: floorIdx="+ (g("mapY")*10+g("mapX")+1) +" cell=("+g("charaX")/5+","+g("charaY")/5+")");
    for(int i=0;i<10;i++){
      key(4,"LeftKey");
      int fi=g("mapY")*10+g("mapX")+1;
      log("step"+i+" Left -> floorIdx="+fi+" cell=("+(g("charaX")/5)+","+(g("charaY")/5)+") strNumber="+g("strNumber")+" msgFlag="+g("messageFlag"));
      if(fi!=1 && fi!=11) { // 已发生楼层跳转
        for(int j=0;j<8 && (g("mapY")*10+g("mapX")+1)==fi;j++){ key(8,"UpKey"); key(2,"DownKey"); }
        log("   after up/down -> floorIdx="+(g("mapY")*10+g("mapX")+1)+" cell=("+(g("charaX")/5)+","+(g("charaY")/5)+")");
        break;
      }
    }
    System.exit(0);
  }
}
