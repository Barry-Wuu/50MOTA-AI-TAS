import java.applet.Applet;
import java.applet.AppletContext;
import java.applet.AppletStub;
import java.applet.AudioClip;
import java.awt.*;
import java.net.URL;
import java.util.Enumeration;
import java.util.Iterator;
import javax.swing.JFrame;

public class RunApplet {
    static class Stub implements AppletStub, AppletContext {
        Applet applet;
        public boolean isActive() { return true; }
        public URL getDocumentBase() { try { return new URL("file:."); } catch (Exception e) { return null; } }
        public URL getCodeBase() { try { return new URL("file:."); } catch (Exception e) { return null; } }
        public String getParameter(String n) { return null; }
        public AppletContext getAppletContext() { return this; }
        public void appletResize(int w, int h) {}
        public AudioClip getAudioClip(URL u) { return null; }
        public Image getImage(URL u) { return Toolkit.getDefaultToolkit().getImage(u); }
        public Applet getApplet(String n) { return null; }
        public Enumeration<Applet> getApplets() { return new Enumeration<Applet>() {
            public boolean hasMoreElements() { return false; }
            public Applet nextElement() { return null; } }; }
        public void showDocument(URL u) {}
        public void showDocument(URL u, String t) {}
        public void showStatus(String s) {}
        public void setStream(String k, java.io.InputStream s) {}
        public java.io.InputStream getStream(String k) { return null; }
        public Iterator<String> getStreamKeys() { return new Iterator<String>() {
            public boolean hasNext() { return false; } public String next() { return null; } public void remove() {} }; }
    }
    public static void main(String[] args) throws Exception {
        String cls = args.length > 0 ? args[0] : "MTower";
        int w = args.length > 1 ? Integer.parseInt(args[1]) : 820;
        int h = args.length > 2 ? Integer.parseInt(args[2]) : 520;
        Applet a = (Applet) Class.forName(cls).getDeclaredConstructor().newInstance();
        Stub stub = new Stub();
        stub.applet = a;
        a.setStub(stub);
        JFrame f = new JFrame("Magic Tower Java");
        f.setLayout(new BorderLayout());
        f.add(a, BorderLayout.CENTER);
        f.setSize(w, h);
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        a.init();
        f.setVisible(true);
        a.start();
    }
}
