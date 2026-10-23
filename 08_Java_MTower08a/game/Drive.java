import java.applet.*; import java.awt.*; import java.io.*; import java.lang.reflect.*;
public class Drive {
  static Applet app; static Field[] FS;
  static Field F(String n){ try{ return app.getClass().getDeclaredField(n);}catch(Exception e){ return null;} }
  static Object g(String n) throws Exception { Field f=F(n); f.setAccessible(true); return f.get(app); }
  static void p(String n,Object v) throws Exception { Field f=F(n); f.setAccessible(true);
      if(f.getType()==boolean.class) f.setBoolean(app,((Boolean)v).booleanValue()); else f.setInt(app,((Number)v).intValue()); }
  static String snap() throws Exception { StringBuilder b=new StringBuilder("{"); boolean first=true;
    for(Field f: FS){ if(f.getType().isPrimitive() && !Modifier.isStatic(f.getModifiers())){ f.setAccessible(true);
        Object v=f.get(app); if(!first)b.append(","); first=false;
        b.append('"').append(f.getName()).append("\":").append(f.getType()==boolean.class?String.valueOf(v):(v instanceof Character?String.valueOf((int)(char)(Character)v):String.valueOf(v))); } }
    return b.append("}").toString(); }
  public static void main(String[] a) throws Exception {
    app=(Applet)Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new RunApplet.Stub());
    Frame fr=new Frame("d"); fr.setSize(820,520); fr.add(app); fr.setVisible(true);
    app.init(); app.start();
    Object crops=g("imgCrop"); long t0=System.currentTimeMillis();
    while(System.currentTimeMillis()-t0<25000){ if(Array.get(crops,100)!=null) break; Thread.sleep(300);} Thread.sleep(2500);
    FS=app.getClass().getDeclaredFields();
    PrintWriter out=new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[1]),"UTF-8"));
    out.println("{\"boot\":"+snap()+"}"); out.flush();
    p("messageFlag",Boolean.FALSE); p("inputKey",Boolean.TRUE); p("dialogFlag",0);
    String[][] dirs={{"UpKey","8"},{"DownKey","2"},{"LeftKey","4"},{"RightKey","6"}};
    out.println(",\"steps\":[");
    for(int i=0;i<12;i++){
      String dk=dirs[i%4][0]; int ck=Integer.parseInt(dirs[i%4][1]);
      p("currentKey",ck); p(dk,Boolean.TRUE); Thread.sleep(500); p(dk,Boolean.FALSE); Thread.sleep(700);
      if(i>0) out.println(",");
      out.println("{\"key\":\""+dk+"\",\"f\":"+snap()+"}");
      out.flush();
      System.out.println("step "+i+" "+dk+" mapX="+g("mapX")+" mapY="+g("mapY")+" charaX="+g("charaX")+" charaY="+g("charaY")+" dialogFlag="+g("dialogFlag")+" msg="+g("messageFlag"));
    }
    out.println("]"); System.out.println("drive done");
    System.exit(0);
  }
}
