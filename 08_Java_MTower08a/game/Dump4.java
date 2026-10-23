import java.applet.*; import java.awt.*; import java.io.*; import java.lang.reflect.*;
public class Dump4 {
  static Object get(Object o,String n) throws Exception { Field f=o.getClass().getDeclaredField(n); f.setAccessible(true); return f.get(o); }
  static String jstr(String s){ if(s==null) return "null"; StringBuilder b=new StringBuilder("\""); for(char c: s.toCharArray()){ if(c=='"') b.append("\\\""); else if(c=='\\') b.append("\\\\"); else if(c=='\n') b.append("\\n"); else if(c<0x20||c>0xFFFD) b.append(String.format("\\u%04x",(int)c)); else b.append(c);} return b.append("\"").toString(); }
  static String val(Object v){
    if(v==null) return "null";
    Class<?> c=v.getClass();
    if(c.isArray()){
      int n=Array.getLength(v);
      if(n>0 && Array.get(v,0)!=null && Array.get(v,0).getClass().isArray()){
        int m=Array.getLength(Array.get(v,0));
        StringBuilder b=new StringBuilder("{\"_2d\":[" + n + "," + m + "],\"data\":[");
        for(int i=0;i<n;i++){ Object row=Array.get(v,i); int mm=row==null?0:Array.getLength(row); b.append("[");
          for(int j=0;j<mm;j++){ Object e=row==null?null:Array.get(row,j); if(j>0)b.append(",");
            if(e instanceof Character) b.append((int)(char)(Character)e);
            else if(e instanceof Number || e instanceof Boolean) b.append(String.valueOf(e));
            else b.append(jstr(String.valueOf(e)));
          } b.append("]"); if(i<n-1)b.append(","); }
        return b.append("]}").toString();
      }
      StringBuilder b=new StringBuilder("{\"_1d\":" + n + ",\"data\":[");
      for(int i=0;i<n;i++){ Object e=Array.get(v,i); if(i>0)b.append(",");
        if(e instanceof Character) b.append((int)(char)(Character)e); else if(c.getComponentType()==String.class) b.append(jstr((String)e)); else b.append(String.valueOf(e)); }
      return b.append("]}").toString();
    }
    if(v instanceof Character) return String.valueOf((int)(char)(Character)v);
    if(v instanceof Image || v instanceof Canvas || v instanceof Toolkit) return "\"<"+c.getSimpleName()+">\"";
    if(c==String.class) return jstr((String)v);
    if(v instanceof Number || v instanceof Boolean) return String.valueOf(v);
    return jstr(String.valueOf(v));
  }
  public static void main(String[] a) throws Exception {
    Applet app=(Applet)Class.forName("MTower").getDeclaredConstructor().newInstance();
    app.setStub(new RunApplet.Stub());
    Frame f=new Frame("d"); f.setSize(820,520); f.add(app); f.setVisible(true);
    app.init(); app.start();
    Object crops=get(app,"imgCrop"); long t0=System.currentTimeMillis();
    while(System.currentTimeMillis()-t0<25000){ if(Array.get(crops,100)!=null) break; Thread.sleep(300);} Thread.sleep(1500);
    PrintWriter pw=new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[1]),"UTF-8"));
    pw.print("{\"fields\":{");
    Field[] fs=app.getClass().getDeclaredFields(); int k=0;
    for(Field fl: fs){ fl.setAccessible(true); Object v; try{ v=fl.get(app);}catch(Throwable t){continue;}
      if(v==null && !fl.getType().isPrimitive()) continue;
      if(k++>0)pw.print(",");
      pw.print(jstr(fl.getName())+":"+val(v)); }
    pw.print("},\"methods\":[");
    Method[] ms=app.getClass().getDeclaredMethods();
    for(int i=0;i<ms.length;i++){ Method m=ms[i]; if(i>0)pw.print(",");
      pw.print(jstr(m.getName()+"("+ (ms[i].getParameterTypes().length) +"):"+m.getReturnType().getSimpleName())); }
    pw.print("]}"); pw.close();
    System.out.println("dump4 fields="+fs.length+" methods="+ms.length);
    System.exit(0);
  }
}
