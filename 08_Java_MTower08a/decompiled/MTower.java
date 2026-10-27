/*
 * Decompiled with CFR 0.152.
 */
import java.applet.Applet;
import java.applet.AudioClip;
import java.awt.Color;
import java.awt.Component;
import java.awt.Event;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Frame;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.MediaTracker;
import java.awt.Menu;
import java.awt.MenuItem;
import java.awt.MenuShortcut;
import java.awt.PopupMenu;
import java.awt.image.CropImageFilter;
import java.awt.image.FilteredImageSource;
import java.awt.image.MemoryImageSource;
import java.awt.image.PixelGrabber;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;

public class MTower
extends Applet
implements Runnable {
    PopupMenu popup;
    Menu submenu1;
    Menu submenu2;
    Menu submenu3;
    Menu submenu4;
    Menu submenu5;
    Menu submenu6;
    Menu subfont1;
    Menu subfont2;
    Menu subfont3;
    MenuItem menuitem4;
    MenuItem menuitem5;
    MenuItem subload1;
    MenuItem subload2;
    MenuItem subload3;
    MenuItem subload4;
    MenuItem subload5;
    MenuItem subload6;
    MenuItem subload7;
    MenuItem subload8;
    MenuItem subsave1;
    MenuItem subsave2;
    MenuItem subsave3;
    MenuItem subsave4;
    MenuItem subsave5;
    MenuItem subsave6;
    MenuItem subsave7;
    MenuItem subsave8;
    MenuItem subsound1;
    MenuItem subsound2;
    MenuItem subsound3;
    MenuItem subBGM1;
    MenuItem subBGM2;
    MenuItem subBGM3;
    MenuItem LangENG;
    MenuItem LangJPN;
    MenuItem subfont11;
    MenuItem subfont12;
    MenuItem subfont13;
    MenuItem subfont14;
    MenuItem subfont21;
    MenuItem subfont22;
    MenuItem subfont23;
    MenuItem subfont31;
    MenuItem subfont32;
    ZAboutMT d1;
    ZOkCanDialog d2;
    ZscoreMTDialog d3;
    ZLabelDialog d4;
    int charaX;
    int charaY;
    int mapX;
    int mapY;
    int flag3F = 0;
    int sai = 0;
    int sai2 = 0;
    int oldsai = 0;
    int monsflag = 0;
    int VerX = 0;
    int VerY = 0;
    int xp = 150;
    int yp = 0;
    int itemFlag = 0;
    int itemNUM = 0;
    final int ATR_0 = 0;
    final int ATR_CROP1 = 1;
    final int ATR_CROP2 = 2;
    final int ATR_TYPE = 3;
    final int ATR_MODE = 4;
    final int ATR_STRING = 5;
    final int ATR_X = 6;
    final int ATR_Y = 7;
    final int ATR_X2 = 8;
    final int ATR_Y2 = 9;
    final int ATR_ENERGY = 10;
    final int ATR_STRENGTH = 11;
    final int ATR_DEFENCE = 12;
    final int ATR_GOLD = 13;
    final int ATR_ITEM = 14;
    final int ATR_NUMBER = 15;
    final int ATR_JUMP_X = 16;
    final int ATR_JUMP_Y = 17;
    final int ATR_SOUND = 19;
    final int MAP_STREET = 0;
    final int MAP_WALL = 1;
    final int MAP_LOCALGATE = 2;
    final int OBJECT_NORMAL = 0;
    final int OBJECT_MESSAGE = 1;
    final int OBJECT_STATUS = 3;
    final int OBJECT_ITEM = 4;
    final int OBJECT_DOOR = 5;
    final int OBJECT_MONSTER = 6;
    final int OBJECT_SAIDAN = 7;
    final int OBJECT_SCORE = 11;
    final int OBJECT_SELL = 14;
    final int OBJECT_BUY = 15;
    final int OBJECT_KEY = 8;
    final int CONFIG_HI_COUNT = 17;
    final int LOADING_ALL = 0;
    final int YESNO_NONE = 0;
    final int YESNO_YES = 1;
    final int YESNO_NO = 2;
    final int YESNO_WWAH = 3;
    final int YESNO_RESTART = 5;
    final int YESNO_SELL = 6;
    final int YESNO_BUY = 7;
    final int YESNO_SAIDAN = 9;
    final int CROP_YES = 17;
    final int CROP_NO = 18;
    final int CROP_YES2 = 19;
    final int CROP_NO2 = 20;
    final int CROP_ENERGY = 21;
    final int CROP_STRENGTH = 22;
    final int CROP_DEFENCE = 23;
    final int CROP_GOLD = 24;
    final int CROP_BOM = 25;
    final int CROP_WAKU1 = 26;
    final int CROP_WAKU2 = 27;
    final int Screenwidth = 820;
    final int Screenheight = 520;
    int charaXold;
    int charaYold;
    int movePlus;
    int getcoin;
    String[][] strMessage = new String[2][400];
    int strNumber;
    int yesnoNumber;
    int yesnoJudge;
    int yesnoX;
    int yesnoY;
    boolean yesnoFlag;
    boolean messageFlag;
    boolean messageFlag2;
    int messageFlag3;
    boolean loadingFlag;
    boolean configFlag;
    boolean scoreFlag;
    boolean saveFlag;
    boolean popupFlag;
    boolean yusyaFlag;
    boolean openningFlag;
    boolean saidanFlag;
    boolean menuFlag;
    boolean itemKeyFlag;
    boolean focusFlag;
    boolean yanime = false;
    boolean endFlag = false;
    int dialogFlag = 0;
    int FileNo = 0;
    String FileName;
    String FontName;
    URL codeurl;
    boolean UpKey;
    boolean DownKey;
    boolean LeftKey;
    boolean RightKey;
    int currentKey;
    boolean inputKey;
    Thread timer;
    volatile boolean animaFlag;
    Zdata DFlag = new Zdata();
    int TimerCount;
    int countAnimation;
    int countRepaint;
    int waitCounter;
    boolean waitCounterFlag;
    MediaTracker tracker = new MediaTracker(this);
    Image imgMap;
    Image[] imgCrop = new Image[201];
    int cropID;
    int cropIDchara;
    Image imgBuff;
    Image imgBuffMap;
    Image imgBuffStatus;
    Image imgBuffStatus2;
    Image imgBuffCharaX;
    Image imgBuffCharaY;
    Image imgBuffyusya;
    Image imgBuff2;
    Image imgBuff3;
    Image imgBuffopen;
    Graphics gBuff;
    Graphics gBuffMap;
    Graphics gBuffStatus;
    Graphics gBuffStatus2;
    Graphics gBuffCharaX;
    Graphics gBuffCharaY;
    Graphics gBuffyusya;
    Graphics gBuff2;
    Graphics gBuff3;
    Graphics gBuffopen;
    int mdata;
    int mdataBuff;
    int XpBuff;
    int YpBuff;
    boolean[][] mapFlag = new boolean[13][13];
    boolean mapFlagAll;
    boolean mapFlagErase;
    boolean flagDisplayStatus;
    int movingSkip;
    int paintSkip;
    boolean repaintSkip;
    char[][] map = new char[78][130];
    char[][] mapObject = new char[78][130];
    int[][] objectAttribute = new int[200][40];
    int[][] mapAttribute = new int[200][40];
    int[][] mapFrame = new int[][]{{0, 40}, {40, 40}, {80, 40}, {0, 80}, {40, 80}, {80, 80}, {0, 120}, {40, 120}, {80, 120}, {120, 40}, {160, 40}, {200, 40}, {240, 40}, {120, 80}, {160, 80}, {200, 80}, {240, 80}, {120, 120}, {280, 40}, {360, 40}, {280, 80}, {320, 80}, {360, 80}, {280, 120}};
    int[] itemBox = new int[15];
    int[] chieOrb = new int[26];
    int chieNum;
    int itemStrength;
    int itemDefence;
    int score;
    int score2;
    String Name;
    int monsterEnergy;
    int monsterStrength;
    int monsterDefence;
    int monsterGold;
    int attackXp;
    int attackYp;
    int attackDouble = 1;
    boolean attackFlag;
    boolean attackFlagTurn;
    AudioClip[] audio = new AudioClip[50];
    Image simage;
    int oldMapData;
    int oldMapX;
    int oldMapY;
    int[] pixels1 = new int[1600];
    int[] pixels2 = new int[1600];
    int[] pixels3 = new int[1600];
    int[] pixels4 = new int[1600];
    int[] pixels5 = new int[1600];
    int[] pixels6 = new int[1600];

    public void init() {
        this.popup = new PopupMenu("Menu");
        this.submenu1 = new Menu("Load");
        MenuShortcut menuShortcut = new MenuShortcut(49);
        MenuShortcut menuShortcut2 = new MenuShortcut(50);
        MenuShortcut menuShortcut3 = new MenuShortcut(51);
        MenuShortcut menuShortcut4 = new MenuShortcut(52);
        MenuShortcut menuShortcut5 = new MenuShortcut(53);
        MenuShortcut menuShortcut6 = new MenuShortcut(54);
        MenuShortcut menuShortcut7 = new MenuShortcut(55);
        MenuShortcut menuShortcut8 = new MenuShortcut(56);
        this.subload1 = new MenuItem("Data 1", menuShortcut);
        this.subload2 = new MenuItem("Data 2", menuShortcut2);
        this.subload3 = new MenuItem("Data 3", menuShortcut3);
        this.subload4 = new MenuItem("Data 4", menuShortcut4);
        this.subload5 = new MenuItem("Data 5", menuShortcut5);
        this.subload6 = new MenuItem("Data 6", menuShortcut6);
        this.subload7 = new MenuItem("Data 7", menuShortcut7);
        this.subload8 = new MenuItem("Data 8", menuShortcut8);
        this.submenu1.add(this.subload1);
        this.submenu1.add(this.subload2);
        this.submenu1.add(this.subload3);
        this.submenu1.add(this.subload4);
        this.submenu1.add(this.subload5);
        this.submenu1.add(this.subload6);
        this.submenu1.add(this.subload7);
        this.submenu1.add(this.subload8);
        this.submenu2 = new Menu("Save");
        this.subsave1 = new MenuItem("Data 1");
        this.subsave2 = new MenuItem("Data 2");
        this.subsave3 = new MenuItem("Data 3");
        this.subsave4 = new MenuItem("Data 4");
        this.subsave5 = new MenuItem("Data 5");
        this.subsave6 = new MenuItem("Data 6");
        this.subsave7 = new MenuItem("Data 7");
        this.subsave8 = new MenuItem("Data 8");
        this.submenu2.add(this.subsave1);
        this.submenu2.add(this.subsave2);
        this.submenu2.add(this.subsave3);
        this.submenu2.add(this.subsave4);
        this.submenu2.add(this.subsave5);
        this.submenu2.add(this.subsave6);
        this.submenu2.add(this.subsave7);
        this.submenu2.add(this.subsave8);
        MenuShortcut menuShortcut9 = new MenuShortcut(87);
        MenuShortcut menuShortcut10 = new MenuShortcut(79);
        this.submenu3 = new Menu("Sound");
        this.subsound1 = new MenuItem("Wav On", menuShortcut9);
        this.subsound3 = new MenuItem("Au On");
        this.subsound2 = new MenuItem("Off", menuShortcut10);
        this.submenu3.add(this.subsound1);
        this.submenu3.add(this.subsound3);
        this.submenu3.add(this.subsound2);
        MenuShortcut menuShortcut11 = new MenuShortcut(77);
        MenuShortcut menuShortcut12 = new MenuShortcut(79);
        this.submenu4 = new Menu("BGM");
        this.subBGM1 = new MenuItem("Midi On", menuShortcut11);
        this.subBGM3 = new MenuItem("Au On");
        this.subBGM2 = new MenuItem("Off", menuShortcut12);
        this.submenu4.add(this.subBGM1);
        this.submenu4.add(this.subBGM3);
        this.submenu4.add(this.subBGM2);
        MenuShortcut menuShortcut13 = new MenuShortcut(69);
        MenuShortcut menuShortcut14 = new MenuShortcut(80);
        this.submenu5 = new Menu("Language");
        this.LangENG = new MenuItem("English", menuShortcut13);
        this.LangJPN = new MenuItem("Japanese", menuShortcut14);
        this.submenu5.add(this.LangENG);
        this.submenu5.add(this.LangJPN);
        MenuShortcut menuShortcut15 = new MenuShortcut(65);
        this.menuitem4 = new MenuItem("About Magic Tower", menuShortcut15);
        MenuShortcut menuShortcut16 = new MenuShortcut(82);
        this.menuitem5 = new MenuItem("Ranking", menuShortcut16);
        this.submenu6 = new Menu("Font");
        this.subfont1 = new Menu("Name");
        this.subfont2 = new Menu("Style");
        this.subfont3 = new Menu("Size");
        MenuShortcut menuShortcut17 = new MenuShortcut(84);
        this.subfont11 = new MenuItem("TimesRoman", menuShortcut17);
        MenuShortcut menuShortcut18 = new MenuShortcut(68);
        this.subfont12 = new MenuItem("Dialog", menuShortcut18);
        MenuShortcut menuShortcut19 = new MenuShortcut(72);
        this.subfont13 = new MenuItem("Helvetica", menuShortcut19);
        MenuShortcut menuShortcut20 = new MenuShortcut(67);
        this.subfont14 = new MenuItem("Courier", menuShortcut20);
        MenuShortcut menuShortcut21 = new MenuShortcut(78);
        this.subfont21 = new MenuItem("Normal", menuShortcut21);
        MenuShortcut menuShortcut22 = new MenuShortcut(66);
        this.subfont22 = new MenuItem("Bold", menuShortcut22);
        MenuShortcut menuShortcut23 = new MenuShortcut(73);
        this.subfont23 = new MenuItem("Italic", menuShortcut23);
        MenuShortcut menuShortcut24 = new MenuShortcut(76);
        this.subfont31 = new MenuItem("Large", menuShortcut24);
        MenuShortcut menuShortcut25 = new MenuShortcut(83);
        this.subfont32 = new MenuItem("Small", menuShortcut25);
        this.submenu6.add(this.subfont1);
        this.submenu6.add(this.subfont2);
        this.submenu6.add(this.subfont3);
        this.subfont1.add(this.subfont11);
        this.subfont1.add(this.subfont12);
        this.subfont1.add(this.subfont13);
        this.subfont1.add(this.subfont14);
        this.subfont2.add(this.subfont21);
        this.subfont2.add(this.subfont22);
        this.subfont2.add(this.subfont23);
        this.subfont3.add(this.subfont31);
        this.subfont3.add(this.subfont32);
        this.popup.add(this.submenu1);
        this.popup.addSeparator();
        this.popup.add(this.submenu2);
        this.popup.addSeparator();
        this.popup.add(this.menuitem5);
        this.popup.addSeparator();
        this.popup.add(this.submenu3);
        this.popup.addSeparator();
        this.popup.add(this.submenu4);
        this.popup.addSeparator();
        this.popup.add(this.submenu6);
        this.popup.addSeparator();
        this.popup.add(this.submenu5);
        this.popup.addSeparator();
        this.popup.add(this.menuitem4);
        this.add(this.popup);
        this.d1 = new ZAboutMT(new Frame());
        this.d2 = new ZOkCanDialog(new Frame());
        this.d3 = new ZscoreMTDialog(new Frame());
        this.d4 = new ZLabelDialog(new Frame(), "Input Name", true);
        this.requestFocus();
        this.movePlus = 1;
        this.mapObject[67][119] = 8;
        this.TimerCount = 17;
        this.loadingFlag = false;
        this.cropIDchara = 0;
        this.codeurl = this.getCodeBase();
        this.simage = this.getImage(this.getDocumentBase(), "image/title.gif");
        this.tracker.addImage(this.simage, 0);
        try {
            this.tracker.waitForAll();
        }
        catch (InterruptedException interruptedException) {
            // empty catch block
        }
    }

    public void start() {
        this.yesnoNumber = 0;
        this.yesnoJudge = 0;
        this.inputKey = true;
        this.mapFlagAll = true;
        this.mapFlagErase = false;
        this.messageFlag = false;
        this.messageFlag2 = false;
        this.messageFlag3 = 0;
        this.configFlag = true;
        this.yusyaFlag = false;
        this.openningFlag = false;
        this.saidanFlag = false;
        this.menuFlag = false;
        this.itemKeyFlag = false;
        this.attackFlag = false;
        this.scoreFlag = false;
        this.saveFlag = false;
        this.popupFlag = false;
        this.UpKey = false;
        this.DownKey = false;
        this.LeftKey = false;
        this.RightKey = false;
        this.focusFlag = false;
        this.countRepaint = 0;
        this.movingSkip = 0;
        this.paintSkip = 0;
        this.repaintSkip = false;
        this.currentKey = 0;
        this.imgBuff = this.createImage(520, 520);
        this.gBuff = this.imgBuff.getGraphics();
        this.imgBuffStatus = this.createImage(this.xp, 520);
        this.gBuffStatus = this.imgBuffStatus.getGraphics();
        this.imgBuffStatus2 = this.createImage(this.xp, 520);
        this.gBuffStatus2 = this.imgBuffStatus2.getGraphics();
        this.imgBuffMap = this.createImage(40, 40);
        this.gBuffMap = this.imgBuffMap.getGraphics();
        this.imgBuffCharaX = this.createImage(80, 40);
        this.gBuffCharaX = this.imgBuffCharaX.getGraphics();
        this.imgBuffCharaY = this.createImage(40, 80);
        this.gBuffCharaY = this.imgBuffCharaY.getGraphics();
        this.imgBuffyusya = this.createImage(520, 520);
        this.gBuffyusya = this.imgBuffyusya.getGraphics();
        this.imgBuff2 = this.createImage(120, 120);
        this.gBuff2 = this.imgBuff2.getGraphics();
        this.imgBuff3 = this.createImage(40, 40);
        this.gBuff3 = this.imgBuff3.getGraphics();
        this.imgBuffopen = this.createImage(820, 520);
        this.gBuffopen = this.imgBuffopen.getGraphics();
        if (this.timer == null) {
            this.timer = new Thread(this);
            this.animaFlag = true;
            this.timer.start();
        }
    }

    public void stop() {
        if (this.timer != null) {
            this.animaFlag = false;
            this.timer = null;
        }
        this.gBuff.dispose();
        this.gBuffStatus.dispose();
        this.gBuffStatus2.dispose();
        this.gBuffMap.dispose();
        this.gBuffCharaX.dispose();
        this.gBuffCharaY.dispose();
        this.gBuffyusya.dispose();
        this.gBuff2.dispose();
    }

    public void run() {
        while (this.animaFlag) {
            if (this.waitCounterFlag) {
                try {
                    Thread.sleep(this.waitCounter);
                }
                catch (InterruptedException interruptedException) {
                    System.out.println("Thread Exception !!!");
                }
                this.waitCounterFlag = false;
            } else if (!this.attackFlag) {
                try {
                    Thread.sleep(this.TimerCount);
                }
                catch (InterruptedException interruptedException) {
                    System.out.println("Thread Exception !!!");
                }
            }
            if (this.repaintSkip) continue;
            this.repaint();
        }
    }

    public void paint(Graphics graphics) {
        boolean bl = false;
        if (!this.loadingFlag) {
            InputStream inputStream;
            this.loadingFlag = true;
            this.gBuffopen.drawImage(this.simage, 0, 0, this);
            graphics.drawImage(this.imgBuffopen, 0, 0, this);
            this.showStatus("Now Loading Map data .....");
            this.loadMapData();
            this.showStatus("Now Loading Map data ..... Done.");
            this.graphicLoading(graphics);
            this.showStatus("Now Loading Sound data .....");
            this.audio[1] = this.getAudioClip(this.getDocumentBase(), "au/1.au");
            this.audio[2] = this.getAudioClip(this.getDocumentBase(), "au/2.au");
            this.audio[4] = this.getAudioClip(this.getDocumentBase(), "au/4.au");
            this.audio[32] = this.getAudioClip(this.getDocumentBase(), "au/7.au");
            this.audio[33] = this.getAudioClip(this.getDocumentBase(), "au/8.au");
            this.audio[34] = this.getAudioClip(this.getDocumentBase(), "au/9.au");
            this.audio[35] = this.getAudioClip(this.getDocumentBase(), "au/10.au");
            this.audio[36] = this.getAudioClip(this.getDocumentBase(), "au/11.au");
            this.mapObject[72][124] = 2;
            this.subsound3.setEnabled(false);
            this.mapObject[75][124] = '\u0000';
            this.subBGM2.setEnabled(false);
            this.mapObject[76][121] = '\u0000';
            this.LangENG.setEnabled(false);
            this.mapObject[68][127] = 2;
            this.subfont12.setEnabled(false);
            this.mapObject[69][127] = 2;
            this.subfont22.setEnabled(false);
            this.FontName = "Dialog";
            this.mapObject[70][127] = 16;
            this.showStatus("Now Loading Sound data ..... Done.");
            this.BGMset();
            try {
                inputStream = new URL(this.getDocumentBase(), "savedat/data1.dat").openStream();
            }
            catch (FileNotFoundException fileNotFoundException) {
                this.subload1.setEnabled(false);
            }
            catch (IOException iOException) {
                this.subload1.setEnabled(false);
            }
            try {
                inputStream = new URL(this.getDocumentBase(), "savedat/data2.dat").openStream();
            }
            catch (FileNotFoundException fileNotFoundException) {
                this.subload2.setEnabled(false);
            }
            catch (IOException iOException) {
                this.subload2.setEnabled(false);
            }
            try {
                inputStream = new URL(this.getDocumentBase(), "savedat/data3.dat").openStream();
            }
            catch (FileNotFoundException fileNotFoundException) {
                this.subload3.setEnabled(false);
            }
            catch (IOException iOException) {
                this.subload3.setEnabled(false);
            }
            try {
                inputStream = new URL(this.getDocumentBase(), "savedat/data4.dat").openStream();
            }
            catch (FileNotFoundException fileNotFoundException) {
                this.subload4.setEnabled(false);
            }
            catch (IOException iOException) {
                this.subload4.setEnabled(false);
            }
            try {
                inputStream = new URL(this.getDocumentBase(), "savedat/data5.dat").openStream();
            }
            catch (FileNotFoundException fileNotFoundException) {
                this.subload5.setEnabled(false);
            }
            catch (IOException iOException) {
                this.subload5.setEnabled(false);
            }
            try {
                inputStream = new URL(this.getDocumentBase(), "savedat/data6.dat").openStream();
            }
            catch (FileNotFoundException fileNotFoundException) {
                this.subload6.setEnabled(false);
            }
            catch (IOException iOException) {
                this.subload6.setEnabled(false);
            }
            try {
                inputStream = new URL(this.getDocumentBase(), "savedat/data7.dat").openStream();
            }
            catch (FileNotFoundException fileNotFoundException) {
                this.subload7.setEnabled(false);
            }
            catch (IOException iOException) {
                this.subload7.setEnabled(false);
            }
            try {
                inputStream = new URL(this.getDocumentBase(), "savedat/data8.dat").openStream();
            }
            catch (FileNotFoundException fileNotFoundException) {
                this.subload8.setEnabled(false);
            }
            catch (IOException iOException) {
                this.subload8.setEnabled(false);
            }
            this.oldMapData = this.map[this.charaY / 5 + this.mapY * 13][this.charaX / 5 + this.mapX * 13];
            this.oldMapX = this.charaX / 5 + this.mapX * 13;
            this.oldMapY = this.charaY / 5 + this.mapY * 13;
            graphics.setColor(Color.white);
        }
        if (this.saidanFlag) {
            this.saidan(graphics);
        }
        if (this.popupFlag) {
            this.popupFlag = false;
            bl = true;
            this.popup.show(this, this.VerX, this.VerY);
        }
        if (!this.inputKey && !this.focusFlag) {
            bl = true;
        }
        if (this.itemKeyFlag) {
            this.itemKey();
        }
        if (this.paintSkip != 0 && !bl) {
            --this.paintSkip;
            bl = true;
        }
        if (this.flagDisplayStatus && !bl) {
            this.displayConfigWindow(graphics, true, true, true, true);
            this.flagDisplayStatus = false;
        }
        if (this.attackFlag && !bl) {
            this.attackMonster(graphics, this.attackXp, this.attackYp);
            bl = true;
        }
        if (!this.yesnoJudge(graphics) && !bl) {
            bl = true;
        }
        if (!(this.mapFlagAll || this.attackFlag || bl)) {
            if (this.movingSkip != 0) {
                --this.movingSkip;
            } else {
                this.moveCharacter(graphics);
            }
        }
        if (this.yesnoFlag && !bl) {
            bl = true;
        }
        if (this.mapFlagAll && !bl) {
            this.repaintSkip = true;
            this.paintMapAll(graphics);
            this.repaintSkip = false;
            this.movingSkip = 3;
        }
        if (this.configFlag && !bl) {
            this.configFlag = false;
            this.displayConfigWindow(graphics, true, true, true, true);
        }
        if (!(bl || this.yusyaFlag || this.openningFlag)) {
            this.paintMap(graphics);
        }
        if (!bl) {
            this.setMapFlag(graphics);
        }
        if (!bl && this.dialogFlag != 0) {
            if (this.dialogFlag == 1) {
                if (this.VerX + 300 > 820) {
                    this.VerX = 520;
                }
                if (this.VerY + 150 > 520) {
                    this.VerY = 370;
                }
                this.dialogFlag = 0;
                bl = true;
                ((Component)this.d1).setLocation(this.VerX, this.VerY);
                this.d1.init();
            } else if (this.dialogFlag == 3) {
                if (this.VerX + 550 > 820) {
                    this.VerX = 270;
                }
                if (this.VerY + 350 > 520) {
                    this.VerY = 170;
                }
                this.dialogFlag = 0;
                bl = true;
                ((Component)this.d3).setLocation(this.VerX, this.VerY);
                this.d3.init(this.mapObject[76][121], this.mapY + 1, this.codeurl);
                this.requestFocus();
                if (this.d3.Ans != 0) {
                    this.scoreInit(this.d3.Ans);
                }
            } else if (this.dialogFlag == 11) {
                this.dialogFlag = 0;
                bl = true;
                this.Loaddata(1);
            } else if (this.dialogFlag == 12) {
                this.dialogFlag = 0;
                bl = true;
                this.Loaddata(2);
            } else if (this.dialogFlag == 13) {
                this.dialogFlag = 0;
                bl = true;
                this.Loaddata(3);
            } else if (this.dialogFlag == 14) {
                this.dialogFlag = 0;
                bl = true;
                this.Loaddata(4);
            } else if (this.dialogFlag == 15) {
                this.dialogFlag = 0;
                bl = true;
                this.Loaddata(5);
            } else if (this.dialogFlag == 16) {
                this.dialogFlag = 0;
                bl = true;
                this.Loaddata(6);
            } else if (this.dialogFlag == 17) {
                this.dialogFlag = 0;
                bl = true;
                this.Loaddata(7);
            } else if (this.dialogFlag == 18) {
                this.dialogFlag = 0;
                bl = true;
                this.Loaddata(8);
            }
        }
        if (this.endFlag) {
            this.ending(graphics);
        }
        if (!bl) {
            this.eventMT(graphics);
        }
        if (this.messageFlag && !bl && !this.strMessage[this.mapObject[76][121]][this.strNumber].equals("") && this.strNumber != 0) {
            this.drawJapaneseFrame(graphics, this.strMessage[this.mapObject[76][121]][this.strNumber], 50, 80);
            this.inputKey = false;
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.movingSkip = 3;
        }
        if (this.scoreFlag && !bl) {
            this.strNumber = 0;
            this.drawJapaneseFrame(graphics, this.strMessage[this.mapObject[76][121]][this.strNumber], 50, 80);
            this.inputKey = false;
            this.mapFlagErase = false;
            this.mapFlagAll = true;
            this.scoreFlag = false;
        }
        if (this.saveFlag && !bl) {
            this.saveFlag = false;
            this.dosave();
        }
        if (Zdata.DisplayFlag == 1) {
            Zdata.DisplayFlag = 0;
            this.mapFlagAll = true;
            this.mapFlagErase = false;
        }
    }

    public void ichicheck(int n, int n2, int n3) {
        if (!this.itemKeyFlag) {
            n3 = 0;
            if (this.map[n2][n] >= '\u0004' && this.map[n2][n] <= '\u001d') {
                n3 = 150;
            } else if (this.map[n2][n] >= '&' && this.map[n2][n] <= 'n') {
                n3 = 150;
            } else if (this.mapObject[n2][n] == '*' || this.mapObject[n2][n] == '+' || this.mapObject[n2][n] >= '\u008b' && this.mapObject[n2][n] <= '\u009a' || this.mapObject[n2][n] == '\u00af') {
                n3 = 143;
            } else if (this.mapObject[n2][n] == '\u0011' || this.mapObject[n2][n] == '\u0012' || this.mapObject[n2][n] == '(' || this.mapObject[n2][n] == ')' || this.mapObject[n2][n] >= '\u009b' && this.mapObject[n2][n] <= '\u00ae') {
                n3 = 144;
            } else if (this.mapObject[n2][n] == 'E') {
                n3 = 145;
            } else if (this.mapObject[n2][n] == 'W' || this.mapObject[n2][n] == 'X') {
                n3 = 146;
            } else if (this.mapObject[n2][n] == '\u0016') {
                n3 = 155;
            } else if (this.mapObject[n2][n] == 'O') {
                n3 = 183;
            }
            if (n3 != 0) {
                this.showStatus(this.strMessage[this.mapObject[76][121]][n3]);
                this.messageFlag2 = false;
            }
        }
    }

    public void update(Graphics graphics) {
        this.paint(graphics);
    }

    public void mazyutushi(Graphics graphics, int n) {
        int n2 = this.mapObject[66][118];
        if (n == 1) {
            if ((n2 -= 200) <= 0) {
                n2 = 0;
            }
            this.mapObject[66][118] = (char)n2;
        } else {
            if ((n2 -= 100) <= 0) {
                n2 = 0;
            }
            this.mapObject[66][118] = (char)n2;
        }
        if (this.mapObject[72][124] != '\u0000') {
            this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
        }
        graphics.drawImage(this.imgCrop[this.cropIDchara], this.charaX / 5 % 13 * 40 + this.xp, this.charaY / 5 % 13 * 40 + this.yp, this);
        graphics.drawImage(this.imgCrop[25], this.charaX / 5 % 13 * 40 + this.xp, this.charaY / 5 % 13 * 40 + this.yp, this);
        this.twait(600);
        this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, 0, this);
        this.gBuffMap.drawImage(this.imgCrop[this.cropIDchara], 0, 0, this);
        graphics.drawImage(this.imgBuffMap, this.charaX / 5 % 13 * 40 + this.xp, this.charaY / 5 % 13 * 40 + this.yp, this);
        this.displayConfigWindow(graphics, true, true, true, true);
        if (this.mapObject[66][118] == '\u0000') {
            this.mapObject[67][119] = '\u0000';
        }
    }

    public void ichicheck2(Graphics graphics, int n, int n2) {
        int n3 = 0;
        boolean bl = false;
        int n4 = this.mapObject[66][118];
        if (this.mapObject[n2 + 1][n] == ':' && this.mapObject[n2 - 1][n] == ':' && this.mapObject[73][121] == '\u0000') {
            n3 = 243;
        } else if (this.mapObject[n2][n - 1] == ':' && this.mapObject[n2][n + 1] == ':' && this.mapObject[73][121] == '\u0000') {
            n3 = 243;
        }
        if (n3 == 243) {
            this.mapObject[66][118] = (char)(this.mapObject[66][118] / 2);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            graphics.drawImage(this.imgCrop[this.cropIDchara], this.charaX / 5 % 13 * 40 + this.xp, this.charaY / 5 % 13 * 40 + this.yp, this);
            graphics.drawImage(this.imgCrop[25], this.charaX / 5 % 13 * 40 + this.xp, this.charaY / 5 % 13 * 40 + this.yp, this);
            this.twait(600);
            this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, 0, this);
            this.gBuffMap.drawImage(this.imgCrop[this.cropIDchara], 0, 0, this);
            graphics.drawImage(this.imgBuffMap, this.charaX / 5 % 13 * 40 + this.xp, this.charaY / 5 % 13 * 40 + this.yp, this);
            this.displayConfigWindow(graphics, true, true, true, true);
            if (this.mapObject[66][118] == '\u0000') {
                bl = true;
            }
        }
        if (!bl && this.mapObject[n2 + 1][n] == 'c' && this.mapObject[73][121] == '\u0000') {
            n3 = 241;
            this.mazyutushi(graphics, 1);
            if (this.mapObject[n2 + 2][n] == '\u0000' && this.map[n2 + 2][n] == '\u0001') {
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.moveChara(graphics, n, n2 + 1, 3, 0);
            }
            if (this.mapObject[66][118] == '\u0000') {
                bl = true;
            }
        }
        if (!bl && this.mapObject[n2][n - 1] == 'c' && this.mapObject[73][121] == '\u0000') {
            n3 = 241;
            this.mazyutushi(graphics, 1);
            if (this.mapObject[n2][n - 2] == '\u0000' && this.map[n2][n - 2] == '\u0001') {
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.moveChara(graphics, n - 1, n2, 2, 0);
            }
            if (this.mapObject[66][118] == '\u0000') {
                bl = true;
            }
        }
        if (!bl && this.mapObject[n2][n + 1] == 'c' && this.mapObject[73][121] == '\u0000') {
            n3 = 241;
            this.mazyutushi(graphics, 1);
            if (this.mapObject[n2][n + 2] == '\u0000' && this.map[n2][n + 2] == '\u0001') {
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.moveChara(graphics, n + 1, n2, 1, 0);
            }
            if (this.mapObject[66][118] == '\u0000') {
                bl = true;
            }
        }
        if (!bl && this.mapObject[n2 - 1][n] == 'c' && this.mapObject[73][121] == '\u0000') {
            n3 = 241;
            this.mazyutushi(graphics, 1);
            if (this.mapObject[n2 - 2][n] == '\u0000' && this.map[n2 - 2][n] == '\u0001') {
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.moveChara(graphics, n, n2 - 1, 4, 0);
            }
            if (this.mapObject[66][118] == '\u0000') {
                bl = true;
            }
        }
        if (!bl && this.mapObject[n2 + 1][n] == 'd' && this.mapObject[73][121] == '\u0000') {
            n3 = 242;
            this.mazyutushi(graphics, 2);
            if (this.mapObject[66][118] == '\u0000') {
                bl = true;
            }
        }
        if (!bl && this.mapObject[n2][n - 1] == 'd' && this.mapObject[73][121] == '\u0000') {
            n3 = 242;
            this.mazyutushi(graphics, 2);
            if (this.mapObject[66][118] == '\u0000') {
                bl = true;
            }
        }
        if (!bl && this.mapObject[n2][n + 1] == 'd' && this.mapObject[73][121] == '\u0000') {
            n3 = 242;
            this.mazyutushi(graphics, 2);
            if (this.mapObject[66][118] == '\u0000') {
                bl = true;
            }
        }
        if (!bl && this.mapObject[n2 - 1][n] == 'd' && this.mapObject[73][121] == '\u0000') {
            n3 = 242;
            this.mazyutushi(graphics, 2);
            if (this.mapObject[66][118] == '\u0000') {
                bl = true;
            }
        }
        if (this.mapObject[n2 - 1][n] == 'J') {
            n3 = 269;
        }
        if (!bl && n3 == 269) {
            if ((n4 -= 1000) <= 0) {
                n4 = 0;
                bl = true;
            }
            this.mapObject[66][118] = (char)n4;
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            graphics.drawImage(this.imgCrop[this.cropIDchara], this.charaX / 5 % 13 * 40 + this.xp, this.charaY / 5 % 13 * 40 + this.yp, this);
            graphics.drawImage(this.imgCrop[25], this.charaX / 5 % 13 * 40 + this.xp, this.charaY / 5 % 13 * 40 + this.yp, this);
            this.twait(600);
            this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, 0, this);
            this.gBuffMap.drawImage(this.imgCrop[this.cropIDchara], 0, 0, this);
            graphics.drawImage(this.imgBuffMap, this.charaX / 5 % 13 * 40 + this.xp, this.charaY / 5 % 13 * 40 + this.yp, this);
            this.displayConfigWindow(graphics, true, true, true, true);
            if (this.mapObject[66][118] == '\u0000') {
                this.mapObject[67][119] = '\u0000';
            }
        }
        if (n3 != 0) {
            this.showStatus(this.strMessage[this.mapObject[76][121]][n3]);
            this.messageFlag2 = true;
        } else if (!this.messageFlag2) {
            this.showStatus(" ");
        }
        if (bl) {
            this.mapObject[67][119] = '\u0000';
            this.displayCharacter(graphics, n, n2);
        }
    }

    /*
     * Opcode count of 19897 triggered aggressive code reduction.  Override with --aggressivesizethreshold.
     */
    public void eventMT(Graphics graphics) {
        int n;
        int n2;
        char c;
        char c2;
        char c3;
        char c4;
        char c5;
        char c6;
        if (this.mapObject[66][118] == '\u0000') {
            this.mapObject[67][119] = '\u0000';
            if (this.mapObject[66][126] != '\u0000') {
                this.mapObject[66][126] = '\u0000';
            }
            if (this.mapObject[74][126] == '\u0000') {
                this.twait(400);
                this.strNumber = 280;
                this.messageFlag = true;
                this.mapObject[74][126] = 98;
                if (this.mapObject[75][124] != '\u0000') {
                    this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
                }
                this.mapObject[69][124] = 20;
                if (this.mapObject[75][124] != '\u0000') {
                    this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
                }
            } else if (this.mapObject[74][126] == 'b' && !this.messageFlag) {
                c6 = this.mapObject[68][127];
                c5 = this.mapObject[69][127];
                c4 = this.mapObject[70][127];
                c3 = this.mapObject[76][121];
                c2 = this.mapObject[72][124];
                c = this.mapObject[75][124];
                this.loadMapData();
                this.mapFlagAll = true;
                this.paintMapAll(graphics);
                this.mapObject[68][127] = c6;
                this.mapObject[69][127] = c5;
                this.mapObject[70][127] = c4;
                this.mapObject[76][121] = c3;
                this.mapObject[72][124] = c2;
                this.mapObject[75][124] = c;
                this.mapObject[74][126] = '\u0000';
                this.BGMset();
                this.yusyaFlag = false;
                this.saidanFlag = false;
                this.menuFlag = false;
                this.configFlag = true;
            }
        }
        int n3 = 0;
        boolean bl = false;
        if (this.charaX % 5 == 0 && this.charaY % 5 == 0 && !this.messageFlag2) {
            this.ichicheck(this.charaX / 5 + this.mapX * 13, this.charaY / 5 + this.mapY * 13 - 1, n3);
            if (n3 != 0) {
                bl = true;
            }
            this.ichicheck(this.charaX / 5 + this.mapX * 13 - 1, this.charaY / 5 + this.mapY * 13, n3);
            if (n3 != 0 && !bl) {
                bl = true;
            }
            this.ichicheck(this.charaX / 5 + this.mapX * 13 + 1, this.charaY / 5 + this.mapY * 13, n3);
            if (n3 != 0 && !bl) {
                bl = true;
            }
            this.ichicheck(this.charaX / 5 + this.mapX * 13, this.charaY / 5 + this.mapY * 13 + 1, n3);
        }
        if (this.charaX % 5 == 0 && this.charaY % 5 == 0 && (this.mapObject[69][125] != this.charaX / 5 + this.mapX * 13 || this.mapObject[70][125] != this.charaY / 5 + this.mapY * 13)) {
            this.ichicheck2(graphics, this.charaX / 5 + this.mapX * 13, this.charaY / 5 + this.mapY * 13);
            this.mapObject[69][125] = (char)(this.charaX / 5 + this.mapX * 13);
            this.mapObject[70][125] = (char)(this.charaY / 5 + this.mapY * 13);
        }
        int n4 = 0;
        int n5 = 0;
        this.mapFlagAll = false;
        if (!(!false || this.mapObject[67][119] == '\u0000' || this.attackFlag || this.charaX % 5 != 0 || this.charaY % 5 != 0 || !this.yanime || this.UpKey || this.DownKey || this.LeftKey || this.RightKey)) {
            if (this.mapObject[67][119] == '\b') {
                this.cropIDchara = 0;
            } else if (this.mapObject[67][119] == '\u0002') {
                this.cropIDchara = 2;
            } else if (this.mapObject[67][119] == '\u0004') {
                this.cropIDchara = 4;
            } else if (this.mapObject[67][119] == '\u0006') {
                this.cropIDchara = 6;
            }
            n2 = this.map[this.charaY / 5 + this.mapY * 13][this.charaX / 5 + this.mapX * 13];
            this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[n2][1]], 0, 0, this);
            this.gBuffMap.drawImage(this.imgCrop[this.cropIDchara], 0, 0, this);
            graphics.drawImage(this.imgBuffMap, this.charaX / 5 * 40 + this.xp, this.charaY / 5 * 40, this);
            this.twait(100);
            ++this.cropIDchara;
            this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[n2][1]], 0, 0, this);
            this.gBuffMap.drawImage(this.imgCrop[this.cropIDchara], 0, 0, this);
            graphics.drawImage(this.imgBuffMap, this.charaX / 5 * 40 + this.xp, this.charaY / 5 * 40, this);
            this.twait(100);
            this.yanime = false;
        }
        if (this.itemFlag == 4) {
            ((Component)this.d2).setLocation(300, 300);
            this.d2.init(this.strMessage[this.mapObject[76][121]][314]);
            if (this.d2.Ans) {
                this.d2.Ans = false;
                this.mapFlagErase = false;
                this.mapFlagAll = true;
                this.paintMapAll(graphics);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[66][118] = (char)(this.mapObject[66][118] + this.mapObject[67][118] * 10 + this.mapObject[68][118] * 5);
                this.mapObject[75][119] = '\u0000';
                this.showStatus(this.strMessage[this.mapObject[76][121]][190] + String.valueOf(this.mapObject[67][118] * 10 + this.mapObject[68][118] * 5) + this.strMessage[this.mapObject[76][121]][297]);
                this.messageFlag2 = true;
            }
            this.itemFlag = 0;
            this.itemKeyFlag = false;
            this.configFlag = true;
        }
        if (this.itemFlag == 5) {
            ((Component)this.d2).setLocation(300, 300);
            this.d2.init(this.strMessage[this.mapObject[76][121]][314]);
            if (this.d2.Ans) {
                this.d2.Ans = false;
                this.mapFlagErase = false;
                this.mapFlagAll = true;
                this.paintMapAll(graphics);
                n4 = this.charaX / 5 + this.mapX * 13;
                n5 = this.charaY / 5 + this.mapY * 13;
                if (this.map[n5 - 1][n4] == '\u0003') {
                    this.twait(400);
                    this.displayDoor(graphics, n4, n5 - 1, 7);
                    this.map[n5 - 1][n4] = '\u0001';
                    this.displayCharacter(graphics, n4, n5 - 1);
                }
                if (this.map[n5][n4 - 1] == '\u0003') {
                    this.twait(400);
                    this.displayDoor(graphics, n4 - 1, n5, 7);
                    this.map[n5][n4 - 1] = '\u0001';
                    this.displayCharacter(graphics, n4 - 1, n5);
                }
                if (this.map[n5][n4 + 1] == '\u0003') {
                    this.twait(400);
                    this.displayDoor(graphics, n4 + 1, n5, 7);
                    this.map[n5][n4 + 1] = '\u0001';
                    this.displayCharacter(graphics, n4 + 1, n5);
                }
                if (this.map[n5 + 1][n4] == '\u0003') {
                    this.twait(400);
                    this.displayDoor(graphics, n4, n5 + 1, 7);
                    this.map[n5 + 1][n4] = '\u0001';
                    this.displayCharacter(graphics, n4, n5 + 1);
                }
                this.mapObject[76][119] = '\u0000';
            }
            this.itemFlag = 0;
            this.itemKeyFlag = false;
            this.configFlag = true;
        }
        if (this.itemFlag == 6) {
            ((Component)this.d2).setLocation(300, 300);
            this.d2.init(this.strMessage[this.mapObject[76][121]][314]);
            if (this.d2.Ans) {
                this.d2.Ans = false;
                this.mapFlagErase = false;
                this.mapFlagAll = true;
                this.paintMapAll(graphics);
                n2 = 0;
                n = 1;
                if (this.mapObject[74][120] == '\u0001') {
                    n = 2;
                }
                if (this.objectAttribute[this.mapObject[(n5 = this.charaY / 5 + this.mapY * 13) - 1][n4 = this.charaX / 5 + this.mapX * 13]][3] == 6 && this.mapObject[n5 - 1][n4] != '9' && this.mapObject[n5 - 1][n4] != 'J' && this.mapObject[n5 - 1][n4] != '`' && this.mapObject[n5 - 1][n4] != '2' && this.mapObject[n5 - 1][n4] != '3' && this.mapObject[n5 - 1][n4] != '4' && this.mapObject[n5 - 1][n4] != '<' && this.mapObject[n5 - 1][n4] != '=' && this.mapObject[n5 - 1][n4] != '>' && this.mapObject[n5 - 1][n4] != 'F' && this.mapObject[n5 - 1][n4] != 'H') {
                    this.twait(400);
                    if (this.mapObject[72][124] != '\u0001') {
                        this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
                    }
                    n2 += this.objectAttribute[this.mapObject[n5 - 1][n4]][13] * n;
                    this.charaZeno(graphics, n4, n5 - 1);
                }
                if (this.objectAttribute[this.mapObject[n5][n4 - 1]][3] == 6 && this.mapObject[n5][n4 - 1] != '9' && this.mapObject[n5][n4 - 1] != 'J' && this.mapObject[n5][n4 - 1] != '`' && this.mapObject[n5][n4 - 1] != '2' && this.mapObject[n5][n4 - 1] != '3' && this.mapObject[n5][n4 - 1] != '4' && this.mapObject[n5][n4 - 1] != '<' && this.mapObject[n5][n4 - 1] != '=' && this.mapObject[n5][n4 - 1] != '>' && this.mapObject[n5][n4 - 1] != 'F' && this.mapObject[n5][n4 - 1] != 'H') {
                    this.twait(400);
                    if (this.mapObject[72][124] != '\u0001') {
                        this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
                    }
                    n2 += this.objectAttribute[this.mapObject[n5][n4 - 1]][13] * n;
                    this.charaZeno(graphics, n4 - 1, n5);
                }
                if (this.objectAttribute[this.mapObject[n5][n4 + 1]][3] == 6 && this.mapObject[n5][n4 + 1] != '9' && this.mapObject[n5][n4 + 1] != 'J' && this.mapObject[n5][n4 + 1] != '`' && this.mapObject[n5][n4 + 1] != '2' && this.mapObject[n5][n4 + 1] != '3' && this.mapObject[n5][n4 + 1] != '4' && this.mapObject[n5][n4 + 1] != '<' && this.mapObject[n5][n4 + 1] != '=' && this.mapObject[n5][n4 + 1] != '>' && this.mapObject[n5][n4 + 1] != 'F' && this.mapObject[n5][n4 + 1] != 'H') {
                    this.twait(400);
                    if (this.mapObject[72][124] != '\u0001') {
                        this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
                    }
                    n2 += this.objectAttribute[this.mapObject[n5][n4 + 1]][13] * n;
                    this.charaZeno(graphics, n4 + 1, n5);
                }
                if (this.objectAttribute[this.mapObject[n5 + 1][n4]][3] == 6 && this.mapObject[n5 + 1][n4] != '9' && this.mapObject[n5 + 1][n4] != 'J' && this.mapObject[n5 + 1][n4] != '`' && this.mapObject[n5 + 1][n4] != '2' && this.mapObject[n5 + 1][n4] != '3' && this.mapObject[n5 + 1][n4] != '4' && this.mapObject[n5 + 1][n4] != '<' && this.mapObject[n5 + 1][n4] != '=' && this.mapObject[n5 + 1][n4] != '>' && this.mapObject[n5 + 1][n4] != 'F' && this.mapObject[n5 + 1][n4] != 'H') {
                    this.twait(400);
                    if (this.mapObject[72][124] != '\u0001') {
                        this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
                    }
                    n2 += this.objectAttribute[this.mapObject[n5 + 1][n4]][13] * n;
                    this.charaZeno(graphics, n4, n5 + 1);
                }
                this.mapObject[66][120] = '\u0000';
                this.mapObject[69][118] = (char)(this.mapObject[69][118] + n2);
                if (n2 != 0) {
                    this.showStatus(this.strMessage[this.mapObject[76][121]][192] + this.strMessage[this.mapObject[76][121]][298] + String.valueOf(n2) + this.strMessage[this.mapObject[76][121]][205]);
                    this.messageFlag2 = true;
                }
            }
            this.itemFlag = 0;
            this.itemKeyFlag = false;
            this.configFlag = true;
        }
        if (this.itemFlag == 7) {
            ((Component)this.d2).setLocation(300, 300);
            this.d2.init(this.strMessage[this.mapObject[76][121]][314]);
            if (this.d2.Ans) {
                this.d2.Ans = false;
                this.mapFlagErase = false;
                this.mapFlagAll = true;
                this.paintMapAll(graphics);
                n4 = 12 - this.charaX / 5 + this.mapX * 13;
                n5 = 12 - this.charaY / 5 + this.mapY * 13;
                if (this.mapObject[n5][n4] != '\u0000' || this.map[n5][n4] != '\u0001') {
                    this.showStatus(this.strMessage[this.mapObject[76][121]][199]);
                    this.messageFlag2 = true;
                } else {
                    if (this.mapObject[72][124] != '\u0000') {
                        this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                    }
                    this.displayCharacter(graphics, this.charaX / 5 + this.mapX * 13, this.charaY / 5 + this.mapY * 13);
                    this.charaX = (12 - this.charaX / 5) * 5;
                    this.charaY = (12 - this.charaY / 5) * 5;
                    this.mapObject[67][120] = (char)(this.mapObject[67][120] + '\u0001');
                    if (this.mapObject[67][120] >= '\u0004') {
                        this.mapObject[67][120] = '\u0000';
                    }
                    this.showStatus(this.strMessage[this.mapObject[76][121]][193]);
                    this.messageFlag2 = true;
                }
            }
            this.itemFlag = 0;
            this.itemKeyFlag = false;
            this.configFlag = true;
        }
        if (this.itemFlag == 8) {
            ((Component)this.d2).setLocation(300, 300);
            this.d2.init(this.strMessage[this.mapObject[76][121]][314]);
            if (this.d2.Ans) {
                this.d2.Ans = false;
                this.mapFlagErase = false;
                this.mapFlagAll = true;
                this.paintMapAll(graphics);
                n4 = this.charaX / 5 + (this.mapX + 1) * 13;
                n5 = this.charaY / 5 + this.mapY * 13;
                if (this.mapY * 10 + this.mapX + 1 == 52) {
                    n4 = this.charaX / 5 + 0;
                    n5 = this.charaY / 5 + 0;
                } else if (this.mapX == 9) {
                    n4 = this.charaX / 5 + (this.mapX - 9) * 13;
                    n5 = this.charaY / 5 + (this.mapY + 1) * 13;
                }
                if (this.mapObject[n5][n4] != '\u0000' || this.map[n5][n4] != '\u0001') {
                    this.showStatus(this.strMessage[this.mapObject[76][121]][200]);
                    this.messageFlag2 = true;
                } else {
                    if (this.mapObject[72][124] != '\u0000') {
                        this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                    }
                    this.displayCharacter(graphics, this.charaX / 5 + this.mapX * 13, this.charaY / 5 + this.mapY * 13);
                    if (this.mapY * 10 + this.mapX + 1 == 52) {
                        this.mapX = 0;
                        this.mapY = 0;
                    } else if (this.mapX == 9) {
                        this.mapX -= 9;
                        ++this.mapY;
                    } else {
                        ++this.mapX;
                    }
                    this.mapObject[68][120] = '\u0000';
                    this.mapFlagAll = true;
                    this.mapFlagErase = false;
                    this.showStatus(this.strMessage[this.mapObject[76][121]][194]);
                    this.messageFlag2 = true;
                    this.BGMset();
                    if (this.mapY * 10 + this.mapX + 1 <= 50 && this.mapY * 10 + this.mapX + 1 - this.mapObject[71][118] >= 0) {
                        this.mapObject[71][118] = (char)(this.mapY * 10 + this.mapX + 1);
                        if (this.mapY * 10 + this.mapX + 1 > 25 && this.mapObject[35][58] == 'E') {
                            this.mapObject[35][58] = '\u0000';
                        }
                        if (this.mapObject[71][118] == ')' && this.mapObject[41][123] == 'E') {
                            this.mapObject[41][123] = '\u0000';
                        }
                        if (this.mapObject[71][118] == '2' && this.mapObject[55][110] == 'E') {
                            this.mapObject[55][110] = '\u0000';
                        }
                        if (this.mapObject[71][118] == '2' && this.mapObject[54][110] == 'E') {
                            this.mapObject[54][110] = '\u0000';
                        }
                    }
                }
            }
            this.itemFlag = 0;
            this.itemKeyFlag = false;
            this.configFlag = true;
        }
        if (this.itemFlag == 9) {
            ((Component)this.d2).setLocation(300, 300);
            this.d2.init(this.strMessage[this.mapObject[76][121]][314]);
            if (this.d2.Ans) {
                this.d2.Ans = false;
                this.mapFlagErase = false;
                this.mapFlagAll = true;
                this.paintMapAll(graphics);
                n4 = this.charaX / 5 + (this.mapX - 1) * 13;
                n5 = this.charaY / 5 + this.mapY * 13;
                if (this.mapY * 10 + this.mapX + 1 == 1) {
                    n4 = this.charaX / 5 + 13;
                    n5 = this.charaY / 5 + 65;
                } else if (this.mapX == 0) {
                    n4 = this.charaX / 5 + (this.mapX + 9) * 13;
                    n5 = this.charaY / 5 + (this.mapY - 1) * 13;
                }
                if (this.mapObject[n5][n4] != '\u0000' || this.map[n5][n4] != '\u0001') {
                    this.showStatus(this.strMessage[this.mapObject[76][121]][201]);
                    this.messageFlag2 = true;
                } else {
                    if (this.mapObject[72][124] != '\u0000') {
                        this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                    }
                    this.displayCharacter(graphics, this.charaX / 5 + this.mapX * 13, this.charaY / 5 + this.mapY * 13);
                    if (this.mapY * 10 + this.mapX + 1 == 1) {
                        this.mapX = 1;
                        this.mapY = 5;
                    } else if (this.mapX == 0) {
                        this.mapX += 9;
                        --this.mapY;
                    } else {
                        --this.mapX;
                    }
                    this.mapObject[69][120] = '\u0000';
                    this.mapFlagAll = true;
                    this.mapFlagErase = false;
                    this.showStatus(this.strMessage[this.mapObject[76][121]][195]);
                    this.messageFlag2 = true;
                    this.BGMset();
                }
            }
            this.itemFlag = 0;
            this.itemKeyFlag = false;
            this.configFlag = true;
        }
        if (this.itemFlag == 11) {
            ((Component)this.d2).setLocation(300, 300);
            this.d2.init(this.strMessage[this.mapObject[76][121]][314]);
            if (this.d2.Ans) {
                this.d2.Ans = false;
                this.mapFlagErase = false;
                this.mapFlagAll = true;
                this.paintMapAll(graphics);
                n2 = 0;
                n4 = this.charaX / 5 + this.mapX * 13;
                n5 = this.charaY / 5 + this.mapY * 13;
                if (this.mapObject[n5 - 1][n4] == 'O') {
                    this.twait(400);
                    this.displayDoor(graphics, n4, n5 - 1, 9);
                    this.map[n5 - 1][n4] = '\u0001';
                    this.mapObject[n5 - 1][n4] = '\u0000';
                    this.displayCharacter(graphics, n4, n5 - 1);
                    n2 = 1;
                }
                if (this.mapObject[n5][n4 - 1] == 'O') {
                    this.twait(400);
                    this.displayDoor(graphics, n4 - 1, n5, 10);
                    this.map[n5][n4 - 1] = '\u0001';
                    this.mapObject[n5][n4 - 1] = '\u0000';
                    this.displayCharacter(graphics, n4 - 1, n5);
                    n2 = 1;
                }
                if (this.mapObject[n5][n4 + 1] == 'O') {
                    this.twait(400);
                    this.displayDoor(graphics, n4 + 1, n5, 11);
                    this.map[n5][n4 + 1] = '\u0001';
                    this.mapObject[n5][n4 + 1] = '\u0000';
                    this.displayCharacter(graphics, n4 + 1, n5);
                    n2 = 1;
                }
                if (this.mapObject[n5 + 1][n4] == 'O') {
                    this.twait(400);
                    this.displayDoor(graphics, n4, n5 + 1, 12);
                    this.map[n5 + 1][n4] = '\u0001';
                    this.mapObject[n5 + 1][n4] = '\u0000';
                    this.displayCharacter(graphics, n4, n5 + 1);
                    n2 = 1;
                }
                if (n2 == 1) {
                    this.showStatus(this.strMessage[this.mapObject[76][121]][196]);
                    this.messageFlag2 = true;
                }
            }
            this.itemFlag = 0;
            this.itemKeyFlag = false;
            this.configFlag = true;
        }
        if (this.itemFlag == 12) {
            ((Component)this.d2).setLocation(300, 300);
            this.d2.init(this.strMessage[this.mapObject[76][121]][314]);
            if (this.d2.Ans) {
                this.d2.Ans = false;
                this.mapFlagErase = false;
                this.mapFlagAll = true;
                this.paintMapAll(graphics);
                boolean bl2 = false;
                n4 = this.mapX * 13;
                n5 = this.mapY * 13;
                n = 0;
                while (n < 12) {
                    n2 = 0;
                    while (n2 < 12) {
                        if (this.mapObject[n5 + n2][n4 + n] == '\u0002') {
                            this.twait(400);
                            this.displayDoor(graphics, n4 + n, n5 + n2, 1);
                            this.mapObject[n5 + n2][n4 + n] = '\u0000';
                            this.displayCharacter(graphics, n4 + n, n5 + n2);
                            bl2 = true;
                        }
                        ++n2;
                    }
                    ++n;
                }
                this.mapObject[72][120] = '\u0000';
                if (bl2) {
                    this.showStatus(this.strMessage[this.mapObject[76][121]][197]);
                    this.messageFlag2 = true;
                }
            }
            this.itemFlag = 0;
            this.itemKeyFlag = false;
            this.configFlag = true;
        }
        if (this.itemFlag == 13) {
            ((Component)this.d2).setLocation(300, 300);
            this.d2.init(this.strMessage[this.mapObject[76][121]][314]);
            if (this.d2.Ans) {
                this.d2.Ans = false;
                this.mapFlagErase = false;
                this.mapFlagAll = true;
                this.paintMapAll(graphics);
                n4 = this.mapX * 13;
                n5 = this.mapY * 13;
                n = 0;
                while (n < 12) {
                    n2 = 0;
                    while (n2 < 12) {
                        if (this.map[n5 + n2][n4 + n] == '\u0003') {
                            this.twait(400);
                            this.displayDoor(graphics, n4 + n, n5 + n2, 7);
                            this.map[n5 + n2][n4 + n] = '\u0001';
                            this.displayCharacter(graphics, n4 + n, n5 + n2);
                        }
                        ++n2;
                    }
                    ++n;
                }
                this.mapObject[73][120] = '\u0000';
                this.showStatus(this.strMessage[this.mapObject[76][121]][198]);
                this.messageFlag2 = true;
            }
            this.itemFlag = 0;
            this.itemKeyFlag = false;
            this.configFlag = true;
        }
        if (this.mapObject[71][127] == '\f' && this.inputKey) {
            c6 = this.mapObject[68][127];
            c5 = this.mapObject[69][127];
            c4 = this.mapObject[70][127];
            c3 = this.mapObject[76][121];
            c2 = this.mapObject[72][124];
            c = this.mapObject[75][124];
            this.loadMapData();
            this.mapFlagAll = true;
            this.mapObject[68][127] = c6;
            this.mapObject[69][127] = c5;
            this.mapObject[70][127] = c4;
            this.mapObject[76][121] = c3;
            this.mapObject[72][124] = c2;
            this.mapObject[75][124] = c;
            this.mapObject[74][126] = '\u0000';
            this.mapObject[72][127] = '\u0001';
            this.BGMset();
            this.yusyaFlag = false;
            this.saidanFlag = false;
            this.menuFlag = false;
        }
        if (this.mapObject[71][127] == '\u000b' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.OpenningZeno(graphics, 4);
            this.OpenningZeno(graphics, 5);
            this.mapObject[71][127] = 12;
        }
        if (this.mapObject[71][127] == '\n' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 52;
            this.messageFlag = true;
            this.mapObject[71][127] = 11;
        }
        if (this.mapObject[71][127] == '\t' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 51;
            this.messageFlag = true;
            this.mapObject[71][127] = 10;
        }
        if (this.mapObject[71][127] == '\b' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 50;
            this.messageFlag = true;
            this.mapObject[71][127] = 9;
        }
        if (this.mapObject[71][127] == '\u0007' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 49;
            this.messageFlag = true;
            this.mapObject[71][127] = 8;
        }
        if (this.mapObject[71][127] == '\u0006' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 48;
            this.messageFlag = true;
            this.mapObject[71][127] = 7;
        }
        if (this.mapObject[71][127] == '\u0005' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 47;
            this.messageFlag = true;
            this.mapObject[71][127] = 6;
        }
        if (this.mapObject[71][127] == '\u0004' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 46;
            this.messageFlag = true;
            this.mapObject[71][127] = 5;
        }
        if (this.mapObject[71][127] == '\u0003' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 45;
            this.messageFlag = true;
            this.mapObject[71][127] = 4;
        }
        if (this.mapObject[71][127] == '\u0002' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.Zeno2(graphics, 123, 57);
            this.mapObject[71][127] = 3;
        }
        if (this.mapObject[71][127] == '\u0001' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59 && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 44;
            this.messageFlag = true;
            this.mapObject[71][127] = 2;
        }
        if (this.mapObject[57][123] == 'X' && this.mapObject[71][127] == '\u0000' && this.mapObject[76][126] == '\u0001' && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 59) {
            this.twait(800);
            this.strNumber = 43;
            this.messageFlag = true;
            this.mapObject[71][127] = '\u0001';
        }
        if (this.mapObject[74][126] == '\u0016' && !this.messageFlag && this.mapObject[73][124] == '\u0000') {
            this.Name = "";
            if (this.score2 <= 9) {
                ((Component)this.d4).setVisible(true);
                this.mapObject[73][124] = '\u0001';
            } else {
                this.mapObject[73][124] = '\u0001';
            }
        }
        if (this.mapObject[74][126] == '\u0016' && !this.messageFlag && this.mapObject[73][124] == '\u0001' && !this.d4.isShowing()) {
            if (this.score2 <= 9 && this.d4.str != "") {
                this.Name = this.d4.str;
                this.rankUpdate(this.mapY);
            }
            this.mapObject[73][124] = 2;
            this.d3.init(this.mapObject[76][121], this.mapY + 1, this.codeurl);
            if (this.d3.Ans != 0) {
                this.scoreInit(this.d3.Ans);
            }
        }
        if (this.mapObject[74][126] == '\u0016' && !this.messageFlag && this.mapObject[73][124] == '\u0002' && !this.d3.isShowing()) {
            if (this.mapObject[75][125] == '\u0001') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[55][110] = '\u0000';
                this.displayCharacter(graphics, 110, 55);
            } else {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[54][110] = '\u0000';
                this.displayCharacter(graphics, 110, 54);
            }
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[69][124] = 16;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[74][126] = '\u0000';
            this.mapObject[73][124] = '\u0000';
        }
        if (this.mapObject[72][125] == '\u0001' && this.mapObject[55][110] == '\u0000' && this.mapObject[74][125] == '\u0000') {
            if (this.mapObject[54][109] == ':') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[54][109] = '\u0000';
                this.displayCharacter(graphics, 109, 54);
            }
            if (this.mapObject[54][110] == ':') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[54][110] = '\u0000';
                this.displayCharacter(graphics, 110, 54);
            }
            if (this.mapObject[54][111] == ':') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[54][111] = '\u0000';
                this.displayCharacter(graphics, 111, 54);
            }
            if (this.mapObject[55][111] == ':') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[55][111] = '\u0000';
                this.displayCharacter(graphics, 111, 55);
            }
            if (this.mapObject[56][111] == ':') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[56][111] = '\u0000';
                this.displayCharacter(graphics, 111, 56);
            }
            if (this.mapObject[56][110] == ':') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[56][110] = '\u0000';
                this.displayCharacter(graphics, 110, 56);
            }
            if (this.mapObject[56][109] == ':') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[56][109] = '\u0000';
                this.displayCharacter(graphics, 109, 56);
            }
            if (this.mapObject[55][109] == ':') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[55][109] = '\u0000';
                this.displayCharacter(graphics, 109, 55);
            }
            this.twait(400);
            this.displayDoor(graphics, 110, 59, 5);
            this.mapObject[59][110] = '\u0000';
            this.displayCharacter(graphics, 110, 59);
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            if (this.mapObject[35][58] == 'E') {
                this.mapObject[35][58] = '\u0000';
            }
            if (this.charaX / 5 + this.mapX * 13 == 110 && this.charaY / 5 + this.mapY * 13 == 54) {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[55][110] = 69;
                this.displayCharacter(graphics, 110, 55);
                this.mapObject[75][125] = '\u0001';
            } else {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[54][110] = 69;
                this.displayCharacter(graphics, 110, 54);
            }
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[57][109] = 78;
            this.displayCharacter(graphics, 109, 57);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[57][110] = 78;
            this.displayCharacter(graphics, 110, 57);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[57][111] = 78;
            this.displayCharacter(graphics, 111, 57);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[56][106] = 82;
            this.displayCharacter(graphics, 106, 56);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[56][107] = 82;
            this.displayCharacter(graphics, 107, 56);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[56][108] = 82;
            this.displayCharacter(graphics, 108, 56);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[56][112] = 85;
            this.displayCharacter(graphics, 112, 56);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[56][113] = 85;
            this.displayCharacter(graphics, 113, 56);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[56][114] = 85;
            this.displayCharacter(graphics, 114, 56);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[54][109] = 28;
            this.displayCharacter(graphics, 109, 54);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[54][111] = 109;
            this.displayCharacter(graphics, 111, 54);
            this.mapObject[74][125] = '\u0001';
            this.mapObject[69][124] = 16;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (this.mapObject[54][109] == ':' && this.mapObject[54][110] == '\u0000' && this.mapObject[54][111] == ':' && this.mapObject[55][109] == '\u0000' && this.mapObject[55][110] == '9' && this.mapObject[55][111] == '\u0000' && this.mapObject[56][109] == ':' && this.mapObject[56][110] == '\u0000' && this.mapObject[56][111] == ':' && this.mapObject[72][126] == '\u0000') {
            this.objectAttribute[57][10] = 800;
            this.objectAttribute[57][11] = 500;
            this.objectAttribute[57][12] = 100;
            this.mapObject[72][126] = '\u0001';
            this.twait(400);
            this.strNumber = 42;
            this.messageFlag = true;
        }
        if (this.mapObject[74][126] == '\u001e') {
            this.Madoushi2(graphics, 110, 55);
            this.mapObject[54][109] = 58;
            this.displayCharacter(graphics, 109, 54);
            this.mapObject[54][110] = 58;
            this.displayCharacter(graphics, 110, 54);
            this.mapObject[54][111] = 58;
            this.displayCharacter(graphics, 111, 54);
            this.mapObject[55][111] = 58;
            this.displayCharacter(graphics, 111, 55);
            this.mapObject[56][111] = 58;
            this.displayCharacter(graphics, 111, 56);
            this.mapObject[56][110] = 58;
            this.displayCharacter(graphics, 110, 56);
            this.mapObject[56][109] = 58;
            this.displayCharacter(graphics, 109, 56);
            this.mapObject[55][109] = 58;
            this.displayCharacter(graphics, 109, 55);
            this.mapObject[74][126] = '\u0000';
            this.mapObject[69][124] = 29;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.menuFlag = false;
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 110 && this.charaY / 5 + this.mapY * 13 == 58 && this.mapObject[54][110] == '\u0000' && this.mapObject[59][110] == '\u0000' && this.mapObject[72][125] == '\u0000') {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.displayDoor(graphics, 110, 59, 4);
            this.mapObject[59][110] = 20;
            this.displayCharacter(graphics, 110, 59);
            this.Zeno(graphics, 110, 55);
            this.twait(400);
            this.strNumber = 41;
            this.messageFlag = true;
            this.mapObject[74][126] = 30;
            this.mapObject[72][125] = '\u0001';
            this.menuFlag = true;
        }
        if (this.mapObject[53][92] == '\u0000' && this.mapObject[68][126] == '\u0001' && this.mapObject[60][99] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 99, 60, 5);
            this.mapObject[60][99] = '\u0000';
            this.displayCharacter(graphics, 99, 60);
            this.mapObject[68][126] = 2;
        }
        if (this.mapObject[53][92] == '\u0000' && this.mapObject[68][126] == '\u0000') {
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[53][92] = 58;
            this.displayCharacter(graphics, 92, 53);
            this.mapObject[68][126] = '\u0001';
        }
        if (this.charaX % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 34 && this.charaY / 5 + this.mapY * 13 == 53 && this.mapObject[53][35] == ':') {
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 35, 53, 1, 0);
            this.moveChara(graphics, 36, 53, 1, 0);
            this.twait(400);
            this.displayDoor(graphics, 33, 53, 8);
            this.map[53][33] = 3;
            this.displayCharacter(graphics, 33, 53);
            this.twait(400);
            this.displayDoor(graphics, 36, 53, 8);
            this.map[53][36] = 3;
            this.displayCharacter(graphics, 36, 53);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.charaX / 5 + this.mapX * 13 == 19 && this.charaY / 5 + this.mapY * 13 == 62 && this.mapObject[58][19] == '9' && !this.messageFlag && this.mapObject[72][126] == '\u0004') {
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[58][19] = '\u0000';
            this.displayCharacter(graphics, 19, 58);
            if (this.mapObject[49][57] == 'X') {
                this.mapObject[49][57] = '\u0000';
            }
            this.mapObject[57][123] = 88;
            this.objectAttribute[88][5] = 99;
            this.mapObject[72][126] = 5;
            this.menuFlag = false;
        }
        if (this.charaX / 5 + this.mapX * 13 == 19 && this.charaY / 5 + this.mapY * 13 == 62 && this.mapObject[60][19] == 'Z' && this.mapObject[58][19] == '9' && !this.messageFlag && this.mapObject[72][126] == '\u0003') {
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            graphics.drawImage(this.imgCrop[25], 240 + this.xp, 320 + this.yp, this);
            this.twait(400);
            this.mapObject[60][19] = '\u0000';
            this.displayCharacter(graphics, 19, 60);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[59][19] = '\u0000';
            this.displayCharacter(graphics, 19, 59);
            this.mapObject[60][18] = '\u0000';
            this.displayCharacter(graphics, 18, 60);
            this.mapObject[60][20] = '\u0000';
            this.displayCharacter(graphics, 20, 60);
            this.mapObject[61][19] = '\u0000';
            this.displayCharacter(graphics, 19, 61);
            this.twait(400);
            this.strNumber = 40;
            this.messageFlag = true;
            this.mapObject[73][127] = '\u0001';
            this.mapObject[72][126] = 4;
        }
        if (this.charaX / 5 + this.mapX * 13 == 19 && this.charaY / 5 + this.mapY * 13 == 62 && this.mapObject[60][19] == 'Z' && this.mapObject[58][19] == '9' && !this.messageFlag && this.mapObject[72][126] == '\u0002') {
            this.twait(400);
            this.Madoushi(graphics, 19, 60);
            this.mapObject[59][19] = 58;
            this.displayCharacter(graphics, 19, 59);
            this.mapObject[60][18] = 58;
            this.displayCharacter(graphics, 18, 60);
            this.mapObject[60][20] = 58;
            this.displayCharacter(graphics, 20, 60);
            this.mapObject[61][19] = 58;
            this.displayCharacter(graphics, 19, 61);
            this.twait(400);
            this.strNumber = 39;
            this.messageFlag = true;
            this.mapObject[73][127] = '\u0001';
            this.mapObject[72][126] = 3;
        }
        if (this.charaX / 5 + this.mapX * 13 == 19 && this.charaY / 5 + this.mapY * 13 == 62 && this.mapObject[60][19] == 'Z' && this.mapObject[58][19] == '9' && !this.messageFlag && this.mapObject[72][126] == '\u0001') {
            this.twait(400);
            this.strNumber = 38;
            this.messageFlag = true;
            this.mapObject[73][127] = '\u0001';
            this.mapObject[72][126] = 2;
        }
        if (this.charaX % 5 == 0 && this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 19 && this.charaY / 5 + this.mapY * 13 == 62 && this.mapObject[60][19] == 'Z' && this.mapObject[72][126] == '\u0000') {
            this.Zeno(graphics, 19, 58);
            this.twait(400);
            this.strNumber = 37;
            this.messageFlag = true;
            this.mapObject[73][127] = '\u0001';
            this.mapObject[72][126] = '\u0001';
            this.menuFlag = true;
        }
        if (this.mapObject[68][125] == '\u0001' && this.mapObject[54][2] == '\u0000' && this.mapObject[54][10] == '\u0000') {
            this.mapObject[68][125] = 2;
            this.twait(400);
            this.displayDoor(graphics, 5, 58, 8);
            this.map[58][5] = 3;
            this.mapObject[58][5] = '\u0000';
            this.displayCharacter(graphics, 5, 58);
            this.twait(400);
            this.displayDoor(graphics, 6, 58, 8);
            this.map[58][6] = 3;
            this.mapObject[58][6] = '\u0000';
            this.displayCharacter(graphics, 6, 58);
            this.twait(400);
            this.displayDoor(graphics, 7, 58, 8);
            this.map[58][7] = 3;
            this.mapObject[58][7] = '\u0000';
            this.displayCharacter(graphics, 7, 58);
            this.twait(400);
            this.displayDoor(graphics, 5, 59, 7);
            this.map[59][5] = '\u0001';
            this.displayCharacter(graphics, 5, 59);
            this.twait(400);
            this.displayDoor(graphics, 7, 59, 7);
            this.map[59][7] = '\u0001';
            this.displayCharacter(graphics, 7, 59);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[57][6] = 108;
            this.displayCharacter(graphics, 6, 57);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[74][126] == '\u0015' && !this.messageFlag && this.mapObject[73][124] == '\u0000') {
            this.Name = "";
            if (this.score2 <= 9) {
                ((Component)this.d4).setVisible(true);
                this.mapObject[73][124] = '\u0001';
            } else {
                this.mapObject[73][124] = '\u0001';
            }
        }
        if (this.mapObject[74][126] == '\u0015' && !this.messageFlag && this.mapObject[73][124] == '\u0001' && !this.d4.isShowing()) {
            if (this.score2 <= 9 && this.d4.str != "") {
                this.Name = this.d4.str;
                this.rankUpdate(this.mapY);
            }
            this.mapObject[73][124] = 2;
            this.d3.init(this.mapObject[76][121], this.mapY + 1, this.codeurl);
            if (this.d3.Ans != 0) {
                this.scoreInit(this.d3.Ans);
            }
        }
        if (this.mapObject[74][126] == '\u0015' && !this.messageFlag && this.mapObject[73][124] == '\u0002' && !this.d3.isShowing()) {
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[41][123] = '\u0000';
            this.displayCharacter(graphics, 123, 41);
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[69][124] = 23;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[74][126] = '\u0000';
            this.mapObject[73][124] = '\u0000';
        }
        if (this.mapObject[66][126] == '\u0013' && !this.messageFlag) {
            this.twait(400);
            this.moveChara(graphics, 123, 45, 4, 2);
            this.moveChara(graphics, 123, 44, 4, 2);
            this.moveChara(graphics, 123, 43, 4, 2);
            this.moveChara(graphics, 123, 42, 4, 2);
            this.moveChara(graphics, 123, 41, 4, 2);
            this.twait(200);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[40][123] = '\u0000';
            this.displayCharacter(graphics, 123, 40);
            this.twait(400);
            this.twait(400);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[41][123] = 69;
            this.displayCharacter(graphics, 123, 41);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[41][119] = 81;
            this.displayCharacter(graphics, 119, 41);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[41][120] = 81;
            this.displayCharacter(graphics, 120, 41);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[41][121] = 81;
            this.displayCharacter(graphics, 121, 41);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[41][125] = 84;
            this.displayCharacter(graphics, 125, 41);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[41][126] = 84;
            this.displayCharacter(graphics, 126, 41);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[41][127] = 84;
            this.displayCharacter(graphics, 127, 41);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[43][120] = 77;
            this.displayCharacter(graphics, 120, 43);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[43][121] = 77;
            this.displayCharacter(graphics, 121, 43);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[43][122] = 77;
            this.displayCharacter(graphics, 122, 43);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[43][124] = '\u0001';
            this.displayCharacter(graphics, 124, 43);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[43][125] = '\u0001';
            this.displayCharacter(graphics, 125, 43);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[43][126] = '\u0001';
            this.displayCharacter(graphics, 126, 43);
            this.mapObject[66][126] = 20;
            this.mapObject[60][19] = 90;
            this.menuFlag = false;
        }
        if (this.mapObject[66][126] == '\u0012' && !this.attackFlag) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[45][123] = 90;
            this.displayCharacter(graphics, 123, 45);
            this.mapObject[47][123] = '\u0000';
            this.twait(400);
            this.displayDoor(graphics, 123, 47, 5);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.map[40][123] = 90;
            this.displayCharacter(graphics, 123, 40);
            this.twait(400);
            this.strNumber = 36;
            this.messageFlag = true;
            this.mapObject[66][126] = 19;
            this.mapObject[69][124] = 23;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[73][127] = 2;
        }
        if (this.mapObject[66][126] == '\u0011' && !this.messageFlag) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.moveChara(graphics, 123, 41, 3, 0);
            this.moveChara(graphics, 123, 42, 3, 0);
            this.moveChara(graphics, 123, 43, 3, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[90][10];
            this.monsterStrength = this.objectAttribute[90][11];
            this.monsterDefence = this.objectAttribute[90][12];
            this.monsterGold = this.objectAttribute[90][13];
            this.monsStatus(graphics, 90);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 18;
        }
        if (this.mapObject[66][126] == '\u0010' && !this.messageFlag) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.strNumber = 35;
            this.messageFlag = true;
            this.mapObject[73][127] = 2;
            this.mapObject[66][126] = 17;
        }
        if (this.mapObject[66][126] == '\u000f' && !this.attackFlag) {
            this.moveChara(graphics, 127, 41, 2, 0);
            this.moveChara(graphics, 126, 41, 2, 0);
            this.moveChara(graphics, 125, 41, 3, 0);
            this.moveChara(graphics, 125, 42, 2, 0);
            this.moveChara(graphics, 124, 42, 3, 0);
            this.moveChara(graphics, 124, 43, 2, 0);
            this.moveChara(graphics, 123, 43, 3, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[91][10];
            this.monsterStrength = this.objectAttribute[91][11];
            this.monsterDefence = this.objectAttribute[91][12];
            this.monsterGold = this.objectAttribute[91][13];
            this.monsStatus(graphics, 91);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 16;
        }
        if (this.mapObject[66][126] == '\u000e' && !this.attackFlag) {
            this.moveChara(graphics, 126, 41, 2, 0);
            this.moveChara(graphics, 125, 41, 3, 0);
            this.moveChara(graphics, 125, 42, 2, 0);
            this.moveChara(graphics, 124, 42, 3, 0);
            this.moveChara(graphics, 124, 43, 2, 0);
            this.moveChara(graphics, 123, 43, 3, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[91][10];
            this.monsterStrength = this.objectAttribute[91][11];
            this.monsterDefence = this.objectAttribute[91][12];
            this.monsterGold = this.objectAttribute[91][13];
            this.monsStatus(graphics, 91);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 15;
        }
        if (this.mapObject[66][126] == '\r' && !this.messageFlag) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.moveChara(graphics, 125, 41, 3, 0);
            this.moveChara(graphics, 125, 42, 2, 0);
            this.moveChara(graphics, 124, 42, 3, 0);
            this.moveChara(graphics, 124, 43, 2, 0);
            this.moveChara(graphics, 123, 43, 3, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[91][10];
            this.monsterStrength = this.objectAttribute[91][11];
            this.monsterDefence = this.objectAttribute[91][12];
            this.monsterGold = this.objectAttribute[91][13];
            this.monsStatus(graphics, 91);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 14;
        }
        if (this.mapObject[66][126] == '\f' && !this.messageFlag) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.strNumber = 34;
            this.messageFlag = true;
            this.mapObject[73][127] = 2;
            this.mapObject[66][126] = 13;
        }
        if (this.mapObject[66][126] == '\u000b' && !this.attackFlag) {
            this.moveChara(graphics, 119, 41, 1, 0);
            this.moveChara(graphics, 120, 41, 1, 0);
            this.moveChara(graphics, 121, 41, 3, 0);
            this.moveChara(graphics, 121, 42, 1, 0);
            this.moveChara(graphics, 122, 42, 3, 0);
            this.moveChara(graphics, 122, 43, 1, 0);
            this.moveChara(graphics, 123, 43, 3, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[92][10];
            this.monsterStrength = this.objectAttribute[92][11];
            this.monsterDefence = this.objectAttribute[92][12];
            this.monsterGold = this.objectAttribute[92][13];
            this.monsStatus(graphics, 92);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 12;
        }
        if (this.mapObject[66][126] == '\n' && !this.attackFlag) {
            this.moveChara(graphics, 120, 41, 1, 0);
            this.moveChara(graphics, 121, 41, 3, 0);
            this.moveChara(graphics, 121, 42, 1, 0);
            this.moveChara(graphics, 122, 42, 3, 0);
            this.moveChara(graphics, 122, 43, 1, 0);
            this.moveChara(graphics, 123, 43, 3, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[92][10];
            this.monsterStrength = this.objectAttribute[92][11];
            this.monsterDefence = this.objectAttribute[92][12];
            this.monsterGold = this.objectAttribute[92][13];
            this.monsStatus(graphics, 92);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 11;
        }
        if (this.mapObject[66][126] == '\t' && !this.messageFlag) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.moveChara(graphics, 121, 41, 3, 0);
            this.moveChara(graphics, 121, 42, 1, 0);
            this.moveChara(graphics, 122, 42, 3, 0);
            this.moveChara(graphics, 122, 43, 1, 0);
            this.moveChara(graphics, 123, 43, 3, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[92][10];
            this.monsterStrength = this.objectAttribute[92][11];
            this.monsterDefence = this.objectAttribute[92][12];
            this.monsterGold = this.objectAttribute[92][13];
            this.monsStatus(graphics, 92);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 10;
        }
        if (this.mapObject[66][126] == '\b' && !this.messageFlag) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.strNumber = 33;
            this.messageFlag = true;
            this.mapObject[73][127] = 2;
            this.mapObject[66][126] = 9;
        }
        if (this.mapObject[66][126] == '\u0007' && !this.attackFlag) {
            this.moveChara(graphics, 126, 43, 2, 0);
            this.moveChara(graphics, 125, 43, 2, 0);
            this.moveChara(graphics, 124, 43, 3, 0);
            this.moveChara(graphics, 124, 44, 2, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[93][10];
            this.monsterStrength = this.objectAttribute[93][11];
            this.monsterDefence = this.objectAttribute[93][12];
            this.monsterGold = this.objectAttribute[93][13];
            this.monsStatus(graphics, 93);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 8;
        }
        if (this.mapObject[66][126] == '\u0006' && !this.attackFlag) {
            this.moveChara(graphics, 125, 43, 2, 0);
            this.moveChara(graphics, 124, 43, 3, 0);
            this.moveChara(graphics, 124, 44, 2, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[93][10];
            this.monsterStrength = this.objectAttribute[93][11];
            this.monsterDefence = this.objectAttribute[93][12];
            this.monsterGold = this.objectAttribute[93][13];
            this.monsStatus(graphics, 93);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 7;
        }
        if (this.mapObject[66][126] == '\u0005' && !this.messageFlag) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.moveChara(graphics, 124, 43, 3, 0);
            this.moveChara(graphics, 124, 44, 2, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[93][10];
            this.monsterStrength = this.objectAttribute[93][11];
            this.monsterDefence = this.objectAttribute[93][12];
            this.monsterGold = this.objectAttribute[93][13];
            this.monsStatus(graphics, 93);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 6;
        }
        if (this.mapObject[66][126] == '\u0004' && !this.messageFlag) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.strNumber = 32;
            this.messageFlag = true;
            this.mapObject[73][127] = 2;
            this.mapObject[66][126] = 5;
        }
        if (this.mapObject[66][126] == '\u0003' && !this.attackFlag) {
            this.moveChara(graphics, 120, 43, 1, 0);
            this.moveChara(graphics, 121, 43, 1, 0);
            this.moveChara(graphics, 122, 43, 3, 0);
            this.moveChara(graphics, 122, 44, 1, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[94][10];
            this.monsterStrength = this.objectAttribute[94][11];
            this.monsterDefence = this.objectAttribute[94][12];
            this.monsterGold = this.objectAttribute[94][13];
            this.monsStatus(graphics, 94);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 4;
        }
        if (this.mapObject[66][126] == '\u0002' && !this.attackFlag) {
            this.moveChara(graphics, 121, 43, 1, 0);
            this.moveChara(graphics, 122, 43, 3, 0);
            this.moveChara(graphics, 122, 44, 1, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[94][10];
            this.monsterStrength = this.objectAttribute[94][11];
            this.monsterDefence = this.objectAttribute[94][12];
            this.monsterGold = this.objectAttribute[94][13];
            this.monsStatus(graphics, 94);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 3;
        }
        if (this.mapObject[66][126] == '\u0001' && !this.messageFlag) {
            this.mapObject[69][124] = 17;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.moveChara(graphics, 122, 43, 3, 0);
            this.moveChara(graphics, 122, 44, 1, 0);
            this.moveChara(graphics, 123, 44, 3, 0);
            this.monsterEnergy = this.objectAttribute[94][10];
            this.monsterStrength = this.objectAttribute[94][11];
            this.monsterDefence = this.objectAttribute[94][12];
            this.monsterGold = this.objectAttribute[94][13];
            this.monsStatus(graphics, 94);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[66][126] = 2;
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 46 && this.mapObject[47][123] == '\u0000' && this.mapObject[41][123] == 'Z' && this.mapObject[66][126] == '\u0000') {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.displayDoor(graphics, 123, 47, 4);
            this.mapObject[47][123] = 20;
            this.displayCharacter(graphics, 123, 30);
            if (this.mapObject[43][120] != '^') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[43][120] = 94;
                this.displayCharacter(graphics, 120, 43);
            }
            if (this.mapObject[43][121] != '^') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[43][121] = 94;
                this.displayCharacter(graphics, 121, 43);
            }
            if (this.mapObject[43][122] != '^') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[43][122] = 94;
                this.displayCharacter(graphics, 122, 43);
            }
            if (this.mapObject[43][124] != ']') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[43][124] = 93;
                this.displayCharacter(graphics, 124, 43);
            }
            if (this.mapObject[43][125] != ']') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[43][125] = 93;
                this.displayCharacter(graphics, 125, 43);
            }
            if (this.mapObject[43][126] != ']') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[43][126] = 93;
                this.displayCharacter(graphics, 126, 43);
            }
            if (this.mapObject[41][119] != '\\') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[41][119] = 92;
                this.displayCharacter(graphics, 119, 41);
            }
            if (this.mapObject[41][120] != '\\') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[41][120] = 92;
                this.displayCharacter(graphics, 120, 41);
            }
            if (this.mapObject[41][121] != '\\') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[41][121] = 92;
                this.displayCharacter(graphics, 121, 41);
            }
            if (this.mapObject[41][125] != '[') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[41][125] = 91;
                this.displayCharacter(graphics, 125, 41);
            }
            if (this.mapObject[41][126] != '[') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[41][126] = 91;
                this.displayCharacter(graphics, 126, 41);
            }
            if (this.mapObject[41][127] != '[') {
                this.twait(400);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[41][127] = 91;
                this.displayCharacter(graphics, 127, 41);
            }
            this.twait(400);
            this.strNumber = 31;
            this.messageFlag = true;
            this.mapObject[73][127] = 2;
            this.mapObject[66][126] = '\u0001';
            this.menuFlag = true;
        }
        if (this.mapObject[41][108] == '\u0000' && this.mapObject[43][110] == '\u0000' && this.mapObject[41][106] == '\u0002' && this.mapObject[41][110] == '\u0002' && this.mapObject[43][106] == '\u0002' && this.mapObject[43][108] == '\u0002' && this.mapObject[45][106] == '\u0002' && this.mapObject[45][108] == '\u0002' && this.mapObject[45][110] == '\u0002') {
            this.twait(400);
            this.mapObject[43][108] = 107;
            this.twait(400);
            this.displayDoor(graphics, 108, 43, 1);
            this.displayCharacter(graphics, 108, 43);
        }
        if (this.mapObject[49][92] == '\u0000' && this.mapObject[49][94] == '\u0000' && this.map[48][93] == '\u0003') {
            this.mapObject[48][93] = 89;
            this.map[48][93] = '\u0001';
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 93 && this.charaY / 5 + this.mapY * 13 == 45 && this.mapObject[44][93] == '\u0000') {
            this.twait(400);
            this.displayDoor(graphics, 93, 44, 4);
            this.mapObject[44][93] = 20;
            this.displayCharacter(graphics, 93, 44);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[45][58] == '\u0000' && this.mapObject[42][58] == '\u0014') {
            this.mapObject[45][57] = '\u0000';
            this.displayCharacter(graphics, 57, 45);
            this.mapObject[45][59] = '\u0000';
            this.displayCharacter(graphics, 59, 45);
            this.mapObject[44][57] = '\u0000';
            this.displayCharacter(graphics, 57, 44);
            this.mapObject[44][58] = '\u0000';
            this.displayCharacter(graphics, 58, 44);
            this.mapObject[44][59] = '\u0000';
            this.displayCharacter(graphics, 59, 44);
            this.mapObject[43][57] = '\u0000';
            this.displayCharacter(graphics, 57, 43);
            this.mapObject[43][58] = '\u0000';
            this.displayCharacter(graphics, 58, 43);
            this.mapObject[43][59] = '\u0000';
            this.displayCharacter(graphics, 59, 43);
            this.twait(400);
            this.displayDoor(graphics, 58, 42, 5);
            this.mapObject[42][58] = '\u0000';
            this.displayCharacter(graphics, 58, 42);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[43][57] = 77;
            this.displayCharacter(graphics, 57, 43);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[43][58] = 77;
            this.displayCharacter(graphics, 58, 43);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[43][59] = 77;
            this.displayCharacter(graphics, 59, 43);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[44][58] = 110;
            this.displayCharacter(graphics, 58, 44);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 58 && this.charaY / 5 + this.mapY * 13 == 21 && this.mapObject[22][58] == '\u0000' && this.mapObject[19][58] == 'G') {
            this.twait(400);
            this.displayDoor(graphics, 58, 22, 4);
            this.mapObject[22][58] = 20;
            this.displayCharacter(graphics, 58, 22);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[49][57] == 'X' && this.mapX + 1 + this.mapY * 10 == 35 && this.mapObject[71][126] == '\u0000') {
            this.mapObject[11][24] = '\u0000';
            this.objectAttribute[88][5] = 29;
            this.mapObject[71][126] = '\u0001';
        }
        if (this.mapObject[67][125] == '\u0000' && this.mapObject[43][44] == '\u0000' && this.mapObject[43][46] == '\u0000' && this.mapObject[43][48] == '\u0000' && this.mapObject[43][50] == '\u0000' && this.mapObject[47][44] == '\u0000' && this.mapObject[47][46] == '\u0000' && this.mapObject[47][48] == '\u0000' && this.mapObject[47][50] == '\u0000') {
            this.mapObject[67][125] = '\u0001';
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[45][41] = 28;
            this.displayCharacter(graphics, 41, 45);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[44][40] = '\u0001';
            this.displayCharacter(graphics, 40, 44);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[44][42] = '\u0001';
            this.displayCharacter(graphics, 42, 44);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[46][40] = '\u0001';
            this.displayCharacter(graphics, 40, 46);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[46][42] = '\u0001';
            this.displayCharacter(graphics, 42, 46);
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 36 && this.charaY / 5 + this.mapY * 13 == 44 && this.mapObject[43][36] == '\u0000' && this.mapObject[44][35] == '^' && this.mapObject[44][37] == '^' && this.mapObject[46][35] == ']' && this.mapObject[46][37] == ']') {
            this.twait(400);
            this.displayDoor(graphics, 36, 43, 4);
            this.mapObject[43][36] = 20;
            this.displayCharacter(graphics, 36, 43);
            this.twait(400);
            this.displayDoor(graphics, 36, 47, 4);
            this.mapObject[47][36] = 20;
            this.displayCharacter(graphics, 36, 47);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 36 && this.charaY / 5 + this.mapY * 13 == 46 && this.mapObject[43][36] == '\u0000' && this.mapObject[44][35] == '^' && this.mapObject[44][37] == '^' && this.mapObject[46][35] == ']' && this.mapObject[46][37] == ']') {
            this.twait(400);
            this.displayDoor(graphics, 36, 43, 4);
            this.mapObject[43][36] = 20;
            this.displayCharacter(graphics, 36, 43);
            this.twait(400);
            this.displayDoor(graphics, 36, 47, 4);
            this.mapObject[47][36] = 20;
            this.displayCharacter(graphics, 36, 47);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.charaX % 5 == 0 && this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 35 && this.charaY / 5 + this.mapY * 13 == 49 && this.map[49][34] != '\u0003') {
            this.twait(400);
            this.displayDoor(graphics, 34, 49, 8);
            this.map[49][34] = 3;
            this.displayCharacter(graphics, 34, 49);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[44][35] == '\u0000' && this.mapObject[44][37] == '\u0000' && this.mapObject[46][35] == '\u0000' && this.mapObject[46][37] == '\u0000' && this.mapObject[43][36] == '\u0014' && this.mapObject[47][36] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 36, 43, 5);
            this.mapObject[43][36] = '\u0000';
            this.displayCharacter(graphics, 36, 43);
            this.twait(400);
            this.displayDoor(graphics, 36, 47, 5);
            this.mapObject[47][36] = '\u0000';
            this.displayCharacter(graphics, 36, 47);
        }
        if (!this.messageFlag && this.charaX % 5 == 0 && this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 19 && this.charaY / 5 + this.mapY * 13 == 49 && this.mapObject[76][125] == '\u0004') {
            this.twait(400);
            this.moveChara(graphics, 19, 48, 4, 2);
            this.moveChara(graphics, 19, 47, 4, 2);
            this.moveChara(graphics, 19, 46, 4, 2);
            this.moveChara(graphics, 19, 45, 4, 2);
            this.moveChara(graphics, 19, 44, 4, 2);
            this.moveChara(graphics, 19, 43, 4, 2);
            this.moveChara(graphics, 19, 42, 4, 2);
            this.moveChara(graphics, 19, 41, 4, 2);
            this.moveChara(graphics, 19, 40, 1, 2);
            this.moveChara(graphics, 20, 40, 1, 2);
            this.moveChara(graphics, 21, 40, 1, 2);
            this.moveChara(graphics, 22, 40, 1, 2);
            this.moveChara(graphics, 23, 40, 1, 2);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[40][24] = '\u0000';
            this.displayCharacter(graphics, 24, 40);
            if (this.mapObject[28][111] == 'X') {
                this.mapObject[28][111] = '\u0000';
            }
            this.mapObject[11][24] = 88;
            this.objectAttribute[88][5] = 6;
            this.mapObject[76][125] = 5;
            this.menuFlag = false;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (!this.attackFlag && this.charaX % 5 == 0 && this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 19 && this.charaY / 5 + this.mapY * 13 == 49 && this.mapObject[76][125] == '\u0003') {
            this.mapObject[48][19] = 90;
            this.displayCharacter(graphics, 19, 48);
            this.twait(400);
            this.strNumber = 28;
            this.messageFlag = true;
            this.mapObject[73][127] = '\u0001';
            this.mapObject[76][125] = 4;
        }
        if (this.charaX % 5 == 0 && this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 19 && this.charaY / 5 + this.mapY * 13 == 49 && this.mapObject[76][125] == '\u0002') {
            this.twait(600);
            this.moveChara(graphics, 19, 45, 3, 0);
            this.moveChara(graphics, 19, 46, 3, 0);
            this.moveChara(graphics, 19, 47, 3, 0);
            this.monsterEnergy = this.objectAttribute[90][10];
            this.monsterStrength = this.objectAttribute[90][11];
            this.monsterDefence = this.objectAttribute[90][12];
            this.monsterGold = this.objectAttribute[90][13];
            this.monsStatus(graphics, 90);
            this.attackFlag = true;
            this.attackFlagTurn = false;
            this.waitCounterFlag = true;
            this.monsflag = 1;
            this.attackXp = this.charaX / 5 + this.mapX * 13;
            this.attackYp = this.charaY / 5 + this.mapY * 13 - 1;
            this.mapObject[76][125] = 3;
        }
        if (this.charaX % 5 == 0 && this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 19 && this.charaY / 5 + this.mapY * 13 == 49 && this.mapObject[76][125] == '\u0001') {
            this.twait(600);
            this.strNumber = 222;
            this.messageFlag = true;
            this.mapObject[73][127] = '\u0001';
            this.mapObject[76][125] = 2;
        }
        if (this.charaX % 5 == 0 && this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 19 && this.charaY / 5 + this.mapY * 13 == 49 && this.mapObject[76][125] == '\u0000') {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(600);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[40][24] = 90;
            this.displayCharacter(graphics, 24, 40);
            this.twait(400);
            this.moveChara(graphics, 24, 40, 2, 0);
            this.moveChara(graphics, 23, 40, 2, 0);
            this.moveChara(graphics, 22, 40, 2, 0);
            this.moveChara(graphics, 21, 40, 2, 0);
            this.moveChara(graphics, 20, 40, 2, 0);
            this.moveChara(graphics, 19, 40, 3, 0);
            this.moveChara(graphics, 19, 41, 3, 0);
            this.moveChara(graphics, 19, 42, 3, 0);
            this.moveChara(graphics, 19, 43, 3, 0);
            this.moveChara(graphics, 19, 44, 3, 0);
            this.twait(600);
            this.strNumber = 27;
            this.messageFlag = true;
            this.mapObject[73][127] = '\u0001';
            this.mapObject[76][125] = '\u0001';
            this.menuFlag = true;
        }
        if (this.mapObject[31][120] == '\u0000' && this.mapObject[31][121] == '\u0000' && this.mapObject[31][122] == '\u0000' && this.mapObject[31][124] == '\u0000' && this.mapObject[31][125] == '\u0000' && this.mapObject[31][126] == '\u0000' && this.mapObject[30][123] == '\u0014' && this.mapObject[33][123] == '\u0014') {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.displayDoor(graphics, 123, 30, 5);
            this.mapObject[30][123] = '\u0000';
            this.displayCharacter(graphics, 123, 30);
            this.twait(400);
            this.displayDoor(graphics, 123, 33, 5);
            this.mapObject[33][123] = '\u0000';
            this.displayCharacter(graphics, 123, 33);
            this.mapObject[74][126] = '\u0000';
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.map[27][123] = 70;
            this.displayCharacter(graphics, 123, 27);
            this.twait(400);
            this.mapObject[69][124] = 28;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 32 && this.mapObject[33][123] == '\u0000' && this.mapObject[30][123] == '\u0000' && this.mapObject[31][120] == '-') {
            this.twait(400);
            this.displayDoor(graphics, 123, 30, 4);
            this.mapObject[30][123] = 20;
            this.displayCharacter(graphics, 123, 30);
            this.twait(400);
            this.displayDoor(graphics, 123, 33, 4);
            this.mapObject[33][123] = 20;
            this.displayCharacter(graphics, 123, 33);
            this.mapObject[74][126] = '\u0000';
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[69][124] = 15;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (this.mapObject[71][118] == '\u001d' && this.mapX + 1 + this.mapY * 10 < 29 && this.mapObject[30][110] == 'X' && this.map[29][110] == '\u0003') {
            this.map[29][110] = '\u0001';
            this.mapObject[30][110] = '\u0000';
            this.mapObject[28][111] = 88;
            this.objectAttribute[88][5] = 25;
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 71 && this.charaY / 5 + this.mapY * 13 == 33 && this.mapObject[67][126] == '\u0000') {
            this.strNumber = 22;
            this.messageFlag = true;
            this.mapObject[67][126] = '\u0001';
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[69][124] = 19;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.map[26][45] = '\u0001';
            this.map[27][44] = 3;
            this.map[27][46] = 3;
            this.map[28][45] = '\u0001';
            this.map[29][45] = '\u0001';
            this.map[30][45] = '\u0001';
        }
        if (this.mapObject[74][126] == '\u0014' && !this.messageFlag && this.mapObject[73][124] == '\u0000') {
            this.Name = "";
            if (this.score2 <= 9) {
                ((Component)this.d4).setVisible(true);
                this.mapObject[73][124] = '\u0001';
            } else {
                this.mapObject[73][124] = '\u0001';
            }
        }
        if (this.mapObject[74][126] == '\u0014' && !this.messageFlag && this.mapObject[73][124] == '\u0001' && !this.d4.isShowing()) {
            if (this.score2 <= 9 && this.d4.str != "") {
                this.Name = this.d4.str;
                this.rankUpdate(this.mapY);
            }
            this.mapObject[73][124] = 2;
            this.d3.init(this.mapObject[76][121], this.mapY + 1, this.codeurl);
            if (this.d3.Ans != 0) {
                this.scoreInit(this.d3.Ans);
            }
        }
        if (this.mapObject[74][126] == '\u0014' && !this.messageFlag && this.mapObject[73][124] == '\u0002' && !this.d3.isShowing()) {
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[35][58] = '\u0000';
            this.displayCharacter(graphics, 58, 35);
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[69][124] = 28;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[74][126] = '\u0000';
            this.mapObject[73][124] = '\u0000';
        }
        if (this.mapObject[32][58] == '\u0000' && this.mapObject[36][58] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 58, 36, 5);
            this.mapObject[36][58] = '\u0000';
            this.displayCharacter(graphics, 58, 36);
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            if (this.mapObject[55][110] == 'E') {
                this.mapObject[55][110] = '\u0000';
            } else if (this.mapObject[54][110] == 'E') {
                this.mapObject[54][110] = '\u0000';
            }
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[35][58] = 69;
            this.displayCharacter(graphics, 58, 35);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[34][56] = 28;
            this.displayCharacter(graphics, 56, 34);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[34][57] = 28;
            this.displayCharacter(graphics, 57, 34);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[34][58] = 28;
            this.displayCharacter(graphics, 58, 34);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[34][59] = 28;
            this.displayCharacter(graphics, 59, 34);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[34][60] = 28;
            this.displayCharacter(graphics, 60, 34);
            this.mapObject[69][124] = 28;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 58 && this.charaY / 5 + this.mapY * 13 == 35 && this.mapObject[32][58] == '`' && this.mapObject[36][58] == '\u0000') {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.displayDoor(graphics, 58, 36, 4);
            this.mapObject[36][58] = 20;
            this.displayCharacter(graphics, 58, 36);
            this.twait(400);
            this.strNumber = 21;
            this.messageFlag = true;
            this.mapObject[69][124] = 15;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 45 && this.charaY / 5 + this.mapY * 13 == 26) {
            this.endFlag = true;
        }
        if (this.mapObject[74][126] == '\u0010' && !this.messageFlag && this.mapObject[73][124] == '\u0000') {
            this.Name = "";
            if (this.score2 <= 9) {
                ((Component)this.d4).setVisible(true);
                this.mapObject[73][124] = '\u0001';
            } else {
                this.mapObject[73][124] = '\u0001';
            }
        }
        if (this.mapObject[74][126] == '\u0010' && !this.messageFlag && this.mapObject[73][124] == '\u0001' && !this.d4.isShowing()) {
            if (this.score2 <= 9 && this.d4.str != "") {
                this.Name = this.d4.str;
                this.rankUpdate(this.mapY);
            }
            this.mapObject[73][124] = 2;
            this.d3.init(this.mapObject[76][121], this.mapY + 1, this.codeurl);
            if (this.d3.Ans != 0) {
                this.scoreInit(this.d3.Ans);
            }
        }
        if (this.mapObject[74][126] == '\u0010' && !this.messageFlag && this.mapObject[73][124] == '\u0002' && !this.d3.isShowing()) {
            this.mapObject[74][126] = '\u0000';
            this.mapObject[73][124] = '\u0000';
        }
        if (this.mapObject[74][127] == '\u0001' && this.map[14][123] == '2' && this.mapObject[22][123] == '\u0000' && this.mapObject[16][123] == '\u0000') {
            this.twait(400);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[17][123] = 69;
            this.displayCharacter(graphics, 123, 17);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[18][121] = 80;
            this.displayCharacter(graphics, 121, 18);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[19][121] = 80;
            this.displayCharacter(graphics, 121, 19);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[20][121] = 80;
            this.displayCharacter(graphics, 121, 20);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[18][125] = 83;
            this.displayCharacter(graphics, 125, 18);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[19][125] = 83;
            this.displayCharacter(graphics, 125, 19);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[20][125] = 83;
            this.displayCharacter(graphics, 125, 20);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[21][122] = 76;
            this.displayCharacter(graphics, 122, 21);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[21][123] = 76;
            this.displayCharacter(graphics, 123, 21);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[21][124] = 76;
            this.displayCharacter(graphics, 124, 21);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[18][122] = '\u0001';
            this.displayCharacter(graphics, 122, 18);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[18][123] = '\u0001';
            this.displayCharacter(graphics, 123, 18);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[18][124] = '\u0001';
            this.displayCharacter(graphics, 124, 18);
            this.mapObject[74][127] = 2;
        }
        if (this.mapObject[19][123] == '\u0000' && this.mapObject[22][123] == '\u0014' && this.mapObject[16][123] == '\u0014') {
            this.twait(400);
            this.twait(400);
            this.displayDoor(graphics, 123, 16, 5);
            this.mapObject[16][123] = '\u0000';
            this.displayCharacter(graphics, 123, 16);
            this.twait(400);
            this.displayDoor(graphics, 123, 22, 5);
            this.mapObject[22][123] = '\u0000';
            this.displayCharacter(graphics, 123, 22);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.map[14][123] = 50;
            this.displayCharacter(graphics, 123, 14);
            this.twait(400);
            this.strNumber = 20;
            this.messageFlag = true;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[69][124] = 26;
            this.mapObject[74][127] = '\u0001';
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 21 && this.mapObject[22][123] == '\u0000' && this.mapObject[16][123] == '\u0014') {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.twait(400);
            this.displayDoor(graphics, 123, 22, 4);
            this.mapObject[22][123] = 20;
            this.displayCharacter(graphics, 123, 22);
            this.mapObject[74][126] = '\u0000';
            this.banpaia(graphics);
            this.twait(400);
            this.strNumber = 19;
            this.messageFlag = true;
            this.mapObject[69][124] = 14;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (this.mapObject[74][126] == '\u0011' && !this.messageFlag) {
            this.twait(200);
            this.mapObject[75][119] = '\u0001';
            this.mapObject[24][76] = 151;
            this.configFlag = true;
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[19][58] == '\u0000' && this.mapObject[22][58] == '\u0014' && this.mapObject[16][58] == '\u0014') {
            this.mapObject[19][57] = '\u0000';
            this.displayCharacter(graphics, 57, 19);
            this.mapObject[19][59] = '\u0000';
            this.displayCharacter(graphics, 59, 19);
            this.mapObject[18][57] = '\u0000';
            this.displayCharacter(graphics, 57, 18);
            this.mapObject[18][58] = '\u0000';
            this.displayCharacter(graphics, 58, 18);
            this.mapObject[18][59] = '\u0000';
            this.displayCharacter(graphics, 59, 18);
            this.mapObject[17][57] = '\u0000';
            this.displayCharacter(graphics, 57, 17);
            this.mapObject[17][58] = '\u0000';
            this.displayCharacter(graphics, 58, 17);
            this.mapObject[17][59] = '\u0000';
            this.displayCharacter(graphics, 59, 17);
            this.twait(400);
            this.displayDoor(graphics, 58, 22, 5);
            this.mapObject[22][58] = '\u0000';
            this.displayCharacter(graphics, 58, 22);
            this.displayDoor(graphics, 58, 16, 5);
            this.mapObject[16][58] = '\u0000';
            this.displayCharacter(graphics, 58, 16);
            this.mapObject[74][126] = '\u0000';
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[18][58] = 114;
            this.displayCharacter(graphics, 58, 18);
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 58 && this.charaY / 5 + this.mapY * 13 == 21 && this.mapObject[22][58] == '\u0000' && this.mapObject[19][58] == 'G') {
            this.twait(400);
            this.displayDoor(graphics, 58, 22, 4);
            this.mapObject[22][58] = 20;
            this.displayCharacter(graphics, 58, 22);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[74][126] == '\r' && !this.messageFlag) {
            this.twait(400);
            this.moveChara(graphics, 61, 14, 2, 0);
            this.moveChara(graphics, 60, 14, 2, 0);
            this.moveChara(graphics, 59, 14, 2, 0);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[14][58] = '\u0000';
            this.displayCharacter(graphics, 58, 14);
            this.mapObject[30][110] = 88;
            this.objectAttribute[88][5] = 24;
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[74][126] == '\u000e' && !this.messageFlag) {
            this.moveChara(graphics, 123, 10, 3, 0);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[11][123] = '\u0000';
            this.displayCharacter(graphics, 123, 11);
            this.mapObject[14][61] = 88;
            this.objectAttribute[88][5] = 17;
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[66][125] == '\u0000' && this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 9 && this.map[11][123] == '\u0016') {
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[11][118] = 87;
            this.displayCharacter(graphics, 118, 11);
            this.objectAttribute[87][5] = 16;
            this.mapObject[66][125] = '\u0001';
            this.twait(400);
            this.moveChara(graphics, 118, 11, 4, 0);
            this.moveChara(graphics, 118, 10, 4, 0);
            this.moveChara(graphics, 118, 9, 4, 0);
            this.moveChara(graphics, 118, 8, 1, 0);
            this.moveChara(graphics, 119, 8, 1, 0);
            this.moveChara(graphics, 120, 8, 3, 0);
            this.moveChara(graphics, 120, 9, 3, 0);
            this.moveChara(graphics, 120, 10, 3, 0);
            this.moveChara(graphics, 120, 11, 1, 0);
            this.moveChara(graphics, 121, 11, 1, 0);
            this.moveChara(graphics, 122, 11, 4, 0);
            this.moveChara(graphics, 122, 10, 1, 0);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[74][126] == '\u000b' && !this.messageFlag && this.mapObject[73][124] == '\u0000') {
            this.Name = "";
            if (this.score2 <= 9) {
                ((Component)this.d4).setVisible(true);
                this.mapObject[73][124] = '\u0001';
            } else {
                this.mapObject[73][124] = '\u0001';
            }
        }
        if (this.mapObject[74][126] == '\u000b' && !this.messageFlag && this.mapObject[73][124] == '\u0001' && !this.d4.isShowing()) {
            if (this.score2 <= 9 && this.d4.str != "") {
                this.Name = this.d4.str;
                this.rankUpdate(this.mapY);
            }
            this.mapObject[73][124] = 2;
            this.d3.init(this.mapObject[76][121], this.mapY + 1, this.codeurl);
            if (this.d3.Ans != 0) {
                this.scoreInit(this.d3.Ans);
            }
        }
        if (this.mapObject[74][126] == '\u000b' && !this.messageFlag && this.mapObject[73][124] == '\u0002' && !this.d3.isShowing()) {
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[4][123] = '\u0000';
            this.displayCharacter(graphics, 123, 4);
            this.mapObject[74][126] = '\u0000';
            this.mapObject[73][124] = '\u0000';
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[69][124] = 27;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (this.mapObject[74][126] == '\u000f' && !this.messageFlag) {
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[4][123] = 69;
            this.displayCharacter(graphics, 123, 4);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[3][118] = 13;
            this.displayCharacter(graphics, 118, 3);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[3][119] = 13;
            this.displayCharacter(graphics, 119, 3);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[3][120] = 13;
            this.displayCharacter(graphics, 120, 3);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[3][126] = 14;
            this.displayCharacter(graphics, 126, 3);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[3][127] = 14;
            this.displayCharacter(graphics, 127, 3);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[3][128] = 14;
            this.displayCharacter(graphics, 128, 3);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[4][118] = 12;
            this.displayCharacter(graphics, 118, 4);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[4][119] = 12;
            this.displayCharacter(graphics, 119, 4);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[4][120] = 12;
            this.displayCharacter(graphics, 120, 4);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[4][126] = '\u0001';
            this.displayCharacter(graphics, 126, 4);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[4][127] = '\u0001';
            this.displayCharacter(graphics, 127, 4);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[4][128] = '\u0001';
            this.displayCharacter(graphics, 128, 4);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[1][123] == '\u0000' && this.mapObject[4][121] == '\u0014' && this.mapObject[4][125] == '\u0014' && this.mapObject[7][123] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 121, 4, 5);
            this.mapObject[4][121] = '\u0000';
            this.displayCharacter(graphics, 121, 4);
            this.twait(400);
            this.displayDoor(graphics, 125, 4, 5);
            this.mapObject[4][125] = '\u0000';
            this.displayCharacter(graphics, 125, 4);
            this.twait(400);
            this.displayDoor(graphics, 123, 7, 5);
            this.mapObject[7][123] = '\u0000';
            this.displayCharacter(graphics, 123, 7);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.map[11][123] = 22;
            this.displayCharacter(graphics, 123, 11);
            this.twait(400);
            this.strNumber = 15;
            this.messageFlag = true;
            this.mapObject[74][126] = 15;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[69][124] = 27;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (this.mapObject[4][122] == '\u0000' && this.mapObject[4][123] == '\u0000' && this.mapObject[4][124] == '\u0000' && this.mapObject[5][122] == '\u0000' && this.mapObject[5][124] == '\u0000' && this.mapObject[6][122] == '\u0000' && this.mapObject[6][123] == '\u0000' && this.mapObject[6][124] == '\u0000' && this.mapObject[3][123] == '\u0014') {
            this.twait(400);
            this.strNumber = 14;
            this.messageFlag = true;
            this.twait(400);
            this.displayDoor(graphics, 123, 3, 5);
            this.mapObject[3][123] = '\u0000';
            this.displayCharacter(graphics, 123, 3);
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
        }
        if (this.mapObject[75][126] == '\u0001' && !this.messageFlag) {
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 123, 3, 4, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 123, 2, 4, 0);
            this.twait(250);
            this.twait(400);
            this.displayDoor(graphics, 122, 6, 7);
            this.map[6][122] = '\u0001';
            this.displayCharacter(graphics, 122, 6);
            this.twait(400);
            this.displayDoor(graphics, 124, 6, 7);
            this.map[6][124] = '\u0001';
            this.displayCharacter(graphics, 124, 6);
            this.twait(400);
            this.displayDoor(graphics, 123, 3, 4);
            this.mapObject[3][123] = 20;
            this.displayCharacter(graphics, 123, 3);
            this.twait(400);
            this.displayDoor(graphics, 123, 7, 4);
            this.mapObject[7][123] = 20;
            this.displayCharacter(graphics, 123, 7);
            this.twait(400);
            this.displayDoor(graphics, 121, 4, 5);
            this.mapObject[4][121] = '\u0000';
            this.displayCharacter(graphics, 121, 4);
            this.twait(400);
            this.displayDoor(graphics, 125, 4, 5);
            this.mapObject[4][125] = '\u0000';
            this.displayCharacter(graphics, 125, 4);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 119, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 120, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 121, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 122, 4, 3, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 122, 5, 3, 0);
            this.twait(150);
            if (this.mapObject[72][124] == '\u0001') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 122, 6, 1, 0);
            this.twait(250);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 127, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 126, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 125, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 124, 4, 2, 0);
            this.twait(250);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 120, 3, 3, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 120, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 121, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 122, 4, 3, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 122, 5, 3, 0);
            this.twait(250);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 126, 3, 3, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 126, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 125, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 124, 4, 3, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 124, 5, 3, 0);
            this.twait(250);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 119, 3, 3, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 119, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 120, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 121, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 122, 4, 3, 0);
            this.twait(250);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 127, 3, 3, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 127, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 126, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 125, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 124, 4, 3, 0);
            this.twait(250);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 118, 3, 3, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 118, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 119, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 120, 4, 1, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 121, 4, 1, 0);
            this.twait(250);
            if (this.mapObject[72][124] != '\u0001') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 128, 3, 3, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 128, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 127, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 126, 4, 2, 0);
            this.twait(150);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.moveChara(graphics, 125, 4, 2, 0);
            this.twait(250);
            this.twait(400);
            this.displayDoor(graphics, 121, 4, 4);
            this.mapObject[4][121] = 20;
            this.displayCharacter(graphics, 121, 4);
            this.twait(400);
            this.displayDoor(graphics, 125, 4, 4);
            this.mapObject[4][125] = 20;
            this.displayCharacter(graphics, 125, 4);
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[69][124] = 13;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[75][126] = 2;
        }
        if (this.charaX % 5 == 0 && this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 123 && this.charaY / 5 + this.mapY * 13 == 5 && this.mapObject[3][123] == '\u0010' && this.mapObject[75][126] == '\u0000') {
            this.twait(400);
            this.strNumber = 13;
            this.messageFlag = true;
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[75][126] = '\u0001';
        }
        if (this.mapObject[74][126] == '\f' && !this.messageFlag) {
            this.twait(200);
            this.mapObject[71][119] = '\u0001';
            this.configFlag = true;
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[73][126] == '\u0004' && !this.messageFlag) {
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            graphics.drawImage(this.imgCrop[this.cropIDchara], 200 + this.xp, 360, this);
            graphics.drawImage(this.imgCrop[25], 200 + this.xp, 360, this);
            this.twait(600);
            this.mapObject[67][119] = '\u0000';
            this.flag3F = 1;
            this.map[9][31] = 116;
            this.displayCharacter(graphics, 31, 9);
            this.mapObject[69][119] = '\u0000';
            this.mapObject[70][119] = '\u0000';
            this.mapObject[73][126] = 5;
            this.mapObject[74][126] = 5;
            if (this.mapObject[76][121] == '\u0000') {
                this.OpenningZeno(graphics, 3);
            } else {
                this.OpenningZeno(graphics, 2);
            }
            this.flag3F = 1;
            this.openningFlag = true;
            this.mapX = this.mapAttribute[116][16] / 13;
            this.mapY = this.mapAttribute[116][17] / 13;
            this.charaX = this.mapAttribute[116][16] % 13 * 5;
            this.charaY = this.mapAttribute[116][17] % 13 * 5;
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.UpKey = false;
            this.DownKey = false;
            this.LeftKey = false;
            this.RightKey = false;
            this.mapObject[74][126] = '\u0000';
            this.mapObject[66][118] = 400;
            this.mapObject[67][118] = 10;
            this.mapObject[68][118] = 10;
        }
        if (!this.messageFlag) {
            if (this.mapObject[74][126] == '\u0006') {
                this.strNumber = 266;
                this.messageFlag = true;
            } else if (this.mapObject[74][126] == '\u0007') {
                this.strNumber = 2;
                this.messageFlag = true;
            } else if (this.mapObject[74][126] == '\b') {
                this.strNumber = 3;
                this.messageFlag = true;
            } else if (this.mapObject[74][126] == '\t') {
                this.flag3F = 1;
                this.openningFlag = false;
                this.map[66][1] = 117;
                this.BGMset();
            }
        }
        if (this.mapObject[73][126] == '\u0003' && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 223;
            this.messageFlag = true;
            this.mapObject[73][126] = 4;
        }
        if (this.mapObject[73][126] == '\u0002' && !this.messageFlag) {
            this.twait(400);
            this.Madoushi(graphics, 31, 9);
            this.mapObject[8][31] = 58;
            this.displayCharacter(graphics, 31, 8);
            this.mapObject[9][30] = 58;
            this.displayCharacter(graphics, 30, 9);
            this.mapObject[9][32] = 58;
            this.displayCharacter(graphics, 32, 9);
            this.mapObject[10][31] = 58;
            this.displayCharacter(graphics, 31, 10);
            this.mapObject[73][126] = 3;
        }
        if (this.mapObject[73][126] == '\u0001' && !this.messageFlag) {
            this.twait(400);
            this.strNumber = 222;
            this.messageFlag = true;
            this.mapObject[73][126] = 2;
        }
        if (this.charaY % 5 == 0 && this.charaX / 5 + this.mapX * 13 == 31 && this.charaY / 5 + this.mapY * 13 == 9 && this.mapObject[73][126] == '\u0000') {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.Zeno(graphics, 31, 7);
            this.twait(400);
            this.strNumber = 10;
            this.messageFlag = true;
            this.mapObject[73][126] = '\u0001';
            this.mapObject[74][126] = 3;
        }
        if (this.mapObject[74][126] == '\u0001' && !this.messageFlag) {
            this.flag3F = 0;
            this.twait(400);
            this.displayDoor(graphics, 15, 7, 7);
            this.map[7][15] = '\u0001';
            this.displayCharacter(graphics, 15, 7);
            this.twait(400);
            this.moveChara(graphics, 16, 7, 2, 0);
            this.moveChara(graphics, 15, 7, 2, 0);
            this.moveChara(graphics, 14, 7, 3, 0);
            this.objectAttribute[87][5] = 5;
            this.mapObject[7][31] = '\u0000';
            this.mapObject[8][31] = '\u0000';
            this.mapObject[9][30] = '\u0000';
            this.mapObject[9][32] = '\u0000';
            this.mapObject[10][31] = '\u0000';
            this.map[9][31] = '\u0001';
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[74][126] == '\u0002' && !this.messageFlag) {
            this.twait(400);
            this.moveChara(graphics, 14, 8, 3, 0);
            this.moveChara(graphics, 14, 9, 3, 0);
            this.moveChara(graphics, 14, 10, 3, 0);
            this.twait(400);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[11][14] = '\u0000';
            this.displayCharacter(graphics, 14, 11);
            this.mapObject[74][126] = '\u0000';
        }
        if (this.mapObject[69][126] == '\u0001' && this.mapObject[4][24] == '\u00ae' && !this.messageFlag) {
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[69][126] = 2;
            this.mapObject[69][118] = (char)(this.mapObject[69][118] + 1000);
            this.mapObject[4][24] = 173;
            this.configFlag = true;
        }
        if (this.mapObject[70][126] == '\u0001' && this.mapObject[7][24] == '\u0098' && !this.messageFlag) {
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.mapObject[70][126] = 2;
            this.mapObject[67][118] = (char)((double)this.mapObject[67][118] * 1.03);
            this.mapObject[68][118] = (char)((double)this.mapObject[68][118] * 1.03);
            this.mapObject[7][24] = 151;
            this.configFlag = true;
        }
        if (this.mapObject[2][19] == '\u0000' && this.mapObject[2][21] == '\u0000' && this.mapObject[5][18] == '\u0013') {
            this.twait(400);
            this.displayDoor(graphics, 18, 5, 6);
            this.mapObject[5][18] = '\u0000';
            this.displayCharacter(graphics, 18, 5);
            this.twait(400);
            this.displayDoor(graphics, 22, 5, 6);
            this.mapObject[5][22] = '\u0000';
            this.displayCharacter(graphics, 22, 5);
            this.twait(400);
            this.displayDoor(graphics, 18, 8, 6);
            this.mapObject[8][18] = '\u0000';
            this.displayCharacter(graphics, 18, 8);
            this.twait(400);
            this.displayDoor(graphics, 22, 8, 6);
            this.mapObject[8][22] = '\u0000';
            this.displayCharacter(graphics, 22, 8);
            this.twait(400);
            this.displayDoor(graphics, 18, 11, 6);
            this.mapObject[11][18] = '\u0000';
            this.displayCharacter(graphics, 18, 11);
            this.twait(400);
            this.displayDoor(graphics, 22, 11, 6);
            this.mapObject[11][22] = '\u0000';
            this.displayCharacter(graphics, 22, 11);
        }
        if (this.mapObject[5][100] == '\u0000' && this.mapObject[5][102] == '\u0000' && this.mapObject[4][101] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 101, 4, 5);
            this.mapObject[4][101] = '\u0000';
            this.displayCharacter(graphics, 101, 4);
        }
        if (this.mapObject[18][1] == '\u0000' && this.mapObject[18][3] == '\u0000' && this.mapObject[17][2] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 2, 17, 5);
            this.mapObject[17][2] = '\u0000';
            this.displayCharacter(graphics, 2, 17);
        }
        if (this.mapObject[14][40] == '\u0000' && this.mapObject[14][42] == '\u0000' && this.mapObject[15][41] == '\u0000' && this.map[16][40] == '\u0003') {
            this.twait(400);
            this.map[16][40] = '\u0001';
            this.mapObject[16][40] = 28;
            this.displayDoor(graphics, 40, 16, 7);
            this.displayCharacter(graphics, 123, 3);
        }
        if (this.mapObject[18][79] == '\u0000' && this.mapObject[18][81] == '\u0000' && this.mapObject[17][80] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 80, 17, 5);
            this.mapObject[17][80] = '\u0000';
            this.displayCharacter(graphics, 80, 17);
        }
        if (this.mapObject[21][79] == '\u0000' && this.mapObject[21][81] == '\u0000' && this.mapObject[20][80] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 80, 20, 5);
            this.mapObject[20][80] = '\u0000';
            this.displayCharacter(graphics, 80, 20);
        }
        if (this.mapObject[18][87] == '\u0000' && this.mapObject[18][89] == '\u0000' && this.mapObject[17][88] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 88, 17, 5);
            this.mapObject[17][88] = '\u0000';
            this.displayCharacter(graphics, 88, 17);
        }
        if (this.mapObject[21][87] == '\u0000' && this.mapObject[21][89] == '\u0000' && this.mapObject[20][88] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 88, 20, 5);
            this.mapObject[20][88] = '\u0000';
            this.displayCharacter(graphics, 88, 20);
        }
        if (this.mapObject[49][14] == '\u0000' && this.mapObject[49][16] == '\u0000' && this.mapObject[48][15] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 15, 48, 5);
            this.mapObject[48][15] = '\u0000';
            this.displayCharacter(graphics, 15, 48);
        }
        if (this.mapObject[61][44] == '\u0000' && this.mapObject[61][46] == '\u0000' && this.mapObject[60][45] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 45, 60, 5);
            this.mapObject[60][45] = '\u0000';
            this.displayCharacter(graphics, 45, 60);
        }
        if (this.mapObject[61][60] == '\u0000' && this.mapObject[63][60] == '\u0000' && this.mapObject[62][59] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 59, 62, 5);
            this.mapObject[62][59] = '\u0000';
            this.displayCharacter(graphics, 59, 62);
        }
        if (this.mapObject[61][57] == '\u0000' && this.mapObject[63][57] == '\u0000' && this.mapObject[62][56] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 56, 62, 5);
            this.mapObject[62][56] = '\u0000';
            this.displayCharacter(graphics, 56, 62);
        }
        if (this.mapObject[62][109] == '\u0000' && this.mapObject[62][111] == '\u0000' && this.mapObject[61][110] == '\u0014') {
            this.twait(400);
            this.displayDoor(graphics, 110, 61, 5);
            this.mapObject[61][110] = '\u0000';
            this.displayCharacter(graphics, 110, 61);
        }
        if (this.mapObject[60][109] == '\u0000' && this.mapObject[60][111] == '\u0000' && this.mapObject[59][110] == '\u0014' && this.mapObject[71][125] == '\u0000') {
            this.twait(400);
            this.displayDoor(graphics, 110, 59, 5);
            this.mapObject[59][110] = '\u0000';
            this.displayCharacter(graphics, 110, 59);
            this.mapObject[71][125] = '\u0001';
        }
    }

    public void saidan(Graphics graphics) {
        if (this.sai >= 5) {
            this.sai -= 4;
        } else if (this.sai <= 0) {
            this.sai += 4;
        }
        int n = 420;
        int n2 = 174;
        int n3 = 50;
        int n4 = 80;
        n4 = this.charaY / 5 % 13 <= 6 ? (this.charaY / 5 % 13 + 2) * 40 : (this.charaY / 5 % 13 - 6) * 40 - 20;
        if (this.oldsai == 0) {
            graphics.setColor(Color.black);
            graphics.fillRoundRect(n3 + this.xp, n4 + this.yp, n, 200, 10, 10);
            graphics.setColor(Color.white);
            graphics.fillRoundRect(n3 + this.xp + 2, n4 + this.yp + 2, n - 4, 37, 10, 10);
            graphics.setColor(Color.white);
            graphics.fillRoundRect(n3 + this.xp + 2, n4 + this.yp + 40 + 1, n - 4, 38, 10, 10);
            graphics.fillRoundRect(n3 + this.xp + 2, n4 + this.yp + 80 + 1, n - 4, 38, 10, 10);
            graphics.fillRoundRect(n3 + this.xp + 2, n4 + this.yp + 120 + 1, n - 4, 38, 10, 10);
            graphics.fillRoundRect(n3 + this.xp + 2, n4 + this.yp + 160 + 1, n - 4, 37, 10, 10);
            graphics.setColor(Color.yellow);
            graphics.fillRoundRect(n3 + this.xp + 2, n4 + this.yp + 40 * this.sai + 1, n - 4, 38, 10, 10);
            this.oldsai = this.sai;
        }
        int n5 = n4;
        this.drawJapanese(graphics, this.strMessage[this.mapObject[76][121]][208], n3 + 10, n4 + this.yp + 10, 410);
        n4 = n5 + 40;
        this.drawJapanese(graphics, this.strMessage[this.mapObject[76][121]][209] + (this.mapObject[66][119] + '\u0001') * 100 + this.strMessage[this.mapObject[76][121]][210], n3 + 10, n4 + this.yp + 10, 410);
        n4 = n5 + 80;
        this.drawJapanese(graphics, this.strMessage[this.mapObject[76][121]][211] + (this.mapY * 2 + 2) + this.strMessage[this.mapObject[76][121]][212], n3 + 10, n4 + this.yp + 10, 410);
        n4 = n5 + 120;
        this.drawJapanese(graphics, this.strMessage[this.mapObject[76][121]][213] + (this.mapY * 4 + 4) + this.strMessage[this.mapObject[76][121]][212], n3 + 10, n4 + this.yp + 10, 410);
        n4 = n5 + 160;
        this.drawJapanese(graphics, this.strMessage[this.mapObject[76][121]][214], n3 + 10, n4 + this.yp + 10, 410);
        if (this.sai != this.oldsai) {
            n4 = this.charaY / 5 % 13 <= 6 ? (this.charaY / 5 % 13 + 2) * 40 : (this.charaY / 5 % 13 - 6) * 40 - 20;
            graphics.setColor(Color.white);
            graphics.fillRoundRect(n3 + this.xp + 2, n4 + this.yp + 40 * this.oldsai + 1, n - 4, 38, 10, 10);
            graphics.setColor(Color.yellow);
            graphics.fillRoundRect(n3 + this.xp + 2, n4 + this.yp + 40 * this.sai + 1, n - 4, 38, 10, 10);
            this.oldsai = this.sai;
        }
        if ((this.sai2 == 1 || this.sai2 == 2 || this.sai2 == 3) && this.inputKey) {
            if (this.mapObject[69][118] >= this.getcoin) {
                if (this.sai2 == 1) {
                    this.mapObject[66][118] = (char)(this.mapObject[66][118] + (this.mapObject[66][119] + '\u0001') * 100);
                } else if (this.sai2 == 2) {
                    this.mapObject[67][118] = (char)(this.mapObject[67][118] + this.mapY * 2 + 2);
                } else if (this.sai2 == 3) {
                    this.mapObject[68][118] = (char)(this.mapObject[68][118] + this.mapY * 4 + 4);
                }
                this.messageFlag = true;
                this.strNumber = 1;
                this.strMessage[this.mapObject[76][121]][this.strNumber] = this.strMessage[this.mapObject[76][121]][283];
                this.mapObject[66][119] = (char)(this.mapObject[66][119] + '\u0001');
                this.mapObject[69][118] = (char)(this.mapObject[69][118] - this.getcoin);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.configFlag = true;
            } else {
                this.messageFlag = true;
                this.strNumber = 215;
            }
        }
        if (this.sai2 != 0) {
            this.saidanFlag = false;
            this.itemKeyFlag = false;
        }
        if (this.sai2 == 4) {
            this.configFlag = true;
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
        }
    }

    public boolean yesnoJudge(Graphics graphics) {
        if (this.yesnoNumber != 0) {
            if (!this.yesnoFlag) {
                if (this.yesnoJudge == 1) {
                    graphics.drawImage(this.imgCrop[19], this.yesnoX + this.xp, this.yesnoY, this);
                } else {
                    graphics.drawImage(this.imgCrop[17], this.yesnoX + this.xp, this.yesnoY, this);
                }
                if (this.yesnoJudge == 2) {
                    graphics.drawImage(this.imgCrop[20], this.yesnoX + 40 + this.xp, this.yesnoY, this);
                } else {
                    graphics.drawImage(this.imgCrop[18], this.yesnoX + 40 + this.xp, this.yesnoY, this);
                }
                if (this.yesnoJudge == 1) {
                    if (this.mapObject[72][124] != '\u0000') {
                        this.audio[1].play();
                    }
                } else if (this.yesnoJudge == 2 && this.mapObject[72][124] != '\u0000') {
                    this.audio[2].play();
                }
            }
            if (this.yesnoNumber == 3) {
                if (this.yesnoFlag) {
                    this.drawJapaneseFrame(graphics, "\uff37\uff37\uff21\u306e\u30db\u30fc\u30e0\u30da\u30fc\u30b8\u3078\u30b8\u30e3\u30f3\u30d7\u3057\u307e\u3059\u3002\u3000\u3088\u308d\u3057\u3044\u3067\u3059\u304b\uff1f", 50, 80);
                    this.yesnoFlag = false;
                }
                if (this.yesnoJudge == 1) {
                    try {
                        URL uRL = new URL("http://wwajp.com/index.html");
                        this.getAppletContext().showDocument(uRL, "new");
                    }
                    catch (MalformedURLException malformedURLException) {
                        System.err.println("URL Error!");
                    }
                }
            }
            if (this.yesnoNumber == 5) {
                if (this.yesnoFlag) {
                    this.drawJapaneseFrame(graphics, "\u30ef\u30fc\u30eb\u30c9\u306e\u521d\u3081\u304b\u3089\u30b9\u30bf\u30fc\u30c8\u3057\u306a\u304a\u3057\u307e\u3059\u304b\uff1f", 50, 80);
                    this.yesnoFlag = false;
                }
                if (this.yesnoJudge == 1) {
                    this.loadMapData();
                    this.mapObject[67][119] = 8;
                }
            }
            int n = 420;
            int n2 = 174;
            int n3 = 50;
            int n4 = 80;
            n4 = this.charaY / 5 % 13 <= 6 ? (this.charaY / 5 % 13 + 2) * 40 : (this.charaY / 5 % 13 - 6) * 40 - 20;
            this.yesnoX = n3 + n - 80 - 20;
            this.yesnoY = n4 + n2 - 40 - 20;
            if (this.yesnoNumber == 9) {
                if (this.yesnoFlag) {
                    this.drawJapaneseFrame(graphics, this.strMessage[this.mapObject[76][121]][this.strNumber], 50, 80);
                    this.yesnoFlag = false;
                }
                if (this.yesnoJudge == 1) {
                    this.saidanFlag = true;
                    this.sai = 1;
                    this.sai2 = 0;
                    this.oldsai = 0;
                    this.inputKey = false;
                }
            }
            if (this.yesnoNumber == 6) {
                if (this.yesnoFlag) {
                    this.drawJapaneseFrame(graphics, this.strMessage[this.mapObject[76][121]][this.strNumber], 50, 80);
                    this.yesnoFlag = false;
                }
                if (this.yesnoJudge == 1) {
                    if (this.mapObject[69][118] >= this.objectAttribute[this.mdataBuff][13]) {
                        this.mapObject[69][118] = (char)(this.mapObject[69][118] - this.objectAttribute[this.mdataBuff][13]);
                        if (this.mdataBuff == 18) {
                            this.mapObject[75][118] = (char)(this.mapObject[75][118] + '\u0001');
                            this.mapObject[this.YpBuff][this.XpBuff] = 40;
                        } else if (this.mdataBuff == 17) {
                            this.mapObject[74][118] = (char)(this.mapObject[74][118] + '\u0001');
                        } else if (this.mdataBuff == 41) {
                            this.mapObject[74][118] = (char)(this.mapObject[74][118] + 5);
                            this.mapObject[this.YpBuff][this.XpBuff] = 155;
                        } else if (this.mdataBuff == 156) {
                            this.mapObject[76][118] = (char)(this.mapObject[76][118] + '\u0001');
                            this.mapObject[this.YpBuff][this.XpBuff] = 157;
                        } else if (this.mdataBuff == 159) {
                            this.mapObject[75][118] = (char)(this.mapObject[75][118] + '\u0001');
                            this.mapObject[this.YpBuff][this.XpBuff] = 160;
                        } else if (this.mdataBuff == 162) {
                            this.mapObject[74][118] = (char)(this.mapObject[74][118] + 4);
                            this.mapObject[75][118] = (char)(this.mapObject[75][118] + '\u0001');
                            this.mapObject[this.YpBuff][this.XpBuff] = 163;
                        } else if (this.mdataBuff == 164) {
                            this.mapObject[74][118] = (char)(this.mapObject[74][118] + 3);
                            this.mapObject[this.YpBuff][this.XpBuff] = 165;
                        } else if (this.mdataBuff == 166) {
                            this.mapObject[75][118] = (char)(this.mapObject[75][118] + 3);
                            this.mapObject[this.YpBuff][this.XpBuff] = 169;
                        } else if (this.mdataBuff == 168) {
                            this.mapObject[66][118] = (char)(this.mapObject[66][118] + 2000);
                            this.mapObject[this.YpBuff][this.XpBuff] = 169;
                        } else if (this.mdataBuff == 170) {
                            this.mapObject[73][120] = '\u0001';
                            this.mapObject[this.YpBuff][this.XpBuff] = 171;
                        }
                        this.displayConfigWindow(graphics, true, true, true, false);
                        this.messageFlag = true;
                        this.strNumber = 1;
                        this.strMessage[this.mapObject[76][121]][this.strNumber] = this.strMessage[this.mapObject[76][121]][98];
                    } else {
                        this.messageFlag = true;
                        this.strNumber = 1;
                        this.strMessage[this.mapObject[76][121]][this.strNumber] = this.strMessage[this.mapObject[76][121]][18];
                    }
                }
            }
            if (this.yesnoNumber == 7) {
                if (this.yesnoFlag) {
                    this.drawJapaneseFrame(graphics, this.strMessage[this.mapObject[76][121]][this.strNumber], 50, 80);
                    this.yesnoFlag = false;
                }
                if (this.yesnoJudge == 1) {
                    if (this.mapObject[74][118] > '\u0000') {
                        this.mapObject[74][118] = (char)(this.mapObject[74][118] - '\u0001');
                        this.mapObject[69][118] = (char)(this.mapObject[69][118] + this.objectAttribute[this.mdataBuff][13]);
                        this.mapObject[66][118] = (char)(this.mapObject[66][118] + this.objectAttribute[this.mdataBuff][13]);
                        this.displayConfigWindow(graphics, true, true, true, false);
                    } else {
                        this.messageFlag = true;
                        this.strNumber = 1;
                        this.strMessage[this.mapObject[76][121]][this.strNumber] = this.strMessage[this.mapObject[76][121]][252];
                    }
                }
            }
            if (this.yesnoJudge != 0) {
                this.yesnoNumber = 0;
                this.yesnoJudge = 0;
                this.mapFlagAll = true;
                this.mapFlagErase = false;
            }
            return false;
        }
        return true;
    }

    public void paintMapAll(Graphics graphics) {
        int n;
        int n2;
        if (this.itemFlag != 3 && !this.yusyaFlag && !this.messageFlag && this.mapFlagErase && this.flag3F == 0) {
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(8 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            n2 = 66;
            while (n2 < 77) {
                n = 105;
                while (n < 116) {
                    int n3 = this.mapObject[n2][n] % 11 + 1;
                    int n4 = this.mapObject[n2][n] / 11 + 1;
                    graphics.drawImage(this.imgCrop[26], n3 * 40 + this.xp, n4 * 40 + this.yp, this);
                    this.twait(10);
                    ++n;
                }
                ++n2;
            }
            this.twait(20);
        }
        if (!this.yusyaFlag) {
            n2 = 0;
            while (n2 < 13) {
                n = 0;
                while (n < 13) {
                    this.mdata = this.map[n2 + this.mapY * 13][n + this.mapX * 13];
                    this.cropID = this.mapAttribute[this.mdata][1];
                    this.gBuff.drawImage(this.imgCrop[this.cropID], n * 40, n2 * 40, this);
                    this.mdata = this.mapObject[n2 + this.mapY * 13][n + this.mapX * 13];
                    if (this.mdata != 0) {
                        this.cropID = this.objectAttribute[this.mdata][1];
                        this.gBuff.drawImage(this.imgCrop[this.cropID], n * 40, n2 * 40, this);
                    }
                    if (this.mapObject[67][119] != '\u0000' && !this.openningFlag && !this.endFlag && this.charaX / 5 == n && this.charaY / 5 == n2) {
                        this.gBuff.drawImage(this.imgCrop[this.cropIDchara], n * 40, n2 * 40, this);
                    }
                    ++n;
                }
                ++n2;
            }
        }
        this.displayConfigWindow(graphics, true, true, true, true);
        if (!this.yusyaFlag) {
            graphics.drawImage(this.imgBuff, 0 + this.xp, 0 + this.yp, this);
        }
        if (this.mapFlagErase && this.flag3F == 0 && !this.yusyaFlag) {
            this.BGMset();
        }
        this.mapFlagAll = false;
        if (this.mapObject[74][126] == '\u0005') {
            this.mapObject[74][126] = 6;
        }
        if (this.yusyaFlag) {
            this.ItemExe(0);
        }
        if (this.itemFlag == 2) {
            if (this.chieNum != 0) {
                --this.chieNum;
                this.ItemExe(1);
            } else {
                this.itemFlag = 0;
            }
        }
        this.focusFlag = false;
    }

    public void BGMset() {
        if (this.mapObject[75][124] != '\u0000') {
            this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
        }
        if (this.mapY == 0) {
            this.mapObject[69][124] = 27;
        } else if (this.mapY == 1) {
            this.mapObject[69][124] = 26;
        } else if (this.mapY == 2) {
            this.mapObject[69][124] = 28;
        } else if (this.mapY == 3) {
            this.mapObject[69][124] = 23;
        } else if (this.mapY >= 4) {
            this.mapObject[69][124] = 16;
        }
        if (this.mapObject[75][124] != '\u0000') {
            this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
        }
    }

    public void paintMap(Graphics graphics) {
        int n;
        int n2;
        int n3;
        int n4;
        this.cropIDchara = 0;
        if (this.mapObject[67][119] == '\b') {
            this.cropIDchara = 0;
        } else if (this.mapObject[67][119] == '\u0002') {
            this.cropIDchara = 2;
        } else if (this.mapObject[67][119] == '\u0004') {
            this.cropIDchara = 4;
        } else if (this.mapObject[67][119] == '\u0006') {
            this.cropIDchara = 6;
        }
        if (this.charaX % 5 > 2 && (this.mapObject[67][119] == '\u0004' || this.mapObject[67][119] == '\u0006') || this.charaY % 5 > 2 && (this.mapObject[67][119] == '\b' || this.mapObject[67][119] == '\u0002')) {
            ++this.cropIDchara;
        }
        if (this.charaX % 5 == 0 && (this.mapObject[67][119] == '\u0004' || this.mapObject[67][119] == '\u0006') || this.charaY % 5 == 0 && (this.mapObject[67][119] == '\b' || this.mapObject[67][119] == '\u0002')) {
            if (this.mapObject[67][119] == '\b') {
                this.cropIDchara = 28;
            } else if (this.mapObject[67][119] == '\u0002') {
                this.cropIDchara = 29;
            } else if (this.mapObject[67][119] == '\u0004') {
                this.cropIDchara = 30;
            } else if (this.mapObject[67][119] == '\u0006') {
                this.cropIDchara = 31;
            }
        }
        if (this.mapObject[67][119] == '\u0004' || this.mapObject[67][119] == '\u0006') {
            n4 = this.charaX / 5;
            n3 = this.charaY / 5;
            if (this.charaX % 5 == 0 && this.mapObject[67][119] == '\u0006') {
                --n4;
            }
            if (this.charaX == 65 && this.mapObject[67][119] == '\u0004') {
                --n4;
            }
            n2 = n4;
            n = n3;
            if (n4 >= 0) {
                this.mdata = this.map[n3 + this.mapY * 13][n4 + this.mapX * 13];
                this.cropID = this.mapAttribute[this.mdata][1];
                this.gBuffCharaX.drawImage(this.imgCrop[this.cropID], 0, 0, this);
            }
            this.mdata = this.map[n3 + this.mapY * 13][++n4 + this.mapX * 13];
            this.cropID = this.mapAttribute[this.mdata][1];
            this.gBuffCharaX.drawImage(this.imgCrop[this.cropID], 40, 0, this);
            n4 = this.charaX % 5 * 8;
            if (this.charaX % 5 == 0 && this.mapObject[67][119] == '\u0006') {
                n4 += 40;
            }
            if (this.charaX == 65 && this.mapObject[67][119] == '\u0004') {
                n4 += 40;
            }
            n3 = this.charaY % 5 * 8;
            this.gBuffCharaX.drawImage(this.imgCrop[this.cropIDchara], n4, n3, this);
            n4 = n2;
            n3 = n;
            if (n4 >= 0) {
                this.mdata = this.mapObject[n3 + this.mapY * 13][n4 + this.mapX * 13];
                if (this.mdata != 0) {
                    this.cropID = this.objectAttribute[this.mdata][1];
                    this.gBuffCharaX.drawImage(this.imgCrop[this.cropID], 0, 0, this);
                }
            }
            this.mdata = this.mapObject[n3 + this.mapY * 13][++n4 + this.mapX * 13];
            if (this.mdata != 0) {
                this.cropID = this.objectAttribute[this.mdata][1];
                this.gBuffCharaX.drawImage(this.imgCrop[this.cropID], 40, 0, this);
            }
            n4 = this.charaX / 5 * 40;
            if (this.charaX % 5 == 0 && this.mapObject[67][119] == '\u0006') {
                n4 -= 40;
            }
            if (this.charaX == 65 && this.mapObject[67][119] == '\u0004') {
                n4 -= 40;
            }
            n3 = this.charaY / 5 * 40;
            graphics.drawImage(this.imgBuffCharaX, n4 + this.xp, n3 + this.yp, this);
        }
        if (this.mapObject[67][119] == '\b' || this.mapObject[67][119] == '\u0002') {
            n4 = this.charaX / 5;
            n3 = this.charaY / 5;
            if (this.charaY % 5 == 0 && this.mapObject[67][119] == '\u0002') {
                --n3;
            }
            n2 = n4;
            n = n3;
            if (n3 >= 0) {
                this.mdata = this.map[n3 + this.mapY * 13][n4 + this.mapX * 13];
                this.cropID = this.mapAttribute[this.mdata][1];
                this.gBuffCharaY.drawImage(this.imgCrop[this.cropID], 0, 0, this);
            }
            this.mdata = this.map[++n3 + this.mapY * 13][n4 + this.mapX * 13];
            this.cropID = this.mapAttribute[this.mdata][1];
            this.gBuffCharaY.drawImage(this.imgCrop[this.cropID], 0, 40, this);
            n4 = this.charaX % 5 * 8;
            n3 = this.charaY % 5 * 8;
            if (this.charaY % 5 == 0 && this.mapObject[67][119] == '\u0002') {
                n3 += 40;
            }
            this.gBuffCharaY.drawImage(this.imgCrop[this.cropIDchara], n4, n3, this);
            n4 = n2;
            n3 = n;
            if (n3 >= 0) {
                this.mdata = this.mapObject[n3 + this.mapY * 13][n4 + this.mapX * 13];
                if (this.mdata != 0) {
                    this.cropID = this.objectAttribute[this.mdata][1];
                    this.gBuffCharaY.drawImage(this.imgCrop[this.cropID], 0, 0, this);
                }
            }
            this.mdata = this.mapObject[++n3 + this.mapY * 13][n4 + this.mapX * 13];
            if (this.mdata != 0) {
                this.cropID = this.objectAttribute[this.mdata][1];
                this.gBuffCharaY.drawImage(this.imgCrop[this.cropID], 0, 40, this);
            }
            n4 = this.charaX / 5 * 40;
            n3 = this.charaY / 5 * 40;
            if (this.charaY % 5 == 0 && this.mapObject[67][119] == '\u0002') {
                n3 -= 40;
            }
            graphics.drawImage(this.imgBuffCharaY, n4 + this.xp, n3 + this.yp, this);
        }
        int n5 = 0;
        while (n5 < 13) {
            int n6 = 0;
            while (n6 < 13) {
                if (this.mapFlag[n6][n5]) {
                    this.mdata = this.map[n5 + this.mapY * 13][n6 + this.mapX * 13];
                    this.cropID = this.mapAttribute[this.mdata][1];
                    this.gBuffMap.drawImage(this.imgCrop[this.cropID], 0, 0, this);
                    this.mdata = this.mapObject[n5 + this.mapY * 13][n6 + this.mapX * 13];
                    if (this.mdata != 0) {
                        this.cropID = this.countAnimation % 22 < 13 || this.objectAttribute[this.mdata][2] == 0 ? this.objectAttribute[this.mdata][1] : this.objectAttribute[this.mdata][2];
                        this.gBuffMap.drawImage(this.imgCrop[this.cropID], 0, 0, this);
                    }
                    graphics.drawImage(this.imgBuffMap, n6 * 40 + this.xp, n5 * 40 + this.yp, this);
                }
                ++n6;
            }
            ++n5;
        }
    }

    public void setMapFlag(Graphics graphics) {
        int n = 0;
        while (n < 13) {
            int n2 = 0;
            while (n2 < 13) {
                this.mdata = this.mapObject[n + this.mapY * 13][n2 + this.mapX * 13];
                this.mapFlag[n2][n] = false;
                if (this.mdata != 0 && this.countAnimation % 13 == n2 && this.objectAttribute[this.mdata][2] != 0) {
                    this.mapFlag[n2][n] = true;
                }
                ++n2;
            }
            ++n;
        }
        ++this.countAnimation;
    }

    public boolean keyDown(Event event, int n) {
        if (n == 1 && !this.menuFlag) {
            this.dialogFlag = 1;
            return true;
        }
        if (n == 18 && !this.menuFlag) {
            this.dialogFlag = 3;
            return true;
        }
        if (n == 5 && this.LangENG.isEnabled()) {
            this.mapObject[76][121] = '\u0000';
            this.menulang();
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (n == 16 && this.LangJPN.isEnabled()) {
            this.mapObject[76][121] = '\u0001';
            this.menulang();
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (n == 23 && this.subsound1.isEnabled()) {
            this.mapObject[72][124] = '\u0001';
            this.subsound1.setEnabled(false);
            this.subsound3.setEnabled(true);
            this.subsound2.setEnabled(true);
            this.showStatus(this.strMessage[this.mapObject[76][121]][289]);
            this.messageFlag2 = true;
            return true;
        }
        if (n == 15 && this.subsound2.isEnabled()) {
            this.mapObject[72][124] = '\u0000';
            this.subsound1.setEnabled(true);
            this.subsound3.setEnabled(true);
            this.subsound2.setEnabled(false);
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[75][124] = '\u0000';
            this.subBGM1.setEnabled(true);
            this.subBGM3.setEnabled(true);
            this.subBGM2.setEnabled(false);
            this.showStatus(this.strMessage[this.mapObject[76][121]][291]);
            this.messageFlag2 = true;
            return true;
        }
        if (n == 13 && this.subBGM1.isEnabled()) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[75][124] = '\u0001';
            this.subBGM1.setEnabled(false);
            this.subBGM3.setEnabled(true);
            this.subBGM2.setEnabled(true);
            this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            this.showStatus(this.strMessage[this.mapObject[76][121]][290]);
            this.messageFlag2 = true;
            return true;
        }
        if (n == 20 && this.subfont11.isEnabled()) {
            this.FontName = "TimesRoman";
            this.mapObject[68][127] = '\u0001';
            this.subfont11.setEnabled(false);
            this.subfont12.setEnabled(true);
            this.subfont13.setEnabled(true);
            this.subfont14.setEnabled(true);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (n == 4 && this.subfont12.isEnabled()) {
            this.FontName = "Dialog";
            this.mapObject[68][127] = 2;
            this.subfont11.setEnabled(true);
            this.subfont12.setEnabled(false);
            this.subfont13.setEnabled(true);
            this.subfont14.setEnabled(true);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (n == 8 && this.subfont13.isEnabled()) {
            this.FontName = "Helvetica";
            this.mapObject[68][127] = 3;
            this.subfont11.setEnabled(true);
            this.subfont12.setEnabled(true);
            this.subfont13.setEnabled(false);
            this.subfont14.setEnabled(true);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (n == 3 && this.subfont14.isEnabled()) {
            this.FontName = "Courier";
            this.mapObject[68][127] = 4;
            this.subfont11.setEnabled(true);
            this.subfont12.setEnabled(true);
            this.subfont13.setEnabled(true);
            this.subfont14.setEnabled(false);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (n == 12 && this.mapObject[70][127] <= '\u001e') {
            this.mapObject[70][127] = (char)(this.mapObject[70][127] + 2);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (n == 19 && this.mapObject[70][127] >= '\n') {
            this.mapObject[70][127] = (char)(this.mapObject[70][127] - 2);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (n == 14 && this.subfont21.isEnabled()) {
            this.mapObject[69][127] = '\u0001';
            this.subfont21.setEnabled(false);
            this.subfont22.setEnabled(true);
            this.subfont23.setEnabled(true);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (n == 2 && this.subfont22.isEnabled()) {
            this.mapObject[69][127] = 2;
            this.subfont21.setEnabled(true);
            this.subfont22.setEnabled(false);
            this.subfont23.setEnabled(true);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (n == 9 && this.subfont23.isEnabled()) {
            this.mapObject[69][127] = 3;
            this.subfont21.setEnabled(true);
            this.subfont22.setEnabled(true);
            this.subfont23.setEnabled(false);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            return true;
        }
        if (this.subload1.isEnabled() && (event.modifiers & 2) != 0 && n == 49) {
            this.dialogFlag = 11;
            return true;
        }
        if (this.subload2.isEnabled() && (event.modifiers & 2) != 0 && n == 50) {
            this.dialogFlag = 12;
            return true;
        }
        if (this.subload3.isEnabled() && (event.modifiers & 2) != 0 && n == 51) {
            this.dialogFlag = 13;
            return true;
        }
        if (this.subload4.isEnabled() && (event.modifiers & 2) != 0 && n == 52) {
            this.dialogFlag = 14;
            return true;
        }
        if (this.subload5.isEnabled() && (event.modifiers & 2) != 0 && n == 53) {
            this.dialogFlag = 15;
            return true;
        }
        if (this.subload6.isEnabled() && (event.modifiers & 2) != 0 && n == 54) {
            this.dialogFlag = 16;
            return true;
        }
        if (this.subload7.isEnabled() && (event.modifiers & 2) != 0 && n == 55) {
            this.dialogFlag = 17;
            return true;
        }
        if (this.subload8.isEnabled() && (event.modifiers & 2) != 0 && n == 56) {
            this.dialogFlag = 18;
            return true;
        }
        if (n == 65535 || n == 0) {
            this.VerX = 0;
            this.VerY = 0;
            this.popupFlag = true;
            return true;
        }
        if (n == 27) {
            this.configFlag = true;
            if (this.itemKeyFlag) {
                this.itemKeyFlag = false;
                this.itemFlag = 0;
            }
            if (!this.inputKey) {
                this.inputKey = true;
            }
            if (this.messageFlag) {
                this.messageFlag = false;
            }
            if (this.yusyaFlag) {
                this.yusyaFlag = false;
                this.itemKeyFlag = false;
            }
            if (this.itemFlag != 0) {
                this.itemFlag = 0;
            }
            if (this.saidanFlag) {
                this.sai2 = 4;
            }
            if (this.yesnoNumber != 0) {
                this.yesnoJudge = 2;
            }
            return true;
        }
        if (n == 10) {
            if (this.yesnoNumber != 0) {
                this.yesnoJudge = 1;
                return true;
            }
            if (!this.saidanFlag && this.itemKeyFlag && this.itemNUM == 0 && (this.itemFlag == 0 && !this.messageFlag || this.itemFlag == 1) && !this.menuFlag) {
                this.ItemExe(0);
                return true;
            }
            if (!this.saidanFlag && this.itemKeyFlag && this.itemNUM == 1 && (this.itemFlag == 2 || this.itemFlag == 0 && !this.messageFlag) && !this.menuFlag) {
                this.ItemExe(1);
                return true;
            }
            if (!(this.saidanFlag || !this.itemKeyFlag || this.itemNUM != 2 || this.mapObject[73][119] != '\u0001' || this.itemFlag != 0 && this.itemFlag != 3 || this.messageFlag || this.menuFlag)) {
                this.ItemExe(2);
                return true;
            }
            if (!this.saidanFlag && this.itemKeyFlag && this.itemNUM >= 4 && this.itemNUM <= 9 && !this.menuFlag) {
                this.itemFlag = this.itemNUM;
                return true;
            }
            if (!this.saidanFlag && this.itemKeyFlag && this.itemNUM >= 11 && this.itemNUM <= 13 && !this.menuFlag) {
                this.itemFlag = this.itemNUM;
                return true;
            }
            if (!(this.saidanFlag || !this.itemKeyFlag || this.itemNUM != 3 && this.itemNUM != 10 && this.itemNUM != 14 || this.menuFlag)) {
                this.itemFlag = 0;
                this.itemKeyFlag = false;
                this.configFlag = true;
                return true;
            }
            if (this.saidanFlag) {
                this.sai2 = this.sai;
                this.inputKey = true;
                return true;
            }
            if (!this.saidanFlag && this.itemKeyFlag) {
                this.inputKey = true;
                if (this.messageFlag) {
                    this.messageFlag = false;
                }
                if (this.yusyaFlag) {
                    this.yusyaFlag = false;
                    this.itemKeyFlag = false;
                }
                if (this.itemFlag != 0) {
                    this.itemFlag = 0;
                    this.configFlag = true;
                }
                this.countRepaint = 0;
                return true;
            }
            if (!this.inputKey) {
                this.inputKey = true;
            } else if (!this.messageFlag) {
                this.itemKeyFlag = true;
                this.itemKey();
                this.configFlag = true;
                this.itemFlag = 0;
            }
            if (this.messageFlag) {
                this.messageFlag = false;
            }
            if (this.yusyaFlag) {
                this.yusyaFlag = false;
                this.itemKeyFlag = false;
            }
            if (this.itemFlag == 2) {
                this.itemFlag = 0;
            }
            return true;
        }
        if ((n == 1005 || n == 1006 || n == 1007 || n == 1004 || n == 50 || n == 52 || n == 54 || n == 56) && !this.menuFlag && this.itemFlag == 3 && this.itemKeyFlag) {
            this.itemKeyFlag = false;
            this.itemFlag = 0;
            this.configFlag = true;
        }
        if (!(n != 56 && n != 1004 || this.menuFlag)) {
            if (!this.saidanFlag) {
                this.UpKey = true;
                this.currentKey = 8;
            } else {
                --this.sai;
            }
            return true;
        }
        if (!(n != 50 && n != 1005 || this.menuFlag)) {
            if (!this.saidanFlag) {
                this.DownKey = true;
                this.currentKey = 2;
            } else {
                ++this.sai;
            }
            return true;
        }
        if (!(n != 52 && n != 1006 || this.menuFlag)) {
            this.LeftKey = true;
            this.currentKey = 4;
            return true;
        }
        if (!(n != 54 && n != 1007 || this.menuFlag)) {
            this.RightKey = true;
            this.currentKey = 6;
            return true;
        }
        if (n == 1000 && !this.menuFlag) {
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            return true;
        }
        return true;
    }

    public boolean keyUp(Event event, int n) {
        if (n == 1004) {
            this.UpKey = false;
        } else if (n == 1005) {
            this.DownKey = false;
        } else if (n == 1006) {
            this.LeftKey = false;
        } else if (n == 1007) {
            this.RightKey = false;
        } else {
            this.UpKey = false;
            this.DownKey = false;
            this.LeftKey = false;
            this.RightKey = false;
        }
        return true;
    }

    public boolean mouseDown(Event event, int n, int n2) {
        int n3 = 80;
        n3 = this.charaY / 5 % 13 <= 6 ? (this.charaY / 5 % 13 + 2) * 40 : (this.charaY / 5 % 13 - 6) * 40 - 20;
        this.VerX = n;
        this.VerY = n2;
        if (event.modifiers == 0) {
            if (!(this.saidanFlag || this.VerX < 19 || this.VerX >= 59 || this.VerY < 254 || this.VerY >= 294 || this.mapObject[71][119] != '\u0001' || (this.itemFlag != 0 || this.messageFlag) && this.itemFlag != 1 || this.menuFlag)) {
                this.itemNUM = 0;
                this.configFlag = true;
                this.itemKeyFlag = true;
                this.ItemExe(0);
                return true;
            }
            if (!(this.saidanFlag || this.VerX < 59 || this.VerX >= 99 || this.VerY < 254 || this.VerY >= 294 || this.mapObject[72][119] != '\u0001' || this.itemFlag != 2 && (this.itemFlag != 0 || this.messageFlag) || this.menuFlag)) {
                this.itemNUM = 1;
                this.configFlag = true;
                this.itemKeyFlag = true;
                this.ItemExe(1);
                return true;
            }
            if (!(this.saidanFlag || this.VerX < 99 || this.VerX >= 139 || this.VerY < 254 || this.VerY >= 294 || this.mapObject[73][119] != '\u0001' || this.itemFlag != 0 && this.itemFlag != 3 || this.messageFlag || this.menuFlag)) {
                this.itemNUM = 2;
                this.configFlag = true;
                this.itemKeyFlag = true;
                this.ItemExe(2);
                return true;
            }
            if (!this.saidanFlag && this.VerX >= 59 && this.VerX < 99 && this.VerY >= 294 && this.VerY < 334 && this.mapObject[75][119] == '\u0001' && !this.menuFlag) {
                this.itemFlag = 4;
                this.itemNUM = 4;
                this.configFlag = true;
                this.itemKeyFlag = true;
                return true;
            }
            if (!this.saidanFlag && this.VerX >= 99 && this.VerX < 139 && this.VerY >= 294 && this.VerY < 334 && this.mapObject[76][119] == '\u0001' && !this.menuFlag) {
                this.itemFlag = 5;
                this.itemNUM = 5;
                this.configFlag = true;
                this.itemKeyFlag = true;
                return true;
            }
            if (!this.saidanFlag && this.VerX >= 19 && this.VerX < 59 && this.VerY >= 334 && this.VerY < 374 && this.mapObject[66][120] == '\u0001' && !this.menuFlag) {
                this.itemFlag = 6;
                this.itemNUM = 6;
                this.configFlag = true;
                this.itemKeyFlag = true;
                return true;
            }
            if (!this.saidanFlag && this.VerX >= 59 && this.VerX < 99 && this.VerY >= 334 && this.VerY < 374 && this.mapObject[67][120] != '\u0000' && !this.menuFlag) {
                this.itemFlag = 7;
                this.itemNUM = 7;
                this.configFlag = true;
                this.itemKeyFlag = true;
                return true;
            }
            if (!this.saidanFlag && this.VerX >= 99 && this.VerX < 139 && this.VerY >= 334 && this.VerY < 374 && this.mapObject[68][120] == '\u0001' && !this.menuFlag) {
                this.itemFlag = 8;
                this.itemNUM = 8;
                this.configFlag = true;
                this.itemKeyFlag = true;
                return true;
            }
            if (!this.saidanFlag && this.VerX >= 19 && this.VerX < 59 && this.VerY >= 374 && this.VerY < 414 && this.mapObject[69][120] == '\u0001' && !this.menuFlag) {
                this.itemFlag = 9;
                this.itemNUM = 9;
                this.configFlag = true;
                this.itemKeyFlag = true;
                return true;
            }
            if (!this.saidanFlag && this.VerX >= 99 && this.VerX < 139 && this.VerY >= 374 && this.VerY < 414 && this.mapObject[71][120] == '\u0001' && !this.menuFlag) {
                this.itemFlag = 11;
                this.itemNUM = 11;
                this.configFlag = true;
                this.itemKeyFlag = true;
                return true;
            }
            if (!this.saidanFlag && this.VerX >= 19 && this.VerX < 59 && this.VerY >= 414 && this.VerY < 454 && this.mapObject[72][120] == '\u0001' && !this.menuFlag) {
                this.itemFlag = 12;
                this.itemNUM = 12;
                this.configFlag = true;
                this.itemKeyFlag = true;
                return true;
            }
            if (!this.saidanFlag && this.VerX >= 59 && this.VerX < 99 && this.VerY >= 414 && this.VerY < 454 && this.mapObject[73][120] == '\u0001' && !this.menuFlag) {
                this.itemFlag = 13;
                this.itemNUM = 13;
                this.configFlag = true;
                this.itemKeyFlag = true;
                return true;
            }
            if (this.saidanFlag && this.VerX > 52 + this.xp && this.VerX < 416 + this.xp && this.VerY > n3 + 41 + this.yp && this.VerY < n3 + 198 + this.yp) {
                this.sai2 = this.sai;
                this.inputKey = true;
                return true;
            }
            if (!this.saidanFlag) {
                n = this.VerX - this.xp;
                n2 = this.VerY - this.yp;
                this.inputKey = true;
                if (this.messageFlag) {
                    this.messageFlag = false;
                }
                if (this.yusyaFlag) {
                    this.yusyaFlag = false;
                    this.itemKeyFlag = false;
                }
                if (this.itemFlag == 2) {
                    this.itemFlag = 0;
                }
                this.countRepaint = 0;
                if (this.yesnoNumber != 0) {
                    if (n > this.yesnoX && n < this.yesnoX + 40 && n2 > this.yesnoY && n2 < this.yesnoY + 40) {
                        this.yesnoJudge = 1;
                    } else if (n > this.yesnoX + 40 && n < this.yesnoX + 80 && n2 > this.yesnoY && n2 < this.yesnoY + 40) {
                        this.yesnoJudge = 2;
                    }
                    return true;
                }
                if (n > 0 && n < 520 && n2 > 0 && n2 < 520) {
                    int n4 = n2 >= this.charaY * 8 + 20 ? n2 - (this.charaY * 8 + 20) : this.charaY * 8 + 20 - n2;
                    int n5 = n >= this.charaX * 8 + 20 ? n - (this.charaX * 8 + 20) : this.charaX * 8 + 20 - n;
                    if (this.charaY * 8 + 20 < n2 && n4 > n5) {
                        this.DownKey = true;
                    } else if (this.charaY * 8 + 20 > n2 && n4 > n5) {
                        this.UpKey = true;
                    } else if (this.charaX * 8 + 20 < n && n4 < n5) {
                        this.RightKey = true;
                    } else if (this.charaX * 8 + 20 > n && n4 < n5) {
                        this.LeftKey = true;
                    }
                }
            }
        } else {
            this.popupFlag = true;
        }
        return true;
    }

    public boolean mouseMove(Event event, int n, int n2) {
        int n3 = 80;
        n3 = this.charaY / 5 % 13 <= 6 ? (this.charaY / 5 % 13 + 2) * 40 : (this.charaY / 5 % 13 - 6) * 40 - 20;
        if (this.saidanFlag && n > 52 + this.xp && n < 416 + this.xp && n2 > n3 + 41 + this.yp && n2 < n3 + 198 + this.yp) {
            if (n2 < n3 + 80) {
                this.sai = 1;
            } else if (n2 < n3 + 120) {
                this.sai = 2;
            } else if (n2 < n3 + 160) {
                this.sai = 3;
            } else if (n2 < n3 + 200) {
                this.sai = 4;
            }
        }
        return true;
    }

    public boolean mouseUp(Event event, int n, int n2) {
        this.UpKey = false;
        this.DownKey = false;
        this.LeftKey = false;
        this.RightKey = false;
        return true;
    }

    public boolean gotFocus(Event event, Object object) {
        this.mapFlagAll = true;
        this.mapFlagErase = false;
        this.inputKey = true;
        this.focusFlag = true;
        return true;
    }

    public void itemKey() {
        boolean bl = false;
        int n = -1;
        int[] nArray = new int[15];
        int n2 = 0;
        while (n2 < 5) {
            int n3 = 0;
            while (n3 < 3) {
                int n4 = 71 + n2 * 3 + n3;
                int n5 = 119;
                if (n2 * 3 + n3 >= 6) {
                    n4 -= 11;
                    n5 = 120;
                }
                if (this.mapObject[n4][n5] != '\u0000') {
                    nArray[n2 * 3 + n3] = 1;
                    if (n == -1) {
                        n = n2 * 3 + n3;
                    }
                } else {
                    nArray[n2 * 3 + n3] = 0;
                }
                ++n3;
            }
            ++n2;
        }
        if (n != -1) {
            if (nArray[this.itemNUM] == 0) {
                this.itemNUM = n;
            }
            if (this.DownKey) {
                this.configFlag = true;
                this.DownKey = false;
                this.itemNUM += 3;
                if (this.itemNUM >= 15) {
                    this.itemNUM -= 15;
                }
                if (nArray[this.itemNUM] == 0) {
                    this.itemNUM += 3;
                    if (this.itemNUM >= 15) {
                        this.itemNUM -= 15;
                    }
                }
                if (nArray[this.itemNUM] == 0) {
                    this.itemNUM += 3;
                    if (this.itemNUM >= 15) {
                        this.itemNUM -= 15;
                    }
                }
                if (nArray[this.itemNUM] == 0) {
                    this.itemNUM += 3;
                    if (this.itemNUM >= 15) {
                        this.itemNUM -= 15;
                    }
                }
                if (nArray[this.itemNUM] == 0) {
                    this.itemNUM += 3;
                    if (this.itemNUM >= 15) {
                        this.itemNUM -= 15;
                    }
                }
            } else if (this.UpKey) {
                this.configFlag = true;
                this.UpKey = false;
                this.itemNUM -= 3;
                if (this.itemNUM < 0) {
                    this.itemNUM += 15;
                }
                if (nArray[this.itemNUM] == 0) {
                    this.itemNUM -= 3;
                    if (this.itemNUM < 0) {
                        this.itemNUM += 15;
                    }
                }
                if (nArray[this.itemNUM] == 0) {
                    this.itemNUM -= 3;
                    if (this.itemNUM < 0) {
                        this.itemNUM += 15;
                    }
                }
                if (nArray[this.itemNUM] == 0) {
                    this.itemNUM -= 3;
                    if (this.itemNUM < 0) {
                        this.itemNUM += 15;
                    }
                }
                if (nArray[this.itemNUM] == 0) {
                    this.itemNUM -= 3;
                    if (this.itemNUM < 0) {
                        this.itemNUM += 15;
                    }
                }
            } else if (this.RightKey) {
                this.configFlag = true;
                this.RightKey = false;
                ++this.itemNUM;
                if (this.itemNUM % 3 == 0) {
                    this.itemNUM -= 3;
                }
                if (nArray[this.itemNUM] == 0) {
                    ++this.itemNUM;
                    if (this.itemNUM % 3 == 0) {
                        this.itemNUM -= 3;
                    }
                }
                if (nArray[this.itemNUM] == 0) {
                    ++this.itemNUM;
                    if (this.itemNUM % 3 == 0) {
                        this.itemNUM -= 3;
                    }
                }
            } else if (this.LeftKey) {
                this.configFlag = true;
                this.LeftKey = false;
                --this.itemNUM;
                if ((this.itemNUM + 1) % 3 == 0) {
                    this.itemNUM += 3;
                }
                if (nArray[this.itemNUM] == 0) {
                    --this.itemNUM;
                    if ((this.itemNUM + 1) % 3 == 0) {
                        this.itemNUM += 3;
                    }
                }
                if (nArray[this.itemNUM] == 0) {
                    --this.itemNUM;
                    if ((this.itemNUM + 1) % 3 == 0) {
                        this.itemNUM += 3;
                    }
                }
            }
        } else {
            this.itemKeyFlag = false;
        }
    }

    public boolean action(Event event, Object object) {
        if (event.target == this.subload1) {
            this.Loaddata(1);
        } else if (event.target == this.subload2) {
            this.Loaddata(2);
        } else if (event.target == this.subload3) {
            this.Loaddata(3);
        } else if (event.target == this.subload4) {
            this.Loaddata(4);
        } else if (event.target == this.subload5) {
            this.Loaddata(5);
        } else if (event.target == this.subload6) {
            this.Loaddata(6);
        } else if (event.target == this.subload7) {
            this.Loaddata(7);
        } else if (event.target == this.subload8) {
            this.Loaddata(8);
        } else if (event.target == this.subsave1 && !this.menuFlag) {
            this.Savedata(1);
        } else if (event.target == this.subsave2 && !this.menuFlag) {
            this.Savedata(2);
        } else if (event.target == this.subsave3 && !this.menuFlag) {
            this.Savedata(3);
        } else if (event.target == this.subsave4 && !this.menuFlag) {
            this.Savedata(4);
        } else if (event.target == this.subsave5 && !this.menuFlag) {
            this.Savedata(5);
        } else if (event.target == this.subsave6 && !this.menuFlag) {
            this.Savedata(6);
        } else if (event.target == this.subsave7 && !this.menuFlag) {
            this.Savedata(7);
        } else if (event.target == this.subsave8 && !this.menuFlag) {
            this.Savedata(8);
        } else if (event.target == this.subsound1) {
            this.mapObject[72][124] = '\u0001';
            this.subsound1.setEnabled(false);
            this.subsound3.setEnabled(true);
            this.subsound2.setEnabled(true);
            this.showStatus(this.strMessage[this.mapObject[76][121]][289]);
            this.messageFlag2 = true;
        } else if (event.target == this.subsound3) {
            this.mapObject[72][124] = 2;
            this.subsound1.setEnabled(true);
            this.subsound3.setEnabled(false);
            this.subsound2.setEnabled(true);
            this.showStatus(this.strMessage[this.mapObject[76][121]][292]);
            this.messageFlag2 = true;
        } else if (event.target == this.subsound2) {
            this.mapObject[72][124] = '\u0000';
            this.subsound1.setEnabled(true);
            this.subsound3.setEnabled(true);
            this.subsound2.setEnabled(false);
            this.showStatus(this.strMessage[this.mapObject[76][121]][294]);
            this.messageFlag2 = true;
        } else if (event.target == this.subBGM1) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[75][124] = '\u0001';
            this.subBGM1.setEnabled(false);
            this.subBGM3.setEnabled(true);
            this.subBGM2.setEnabled(true);
            this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            this.showStatus(this.strMessage[this.mapObject[76][121]][290]);
            this.messageFlag2 = true;
        } else if (event.target == this.subBGM3) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[75][124] = 2;
            this.subBGM1.setEnabled(true);
            this.subBGM3.setEnabled(false);
            this.subBGM2.setEnabled(true);
            this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            this.showStatus(this.strMessage[this.mapObject[76][121]][293]);
            this.messageFlag2 = true;
        } else if (event.target == this.subBGM2) {
            if (this.mapObject[75][124] != '\u0000') {
                this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
            }
            this.mapObject[75][124] = '\u0000';
            this.subBGM1.setEnabled(true);
            this.subBGM3.setEnabled(true);
            this.subBGM2.setEnabled(false);
            this.showStatus(this.strMessage[this.mapObject[76][121]][295]);
            this.messageFlag2 = true;
        } else if (event.target == this.LangENG && this.mapObject[76][121] == '\u0001') {
            this.mapObject[76][121] = '\u0000';
            this.menulang();
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        } else if (event.target == this.LangJPN && this.mapObject[76][121] == '\u0000') {
            this.mapObject[76][121] = '\u0001';
            this.menulang();
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        } else if (event.target == this.menuitem4 && !this.menuFlag) {
            this.dialogFlag = 1;
        } else if (event.target == this.menuitem5 && !this.menuFlag) {
            this.dialogFlag = 3;
        } else if (event.target == this.subfont11 && this.mapObject[68][127] != '\u0001') {
            this.FontName = "TimesRoman";
            this.mapObject[68][127] = '\u0001';
            this.subfont11.setEnabled(false);
            this.subfont12.setEnabled(true);
            this.subfont13.setEnabled(true);
            this.subfont14.setEnabled(true);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        } else if (event.target == this.subfont12 && this.mapObject[68][127] != '\u0002') {
            this.FontName = "Dialog";
            this.mapObject[68][127] = 2;
            this.subfont11.setEnabled(true);
            this.subfont12.setEnabled(false);
            this.subfont13.setEnabled(true);
            this.subfont14.setEnabled(true);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        } else if (event.target == this.subfont13 && this.mapObject[68][127] != '\u0003') {
            this.FontName = "Helvetica";
            this.mapObject[68][127] = 3;
            this.subfont11.setEnabled(true);
            this.subfont12.setEnabled(true);
            this.subfont13.setEnabled(false);
            this.subfont14.setEnabled(true);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        } else if (event.target == this.subfont14 && this.mapObject[68][127] != '\u0004') {
            this.FontName = "Courier";
            this.mapObject[68][127] = 4;
            this.subfont11.setEnabled(true);
            this.subfont12.setEnabled(true);
            this.subfont13.setEnabled(true);
            this.subfont14.setEnabled(false);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        } else if (event.target == this.subfont31 && this.mapObject[70][127] <= '\u001e') {
            this.mapObject[70][127] = (char)(this.mapObject[70][127] + 2);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        } else if (event.target == this.subfont32 && this.mapObject[70][127] >= '\n') {
            this.mapObject[70][127] = (char)(this.mapObject[70][127] - 2);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        } else if (event.target == this.subfont21 && this.mapObject[69][127] != '\u0001') {
            this.mapObject[69][127] = '\u0001';
            this.subfont21.setEnabled(false);
            this.subfont22.setEnabled(true);
            this.subfont23.setEnabled(true);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        } else if (event.target == this.subfont22 && this.mapObject[69][127] != '\u0002') {
            this.mapObject[69][127] = 2;
            this.subfont21.setEnabled(true);
            this.subfont22.setEnabled(false);
            this.subfont23.setEnabled(true);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        } else if (event.target == this.subfont23 && this.mapObject[69][127] != '\u0003') {
            this.mapObject[69][127] = 3;
            this.subfont21.setEnabled(true);
            this.subfont22.setEnabled(true);
            this.subfont23.setEnabled(false);
            this.mapFlagAll = true;
            this.mapFlagErase = false;
            this.inputKey = true;
            this.focusFlag = true;
            this.inputKey = true;
        }
        return true;
    }

    public void AudioStop(int n) {
        if (this.audio[n] != null) {
            this.audio[n].stop();
        }
    }

    public void AudioPlay(int n) {
        boolean bl = false;
        if (n == 5) {
            this.FileName = "wav/20f.wav";
        } else if (n == 6) {
            this.FileName = "wav/3f.wav";
        } else if (n == 7) {
            this.FileName = "wav/Get.wav";
        } else if (n == 8) {
            this.FileName = "wav/Kai.wav";
        } else if (n == 9) {
            this.FileName = "wav/Kai2.wav";
        } else if (n == 10) {
            this.FileName = "wav/Open.wav";
        } else if (n == 11) {
            this.FileName = "wav/Taisen.wav";
        } else if (n == 12) {
            this.FileName = "wav/Zeno.wav";
        } else if (n == 13) {
            this.FileName = "midi/A_005xgw.mid";
            bl = true;
        } else if (n == 14) {
            this.FileName = "midi/A_007xgw.mid";
            bl = true;
        } else if (n == 15) {
            this.FileName = "midi/A_008xgw.mid";
            bl = true;
        } else if (n == 16) {
            this.FileName = "midi/A_019xgw.mid";
            bl = true;
        } else if (n == 17) {
            this.FileName = "midi/A_023xgw.mid";
            bl = true;
        } else if (n == 18) {
            this.FileName = "midi/A_027xgw.mid";
            bl = true;
        } else if (n == 19) {
            this.FileName = "midi/A_032xgw.mid";
            bl = true;
        } else if (n == 20) {
            this.FileName = "midi/A_046xgw.mid";
            bl = true;
        } else if (n == 21) {
            this.FileName = "midi/A_050xgw.mid";
            bl = true;
        } else if (n == 22) {
            this.FileName = "midi/A_085xgw.mid";
            bl = true;
        } else if (n == 23) {
            this.FileName = "midi/A_118xgw.mid";
            bl = true;
        } else if (n == 24) {
            this.FileName = "midi/B_014xgw.mid";
            bl = true;
        } else if (n == 25) {
            this.FileName = "midi/B_018xgw.mid";
            bl = true;
        } else if (n == 26) {
            this.FileName = "midi/B_058xgw.mid";
            bl = true;
        } else if (n == 27) {
            this.FileName = "midi/B_067xgw.mid";
            bl = true;
        } else if (n == 28) {
            this.FileName = "midi/B_110xgw.mid";
            bl = true;
        } else if (n == 29) {
            this.FileName = "midi/B_117xgw.mid";
            bl = true;
        } else if (n == 30) {
            this.FileName = "au/5.au";
        } else if (n == 31) {
            this.FileName = "au/6.au";
        } else if (n == 37) {
            this.FileName = "au/12.au";
        } else if (n == 38) {
            this.FileName = "au/13.au";
            bl = true;
        } else if (n == 39) {
            this.FileName = "au/14.au";
            bl = true;
        } else if (n == 40) {
            this.FileName = "au/15.au";
            bl = true;
        } else if (n == 41) {
            this.FileName = "au/16.au";
            bl = true;
        } else if (n == 42) {
            this.FileName = "au/17.au";
            bl = true;
        } else if (n == 43) {
            this.FileName = "au/18.au";
            bl = true;
        } else if (n == 44) {
            this.FileName = "au/19.au";
            bl = true;
        } else if (n == 45) {
            this.FileName = "au/20.au";
            bl = true;
        } else if (n == 46) {
            this.FileName = "au/21.au";
            bl = true;
        } else if (n == 47) {
            this.FileName = "au/22.au";
            bl = true;
        } else if (n == 48) {
            this.FileName = "au/23.au";
            bl = true;
        } else if (n == 49) {
            this.FileName = "au/24.au";
            bl = true;
        } else if (n == 50) {
            this.FileName = "au/25.au";
            bl = true;
        } else if (n == 51) {
            this.FileName = "au/26.au";
            bl = true;
        } else if (n == 52) {
            this.FileName = "au/27.au";
            bl = true;
        } else if (n == 53) {
            this.FileName = "au/28.au";
            bl = true;
        } else if (n == 54) {
            this.FileName = "au/29.au";
            bl = true;
        }
        if (n != 0 && this.audio[n] == null) {
            this.audio[n] = this.getAudioClip(this.getDocumentBase(), this.FileName);
        }
        if (n != 0 && !bl && this.audio[n] != null) {
            this.audio[n].play();
        } else if (n != 0 && this.audio[n] != null) {
            this.audio[n].loop();
        }
    }

    public void menulang() {
        if (this.mapObject[76][121] == '\u0001') {
            this.LangENG.setEnabled(true);
            this.LangJPN.setEnabled(false);
            this.submenu1.setLabel("\u30ed\u30fc\u30c9");
            this.subload1.setLabel("\u30c7\u30fc\u30bf 1");
            this.subload2.setLabel("\u30c7\u30fc\u30bf 2");
            this.subload3.setLabel("\u30c7\u30fc\u30bf 3");
            this.subload4.setLabel("\u30c7\u30fc\u30bf 4");
            this.subload5.setLabel("\u30c7\u30fc\u30bf 5");
            this.subload6.setLabel("\u30c7\u30fc\u30bf 6");
            this.subload7.setLabel("\u30c7\u30fc\u30bf 7");
            this.subload8.setLabel("\u30c7\u30fc\u30bf 8");
            this.submenu2.setLabel("\u30bb\u30fc\u30d6");
            this.subsave1.setLabel("\u30c7\u30fc\u30bf 1");
            this.subsave2.setLabel("\u30c7\u30fc\u30bf 2");
            this.subsave3.setLabel("\u30c7\u30fc\u30bf 3");
            this.subsave4.setLabel("\u30c7\u30fc\u30bf 4");
            this.subsave5.setLabel("\u30c7\u30fc\u30bf 5");
            this.subsave6.setLabel("\u30c7\u30fc\u30bf 6");
            this.subsave7.setLabel("\u30c7\u30fc\u30bf 7");
            this.subsave8.setLabel("\u30c7\u30fc\u30bf 8");
            this.submenu3.setLabel("\u30b5\u30a6\u30f3\u30c9");
            this.subsound1.setLabel("WAV\u30aa\u30f3");
            this.subsound3.setLabel("Au\u30aa\u30f3");
            this.subsound2.setLabel("\u30aa\u30d5");
            this.submenu4.setLabel("BGM");
            this.subBGM1.setLabel("Midi\u30aa\u30f3");
            this.subBGM3.setLabel("Au\u30aa\u30f3");
            this.subBGM2.setLabel("\u30aa\u30d5");
            this.submenu5.setLabel("\u8a00\u8a9e");
            this.LangENG.setLabel("\u82f1\u8a9e");
            this.LangJPN.setLabel("\u65e5\u672c\u8a9e");
            this.menuitem4.setLabel("\u30d0\u30fc\u30b8\u30e7\u30f3\u60c5\u5831");
            this.menuitem5.setLabel("\u30e9\u30f3\u30ad\u30f3\u30b0");
            this.submenu6.setLabel("\u30d5\u30a9\u30f3\u30c8");
            this.subfont1.setLabel("\u540d\u524d");
            this.subfont2.setLabel("\u30b9\u30bf\u30a4\u30eb");
            this.subfont3.setLabel("\u30b5\u30a4\u30ba");
            this.subfont11.setLabel("TimesRoman");
            this.subfont12.setLabel("Dialog");
            this.subfont13.setLabel("Helvetica");
            this.subfont14.setLabel("Courier");
            this.subfont21.setLabel("\u666e\u901a");
            this.subfont22.setLabel("\u592a\u5b57");
            this.subfont23.setLabel("\u659c\u4f53");
            this.subfont31.setLabel("\u5927\u304d\u3044");
            this.subfont32.setLabel("\u5c0f\u3055\u3044");
        } else {
            this.LangENG.setEnabled(false);
            this.LangJPN.setEnabled(true);
            this.submenu1.setLabel("Load");
            this.subload1.setLabel("Data 1");
            this.subload2.setLabel("Data 2");
            this.subload3.setLabel("Data 3");
            this.subload4.setLabel("Data 4");
            this.subload5.setLabel("Data 5");
            this.subload6.setLabel("Data 6");
            this.subload7.setLabel("Data 7");
            this.subload8.setLabel("Data 8");
            this.submenu2.setLabel("Save");
            this.subsave1.setLabel("Data 1");
            this.subsave2.setLabel("Data 2");
            this.subsave3.setLabel("Data 3");
            this.subsave4.setLabel("Data 4");
            this.subsave5.setLabel("Data 5");
            this.subsave6.setLabel("Data 6");
            this.subsave7.setLabel("Data 7");
            this.subsave8.setLabel("Data 8");
            this.submenu3.setLabel("Sound");
            this.subsound1.setLabel("WavOn");
            this.subsound3.setLabel("AuOn");
            this.subsound2.setLabel("Off");
            this.submenu4.setLabel("BGM");
            this.subBGM1.setLabel("MidiOn");
            this.subBGM3.setLabel("AuOn");
            this.subBGM2.setLabel("Off");
            this.submenu5.setLabel("Language");
            this.LangENG.setLabel("English");
            this.LangJPN.setLabel("Japanese");
            this.menuitem4.setLabel("About Magic Tower");
            this.menuitem5.setLabel("Ranking");
            this.submenu6.setLabel("Font");
            this.subfont1.setLabel("Name");
            this.subfont2.setLabel("Style");
            this.subfont3.setLabel("Size");
            this.subfont11.setLabel("TimesRoman");
            this.subfont12.setLabel("Dialog");
            this.subfont13.setLabel("Helvetica");
            this.subfont14.setLabel("Courier");
            this.subfont21.setLabel("Normal");
            this.subfont22.setLabel("Bold");
            this.subfont23.setLabel("Italic");
            this.subfont31.setLabel("Large");
            this.subfont32.setLabel("Small");
        }
    }

    public boolean directCheck(Graphics graphics, int n, int n2) {
        boolean bl = true;
        this.mdata = this.map[n2][n];
        if (this.mapAttribute[this.mdata][3] == 1) {
            this.strNumber = this.mapAttribute[this.mdata][5];
            if (this.strNumber != 0) {
                this.messageFlag = true;
            }
            bl = false;
        }
        this.mdata = this.mapObject[n2][n];
        if (this.mdata != 0) {
            bl = false;
            if (this.objectAttribute[this.mdata][3] == 0) {
                if (this.objectAttribute[this.mdata][4] == 1) {
                    bl = true;
                }
            } else if (this.objectAttribute[this.mdata][3] == 3) {
                this.mapObject[66][118] = (char)(this.mapObject[66][118] + this.objectAttribute[this.mdata][10]);
                this.mapObject[67][118] = (char)(this.mapObject[67][118] + this.objectAttribute[this.mdata][11]);
                this.mapObject[68][118] = (char)(this.mapObject[68][118] + this.objectAttribute[this.mdata][12]);
                this.mapObject[69][118] = (char)(this.mapObject[69][118] + this.objectAttribute[this.mdata][13]);
                if (this.mdata == 30) {
                    this.mapObject[69][119] = 30;
                } else if (this.mdata == 31) {
                    this.mapObject[69][119] = 31;
                } else if (this.mdata == 32) {
                    this.mapObject[69][119] = 32;
                } else if (this.mdata == 33) {
                    this.mapObject[69][119] = 33;
                } else if (this.mdata == 34) {
                    this.mapObject[69][119] = 34;
                } else if (this.mdata == 35) {
                    this.mapObject[70][119] = 35;
                } else if (this.mdata == 36) {
                    this.mapObject[70][119] = 36;
                } else if (this.mdata == 37) {
                    this.mapObject[70][119] = 37;
                } else if (this.mdata == 38) {
                    this.mapObject[70][119] = 38;
                } else if (this.mdata == 39) {
                    this.mapObject[70][119] = 39;
                }
                this.configFlag = true;
                this.messageFlag = false;
                this.strNumber = this.objectAttribute[this.mdata][5];
                this.showStatus(this.strMessage[this.mapObject[76][121]][this.strNumber]);
                this.messageFlag2 = true;
                this.messageFlag3 = this.strNumber;
                bl = true;
                this.mapObject[n2][n] = '\u0000';
                this.displayCharacter(graphics, n, n2);
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
            } else if (this.objectAttribute[this.mdata][3] == 8) {
                if (this.mdata == 1) {
                    this.mapObject[74][118] = (char)(this.mapObject[74][118] + '\u0001');
                } else if (this.mdata == 3) {
                    this.mapObject[75][118] = (char)(this.mapObject[75][118] + '\u0001');
                } else if (this.mdata == 28) {
                    this.mapObject[76][118] = (char)(this.mapObject[76][118] + '\u0001');
                }
                this.displayConfigWindow(graphics, true, true, true, false);
                this.strNumber = this.objectAttribute[this.mdata][5];
                this.showStatus(this.strMessage[this.mapObject[76][121]][this.strNumber]);
                this.messageFlag2 = true;
                this.messageFlag3 = this.strNumber;
                bl = true;
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[n2][n] = '\u0000';
                this.displayCharacter(graphics, n, n2);
            } else if (this.objectAttribute[this.mdata][3] == 4) {
                if (this.mdata == 25) {
                    this.mapObject[72][119] = '\u0001';
                } else if (this.mdata == 26) {
                    this.mapObject[73][119] = '\u0001';
                } else if (this.mdata == 103) {
                    this.mapObject[74][119] = '\u0001';
                } else if (this.mdata == 104) {
                    this.mapObject[75][119] = '\u0001';
                } else if (this.mdata == 114) {
                    this.mapObject[76][119] = '\u0001';
                } else if (this.mdata == 105) {
                    this.mapObject[66][120] = '\u0001';
                } else if (this.mdata == 106) {
                    this.mapObject[67][120] = '\u0001';
                } else if (this.mdata == 107) {
                    this.mapObject[68][120] = '\u0001';
                } else if (this.mdata == 108) {
                    this.mapObject[69][120] = '\u0001';
                } else if (this.mdata == 109) {
                    this.mapObject[70][120] = '\u0001';
                } else if (this.mdata == 110) {
                    this.mapObject[71][120] = '\u0001';
                } else if (this.mdata == 111) {
                    this.mapObject[72][120] = '\u0001';
                } else if (this.mdata == 112) {
                    this.mapObject[73][120] = '\u0001';
                } else if (this.mdata == 113) {
                    this.mapObject[74][120] = '\u0001';
                }
                this.messageFlag = false;
                this.configFlag = true;
                this.strNumber = this.objectAttribute[this.mdata][5];
                this.showStatus(this.strMessage[this.mapObject[76][121]][this.strNumber]);
                this.messageFlag2 = true;
                this.messageFlag3 = this.strNumber;
                bl = true;
                if (this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.mapObject[n2][n] = '\u0000';
                this.displayCharacter(graphics, n, n2);
            } else if (this.objectAttribute[this.mdata][3] == 5) {
                boolean bl2 = false;
                if (this.mdata == 2 & this.mapObject[74][118] > '\u0000') {
                    this.mapObject[74][118] = (char)(this.mapObject[74][118] - '\u0001');
                    bl2 = true;
                } else if (this.mdata == 4 & this.mapObject[75][118] > '\u0000') {
                    this.mapObject[75][118] = (char)(this.mapObject[75][118] - '\u0001');
                    bl2 = true;
                } else if (this.mdata == 27 & this.mapObject[76][118] > '\u0000') {
                    this.mapObject[76][118] = (char)(this.mapObject[76][118] - '\u0001');
                    bl2 = true;
                } else if (this.mdata == 89 || this.mdata == 115) {
                    bl2 = true;
                }
                if (bl2) {
                    this.messageFlag = false;
                    this.messageFlag2 = true;
                    this.messageFlag3 = this.strNumber;
                    if (this.mapObject[n2][n] == this.mdata) {
                        if (this.mdata == 2) {
                            this.displayDoor(graphics, n, n2, 1);
                        } else if (this.mdata == 4) {
                            this.displayDoor(graphics, n, n2, 2);
                        } else if (this.mdata == 27) {
                            this.displayDoor(graphics, n, n2, 3);
                        } else if (this.mdata == 89) {
                            this.displayDoor(graphics, n, n2, 7);
                        } else if (this.mdata == 115 && this.mapX + 1 + this.mapY * 10 == 23) {
                            this.displayDoor(graphics, n, n2, 8);
                            this.map[n2][n] = 3;
                        }
                        this.mapObject[n2][n] = n == 110 && n2 == 16 ? 103 : (n == 76 && n2 == 24 ? 154 : (n == 24 && n2 == 14 ? 17 : (this.mapObject[68][125] == '\u0001' && n == 10 && n2 == 54 ? 99 : 0)));
                        this.displayCharacter(graphics, n, n2);
                    }
                    this.configFlag = true;
                } else {
                    this.messageFlag = false;
                    if (this.mdata == 27) {
                        this.showStatus(this.strMessage[this.mapObject[76][121]][149]);
                        this.messageFlag2 = true;
                    } else {
                        if (this.mdata == 4) {
                            this.showStatus(this.strMessage[this.mapObject[76][121]][148]);
                            this.messageFlag2 = true;
                        } else {
                            this.showStatus(this.strMessage[this.mapObject[76][121]][147]);
                        }
                        this.messageFlag2 = true;
                    }
                }
            } else if (this.objectAttribute[this.mdata][3] == 6) {
                this.attackFlag = true;
                this.attackFlagTurn = true;
                this.monsflag = 1;
                this.monsterEnergy = this.objectAttribute[this.mdata][10];
                this.monsterStrength = this.objectAttribute[this.mdata][11];
                this.monsterDefence = this.objectAttribute[this.mdata][12];
                this.monsterGold = this.objectAttribute[this.mdata][13];
                this.monsStatus(graphics, this.mdata);
                this.attackXp = n;
                this.attackYp = n2;
                if (this.mapObject[67][118] < this.monsterDefence) {
                    this.attackFlag = false;
                    this.attackFlagTurn = false;
                    this.showStatus(this.strMessage[this.mapObject[76][121]][221]);
                    this.messageFlag2 = true;
                }
            } else if (this.objectAttribute[this.mdata][3] == 1) {
                if (this.mapObject[72][124] != '\u0000' && this.mdata == 177) {
                    this.AudioPlay(7 + (this.mapObject[72][124] - '\u0001') * 25);
                }
                this.messageFlag = true;
                this.strNumber = this.objectAttribute[this.mdata][5];
                if (this.strNumber == 55) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[66][122] = '\u0001';
                    }
                } else if (this.strNumber == 56) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[67][122] = '\u0001';
                    }
                } else if (this.strNumber == 57) {
                    this.mapObject[n2][n] = 172;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[68][122] = '\u0001';
                    }
                } else if (this.strNumber == 58) {
                    this.mapObject[n2][n] = 172;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[69][122] = '\u0001';
                    }
                } else if (this.strNumber == 59) {
                    this.mapObject[n2][n] = 172;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[70][122] = '\u0001';
                    }
                } else if (this.strNumber == 60) {
                    this.mapObject[n2][n] = 172;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[71][122] = '\u0001';
                    }
                } else if (this.strNumber == 61) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[72][122] = '\u0001';
                    }
                } else if (this.strNumber == 62) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[73][122] = '\u0001';
                    }
                } else if (this.strNumber == 63) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[74][122] = '\u0001';
                    }
                } else if (this.strNumber == 64) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[75][122] = '\u0001';
                    }
                } else if (this.strNumber == 65) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[76][122] = '\u0001';
                    }
                } else if (this.strNumber == 66) {
                    this.mapObject[n2][n] = 172;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[66][123] = '\u0001';
                    }
                } else if (this.strNumber == 67) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[67][123] = '\u0001';
                    }
                } else if (this.strNumber == 68) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[68][123] = '\u0001';
                    }
                } else if (this.strNumber == 69) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[69][123] = '\u0001';
                    }
                } else if (this.strNumber == 70) {
                    this.mapObject[n2][n] = 172;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[70][123] = '\u0001';
                    }
                } else if (this.strNumber == 71) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[71][123] = '\u0001';
                    }
                } else if (this.strNumber == 72) {
                    this.mapObject[n2][n] = 172;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[72][123] = '\u0001';
                    }
                } else if (this.strNumber == 73) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[73][123] = '\u0001';
                    }
                } else if (this.strNumber == 74) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[74][123] = '\u0001';
                    }
                } else if (this.strNumber == 75) {
                    this.mapObject[n2][n] = 172;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[75][123] = '\u0001';
                    }
                } else if (this.strNumber == 76) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[76][123] = '\u0001';
                    }
                } else if (this.strNumber == 77) {
                    this.mapObject[n2][n] = 172;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[66][124] = '\u0001';
                    }
                } else if (this.strNumber == 78) {
                    this.mapObject[n2][n] = 151;
                    if (this.mapObject[72][119] == '\u0001') {
                        this.mapObject[67][124] = '\u0001';
                    }
                } else if (this.strNumber == 85) {
                    this.mapObject[69][126] = '\u0001';
                } else if (this.strNumber == 80) {
                    this.mapObject[70][126] = '\u0001';
                }
                if (this.strNumber == 4) {
                    this.mapObject[74][126] = '\u0001';
                } else if (this.strNumber == 5) {
                    this.mapObject[74][126] = 2;
                } else if (this.strNumber == 6) {
                    this.objectAttribute[88][5] = 7;
                    this.mapObject[49][57] = 88;
                    this.map[48][56] = '\u0001';
                } else if (this.strNumber == 10) {
                    this.mapObject[74][126] = 3;
                    this.twait(1000);
                } else if (this.strNumber == 11) {
                    this.mapObject[74][126] = 5;
                } else if (this.strNumber == 81) {
                    this.mapObject[74][126] = 12;
                    this.mapObject[n2][n] = 175;
                } else if (this.strNumber == 17) {
                    this.twait(400);
                    this.displayDoor(graphics, 60, 14, 7);
                    this.map[14][60] = '\u0001';
                    this.displayCharacter(graphics, 60, 14);
                    this.mapObject[74][126] = 13;
                } else if (this.strNumber == 16) {
                    this.mapObject[74][126] = 14;
                } else if (this.strNumber == 82) {
                    this.mapObject[74][126] = 17;
                } else if (this.strNumber == 25) {
                    this.objectAttribute[88][5] = 26;
                } else if (this.strNumber == 29) {
                    this.objectAttribute[88][5] = 30;
                } else if (this.strNumber == 23) {
                    this.objectAttribute[44][2] = 0;
                }
            }
            if (this.objectAttribute[this.mdata][3] == 7) {
                this.strNumber = 1;
                this.getcoin = ((this.mapObject[66][119] + '\u0001') * (this.mapObject[66][119] + '\u0001') - (this.mapObject[66][119] + '\u0001') + 2) * 10;
                this.strMessage[this.mapObject[76][121]][1] = this.strMessage[this.mapObject[76][121]][206] + this.getcoin + this.strMessage[this.mapObject[76][121]][207];
                this.yesnoNumber = 9;
                this.yesnoFlag = true;
            }
            if (this.objectAttribute[this.mdata][3] == 11) {
                if (this.mapObject[75][124] != '\u0000') {
                    this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
                }
                this.mapObject[69][124] = 22;
                if (this.mapObject[75][124] != '\u0000') {
                    this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
                }
                this.strNumber = this.objectAttribute[this.mdata][5];
                String string = "";
                String string2 = "";
                this.score = 0;
                this.score2 = 0;
                switch (this.mapY) {
                    case 0: {
                        this.score += (this.mapObject[66][118] - 400) / 50 + 60;
                        this.score += (this.mapObject[67][118] - 29) * 3;
                        this.score += (this.mapObject[68][118] - 35) * 2;
                        this.score += this.mapObject[74][118];
                        this.score += this.mapObject[75][118] * 2;
                        this.score += this.mapObject[76][118] * 3;
                        this.mapObject[74][126] = 11;
                        this.rankSearch(this.mapY);
                        string = this.strMessage[0][this.strNumber] + String.valueOf(this.score) + this.strMessage[0][this.strNumber + 1];
                        string2 = this.strMessage[1][this.strNumber] + String.valueOf(this.score) + this.strMessage[1][this.strNumber + 1];
                        if (this.score2 != 10) {
                            string = string + this.strMessage[0][248] + String.valueOf(this.score2 + 1) + this.strMessage[0][249];
                            string2 = string2 + this.strMessage[1][248] + String.valueOf(this.score2 + 1) + this.strMessage[1][249];
                        }
                        if (this.score < 50) {
                            string = string + this.strMessage[0][226];
                            string2 = string2 + this.strMessage[1][226];
                        } else if (this.score < 60) {
                            string = string + this.strMessage[0][227];
                            string2 = string2 + this.strMessage[1][227];
                        } else if (this.score < 80) {
                            string = string + this.strMessage[0][228];
                            string2 = string2 + this.strMessage[1][228];
                        } else if (this.score < 100) {
                            string = string + this.strMessage[0][229];
                            string2 = string2 + this.strMessage[1][229];
                        } else if (this.score >= 100) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][233] + this.strMessage[0][238] + this.strMessage[0][239];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][233] + this.strMessage[1][238] + this.strMessage[1][239];
                        }
                        this.strNumber = 1;
                        this.strMessage[0][this.strNumber] = string;
                        this.strMessage[1][this.strNumber] = string2;
                        this.messageFlag = true;
                        break;
                    }
                    case 1: {
                        this.score += (this.mapObject[66][118] - 800) / 100 + 60;
                        this.score += (this.mapObject[67][118] - 74) * 2;
                        this.score += this.mapObject[68][118] - 80;
                        this.score += this.mapObject[74][118];
                        this.score += this.mapObject[75][118] * 2;
                        this.score += this.mapObject[76][118] * 3;
                        this.mapObject[74][126] = 16;
                        this.rankSearch(this.mapY);
                        string = this.strMessage[0][this.strNumber] + this.score + this.strMessage[0][this.strNumber + 1];
                        string2 = this.strMessage[1][this.strNumber] + this.score + this.strMessage[1][this.strNumber + 1];
                        if (this.score2 != 10) {
                            string = string + this.strMessage[0][248] + String.valueOf(this.score2 + 1) + this.strMessage[0][249];
                            string2 = string2 + this.strMessage[1][248] + String.valueOf(this.score2 + 1) + this.strMessage[1][249];
                        }
                        if (this.score < 50) {
                            string = string + this.strMessage[0][226];
                            string2 = string2 + this.strMessage[1][226];
                        } else if (this.score < 60) {
                            string = string + this.strMessage[0][227];
                            string2 = string2 + this.strMessage[1][227];
                        } else if (this.score < 80) {
                            string = string + this.strMessage[0][228];
                            string2 = string2 + this.strMessage[1][228];
                        } else if (this.score < 100) {
                            string = string + this.strMessage[0][229];
                            string2 = string2 + this.strMessage[1][229];
                        } else if (this.score < 130) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][233] + this.strMessage[0][238] + this.strMessage[0][239];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][233] + this.strMessage[1][238] + this.strMessage[1][239];
                        } else if (this.score < 160) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][234] + this.strMessage[0][238] + this.strMessage[0][239];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][234] + this.strMessage[1][238] + this.strMessage[1][239];
                        } else if (this.score >= 160) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][235] + this.strMessage[0][238] + this.strMessage[0][239];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][235] + this.strMessage[1][238] + this.strMessage[1][239];
                        }
                        this.strNumber = 1;
                        this.strMessage[0][this.strNumber] = string;
                        this.strMessage[1][this.strNumber] = string2;
                        this.messageFlag = true;
                        this.objectAttribute[69][3] = 1;
                        this.objectAttribute[69][5] = 296;
                        break;
                    }
                    case 2: {
                        this.score += (this.mapObject[66][118] - 3000) / 400 + 60;
                        this.score += (this.mapObject[67][118] - 240) / 2;
                        this.score += (this.mapObject[68][118] - 300) / 3;
                        this.score += this.mapObject[74][118];
                        this.score += this.mapObject[75][118] * 2;
                        this.score += this.mapObject[76][118] * 3;
                        this.mapObject[74][126] = 20;
                        this.rankSearch(this.mapY);
                        string = this.strMessage[0][this.strNumber] + this.score + this.strMessage[0][this.strNumber + 1];
                        string2 = this.strMessage[1][this.strNumber] + this.score + this.strMessage[1][this.strNumber + 1];
                        if (this.score2 != 10) {
                            string = string + this.strMessage[0][248] + String.valueOf(this.score2 + 1) + this.strMessage[0][249];
                            string2 = string2 + this.strMessage[1][248] + String.valueOf(this.score2 + 1) + this.strMessage[1][249];
                        }
                        if (this.score < 50) {
                            string = string + this.strMessage[0][226];
                            string2 = string2 + this.strMessage[1][226];
                        } else if (this.score < 60) {
                            string = string + this.strMessage[0][227];
                            string2 = string2 + this.strMessage[1][227];
                        } else if (this.score < 80) {
                            string = string + this.strMessage[0][228];
                            string2 = string2 + this.strMessage[1][228];
                        } else if (this.score < 100) {
                            string = string + this.strMessage[0][229];
                            string2 = string2 + this.strMessage[1][229];
                        } else if (this.score < 130) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][233] + this.strMessage[0][238] + this.strMessage[0][240];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][233] + this.strMessage[1][238] + this.strMessage[1][240];
                        } else if (this.score < 160) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][233] + this.strMessage[0][238] + this.strMessage[0][240];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][233] + this.strMessage[1][238] + this.strMessage[1][240];
                        } else if (this.score < 190) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][235] + this.strMessage[0][238] + this.strMessage[0][240];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][235] + this.strMessage[1][238] + this.strMessage[1][240];
                        } else if (this.score < 250) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][236] + this.strMessage[0][238] + this.strMessage[0][240];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][236] + this.strMessage[1][238] + this.strMessage[1][240];
                        } else if (this.score >= 250) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][237] + this.strMessage[0][238] + this.strMessage[0][240];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][237] + this.strMessage[1][238] + this.strMessage[1][240];
                        }
                        this.strNumber = 1;
                        this.strMessage[0][this.strNumber] = string;
                        this.strMessage[1][this.strNumber] = string2;
                        this.messageFlag = true;
                        break;
                    }
                    case 3: {
                        this.score += (this.mapObject[66][118] - 1600) / 200 + 60;
                        this.score += this.mapObject[67][118] - 152;
                        this.score += (this.mapObject[68][118] - 198) / 2;
                        this.score += this.mapObject[74][118];
                        this.score += this.mapObject[75][118] * 2;
                        this.score += this.mapObject[76][118] * 3;
                        this.mapObject[74][126] = 21;
                        this.rankSearch(this.mapY);
                        string = this.strMessage[0][this.strNumber] + this.score + this.strMessage[0][this.strNumber + 1];
                        string2 = this.strMessage[1][this.strNumber] + this.score + this.strMessage[1][this.strNumber + 1];
                        if (this.score2 != 10) {
                            string = string + this.strMessage[0][248] + String.valueOf(this.score2 + 1) + this.strMessage[0][249];
                            string2 = string2 + this.strMessage[1][248] + String.valueOf(this.score2 + 1) + this.strMessage[1][249];
                        }
                        if (this.score < 50) {
                            string = string + this.strMessage[0][226];
                            string2 = string2 + this.strMessage[1][226];
                        } else if (this.score < 60) {
                            string = string + this.strMessage[0][227];
                            string2 = string2 + this.strMessage[1][227];
                        } else if (this.score < 80) {
                            string = string + this.strMessage[0][228];
                            string2 = string2 + this.strMessage[1][228];
                        } else if (this.score < 100) {
                            string = string + this.strMessage[0][229];
                            string2 = string2 + this.strMessage[1][229];
                        } else if (this.score < 130) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][233] + this.strMessage[0][238] + this.strMessage[0][239];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][233] + this.strMessage[1][238] + this.strMessage[1][239];
                        } else if (this.score < 160) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][234] + this.strMessage[0][238] + this.strMessage[0][239];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][234] + this.strMessage[1][238] + this.strMessage[1][239];
                        } else if (this.score < 190) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][235] + this.strMessage[0][238] + this.strMessage[0][239];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][235] + this.strMessage[1][238] + this.strMessage[1][239];
                        } else if (this.score >= 190) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][236] + this.strMessage[0][238] + this.strMessage[0][239];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][236] + this.strMessage[1][238] + this.strMessage[1][239];
                        }
                        this.strNumber = 1;
                        this.strMessage[0][this.strNumber] = string;
                        this.strMessage[1][this.strNumber] = string2;
                        this.messageFlag = true;
                        break;
                    }
                    case 4: {
                        this.score += (this.mapObject[66][118] - 3000) / 400 + 60;
                        this.score += (this.mapObject[67][118] - 240) / 2;
                        this.score += (this.mapObject[68][118] - 300) / 3;
                        this.score += this.mapObject[74][118];
                        this.score += this.mapObject[75][118] * 2;
                        this.score += this.mapObject[76][118] * 3;
                        this.mapObject[74][126] = 22;
                        this.rankSearch(this.mapY);
                        string = this.strMessage[0][this.strNumber] + this.score + this.strMessage[0][this.strNumber + 1];
                        string2 = this.strMessage[1][this.strNumber] + this.score + this.strMessage[1][this.strNumber + 1];
                        if (this.score2 != 10) {
                            string = string + this.strMessage[0][248] + String.valueOf(this.score2 + 1) + this.strMessage[0][249];
                            string2 = string2 + this.strMessage[1][248] + String.valueOf(this.score2 + 1) + this.strMessage[1][249];
                        }
                        if (this.score < 50) {
                            string = string + this.strMessage[0][226];
                            string2 = string2 + this.strMessage[1][226];
                        } else if (this.score < 60) {
                            string = string + this.strMessage[0][227];
                            string2 = string2 + this.strMessage[1][227];
                        } else if (this.score < 80) {
                            string = string + this.strMessage[0][228];
                            string2 = string2 + this.strMessage[1][228];
                        } else if (this.score < 100) {
                            string = string + this.strMessage[0][229];
                            string2 = string2 + this.strMessage[1][229];
                        } else if (this.score < 130) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][233] + this.strMessage[0][238] + this.strMessage[0][240];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][233] + this.strMessage[1][238] + this.strMessage[1][240];
                        } else if (this.score < 160) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][234] + this.strMessage[0][238] + this.strMessage[0][240];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][234] + this.strMessage[1][238] + this.strMessage[1][240];
                        } else if (this.score < 190) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][235] + this.strMessage[0][238] + this.strMessage[0][240];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][235] + this.strMessage[1][238] + this.strMessage[1][240];
                        } else if (this.score < 250) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][236] + this.strMessage[0][238] + this.strMessage[0][240];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][236] + this.strMessage[1][238] + this.strMessage[1][240];
                        } else if (this.score >= 250) {
                            string = string + this.strMessage[0][230] + this.strMessage[0][231] + this.strMessage[0][232] + this.strMessage[0][237] + this.strMessage[0][238] + this.strMessage[0][240];
                            string2 = string2 + this.strMessage[1][230] + this.strMessage[1][231] + this.strMessage[1][232] + this.strMessage[1][237] + this.strMessage[1][238] + this.strMessage[1][240];
                        }
                        this.strNumber = 1;
                        this.strMessage[0][this.strNumber] = string;
                        this.strMessage[1][this.strNumber] = string2;
                        this.messageFlag = true;
                    }
                }
            } else if (this.objectAttribute[this.mdata][3] == 15) {
                this.mdataBuff = this.mdata;
                this.XpBuff = n;
                this.YpBuff = n2;
                this.strNumber = this.objectAttribute[this.mdata][5];
                this.yesnoNumber = 7;
                this.yesnoFlag = true;
                if (this.objectAttribute[this.mdata][19] != 0 && this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(this.objectAttribute[this.mdata][19] + (this.mapObject[72][124] - '\u0001') * 25);
                }
            } else if (this.objectAttribute[this.mdata][3] == 14) {
                this.mdataBuff = this.mdata;
                this.XpBuff = n;
                this.YpBuff = n2;
                this.strNumber = this.objectAttribute[this.mdata][5];
                this.yesnoNumber = 6;
                this.yesnoFlag = true;
                if (this.objectAttribute[this.mdata][19] != 0 && this.mapObject[72][124] != '\u0000') {
                    this.AudioPlay(this.objectAttribute[this.mdata][19] + (this.mapObject[72][124] - '\u0001') * 25);
                }
            }
        }
        return bl;
    }

    public void monsStatus(Graphics graphics, int n) {
        if (n != 0) {
            Image image = this.getImage(this.getDocumentBase(), "image/right2.gif");
            this.gBuffStatus.drawImage(image, 0, 280, this);
            Font font = new Font(this.FontName, 1, this.mapObject[70][127] + 2);
            if (this.mapObject[69][127] == '\u0001') {
                font = new Font(this.FontName, 0, this.mapObject[70][127] + 2);
            } else if (this.mapObject[69][127] == '\u0003') {
                font = new Font(this.FontName, 2, this.mapObject[70][127] + 2);
            }
            this.gBuffStatus.setFont(font);
            this.gBuffStatus.setColor(Color.white);
            boolean bl = false;
            this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, 0, this);
            this.gBuffMap.drawImage(this.imgCrop[this.objectAttribute[n][1]], 0, 0, this);
            this.gBuffStatus.drawImage(this.imgBuffMap, 49, 295, 50, 50, this);
            FontMetrics fontMetrics = this.getFontMetrics(font);
            int n2 = fontMetrics.stringWidth(this.strMessage[this.mapObject[76][121]][this.objectAttribute[n][5]]);
            this.gBuffStatus.drawString(this.strMessage[this.mapObject[76][121]][this.objectAttribute[n][5]], 74 - n2 / 2, 370);
            n2 = fontMetrics.stringWidth(String.valueOf(this.monsterEnergy)) - 16;
            this.gBuffStatus.drawString(String.valueOf(this.monsterEnergy), 108 - n2, 397);
            n2 = fontMetrics.stringWidth(String.valueOf(this.objectAttribute[n][11])) - 16;
            this.gBuffStatus.drawString(String.valueOf(this.objectAttribute[n][11]), 108 - n2, 423);
            n2 = fontMetrics.stringWidth(String.valueOf(this.objectAttribute[n][12])) - 16;
            this.gBuffStatus.drawString(String.valueOf(this.objectAttribute[n][12]), 108 - n2, 449);
            n2 = fontMetrics.stringWidth(String.valueOf(this.objectAttribute[n][13])) - 16;
            this.gBuffStatus.drawString(String.valueOf(this.objectAttribute[n][13]), 108 - n2, 475);
            graphics.drawImage(this.imgBuffStatus, 520 + this.xp, 0 + this.yp, this);
            this.displayConfigWindow(graphics, true, true, false, false);
            this.attackDouble = 1;
            if (this.mapObject[74][119] == '\u0001' && (n == 48 || n == 49 || n == 59)) {
                this.attackDouble = 2;
            }
            if (this.mapObject[70][120] == '\u0001' && n == 74) {
                this.attackDouble = 2;
            }
        }
    }

    public void rankSearch(int n) {
        int n2;
        int n3;
        String[][] stringArray = new String[10][5];
        int[][] nArray = new int[11][4];
        boolean bl = false;
        this.FileName = "score/score";
        if (n == 0) {
            this.FileName = this.FileName + "1.dat";
        } else if (n == 1) {
            this.FileName = this.FileName + "2.dat";
        } else if (n == 2) {
            this.FileName = this.FileName + "3.dat";
        } else if (n == 3) {
            this.FileName = this.FileName + "4.dat";
        } else if (n == 4) {
            this.FileName = this.FileName + "5.dat";
        }
        try {
            InputStream inputStream = new URL(this.codeurl, this.FileName).openStream();
            DataInputStream dataInputStream = new DataInputStream(inputStream);
            n3 = 0;
            while (n3 < 10) {
                n2 = 0;
                while (n2 < 5) {
                    stringArray[n3][n2] = dataInputStream.readUTF();
                    ++n2;
                }
                ++n3;
            }
            bl = true;
            dataInputStream.close();
        }
        catch (Exception exception) {
            System.out.println("Error: " + exception);
        }
        if (bl) {
            n3 = 0;
            while (n3 < 10) {
                nArray[n3][0] = Integer.parseInt(stringArray[n3][0]);
                nArray[n3][1] = Integer.parseInt(stringArray[n3][2]);
                nArray[n3][2] = Integer.parseInt(stringArray[n3][3]);
                nArray[n3][3] = Integer.parseInt(stringArray[n3][4]);
                ++n3;
            }
            nArray[10][0] = this.score;
            nArray[10][1] = this.mapObject[66][118];
            nArray[10][2] = this.mapObject[67][118];
            nArray[10][3] = this.mapObject[68][118];
            this.score2 = 10;
            n3 = 0;
            while (n3 < 10) {
                n2 = 0;
                while (n2 < 10) {
                    int n4;
                    int n5;
                    int n6;
                    int n7;
                    if (nArray[n2][0] < nArray[n2 + 1][0]) {
                        n7 = nArray[n2 + 1][0];
                        n6 = nArray[n2 + 1][1];
                        n5 = nArray[n2 + 1][2];
                        n4 = nArray[n2 + 1][3];
                        nArray[n2 + 1][0] = nArray[n2][0];
                        nArray[n2 + 1][1] = nArray[n2][1];
                        nArray[n2 + 1][2] = nArray[n2][2];
                        nArray[n2 + 1][3] = nArray[n2][3];
                        nArray[n2][0] = n7;
                        nArray[n2][1] = n6;
                        nArray[n2][2] = n5;
                        nArray[n2][3] = n4;
                        if (n2 + 1 == this.score2) {
                            --this.score2;
                        }
                    } else if (nArray[n2][0] == nArray[n2 + 1][0]) {
                        if (nArray[n2][1] < nArray[n2 + 1][1]) {
                            n7 = nArray[n2 + 1][0];
                            n6 = nArray[n2 + 1][1];
                            n5 = nArray[n2 + 1][2];
                            n4 = nArray[n2 + 1][3];
                            nArray[n2 + 1][0] = nArray[n2][0];
                            nArray[n2 + 1][1] = nArray[n2][1];
                            nArray[n2 + 1][2] = nArray[n2][2];
                            nArray[n2 + 1][3] = nArray[n2][3];
                            nArray[n2][0] = n7;
                            nArray[n2][1] = n6;
                            nArray[n2][2] = n5;
                            nArray[n2][3] = n4;
                            if (n2 + 1 == this.score2) {
                                --this.score2;
                            }
                        } else if (nArray[n2][1] == nArray[n2 + 1][1]) {
                            if (nArray[n2][2] < nArray[n2 + 1][2]) {
                                n7 = nArray[n2 + 1][0];
                                n6 = nArray[n2 + 1][1];
                                n5 = nArray[n2 + 1][2];
                                n4 = nArray[n2 + 1][3];
                                nArray[n2 + 1][0] = nArray[n2][0];
                                nArray[n2 + 1][1] = nArray[n2][1];
                                nArray[n2 + 1][2] = nArray[n2][2];
                                nArray[n2 + 1][3] = nArray[n2][3];
                                nArray[n2][0] = n7;
                                nArray[n2][1] = n6;
                                nArray[n2][2] = n5;
                                nArray[n2][3] = n4;
                                if (n2 + 1 == this.score2) {
                                    --this.score2;
                                }
                            } else if (nArray[n2][2] == nArray[n2 + 1][2] && nArray[n2][3] < nArray[n2 + 1][3]) {
                                n7 = nArray[n2 + 1][0];
                                n6 = nArray[n2 + 1][1];
                                n5 = nArray[n2 + 1][2];
                                n4 = nArray[n2 + 1][3];
                                nArray[n2 + 1][0] = nArray[n2][0];
                                nArray[n2 + 1][1] = nArray[n2][1];
                                nArray[n2 + 1][2] = nArray[n2][2];
                                nArray[n2 + 1][3] = nArray[n2][3];
                                nArray[n2][0] = n7;
                                nArray[n2][1] = n6;
                                nArray[n2][2] = n5;
                                nArray[n2][3] = n4;
                                if (n2 + 1 == this.score2) {
                                    --this.score2;
                                }
                            }
                        }
                    }
                    ++n2;
                }
                ++n3;
            }
        }
    }

    public void rankUpdate(int n) {
        String[][] stringArray = new String[10][5];
        boolean bl = false;
        this.FileName = "score/score";
        if (n == 0) {
            this.FileName = this.FileName + "1.dat";
        } else if (n == 1) {
            this.FileName = this.FileName + "2.dat";
        } else if (n == 2) {
            this.FileName = this.FileName + "3.dat";
        } else if (n == 3) {
            this.FileName = this.FileName + "4.dat";
        } else if (n == 4) {
            this.FileName = this.FileName + "5.dat";
        }
        try {
            int n2;
            InputStream inputStream = new URL(this.codeurl, this.FileName).openStream();
            DataInputStream dataInputStream = new DataInputStream(inputStream);
            int n3 = 0;
            while (n3 < 10) {
                n2 = 0;
                while (n2 < 5) {
                    stringArray[n3][n2] = dataInputStream.readUTF();
                    ++n2;
                }
                ++n3;
            }
            dataInputStream.close();
            if (this.score2 != 9) {
                n3 = 1;
                while (n3 < 10 - this.score2) {
                    stringArray[10 - n3][0] = stringArray[9 - n3][0];
                    stringArray[10 - n3][1] = stringArray[9 - n3][1];
                    stringArray[10 - n3][2] = stringArray[9 - n3][2];
                    stringArray[10 - n3][3] = stringArray[9 - n3][3];
                    stringArray[10 - n3][4] = stringArray[9 - n3][4];
                    ++n3;
                }
            }
            stringArray[this.score2][0] = String.valueOf(this.score);
            stringArray[this.score2][1] = this.Name;
            stringArray[this.score2][2] = String.valueOf((int)this.mapObject[66][118]);
            stringArray[this.score2][3] = String.valueOf((int)this.mapObject[67][118]);
            stringArray[this.score2][4] = String.valueOf((int)this.mapObject[68][118]);
            FileOutputStream fileOutputStream = new FileOutputStream(this.FileName);
            DataOutputStream dataOutputStream = new DataOutputStream(fileOutputStream);
            n3 = 0;
            while (n3 < 10) {
                n2 = 0;
                while (n2 < 5) {
                    dataOutputStream.writeUTF(stringArray[n3][n2]);
                    ++n2;
                }
                ++n3;
            }
            dataOutputStream.close();
        }
        catch (Exception exception) {
            System.out.println("Error: " + exception);
        }
    }

    public boolean pointCheck(Graphics graphics) {
        int n = this.charaY / 5;
        int n2 = this.charaX / 5;
        int n3 = this.map[n + this.mapY * 13][n2 + this.mapX * 13];
        if (n3 == this.oldMapData && this.oldMapX == n2 + this.mapX * 13 && this.oldMapY == n + this.mapY * 13) {
            return false;
        }
        this.oldMapData = n3;
        this.oldMapX = n2 + this.mapX * 13;
        this.oldMapY = n + this.mapY * 13;
        if (this.mapAttribute[n3][3] == 0) {
            if (this.monsflag != 0) {
                this.monsflag = 0;
                this.displayConfigWindow(graphics, true, true, true, true);
            }
            this.strNumber = this.mapAttribute[n3][5];
            if (!this.messageFlag2) {
                this.showStatus(this.strMessage[this.mapObject[76][121]][267]);
            }
            this.messageFlag2 = false;
            if (this.strNumber != 0) {
                this.messageFlag = true;
                return true;
            }
        }
        if (this.mapAttribute[n3][3] == 2) {
            this.mapX = this.mapAttribute[n3][16] / 13;
            this.mapY = this.mapAttribute[n3][17] / 13;
            this.charaX = this.mapAttribute[n3][16] % 13 * 5;
            this.charaY = this.mapAttribute[n3][17] % 13 * 5;
            if (this.mapY * 10 + this.mapX + 1 <= 50 && this.mapY * 10 + this.mapX + 1 - this.mapObject[71][118] >= 0) {
                this.mapObject[71][118] = (char)(this.mapY * 10 + this.mapX + 1);
                if (this.mapObject[71][118] == '\u0015' && this.mapObject[17][123] == 'E') {
                    this.mapObject[17][123] = '\u0000';
                }
                if (this.mapY * 10 + this.mapX + 1 > 25 && this.mapObject[35][58] == 'E') {
                    this.mapObject[35][58] = '\u0000';
                }
                if (this.mapObject[71][118] == ')' && this.mapObject[41][123] == 'E') {
                    this.mapObject[41][123] = '\u0000';
                }
            }
            this.mapFlagAll = true;
            this.mapFlagErase = true;
            this.UpKey = false;
            this.DownKey = false;
            this.LeftKey = false;
            this.RightKey = false;
            if (n3 != 116 && n3 != 117) {
                this.showStatus(this.strMessage[this.mapObject[76][121]][247]);
                this.messageFlag2 = true;
                this.messageFlag3 = this.mapAttribute[n3][5];
            }
            this.mapObject[67][119] = (char)this.mapAttribute[n3][10];
            this.BGMset();
            if (this.itemFlag != 3 && n3 != 117 && this.mapObject[72][124] != '\u0000') {
                return true;
            }
        }
        return false;
    }

    public void moveCharacter(Graphics graphics) {
        this.charaXold = this.charaX;
        this.charaYold = this.charaY;
        if (this.charaX % 5 == 0 && this.charaY % 5 == 0) {
            int n;
            int n2;
            if (this.pointCheck(graphics)) {
                return;
            }
            int n3 = this.UpKey && this.currentKey == 8 ? 8 : (this.DownKey && this.currentKey == 2 ? 2 : (this.LeftKey && this.currentKey == 4 ? 4 : (this.RightKey && this.currentKey == 6 ? 6 : 0)));
            if (n3 != 0) {
                this.itemFlag = 0;
            }
            if (!(this.UpKey || this.DownKey || this.LeftKey || this.RightKey)) {
                if (this.countRepaint >= 30) {
                    n2 = this.mapX * 13 + (this.countRepaint - 30) % 169 / 13;
                    n = this.mapY * 13 + (this.countRepaint - 30) % 13;
                    if (n2 != this.charaX / 5 + this.mapX * 13 || n != this.charaY / 5 + this.mapY * 13) {
                        this.displayCharacter(graphics, n2, n);
                    }
                    if ((this.countRepaint - 30) % 121 == 120) {
                        this.displayConfigWindow(graphics, false, false, false, false);
                    }
                }
                ++this.countRepaint;
            } else {
                this.countRepaint = 0;
            }
            if (n3 == 8 || n3 == 0 && this.UpKey) {
                this.mapObject[67][119] = 8;
                if (this.charaY != 0 && this.directCheck(graphics, n2 = this.charaX / 5 + this.mapX * 13, n = this.charaY / 5 + this.mapY * 13 - 1)) {
                    this.charaY -= this.movePlus;
                    this.yanime = true;
                }
            } else if (n3 == 2 || n3 == 0 && this.DownKey) {
                this.mapObject[67][119] = 2;
                if (this.charaY != 65 && this.directCheck(graphics, n2 = this.charaX / 5 + this.mapX * 13, n = this.charaY / 5 + this.mapY * 13 + 1)) {
                    this.charaY += this.movePlus;
                    this.yanime = true;
                }
            } else if (n3 == 4 || n3 == 0 && this.LeftKey) {
                this.mapObject[67][119] = 4;
                if (this.charaX != 0) {
                    n2 = this.charaX / 5 + this.mapX * 13 - 1;
                    n = this.charaY / 5 + this.mapY * 13;
                    this.mdata = this.map[n][n2];
                    if (this.directCheck(graphics, n2, n)) {
                        this.charaX -= this.movePlus;
                        this.yanime = true;
                    }
                }
            } else if (n3 == 6 || n3 == 0 && this.RightKey) {
                this.mapObject[67][119] = 6;
                if (this.charaX != 60) {
                    n2 = this.charaX / 5 + this.mapX * 13 + 1;
                    n = this.charaY / 5 + this.mapY * 13;
                    this.mdata = this.map[n][n2];
                    if (this.directCheck(graphics, n2, n)) {
                        this.charaX += this.movePlus;
                        this.yanime = true;
                    }
                }
            }
        } else if (this.mapObject[67][119] == '\b') {
            this.charaY -= this.movePlus;
        } else if (this.mapObject[67][119] == '\u0002') {
            this.charaY += this.movePlus;
        } else if (this.mapObject[67][119] == '\u0004') {
            this.charaX -= this.movePlus;
        } else if (this.mapObject[67][119] == '\u0006') {
            this.charaX += this.movePlus;
        }
    }

    public void drawJapanese(Graphics graphics, String string, int n, int n2, int n3) {
        char[] cArray = new char[1];
        Font font = new Font(this.FontName, 1, this.mapObject[70][127]);
        if (this.mapObject[69][127] == '\u0001') {
            font = new Font(this.FontName, 0, this.mapObject[70][127]);
        } else if (this.mapObject[69][127] == '\u0003') {
            font = new Font(this.FontName, 2, this.mapObject[70][127]);
        }
        FontMetrics fontMetrics = this.getFontMetrics(font);
        graphics.setFont(font);
        graphics.setColor(Color.black);
        int n4 = 0;
        int n5 = n;
        int n6 = n2;
        int n7 = 0;
        while (n7 < string.length()) {
            if (string.charAt(n7) == '\n') {
                n5 = n;
                n6 += 22;
                n4 = 0;
            } else {
                if (n4 >= n3) {
                    n5 = n;
                    n6 += 22;
                    n4 = 0;
                }
                cArray[0] = string.charAt(n7);
                graphics.drawString(new String(cArray), n5 + 2 + this.xp, n6 + 16 + this.yp);
                int n8 = fontMetrics.stringWidth(new String(cArray));
                n5 += n8;
                n4 += n8;
            }
            ++n7;
        }
    }

    public void drawJapaneseFrame(Graphics graphics, String string, int n, int n2) {
        int n3 = 420;
        int n4 = 174;
        if (this.mapObject[73][127] == '\u0000') {
            n2 = this.charaY / 5 % 13 <= 6 ? (this.charaY / 5 % 13 + 2) * 40 : (this.charaY / 5 % 13 - 6) * 40 - 20;
        } else if (this.mapObject[73][127] == '\u0001') {
            n2 = 20;
            this.mapObject[73][127] = '\u0000';
        } else if (this.mapObject[73][127] == '\u0002') {
            n2 = 340;
            this.mapObject[73][127] = '\u0000';
        }
        switch (this.itemFlag) {
            case 0: {
                if (this.strMessage[this.mapObject[76][121]][this.strNumber].equals("")) break;
                this.yesnoX = n + n3 - 80 - 20;
                this.yesnoY = n2 + n4 - 40 - 20;
                graphics.setColor(Color.black);
                graphics.fillRoundRect(n + this.xp, n2 + this.yp, n3, n4, 10, 10);
                graphics.setColor(Color.white);
                graphics.fillRoundRect(n + 1 + this.xp, n2 + 1 + this.yp, n3 - 2, n4 - 2, 10, 10);
                this.drawJapanese(graphics, string, n + 10, n2 + 10, n3 - 40);
                break;
            }
            case 2: {
                this.yesnoX = n + n3 - 80 - 20;
                this.yesnoY = n2 + n4 - 40 - 20;
                graphics.setColor(Color.black);
                graphics.fillRoundRect(n + this.xp, n2 + this.yp, n3, n4, 10, 10);
                graphics.setColor(Color.white);
                graphics.fillRoundRect(n + 1 + this.xp, n2 + 1 + this.yp, n3 - 2, n4 - 2, 10, 10);
                if (this.chieOrb[this.chieNum] == 0) {
                    string = this.strMessage[this.mapObject[76][121]][97];
                    this.itemFlag = 0;
                    this.itemKeyFlag = false;
                    this.configFlag = true;
                } else {
                    string = this.strMessage[this.mapObject[76][121]][282] + String.valueOf(this.chieOrb[this.chieNum]) + "\uff1a" + this.strMessage[this.mapObject[76][121]][this.chieOrb[this.chieNum] + 54];
                }
                this.drawJapanese(graphics, string, n + 10, n2 + 10, n3 - 40);
                break;
            }
            case 1: {
                int n5;
                int n6;
                int[] nArray = new int[20];
                this.yusyaFlag = true;
                Image image = this.getImage(this.getDocumentBase(), "image/yusya.gif");
                Font font = new Font(this.FontName, 1, this.mapObject[70][127] + 6);
                if (this.mapObject[69][127] == '\u0001') {
                    font = new Font(this.FontName, 0, this.mapObject[70][127] + 6);
                } else if (this.mapObject[69][127] == '\u0003') {
                    font = new Font(this.FontName, 2, this.mapObject[70][127] + 6);
                }
                this.gBuffyusya.setFont(font);
                this.gBuffyusya.setColor(Color.white);
                this.gBuffyusya.drawImage(image, 0, 0, this);
                this.drawJapanese(this.gBuffyusya, this.strMessage[this.mapObject[76][121]][184], 24 - this.xp, 25 - this.yp, 450);
                int n7 = 0;
                int n8 = 0;
                int n9 = 0;
                while (n9 < 13) {
                    n6 = 0;
                    while (n6 < 13) {
                        if (this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13] != '\u0000' && this.objectAttribute[this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13]][3] == 6 && this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13] != '2' && this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13] != '3' && this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13] != '4' && this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13] != '<' && this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13] != '=' && this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13] != '>' && this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13] != 'F' && this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13] != 'H') {
                            if (n7 == 0) {
                                nArray[n7] = this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13];
                                ++n7;
                            } else {
                                n8 = 0;
                                n5 = 0;
                                while (n5 < n7) {
                                    if (nArray[n5] == this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13]) {
                                        n8 = 1;
                                    }
                                    ++n5;
                                }
                                if (n8 == 0) {
                                    nArray[n7] = this.mapObject[n9 + this.mapY * 13][n6 + this.mapX * 13];
                                    ++n7;
                                }
                            }
                        }
                        ++n6;
                    }
                    ++n9;
                }
                n5 = 0;
                while (n5 < n7) {
                    n8 = 0;
                    while (n8 < n7) {
                        if (this.objectAttribute[nArray[n8]][13] < this.objectAttribute[nArray[n8 + 1]][13]) {
                            n6 = nArray[n8];
                            nArray[n8] = nArray[n8 + 1];
                            nArray[n8 + 1] = n6;
                        }
                        ++n8;
                    }
                    ++n5;
                }
                if (n7 >= 7) {
                    n7 = 7;
                }
                n6 = 0;
                while (n6 < n7) {
                    int n10;
                    FontMetrics fontMetrics;
                    font = new Font(this.FontName, 1, this.mapObject[70][127] + 2);
                    if (this.mapObject[69][127] == '\u0001') {
                        font = new Font(this.FontName, 0, this.mapObject[70][127] + 2);
                    } else if (this.mapObject[69][127] == '\u0003') {
                        font = new Font(this.FontName, 2, this.mapObject[70][127] + 2);
                    }
                    this.gBuffyusya.setFont(font);
                    this.gBuffyusya.setColor(Color.white);
                    this.gBuffyusya.drawImage(this.imgCrop[this.mapAttribute[1][1]], 22, n6 * 55 + 112, 50, 50, this);
                    this.gBuffyusya.drawImage(this.imgCrop[this.objectAttribute[nArray[n6]][1]], 22, n6 * 55 + 112, 50, 50, this);
                    this.gBuffyusya.drawString(this.strMessage[this.mapObject[76][121]][this.objectAttribute[nArray[n6]][5]], 80, n6 * 55 + 132);
                    if (this.mapObject[67][118] <= this.objectAttribute[nArray[n6]][12]) {
                        this.gBuffyusya.setColor(Color.red);
                        this.gBuffyusya.drawString(this.strMessage[this.mapObject[76][121]][189], 233, n6 * 55 + 132);
                    } else {
                        this.gBuffyusya.drawString(this.strMessage[this.mapObject[76][121]][188], 233, n6 * 55 + 132);
                        fontMetrics = this.getFontMetrics(font);
                        int n11 = this.objectAttribute[nArray[n6]][10] % (this.mapObject[67][118] - this.objectAttribute[nArray[n6]][12]);
                        if (n11 != 0) {
                            n11 = 1;
                        }
                        int n12 = (this.objectAttribute[nArray[n6]][11] - this.mapObject[68][118]) * (this.objectAttribute[nArray[n6]][10] / (this.mapObject[67][118] - this.objectAttribute[nArray[n6]][12]) - 1 + n11);
                        if (this.mapObject[68][118] - this.objectAttribute[nArray[n6]][11] >= 0) {
                            n12 = 0;
                        }
                        this.gBuffyusya.setColor(Color.red);
                        n10 = fontMetrics.stringWidth(String.valueOf(n12));
                        this.gBuffyusya.drawString(String.valueOf(n12), 490 - n10, n6 * 55 + 132);
                    }
                    this.gBuffyusya.setColor(Color.white);
                    fontMetrics = this.getFontMetrics(font);
                    n10 = fontMetrics.stringWidth(String.valueOf(this.objectAttribute[nArray[n6]][10]));
                    this.gBuffyusya.drawImage(this.imgCrop[21], 80, n6 * 55 + 134, this);
                    this.gBuffyusya.drawString(String.valueOf(this.objectAttribute[nArray[n6]][10]), 175 - n10, n6 * 55 + 160);
                    n10 = fontMetrics.stringWidth(String.valueOf(this.objectAttribute[nArray[n6]][11]));
                    this.gBuffyusya.drawImage(this.imgCrop[22], 185, n6 * 55 + 134, this);
                    this.gBuffyusya.drawString(String.valueOf(this.objectAttribute[nArray[n6]][11]), 281 - n10, n6 * 55 + 160);
                    n10 = fontMetrics.stringWidth(String.valueOf(this.objectAttribute[nArray[n6]][12]));
                    this.gBuffyusya.drawImage(this.imgCrop[23], 290, n6 * 55 + 134, this);
                    this.gBuffyusya.drawString(String.valueOf(this.objectAttribute[nArray[n6]][12]), 387 - n10, n6 * 55 + 160);
                    n10 = fontMetrics.stringWidth(String.valueOf(this.objectAttribute[nArray[n6]][13]));
                    this.gBuffyusya.drawImage(this.imgCrop[24], 395, n6 * 55 + 134, this);
                    this.gBuffyusya.drawString(String.valueOf(this.objectAttribute[nArray[n6]][13]), 490 - n10, n6 * 55 + 160);
                    ++n6;
                }
                graphics.drawImage(this.imgBuffyusya, this.xp, this.yp, this);
                this.itemFlag = 0;
            }
        }
    }

    public void twait(int n) {
        try {
        }
        catch (InterruptedException interruptedException) {
            System.out.println("Thread Exception !!!");
        }
    }

    /*
     * Opcode count of 27851 triggered aggressive code reduction.  Override with --aggressivesizethreshold.
     */
    public void loadMapData() {
        int n;
        int n2;
        int n3 = 0;
        while (n3 < 78) {
            n2 = 0;
            while (n2 < 130) {
                this.mapObject[n3][n2] = '\u0000';
                ++n2;
            }
            ++n3;
        }
        n3 = 0;
        while (n3 < 78) {
            n2 = 0;
            while (n2 < 130) {
                this.map[n3][n2] = '\u0001';
                if (n2 % 13 == 0 && n3 % 13 == 0) {
                    this.map[n3][n2] = 30;
                } else if (n2 % 13 == 12 && n3 % 13 == 0) {
                    this.map[n3][n2] = 32;
                } else if (n3 % 13 == 0) {
                    this.map[n3][n2] = 31;
                } else if (n2 % 13 == 0 && n3 % 13 == 12) {
                    this.map[n3][n2] = 35;
                } else if (n2 % 13 == 12 && n3 % 13 == 12) {
                    this.map[n3][n2] = 37;
                } else if (n3 % 13 == 12) {
                    this.map[n3][n2] = 36;
                } else if (n2 % 13 == 0) {
                    this.map[n3][n2] = 33;
                } else if (n2 % 13 == 12) {
                    this.map[n3][n2] = 34;
                }
                ++n2;
            }
            ++n3;
        }
        this.map[1][1] = 4;
        this.map[2][1] = 3;
        this.map[2][2] = 3;
        this.map[2][3] = 3;
        this.map[2][4] = 3;
        this.map[2][5] = 3;
        this.map[2][6] = 3;
        this.map[2][7] = 3;
        this.map[2][8] = 3;
        this.map[2][9] = 3;
        this.map[2][10] = 3;
        this.map[3][6] = 3;
        this.map[3][10] = 3;
        this.map[4][4] = 3;
        this.map[4][6] = 3;
        this.map[4][10] = 3;
        this.map[5][1] = 3;
        this.map[5][3] = 3;
        this.map[5][4] = 3;
        this.map[5][6] = 3;
        this.map[5][7] = 3;
        this.map[5][8] = 3;
        this.map[5][10] = 3;
        this.map[6][4] = 3;
        this.map[6][10] = 3;
        this.map[7][4] = 3;
        this.map[7][6] = 3;
        this.map[7][7] = 3;
        this.map[7][8] = 3;
        this.map[7][9] = 3;
        this.map[7][10] = 3;
        this.map[8][1] = 3;
        this.map[8][3] = 3;
        this.map[8][4] = 3;
        this.map[9][4] = 3;
        this.map[9][5] = 3;
        this.map[9][7] = 3;
        this.map[9][8] = 3;
        this.map[9][9] = 3;
        this.map[9][11] = 3;
        this.map[10][4] = 3;
        this.map[10][8] = 3;
        this.map[11][4] = 3;
        this.map[11][8] = 3;
        this.map[1][14] = 5;
        this.map[2][16] = 3;
        this.map[2][17] = 3;
        this.map[2][23] = 3;
        this.map[2][24] = 3;
        this.map[3][15] = 3;
        this.map[3][16] = 3;
        this.map[3][17] = 3;
        this.map[3][18] = 3;
        this.map[3][19] = 3;
        this.map[3][21] = 3;
        this.map[3][22] = 3;
        this.map[3][23] = 3;
        this.map[3][24] = 3;
        this.map[4][15] = 3;
        this.map[4][18] = 3;
        this.map[4][22] = 3;
        this.map[5][15] = 3;
        this.map[6][15] = 3;
        this.map[6][16] = 3;
        this.map[6][17] = 3;
        this.map[6][18] = 3;
        this.map[6][22] = 3;
        this.map[6][23] = 3;
        this.map[6][24] = 3;
        this.map[7][15] = 3;
        this.map[7][18] = 3;
        this.map[7][22] = 3;
        this.map[8][15] = 3;
        this.map[9][15] = 3;
        this.map[9][16] = 3;
        this.map[9][17] = 3;
        this.map[9][18] = 3;
        this.map[9][22] = 3;
        this.map[9][23] = 3;
        this.map[9][24] = 3;
        this.map[10][15] = 3;
        this.map[10][18] = 3;
        this.map[10][22] = 3;
        this.map[11][14] = 6;
        this.map[11][15] = 3;
        this.map[1][29] = 3;
        this.map[1][33] = 3;
        this.map[1][35] = 3;
        this.map[2][29] = 3;
        this.map[2][33] = 3;
        this.map[3][29] = 3;
        this.map[3][33] = 3;
        this.map[3][35] = 3;
        this.map[3][36] = 3;
        this.map[3][37] = 3;
        this.map[4][28] = 3;
        this.map[4][29] = 3;
        this.map[4][30] = 3;
        this.map[4][32] = 3;
        this.map[4][33] = 3;
        this.map[4][35] = 3;
        this.map[6][28] = 3;
        this.map[6][29] = 3;
        this.map[6][33] = 3;
        this.map[6][35] = 3;
        this.map[6][36] = 3;
        this.map[6][37] = 3;
        this.map[7][29] = 3;
        this.map[7][30] = 3;
        this.map[7][32] = 3;
        this.map[7][33] = 3;
        this.map[7][35] = 3;
        this.map[8][29] = 3;
        this.map[8][33] = 3;
        this.map[9][29] = 3;
        this.map[9][33] = 3;
        this.map[9][35] = 3;
        this.map[9][36] = 3;
        this.map[9][37] = 3;
        this.map[10][27] = 3;
        this.map[10][28] = 3;
        this.map[10][29] = 3;
        this.map[10][30] = 3;
        this.map[10][32] = 3;
        this.map[10][33] = 3;
        this.map[10][35] = 3;
        this.map[11][27] = 7;
        this.map[11][33] = 3;
        this.map[11][37] = 8;
        this.map[1][43] = 3;
        this.map[1][47] = 3;
        this.map[2][43] = 3;
        this.map[2][47] = 3;
        this.map[3][43] = 3;
        this.map[3][47] = 3;
        this.map[4][40] = 3;
        this.map[4][42] = 3;
        this.map[4][43] = 3;
        this.map[4][44] = 3;
        this.map[4][46] = 3;
        this.map[4][47] = 3;
        this.map[4][48] = 3;
        this.map[4][50] = 3;
        this.map[6][43] = 3;
        this.map[6][44] = 3;
        this.map[6][45] = 3;
        this.map[6][46] = 3;
        this.map[6][47] = 3;
        this.map[6][48] = 3;
        this.map[6][49] = 3;
        this.map[6][50] = 3;
        this.map[8][41] = 3;
        this.map[8][42] = 3;
        this.map[8][44] = 3;
        this.map[8][45] = 3;
        this.map[8][46] = 3;
        this.map[8][48] = 3;
        this.map[8][49] = 3;
        this.map[9][41] = 3;
        this.map[9][45] = 3;
        this.map[9][49] = 3;
        this.map[10][41] = 3;
        this.map[10][45] = 3;
        this.map[10][49] = 3;
        this.map[11][40] = 10;
        this.map[11][41] = 3;
        this.map[11][45] = 3;
        this.map[11][49] = 3;
        this.map[11][50] = 9;
        this.map[1][53] = 12;
        this.map[1][54] = 3;
        this.map[1][59] = 3;
        this.map[2][54] = 3;
        this.map[2][57] = 3;
        this.map[2][59] = 3;
        this.map[2][62] = 3;
        this.map[3][57] = 3;
        this.map[3][59] = 3;
        this.map[3][62] = 3;
        this.map[4][53] = 3;
        this.map[4][54] = 3;
        this.map[4][55] = 3;
        this.map[4][57] = 3;
        this.map[4][59] = 3;
        this.map[4][62] = 3;
        this.map[5][57] = 3;
        this.map[5][59] = 3;
        this.map[5][60] = 3;
        this.map[5][61] = 3;
        this.map[5][62] = 3;
        this.map[6][57] = 3;
        this.map[7][53] = 3;
        this.map[7][55] = 3;
        this.map[7][56] = 3;
        this.map[7][57] = 3;
        this.map[7][59] = 3;
        this.map[7][60] = 3;
        this.map[7][61] = 3;
        this.map[7][62] = 3;
        this.map[8][57] = 3;
        this.map[8][59] = 3;
        this.map[9][57] = 3;
        this.map[9][59] = 3;
        this.map[9][61] = 3;
        this.map[9][62] = 3;
        this.map[9][63] = 3;
        this.map[10][53] = 3;
        this.map[10][54] = 3;
        this.map[10][55] = 3;
        this.map[10][56] = 3;
        this.map[10][57] = 3;
        this.map[10][59] = 3;
        this.map[10][61] = 3;
        this.map[11][53] = 11;
        this.map[11][59] = 3;
        this.map[1][66] = 13;
        this.map[1][67] = 3;
        this.map[1][70] = 3;
        this.map[2][67] = 3;
        this.map[2][70] = 3;
        this.map[2][72] = 3;
        this.map[2][73] = 3;
        this.map[2][74] = 3;
        this.map[2][75] = 3;
        this.map[3][67] = 3;
        this.map[3][68] = 3;
        this.map[3][70] = 3;
        this.map[3][72] = 3;
        this.map[4][72] = 3;
        this.map[5][67] = 3;
        this.map[5][68] = 3;
        this.map[5][69] = 3;
        this.map[5][70] = 3;
        this.map[5][72] = 3;
        this.map[5][73] = 3;
        this.map[5][74] = 3;
        this.map[5][75] = 3;
        this.map[5][76] = 3;
        this.map[7][66] = 3;
        this.map[7][67] = 3;
        this.map[7][68] = 3;
        this.map[7][69] = 3;
        this.map[7][70] = 3;
        this.map[7][72] = 3;
        this.map[7][73] = 3;
        this.map[7][74] = 3;
        this.map[7][75] = 3;
        this.map[8][70] = 3;
        this.map[9][70] = 3;
        this.map[9][72] = 3;
        this.map[9][73] = 3;
        this.map[9][75] = 3;
        this.map[10][67] = 3;
        this.map[10][68] = 3;
        this.map[10][69] = 3;
        this.map[10][70] = 3;
        this.map[10][72] = 3;
        this.map[10][75] = 3;
        this.map[11][72] = 3;
        this.map[11][75] = 3;
        this.map[11][76] = 14;
        this.map[1][79] = 16;
        this.map[1][80] = 3;
        this.map[1][82] = 3;
        this.map[1][86] = 3;
        this.map[1][88] = 3;
        this.map[2][80] = 3;
        this.map[2][82] = 3;
        this.map[2][86] = 3;
        this.map[2][88] = 3;
        this.map[3][80] = 3;
        this.map[3][82] = 3;
        this.map[3][84] = 3;
        this.map[3][86] = 3;
        this.map[3][88] = 3;
        this.map[4][80] = 3;
        this.map[4][82] = 3;
        this.map[4][84] = 3;
        this.map[4][86] = 3;
        this.map[4][88] = 3;
        this.map[5][80] = 3;
        this.map[5][82] = 3;
        this.map[5][84] = 3;
        this.map[5][86] = 3;
        this.map[5][88] = 3;
        this.map[7][80] = 3;
        this.map[7][82] = 3;
        this.map[7][84] = 3;
        this.map[7][86] = 3;
        this.map[7][88] = 3;
        this.map[8][80] = 3;
        this.map[8][82] = 3;
        this.map[8][84] = 3;
        this.map[8][86] = 3;
        this.map[8][88] = 3;
        this.map[9][80] = 3;
        this.map[9][82] = 3;
        this.map[9][84] = 3;
        this.map[9][86] = 3;
        this.map[9][88] = 3;
        this.map[10][80] = 3;
        this.map[10][82] = 3;
        this.map[10][84] = 3;
        this.map[10][86] = 3;
        this.map[10][88] = 3;
        this.map[11][82] = 3;
        this.map[11][84] = 3;
        this.map[11][86] = 3;
        this.map[11][88] = 3;
        this.map[11][89] = 15;
        this.map[1][92] = 17;
        this.map[1][97] = 18;
        this.map[1][99] = 3;
        this.map[2][94] = 3;
        this.map[2][95] = 3;
        this.map[2][99] = 3;
        this.map[3][93] = 3;
        this.map[3][94] = 3;
        this.map[3][95] = 3;
        this.map[3][96] = 3;
        this.map[3][98] = 3;
        this.map[3][99] = 3;
        this.map[4][93] = 3;
        this.map[4][99] = 3;
        this.map[4][100] = 3;
        this.map[4][102] = 3;
        this.map[5][93] = 3;
        this.map[5][94] = 3;
        this.map[5][95] = 3;
        this.map[5][96] = 3;
        this.map[5][97] = 3;
        this.map[5][99] = 3;
        this.map[6][97] = 3;
        this.map[6][99] = 3;
        this.map[7][92] = 3;
        this.map[7][93] = 3;
        this.map[7][94] = 3;
        this.map[7][95] = 3;
        this.map[7][97] = 3;
        this.map[7][99] = 3;
        this.map[7][100] = 3;
        this.map[7][102] = 3;
        this.map[9][93] = 3;
        this.map[9][94] = 3;
        this.map[9][95] = 3;
        this.map[9][96] = 3;
        this.map[9][97] = 3;
        this.map[9][98] = 3;
        this.map[9][99] = 3;
        this.map[9][100] = 3;
        this.map[9][101] = 3;
        this.map[10][94] = 3;
        this.map[10][97] = 3;
        this.map[10][100] = 3;
        this.map[11][97] = 3;
        this.map[1][110] = 19;
        this.map[2][108] = 3;
        this.map[2][112] = 3;
        this.map[3][106] = 3;
        this.map[3][107] = 3;
        this.map[3][108] = 3;
        this.map[3][109] = 3;
        this.map[3][111] = 3;
        this.map[3][112] = 3;
        this.map[3][113] = 3;
        this.map[3][114] = 3;
        this.map[4][108] = 3;
        this.map[5][112] = 3;
        this.map[5][113] = 3;
        this.map[5][115] = 3;
        this.map[6][105] = 3;
        this.map[6][106] = 3;
        this.map[6][107] = 3;
        this.map[6][108] = 3;
        this.map[6][109] = 3;
        this.map[6][110] = 3;
        this.map[6][112] = 3;
        this.map[7][110] = 3;
        this.map[7][112] = 3;
        this.map[7][114] = 3;
        this.map[8][107] = 3;
        this.map[8][110] = 3;
        this.map[8][112] = 3;
        this.map[8][113] = 3;
        this.map[8][114] = 3;
        this.map[9][106] = 3;
        this.map[9][107] = 3;
        this.map[9][108] = 3;
        this.map[9][110] = 3;
        this.map[9][112] = 3;
        this.map[10][107] = 3;
        this.map[10][110] = 3;
        this.map[10][112] = 3;
        this.map[11][105] = 20;
        this.map[2][118] = 3;
        this.map[2][119] = 3;
        this.map[2][120] = 3;
        this.map[2][121] = 3;
        this.map[2][125] = 3;
        this.map[2][126] = 3;
        this.map[2][127] = 3;
        this.map[2][128] = 3;
        this.map[3][121] = 3;
        this.map[3][122] = 3;
        this.map[3][124] = 3;
        this.map[3][125] = 3;
        this.map[5][118] = 3;
        this.map[5][119] = 3;
        this.map[5][120] = 3;
        this.map[5][121] = 3;
        this.map[5][125] = 3;
        this.map[5][126] = 3;
        this.map[5][127] = 3;
        this.map[5][128] = 3;
        this.map[6][121] = 3;
        this.map[6][122] = 3;
        this.map[6][124] = 3;
        this.map[6][125] = 3;
        this.map[7][121] = 3;
        this.map[7][122] = 3;
        this.map[7][124] = 3;
        this.map[7][125] = 3;
        this.map[8][121] = 3;
        this.map[8][122] = 3;
        this.map[8][124] = 3;
        this.map[8][125] = 3;
        this.map[9][119] = 3;
        this.map[9][121] = 3;
        this.map[9][122] = 3;
        this.map[9][124] = 3;
        this.map[9][125] = 3;
        this.map[9][127] = 3;
        this.map[10][119] = 3;
        this.map[10][121] = 3;
        this.map[10][125] = 3;
        this.map[10][127] = 3;
        this.map[11][118] = 21;
        this.map[11][119] = 3;
        this.map[11][127] = 3;
        this.map[14][4] = 3;
        this.map[14][9] = 3;
        this.map[15][4] = 3;
        this.map[15][7] = 3;
        this.map[15][9] = 3;
        this.map[16][4] = 3;
        this.map[16][6] = 3;
        this.map[16][7] = 3;
        this.map[17][1] = 3;
        this.map[17][3] = 3;
        this.map[17][4] = 3;
        this.map[17][7] = 3;
        this.map[17][8] = 3;
        this.map[17][9] = 3;
        this.map[17][10] = 3;
        this.map[18][4] = 3;
        this.map[18][10] = 3;
        this.map[19][4] = 3;
        this.map[19][5] = 3;
        this.map[19][6] = 3;
        this.map[19][7] = 3;
        this.map[19][10] = 3;
        this.map[20][10] = 3;
        this.map[21][1] = 3;
        this.map[21][3] = 3;
        this.map[21][4] = 3;
        this.map[21][5] = 3;
        this.map[21][6] = 3;
        this.map[21][7] = 3;
        this.map[21][8] = 3;
        this.map[21][9] = 3;
        this.map[21][10] = 3;
        this.map[23][5] = 3;
        this.map[23][7] = 3;
        this.map[23][8] = 3;
        this.map[23][10] = 3;
        this.map[24][5] = 3;
        this.map[24][7] = 3;
        this.map[24][10] = 3;
        this.map[24][6] = 23;
        this.map[24][11] = 24;
        this.map[14][17] = 3;
        this.map[14][21] = 3;
        this.map[15][14] = 3;
        this.map[15][15] = 3;
        this.map[15][17] = 3;
        this.map[15][19] = 3;
        this.map[15][21] = 3;
        this.map[15][23] = 3;
        this.map[15][24] = 3;
        this.map[16][17] = 3;
        this.map[16][21] = 3;
        this.map[17][15] = 3;
        this.map[17][16] = 3;
        this.map[17][17] = 3;
        this.map[17][18] = 3;
        this.map[17][20] = 3;
        this.map[17][21] = 3;
        this.map[17][22] = 3;
        this.map[17][23] = 3;
        this.map[18][21] = 3;
        this.map[19][14] = 3;
        this.map[19][15] = 3;
        this.map[19][16] = 3;
        this.map[19][17] = 3;
        this.map[20][17] = 3;
        this.map[20][21] = 3;
        this.map[21][17] = 3;
        this.map[21][18] = 3;
        this.map[21][19] = 3;
        this.map[21][20] = 3;
        this.map[21][21] = 3;
        this.map[21][23] = 3;
        this.map[22][17] = 3;
        this.map[22][21] = 3;
        this.map[23][14] = 3;
        this.map[23][15] = 3;
        this.map[23][17] = 3;
        this.map[23][21] = 3;
        this.map[23][22] = 3;
        this.map[23][24] = 3;
        this.map[24][14] = 26;
        this.map[24][24] = 25;
        this.map[16][31] = 3;
        this.map[16][32] = 3;
        this.map[16][33] = 3;
        this.map[17][30] = 3;
        this.map[17][31] = 3;
        this.map[17][32] = 3;
        this.map[17][33] = 3;
        this.map[17][34] = 3;
        this.map[18][30] = 3;
        this.map[18][31] = 3;
        this.map[18][33] = 3;
        this.map[18][34] = 3;
        this.map[19][30] = 3;
        this.map[19][31] = 3;
        this.map[19][33] = 3;
        this.map[19][34] = 3;
        this.map[20][31] = 3;
        this.map[20][33] = 3;
        this.map[23][27] = 3;
        this.map[23][28] = 3;
        this.map[23][29] = 3;
        this.map[23][30] = 3;
        this.map[23][31] = 3;
        this.map[23][33] = 3;
        this.map[23][34] = 3;
        this.map[23][35] = 3;
        this.map[23][36] = 3;
        this.map[23][37] = 3;
        this.map[24][27] = 27;
        this.map[24][37] = 28;
        this.map[14][43] = 3;
        this.map[14][47] = 3;
        this.map[15][43] = 3;
        this.map[15][45] = 3;
        this.map[15][47] = 3;
        this.map[16][40] = 3;
        this.map[16][43] = 3;
        this.map[16][45] = 3;
        this.map[16][47] = 3;
        this.map[16][48] = 3;
        this.map[16][50] = 3;
        this.map[17][40] = 3;
        this.map[17][42] = 3;
        this.map[17][43] = 3;
        this.map[17][45] = 3;
        this.map[17][47] = 3;
        this.map[19][43] = 3;
        this.map[19][44] = 3;
        this.map[19][46] = 3;
        this.map[19][47] = 3;
        this.map[20][41] = 3;
        this.map[20][43] = 3;
        this.map[20][47] = 3;
        this.map[20][48] = 3;
        this.map[20][49] = 3;
        this.map[21][41] = 3;
        this.map[22][41] = 3;
        this.map[22][43] = 3;
        this.map[22][44] = 3;
        this.map[22][46] = 3;
        this.map[22][47] = 3;
        this.map[22][49] = 3;
        this.map[22][50] = 3;
        this.map[23][41] = 3;
        this.map[23][43] = 3;
        this.map[23][47] = 3;
        this.map[24][41] = 3;
        this.map[24][47] = 3;
        this.map[24][45] = 38;
        this.map[24][50] = 29;
        this.map[14][60] = 3;
        this.map[15][56] = 3;
        this.map[15][60] = 3;
        this.map[16][56] = 3;
        this.map[16][57] = 3;
        this.map[16][59] = 3;
        this.map[16][60] = 3;
        this.map[16][61] = 3;
        this.map[16][62] = 3;
        this.map[17][54] = 3;
        this.map[17][55] = 3;
        this.map[17][56] = 3;
        this.map[17][60] = 3;
        this.map[18][54] = 3;
        this.map[18][56] = 3;
        this.map[18][60] = 3;
        this.map[19][54] = 3;
        this.map[19][56] = 3;
        this.map[19][60] = 3;
        this.map[19][62] = 3;
        this.map[20][54] = 3;
        this.map[20][56] = 3;
        this.map[20][60] = 3;
        this.map[20][62] = 3;
        this.map[21][54] = 3;
        this.map[21][56] = 3;
        this.map[21][60] = 3;
        this.map[21][62] = 3;
        this.map[22][56] = 3;
        this.map[22][57] = 3;
        this.map[22][59] = 3;
        this.map[22][60] = 3;
        this.map[22][62] = 3;
        this.map[22][63] = 3;
        this.map[23][54] = 3;
        this.map[23][56] = 3;
        this.map[23][60] = 3;
        this.map[24][56] = 3;
        this.map[14][58] = 40;
        this.map[24][58] = 39;
        this.map[14][69] = 3;
        this.map[14][73] = 3;
        this.map[16][69] = 3;
        this.map[16][73] = 3;
        this.map[17][66] = 3;
        this.map[17][67] = 3;
        this.map[17][68] = 3;
        this.map[17][69] = 3;
        this.map[17][70] = 3;
        this.map[17][72] = 3;
        this.map[17][73] = 3;
        this.map[17][74] = 3;
        this.map[17][76] = 3;
        this.map[18][69] = 3;
        this.map[18][73] = 3;
        this.map[19][73] = 3;
        this.map[20][69] = 3;
        this.map[20][73] = 3;
        this.map[21][66] = 3;
        this.map[21][67] = 2;
        this.map[21][68] = 3;
        this.map[21][69] = 3;
        this.map[21][70] = 3;
        this.map[21][72] = 3;
        this.map[21][73] = 3;
        this.map[21][74] = 3;
        this.map[21][76] = 3;
        this.map[22][69] = 3;
        this.map[22][73] = 3;
        this.map[23][75] = 3;
        this.map[23][76] = 3;
        this.map[24][69] = 3;
        this.map[24][73] = 3;
        this.map[14][71] = 41;
        this.map[24][71] = 42;
        this.map[14][82] = 3;
        this.map[14][86] = 3;
        this.map[15][82] = 3;
        this.map[15][86] = 3;
        this.map[16][82] = 3;
        this.map[16][84] = 3;
        this.map[16][86] = 3;
        this.map[17][79] = 3;
        this.map[17][81] = 3;
        this.map[17][82] = 3;
        this.map[17][84] = 3;
        this.map[17][86] = 3;
        this.map[17][87] = 3;
        this.map[17][89] = 3;
        this.map[18][82] = 3;
        this.map[18][84] = 3;
        this.map[18][86] = 3;
        this.map[19][82] = 3;
        this.map[19][84] = 3;
        this.map[19][86] = 3;
        this.map[20][79] = 3;
        this.map[20][81] = 3;
        this.map[20][82] = 3;
        this.map[20][84] = 3;
        this.map[20][86] = 3;
        this.map[20][87] = 3;
        this.map[20][89] = 3;
        this.map[21][82] = 3;
        this.map[21][86] = 3;
        this.map[22][82] = 3;
        this.map[22][83] = 3;
        this.map[22][85] = 3;
        this.map[22][86] = 3;
        this.map[23][79] = 3;
        this.map[23][81] = 3;
        this.map[23][82] = 3;
        this.map[23][86] = 3;
        this.map[23][87] = 3;
        this.map[23][89] = 3;
        this.map[14][84] = 44;
        this.map[24][84] = 43;
        this.map[15][95] = 3;
        this.map[15][99] = 3;
        this.map[16][93] = 3;
        this.map[16][94] = 3;
        this.map[16][95] = 3;
        this.map[16][96] = 3;
        this.map[16][97] = 2;
        this.map[16][98] = 3;
        this.map[16][99] = 3;
        this.map[18][95] = 3;
        this.map[18][99] = 3;
        this.map[19][92] = 3;
        this.map[19][93] = 3;
        this.map[19][94] = 3;
        this.map[19][95] = 3;
        this.map[19][96] = 3;
        this.map[19][98] = 3;
        this.map[19][99] = 3;
        this.map[19][100] = 3;
        this.map[19][101] = 3;
        this.map[19][102] = 3;
        this.map[21][93] = 3;
        this.map[21][94] = 3;
        this.map[21][96] = 3;
        this.map[21][97] = 3;
        this.map[21][98] = 3;
        this.map[21][100] = 3;
        this.map[21][101] = 3;
        this.map[22][94] = 3;
        this.map[22][97] = 3;
        this.map[22][100] = 3;
        this.map[23][94] = 3;
        this.map[23][97] = 3;
        this.map[23][100] = 3;
        this.map[24][94] = 3;
        this.map[24][97] = 3;
        this.map[24][100] = 3;
        this.map[14][92] = 46;
        this.map[14][97] = 45;
        this.map[14][107] = 3;
        this.map[14][113] = 3;
        this.map[15][107] = 3;
        this.map[15][110] = 3;
        this.map[15][113] = 3;
        this.map[16][106] = 3;
        this.map[16][107] = 3;
        this.map[16][109] = 3;
        this.map[16][111] = 3;
        this.map[16][113] = 3;
        this.map[16][115] = 3;
        this.map[17][107] = 3;
        this.map[17][113] = 3;
        this.map[18][107] = 3;
        this.map[18][110] = 3;
        this.map[18][113] = 3;
        this.map[19][106] = 3;
        this.map[19][107] = 3;
        this.map[19][113] = 3;
        this.map[20][107] = 3;
        this.map[20][108] = 3;
        this.map[20][109] = 3;
        this.map[20][111] = 3;
        this.map[20][112] = 3;
        this.map[20][113] = 3;
        this.map[20][114] = 3;
        this.map[22][106] = 3;
        this.map[22][107] = 3;
        this.map[22][108] = 3;
        this.map[22][109] = 3;
        this.map[22][111] = 3;
        this.map[22][112] = 3;
        this.map[23][106] = 3;
        this.map[23][112] = 3;
        this.map[23][113] = 3;
        this.map[23][114] = 3;
        this.map[24][108] = 3;
        this.map[14][105] = 47;
        this.map[24][110] = 48;
        this.map[15][118] = 3;
        this.map[15][119] = 3;
        this.map[15][120] = 3;
        this.map[15][121] = 3;
        this.map[15][125] = 3;
        this.map[15][126] = 3;
        this.map[15][127] = 3;
        this.map[15][128] = 3;
        this.map[16][118] = 3;
        this.map[16][119] = 3;
        this.map[16][120] = 3;
        this.map[16][121] = 3;
        this.map[16][122] = 3;
        this.map[16][124] = 3;
        this.map[16][125] = 3;
        this.map[16][126] = 3;
        this.map[16][127] = 3;
        this.map[16][128] = 3;
        this.map[17][120] = 3;
        this.map[17][126] = 3;
        this.map[18][120] = 3;
        this.map[18][126] = 3;
        this.map[19][118] = 3;
        this.map[19][120] = 3;
        this.map[19][126] = 3;
        this.map[19][128] = 3;
        this.map[20][120] = 3;
        this.map[20][126] = 3;
        this.map[21][120] = 3;
        this.map[21][126] = 3;
        this.map[22][119] = 3;
        this.map[22][120] = 3;
        this.map[22][121] = 3;
        this.map[22][122] = 3;
        this.map[22][124] = 3;
        this.map[22][125] = 3;
        this.map[22][126] = 3;
        this.map[22][127] = 3;
        this.map[23][121] = 3;
        this.map[23][125] = 3;
        this.map[24][123] = 49;
        this.map[29][3] = 3;
        this.map[29][4] = 3;
        this.map[29][8] = 3;
        this.map[29][9] = 3;
        this.map[30][3] = 3;
        this.map[30][4] = 3;
        this.map[30][8] = 3;
        this.map[30][9] = 3;
        this.map[34][3] = 3;
        this.map[34][4] = 3;
        this.map[34][8] = 3;
        this.map[34][9] = 3;
        this.map[35][3] = 3;
        this.map[35][4] = 3;
        this.map[35][8] = 3;
        this.map[35][9] = 3;
        this.map[27][6] = 51;
        this.map[37][6] = 52;
        this.map[27][14] = 3;
        this.map[27][15] = 3;
        this.map[27][16] = 3;
        this.map[27][17] = 3;
        this.map[27][18] = 3;
        this.map[27][19] = 3;
        this.map[27][20] = 3;
        this.map[27][21] = 3;
        this.map[27][22] = 3;
        this.map[27][23] = 3;
        this.map[27][24] = 3;
        this.map[28][14] = 3;
        this.map[28][15] = 3;
        this.map[28][16] = 3;
        this.map[28][17] = 3;
        this.map[28][18] = 3;
        this.map[28][19] = 3;
        this.map[28][20] = 3;
        this.map[28][21] = 3;
        this.map[28][22] = 3;
        this.map[28][23] = 3;
        this.map[28][24] = 3;
        this.map[29][14] = 3;
        this.map[29][15] = 3;
        this.map[29][16] = 3;
        this.map[29][17] = 3;
        this.map[29][18] = 3;
        this.map[29][19] = 3;
        this.map[29][20] = 3;
        this.map[29][21] = 3;
        this.map[29][22] = 3;
        this.map[29][23] = 3;
        this.map[29][24] = 3;
        this.map[30][14] = 3;
        this.map[30][15] = 3;
        this.map[30][16] = 3;
        this.map[30][17] = 3;
        this.map[30][18] = 3;
        this.map[30][19] = 3;
        this.map[30][20] = 3;
        this.map[30][21] = 3;
        this.map[30][22] = 3;
        this.map[30][23] = 3;
        this.map[30][24] = 3;
        this.map[31][14] = 3;
        this.map[31][15] = 3;
        this.map[31][16] = 3;
        this.map[31][17] = 3;
        this.map[31][21] = 3;
        this.map[31][22] = 3;
        this.map[31][23] = 3;
        this.map[31][24] = 3;
        this.map[32][14] = 3;
        this.map[32][15] = 3;
        this.map[32][16] = 3;
        this.map[32][17] = 3;
        this.map[32][21] = 3;
        this.map[32][22] = 3;
        this.map[32][23] = 3;
        this.map[32][24] = 3;
        this.map[33][14] = 3;
        this.map[33][15] = 3;
        this.map[33][16] = 3;
        this.map[33][17] = 3;
        this.map[33][21] = 3;
        this.map[33][22] = 3;
        this.map[33][23] = 3;
        this.map[33][24] = 3;
        this.map[34][14] = 3;
        this.map[34][15] = 3;
        this.map[34][16] = 3;
        this.map[34][17] = 3;
        this.map[34][18] = 3;
        this.map[34][20] = 3;
        this.map[34][21] = 3;
        this.map[34][22] = 3;
        this.map[34][23] = 3;
        this.map[34][24] = 3;
        this.map[35][14] = 3;
        this.map[35][15] = 3;
        this.map[35][16] = 3;
        this.map[35][17] = 3;
        this.map[35][18] = 3;
        this.map[35][20] = 3;
        this.map[35][21] = 3;
        this.map[35][22] = 3;
        this.map[35][23] = 3;
        this.map[35][24] = 3;
        this.map[36][14] = 3;
        this.map[36][15] = 3;
        this.map[36][16] = 3;
        this.map[36][17] = 3;
        this.map[36][21] = 3;
        this.map[36][22] = 3;
        this.map[36][23] = 3;
        this.map[36][24] = 3;
        this.map[37][14] = 3;
        this.map[37][15] = 3;
        this.map[37][16] = 3;
        this.map[37][17] = 3;
        this.map[37][21] = 3;
        this.map[37][22] = 3;
        this.map[37][23] = 3;
        this.map[37][24] = 3;
        this.map[32][19] = 54;
        this.map[37][19] = 53;
        this.map[27][27] = 55;
        this.map[27][37] = 56;
        this.map[28][43] = 3;
        this.map[28][44] = 3;
        this.map[28][45] = 3;
        this.map[28][46] = 3;
        this.map[28][47] = 3;
        this.map[29][42] = 3;
        this.map[29][43] = 3;
        this.map[29][44] = 3;
        this.map[29][45] = 3;
        this.map[29][46] = 3;
        this.map[29][47] = 3;
        this.map[29][48] = 3;
        this.map[30][41] = 3;
        this.map[30][42] = 3;
        this.map[30][43] = 3;
        this.map[30][44] = 3;
        this.map[30][45] = 3;
        this.map[30][46] = 3;
        this.map[30][47] = 3;
        this.map[30][48] = 3;
        this.map[30][49] = 3;
        this.map[31][41] = 3;
        this.map[31][42] = 3;
        this.map[31][43] = 3;
        this.map[31][47] = 3;
        this.map[31][48] = 3;
        this.map[31][49] = 3;
        this.map[32][41] = 3;
        this.map[32][42] = 3;
        this.map[32][43] = 3;
        this.map[32][47] = 3;
        this.map[32][48] = 3;
        this.map[32][49] = 3;
        this.map[33][41] = 3;
        this.map[33][42] = 3;
        this.map[33][43] = 3;
        this.map[33][47] = 3;
        this.map[33][48] = 3;
        this.map[33][49] = 3;
        this.map[34][41] = 3;
        this.map[34][42] = 3;
        this.map[34][43] = 3;
        this.map[34][44] = 3;
        this.map[34][46] = 3;
        this.map[34][47] = 3;
        this.map[34][48] = 3;
        this.map[34][49] = 3;
        this.map[35][42] = 3;
        this.map[35][43] = 3;
        this.map[35][44] = 3;
        this.map[35][46] = 3;
        this.map[35][47] = 3;
        this.map[35][48] = 3;
        this.map[36][43] = 3;
        this.map[36][44] = 3;
        this.map[36][46] = 3;
        this.map[36][47] = 3;
        this.map[36][41] = 58;
        this.map[37][40] = 57;
        this.map[28][56] = 3;
        this.map[28][57] = 3;
        this.map[28][58] = 3;
        this.map[28][59] = 3;
        this.map[28][60] = 3;
        this.map[29][55] = 3;
        this.map[29][56] = 3;
        this.map[29][60] = 3;
        this.map[29][61] = 3;
        this.map[30][54] = 3;
        this.map[30][55] = 3;
        this.map[30][61] = 3;
        this.map[30][62] = 3;
        this.map[31][54] = 3;
        this.map[31][57] = 3;
        this.map[31][59] = 3;
        this.map[31][62] = 3;
        this.map[32][54] = 3;
        this.map[32][62] = 3;
        this.map[33][54] = 3;
        this.map[33][57] = 3;
        this.map[33][59] = 3;
        this.map[33][62] = 3;
        this.map[34][54] = 3;
        this.map[34][55] = 3;
        this.map[34][61] = 3;
        this.map[34][62] = 3;
        this.map[35][55] = 3;
        this.map[35][56] = 3;
        this.map[35][60] = 3;
        this.map[35][61] = 3;
        this.map[36][56] = 3;
        this.map[36][57] = 3;
        this.map[36][59] = 3;
        this.map[36][60] = 3;
        this.map[36][54] = 59;
        this.map[37][53] = 60;
        this.map[28][69] = 3;
        this.map[28][70] = 3;
        this.map[28][71] = 3;
        this.map[28][72] = 3;
        this.map[28][73] = 3;
        this.map[29][68] = 3;
        this.map[29][69] = 3;
        this.map[29][70] = 3;
        this.map[29][71] = 3;
        this.map[29][72] = 3;
        this.map[29][73] = 3;
        this.map[29][74] = 3;
        this.map[30][67] = 3;
        this.map[30][68] = 3;
        this.map[30][69] = 3;
        this.map[30][73] = 3;
        this.map[30][74] = 3;
        this.map[30][75] = 3;
        this.map[31][67] = 3;
        this.map[31][68] = 3;
        this.map[31][74] = 3;
        this.map[31][75] = 3;
        this.map[32][67] = 3;
        this.map[32][68] = 3;
        this.map[32][74] = 3;
        this.map[32][75] = 3;
        this.map[33][67] = 3;
        this.map[33][68] = 3;
        this.map[33][74] = 3;
        this.map[33][75] = 3;
        this.map[34][67] = 3;
        this.map[34][68] = 3;
        this.map[34][69] = 3;
        this.map[34][73] = 3;
        this.map[34][74] = 3;
        this.map[34][75] = 3;
        this.map[35][68] = 3;
        this.map[35][69] = 3;
        this.map[35][70] = 3;
        this.map[35][72] = 3;
        this.map[35][73] = 3;
        this.map[35][74] = 3;
        this.map[36][69] = 3;
        this.map[36][70] = 3;
        this.map[36][72] = 3;
        this.map[36][73] = 3;
        this.map[36][67] = 62;
        this.map[37][66] = 61;
        this.map[27][79] = 3;
        this.map[27][80] = 3;
        this.map[27][81] = 3;
        this.map[27][82] = 3;
        this.map[27][86] = 3;
        this.map[27][87] = 3;
        this.map[27][88] = 3;
        this.map[27][89] = 3;
        this.map[28][79] = 3;
        this.map[28][80] = 3;
        this.map[28][81] = 3;
        this.map[28][82] = 3;
        this.map[28][86] = 3;
        this.map[28][87] = 3;
        this.map[28][88] = 3;
        this.map[28][89] = 3;
        this.map[29][79] = 3;
        this.map[29][80] = 3;
        this.map[29][81] = 3;
        this.map[29][82] = 3;
        this.map[29][83] = 3;
        this.map[29][85] = 3;
        this.map[29][86] = 3;
        this.map[29][87] = 3;
        this.map[29][88] = 3;
        this.map[29][89] = 3;
        this.map[30][79] = 3;
        this.map[30][80] = 3;
        this.map[30][81] = 3;
        this.map[30][82] = 3;
        this.map[30][83] = 3;
        this.map[30][85] = 3;
        this.map[30][86] = 3;
        this.map[30][87] = 3;
        this.map[30][88] = 3;
        this.map[30][89] = 3;
        this.map[31][79] = 3;
        this.map[31][80] = 3;
        this.map[31][81] = 3;
        this.map[31][82] = 3;
        this.map[31][83] = 3;
        this.map[31][85] = 3;
        this.map[31][86] = 3;
        this.map[31][87] = 3;
        this.map[31][88] = 3;
        this.map[31][89] = 3;
        this.map[32][79] = 3;
        this.map[32][80] = 3;
        this.map[32][81] = 3;
        this.map[32][82] = 3;
        this.map[32][83] = 3;
        this.map[32][85] = 3;
        this.map[32][86] = 3;
        this.map[32][87] = 3;
        this.map[32][88] = 3;
        this.map[32][89] = 3;
        this.map[33][79] = 3;
        this.map[33][80] = 3;
        this.map[33][81] = 3;
        this.map[33][82] = 3;
        this.map[33][83] = 3;
        this.map[33][85] = 3;
        this.map[33][86] = 3;
        this.map[33][87] = 3;
        this.map[33][88] = 3;
        this.map[33][89] = 3;
        this.map[34][79] = 3;
        this.map[34][80] = 3;
        this.map[34][81] = 3;
        this.map[34][82] = 3;
        this.map[34][83] = 3;
        this.map[34][85] = 3;
        this.map[34][86] = 3;
        this.map[34][87] = 3;
        this.map[34][88] = 3;
        this.map[34][89] = 3;
        this.map[35][79] = 3;
        this.map[35][80] = 3;
        this.map[35][81] = 3;
        this.map[35][82] = 3;
        this.map[35][83] = 3;
        this.map[35][85] = 3;
        this.map[35][86] = 3;
        this.map[35][87] = 3;
        this.map[35][88] = 3;
        this.map[35][89] = 3;
        this.map[36][81] = 3;
        this.map[36][82] = 3;
        this.map[36][83] = 3;
        this.map[36][85] = 3;
        this.map[36][86] = 3;
        this.map[36][87] = 3;
        this.map[36][80] = 63;
        this.map[37][89] = 64;
        this.map[28][97] = 3;
        this.map[28][98] = 3;
        this.map[28][99] = 3;
        this.map[28][100] = 3;
        this.map[28][101] = 3;
        this.map[29][97] = 3;
        this.map[29][101] = 3;
        this.map[30][97] = 3;
        this.map[30][101] = 3;
        this.map[31][97] = 3;
        this.map[31][101] = 3;
        this.map[32][97] = 3;
        this.map[32][98] = 3;
        this.map[32][100] = 3;
        this.map[32][101] = 3;
        this.map[37][92] = 66;
        this.map[37][102] = 65;
        this.map[27][112] = 3;
        this.map[27][113] = 3;
        this.map[27][114] = 3;
        this.map[27][115] = 3;
        this.map[28][107] = 3;
        this.map[28][108] = 3;
        this.map[28][112] = 3;
        this.map[28][113] = 3;
        this.map[28][114] = 3;
        this.map[28][115] = 3;
        this.map[29][106] = 3;
        this.map[29][107] = 3;
        this.map[29][108] = 3;
        this.map[29][109] = 3;
        this.map[29][110] = 3;
        this.map[29][111] = 3;
        this.map[29][112] = 3;
        this.map[29][113] = 3;
        this.map[29][114] = 3;
        this.map[29][115] = 3;
        this.map[30][106] = 3;
        this.map[30][107] = 3;
        this.map[30][108] = 3;
        this.map[30][109] = 3;
        this.map[30][111] = 3;
        this.map[30][112] = 3;
        this.map[30][113] = 3;
        this.map[30][114] = 3;
        this.map[30][115] = 3;
        this.map[31][106] = 3;
        this.map[31][107] = 3;
        this.map[31][108] = 3;
        this.map[31][109] = 3;
        this.map[31][111] = 3;
        this.map[31][112] = 3;
        this.map[31][113] = 3;
        this.map[31][114] = 3;
        this.map[31][115] = 3;
        this.map[32][106] = 3;
        this.map[32][107] = 3;
        this.map[32][108] = 3;
        this.map[32][109] = 3;
        this.map[32][111] = 3;
        this.map[32][112] = 3;
        this.map[32][113] = 3;
        this.map[32][114] = 3;
        this.map[32][115] = 3;
        this.map[33][106] = 3;
        this.map[33][107] = 3;
        this.map[33][108] = 3;
        this.map[33][109] = 3;
        this.map[33][111] = 3;
        this.map[33][112] = 3;
        this.map[33][113] = 3;
        this.map[33][114] = 3;
        this.map[33][115] = 3;
        this.map[34][106] = 3;
        this.map[34][107] = 3;
        this.map[34][108] = 3;
        this.map[34][109] = 3;
        this.map[34][111] = 3;
        this.map[34][112] = 3;
        this.map[34][113] = 3;
        this.map[34][114] = 3;
        this.map[34][115] = 3;
        this.map[35][106] = 3;
        this.map[35][107] = 3;
        this.map[35][108] = 3;
        this.map[35][109] = 3;
        this.map[35][111] = 3;
        this.map[35][112] = 3;
        this.map[35][113] = 3;
        this.map[35][114] = 3;
        this.map[35][115] = 3;
        this.map[36][107] = 3;
        this.map[36][108] = 3;
        this.map[36][112] = 3;
        this.map[36][113] = 3;
        this.map[36][114] = 3;
        this.map[36][115] = 3;
        this.map[37][107] = 3;
        this.map[37][108] = 3;
        this.map[37][112] = 3;
        this.map[37][113] = 3;
        this.map[37][114] = 3;
        this.map[37][115] = 3;
        this.map[37][105] = 67;
        this.map[37][110] = 68;
        this.map[27][118] = 3;
        this.map[27][119] = 3;
        this.map[27][120] = 3;
        this.map[27][121] = 3;
        this.map[27][125] = 3;
        this.map[27][126] = 3;
        this.map[27][127] = 3;
        this.map[27][128] = 3;
        this.map[28][118] = 3;
        this.map[28][119] = 3;
        this.map[28][120] = 3;
        this.map[28][121] = 3;
        this.map[28][125] = 3;
        this.map[28][126] = 3;
        this.map[28][127] = 3;
        this.map[28][128] = 3;
        this.map[29][118] = 3;
        this.map[29][119] = 3;
        this.map[29][120] = 3;
        this.map[29][121] = 3;
        this.map[29][122] = 3;
        this.map[29][124] = 3;
        this.map[29][125] = 3;
        this.map[29][126] = 3;
        this.map[29][127] = 3;
        this.map[29][128] = 3;
        this.map[30][118] = 3;
        this.map[30][119] = 3;
        this.map[30][120] = 3;
        this.map[30][121] = 3;
        this.map[30][122] = 3;
        this.map[30][124] = 3;
        this.map[30][125] = 3;
        this.map[30][126] = 3;
        this.map[30][127] = 3;
        this.map[30][128] = 3;
        this.map[33][118] = 3;
        this.map[33][119] = 3;
        this.map[33][120] = 3;
        this.map[33][121] = 3;
        this.map[33][122] = 3;
        this.map[33][124] = 3;
        this.map[33][125] = 3;
        this.map[33][126] = 3;
        this.map[33][127] = 3;
        this.map[33][128] = 3;
        this.map[34][118] = 3;
        this.map[34][119] = 3;
        this.map[34][120] = 3;
        this.map[34][121] = 3;
        this.map[34][122] = 3;
        this.map[34][124] = 3;
        this.map[34][125] = 3;
        this.map[34][126] = 3;
        this.map[34][127] = 3;
        this.map[34][128] = 3;
        this.map[35][118] = 3;
        this.map[35][119] = 3;
        this.map[35][120] = 3;
        this.map[35][121] = 3;
        this.map[35][125] = 3;
        this.map[35][126] = 3;
        this.map[35][127] = 3;
        this.map[35][128] = 3;
        this.map[36][118] = 3;
        this.map[36][119] = 3;
        this.map[36][120] = 3;
        this.map[36][121] = 3;
        this.map[36][125] = 3;
        this.map[36][126] = 3;
        this.map[36][127] = 3;
        this.map[36][128] = 3;
        this.map[37][118] = 3;
        this.map[37][119] = 3;
        this.map[37][120] = 3;
        this.map[37][121] = 3;
        this.map[37][125] = 3;
        this.map[37][126] = 3;
        this.map[37][127] = 3;
        this.map[37][128] = 3;
        this.map[37][123] = 69;
        this.map[40][5] = 3;
        this.map[40][7] = 3;
        this.map[41][5] = 3;
        this.map[41][7] = 3;
        this.map[42][3] = 3;
        this.map[42][4] = 3;
        this.map[42][5] = 3;
        this.map[42][7] = 3;
        this.map[42][9] = 3;
        this.map[43][5] = 3;
        this.map[43][7] = 3;
        this.map[43][9] = 3;
        this.map[44][2] = 3;
        this.map[44][3] = 3;
        this.map[44][4] = 3;
        this.map[44][5] = 3;
        this.map[44][7] = 3;
        this.map[44][8] = 3;
        this.map[44][9] = 3;
        this.map[44][10] = 3;
        this.map[46][2] = 3;
        this.map[46][3] = 3;
        this.map[46][4] = 3;
        this.map[46][5] = 3;
        this.map[46][7] = 3;
        this.map[46][8] = 3;
        this.map[46][9] = 3;
        this.map[46][10] = 3;
        this.map[47][3] = 3;
        this.map[47][5] = 3;
        this.map[47][7] = 3;
        this.map[48][3] = 3;
        this.map[48][5] = 3;
        this.map[48][7] = 3;
        this.map[48][8] = 3;
        this.map[48][9] = 3;
        this.map[49][5] = 3;
        this.map[49][7] = 3;
        this.map[50][5] = 3;
        this.map[50][7] = 3;
        this.map[40][6] = 71;
        this.map[50][6] = 72;
        this.map[41][16] = 3;
        this.map[41][17] = 3;
        this.map[41][18] = 3;
        this.map[41][20] = 3;
        this.map[41][21] = 3;
        this.map[41][22] = 3;
        this.map[42][15] = 3;
        this.map[42][16] = 3;
        this.map[42][22] = 3;
        this.map[42][23] = 3;
        this.map[42][24] = 3;
        this.map[43][18] = 3;
        this.map[43][20] = 3;
        this.map[43][22] = 3;
        this.map[44][18] = 3;
        this.map[44][20] = 3;
        this.map[45][14] = 3;
        this.map[45][15] = 3;
        this.map[45][16] = 3;
        this.map[45][17] = 3;
        this.map[45][18] = 3;
        this.map[45][20] = 3;
        this.map[45][22] = 3;
        this.map[45][23] = 3;
        this.map[45][24] = 3;
        this.map[46][18] = 3;
        this.map[46][20] = 3;
        this.map[46][22] = 3;
        this.map[47][18] = 3;
        this.map[47][20] = 3;
        this.map[48][14] = 3;
        this.map[48][16] = 3;
        this.map[48][17] = 3;
        this.map[48][18] = 3;
        this.map[48][20] = 3;
        this.map[48][21] = 3;
        this.map[48][22] = 3;
        this.map[48][23] = 3;
        this.map[48][24] = 3;
        this.map[49][17] = 3;
        this.map[49][21] = 3;
        this.map[40][24] = 74;
        this.map[50][19] = 73;
        this.map[41][29] = 3;
        this.map[41][33] = 3;
        this.map[41][35] = 3;
        this.map[41][36] = 3;
        this.map[41][37] = 3;
        this.map[42][28] = 3;
        this.map[42][29] = 3;
        this.map[42][33] = 3;
        this.map[43][29] = 3;
        this.map[43][30] = 3;
        this.map[43][32] = 3;
        this.map[43][33] = 3;
        this.map[43][34] = 3;
        this.map[43][35] = 3;
        this.map[43][37] = 3;
        this.map[44][29] = 3;
        this.map[44][34] = 3;
        this.map[45][29] = 3;
        this.map[45][31] = 3;
        this.map[45][32] = 3;
        this.map[45][34] = 3;
        this.map[46][34] = 3;
        this.map[47][28] = 3;
        this.map[47][29] = 3;
        this.map[47][30] = 3;
        this.map[47][31] = 3;
        this.map[47][32] = 3;
        this.map[47][33] = 3;
        this.map[47][34] = 3;
        this.map[47][35] = 3;
        this.map[47][37] = 3;
        this.map[48][30] = 3;
        this.map[48][34] = 3;
        this.map[49][28] = 3;
        this.map[49][30] = 3;
        this.map[49][32] = 3;
        this.map[50][34] = 3;
        this.map[40][27] = 76;
        this.map[40][37] = 75;
        this.map[40][43] = 3;
        this.map[40][47] = 3;
        this.map[42][43] = 3;
        this.map[42][44] = 3;
        this.map[42][45] = 3;
        this.map[42][46] = 3;
        this.map[42][47] = 3;
        this.map[42][48] = 3;
        this.map[42][49] = 3;
        this.map[42][50] = 3;
        this.map[43][40] = 3;
        this.map[43][42] = 3;
        this.map[43][43] = 3;
        this.map[43][45] = 3;
        this.map[43][47] = 3;
        this.map[43][49] = 3;
        this.map[44][43] = 3;
        this.map[44][45] = 3;
        this.map[44][47] = 3;
        this.map[44][49] = 3;
        this.map[46][43] = 3;
        this.map[46][45] = 3;
        this.map[46][47] = 3;
        this.map[46][49] = 3;
        this.map[47][40] = 3;
        this.map[47][42] = 3;
        this.map[47][43] = 3;
        this.map[47][45] = 3;
        this.map[47][47] = 3;
        this.map[47][49] = 3;
        this.map[48][43] = 3;
        this.map[48][44] = 3;
        this.map[48][45] = 3;
        this.map[48][46] = 3;
        this.map[48][47] = 3;
        this.map[48][48] = 3;
        this.map[48][49] = 3;
        this.map[48][50] = 3;
        this.map[49][41] = 3;
        this.map[50][43] = 3;
        this.map[50][47] = 3;
        this.map[40][40] = 77;
        this.map[50][45] = 78;
        this.map[40][53] = 3;
        this.map[40][54] = 3;
        this.map[40][55] = 3;
        this.map[40][56] = 3;
        this.map[41][60] = 3;
        this.map[41][61] = 3;
        this.map[41][62] = 3;
        this.map[41][63] = 3;
        this.map[42][54] = 3;
        this.map[42][55] = 3;
        this.map[42][56] = 3;
        this.map[42][57] = 3;
        this.map[42][59] = 3;
        this.map[42][60] = 3;
        this.map[42][61] = 3;
        this.map[42][62] = 3;
        this.map[42][63] = 3;
        this.map[43][54] = 3;
        this.map[43][56] = 3;
        this.map[43][60] = 3;
        this.map[43][61] = 3;
        this.map[43][62] = 3;
        this.map[43][63] = 3;
        this.map[44][54] = 3;
        this.map[44][56] = 3;
        this.map[44][60] = 3;
        this.map[44][61] = 3;
        this.map[44][62] = 3;
        this.map[44][63] = 3;
        this.map[45][54] = 3;
        this.map[45][56] = 3;
        this.map[45][60] = 3;
        this.map[45][61] = 3;
        this.map[45][62] = 3;
        this.map[45][63] = 3;
        this.map[46][54] = 3;
        this.map[46][56] = 3;
        this.map[46][60] = 3;
        this.map[46][61] = 3;
        this.map[46][62] = 3;
        this.map[46][63] = 3;
        this.map[47][54] = 3;
        this.map[47][56] = 3;
        this.map[47][60] = 3;
        this.map[47][61] = 3;
        this.map[47][62] = 3;
        this.map[47][63] = 3;
        this.map[48][54] = 3;
        this.map[48][56] = 3;
        this.map[48][60] = 3;
        this.map[48][61] = 3;
        this.map[48][62] = 3;
        this.map[48][63] = 3;
        this.map[49][54] = 3;
        this.map[49][56] = 3;
        this.map[49][60] = 3;
        this.map[49][61] = 3;
        this.map[49][62] = 3;
        this.map[49][63] = 3;
        this.map[50][56] = 3;
        this.map[50][60] = 3;
        this.map[50][61] = 3;
        this.map[50][62] = 3;
        this.map[50][63] = 3;
        this.map[40][63] = 80;
        this.map[50][58] = 79;
        this.map[41][68] = 3;
        this.map[41][70] = 3;
        this.map[41][72] = 3;
        this.map[41][74] = 3;
        this.map[42][67] = 3;
        this.map[42][68] = 3;
        this.map[42][70] = 3;
        this.map[42][72] = 3;
        this.map[42][74] = 3;
        this.map[42][75] = 3;
        this.map[43][70] = 3;
        this.map[43][72] = 3;
        this.map[44][67] = 3;
        this.map[44][68] = 3;
        this.map[44][69] = 3;
        this.map[44][73] = 3;
        this.map[44][74] = 3;
        this.map[44][75] = 3;
        this.map[46][67] = 3;
        this.map[46][68] = 3;
        this.map[46][69] = 3;
        this.map[46][73] = 3;
        this.map[46][74] = 3;
        this.map[46][75] = 3;
        this.map[47][70] = 3;
        this.map[47][72] = 3;
        this.map[48][67] = 3;
        this.map[48][68] = 3;
        this.map[48][70] = 3;
        this.map[48][72] = 3;
        this.map[48][74] = 3;
        this.map[48][75] = 3;
        this.map[49][68] = 3;
        this.map[49][70] = 3;
        this.map[49][72] = 3;
        this.map[49][74] = 3;
        this.map[40][76] = 81;
        this.map[50][76] = 82;
        this.map[41][81] = 3;
        this.map[41][82] = 3;
        this.map[41][83] = 3;
        this.map[41][84] = 3;
        this.map[41][85] = 3;
        this.map[41][86] = 3;
        this.map[41][87] = 3;
        this.map[42][80] = 3;
        this.map[42][81] = 3;
        this.map[42][84] = 3;
        this.map[42][87] = 3;
        this.map[42][88] = 3;
        this.map[43][80] = 3;
        this.map[43][84] = 3;
        this.map[43][88] = 3;
        this.map[44][80] = 3;
        this.map[44][84] = 3;
        this.map[44][88] = 3;
        this.map[45][80] = 3;
        this.map[45][81] = 3;
        this.map[45][82] = 3;
        this.map[45][83] = 3;
        this.map[45][84] = 3;
        this.map[45][85] = 3;
        this.map[45][86] = 3;
        this.map[45][87] = 3;
        this.map[45][88] = 3;
        this.map[46][80] = 3;
        this.map[46][84] = 3;
        this.map[46][88] = 3;
        this.map[47][80] = 3;
        this.map[47][84] = 3;
        this.map[47][88] = 3;
        this.map[48][80] = 3;
        this.map[48][81] = 3;
        this.map[48][84] = 3;
        this.map[48][87] = 3;
        this.map[48][88] = 3;
        this.map[49][81] = 3;
        this.map[49][82] = 3;
        this.map[49][83] = 3;
        this.map[49][84] = 3;
        this.map[49][85] = 3;
        this.map[49][86] = 3;
        this.map[49][87] = 3;
        this.map[40][79] = 84;
        this.map[50][89] = 83;
        this.map[41][94] = 3;
        this.map[41][100] = 3;
        this.map[42][93] = 3;
        this.map[42][94] = 3;
        this.map[42][95] = 3;
        this.map[42][96] = 3;
        this.map[42][97] = 3;
        this.map[42][99] = 3;
        this.map[42][100] = 3;
        this.map[42][101] = 3;
        this.map[43][97] = 3;
        this.map[43][99] = 3;
        this.map[43][101] = 3;
        this.map[44][92] = 3;
        this.map[44][94] = 3;
        this.map[44][95] = 3;
        this.map[44][97] = 3;
        this.map[44][99] = 3;
        this.map[44][101] = 3;
        this.map[45][97] = 3;
        this.map[45][99] = 3;
        this.map[45][101] = 3;
        this.map[46][95] = 3;
        this.map[46][96] = 3;
        this.map[46][97] = 3;
        this.map[46][99] = 3;
        this.map[47][95] = 3;
        this.map[47][99] = 3;
        this.map[47][100] = 3;
        this.map[47][101] = 3;
        this.map[48][92] = 3;
        this.map[48][93] = 3;
        this.map[48][94] = 3;
        this.map[48][95] = 3;
        this.map[48][96] = 3;
        this.map[48][97] = 3;
        this.map[48][98] = 3;
        this.map[48][99] = 3;
        this.map[49][95] = 3;
        this.map[49][99] = 3;
        this.map[40][92] = 85;
        this.map[40][102] = 86;
        this.map[40][112] = 3;
        this.map[41][112] = 3;
        this.map[42][112] = 3;
        this.map[43][112] = 3;
        this.map[43][113] = 3;
        this.map[43][115] = 3;
        this.map[44][112] = 3;
        this.map[45][112] = 3;
        this.map[45][114] = 3;
        this.map[46][112] = 3;
        this.map[47][105] = 3;
        this.map[47][107] = 3;
        this.map[47][108] = 3;
        this.map[47][109] = 3;
        this.map[47][110] = 3;
        this.map[47][111] = 3;
        this.map[47][112] = 3;
        this.map[47][113] = 3;
        this.map[47][115] = 3;
        this.map[48][108] = 3;
        this.map[48][112] = 3;
        this.map[49][110] = 3;
        this.map[50][108] = 3;
        this.map[50][112] = 3;
        this.map[40][115] = 87;
        this.map[50][115] = 88;
        this.map[45][118] = 3;
        this.map[45][119] = 3;
        this.map[45][120] = 3;
        this.map[45][126] = 3;
        this.map[45][127] = 3;
        this.map[45][128] = 3;
        this.map[46][118] = 3;
        this.map[46][119] = 3;
        this.map[46][120] = 3;
        this.map[46][126] = 3;
        this.map[46][127] = 3;
        this.map[46][128] = 3;
        this.map[47][118] = 3;
        this.map[47][119] = 3;
        this.map[47][120] = 3;
        this.map[47][121] = 3;
        this.map[47][122] = 3;
        this.map[47][124] = 3;
        this.map[47][125] = 3;
        this.map[47][126] = 3;
        this.map[47][127] = 3;
        this.map[47][128] = 3;
        this.map[48][121] = 3;
        this.map[48][125] = 3;
        this.map[49][121] = 3;
        this.map[49][125] = 3;
        this.map[50][128] = 89;
        this.map[53][2] = 3;
        this.map[53][5] = 3;
        this.map[53][7] = 3;
        this.map[53][10] = 3;
        this.map[54][5] = 3;
        this.map[54][7] = 3;
        this.map[55][2] = 3;
        this.map[55][4] = 3;
        this.map[55][5] = 3;
        this.map[55][7] = 3;
        this.map[55][8] = 3;
        this.map[55][10] = 3;
        this.map[56][2] = 3;
        this.map[56][4] = 3;
        this.map[56][8] = 3;
        this.map[56][10] = 3;
        this.map[57][4] = 3;
        this.map[57][5] = 3;
        this.map[57][7] = 3;
        this.map[57][8] = 3;
        this.map[59][5] = 3;
        this.map[59][7] = 3;
        this.map[60][2] = 3;
        this.map[60][3] = 3;
        this.map[60][5] = 3;
        this.map[60][7] = 3;
        this.map[60][9] = 3;
        this.map[60][10] = 3;
        this.map[61][2] = 3;
        this.map[61][5] = 3;
        this.map[61][7] = 3;
        this.map[61][10] = 3;
        this.map[62][2] = 3;
        this.map[62][5] = 3;
        this.map[62][7] = 3;
        this.map[62][10] = 3;
        this.map[63][2] = 3;
        this.map[63][5] = 3;
        this.map[63][7] = 3;
        this.map[63][10] = 3;
        this.map[53][6] = 91;
        this.map[63][6] = 92;
        this.map[53][17] = 3;
        this.map[53][21] = 3;
        this.map[54][17] = 3;
        this.map[54][21] = 3;
        this.map[55][14] = 3;
        this.map[55][15] = 3;
        this.map[55][17] = 3;
        this.map[55][21] = 3;
        this.map[55][22] = 3;
        this.map[55][24] = 3;
        this.map[56][17] = 3;
        this.map[56][18] = 3;
        this.map[56][20] = 3;
        this.map[56][21] = 3;
        this.map[58][15] = 3;
        this.map[58][16] = 3;
        this.map[58][17] = 3;
        this.map[58][18] = 3;
        this.map[58][20] = 3;
        this.map[58][21] = 3;
        this.map[59][17] = 3;
        this.map[59][21] = 3;
        this.map[59][22] = 3;
        this.map[59][24] = 3;
        this.map[60][14] = 3;
        this.map[60][15] = 3;
        this.map[60][17] = 3;
        this.map[60][21] = 3;
        this.map[61][17] = 3;
        this.map[61][18] = 3;
        this.map[61][20] = 3;
        this.map[61][21] = 3;
        this.map[61][22] = 3;
        this.map[61][24] = 3;
        this.map[62][15] = 3;
        this.map[62][16] = 3;
        this.map[62][17] = 3;
        this.map[62][21] = 3;
        this.map[63][17] = 3;
        this.map[63][21] = 3;
        this.map[53][14] = 94;
        this.map[63][19] = 93;
        this.map[54][29] = 3;
        this.map[54][30] = 3;
        this.map[54][31] = 3;
        this.map[54][33] = 3;
        this.map[54][34] = 3;
        this.map[54][36] = 3;
        this.map[55][31] = 3;
        this.map[55][33] = 3;
        this.map[55][36] = 3;
        this.map[56][28] = 3;
        this.map[56][29] = 3;
        this.map[56][31] = 3;
        this.map[56][36] = 3;
        this.map[57][31] = 3;
        this.map[57][32] = 3;
        this.map[57][33] = 3;
        this.map[57][34] = 3;
        this.map[57][35] = 3;
        this.map[57][36] = 3;
        this.map[58][28] = 3;
        this.map[58][30] = 3;
        this.map[58][31] = 3;
        this.map[59][28] = 3;
        this.map[59][34] = 3;
        this.map[60][28] = 3;
        this.map[60][29] = 3;
        this.map[60][30] = 3;
        this.map[60][31] = 3;
        this.map[60][32] = 3;
        this.map[60][33] = 3;
        this.map[60][34] = 3;
        this.map[61][29] = 3;
        this.map[61][34] = 3;
        this.map[61][35] = 3;
        this.map[61][36] = 3;
        this.map[62][29] = 3;
        this.map[62][31] = 3;
        this.map[62][32] = 3;
        this.map[63][29] = 3;
        this.map[63][34] = 3;
        this.map[53][27] = 95;
        this.map[63][27] = 96;
        this.map[55][45] = 3;
        this.map[56][44] = 3;
        this.map[56][45] = 3;
        this.map[56][46] = 3;
        this.map[57][43] = 3;
        this.map[57][44] = 3;
        this.map[57][46] = 3;
        this.map[57][47] = 3;
        this.map[58][42] = 3;
        this.map[58][43] = 3;
        this.map[58][47] = 3;
        this.map[58][48] = 3;
        this.map[59][43] = 3;
        this.map[59][44] = 3;
        this.map[59][46] = 3;
        this.map[59][47] = 3;
        this.map[60][44] = 3;
        this.map[60][46] = 3;
        this.map[53][40] = 98;
        this.map[54][53] = 3;
        this.map[54][54] = 3;
        this.map[54][55] = 3;
        this.map[54][56] = 3;
        this.map[54][57] = 3;
        this.map[54][59] = 3;
        this.map[54][60] = 3;
        this.map[54][61] = 3;
        this.map[54][62] = 3;
        this.map[54][63] = 3;
        this.map[55][56] = 3;
        this.map[55][60] = 3;
        this.map[56][54] = 3;
        this.map[56][56] = 3;
        this.map[56][60] = 3;
        this.map[57][56] = 3;
        this.map[57][60] = 3;
        this.map[57][61] = 3;
        this.map[57][62] = 3;
        this.map[58][54] = 3;
        this.map[58][56] = 3;
        this.map[58][57] = 3;
        this.map[58][59] = 3;
        this.map[58][60] = 3;
        this.map[60][53] = 3;
        this.map[60][55] = 3;
        this.map[60][56] = 3;
        this.map[60][57] = 3;
        this.map[60][58] = 3;
        this.map[60][59] = 3;
        this.map[60][60] = 3;
        this.map[60][61] = 3;
        this.map[61][56] = 3;
        this.map[61][59] = 3;
        this.map[61][61] = 3;
        this.map[61][62] = 3;
        this.map[63][56] = 3;
        this.map[63][59] = 3;
        this.map[63][61] = 3;
        this.map[53][53] = 99;
        this.map[53][63] = 100;
        this.map[54][68] = 3;
        this.map[54][74] = 3;
        this.map[55][68] = 3;
        this.map[55][69] = 3;
        this.map[55][70] = 3;
        this.map[55][71] = 3;
        this.map[55][72] = 3;
        this.map[55][73] = 3;
        this.map[55][74] = 3;
        this.map[55][75] = 3;
        this.map[57][66] = 3;
        this.map[57][67] = 3;
        this.map[57][68] = 3;
        this.map[57][69] = 3;
        this.map[57][70] = 3;
        this.map[57][71] = 3;
        this.map[57][72] = 3;
        this.map[57][73] = 3;
        this.map[57][74] = 3;
        this.map[57][75] = 3;
        this.map[58][71] = 3;
        this.map[59][67] = 3;
        this.map[59][68] = 3;
        this.map[59][69] = 3;
        this.map[59][71] = 3;
        this.map[59][74] = 3;
        this.map[60][67] = 3;
        this.map[60][69] = 3;
        this.map[60][71] = 3;
        this.map[60][73] = 3;
        this.map[60][74] = 3;
        this.map[60][75] = 3;
        this.map[61][67] = 3;
        this.map[61][71] = 3;
        this.map[61][74] = 3;
        this.map[62][67] = 3;
        this.map[62][68] = 3;
        this.map[62][69] = 3;
        this.map[62][70] = 3;
        this.map[62][71] = 3;
        this.map[62][74] = 3;
        this.map[53][76] = 101;
        this.map[63][76] = 102;
        this.map[54][81] = 3;
        this.map[54][85] = 3;
        this.map[54][87] = 3;
        this.map[54][88] = 3;
        this.map[55][80] = 3;
        this.map[55][81] = 3;
        this.map[55][82] = 3;
        this.map[55][83] = 3;
        this.map[55][84] = 3;
        this.map[55][85] = 3;
        this.map[56][80] = 3;
        this.map[56][85] = 3;
        this.map[56][87] = 3;
        this.map[56][88] = 3;
        this.map[56][89] = 3;
        this.map[57][80] = 3;
        this.map[57][82] = 3;
        this.map[57][85] = 3;
        this.map[58][82] = 3;
        this.map[58][85] = 3;
        this.map[59][80] = 3;
        this.map[59][82] = 3;
        this.map[59][85] = 3;
        this.map[59][86] = 3;
        this.map[59][87] = 3;
        this.map[59][88] = 3;
        this.map[60][80] = 3;
        this.map[60][85] = 3;
        this.map[61][80] = 3;
        this.map[61][81] = 3;
        this.map[61][82] = 3;
        this.map[61][83] = 3;
        this.map[61][84] = 3;
        this.map[61][85] = 3;
        this.map[61][87] = 3;
        this.map[61][88] = 3;
        this.map[61][89] = 3;
        this.map[62][81] = 3;
        this.map[62][85] = 3;
        this.map[62][87] = 3;
        this.map[53][79] = 104;
        this.map[63][89] = 103;
        this.map[53][95] = 3;
        this.map[54][95] = 3;
        this.map[54][97] = 3;
        this.map[54][98] = 3;
        this.map[54][99] = 3;
        this.map[54][100] = 3;
        this.map[54][101] = 3;
        this.map[55][95] = 3;
        this.map[55][97] = 3;
        this.map[55][99] = 3;
        this.map[55][101] = 3;
        this.map[56][92] = 3;
        this.map[56][94] = 3;
        this.map[56][95] = 3;
        this.map[57][97] = 3;
        this.map[57][99] = 3;
        this.map[57][101] = 3;
        this.map[58][93] = 3;
        this.map[58][94] = 3;
        this.map[58][96] = 3;
        this.map[58][97] = 3;
        this.map[58][98] = 3;
        this.map[58][99] = 3;
        this.map[58][100] = 3;
        this.map[58][101] = 3;
        this.map[59][93] = 3;
        this.map[59][97] = 3;
        this.map[60][93] = 3;
        this.map[60][97] = 3;
        this.map[60][98] = 3;
        this.map[60][100] = 3;
        this.map[60][101] = 3;
        this.map[61][93] = 3;
        this.map[61][94] = 3;
        this.map[61][96] = 3;
        this.map[61][97] = 3;
        this.map[61][101] = 3;
        this.map[62][93] = 3;
        this.map[62][97] = 3;
        this.map[62][101] = 3;
        this.map[63][93] = 3;
        this.map[63][97] = 3;
        this.map[63][101] = 3;
        this.map[63][92] = 106;
        this.map[63][102] = 105;
        this.map[53][105] = 3;
        this.map[53][106] = 3;
        this.map[53][107] = 3;
        this.map[53][113] = 3;
        this.map[53][114] = 3;
        this.map[53][115] = 3;
        this.map[54][105] = 3;
        this.map[54][106] = 3;
        this.map[54][114] = 3;
        this.map[54][115] = 3;
        this.map[55][105] = 3;
        this.map[55][115] = 3;
        this.map[57][106] = 3;
        this.map[57][114] = 3;
        this.map[58][106] = 3;
        this.map[58][114] = 3;
        this.map[59][106] = 3;
        this.map[59][108] = 3;
        this.map[59][109] = 3;
        this.map[59][111] = 3;
        this.map[59][112] = 3;
        this.map[59][114] = 3;
        this.map[60][106] = 3;
        this.map[60][108] = 3;
        this.map[60][112] = 3;
        this.map[60][114] = 3;
        this.map[61][108] = 3;
        this.map[61][109] = 3;
        this.map[61][111] = 3;
        this.map[61][112] = 3;
        this.map[62][105] = 3;
        this.map[62][106] = 3;
        this.map[62][107] = 3;
        this.map[62][108] = 3;
        this.map[62][112] = 3;
        this.map[62][113] = 3;
        this.map[62][114] = 3;
        this.map[62][115] = 3;
        this.map[63][105] = 107;
        this.map[56][121] = 3;
        this.map[56][122] = 3;
        this.map[56][123] = 3;
        this.map[56][124] = 3;
        this.map[56][125] = 3;
        this.map[57][121] = 3;
        this.map[57][125] = 3;
        this.map[58][121] = 3;
        this.map[58][125] = 3;
        this.map[59][121] = 3;
        this.map[59][125] = 3;
        this.map[60][121] = 3;
        this.map[60][122] = 3;
        this.map[60][123] = 3;
        this.map[60][124] = 3;
        this.map[60][125] = 3;
        n3 = 0;
        while (n3 < 13) {
            n2 = 0;
            while (n2 < 13) {
                this.map[65 + n3][0 + n2] = 118;
                ++n2;
            }
            ++n3;
        }
        this.map[66][15] = 3;
        this.map[66][16] = 3;
        this.map[66][17] = 3;
        this.map[66][18] = 3;
        this.map[66][20] = 3;
        this.map[66][21] = 3;
        this.map[66][22] = 3;
        this.map[66][23] = 3;
        this.map[67][16] = 3;
        this.map[67][17] = 3;
        this.map[67][18] = 3;
        this.map[67][20] = 3;
        this.map[67][21] = 3;
        this.map[67][22] = 3;
        this.map[68][14] = 3;
        this.map[68][17] = 3;
        this.map[68][18] = 3;
        this.map[68][20] = 3;
        this.map[68][21] = 3;
        this.map[68][24] = 3;
        this.map[69][14] = 3;
        this.map[69][15] = 3;
        this.map[69][18] = 3;
        this.map[69][20] = 3;
        this.map[69][23] = 3;
        this.map[69][24] = 3;
        this.map[70][14] = 3;
        this.map[70][15] = 3;
        this.map[70][16] = 3;
        this.map[70][22] = 3;
        this.map[70][23] = 3;
        this.map[70][24] = 3;
        this.map[71][14] = 3;
        this.map[71][15] = 3;
        this.map[71][16] = 3;
        this.map[71][17] = 3;
        this.map[71][21] = 3;
        this.map[71][22] = 3;
        this.map[71][23] = 3;
        this.map[71][24] = 3;
        this.map[72][14] = 3;
        this.map[72][15] = 3;
        this.map[72][16] = 3;
        this.map[72][22] = 3;
        this.map[72][23] = 3;
        this.map[72][24] = 3;
        this.map[73][14] = 3;
        this.map[73][15] = 3;
        this.map[73][18] = 3;
        this.map[73][20] = 3;
        this.map[73][23] = 3;
        this.map[73][24] = 3;
        this.map[74][14] = 3;
        this.map[74][17] = 3;
        this.map[74][18] = 3;
        this.map[74][20] = 3;
        this.map[74][21] = 3;
        this.map[74][24] = 3;
        this.map[75][16] = 3;
        this.map[75][17] = 3;
        this.map[75][18] = 3;
        this.map[75][20] = 3;
        this.map[75][21] = 3;
        this.map[75][22] = 3;
        this.map[76][15] = 3;
        this.map[76][16] = 3;
        this.map[76][17] = 3;
        this.map[76][18] = 3;
        this.map[76][20] = 3;
        this.map[76][21] = 3;
        this.map[76][22] = 3;
        this.map[76][23] = 3;
        this.map[66][14] = 110;
        this.mapObject[1][3] = 5;
        this.mapObject[1][4] = 6;
        this.mapObject[1][5] = 5;
        this.mapObject[3][1] = 11;
        this.mapObject[3][4] = 2;
        this.mapObject[3][7] = 13;
        this.mapObject[3][8] = '\u0001';
        this.mapObject[4][2] = 9;
        this.mapObject[4][7] = 14;
        this.mapObject[4][8] = 11;
        this.mapObject[5][2] = 2;
        this.mapObject[5][9] = 2;
        this.mapObject[6][1] = '\u0001';
        this.mapObject[6][6] = 2;
        this.mapObject[6][7] = 7;
        this.mapObject[6][8] = 8;
        this.mapObject[6][9] = 7;
        this.mapObject[7][2] = 10;
        this.mapObject[8][2] = 2;
        this.mapObject[9][6] = 2;
        this.mapObject[9][10] = 2;
        this.mapObject[10][1] = 11;
        this.mapObject[10][3] = '\u0001';
        this.mapObject[10][5] = '\u0001';
        this.mapObject[10][10] = 7;
        this.mapObject[11][1] = 11;
        this.mapObject[11][2] = 26;
        this.mapObject[11][3] = '\u0001';
        this.mapObject[11][9] = 5;
        this.mapObject[11][10] = 12;
        this.mapObject[11][11] = 5;
        this.mapObject[1][16] = 4;
        this.mapObject[2][19] = 15;
        this.mapObject[2][21] = 15;
        this.mapObject[4][16] = '\u0001';
        this.mapObject[4][17] = '\u0001';
        this.mapObject[4][24] = 174;
        this.mapObject[5][16] = '\u0001';
        this.mapObject[5][18] = 19;
        this.mapObject[5][22] = 19;
        this.mapObject[7][16] = 87;
        this.mapObject[7][24] = 152;
        this.mapObject[8][18] = 19;
        this.mapObject[8][22] = 19;
        this.mapObject[10][16] = 12;
        this.mapObject[10][17] = 12;
        this.mapObject[11][16] = 12;
        this.mapObject[11][18] = 19;
        this.mapObject[11][22] = 19;
        this.mapObject[1][27] = '\u0001';
        this.mapObject[1][28] = 14;
        this.mapObject[1][30] = '\u0001';
        this.mapObject[1][31] = 12;
        this.mapObject[1][32] = '\u0001';
        this.mapObject[1][37] = 11;
        this.mapObject[2][28] = 11;
        this.mapObject[2][30] = 12;
        this.mapObject[2][31] = '\u0001';
        this.mapObject[2][32] = 12;
        this.mapObject[2][35] = 2;
        this.mapObject[2][36] = 7;
        this.mapObject[3][27] = 8;
        this.mapObject[3][30] = '\u0001';
        this.mapObject[3][31] = 3;
        this.mapObject[3][32] = '\u0001';
        this.mapObject[4][27] = 2;
        this.mapObject[4][37] = 153;
        this.mapObject[5][29] = 7;
        this.mapObject[5][33] = 5;
        this.mapObject[6][27] = 2;
        this.mapObject[7][27] = 9;
        this.mapObject[7][37] = 11;
        this.mapObject[8][28] = '\u0001';
        this.mapObject[8][35] = 2;
        this.mapObject[8][36] = 8;
        this.mapObject[8][37] = '\u0001';
        this.mapObject[9][27] = 11;
        this.mapObject[9][28] = 13;
        this.mapObject[10][34] = 6;
        this.mapObject[11][35] = 2;
        this.mapObject[1][41] = 3;
        this.mapObject[1][44] = 21;
        this.mapObject[1][45] = 22;
        this.mapObject[1][46] = 23;
        this.mapObject[1][49] = 175;
        this.mapObject[2][40] = 11;
        this.mapObject[2][42] = '\u0001';
        this.mapObject[2][48] = '\u0001';
        this.mapObject[2][50] = 12;
        this.mapObject[3][49] = 10;
        this.mapObject[4][41] = 2;
        this.mapObject[4][45] = 4;
        this.mapObject[4][49] = 2;
        this.mapObject[5][41] = 8;
        this.mapObject[5][43] = 2;
        this.mapObject[5][45] = 6;
        this.mapObject[5][48] = 9;
        this.mapObject[7][40] = 6;
        this.mapObject[7][42] = 5;
        this.mapObject[7][49] = 2;
        this.mapObject[8][40] = 2;
        this.mapObject[8][43] = 2;
        this.mapObject[8][47] = 2;
        this.mapObject[9][43] = 7;
        this.mapObject[9][47] = 8;
        this.mapObject[10][42] = 5;
        this.mapObject[10][44] = '\u0001';
        this.mapObject[10][46] = 13;
        this.mapObject[10][48] = 11;
        this.mapObject[11][42] = '\u0001';
        this.mapObject[11][43] = 5;
        this.mapObject[11][44] = '\u0001';
        this.mapObject[11][47] = 5;
        this.mapObject[1][56] = 6;
        this.mapObject[1][57] = 2;
        this.mapObject[1][62] = 2;
        this.mapObject[2][58] = '\u0001';
        this.mapObject[2][60] = 5;
        this.mapObject[2][61] = 5;
        this.mapObject[2][63] = 6;
        this.mapObject[3][54] = 2;
        this.mapObject[3][55] = 7;
        this.mapObject[3][60] = '\u0001';
        this.mapObject[3][61] = '\u0001';
        this.mapObject[4][56] = 2;
        this.mapObject[4][58] = 7;
        this.mapObject[4][60] = '\u0001';
        this.mapObject[4][61] = '\u0001';
        this.mapObject[5][53] = '\u0001';
        this.mapObject[5][55] = 8;
        this.mapObject[6][53] = '\u0001';
        this.mapObject[6][56] = 7;
        this.mapObject[6][59] = 5;
        this.mapObject[7][54] = 10;
        this.mapObject[7][63] = 6;
        this.mapObject[8][58] = 5;
        this.mapObject[9][53] = 14;
        this.mapObject[9][54] = '\u0001';
        this.mapObject[9][55] = 11;
        this.mapObject[9][56] = 25;
        this.mapObject[9][60] = 2;
        this.mapObject[11][61] = 89;
        this.mapObject[11][63] = 30;
        this.mapObject[1][68] = '\u0001';
        this.mapObject[1][69] = '\u0001';
        this.mapObject[1][72] = 8;
        this.mapObject[1][74] = '\u0001';
        this.mapObject[1][75] = 5;
        this.mapObject[2][68] = '\u0001';
        this.mapObject[2][69] = '\u0001';
        this.mapObject[2][76] = 2;
        this.mapObject[3][69] = 6;
        this.mapObject[3][73] = 11;
        this.mapObject[3][75] = 9;
        this.mapObject[4][67] = 2;
        this.mapObject[4][68] = 2;
        this.mapObject[4][70] = 2;
        this.mapObject[4][73] = 18;
        this.mapObject[4][76] = 7;
        this.mapObject[6][68] = 6;
        this.mapObject[6][69] = 8;
        this.mapObject[6][71] = '\u0001';
        this.mapObject[6][73] = 9;
        this.mapObject[6][74] = 10;
        this.mapObject[8][66] = 8;
        this.mapObject[8][69] = 42;
        this.mapObject[8][72] = 2;
        this.mapObject[8][73] = 2;
        this.mapObject[8][75] = 2;
        this.mapObject[9][67] = 7;
        this.mapObject[9][69] = 14;
        this.mapObject[9][74] = 6;
        this.mapObject[9][76] = 6;
        this.mapObject[10][66] = 2;
        this.mapObject[11][67] = 5;
        this.mapObject[11][70] = 9;
        this.mapObject[11][73] = 11;
        this.mapObject[11][74] = 11;
        this.mapObject[1][81] = 13;
        this.mapObject[1][84] = 41;
        this.mapObject[1][87] = '\u0001';
        this.mapObject[1][89] = 5;
        this.mapObject[2][81] = 11;
        this.mapObject[2][87] = '\u0001';
        this.mapObject[2][89] = 6;
        this.mapObject[3][81] = 7;
        this.mapObject[3][83] = 6;
        this.mapObject[3][85] = 10;
        this.mapObject[3][87] = 11;
        this.mapObject[3][89] = 5;
        this.mapObject[5][79] = 2;
        this.mapObject[5][81] = 2;
        this.mapObject[5][83] = 4;
        this.mapObject[5][85] = 2;
        this.mapObject[5][87] = 9;
        this.mapObject[5][89] = 2;
        this.mapObject[6][80] = 10;
        this.mapObject[6][82] = 8;
        this.mapObject[7][79] = 2;
        this.mapObject[7][81] = 2;
        this.mapObject[7][83] = 2;
        this.mapObject[7][85] = 2;
        this.mapObject[7][87] = 10;
        this.mapObject[7][89] = 2;
        this.mapObject[9][83] = 7;
        this.mapObject[9][85] = 6;
        this.mapObject[9][87] = 12;
        this.mapObject[10][79] = 5;
        this.mapObject[10][81] = 5;
        this.mapObject[10][83] = '\u0001';
        this.mapObject[10][85] = 8;
        this.mapObject[10][87] = '\u0001';
        this.mapObject[11][80] = 6;
        this.mapObject[11][83] = '\u0001';
        this.mapObject[11][85] = 12;
        this.mapObject[11][87] = '\u0001';
        this.mapObject[1][94] = 2;
        this.mapObject[1][95] = 2;
        this.mapObject[1][100] = '\u0001';
        this.mapObject[1][102] = '\u0001';
        this.mapObject[2][98] = 5;
        this.mapObject[2][101] = 28;
        this.mapObject[3][92] = 2;
        this.mapObject[3][97] = 2;
        this.mapObject[3][100] = 12;
        this.mapObject[3][102] = 11;
        this.mapObject[4][94] = '\u0001';
        this.mapObject[4][95] = '\u0001';
        this.mapObject[4][96] = '\u0001';
        this.mapObject[4][101] = 20;
        this.mapObject[5][92] = 11;
        this.mapObject[5][98] = 8;
        this.mapObject[5][100] = 29;
        this.mapObject[5][102] = 29;
        this.mapObject[6][93] = 6;
        this.mapObject[6][94] = 5;
        this.mapObject[6][95] = 6;
        this.mapObject[7][96] = 2;
        this.mapObject[7][98] = 7;
        this.mapObject[7][101] = 2;
        this.mapObject[8][95] = 7;
        this.mapObject[8][97] = 9;
        this.mapObject[8][99] = 8;
        this.mapObject[9][92] = 2;
        this.mapObject[9][102] = 2;
        this.mapObject[10][92] = 5;
        this.mapObject[10][95] = 13;
        this.mapObject[10][96] = '\u0001';
        this.mapObject[10][98] = 3;
        this.mapObject[10][99] = 11;
        this.mapObject[10][102] = 9;
        this.mapObject[11][93] = 7;
        this.mapObject[11][94] = 4;
        this.mapObject[11][95] = '\u0001';
        this.mapObject[11][96] = 14;
        this.mapObject[11][98] = 14;
        this.mapObject[11][98] = '\u0001';
        this.mapObject[11][100] = 2;
        this.mapObject[11][101] = 10;
        this.mapObject[1][107] = 9;
        this.mapObject[1][108] = 2;
        this.mapObject[1][112] = 2;
        this.mapObject[1][113] = 5;
        this.mapObject[1][115] = 11;
        this.mapObject[2][106] = '\u0001';
        this.mapObject[2][114] = 5;
        this.mapObject[3][105] = 10;
        this.mapObject[3][110] = 4;
        this.mapObject[4][106] = '\u0001';
        this.mapObject[4][109] = '\u0001';
        this.mapObject[4][111] = '\u0001';
        this.mapObject[4][112] = 2;
        this.mapObject[4][113] = 2;
        this.mapObject[5][105] = 14;
        this.mapObject[5][107] = 7;
        this.mapObject[5][108] = 2;
        this.mapObject[5][110] = 13;
        this.mapObject[6][111] = 6;
        this.mapObject[6][115] = 10;
        this.mapObject[7][105] = '\u0001';
        this.mapObject[7][107] = 2;
        this.mapObject[7][108] = 10;
        this.mapObject[7][109] = '\u0001';
        this.mapObject[7][113] = 35;
        this.mapObject[8][105] = 10;
        this.mapObject[8][115] = 2;
        this.mapObject[9][105] = 2;
        this.mapObject[9][109] = 2;
        this.mapObject[9][113] = '\u0001';
        this.mapObject[9][115] = 8;
        this.mapObject[10][106] = 11;
        this.mapObject[10][109] = 9;
        this.mapObject[10][111] = 7;
        this.mapObject[10][114] = 9;
        this.mapObject[11][107] = 4;
        this.mapObject[11][110] = 2;
        this.mapObject[11][112] = 2;
        this.mapObject[11][113] = 8;
        this.mapObject[11][115] = 11;
        this.mapObject[5][114] = 89;
        this.mapObject[3][118] = 9;
        this.mapObject[3][119] = 9;
        this.mapObject[3][120] = 9;
        this.mapObject[3][123] = 16;
        this.mapObject[3][126] = 9;
        this.mapObject[3][127] = 9;
        this.mapObject[3][128] = 9;
        this.mapObject[4][119] = 10;
        this.mapObject[4][121] = 20;
        this.mapObject[4][125] = 20;
        this.mapObject[4][127] = 10;
        this.mapObject[6][118] = 9;
        this.mapObject[6][119] = 14;
        this.mapObject[6][120] = 9;
        this.mapObject[6][126] = 9;
        this.mapObject[6][127] = 13;
        this.mapObject[6][128] = 9;
        this.mapObject[7][119] = 10;
        this.mapObject[7][127] = 10;
        this.mapObject[9][118] = 2;
        this.mapObject[9][120] = 2;
        this.mapObject[9][123] = 27;
        this.mapObject[9][126] = 2;
        this.mapObject[9][128] = 2;
        this.mapObject[11][121] = 8;
        this.mapObject[11][125] = 8;
        this.mapObject[11][128] = 12;
        this.mapObject[14][5] = 80;
        this.mapObject[14][7] = 2;
        this.mapObject[14][10] = 66;
        this.mapObject[14][11] = '\u0001';
        this.mapObject[15][2] = 36;
        this.mapObject[15][6] = 7;
        this.mapObject[15][8] = 48;
        this.mapObject[16][5] = 2;
        this.mapObject[16][9] = 2;
        this.mapObject[17][2] = 20;
        this.mapObject[17][6] = 47;
        this.mapObject[17][11] = 45;
        this.mapObject[18][1] = 46;
        this.mapObject[18][3] = 46;
        this.mapObject[18][5] = 48;
        this.mapObject[18][7] = 2;
        this.mapObject[18][8] = 46;
        this.mapObject[19][9] = 66;
        this.mapObject[20][1] = 76;
        this.mapObject[20][4] = 47;
        this.mapObject[20][7] = 2;
        this.mapObject[20][8] = 45;
        this.mapObject[21][2] = 4;
        this.mapObject[21][11] = 47;
        this.mapObject[22][2] = 47;
        this.mapObject[22][4] = 45;
        this.mapObject[22][5] = 2;
        this.mapObject[22][10] = 7;
        this.mapObject[23][1] = '\u0001';
        this.mapObject[23][9] = 2;
        this.mapObject[24][1] = '\u0001';
        this.mapObject[24][2] = '\u0001';
        this.mapObject[24][3] = '\u0001';
        this.mapObject[24][4] = '\u0001';
        this.mapObject[24][8] = 76;
        this.mapObject[24][9] = 47;
        this.mapObject[14][14] = 156;
        this.mapObject[14][18] = '\u0001';
        this.mapObject[14][19] = 80;
        this.mapObject[14][20] = '\u0001';
        this.mapObject[15][16] = 47;
        this.mapObject[16][18] = 46;
        this.mapObject[16][20] = 46;
        this.mapObject[16][23] = 48;
        this.mapObject[17][14] = 2;
        this.mapObject[17][19] = 2;
        this.mapObject[18][15] = 46;
        this.mapObject[18][17] = 2;
        this.mapObject[18][19] = 48;
        this.mapObject[18][22] = 66;
        this.mapObject[18][24] = 47;
        this.mapObject[19][20] = 46;
        this.mapObject[19][21] = 2;
        this.mapObject[19][23] = 83;
        this.mapObject[20][14] = '\u0001';
        this.mapObject[20][15] = '\u0001';
        this.mapObject[20][19] = 76;
        this.mapObject[20][22] = '\u0001';
        this.mapObject[20][24] = 45;
        this.mapObject[21][14] = '\u0001';
        this.mapObject[21][15] = 3;
        this.mapObject[21][22] = 4;
        this.mapObject[21][24] = 2;
        this.mapObject[22][16] = 48;
        this.mapObject[22][18] = 21;
        this.mapObject[22][19] = 22;
        this.mapObject[22][20] = 23;
        this.mapObject[22][22] = 45;
        this.mapObject[22][24] = 48;
        this.mapObject[23][16] = 2;
        this.mapObject[23][18] = 66;
        this.mapObject[23][20] = 66;
        this.mapObject[24][17] = 7;
        this.mapObject[24][21] = 7;
        this.mapObject[14][15] = 89;
        this.mapObject[14][23] = 89;
        this.mapObject[14][24] = 89;
        this.mapObject[14][27] = 79;
        this.mapObject[14][28] = 79;
        this.mapObject[14][29] = 79;
        this.mapObject[14][30] = 79;
        this.mapObject[14][31] = 79;
        this.mapObject[14][32] = 79;
        this.mapObject[14][33] = 79;
        this.mapObject[14][34] = 79;
        this.mapObject[14][35] = 79;
        this.mapObject[14][36] = 79;
        this.mapObject[14][37] = 79;
        this.mapObject[15][27] = 79;
        this.mapObject[15][28] = 79;
        this.mapObject[15][29] = 79;
        this.mapObject[15][30] = 79;
        this.mapObject[15][31] = 79;
        this.mapObject[15][32] = 79;
        this.mapObject[15][33] = 79;
        this.mapObject[15][34] = 79;
        this.mapObject[15][35] = 79;
        this.mapObject[15][36] = 79;
        this.mapObject[15][37] = 79;
        this.mapObject[16][27] = 79;
        this.mapObject[16][28] = 79;
        this.mapObject[16][29] = 79;
        this.mapObject[16][30] = 79;
        this.mapObject[16][34] = 79;
        this.mapObject[16][35] = 79;
        this.mapObject[16][36] = 79;
        this.mapObject[16][37] = 79;
        this.mapObject[17][27] = 79;
        this.mapObject[17][28] = 79;
        this.mapObject[17][29] = 79;
        this.mapObject[17][35] = 79;
        this.mapObject[17][36] = 79;
        this.mapObject[17][37] = 79;
        this.mapObject[18][27] = 79;
        this.mapObject[18][28] = 79;
        this.mapObject[18][29] = 79;
        this.mapObject[18][32] = 34;
        this.mapObject[18][35] = 79;
        this.mapObject[18][36] = 79;
        this.mapObject[18][37] = 79;
        this.mapObject[19][27] = 79;
        this.mapObject[19][28] = 79;
        this.mapObject[19][29] = 79;
        this.mapObject[19][32] = 79;
        this.mapObject[19][35] = 79;
        this.mapObject[19][36] = 79;
        this.mapObject[19][37] = 79;
        this.mapObject[20][27] = 79;
        this.mapObject[20][28] = 79;
        this.mapObject[20][29] = 79;
        this.mapObject[20][30] = 79;
        this.mapObject[20][32] = 79;
        this.mapObject[20][34] = 79;
        this.mapObject[20][35] = 79;
        this.mapObject[20][36] = 79;
        this.mapObject[20][37] = 79;
        this.mapObject[21][27] = 79;
        this.mapObject[21][28] = 79;
        this.mapObject[21][29] = 79;
        this.mapObject[21][30] = 79;
        this.mapObject[21][31] = 79;
        this.mapObject[21][32] = 79;
        this.mapObject[21][33] = 79;
        this.mapObject[21][34] = 79;
        this.mapObject[21][35] = 79;
        this.mapObject[21][36] = 79;
        this.mapObject[21][37] = 79;
        this.mapObject[22][27] = 79;
        this.mapObject[22][28] = 79;
        this.mapObject[22][29] = 79;
        this.mapObject[22][30] = 79;
        this.mapObject[22][31] = 79;
        this.mapObject[22][32] = 79;
        this.mapObject[22][33] = 79;
        this.mapObject[22][34] = 79;
        this.mapObject[22][35] = 79;
        this.mapObject[22][36] = 79;
        this.mapObject[22][37] = 79;
        this.mapObject[23][32] = 2;
        this.mapObject[14][40] = 49;
        this.mapObject[14][42] = 49;
        this.mapObject[14][44] = 83;
        this.mapObject[14][45] = '\u0001';
        this.mapObject[14][46] = 66;
        this.mapObject[14][48] = '\u0001';
        this.mapObject[14][49] = '\u0001';
        this.mapObject[14][50] = '\u0001';
        this.mapObject[15][41] = 49;
        this.mapObject[15][44] = 45;
        this.mapObject[15][46] = 49;
        this.mapObject[15][50] = '\u0001';
        this.mapObject[16][49] = 2;
        this.mapObject[17][41] = 4;
        this.mapObject[17][44] = 4;
        this.mapObject[17][46] = 2;
        this.mapObject[17][49] = 49;
        this.mapObject[18][40] = 66;
        this.mapObject[18][43] = 47;
        this.mapObject[18][45] = 56;
        this.mapObject[18][47] = 47;
        this.mapObject[19][41] = 45;
        this.mapObject[19][45] = 2;
        this.mapObject[19][48] = 66;
        this.mapObject[19][50] = 48;
        this.mapObject[20][40] = 2;
        this.mapObject[20][42] = 2;
        this.mapObject[20][50] = 2;
        this.mapObject[21][43] = 48;
        this.mapObject[21][45] = 2;
        this.mapObject[21][47] = 45;
        this.mapObject[21][49] = 45;
        this.mapObject[22][40] = 46;
        this.mapObject[22][42] = 46;
        this.mapObject[22][48] = 2;
        this.mapObject[23][44] = 66;
        this.mapObject[24][40] = 3;
        this.mapObject[24][43] = 2;
        this.mapObject[22][45] = 89;
        this.mapObject[14][53] = 83;
        this.mapObject[14][54] = 49;
        this.mapObject[14][56] = 2;
        this.mapObject[15][53] = 48;
        this.mapObject[15][63] = 45;
        this.mapObject[16][55] = 45;
        this.mapObject[16][58] = 20;
        this.mapObject[16][63] = 2;
        this.mapObject[17][53] = 2;
        this.mapObject[17][57] = 50;
        this.mapObject[17][58] = 51;
        this.mapObject[17][59] = 52;
        this.mapObject[17][61] = 47;
        this.mapObject[18][55] = '\u0001';
        this.mapObject[18][57] = 60;
        this.mapObject[18][58] = 61;
        this.mapObject[18][59] = 62;
        this.mapObject[18][62] = 47;
        this.mapObject[19][55] = 3;
        this.mapObject[19][57] = 70;
        this.mapObject[19][58] = 71;
        this.mapObject[19][59] = 72;
        this.mapObject[19][61] = 2;
        this.mapObject[19][63] = 46;
        this.mapObject[20][53] = 45;
        this.mapObject[20][55] = '\u0001';
        this.mapObject[21][63] = 76;
        this.mapObject[22][54] = 2;
        this.mapObject[22][61] = 2;
        this.mapObject[23][53] = 47;
        this.mapObject[23][55] = 47;
        this.mapObject[23][62] = 7;
        this.mapObject[24][54] = 46;
        this.mapObject[24][60] = 2;
        this.mapObject[24][61] = 7;
        this.mapObject[24][63] = 159;
        this.mapObject[14][66] = '\u0001';
        this.mapObject[14][67] = 47;
        this.mapObject[14][76] = 47;
        this.mapObject[15][66] = '\u0001';
        this.mapObject[15][67] = 46;
        this.mapObject[15][69] = 2;
        this.mapObject[15][73] = 2;
        this.mapObject[15][74] = 45;
        this.mapObject[16][66] = '\u0001';
        this.mapObject[16][67] = 47;
        this.mapObject[16][70] = 48;
        this.mapObject[16][72] = '\u0001';
        this.mapObject[16][76] = 66;
        this.mapObject[17][71] = 4;
        this.mapObject[17][75] = 2;
        this.mapObject[18][66] = 80;
        this.mapObject[18][67] = '\u0001';
        this.mapObject[18][70] = 66;
        this.mapObject[18][75] = 48;
        this.mapObject[19][66] = 66;
        this.mapObject[19][68] = 56;
        this.mapObject[19][69] = 2;
        this.mapObject[19][71] = 49;
        this.mapObject[20][66] = 83;
        this.mapObject[20][67] = '\u0001';
        this.mapObject[20][72] = '\u0001';
        this.mapObject[20][74] = 47;
        this.mapObject[20][76] = 3;
        this.mapObject[21][71] = 2;
        this.mapObject[21][75] = 2;
        this.mapObject[22][67] = 45;
        this.mapObject[22][70] = 47;
        this.mapObject[22][72] = 47;
        this.mapObject[22][75] = 46;
        this.mapObject[23][69] = 2;
        this.mapObject[23][73] = 2;
        this.mapObject[24][66] = 43;
        this.mapObject[24][74] = 95;
        this.mapObject[24][75] = 89;
        this.mapObject[24][76] = 89;
        this.mapObject[14][87] = 83;
        this.mapObject[14][89] = 80;
        this.mapObject[15][80] = 31;
        this.mapObject[15][88] = 76;
        this.mapObject[16][83] = 49;
        this.mapObject[16][85] = 47;
        this.mapObject[16][87] = '\u0001';
        this.mapObject[16][89] = '\u0001';
        this.mapObject[17][80] = 20;
        this.mapObject[17][88] = 20;
        this.mapObject[18][79] = 29;
        this.mapObject[18][81] = 29;
        this.mapObject[18][83] = 2;
        this.mapObject[18][85] = 4;
        this.mapObject[18][87] = 49;
        this.mapObject[18][89] = 49;
        this.mapObject[20][80] = 20;
        this.mapObject[20][83] = 48;
        this.mapObject[20][85] = 45;
        this.mapObject[20][88] = 20;
        this.mapObject[21][79] = 29;
        this.mapObject[21][81] = 29;
        this.mapObject[21][87] = 48;
        this.mapObject[21][89] = 48;
        this.mapObject[22][84] = 46;
        this.mapObject[23][80] = 2;
        this.mapObject[23][88] = 2;
        this.mapObject[24][79] = 66;
        this.mapObject[24][82] = 47;
        this.mapObject[24][86] = 47;
        this.mapObject[24][89] = 66;
        this.mapObject[14][95] = 4;
        this.mapObject[14][99] = 2;
        this.mapObject[14][100] = 46;
        this.mapObject[14][102] = '\u0001';
        this.mapObject[15][94] = 139;
        this.mapObject[15][101] = 45;
        this.mapObject[15][102] = '\u0001';
        this.mapObject[16][92] = 2;
        this.mapObject[16][102] = 3;
        this.mapObject[17][93] = 66;
        this.mapObject[17][95] = 2;
        this.mapObject[17][96] = 49;
        this.mapObject[17][98] = 49;
        this.mapObject[17][99] = 2;
        this.mapObject[17][100] = 48;
        this.mapObject[17][102] = '\u0001';
        this.mapObject[18][92] = 56;
        this.mapObject[18][94] = 56;
        this.mapObject[18][101] = 47;
        this.mapObject[18][102] = '\u0001';
        this.mapObject[19][97] = 4;
        this.mapObject[20][93] = 48;
        this.mapObject[20][101] = 56;
        this.mapObject[21][92] = 2;
        this.mapObject[21][95] = 2;
        this.mapObject[21][99] = 2;
        this.mapObject[21][102] = 2;
        this.mapObject[22][92] = 46;
        this.mapObject[22][95] = 47;
        this.mapObject[22][96] = 47;
        this.mapObject[22][98] = 45;
        this.mapObject[22][99] = 45;
        this.mapObject[22][102] = 46;
        this.mapObject[23][93] = '\u0001';
        this.mapObject[23][95] = 47;
        this.mapObject[23][96] = 47;
        this.mapObject[23][98] = 45;
        this.mapObject[23][99] = 45;
        this.mapObject[23][101] = '\u0001';
        this.mapObject[24][92] = 66;
        this.mapObject[24][93] = 80;
        this.mapObject[24][96] = '\u0001';
        this.mapObject[24][98] = '\u0001';
        this.mapObject[24][101] = 83;
        this.mapObject[24][102] = 66;
        this.mapObject[14][108] = 66;
        this.mapObject[14][110] = 46;
        this.mapObject[14][112] = 3;
        this.mapObject[14][114] = '\u0001';
        this.mapObject[14][115] = 80;
        this.mapObject[15][114] = 47;
        this.mapObject[16][105] = 2;
        this.mapObject[16][108] = 49;
        this.mapObject[16][110] = 89;
        this.mapObject[16][112] = 49;
        this.mapObject[16][114] = 2;
        this.mapObject[17][110] = 89;
        this.mapObject[17][105] = 7;
        this.mapObject[18][108] = '\u0001';
        this.mapObject[18][112] = '\u0001';
        this.mapObject[18][114] = 45;
        this.mapObject[18][115] = 45;
        this.mapObject[19][105] = 2;
        this.mapObject[19][109] = 56;
        this.mapObject[19][111] = 56;
        this.mapObject[20][105] = 47;
        this.mapObject[20][110] = 4;
        this.mapObject[20][115] = 2;
        this.mapObject[21][107] = 45;
        this.mapObject[21][112] = 49;
        this.mapObject[21][115] = 48;
        this.mapObject[22][105] = 2;
        this.mapObject[22][110] = 49;
        this.mapObject[22][113] = 66;
        this.mapObject[22][114] = '\u0001';
        this.mapObject[23][108] = 2;
        this.mapObject[23][109] = '\u0001';
        this.mapObject[23][111] = '\u0001';
        this.mapObject[23][115] = 47;
        this.mapObject[24][105] = 45;
        this.mapObject[24][107] = 47;
        this.mapObject[24][112] = 2;
        this.mapObject[24][114] = 7;
        this.mapObject[16][123] = 20;
        this.mapObject[17][118] = 83;
        this.mapObject[17][119] = 80;
        this.mapObject[17][127] = 11;
        this.mapObject[17][128] = 76;
        this.mapObject[18][118] = '\u0001';
        this.mapObject[18][122] = 47;
        this.mapObject[18][123] = 47;
        this.mapObject[18][124] = 47;
        this.mapObject[18][128] = '\u0001';
        this.mapObject[19][119] = 4;
        this.mapObject[19][122] = 47;
        this.mapObject[19][124] = 47;
        this.mapObject[19][127] = 4;
        this.mapObject[20][118] = 7;
        this.mapObject[20][122] = 47;
        this.mapObject[20][123] = 47;
        this.mapObject[20][124] = 47;
        this.mapObject[20][128] = 7;
        this.mapObject[21][119] = 7;
        this.mapObject[21][127] = 7;
        this.mapObject[22][118] = 2;
        this.mapObject[22][123] = 27;
        this.mapObject[22][128] = 2;
        this.mapObject[23][119] = 56;
        this.mapObject[23][127] = 56;
        this.mapObject[24][118] = 11;
        this.mapObject[24][121] = 46;
        this.mapObject[24][125] = 46;
        this.mapObject[24][128] = 11;
        this.mapObject[32][6] = 140;
        this.mapObject[27][28] = 115;
        this.mapObject[27][29] = 115;
        this.mapObject[27][30] = 115;
        this.mapObject[27][31] = 115;
        this.mapObject[28][28] = 115;
        this.mapObject[29][28] = 115;
        this.mapObject[29][30] = 115;
        this.mapObject[29][31] = 115;
        this.mapObject[29][34] = 115;
        this.mapObject[29][35] = 115;
        this.mapObject[29][36] = 115;
        this.mapObject[30][28] = 115;
        this.mapObject[30][31] = 115;
        this.mapObject[30][34] = 115;
        this.mapObject[30][36] = 115;
        this.mapObject[31][28] = 115;
        this.mapObject[31][29] = 115;
        this.mapObject[31][30] = 115;
        this.mapObject[31][31] = 115;
        this.mapObject[31][34] = 115;
        this.mapObject[31][35] = 115;
        this.mapObject[31][36] = 115;
        this.mapObject[33][28] = 115;
        this.mapObject[33][29] = 115;
        this.mapObject[33][30] = 115;
        this.mapObject[33][31] = 115;
        this.mapObject[33][33] = 115;
        this.mapObject[33][34] = 115;
        this.mapObject[33][35] = 115;
        this.mapObject[33][36] = 115;
        this.mapObject[34][28] = 115;
        this.mapObject[34][31] = 115;
        this.mapObject[34][33] = 115;
        this.mapObject[35][28] = 115;
        this.mapObject[35][31] = 115;
        this.mapObject[35][33] = 115;
        this.mapObject[35][34] = 115;
        this.mapObject[35][35] = 115;
        this.mapObject[36][28] = 115;
        this.mapObject[36][29] = 115;
        this.mapObject[36][30] = 115;
        this.mapObject[36][31] = 115;
        this.mapObject[36][33] = 115;
        this.mapObject[37][33] = 115;
        this.mapObject[37][37] = 138;
        this.mapObject[34][45] = 27;
        this.mapObject[32][58] = 96;
        this.mapObject[36][58] = 27;
        this.mapObject[30][70] = 79;
        this.mapObject[30][71] = 79;
        this.mapObject[30][72] = 79;
        this.mapObject[31][69] = 79;
        this.mapObject[31][70] = 79;
        this.mapObject[31][71] = 79;
        this.mapObject[31][72] = 79;
        this.mapObject[31][73] = 79;
        this.mapObject[32][69] = 79;
        this.mapObject[32][70] = 79;
        this.mapObject[32][71] = 44;
        this.mapObject[32][72] = 79;
        this.mapObject[32][73] = 79;
        this.mapObject[33][69] = 79;
        this.mapObject[33][70] = 79;
        this.mapObject[33][71] = 27;
        this.mapObject[33][72] = 79;
        this.mapObject[33][73] = 79;
        this.mapObject[34][70] = 79;
        this.mapObject[34][71] = 27;
        this.mapObject[34][72] = 79;
        this.mapObject[35][71] = 27;
        this.mapObject[36][71] = 27;
        this.mapObject[27][84] = 141;
        this.mapObject[30][99] = 161;
        this.mapObject[31][120] = 45;
        this.mapObject[31][121] = 6;
        this.mapObject[31][122] = 5;
        this.mapObject[31][124] = 5;
        this.mapObject[31][125] = 6;
        this.mapObject[31][126] = 45;
        this.mapObject[40][3] = '\u0001';
        this.mapObject[40][4] = '\u0001';
        this.mapObject[40][10] = 67;
        this.mapObject[40][11] = 142;
        this.mapObject[41][1] = 92;
        this.mapObject[41][3] = '\u0001';
        this.mapObject[41][4] = '\u0001';
        this.mapObject[41][8] = 93;
        this.mapObject[42][2] = 93;
        this.mapObject[42][8] = 2;
        this.mapObject[42][10] = 94;
        this.mapObject[42][11] = 94;
        this.mapObject[43][3] = 2;
        this.mapObject[43][4] = 3;
        this.mapObject[43][8] = 81;
        this.mapObject[44][1] = 2;
        this.mapObject[44][11] = 2;
        this.mapObject[45][2] = 94;
        this.mapObject[45][10] = 94;
        this.mapObject[46][1] = 2;
        this.mapObject[46][11] = 2;
        this.mapObject[47][4] = 84;
        this.mapObject[47][6] = 49;
        this.mapObject[47][8] = 77;
        this.mapObject[47][9] = 2;
        this.mapObject[48][1] = 94;
        this.mapObject[48][2] = 94;
        this.mapObject[48][4] = 2;
        this.mapObject[48][6] = 49;
        this.mapObject[48][10] = 95;
        this.mapObject[49][4] = 91;
        this.mapObject[49][8] = '\u0001';
        this.mapObject[49][9] = '\u0001';
        this.mapObject[49][11] = 95;
        this.mapObject[50][1] = 162;
        this.mapObject[50][2] = 67;
        this.mapObject[50][8] = '\u0001';
        this.mapObject[50][9] = '\u0001';
        this.mapObject[40][14] = 84;
        this.mapObject[40][16] = 4;
        this.mapObject[41][15] = 81;
        this.mapObject[42][14] = 2;
        this.mapObject[42][18] = 2;
        this.mapObject[42][20] = 2;
        this.mapObject[43][14] = 93;
        this.mapObject[43][16] = 95;
        this.mapObject[43][21] = 94;
        this.mapObject[43][23] = '\u0001';
        this.mapObject[43][24] = 77;
        this.mapObject[44][15] = '\u0001';
        this.mapObject[44][17] = 95;
        this.mapObject[44][22] = 2;
        this.mapObject[44][24] = '\u0001';
        this.mapObject[46][14] = '\u0001';
        this.mapObject[46][15] = '\u0001';
        this.mapObject[46][16] = '\u0001';
        this.mapObject[46][17] = '\u0001';
        this.mapObject[46][21] = 91;
        this.mapObject[46][23] = '\u0001';
        this.mapObject[46][24] = 3;
        this.mapObject[47][17] = 3;
        this.mapObject[47][22] = 2;
        this.mapObject[47][24] = '\u0001';
        this.mapObject[48][15] = 20;
        this.mapObject[49][14] = 15;
        this.mapObject[49][16] = 15;
        this.mapObject[49][22] = 21;
        this.mapObject[49][23] = 22;
        this.mapObject[49][24] = 23;
        this.mapObject[50][21] = 94;
        this.mapObject[40][29] = 2;
        this.mapObject[40][30] = 49;
        this.mapObject[40][32] = 95;
        this.mapObject[40][33] = 2;
        this.mapObject[41][31] = 67;
        this.mapObject[41][34] = 2;
        this.mapObject[42][27] = 4;
        this.mapObject[42][30] = 143;
        this.mapObject[42][32] = '\u0001';
        this.mapObject[42][37] = 77;
        this.mapObject[43][28] = 67;
        this.mapObject[43][31] = 2;
        this.mapObject[44][27] = 95;
        this.mapObject[44][32] = 49;
        this.mapObject[44][35] = 94;
        this.mapObject[44][37] = 94;
        this.mapObject[45][30] = 92;
        this.mapObject[45][33] = 2;
        this.mapObject[46][28] = 95;
        this.mapObject[46][29] = 2;
        this.mapObject[46][32] = 94;
        this.mapObject[46][35] = 93;
        this.mapObject[46][37] = 93;
        this.mapObject[47][27] = 2;
        this.mapObject[48][29] = 49;
        this.mapObject[48][32] = 93;
        this.mapObject[49][27] = 93;
        this.mapObject[49][31] = '\u0001';
        this.mapObject[49][33] = 95;
        this.mapObject[49][36] = 32;
        this.mapObject[50][27] = '\u0001';
        this.mapObject[50][28] = 95;
        this.mapObject[50][30] = 4;
        this.mapObject[50][32] = 2;
        this.mapObject[40][42] = 67;
        this.mapObject[40][45] = '\u0001';
        this.mapObject[40][48] = '\u0001';
        this.mapObject[40][49] = '\u0001';
        this.mapObject[40][50] = 84;
        this.mapObject[41][43] = 2;
        this.mapObject[41][44] = 95;
        this.mapObject[41][46] = 91;
        this.mapObject[41][47] = 2;
        this.mapObject[41][49] = '\u0001';
        this.mapObject[41][50] = 67;
        this.mapObject[42][41] = 95;
        this.mapObject[43][41] = 2;
        this.mapObject[43][44] = 5;
        this.mapObject[43][46] = 92;
        this.mapObject[43][48] = 45;
        this.mapObject[43][50] = 93;
        this.mapObject[44][44] = 2;
        this.mapObject[44][46] = 2;
        this.mapObject[44][48] = 2;
        this.mapObject[44][50] = 2;
        this.mapObject[46][44] = 2;
        this.mapObject[46][46] = 2;
        this.mapObject[46][48] = 2;
        this.mapObject[46][50] = 2;
        this.mapObject[47][41] = 2;
        this.mapObject[47][44] = 94;
        this.mapObject[47][46] = 6;
        this.mapObject[47][48] = 91;
        this.mapObject[47][50] = 7;
        this.mapObject[48][42] = 94;
        this.mapObject[49][40] = 92;
        this.mapObject[49][43] = 2;
        this.mapObject[49][47] = 2;
        this.mapObject[49][48] = 93;
        this.mapObject[49][50] = 67;
        this.mapObject[50][40] = 77;
        this.mapObject[50][41] = 93;
        this.mapObject[50][49] = '\u0001';
        this.mapObject[50][50] = 81;
        this.mapObject[42][58] = 20;
        this.mapObject[44][57] = 53;
        this.mapObject[44][58] = 54;
        this.mapObject[44][59] = 55;
        this.mapObject[45][57] = 63;
        this.mapObject[45][58] = 64;
        this.mapObject[45][59] = 65;
        this.mapObject[46][57] = 73;
        this.mapObject[46][58] = 74;
        this.mapObject[46][59] = 75;
        this.mapObject[41][53] = 89;
        this.mapObject[41][54] = 89;
        this.mapObject[41][55] = 89;
        this.mapObject[41][56] = 89;
        this.mapObject[42][53] = 89;
        this.mapObject[43][53] = 89;
        this.mapObject[43][55] = 89;
        this.mapObject[44][53] = 89;
        this.mapObject[44][55] = 89;
        this.mapObject[45][53] = 89;
        this.mapObject[45][55] = 89;
        this.mapObject[46][53] = 89;
        this.mapObject[46][55] = 89;
        this.mapObject[47][53] = 89;
        this.mapObject[47][55] = 89;
        this.mapObject[48][53] = 89;
        this.mapObject[48][55] = 89;
        this.mapObject[49][53] = 89;
        this.mapObject[49][55] = 89;
        this.mapObject[50][53] = 89;
        this.mapObject[50][54] = 89;
        this.mapObject[50][55] = 89;
        this.mapObject[40][66] = 144;
        this.mapObject[40][68] = 93;
        this.mapObject[40][72] = 49;
        this.mapObject[40][74] = 91;
        this.mapObject[41][71] = 2;
        this.mapObject[42][66] = 95;
        this.mapObject[42][76] = 95;
        this.mapObject[44][66] = 91;
        this.mapObject[44][71] = 94;
        this.mapObject[44][76] = 92;
        this.mapObject[45][67] = 2;
        this.mapObject[45][70] = 95;
        this.mapObject[45][72] = 95;
        this.mapObject[45][75] = 2;
        this.mapObject[46][71] = 91;
        this.mapObject[46][76] = 91;
        this.mapObject[48][66] = 92;
        this.mapObject[49][71] = 2;
        this.mapObject[50][66] = 77;
        this.mapObject[50][68] = 93;
        this.mapObject[50][70] = '\u0001';
        this.mapObject[50][72] = 49;
        this.mapObject[50][74] = 92;
        this.mapObject[41][69] = 89;
        this.mapObject[41][73] = 89;
        this.mapObject[42][69] = 89;
        this.mapObject[42][73] = 89;
        this.mapObject[43][67] = 89;
        this.mapObject[43][68] = 89;
        this.mapObject[43][69] = 89;
        this.mapObject[43][73] = 89;
        this.mapObject[43][74] = 89;
        this.mapObject[43][75] = 89;
        this.mapObject[47][67] = 89;
        this.mapObject[47][68] = 89;
        this.mapObject[47][69] = 89;
        this.mapObject[47][73] = 89;
        this.mapObject[47][74] = 89;
        this.mapObject[47][75] = 89;
        this.mapObject[48][69] = 89;
        this.mapObject[48][73] = 89;
        this.mapObject[49][69] = 89;
        this.mapObject[49][73] = 89;
        this.mapObject[40][81] = 2;
        this.mapObject[40][87] = 93;
        this.mapObject[40][89] = 77;
        this.mapObject[42][79] = 4;
        this.mapObject[42][82] = 67;
        this.mapObject[42][83] = 67;
        this.mapObject[42][85] = 67;
        this.mapObject[42][86] = 67;
        this.mapObject[42][89] = 91;
        this.mapObject[43][81] = 67;
        this.mapObject[43][82] = 67;
        this.mapObject[43][83] = '\u0001';
        this.mapObject[43][85] = 67;
        this.mapObject[43][86] = 67;
        this.mapObject[43][87] = 67;
        this.mapObject[44][81] = '\u0001';
        this.mapObject[44][82] = '\u0001';
        this.mapObject[44][83] = 105;
        this.mapObject[44][85] = 28;
        this.mapObject[44][86] = '\u0001';
        this.mapObject[44][87] = '\u0001';
        this.mapObject[45][79] = 67;
        this.mapObject[45][89] = 92;
        this.mapObject[46][81] = 84;
        this.mapObject[46][82] = 81;
        this.mapObject[46][83] = 77;
        this.mapObject[46][85] = 81;
        this.mapObject[46][86] = 81;
        this.mapObject[46][87] = 81;
        this.mapObject[47][81] = '\u0001';
        this.mapObject[47][82] = '\u0001';
        this.mapObject[47][83] = '\u0001';
        this.mapObject[47][85] = 84;
        this.mapObject[47][86] = 84;
        this.mapObject[47][87] = 84;
        this.mapObject[48][79] = 93;
        this.mapObject[48][82] = 3;
        this.mapObject[48][83] = 3;
        this.mapObject[48][85] = 77;
        this.mapObject[48][86] = '\u0001';
        this.mapObject[48][89] = 91;
        this.mapObject[50][79] = 145;
        this.mapObject[50][81] = 95;
        this.mapObject[50][87] = 94;
        this.mapObject[40][94] = 27;
        this.mapObject[40][95] = 95;
        this.mapObject[40][99] = 95;
        this.mapObject[40][100] = 2;
        this.mapObject[41][96] = 164;
        this.mapObject[41][97] = '\u0001';
        this.mapObject[42][92] = 94;
        this.mapObject[42][98] = 2;
        this.mapObject[42][102] = 2;
        this.mapObject[43][94] = 93;
        this.mapObject[43][95] = 93;
        this.mapObject[43][100] = '\u0001';
        this.mapObject[44][96] = 4;
        this.mapObject[44][100] = '\u0001';
        this.mapObject[45][95] = 4;
        this.mapObject[45][96] = 4;
        this.mapObject[45][98] = 94;
        this.mapObject[45][100] = '\u0001';
        this.mapObject[45][102] = 94;
        this.mapObject[46][93] = 37;
        this.mapObject[46][98] = 92;
        this.mapObject[46][101] = 91;
        this.mapObject[47][96] = 84;
        this.mapObject[47][97] = 67;
        this.mapObject[47][102] = 2;
        this.mapObject[48][100] = '\u0001';
        this.mapObject[48][102] = 94;
        this.mapObject[49][92] = 15;
        this.mapObject[49][94] = 15;
        this.mapObject[49][101] = 91;
        this.mapObject[50][95] = 2;
        this.mapObject[50][96] = 92;
        this.mapObject[50][98] = 48;
        this.mapObject[50][99] = 2;
        this.mapObject[50][100] = 93;
        this.mapObject[50][102] = 77;
        this.mapObject[41][106] = 2;
        this.mapObject[41][108] = 2;
        this.mapObject[41][110] = 2;
        this.mapObject[41][113] = 166;
        this.mapObject[42][115] = '\u0001';
        this.mapObject[43][106] = 2;
        this.mapObject[43][108] = 2;
        this.mapObject[43][110] = 2;
        this.mapObject[43][114] = 2;
        this.mapObject[44][115] = 93;
        this.mapObject[45][106] = 2;
        this.mapObject[45][108] = 2;
        this.mapObject[45][110] = 2;
        this.mapObject[45][113] = 95;
        this.mapObject[45][115] = 81;
        this.mapObject[46][115] = 94;
        this.mapObject[47][106] = 4;
        this.mapObject[47][114] = 2;
        this.mapObject[48][107] = 94;
        this.mapObject[48][109] = 92;
        this.mapObject[48][110] = 84;
        this.mapObject[48][111] = 91;
        this.mapObject[48][114] = 91;
        this.mapObject[49][106] = 94;
        this.mapObject[49][108] = 2;
        this.mapObject[49][112] = 2;
        this.mapObject[50][105] = 146;
        this.mapObject[50][107] = '\u0001';
        this.mapObject[50][110] = 95;
        this.mapObject[50][113] = 67;
        this.mapObject[41][119] = 92;
        this.mapObject[41][120] = 92;
        this.mapObject[41][121] = 92;
        this.mapObject[41][123] = 90;
        this.mapObject[41][125] = 91;
        this.mapObject[41][126] = 91;
        this.mapObject[41][127] = 91;
        this.mapObject[43][120] = 94;
        this.mapObject[43][121] = 94;
        this.mapObject[43][122] = 94;
        this.mapObject[43][124] = 93;
        this.mapObject[43][125] = 93;
        this.mapObject[43][126] = 93;
        this.mapObject[47][123] = 27;
        this.mapObject[48][118] = 84;
        this.mapObject[48][119] = '\u0001';
        this.mapObject[48][122] = 95;
        this.mapObject[48][124] = 95;
        this.mapObject[48][126] = 67;
        this.mapObject[48][127] = 92;
        this.mapObject[49][118] = 77;
        this.mapObject[49][126] = 93;
        this.mapObject[50][118] = 81;
        this.mapObject[50][120] = 91;
        this.mapObject[50][121] = 4;
        this.mapObject[50][125] = 2;
        this.mapObject[53][1] = 68;
        this.mapObject[53][4] = 3;
        this.mapObject[53][8] = 3;
        this.mapObject[53][11] = 68;
        this.mapObject[54][1] = 2;
        this.mapObject[54][2] = 99;
        this.mapObject[54][10] = 89;
        this.mapObject[54][11] = 2;
        this.mapObject[55][1] = 2;
        this.mapObject[55][11] = 2;
        this.mapObject[56][1] = 2;
        this.mapObject[56][3] = 2;
        this.mapObject[56][5] = 58;
        this.mapObject[56][7] = 58;
        this.mapObject[56][9] = 2;
        this.mapObject[56][11] = 2;
        this.mapObject[57][3] = 100;
        this.mapObject[57][9] = 100;
        this.mapObject[58][1] = 97;
        this.mapObject[58][5] = 4;
        this.mapObject[58][7] = 4;
        this.mapObject[58][11] = 97;
        this.mapObject[59][2] = 97;
        this.mapObject[59][4] = 98;
        this.mapObject[59][6] = 2;
        this.mapObject[59][8] = 98;
        this.mapObject[59][10] = 97;
        this.mapObject[60][1] = 2;
        this.mapObject[60][4] = 2;
        this.mapObject[60][6] = 2;
        this.mapObject[60][8] = 2;
        this.mapObject[60][11] = 2;
        this.mapObject[61][1] = 2;
        this.mapObject[61][3] = 68;
        this.mapObject[61][6] = 2;
        this.mapObject[61][9] = 68;
        this.mapObject[61][11] = 2;
        this.mapObject[62][1] = 2;
        this.mapObject[62][3] = '\u0001';
        this.mapObject[62][4] = '\u0001';
        this.mapObject[62][8] = '\u0001';
        this.mapObject[62][9] = '\u0001';
        this.mapObject[62][11] = 2;
        this.mapObject[63][1] = 78;
        this.mapObject[63][3] = '\u0001';
        this.mapObject[63][4] = 82;
        this.mapObject[63][8] = 85;
        this.mapObject[63][9] = '\u0001';
        this.mapObject[63][11] = 78;
        this.mapObject[53][22] = '\u0001';
        this.mapObject[53][23] = 3;
        this.mapObject[53][24] = '\u0001';
        this.mapObject[54][16] = 98;
        this.mapObject[54][19] = 28;
        this.mapObject[54][22] = '\u0001';
        this.mapObject[54][23] = '\u0001';
        this.mapObject[54][24] = '\u0001';
        this.mapObject[55][16] = 2;
        this.mapObject[56][14] = 147;
        this.mapObject[56][19] = 101;
        this.mapObject[56][22] = 100;
        this.mapObject[56][24] = 99;
        this.mapObject[57][16] = 98;
        this.mapObject[57][17] = 2;
        this.mapObject[57][21] = 2;
        this.mapObject[58][14] = 2;
        this.mapObject[58][24] = 100;
        this.mapObject[60][16] = 97;
        this.mapObject[60][22] = 58;
        this.mapObject[60][24] = 58;
        this.mapObject[61][14] = 78;
        this.mapObject[61][15] = '\u0001';
        this.mapObject[61][16] = '\u0001';
        this.mapObject[62][14] = 97;
        this.mapObject[62][22] = '\u0001';
        this.mapObject[62][23] = '\u0001';
        this.mapObject[62][24] = '\u0001';
        this.mapObject[63][14] = '\u0001';
        this.mapObject[63][15] = '\u0001';
        this.mapObject[63][16] = 85;
        this.mapObject[63][22] = '\u0001';
        this.mapObject[63][23] = 3;
        this.mapObject[63][24] = '\u0001';
        this.mapObject[53][29] = 2;
        this.mapObject[53][31] = 98;
        this.mapObject[53][33] = 2;
        this.mapObject[53][34] = 2;
        this.mapObject[53][35] = 58;
        this.mapObject[55][29] = 2;
        this.mapObject[55][32] = 101;
        this.mapObject[56][27] = 4;
        this.mapObject[56][30] = 99;
        this.mapObject[56][33] = 101;
        this.mapObject[56][35] = 38;
        this.mapObject[57][28] = 98;
        this.mapObject[57][37] = 2;
        this.mapObject[58][29] = 2;
        this.mapObject[58][32] = 78;
        this.mapObject[58][34] = 2;
        this.mapObject[59][31] = 98;
        this.mapObject[59][35] = 100;
        this.mapObject[59][37] = 68;
        this.mapObject[60][27] = 2;
        this.mapObject[60][36] = '\u0001';
        this.mapObject[61][28] = 97;
        this.mapObject[61][30] = 78;
        this.mapObject[61][32] = 101;
        this.mapObject[61][37] = 2;
        this.mapObject[62][30] = 78;
        this.mapObject[62][34] = 2;
        this.mapObject[62][36] = 97;
        this.mapObject[63][30] = 78;
        this.mapObject[63][32] = 4;
        this.mapObject[63][37] = 3;
        this.mapObject[57][45] = 68;
        this.mapObject[58][44] = 68;
        this.mapObject[58][45] = 39;
        this.mapObject[58][46] = 68;
        this.mapObject[59][45] = 68;
        this.mapObject[60][45] = 20;
        this.mapObject[61][44] = 102;
        this.mapObject[61][46] = 102;
        this.mapObject[54][58] = 2;
        this.mapObject[55][53] = 82;
        this.mapObject[55][54] = 82;
        this.mapObject[55][57] = 100;
        this.mapObject[55][59] = 99;
        this.mapObject[55][61] = 168;
        this.mapObject[56][53] = 4;
        this.mapObject[56][55] = 101;
        this.mapObject[56][63] = 98;
        this.mapObject[57][53] = 85;
        this.mapObject[57][54] = 85;
        this.mapObject[57][57] = 99;
        this.mapObject[57][59] = 100;
        this.mapObject[57][63] = 2;
        this.mapObject[58][53] = 4;
        this.mapObject[58][55] = 101;
        this.mapObject[58][58] = 2;
        this.mapObject[58][61] = 148;
        this.mapObject[59][56] = 2;
        this.mapObject[59][59] = 97;
        this.mapObject[59][63] = '\u0001';
        this.mapObject[60][54] = 27;
        this.mapObject[60][62] = 99;
        this.mapObject[61][57] = 101;
        this.mapObject[61][60] = 58;
        this.mapObject[61][63] = 2;
        this.mapObject[62][54] = 107;
        this.mapObject[62][56] = 20;
        this.mapObject[62][59] = 20;
        this.mapObject[62][61] = 2;
        this.mapObject[63][57] = 101;
        this.mapObject[63][60] = 58;
        this.mapObject[63][63] = 78;
        this.mapObject[53][67] = 99;
        this.mapObject[53][68] = 2;
        this.mapObject[53][70] = 21;
        this.mapObject[53][71] = 22;
        this.mapObject[53][72] = 23;
        this.mapObject[53][74] = 4;
        this.mapObject[54][66] = 68;
        this.mapObject[55][66] = 82;
        this.mapObject[55][76] = 2;
        this.mapObject[56][67] = 100;
        this.mapObject[56][68] = 2;
        this.mapObject[56][74] = 97;
        this.mapObject[57][76] = 2;
        this.mapObject[58][66] = 93;
        this.mapObject[58][68] = 92;
        this.mapObject[58][70] = 91;
        this.mapObject[58][72] = 68;
        this.mapObject[58][74] = 2;
        this.mapObject[58][75] = 98;
        this.mapObject[59][73] = 99;
        this.mapObject[60][66] = 48;
        this.mapObject[60][68] = 111;
        this.mapObject[60][70] = 98;
        this.mapObject[60][72] = 2;
        this.mapObject[60][76] = 2;
        this.mapObject[61][69] = 100;
        this.mapObject[61][73] = 149;
        this.mapObject[61][75] = 100;
        this.mapObject[62][66] = 47;
        this.mapObject[63][67] = 9;
        this.mapObject[63][69] = 6;
        this.mapObject[63][71] = 4;
        this.mapObject[63][74] = 2;
        this.mapObject[53][81] = 4;
        this.mapObject[53][85] = 2;
        this.mapObject[53][89] = '\u0001';
        this.mapObject[54][83] = 170;
        this.mapObject[54][86] = 99;
        this.mapObject[54][89] = 85;
        this.mapObject[55][87] = 98;
        this.mapObject[55][89] = '\u0001';
        this.mapObject[56][82] = 2;
        this.mapObject[56][83] = 99;
        this.mapObject[56][86] = 2;
        this.mapObject[57][81] = 97;
        this.mapObject[57][84] = 100;
        this.mapObject[57][87] = 100;
        this.mapObject[58][80] = 2;
        this.mapObject[58][86] = '\u0001';
        this.mapObject[58][89] = 97;
        this.mapObject[59][83] = 3;
        this.mapObject[59][84] = '\u0001';
        this.mapObject[59][89] = 2;
        this.mapObject[60][82] = 4;
        this.mapObject[60][83] = 82;
        this.mapObject[60][84] = 85;
        this.mapObject[61][79] = 99;
        this.mapObject[61][86] = 98;
        this.mapObject[62][82] = 68;
        this.mapObject[62][84] = 82;
        this.mapObject[63][81] = 2;
        this.mapObject[63][83] = 100;
        this.mapObject[63][85] = 2;
        this.mapObject[53][92] = 115;
        this.mapObject[53][93] = 78;
        this.mapObject[53][98] = 68;
        this.mapObject[53][99] = 68;
        this.mapObject[53][100] = 68;
        this.mapObject[54][94] = 150;
        this.mapObject[54][96] = 4;
        this.mapObject[54][102] = 4;
        this.mapObject[55][93] = 99;
        this.mapObject[55][98] = 58;
        this.mapObject[55][100] = 58;
        this.mapObject[56][93] = 4;
        this.mapObject[57][94] = 98;
        this.mapObject[57][98] = 58;
        this.mapObject[57][100] = 58;
        this.mapObject[57][102] = 97;
        this.mapObject[58][95] = 2;
        this.mapObject[59][92] = 97;
        this.mapObject[59][95] = 100;
        this.mapObject[59][101] = 100;
        this.mapObject[60][94] = 82;
        this.mapObject[60][96] = 68;
        this.mapObject[60][99] = 20;
        this.mapObject[61][92] = 100;
        this.mapObject[61][95] = 2;
        this.mapObject[62][95] = 101;
        this.mapObject[62][99] = 33;
        this.mapObject[63][94] = 85;
        this.mapObject[63][96] = 78;
        this.mapObject[59][110] = 20;
        this.mapObject[60][109] = 101;
        this.mapObject[60][111] = 101;
        this.mapObject[61][110] = 20;
        this.mapObject[62][109] = 99;
        this.mapObject[62][111] = 99;
        this.mapObject[63][107] = 27;
        n3 = 0;
        while (n3 < 11) {
            n2 = 0;
            while (n2 < 11) {
                this.mapObject[53 + n3][118 + n2] = 86;
                ++n2;
            }
            ++n3;
        }
        this.mapObject[56][121] = '\u0000';
        this.mapObject[56][122] = '\u0000';
        this.mapObject[56][123] = '\u0000';
        this.mapObject[56][124] = '\u0000';
        this.mapObject[56][125] = '\u0000';
        this.mapObject[57][121] = '\u0000';
        this.mapObject[57][122] = '\u0000';
        this.mapObject[57][123] = '\u0000';
        this.mapObject[57][124] = '\u0000';
        this.mapObject[57][125] = '\u0000';
        this.mapObject[58][121] = '\u0000';
        this.mapObject[58][122] = '\u0000';
        this.mapObject[58][123] = '\u0000';
        this.mapObject[58][124] = '\u0000';
        this.mapObject[58][125] = '\u0000';
        this.mapObject[59][121] = '\u0000';
        this.mapObject[59][122] = '\u0000';
        this.mapObject[59][123] = '\u0000';
        this.mapObject[59][124] = '\u0000';
        this.mapObject[59][125] = '\u0000';
        this.mapObject[60][121] = '\u0000';
        this.mapObject[60][122] = '\u0000';
        this.mapObject[60][123] = '\u0000';
        this.mapObject[60][124] = '\u0000';
        this.mapObject[60][125] = '\u0000';
        this.mapObject[71][19] = 113;
        this.mapObject[66][105] = '\u0000';
        this.mapObject[66][106] = '\u0001';
        this.mapObject[66][107] = 2;
        this.mapObject[66][108] = 3;
        this.mapObject[66][109] = 4;
        this.mapObject[66][110] = 5;
        this.mapObject[66][111] = 6;
        this.mapObject[66][112] = 7;
        this.mapObject[66][113] = 8;
        this.mapObject[66][114] = 9;
        this.mapObject[66][115] = 10;
        this.mapObject[67][105] = 21;
        this.mapObject[67][106] = 32;
        this.mapObject[67][107] = 43;
        this.mapObject[67][108] = 54;
        this.mapObject[67][109] = 65;
        this.mapObject[67][110] = 76;
        this.mapObject[67][111] = 87;
        this.mapObject[67][112] = 98;
        this.mapObject[67][113] = 109;
        this.mapObject[67][114] = 120;
        this.mapObject[67][115] = 119;
        this.mapObject[68][105] = 118;
        this.mapObject[68][106] = 117;
        this.mapObject[68][107] = 116;
        this.mapObject[68][108] = 115;
        this.mapObject[68][109] = 114;
        this.mapObject[68][110] = 113;
        this.mapObject[68][111] = 112;
        this.mapObject[68][112] = 111;
        this.mapObject[68][113] = 110;
        this.mapObject[68][114] = 99;
        this.mapObject[68][115] = 88;
        this.mapObject[69][105] = 77;
        this.mapObject[69][106] = 66;
        this.mapObject[69][107] = 55;
        this.mapObject[69][108] = 44;
        this.mapObject[69][109] = 33;
        this.mapObject[69][110] = 22;
        this.mapObject[69][111] = 11;
        this.mapObject[69][112] = 12;
        this.mapObject[69][113] = 13;
        this.mapObject[69][114] = 14;
        this.mapObject[69][115] = 15;
        this.mapObject[70][105] = 16;
        this.mapObject[70][106] = 17;
        this.mapObject[70][107] = 18;
        this.mapObject[70][108] = 19;
        this.mapObject[70][109] = 20;
        this.mapObject[70][110] = 31;
        this.mapObject[70][111] = 42;
        this.mapObject[70][112] = 53;
        this.mapObject[70][113] = 64;
        this.mapObject[70][114] = 75;
        this.mapObject[70][115] = 86;
        this.mapObject[71][105] = 97;
        this.mapObject[71][106] = 108;
        this.mapObject[71][107] = 107;
        this.mapObject[71][108] = 106;
        this.mapObject[71][109] = 105;
        this.mapObject[71][110] = 104;
        this.mapObject[71][111] = 103;
        this.mapObject[71][112] = 102;
        this.mapObject[71][113] = 101;
        this.mapObject[71][114] = 100;
        this.mapObject[71][115] = 89;
        this.mapObject[72][105] = 78;
        this.mapObject[72][106] = 67;
        this.mapObject[72][107] = 56;
        this.mapObject[72][108] = 45;
        this.mapObject[72][109] = 34;
        this.mapObject[72][110] = 23;
        this.mapObject[72][111] = 24;
        this.mapObject[72][112] = 25;
        this.mapObject[72][113] = 26;
        this.mapObject[72][114] = 27;
        this.mapObject[72][115] = 28;
        this.mapObject[73][105] = 29;
        this.mapObject[73][106] = 30;
        this.mapObject[73][107] = 41;
        this.mapObject[73][108] = 52;
        this.mapObject[73][109] = 63;
        this.mapObject[73][110] = 74;
        this.mapObject[73][111] = 85;
        this.mapObject[73][112] = 96;
        this.mapObject[73][113] = 95;
        this.mapObject[73][114] = 94;
        this.mapObject[73][115] = 93;
        this.mapObject[74][105] = 92;
        this.mapObject[74][106] = 91;
        this.mapObject[74][107] = 90;
        this.mapObject[74][108] = 79;
        this.mapObject[74][109] = 68;
        this.mapObject[74][110] = 57;
        this.mapObject[74][111] = 46;
        this.mapObject[74][112] = 35;
        this.mapObject[74][113] = 36;
        this.mapObject[74][114] = 37;
        this.mapObject[74][115] = 38;
        this.mapObject[75][105] = 39;
        this.mapObject[75][106] = 40;
        this.mapObject[75][107] = 51;
        this.mapObject[75][108] = 62;
        this.mapObject[75][109] = 73;
        this.mapObject[75][110] = 84;
        this.mapObject[75][111] = 83;
        this.mapObject[75][112] = 82;
        this.mapObject[75][113] = 81;
        this.mapObject[75][114] = 80;
        this.mapObject[75][115] = 69;
        this.mapObject[76][105] = 58;
        this.mapObject[76][106] = 47;
        this.mapObject[76][107] = 48;
        this.mapObject[76][108] = 49;
        this.mapObject[76][109] = 50;
        this.mapObject[76][110] = 61;
        this.mapObject[76][111] = 72;
        this.mapObject[76][112] = 71;
        this.mapObject[76][113] = 70;
        this.mapObject[76][114] = 59;
        this.mapObject[76][115] = 60;
        this.mapObject[66][118] = 1000;
        this.mapObject[66][119] = '\u0000';
        this.mapObject[66][120] = '\u0000';
        this.mapObject[66][121] = '\u0000';
        this.mapObject[66][122] = '\u0000';
        this.mapObject[66][123] = '\u0000';
        this.mapObject[66][124] = '\u0000';
        this.mapObject[66][125] = '\u0000';
        this.mapObject[66][126] = '\u0000';
        this.mapObject[66][127] = '\u0000';
        this.mapObject[66][128] = '\u0000';
        this.mapObject[67][118] = 100;
        this.mapObject[67][119] = 8;
        this.mapObject[67][120] = '\u0000';
        this.mapObject[67][121] = '\u0000';
        this.mapObject[67][122] = '\u0000';
        this.mapObject[67][123] = '\u0000';
        this.mapObject[67][124] = '\u0000';
        this.mapObject[67][125] = '\u0000';
        this.mapObject[67][126] = '\u0000';
        this.mapObject[67][127] = '\u0000';
        this.mapObject[67][128] = '\u0000';
        this.mapObject[68][118] = 100;
        this.mapObject[68][119] = '\u0000';
        this.mapObject[68][120] = '\u0000';
        this.mapObject[68][121] = '\u0000';
        this.mapObject[68][122] = '\u0000';
        this.mapObject[68][123] = '\u0000';
        this.mapObject[68][124] = '\u0000';
        this.mapObject[68][125] = '\u0000';
        this.mapObject[68][126] = '\u0000';
        this.mapObject[68][127] = 2;
        this.mapObject[68][128] = '\u0000';
        this.mapObject[69][118] = '\u0000';
        this.mapObject[69][119] = 34;
        this.mapObject[69][120] = '\u0000';
        this.mapObject[69][121] = '\u0000';
        this.mapObject[69][122] = '\u0000';
        this.mapObject[69][123] = '\u0000';
        this.mapObject[69][124] = '\u0000';
        this.mapObject[69][125] = '\u0000';
        this.mapObject[69][126] = '\u0000';
        this.mapObject[69][127] = 2;
        this.mapObject[69][128] = '\u0000';
        this.mapObject[70][118] = '\u0001';
        this.mapObject[70][119] = 39;
        this.mapObject[70][120] = '\u0000';
        this.mapObject[70][121] = '\u0000';
        this.mapObject[70][122] = '\u0000';
        this.mapObject[70][123] = '\u0000';
        this.mapObject[70][124] = '\u0000';
        this.mapObject[70][125] = '\u0000';
        this.mapObject[70][126] = '\u0000';
        this.mapObject[70][127] = 16;
        this.mapObject[70][128] = '\u0000';
        this.mapObject[71][118] = '\u0001';
        this.mapObject[71][119] = '\u0000';
        this.mapObject[71][120] = '\u0000';
        this.mapObject[71][121] = '\u0000';
        this.mapObject[71][122] = '\u0000';
        this.mapObject[71][123] = '\u0000';
        this.mapObject[71][124] = '\u0000';
        this.mapObject[71][125] = '\u0000';
        this.mapObject[71][126] = '\u0000';
        this.mapObject[71][127] = '\u0000';
        this.mapObject[71][128] = '\u0000';
        this.mapObject[72][118] = 6;
        this.mapObject[72][119] = '\u0000';
        this.mapObject[72][120] = '\u0000';
        this.mapObject[72][121] = '\u0000';
        this.mapObject[72][122] = '\u0000';
        this.mapObject[72][123] = '\u0000';
        this.mapObject[72][124] = 2;
        this.mapObject[72][125] = '\u0000';
        this.mapObject[72][126] = '\u0000';
        this.mapObject[72][127] = '\u0000';
        this.mapObject[72][128] = '\u0000';
        this.mapObject[73][118] = 11;
        this.mapObject[73][119] = '\u0000';
        this.mapObject[73][120] = '\u0000';
        this.mapObject[73][121] = '\u0000';
        this.mapObject[73][122] = '\u0000';
        this.mapObject[73][123] = '\u0000';
        this.mapObject[73][124] = '\u0000';
        this.mapObject[73][125] = '\u0000';
        this.mapObject[73][126] = '\u0000';
        this.mapObject[73][127] = '\u0000';
        this.mapObject[73][128] = '\u0000';
        this.mapObject[74][118] = '\u0000';
        this.mapObject[74][119] = '\u0000';
        this.mapObject[74][120] = '\u0000';
        this.mapObject[74][121] = '\u0000';
        this.mapObject[74][122] = '\u0000';
        this.mapObject[74][123] = '\u0000';
        this.mapObject[74][124] = '\u0000';
        this.mapObject[74][125] = '\u0000';
        this.mapObject[74][126] = '\u0000';
        this.mapObject[74][127] = '\u0000';
        this.mapObject[74][128] = '\u0000';
        this.mapObject[75][118] = '\u0000';
        this.mapObject[75][119] = '\u0000';
        this.mapObject[75][120] = '\u0000';
        this.mapObject[75][121] = '\u0000';
        this.mapObject[75][122] = '\u0000';
        this.mapObject[75][123] = '\u0000';
        this.mapObject[75][124] = '\u0000';
        this.mapObject[75][125] = '\u0000';
        this.mapObject[75][126] = '\u0000';
        this.mapObject[75][127] = '\u0001';
        this.mapObject[75][128] = '\u0000';
        this.mapObject[76][118] = '\u0000';
        this.mapObject[76][119] = '\u0000';
        this.mapObject[76][120] = '\u0000';
        this.mapObject[76][121] = '\u0000';
        this.mapObject[76][122] = '\u0000';
        this.mapObject[76][123] = '\u0000';
        this.mapObject[76][124] = '\u0000';
        this.mapObject[76][125] = '\u0000';
        this.mapObject[76][126] = '\u0000';
        this.mapObject[76][127] = '\u0000';
        this.mapObject[76][128] = '\u0000';
        this.charaX = this.mapObject[72][118];
        this.charaY = this.mapObject[73][118];
        this.mapX = this.charaX / 13;
        this.charaX = this.charaX % 13 * 5;
        this.mapY = this.charaY / 13;
        this.charaY = this.charaY % 13 * 5;
        int n4 = 0;
        while (n4 < 200) {
            n = 0;
            while (n < 40) {
                this.objectAttribute[n4][n] = 0;
                ++n;
            }
            ++n4;
        }
        n = 0;
        while (n < 2) {
            n4 = 0;
            while (n4 < 400) {
                this.strMessage[n][n4] = "";
                ++n4;
            }
            ++n;
        }
        this.loadMapData2();
    }

    /*
     * Opcode count of 17537 triggered aggressive code reduction.  Override with --aggressivesizethreshold.
     */
    public void loadMapData2() {
        this.objectAttribute[2][3] = 5;
        this.objectAttribute[2][1] = 36;
        this.objectAttribute[2][2] = 0;
        this.objectAttribute[2][6] = 0;
        this.objectAttribute[2][7] = 160;
        this.objectAttribute[4][3] = 5;
        this.objectAttribute[4][1] = 37;
        this.objectAttribute[4][2] = 0;
        this.objectAttribute[4][6] = 40;
        this.objectAttribute[4][7] = 160;
        this.objectAttribute[27][3] = 5;
        this.objectAttribute[27][1] = 38;
        this.objectAttribute[27][2] = 0;
        this.objectAttribute[27][6] = 80;
        this.objectAttribute[27][7] = 160;
        this.objectAttribute[115][3] = 5;
        this.objectAttribute[115][1] = 32;
        this.objectAttribute[115][2] = 0;
        this.objectAttribute[19][3] = 0;
        this.objectAttribute[19][1] = 40;
        this.objectAttribute[19][2] = 0;
        this.objectAttribute[19][6] = 160;
        this.objectAttribute[19][7] = 160;
        this.objectAttribute[20][3] = 0;
        this.objectAttribute[20][1] = 39;
        this.objectAttribute[20][2] = 0;
        this.objectAttribute[20][6] = 120;
        this.objectAttribute[20][7] = 160;
        this.objectAttribute[21][3] = 0;
        this.objectAttribute[21][1] = 45;
        this.objectAttribute[21][2] = 0;
        this.objectAttribute[21][6] = 120;
        this.objectAttribute[21][7] = 200;
        this.objectAttribute[23][3] = 0;
        this.objectAttribute[23][1] = 48;
        this.objectAttribute[23][2] = 0;
        this.objectAttribute[23][6] = 200;
        this.objectAttribute[23][7] = 200;
        this.objectAttribute[53][3] = 0;
        this.objectAttribute[53][1] = 145;
        this.objectAttribute[53][2] = 146;
        this.objectAttribute[53][6] = 120;
        this.objectAttribute[53][7] = 600;
        this.objectAttribute[53][8] = 80;
        this.objectAttribute[53][9] = 640;
        this.objectAttribute[54][3] = 0;
        this.objectAttribute[54][1] = 147;
        this.objectAttribute[54][2] = 148;
        this.objectAttribute[54][6] = 160;
        this.objectAttribute[54][7] = 600;
        this.objectAttribute[54][8] = 120;
        this.objectAttribute[54][9] = 640;
        this.objectAttribute[55][3] = 0;
        this.objectAttribute[55][1] = 149;
        this.objectAttribute[55][2] = 150;
        this.objectAttribute[55][6] = 200;
        this.objectAttribute[55][7] = 600;
        this.objectAttribute[55][8] = 160;
        this.objectAttribute[55][9] = 640;
        this.objectAttribute[63][3] = 0;
        this.objectAttribute[63][1] = 151;
        this.objectAttribute[63][2] = 152;
        this.objectAttribute[63][6] = 240;
        this.objectAttribute[63][7] = 600;
        this.objectAttribute[63][8] = 200;
        this.objectAttribute[63][9] = 640;
        this.objectAttribute[64][3] = 0;
        this.objectAttribute[64][1] = 153;
        this.objectAttribute[64][2] = 154;
        this.objectAttribute[64][6] = 280;
        this.objectAttribute[64][7] = 600;
        this.objectAttribute[64][8] = 240;
        this.objectAttribute[64][9] = 640;
        this.objectAttribute[65][3] = 0;
        this.objectAttribute[65][1] = 155;
        this.objectAttribute[65][2] = 156;
        this.objectAttribute[65][6] = 320;
        this.objectAttribute[65][7] = 600;
        this.objectAttribute[65][8] = 280;
        this.objectAttribute[65][9] = 640;
        this.objectAttribute[73][3] = 0;
        this.objectAttribute[73][1] = 157;
        this.objectAttribute[73][2] = 158;
        this.objectAttribute[73][6] = 360;
        this.objectAttribute[73][7] = 600;
        this.objectAttribute[73][8] = 320;
        this.objectAttribute[73][9] = 640;
        this.objectAttribute[75][3] = 0;
        this.objectAttribute[75][1] = 161;
        this.objectAttribute[75][2] = 162;
        this.objectAttribute[75][6] = 40;
        this.objectAttribute[75][7] = 640;
        this.objectAttribute[75][8] = 0;
        this.objectAttribute[75][9] = 680;
        this.objectAttribute[86][3] = 0;
        this.objectAttribute[86][1] = 43;
        this.objectAttribute[86][2] = 44;
        this.objectAttribute[86][6] = 40;
        this.objectAttribute[86][7] = 200;
        this.objectAttribute[86][8] = 80;
        this.objectAttribute[86][9] = 200;
        this.mapAttribute[1][3] = 0;
        this.mapAttribute[1][1] = 32;
        this.mapAttribute[1][2] = 0;
        this.mapAttribute[1][6] = 200;
        this.mapAttribute[1][7] = 160;
        this.mapAttribute[2][3] = 0;
        this.mapAttribute[2][1] = 33;
        this.mapAttribute[2][2] = 0;
        this.mapAttribute[2][6] = 240;
        this.mapAttribute[2][7] = 160;
        this.mapAttribute[3][3] = 1;
        this.mapAttribute[3][1] = 33;
        this.mapAttribute[3][2] = 0;
        this.mapAttribute[30][3] = 1;
        this.mapAttribute[30][1] = 8;
        this.mapAttribute[30][2] = 0;
        this.mapAttribute[30][6] = 0;
        this.mapAttribute[30][7] = 0;
        this.mapAttribute[31][3] = 1;
        this.mapAttribute[31][1] = 9;
        this.mapAttribute[31][2] = 0;
        this.mapAttribute[31][6] = 0;
        this.mapAttribute[31][7] = 0;
        this.mapAttribute[32][3] = 1;
        this.mapAttribute[32][1] = 10;
        this.mapAttribute[32][2] = 0;
        this.mapAttribute[32][6] = 0;
        this.mapAttribute[32][7] = 0;
        this.mapAttribute[33][3] = 1;
        this.mapAttribute[33][1] = 11;
        this.mapAttribute[33][2] = 0;
        this.mapAttribute[33][6] = 0;
        this.mapAttribute[33][7] = 0;
        this.mapAttribute[34][3] = 1;
        this.mapAttribute[34][1] = 13;
        this.mapAttribute[34][2] = 0;
        this.mapAttribute[34][6] = 0;
        this.mapAttribute[34][7] = 0;
        this.mapAttribute[35][3] = 1;
        this.mapAttribute[35][1] = 14;
        this.mapAttribute[35][2] = 0;
        this.mapAttribute[35][6] = 0;
        this.mapAttribute[35][7] = 0;
        this.mapAttribute[36][3] = 1;
        this.mapAttribute[36][1] = 15;
        this.mapAttribute[36][2] = 0;
        this.mapAttribute[36][6] = 0;
        this.mapAttribute[36][7] = 0;
        this.mapAttribute[37][3] = 1;
        this.mapAttribute[37][1] = 16;
        this.mapAttribute[37][2] = 0;
        this.mapAttribute[37][6] = 0;
        this.mapAttribute[37][7] = 0;
        this.strMessage[1][2] = "\u300c\u30fb\u30fb\u30fb\u30fb\u30fb\u304a\u3044\u30fb\u30fb\u30fb\u300d";
        this.strMessage[0][2] = "\"------ Hey!\"";
        this.strMessage[1][3] = "\u300c\u30fb\u30fb\u30fb\u30fb\u30fb\u304a\u3044\u3063\uff01\u8d77\u304d\u308d\uff01\u300d";
        this.strMessage[0][3] = "\"------ Hey! Wake up!\"";
        this.objectAttribute[87][3] = 1;
        this.objectAttribute[87][1] = 51;
        this.objectAttribute[87][2] = 52;
        this.objectAttribute[87][6] = 360;
        this.objectAttribute[87][7] = 200;
        this.objectAttribute[87][8] = 0;
        this.objectAttribute[87][9] = 240;
        this.objectAttribute[87][5] = 4;
        this.strMessage[1][4] = "\u76d7\u8cca\u300c\u304a\u304a\u7121\u4e8b\u304b\uff01\u304a\u307e\u3048\u3001\u3053\u3053\u306e\u9b54\u5c0e\u5e2b\u306b\u6355\u307e\u3063\u3066\u3053\u306e\u7262\u5c4b\u306b\u5165\u308c\u3089\u308c\u3066\u305f\u3093\u3060\u3088\u3002\u3067\u3001\u4eca\u307e\u3067\u6c17\u3092\u5931\u3063\u3066\u3044\u305f\u8a33\u3060\u3002\u306b\u3057\u3066\u3082\u3001\u304a\u307e\u3048\u904b\u304c\u3044\u3044\u305c\u3002\u3061\u3087\u3046\u3069\u629c\u3051\u7a74\u304c\u5b8c\u6210\u3057\u305f\u3068\u304d\u306b\u6765\u308b\u3093\u3060\u304b\u3089\u306a\u3002\u305d\u3046\u3044\u3046\u8a33\u3067\u4ffa\u306f\u4eca\u304b\u3089\u8131\u8d70\u3059\u308b\u3068\u3053\u308d\u3060\u3002\u304a\u307e\u3048\u3082\u3064\u3044\u3066\u3053\u3044\u3002\u300d";
        this.strMessage[0][4] = "The thief says \"What a relief you're okay!\nYou were caught and thrown into this prison by the Magic Sergeant.\nYou were unconscious when you got here.\nNevertheless, you are so lucky that you just woke up.\nI've finished the escape tunnel. Let's break out.\"";
        this.strMessage[1][5] = "\u76d7\u8cca\u300c\u3088\u3057\u3001\u3058\u3083\u3042\u4ffa\u306f\u5148\u306b\u884c\u304b\u305b\u3066\u3082\u3089\u3046\u305c\u3002\u3042\u3042\u3001\u305d\u308c\u304b\u3089\u304a\u307e\u3048\u306e\u5263\u3068\u76fe\u3001\u3042\u3044\u3064\u3089\u306b\u53d6\u308a\u4e0a\u3052\u3089\u308c\u3061\u307e\u3063\u305f\u307f\u305f\u3044\u3060\u306a\u3002\u3053\u306e\u5854\u306e\u4e2d\u3092\u4e38\u8170\u3067\u6b69\u304d\u56de\u308b\u306e\u306f\u3084\u3081\u305f\u65b9\u304c\u3044\u3044\u3002\u78ba\u304b\uff15\u968e\u306b\u5263\u3001\uff19\u968e\u306b\u76fe\u304c\u3042\u3063\u305f\u306f\u305a\u3060\u304b\u3089\u3001\u307e\u305a\u305d\u308c\u3092\u624b\u306b\u5165\u308c\u308b\u3053\u3068\u3092\u8003\u3048\u308b\u3093\u3060\u306a\u3002\u3058\u3083\u3042\u3001\u307e\u305f\u306a\u3063\uff01\u300d";
        this.strMessage[0][5] = "The thief says \"O.K. Well, excuse my going first. Your weapon and shield were stolen by the guards. It's not wise to wander about without them. I heard that there is a sword on the 5th floor and a shield on the 9th. You had better get them. See you!\"";
        this.strMessage[1][6] = "\u76d7\u8cca\u300c\u3088\u3046\u3063\uff01\u307e\u305f\u4f1a\u3063\u305f\u306a\u3002\u3053\u3053\u306e\u9580\u756a\u3092\u5012\u3057\u3066\u304f\u308c\u3066\u52a9\u304b\u3063\u305f\u305c\u3001\u30c9\u30b8\u3063\u3066\u307e\u305f\u6355\u307e\u3063\u3061\u307e\u3063\u3066\u306a\u3002\u4eca\u5ea6\u306f\u3001\u3053\u3093\u306a\u5965\u306e\u7262\u306b\u9589\u3058\u8fbc\u3081\u3089\u308c\u3061\u307e\u3063\u305f\u3002\u307e\u3042\u3001\u305d\u308c\u306f\u305d\u308c\u3068\u3057\u3066\u3001\uff13\uff15\u968e\u306b\u3044\u308b\u30c9\u30e9\u30b4\u30f3\u306e\u624b\u524d\u307e\u3067\u629c\u3051\u7a74\u3092\u6398\u3063\u3068\u3044\u305f\u3093\u3060\u3002\u958b\u901a\u3055\u305b\u3068\u304f\u304b\u3089\u5148\u306b\u884c\u3063\u3066\u3066\u304f\u308c\u3002\u300d";
        this.strMessage[0][6] = "The thief says \"Ah, we meet again! Thank you. You beat the Gate-Keeper of this area. I was defeated and imprisoned again. Such a small prison this time. I'm making a secret tunnel in front of the Dragon. Go up to 35th floor and wait for me, while I complete the tunnel.\"";
        this.strMessage[1][7] = "\u76d7\u8cca\u300c\u5f8c\u3067\u3061\u3083\u3093\u3068\u884c\u304f\u304b\u3089\uff13\uff15\u968e\u307e\u3067\u5148\u306b\u884c\u3063\u3066\u304a\u3044\u3066\u304f\u308c\u3002\u300d";
        this.strMessage[0][7] = "The thief says \"Don't worry, I'll be there.\"";
        this.objectAttribute[177][5] = 10;
        this.strMessage[1][10] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u300c\u3088\u3046\u3053\u305d\u3001\u300e\u9b54\u6cd5\u306e\u5854\u300f\u3078\u3002\u304a\u307e\u3048\u304c\u3061\u3087\u3046\u3069\uff11\uff10\uff10\u4eba\u76ee\u306e\u4fb5\u5165\u8005\u3060\u3002\u672c\u6765\u306a\u3089\u624b\u4e0b\u5171\u306b\u76f8\u624b\u3092\u3055\u305b\u308b\u3068\u3053\u308d\u3060\u304c\u3001\u7279\u5225\u306b\u3053\u306e\u79c1\u304c\u81ea\u3089\u76f8\u624b\u306b\u306a\u3063\u3066\u3084\u308d\u3046\u3002\u5df1\u306e\u4e0d\u904b\u3092\u546a\u3046\u306e\u3060\u306a\u3002\u300d";
        this.strMessage[0][10] = "The Magic Serg. Zeno says \"Welcome to 'The Magic Tower'. You are the hundredth man who dared to enter my tower. You will now face my guards. Should you happen to survive, I will fight with you in person specially. You should accept your fate.\"";
        this.objectAttribute[178][5] = 11;
        this.strMessage[1][11] = "\u52c7\u8005\u300c\u306a\u3093\u3060\u3063\uff01\uff1f\u3000\u3046\u308f\uff5e\u3063\uff01\uff1f\u300d";
        this.strMessage[0][11] = "The brave man says \"What? Oh!\"";
        this.strMessage[1][13] = "\u30b9\u30b1\u30eb\u30c8\u30f3\uff21\u300c\u3075\u3075\u3075\u3001\u3088\u304f\u3053\u3053\u307e\u3067\u304d\u305f\u306a\u3002\u304b\u304f\u306a\u308b\u4e0a\u306f\u3053\u306e\u4ffa\u69d8\u304c\u3058\u304d\u3058\u304d\u76f8\u624b\u306b\u306a\u3063\u3066\u3084\u308b\u30fb\u30fb\u30fb\u3068\u3044\u3044\u305f\u3044\u3068\u3053\u308d\u3060\u304c\u3001\u307e\u305a\u306f\u8cb4\u69d8\u306e\u529b\u3092\u898b\u305b\u3066\u3082\u3089\u3046\u305e\uff01\u51fa\u4f1a\u3048\uff01\u30b9\u30b1\u30eb\u30c8\u30f3\u5175\u58eb\u305f\u3061\u3088\uff01\u300d";
        this.strMessage[0][13] = "Skeleton A \"Ha ha ha, You are lucky to have gotten so far. Since it has come to this, I shall fight with you personally, but first I must test your strength. Go and fight! Skeleton Soldiers!\"";
        this.strMessage[1][14] = "\u30b9\u30b1\u30eb\u30c8\u30f3\uff21\u300c\u307b\u307b\u3046\u3001\u306a\u304b\u306a\u304b\u30fb\u30fb\u30fb\u3002\u3060\u304c\u3001\u3053\u3053\u304b\u3089\u5148\u3078\u306f\u884c\u304b\u305b\u3093\uff01\u3053\u3053\u3067\u846c\u3063\u3066\u304f\u308c\u308b\u308f\u3063\uff01\u3055\u3042\u3001\u3053\u3044\u3063\uff01\uff01\uff01\u300d";
        this.strMessage[0][14] = "Skeleton A \"How considerably you do. But I will never let you pass. Here, you will die. Fight me!\"";
        this.strMessage[1][15] = "\u30b9\u30b1\u30eb\u30c8\u30f3\uff21\u300c\u3046\u3046\u3046\u30fb\u30fb\u30fb\u3088\u304f\u305e\u3053\u306e\u4ffa\u69d8\u3092\u5012\u305b\u305f\u3082\u306e\u3060\u30fb\u30fb\u30fb\u3002\u3057\u304b\u3057\u3001\u3053\u308c\u304b\u3089\u5148\u306e\u968e\u306f\u3053\u308c\u307e\u3067\u3068\u306f\u6bd4\u3079\u3082\u306e\u306b\u306a\u3089\u3093\u307b\u3069\u5f37\u529b\u306a\u6575\u3068\u30ef\u30ca\u304c\u5f85\u3063\u3066\u3044\u308b\u305e\u3001\u305b\u3044\u305c\u3044\u6c17\u3092\u4ed8\u3051\u308b\u3053\u3068\u3060\u306a\u30fb\u30fb\u30fb\u300d";
        this.strMessage[0][15] = "Skeleton A \"No, It's not possible! You may have defeated me, but beyond this point you must meet some enemies and snares that are powerful beyond anything you've seen. If careless, you will die!\"";
        this.strMessage[1][16] = "\u76d7\u8cca\u300c\u3088\u3063\uff01\u307e\u305f\u3042\u3063\u305f\u306a\u3002\u3059\u3052\u3048\u3058\u3083\u306d\u3048\u304b\u3002\u3053\u3053\u306e\u30d6\u30ed\u30c3\u30af\u306e\u30dc\u30b9\u3092\u5012\u3059\u3068\u306f\u3088\u3002\u4ffa\u3082\u3053\u308c\u4ee5\u4e0a\u3001\u5148\u306e\u968e\u3078\u884c\u3051\u306a\u304f\u3066\u56f0\u3063\u3066\u305f\u3093\u3060\u3002\u3042\u3042\u3001\u3042\u3068\u805e\u3044\u305f\u8a71\u3060\u304c\u3001\uff11\uff11\u968e\u306b\u76fe\u3001\uff11\uff17\u968e\u306b\u5263\u304c\u3042\u308b\u305d\u3046\u3060\u3002\u76fe\u3088\u308a\u3082\u5263\u306e\u65b9\u3092\u5148\u306b\u53d6\u308a\u306b\u884c\u3063\u305f\u65b9\u304c\u3044\u3044\u305d\u3046\u3060\u304b\u3089\u3001\u3046\u307e\u304f\u6575\u3092\u304b\u308f\u3057\u3066\u5263\u3092\u5148\u306b\u53d6\u308a\u306b\u884c\u304f\u3093\u3060\u306a\u3002\u3058\u3083\u3001\u304a\u5148\u306b\uff01\u300d";
        this.strMessage[0][16] = "The thief says \"Hey! We meet again! How greatly you beat the boss of this area. It troubled me that I couldn't go upstairs any more. After I heard that there is a shield on the 11th floor and a sword on the 17th. You had better get a sword first and then a shield. Please excuse my going first!\"";
        this.objectAttribute[88][3] = 1;
        this.objectAttribute[88][1] = 51;
        this.objectAttribute[88][2] = 52;
        this.objectAttribute[88][5] = 17;
        this.strMessage[1][17] = "\u76d7\u8cca\u300c\u3088\u304a\u3063\uff01\u7121\u4e8b\u3060\u3063\u305f\u304b\uff1f\u3053\u3053\u306e\u5927\u30c0\u30b3\u304c\u9053\u3092\u3075\u3055\u3044\u3067\u3044\u3066\u56f0\u3063\u3066\u3044\u305f\u3093\u3060\u304c\u4eca\u3088\u3046\u3084\u304f\u629c\u3051\u7a74\u304c\u5b8c\u6210\u3057\u305f\u3093\u3060\u3002\u304a\u307e\u3048\u3082\u3001\u3053\u3053\u306e\u5927\u30c0\u30b3\u3092\u5012\u3059\u306e\u306f\u5f8c\u56de\u3057\u306b\u3057\u305f\u65b9\u304c\u3044\u3044\u305c\u3002\u3058\u3083\u3042\u3001\u307e\u305f\u306a\u3063\uff01\u300d";
        this.strMessage[0][17] = "The thief says \"Ah! Are you all right? The Big Octopus which lives in here was blocking my progress. Now a loophole has completed at last. You had better put off beating him. See you later!\"";
        this.strMessage[1][18] = "\u300c\u304a\u91d1\u304c\u8db3\u308a\u306a\u3044\u3088\uff01\u300d";
        this.strMessage[0][18] = "\"You don't have enough money.\"";
        this.strMessage[1][19] = "\u30d0\u30f3\u30d1\u30a4\u30a2\u300c\u307b\u307b\u3046\u3001\u8cb4\u69d8\u304b\u3001\u30b9\u30b1\u30eb\u30c8\u30f3\u3092\u5012\u3057\u3066\u4fb5\u5165\u3057\u3066\u304d\u305f\u52c7\u8005\u3068\u3044\u3046\u306e\u306f\u30fb\u30fb\u30fb\u3060\u304c\u3053\u306e\u79c1\u3092\u30b9\u30b1\u30eb\u30c8\u30f3\u5171\u306e\u3088\u3046\u306a\u30b6\u30b3\u3068\u4e00\u7dd2\u306b\u3059\u308b\u306a\u3088\u3002\u4e0d\u6b7b\u306b\u7b49\u3057\u3044\u3053\u306e\u79c1\u306e\u529b\u3092\u898b\u305b\u3066\u3084\u308d\u3046\u3002\u3055\u3042\u3001\u3053\u3044\u3063\uff01\u300d";
        this.strMessage[0][19] = "Vampire \"Well, You beat the skeletons and invaded. Never regard me as small like a skeleton. I will show you that I am as immortal as god. Hey, come on!\"";
        this.strMessage[1][20] = "\u30d0\u30f3\u30d1\u30a4\u30a2\u300c\u3046\u3046\u3046\u30fb\u30fb\u30fb\u3088\u3082\u3084\u3001\u3053\u306e\u79c1\u307e\u3067\u3082\u304c\u6557\u308c\u308b\u3068\u306f\u30fb\u30fb\u30fb\u3069\u3046\u3084\u3089\u8cb4\u69d8\u306e\u529b\u306f\u672c\u7269\u306e\u3088\u3046\u3060\u306a\u30fb\u30fb\u30fb\u3060\u304c\u3001\u305d\u306e\u7a0b\u5ea6\u3067\u306f\u5927\u9b54\u5c0e\u5e2b\u69d8\u306b\u306f\u7d76\u5bfe\u306b\u304b\u306a\u308f\u3093\u305e\u3001\u305b\u3044\u305c\u3044\u675f\u306e\u9593\u52dd\u5229\u306b\u9154\u3044\u3057\u308c\u3066\u3044\u308b\u304c\u3044\u3044\u30fb\u30fb\u30fb\u300d";
        this.strMessage[0][20] = "Vampire \"Good god! I've never dreamed I'd be defeated. There is no doubt of your strength. But you will never win against the Great Magic Master as weak as you are. You shall only celebrate fleeting victory at most.\"";
        this.strMessage[1][21] = "\u5927\u9b54\u5c0e\u5e2b\u300c\u30fb\u30fb\u30fb\u30b8\u30fb\u30fb\u30fb\u30e6\u30a6\u30b7\u30e3\u30fb\u30fb\u30fb\u30fb\u30fb\u30b3\u30ed\u30b9\u30fb\u30fb\u30fb\u300d";
        this.strMessage[0][21] = "Great Magic Master \"-K-I-L-L- -A-N- -I-N-V-A-D-E-R- \"";
        this.strMessage[1][22] = "\u300c\u30fb\u30fb\u30fb\u30b8\u30fb\u30fb\u30fb\u30c8\u30ad\u30cf\u30ad\u30bf\u30ec\u30ea\u30fb\u30fb\u30fb\u30a8\u30e9\u30d0\u30ec\u30b7\u30e2\u30ce\u30e8\u3001\u30b7\u30f2\u30aa\u30bd\u30ec\u30cc\u30ca\u30e9\u30d0\u30b8\u30af\u30a6\u30ce\u30e2\u30f3\u30f2\u30af\u30b0\u30ea\u30c6\u3001\u30ef\u30ac\u30e2\u30c8\u30d8\u30af\u30eb\u30ac\u30e8\u30a4\u30fb\u30fb\u30fb\u300d";
        this.strMessage[0][22] = "\"Now is the time. You were chosen. If you aren't afraid of Death, you should go through the gate of Time and Space, and come to me.\"";
        this.objectAttribute[44][3] = 1;
        this.objectAttribute[44][1] = 57;
        this.objectAttribute[44][2] = 58;
        this.objectAttribute[44][6] = 200;
        this.objectAttribute[44][7] = 240;
        this.objectAttribute[44][8] = 240;
        this.objectAttribute[44][9] = 240;
        this.objectAttribute[44][5] = 23;
        this.strMessage[1][23] = "\u52c7\u8005\u300c\u3053\u308c\u306f\u3063\u2026\u2026\uff01\u4eba\u5f62\u3060\u3063\uff01\u300d";
        this.strMessage[0][23] = "The brave man says \"Oh! What? This is a doll!\"";
        this.strMessage[1][24] = "\u76d7\u8cca\u300c\u3042\u3063\uff01\u307e\u3060\u629c\u3051\u7a74\u3001\u5b8c\u6210\u3057\u3066\u306a\u304b\u3063\u305f\u306e\u306b\u30fb\u30fb\u30fb\u3082\u3046\u5c11\u3057\u5f85\u3063\u3066\u308c\u3070\u30a2\u30a4\u30c6\u30e0\u3092\u4f7f\u308f\u305a\u306b\u3059\u3093\u3060\u306f\u305a\u3060\u305e\u3002\u4e88\u5b9a\u304c\u72c2\u3063\u3061\u307e\u3046\u306a\u30fb\u30fb\u30fb\u3044\u3084\u3001\u6c17\u306b\u3057\u306a\u3044\u3067\u304f\u308c\u3002\u300d";
        this.strMessage[0][24] = "The thief says \"The tunnel has not been completed yet. You should have waited a little longer, and you should not have used items. I had a bug in the program. There! Don't worry!\"";
        this.strMessage[1][25] = "\u76d7\u8cca\u300c\u3042\u3042\u3001\u3084\u3063\u3068\u629c\u3051\u7a74\u304c\u5b8c\u6210\u3057\u305f\u3002\u3042\u308c\uff1f\u307e\u305f\u304a\u524d\u304b\u3002\u3044\u3044\u30bf\u30a4\u30df\u30f3\u30b0\u3067\u304d\u305f\u306a\u3002\u307e\u305f\u629c\u3051\u7a74\u4f5c\u3063\u3068\u3044\u305f\u305c\u3002\u81ea\u7531\u306b\u4f7f\u3063\u3066\u304f\u308c\u3002\u300d";
        this.strMessage[0][25] = "The thief says \"Oh, I have finished the tunnel. What? It's you again. You came at a good time. I have openned a tunnel, and you may use it freely.\"";
        this.strMessage[1][26] = "\u76d7\u8cca\u300c\u3053\u306e\u30d6\u30ed\u30c3\u30af\u306b\u6700\u5f8c\u306e\u30dc\u30b9\u3068\u6355\u307e\u3063\u305f\u30d7\u30ea\u30f3\u30bb\u30b9\u304c\u3044\u308b\u306f\u305a\u3060\u304c\u3001\u4eca\u306f\u307e\u3060\u6226\u3046\u306e\u306f\u65e9\u3059\u304e\u308b\u3060\u308d\u3046\u306a\u3002\u300d";
        this.strMessage[0][26] = "The thief says \"The last boss and the captured princess must be in this area. Hmm, I wonder if we should wait before fighting him.\"";
        this.strMessage[1][27] = "\u91d1\u9a0e\u58eb\u300c\u8cb4\u69d8\u3060\u306a\u3001\u7b2c\uff11\u3001\u7b2c\uff12\u30d6\u30ed\u30c3\u30af\u306e\u30dc\u30b9\u3092\u5012\u3057\u767b\u3063\u3066\u304d\u305f\u52c7\u8005\u3068\u3044\u3046\u306e\u306f\u3002\u3060\u304c\u305d\u308c\u3082\u3001\u3053\u3053\u3067\u7d42\u308f\u308a\u3060\uff01\u3053\u3053\u306e\u30d6\u30ed\u30c3\u30af\u306e\u30dc\u30b9\u3067\u3042\u308b\u79c1\u304c\u81ea\u3089\u8cb4\u69d8\u306e\u9996\u3092\u4e0a\u3052\u3066\u3084\u308b\u308f\u3063\uff01\u899a\u609f\u3057\u308d\u3063\uff01\u300d";
        this.strMessage[0][27] = "The Golden Knight says \"You are a brave man beating the bosses of the first and second areas, and ascending the tower. But the game is over now. Here and Now, I will beat you for myself! Give up!\"";
        this.strMessage[1][28] = "\u91d1\u9a0e\u58eb\u300c\u3046\u3046\u3046\u2026\u2026\u4eca\u56de\u306f\u3053\u306e\u3050\u3089\u3044\u306b\u3057\u3066\u304a\u3044\u3066\u3084\u308b\u2026\u2026\uff14\uff10\u968e\u307e\u3067\u767b\u3063\u3066\u3053\u308c\u305f\u3089\u4eca\u5ea6\u306f\u672c\u6c17\u3067\u76f8\u624b\u3092\u3057\u3066\u3084\u308b\u304b\u3089\u306a\u3063\uff01\u899a\u3048\u3066\u304a\u3051\u3063\uff01\u300d\"";
        this.strMessage[0][28] = "The Golden Knight says \"You think you're pretty strong, huh? If you can make it to the 40th floor, I shall fight with you again. There, you will die!";
        this.strMessage[1][29] = "\u76d7\u8cca\u300c\u304a\u304a\u3001\u6765\u305f\u304b\u3002\u3061\u3083\u3093\u3068\u3001\u629c\u3051\u7a74\u3092\u958b\u901a\u3055\u305b\u3066\u304a\u3044\u305f\u305c\u3001\u3053\u306e\u629c\u3051\u7a74\u3092\u901a\u308c\u3070\u30c9\u30e9\u30b4\u30f3\u306e\u5f8c\u308d\u306b\u51fa\u3089\u308c\u308b\u304b\u3089\u3001\u305d\u3053\u304b\u3089\u4e0a\u306e\u968e\u306b\u884c\u304f\u3093\u3060\u306a\u3002\u300d";
        this.strMessage[0][29] = "The thief says \"There you are. I have just finished the tunnel. As you go through it, you will get to the Dragon. And then you should go up.\"";
        this.strMessage[1][30] = "\u76d7\u8cca\u300c\u3053\u306e\u30d6\u30ed\u30c3\u30af\u306e\u30dc\u30b9\u306e\u91d1\u9a0e\u58eb\u306f\u5f31\u3044\u304f\u305b\u306b\u614b\u5ea6\u3060\u3051\u306f\u3067\u304b\u3044\u304b\u3089\u3001\u3053\u306e\u5854\u306e\u526f\u5c06\u683c\u306e\u9b54\u5c0e\u5e2b\u30bc\u30ce\u306b\u306f\u5acc\u308f\u308c\u3066\u3044\u308b\u3089\u3057\u3044\u3002\u300d";
        this.strMessage[0][30] = "The thief says \"The Golden Knight (who is the boss of this area) has a strong attitude in spite of being weak. It is for this reason that he is disliked by the Magic Serg. Zeno, who is the sub commander of this tower.\"";
        this.strMessage[1][31] = "\u91d1\u9a0e\u58eb\u300c\u3088\u304f\u304d\u305f\u306a\u3002\u4eca\u5ea6\u306f\u3055\u3063\u304d\u306e\u69d8\u306a\u8a33\u306b\u306f\u3044\u304b\u3093\u305e\uff01\u3053\u306e\u5c48\u8fb1\u306f\uff11\uff10\u500d\u306b\u3057\u3066\u8fd4\u3057\u3066\u304f\u308c\u308b\u308f\u3063\uff01\u6b7b\u970a\u5175\u58eb\u7a81\u6483\uff01\u300d";
        this.strMessage[0][31] = "The Golden Knight says \"I wonder how you were able to come so far. I will make sure you go no further. I will humiliate you 10 times as much as you've disgraced this tower. Ghost Soldiers, charge!\"";
        this.strMessage[1][32] = "\u91d1\u9a0e\u58eb\u300c\u3075\u3075\u3093\u3001\u3053\u3093\u306a\u306e\u306f\u5c0f\u624b\u8abf\u3079\u3060\u3063\uff01\u5175\u58eb\u7a81\u6483\uff01\u300d";
        this.strMessage[0][32] = "The Golden Knight says \"Humph, that was nothing! Soldiers, charge!\"";
        this.strMessage[1][33] = "\u91d1\u9a0e\u58eb\u300c\u307e\u3060\u307e\u3060\u3001\u3053\u308c\u304b\u3089\u3063\uff01\u5263\u58eb\u7a81\u6483\uff01\u300d";
        this.strMessage[0][33] = "The Golden Knight says \"We are only beginning. Let's fight from now on. Swordsmen, charge!\"";
        this.strMessage[1][34] = "\u91d1\u9a0e\u58eb\u300c\u3046\u306c\u306c\u2026\u2026\u3060\u304c\u3001\u3053\u308c\u306f\u3069\u3046\u3060\u3063\uff01\u9a0e\u58eb\u7a81\u6483\uff01\u300d";
        this.strMessage[0][34] = "The Golden Knight says \"Heck! How about this attack? Knights, charge!\"";
        this.strMessage[1][35] = "\u91d1\u9a0e\u58eb\u300c\u3046\u3046\u2026\u2026\u79c1\u306e\u90e8\u4e0b\u9054\u3092\u2026\u2026\u8a31\u3055\u3093\u3063\uff01\u8a31\u3055\u3093\u305e\uff01\u4eca\u5ea6\u306f\u624b\u52a0\u6e1b\u306f\u3057\u3066\u3084\u3089\u3093\u3063\uff01\u899a\u609f\u3057\u308d\uff01\u300d";
        this.strMessage[0][35] = "The Golden Knight says \"How dare you defeat my followers? Never shall I forgive you! Now I won't use discretion. Give up!\"";
        this.strMessage[1][36] = "\u91d1\u9a0e\u58eb\u300c\u3054\u307b\u3063\u2026\u2026\u4eca\u56de\u306f\u3053\u306e\u3078\u3093\u3067\u2026\u2026\u306f\u3042\u306f\u3042\u2026\u2026\u8a31\u3057\u3066\u304a\u3044\u3066\u3084\u308b\u2026\u2026\u3002\u3060\u304c\u6b21\u306b\u3084\u308b\u6642\u306f\u4eca\u5ea6\u3053\u305d\u672c\u5f53\u306b\u672c\u6c17\u3067\u76f8\u624b\u3092\u3057\u3066\u3084\u308b\u304b\u3089\u306a\u3063\uff01\u899a\u609f\u3057\u3066\u304a\u3051\u3063\uff01\u300d";
        this.strMessage[0][36] = "The Golden Knight says \"I will unwillingly forgive you this time. But we shall quarrel seriously when we meet again. You had better give up!\"";
        this.strMessage[1][37] = "\u91d1\u9a0e\u58eb\u300c\u3042\u3063\u2026\u2026\uff01\u30bc\u30ce\u69d8\u2026\u2026\u3002\u3042\u3068\u4e00\u6b69\u3068\u3044\u3046\u6240\u3067\u3001\u52c7\u8005\u3092\u53d6\u308a\u9003\u304c\u3057\u3066\u3057\u307e\u3044\u307e\u3057\u305f\u3002\u3069\u3046\u304b\u3001\u304a\u8a31\u3057\u3092\u2026\u2026\u3002\u300d";
        this.strMessage[0][37] = "The Golden Knight says \"Oh! Sir Magic Serg. Zeno. I was not able to catch the brave man. Please forgive me.\"";
        this.strMessage[1][38] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u300c\u53d6\u308a\u9003\u304c\u3057\u305f\u3060\u3068\u2026\u2026\uff1f\u9003\u3052\u3066\u304d\u305f\u306e\u306f\u8cb4\u69d8\u306e\u65b9\u3067\u306f\u306a\u3044\u304b\u3063\uff01\u3053\u306e\u6065\u77e5\u3089\u305a\u3081\u304c\u3063\uff01\u8cb4\u69d8\u306e\u3088\u3046\u306a\u81c6\u75c5\u8005\u306f\u3053\u306e\u5854\u306b\u306f\u4e0d\u8981\u3060\u3063\uff01\u3053\u3053\u3067\u3001\u6b7b\u306d\u3063\uff01\u300d";
        this.strMessage[0][38] = "The Magic Serg. Zeno replies \"You weren't? I dare you to say that again. You come running up here like a coward and tell me you couldn't do your job. What shame! This tower has no need for the likes of you! You've failed me for the last time. You shall now die.\"";
        this.strMessage[1][39] = "\u91d1\u9a0e\u58eb\u300c\u3042\u3042\u3001\u3069\u3046\u304b\u3001\u304a\u8a31\u3057\u2026\u2026\u304e\u3083\u3042\uff5e\uff5e\uff5e\u3063\uff01\uff01\uff01\u300d";
        this.strMessage[0][39] = "The Golden Knight says \"Oh God, please forgive me! Ah!\"";
        this.strMessage[1][40] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u300c\u304a\u898b\u82e6\u3057\u3044\u3068\u3053\u308d\u3092\u304a\u898b\u305b\u3057\u305f\u306a\u2026\u2026\u3002\u3060\u304c\u3001\u5b89\u5fc3\u3057\u3066\u3082\u3089\u304a\u3046\u3002\u79c1\u306f\u3053\u306e\u3088\u3046\u306a\u30b4\u30df\u3068\u306f\u308f\u3051\u304c\u9055\u3046\u3002\u3082\u3057\u3001\u304a\u524d\u304c\u4e0a\u307e\u3067\u767b\u3063\u3066\u3053\u308c\u305f\u306a\u3089\u4eca\u5ea6\u306f\u3001\u79c1\u304c\u76f4\u3005\u306b\u304a\u76f8\u624b\u3057\u3088\u3046\u3002\u5f85\u3063\u3066\u3044\u308b\u305e\u2026\u2026\u3002\u300d";
        this.strMessage[0][40] = "The Magic Serg. Zeno says \"I behaved unbecomingly. But don't worry. I quite different from such a fellow. If you should come up to me, I would fight with you directly. I'm waiting for you.\"";
        this.strMessage[1][41] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u300c\u3088\u304f\u305e\u3001\u3053\u3053\u307e\u3067\u3001\u305f\u3069\u308a\u3064\u3044\u305f\u3082\u306e\u3060\u3002\u8a89\u3081\u3066\u3084\u308d\u3046\u3002\u7d04\u675f\u3069\u304a\u308a\u3001\u3053\u306e\u79c1\u304c\u76f4\u3005\u306b\u76f8\u624b\u3092\u3057\u3088\u3046\u3002\u3055\u3042\u3001\u6765\u308b\u304c\u3044\u3044\u3002\u300d";
        this.strMessage[0][41] = "The Magic Serg. Zeno \"It's amazing that you found your way here at last. I compliment you. Now, as promised, I'll fight with you, man to man!\"";
        this.strMessage[1][42] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u300c\u3046\u3063\u2026\u2026\u3053\u306e\u9663\u5f62\u306f\u2026\u2026\u307e\u305a\u3044\u3063\uff01\u300d";
        this.strMessage[0][42] = "The Magic Serg. Zeno \"Alas...\"";
        this.strMessage[1][43] = "\u52c7\u8005\u300c\u304a\u307e\u3048\u306f\u3063\u2026\u2026\uff01\u3069\u3046\u3057\u3066\u3053\u3093\u306a\u6240\u306b\uff01\u300d";
        this.strMessage[0][43] = "The brave man says \"Who? It's you! Why are you in such a place ?\"";
        this.strMessage[1][44] = "\u76d7\u8cca\u300c\u3075\u3075\u3075\u2026\u2026\u3053\u3053\u306b\u3044\u308b\u3068\u3044\u3046\u4e8b\u306f\u3001\u7b54\u3048\u306f\uff11\u3064\u3057\u304b\u3042\u308b\u307e\u3044\u3002\u3053\u3046\u3044\u3046\u4e8b\u3060\u3063\uff01\u300d";
        this.strMessage[0][44] = "The thief says \"Humph. There is only one reason why I'm here. And this is it!\"";
        this.strMessage[1][45] = "\u52c7\u8005\u300c\u3042\u3063\uff01\u304a\u307e\u3048\u306f\u30bc\u30ce\u30c3\uff01\u751f\u304d\u3066\u3044\u305f\u306e\u304b\uff01\uff1f\u300d";
        this.strMessage[0][45] = "The brave man says \"Huh? Hey! You're Zeno! Were you still alive ?\"";
        this.strMessage[1][46] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u300c\u3042\u3093\u306a\u3053\u3068\u3067\u5012\u3055\u308c\u308b\u3082\u306e\u304b\u3002\u3042\u308c\u306f\u3001\u304a\u307e\u3048\u306e\u6226\u58eb\u3068\u3057\u3066\u306e\u77e5\u6027\u3092\u8a66\u3057\u305f\u306b\u3059\u304e\u3093\u3002\u300d";
        this.strMessage[0][46] = "The Magic Serg. Zeno says \"I will never die. I merely tested your intelligence as a soldier.\"";
        this.strMessage[1][47] = "\u52c7\u8005\u300c\u306a\u306b\u3063\uff01\uff1f\u2026\u2026\u3069\u3046\u3044\u3046\u3053\u3068\u3060\u3063\uff01\u3069\u3046\u3057\u3066\u3001\u3053\u3093\u306a\u4e8b\u3092\u2026\u2026\uff01\uff1f\u300d";
        this.strMessage[0][47] = "The brave man says \"Huh? What do you mean? Why did you do such a thing ?\"";
        this.strMessage[1][48] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u300c\u304a\u307e\u3048\u306e\u6301\u3064\u795e\u5263\u30a6\u30a7\u30dd\u30ca\u30fc\u3001\u305d\u3057\u3066\u79c1\u306e\u6301\u3064\u5168\u80fd\u306e\u6756\u30a4\u30f3\u30c6\u30ea\u30aa\u30f3\u3002\u3053\u306e\uff12\u3064\u306e\u529b\u304c\u5408\u308f\u3055\u308b\u6642\u3001\u5049\u5927\u306a\u308b\u77e5\u6075\u3092\u624b\u306b\u5165\u308c\u308b\u4e8b\u304c\u3067\u304d\u308b\u3068\u3044\u3046\u2026\u2026\u3002\u3057\u304b\u3057\u3001\u305d\u308c\u306b\u306f\u3001\u305d\u306e\u5263\u306e\u529b\u3092\u5341\u5206\u306b\u767a\u63ee\u3067\u304d\u308b\u80fd\u529b\u3092\u6301\u3063\u305f\u6226\u58eb\u304c\u5fc5\u8981\u3068\u306a\u308b\u306e\u3060\u3002\u300d";
        this.strMessage[0][48] = "The Magic Serg. Zeno says \"The Sacred Sword 'Weaponer' which you have and The Omniscient Staff 'Intellion' which I have, Legend says that whoever unites the two will recieve great wisdom. But to this end, it must be assured that the soldier who does so can handle the the power of that sword.\"";
        this.strMessage[1][49] = "\u52c7\u8005\u300c\u305d\u306e\u6226\u58eb\u304c\u4ffa\u3060\u3068\u3044\u3046\u306e\u304b\u2026\u2026\uff01\uff1f\u300d";
        this.strMessage[0][49] = "The brave man says \"What are you saying... Am I the soldier ?\"";
        this.strMessage[1][50] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u300c\u305d\u3046\u3060\u2026\u2026\u3057\u304b\u3057\u3001\u304a\u307e\u3048\u306e\u6280\u91cf\u306f\u305d\u306e\u795e\u5263\u30a6\u30a7\u30dd\u30ca\u30fc\u3092\u4f7f\u3044\u3053\u306a\u3059\u306b\u306f\u5341\u5206\u3067\u306f\u306a\u304b\u3063\u305f\u3002\u3060\u304b\u3089\u3001\u79c1\u306f\u507d\u308a\u306e\u60c5\u5831\u3092\u6d41\u3057\u3001\u69d8\u3005\u306a\u30ef\u30ca\u3092\u3053\u306e\u5854\u306b\u3057\u304b\u3051\u3001\u304a\u307e\u3048\u304c\u6765\u308b\u306e\u3092\u5f85\u3063\u3066\u3044\u305f\u306e\u3060\u3002\u305d\u3057\u3066\u3001\u4e88\u5b9a\u901a\u308a\u3001\u304a\u307e\u3048\u306f\u795e\u5263\u3092\u6271\u3046\u306e\u306b\u5341\u5206\u306a\u529b\u3092\u8eab\u306b\u3064\u3051\u3066\u3053\u3053\u307e\u3067\u6765\u305f\u3002\u300d";
        this.strMessage[0][50] = "The Magic Serg. Zeno says \"Yes. But when you came here, your ability wasn't sufficient to master the sacred sword 'Weaponer'.\"For that reason, I gave false information, set various traps in this tower, and waited for you to come. You came to here master the power enough to using the sacred sword as arranged beforehand.";
        this.strMessage[1][51] = "\u52c7\u8005\u300c\u3067\u306f\u3001\u59eb\u304c\u3055\u3089\u308f\u308c\u305f\u3068\u3044\u3046\u60c5\u5831\u3082\u3001\u4ffa\u3092\u3053\u3053\u307e\u3067\u3001\u304a\u3073\u304d\u5bc4\u305b\u308b\u70ba\u306e\u30ef\u30ca\u3060\u3063\u305f\u3068\u3044\u3046\u306e\u304b\u3063\uff01\uff1f\u300d";
        this.strMessage[0][51] = "The brave man replies \"Well, this means that the rumour that a princess was trapped here... was actually a lie in order to get me here, wasn't it ?\"";
        this.strMessage[1][52] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u300c\u305d\u306e\u901a\u308a\u3060\u3002\u305d\u3057\u3066\u3001\u5f8c\u306f\u79c1\u304c\u304a\u307e\u3048\u306e\u529b\u3092\u53d6\u308a\u3053\u3081\u3070\u3001\u3053\u306e\u8336\u756a\u5287\u3082\u7d42\u308f\u308a\u3068\u306a\u308b\u2026\u2026\u3002\u6642\u306f\u6765\u305f\u308c\u308a\u2026\u2026\u6211\u5168\u80fd\u306a\u308b\u529b\u3092\u7528\u3044\u3066\u3001\u795e\u5263\u3092\u7815\u304d\u5049\u5927\u306a\u308b\u77e5\u6075\u3092\u624b\u306b\u5165\u308c\u3093\u2026\u2026\u3002\u3086\u304f\u305e\u3063\uff01\u795e\u5263\u306e\u6226\u58eb\u3088\uff01\u300d";
        this.strMessage[0][52] = "The Magic Serg. Zeno says \"Yes, that's right. And now, if we can work together, this farce will end. Now is the time to act. Using omniscient power, We shall break the sacred sword and recieve great enlightenment. Soldier of the Sacred Sword! Let's finish this!\"";
        this.objectAttribute[138][3] = 1;
        this.objectAttribute[138][1] = 55;
        this.objectAttribute[138][2] = 56;
        this.objectAttribute[138][5] = 53;
        this.strMessage[1][53] = "\u300c\u308f\u3057\u304c\u8a00\u3046\u3053\u3068\u306f\u4f55\u3082\u306a\u3044\u3002\u3053\u306e\u968e\u306b\u3001\u3042\u308b\u30e1\u30c3\u30bb\u30fc\u30b8\u304c\u96a0\u3055\u308c\u3066\u3044\u308b\u3058\u3083\u308d\u3046\u3002\u300d";
        this.strMessage[0][53] = "\"I have nothing to say. A certain message may be hidden in this room.\"";
        this.strMessage[1][54] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u300c\u30b4\u30db\u30c3\uff01\u304a\u306e\u308c\u3001\u3053\u306e\u79c1\u304c\u5012\u3055\u308c\u308b\u3068\u306f\u2026\u2026\u3001\u3057\u304b\u3057\u3053\u308c\u3050\u3089\u3044\u3067\u6b7b\u306c\u3088\u3046\u306a\u79c1\u3067\u306f\u306a\u3044\uff01\u304a\u306c\u3057\u3068\u3082\u3046\u4e00\u5ea6\u3001\u6226\u3046\u65e5\u304c\u6765\u308b\u3053\u3068\u3092\u697d\u3057\u307f\u306b\u5f85\u3063\u3066\u3044\u308b\u305e\uff01\u300d";
        this.strMessage[0][54] = "The Magic Serg. Zeno says \"You villain. Little did I expect to be beaten. But I would never die in such a way. I'll be looking forward to fighting with you again.\"";
        this.objectAttribute[175][3] = 1;
        this.objectAttribute[175][1] = 55;
        this.objectAttribute[175][2] = 56;
        this.objectAttribute[175][5] = 55;
        this.strMessage[1][55] = "\u300c\u3053\u306e\u5854\u306b\u306f\u9375\u3067\u958b\u3051\u3089\u308c\u308b\u6249\u306e\u307b\u304b\u306b \u201d\u9580\u201d \u3068\u3044\u3046\u3082\u306e\u304c\u3042\u3063\u3066\u3001\u3053\u308c\u306f\u305d\u306e\u9580\u3092\u5b88\u3063\u3066\u3044\u308b\u30e2\u30f3\u30b9\u30bf\u30fc\u3092\u5012\u3055\u306a\u3051\u308c\u3070\u3042\u304b\u306a\u3044\u3058\u3083\u308d\u3046\u3002\u300d";
        this.strMessage[0][55] = "\"There are doors which cannot be openned by a key. You can open these doors by beating the monsters which guard them.\"";
        this.objectAttribute[42][3] = 1;
        this.objectAttribute[42][1] = 55;
        this.objectAttribute[42][2] = 56;
        this.objectAttribute[42][6] = 120;
        this.objectAttribute[42][7] = 240;
        this.objectAttribute[42][8] = 160;
        this.objectAttribute[42][9] = 240;
        this.objectAttribute[42][5] = 56;
        this.strMessage[1][56] = "\u300c\u5546\u4eba\u304b\u3089\u7269\u3092\u8cb7\u3046\u3068\u3001\u3042\u3068\u3067\u91cd\u8981\u306a\u60c5\u5831\u3092\u805e\u304f\u3053\u3068\u304c\u3067\u304d\u308b\u3058\u3083\u308d\u3046\u3002\u300d";
        this.strMessage[0][56] = "\"If you buy goods from merchants, you will be able to hear important information later.\"";
        this.objectAttribute[40][3] = 1;
        this.objectAttribute[40][1] = 49;
        this.objectAttribute[40][2] = 50;
        this.objectAttribute[40][5] = 57;
        this.strMessage[1][57] = "\u300c\u3053\u306e\u5854\u306f\u5168\u90e8\u3067\uff15\uff10\u968e\u5efa\u3066\u3067\u3001\uff11\uff10\u968e\u3054\u3068\u306b\uff11\u3064\u306e\u30d6\u30ed\u30c3\u30af\u3092\u5f62\u6210\u3057\u3066\u3044\u308b\u3002\u5854\u306e\u5185\u90e8\u306b\u306f\u3001\u5404\u30d6\u30ed\u30c3\u30af\u3092\u7d71\u62ec\u3059\u308b\u30dc\u30b9\u304c\u914d\u7f6e\u3055\u308c\u3066\u3044\u3066\u3001\u305d\u3044\u3064\u3089\u3092\u5012\u3055\u306a\u3044\u3053\u3068\u306b\u306f\u3001\u305d\u308c\u3088\u308a\u4e0a\u306e\u968e\u306b\u884c\u304f\u3053\u3068\u306f\u3067\u304d\u306a\u3044\u3060\u308d\u3046\u3002\u300d";
        this.strMessage[0][57] = "\"This tower has fifty floor. Every ten floor form one area. The boss who controls each area, are posted in this tower. You cannot ascend from there if you don't beat them.\"";
        this.objectAttribute[155][3] = 1;
        this.objectAttribute[155][1] = 49;
        this.objectAttribute[155][2] = 50;
        this.objectAttribute[155][5] = 58;
        this.strMessage[1][58] = "\u300c\u796d\u58c7\u306b\u5bc4\u9032\u3057\u305f\u3068\u304d\u306f\u3001\u653b\u6483\u529b\u3088\u308a\u3082\u9632\u5fa1\u529b\u3092\u4e3b\u306b\u4e0a\u3052\u3066\u3082\u3089\u3063\u305f\u65b9\u304c\u3044\u3044\u3067\u3057\u3087\u3046\u3002\u305f\u3060\u3057\u3001\u653b\u6483\u529b\u3092\u307e\u3063\u305f\u304f\u4e0a\u3052\u306a\u3044\u3068\u3001\u3042\u3068\u3067\u5012\u305b\u306a\u3044\u6575\u304c\u3067\u3066\u304f\u308b\u304b\u3082\u3057\u308c\u306a\u3044\u3088\u3002\u300d";
        this.strMessage[0][58] = "\"When you offer gold at an alter, you may as well have your defensive power risen rather than your offensive power. The enemy whom you cannot beat may appear, provided you won't raise your offensive power.\"";
        this.objectAttribute[157][3] = 1;
        this.objectAttribute[157][1] = 49;
        this.objectAttribute[157][2] = 50;
        this.objectAttribute[157][5] = 59;
        this.strMessage[1][59] = "\u300c\uff19\u968e\u3068\uff11\uff16\u968e\u3068\uff11\uff18\u968e\u306e\u629c\u3051\u7a74\u306b\u306f\u6c17\u304c\u4ed8\u3044\u305f\u304b\u3044\uff1f\u300d";
        this.strMessage[0][59] = "\"Did you notice the secret passages on the 9th, 16th, and 18th floors?\"";
        this.objectAttribute[160][3] = 1;
        this.objectAttribute[160][1] = 49;
        this.objectAttribute[160][2] = 50;
        this.objectAttribute[160][5] = 60;
        this.strMessage[1][60] = "\u300c\u5341\u5b57\u67b6\u3092\u6301\u3063\u3066\u3044\u308c\u3070\u3001\u30be\u30f3\u30d3\u3084\u30d0\u30f3\u30d1\u30a4\u30a2\u306b\u5bfe\u3059\u308b\u653b\u6483\u529b\u304c\uff12\u500d\u306b\u306a\u308b\u3002\u7279\u306b\u30d0\u30f3\u30d1\u30a4\u30a2\u306f\u5341\u5b57\u67b6\u3092\u6301\u3063\u3066\u3044\u306a\u3044\u3068\u5012\u305b\u306a\u3044\u3060\u308d\u3046\u3002\u3053\u308c\u3088\u308a\u4e0a\u306e\u968e\u306e\u3069\u3053\u304b\u306b\u3042\u308b\u3089\u3057\u3044\u304c\u2026\u2026\u3002\u300d";
        this.strMessage[0][60] = "\"If you carry a cross, the strength of Zombies and Vampires will be cut in half. It is near impossible to defeat them without a cross, especially Vampires. A cross is on a floor higher than this one.\"";
        this.objectAttribute[43][3] = 1;
        this.objectAttribute[43][1] = 55;
        this.objectAttribute[43][2] = 56;
        this.objectAttribute[43][5] = 61;
        this.strMessage[1][61] = "\u300c\u3053\u306e\u30d6\u30ed\u30c3\u30af\u3067\u306f\u8d64\u3044\u9375\u306f\uff12\u30f6\u6240\u3067\u624b\u306b\u5165\u308b\u305d\u3046\u3058\u3083\u3002\u300d";
        this.strMessage[0][61] = "\"I heard that you can find a red key at two places in this area.\"";
        this.objectAttribute[139][3] = 1;
        this.objectAttribute[139][1] = 55;
        this.objectAttribute[139][2] = 56;
        this.objectAttribute[139][5] = 62;
        this.strMessage[1][62] = "\u300c\u3053\u306e\u30d6\u30ed\u30c3\u30af\u3067\u306f\u3001\u796d\u58c7\u3067\u653b\u6483\u529b\u3092\u4f55\u56de\u304b\u4e0a\u3052\u3066\u3082\u3089\u308f\u306a\u3044\u3068\u30ed\u30c3\u30af\u3068\u3044\u3046\u30e2\u30f3\u30b9\u30bf\u30fc\u304c\u5012\u305b\u306a\u304f\u306a\u3063\u3066\u3057\u307e\u3046\u304b\u3082\u3057\u308c\u3093\u3002\u6ce8\u610f\u3059\u308b\u306e\u3058\u3083\u3002\u300d";
        this.strMessage[0][62] = "\"In this area, if you don't raise your offensive power at an altar a few times, you may not be able to beat 'Rock' monsters. Be careful!\"";
        this.objectAttribute[140][3] = 1;
        this.objectAttribute[140][1] = 55;
        this.objectAttribute[140][2] = 56;
        this.objectAttribute[140][5] = 63;
        this.strMessage[1][63] = "\u300c\u3053\u306e\u30d6\u30ed\u30c3\u30af\u306b\u3001\u3053\u306e\u9b54\u6cd5\u306e\u5854\u306e\u4e3b\u3067\u3042\u308b\u5927\u9b54\u5c0e\u5e2b\u304c\u3044\u308b\u304c\u3001\u4eca\u306e\u304a\u307e\u3048\u3055\u3093\u3067\u306f\u6226\u3063\u3066\u3082\u6b7b\u306b\u306b\u884c\u304f\u3088\u3046\u306a\u3082\u306e\u3058\u3083\u308d\u3046\u3002\u3068\u308a\u3042\u3048\u305a\u3001\u3046\u307e\u304f\u3084\u308a\u3059\u3054\u3057\u3066\u4e0a\u306e\u30d6\u30ed\u30c3\u30af\u306b\u884c\u304f\u306e\u304c\u6b63\u89e3\u3058\u3083\u3002\u300d";
        this.strMessage[0][63] = "\"The Great Magic Master is in this area. He is a proprietor of this magic tower. At your strenght, to attack him means death. It stands to reason that you should not face him, but rather, get items on higher levels first.\"";
        this.objectAttribute[141][3] = 1;
        this.objectAttribute[141][1] = 55;
        this.objectAttribute[141][2] = 56;
        this.objectAttribute[141][5] = 64;
        this.strMessage[1][64] = "\u300c\u3053\u306e\u968e\u307e\u3067\u6765\u305f\u6bb5\u968e\u3067\u3001\u751f\u547d\u529b\uff11\uff15\uff10\uff10\u3001\u653b\u6483\u529b\uff18\uff10\u3001\u9632\u5fa1\u529b\uff19\uff18\u3001\u9375\uff15\u500b\u3001\u7d2b\u306e\u9375\u304c\uff11\u500b\u3042\u308c\u3070\u3001\u307b\u307c\u7406\u60f3\u7684\u3068\u8a00\u3048\u308b\u3058\u3083\u308d\u3046\u3002\u300d";
        this.strMessage[0][64] = "\"In the stage of this floor, if your strength is 1500, offensive power is 80, defensive power is 98, you have five keys, and one blue key, you are almost ideal.\"";
        this.objectAttribute[142][3] = 1;
        this.objectAttribute[142][1] = 55;
        this.objectAttribute[142][2] = 56;
        this.objectAttribute[142][5] = 65;
        this.strMessage[1][65] = "\u300c\u4e8c\u5200\u6d41\u306e\u5263\u58eb\u306f\u653b\u6483\u529b\u304c\u3082\u306e\u3059\u3054\u304f\u9ad8\u3044\u3002\u307e\u3068\u3082\u306b\u6226\u3048\u3070\u5927\u304d\u306a\u30c0\u30e1\u30fc\u30b8\u3092\u53d7\u3051\u308b\u3060\u308d\u3046\u3002\u4e00\u6483\u3067\u5012\u305b\u308b\u3088\u3046\u306b\u306a\u308b\u307e\u3067\u3001\u6226\u308f\u306a\u3044\u65b9\u304c\u3088\u304b\u308d\u3046\u3002\u300d";
        this.strMessage[0][65] = "\"The offensive power of the swordsman who uses two swords is too high. He can use two swords at the same time. You will lose much strength if you fight him normally. You should never fight him before your attacks are stronger than his.\"";
        this.objectAttribute[163][3] = 1;
        this.objectAttribute[163][1] = 49;
        this.objectAttribute[163][2] = 50;
        this.objectAttribute[163][5] = 66;
        this.strMessage[1][66] = "\u300c\u3053\u306e\u5854\u306f\uff15\uff10\u968e\u5efa\u3066\u3060\u304c\u3001\u5b9f\u969b\u306b\u306f\uff14\uff19\u968e\u307e\u3067\u3057\u304b\u884c\u3051\u306a\u3044\u3088\u3046\u3060\u3002\u300d";
        this.strMessage[0][66] = "\"This tower is 50 stories high, but in reality it seems that you cannot go up to the 50th floor.\"";
        this.objectAttribute[143][3] = 1;
        this.objectAttribute[143][1] = 55;
        this.objectAttribute[143][2] = 56;
        this.objectAttribute[143][5] = 67;
        this.strMessage[1][67] = "\u300c\u6025\u304c\u3070\u56de\u308c\u3058\u3083\u3002\u300d";
        this.strMessage[0][67] = "\"More haste, less speed.\"";
        this.objectAttribute[144][3] = 1;
        this.objectAttribute[144][1] = 55;
        this.objectAttribute[144][2] = 56;
        this.objectAttribute[144][5] = 68;
        this.strMessage[1][68] = "\u300c\u3053\u306e\u968e\u306e\uff14\u3064\u306e\u629c\u3051\u7a74\u3092\u3046\u307e\u304f\u4f7f\u3048\u3070\u3001\u5f37\u3044\u6575\u3068\u306f\u6226\u308f\u305a\u306b\u4e0a\u306e\u968e\u306b\u884c\u3051\u308b\u3058\u3083\u308d\u3046\u3002\u300d";
        this.strMessage[0][68] = "\"You may be able to go upstairs without fighting strong enemies, if you could use four tunnels skillfully in this floor.\"";
        this.objectAttribute[145][3] = 1;
        this.objectAttribute[145][1] = 55;
        this.objectAttribute[145][2] = 56;
        this.objectAttribute[145][5] = 69;
        this.strMessage[1][69] = "\u300c\u3053\u306e\u968e\u306e\u5b9d\u7269\u5eab\u306b\u3042\u308b\u5b9d\u3092\u53d6\u308b\u305f\u3081\u306b\u306f\u30de\u30c8\u30c3\u30af\u304c\u5fc5\u8981\u3058\u3083\u3002\u300d";
        this.strMessage[0][69] = "\"You need the mattock in order to get the treasure which is in the item warehouse on this floor.\"";
        this.objectAttribute[165][3] = 1;
        this.objectAttribute[165][1] = 49;
        this.objectAttribute[165][2] = 50;
        this.objectAttribute[165][5] = 70;
        this.strMessage[1][70] = "\u300c\u9580\u756a\u306e\u3044\u308b\u6240\u306b\u306f\u5fc5\u305a\u9580\u304c\u3042\u308b\u3088\u3002\u9006\u306b\u9580\u306e\u3042\u308b\u968e\u306b\u306f\u3001\u305d\u308c\u3092\u5b88\u3063\u3066\u3044\u308b\u6575\u304c\u3044\u308b\u3088\u3002\u3060\u304b\u3089\u2026\u2026\u3002\u300d";
        this.strMessage[0][70] = "\"There is never a gate without a Gate-Keeper. Conversely there are always enemies who keep the gate on floors that have gates. So,\"";
        this.objectAttribute[146][3] = 1;
        this.objectAttribute[146][1] = 55;
        this.objectAttribute[146][2] = 56;
        this.objectAttribute[146][5] = 71;
        this.strMessage[1][71] = "\u300c\uff13\u6642\u306b\u306a\u308c\u3070\u7a7a\u9593\u79fb\u52d5\u306e\u79d8\u5b9d\u304c\u73fe\u308c\u308b\u3058\u3083\u308d\u3046\u3002\u300d";
        this.strMessage[0][71] = "\"At three o'clock, the secret treasure that lets one travel in space will appear.\"";
        this.objectAttribute[167][3] = 1;
        this.objectAttribute[167][1] = 49;
        this.objectAttribute[167][2] = 50;
        this.objectAttribute[167][5] = 72;
        this.strMessage[1][72] = "\u300c\u3053\u306e\u5854\u306e\u3069\u3053\u304b\u306b\u3001\u5e78\u904b\u306e\u91d1\u8ca8\u3068\u3044\u3046\u3082\u306e\u304c\u3042\u3063\u3066\u3001\u305d\u308c\u3092\u6301\u3063\u3066\u3044\u308b\u3068\u6575\u3092\u5012\u3057\u305f\u3068\u304d\u306b\u5f97\u3089\u308c\u308b\u304a\u91d1\u304c\uff12\u500d\u306b\u306a\u308b\u305d\u3046\u3060\u3002\u300d";
        this.strMessage[0][72] = "\"There is a Lucky Gold somewhere in this tower. If you have it, you can get twice as much money when you beat an enemy.\"";
        this.objectAttribute[147][3] = 1;
        this.objectAttribute[147][1] = 55;
        this.objectAttribute[147][2] = 56;
        this.objectAttribute[147][5] = 73;
        this.strMessage[1][73] = "\u300c\u9b54\u8853\u5e2b\u306f\u96a3\u63a5\u3059\u308b\u3068\u9b54\u6cd5\u653b\u6483\u3092\u3057\u3066\u304f\u308b\u3002\u9b54\u5c0e\u5e2b\u306f\u306f\u3055\u307e\u308c\u308b\u3068\u751f\u547d\u529b\u3092\u534a\u5206\u306b\u3059\u308b\u653b\u6483\u3092\u3057\u3066\u304f\u308b\u3002\u9b54\u5c0e\u5e2b\u306e\u306f\u3055\u307f\u653b\u6483\u306f\u81ea\u5206\u306e\u751f\u547d\u529b\u304c\u9ad8\u3044\u307b\u3069\u53d7\u3051\u308b\u30c0\u30e1\u30fc\u30b8\u304c\u5927\u304d\u3044\u306f\u305a\u3058\u3083\u304b\u3089\u6c17\u3092\u3064\u3051\u3066\u306a\u3002\u300d";
        this.strMessage[0][73] = "\"A Magician will attack using magic when he is next to you. The Magic Sergeants will attack and divide the vital power in half when you are caught between two. As for an attack on both sides from the Magic Sergeant, the stronger you are, the more damage you take. So, please be careful.\"";
        this.objectAttribute[148][3] = 1;
        this.objectAttribute[148][1] = 55;
        this.objectAttribute[148][2] = 56;
        this.objectAttribute[148][5] = 74;
        this.strMessage[1][74] = "\u300c\u3053\u306e\u5854\u306e\uff14\uff14\u968e\u306f\u5e7b\u306e\u968e\u3058\u3083\u3002\u666e\u901a\u306e\u968e\u6bb5\u3092\u767b\u308a\u964d\u308a\u3057\u305f\u306e\u3067\u306f\u884c\u304f\u3053\u3068\u304c\u3067\u304d\u306a\u3044\u3089\u3057\u3044\u3002\u30ef\u30fc\u30d7\u3067\u3082\u3057\u306a\u3044\u304b\u304e\u308a\u884c\u304f\u3053\u3068\u306f\u4e0d\u53ef\u80fd\u3058\u3083\u308d\u3046\u3002\u300d";
        this.strMessage[0][74] = "\"The 44th floor in this tower is an illusion. It seems that we cannot go to there even if we use the stairs. I think that it is impossible to get there without teleporting.\"";
        this.objectAttribute[169][3] = 1;
        this.objectAttribute[169][1] = 49;
        this.objectAttribute[169][2] = 50;
        this.objectAttribute[169][5] = 75;
        this.strMessage[1][75] = "\u300c\u795e\u76fe\u306f\u3001\u9b54\u6cd5\u4f7f\u3044\u305f\u3061\u306e\u9b54\u6cd5\u653b\u6483\u3092\u9632\u3050\u529b\u304c\u3042\u308b\u3089\u3057\u3044\u3002\u2026\u2026\u3057\u304b\u3057\u3001\u3053\u306e\u76fe\u306f\u5e7b\u306e\u968e\u306b\u96a0\u3055\u308c\u3066\u3044\u308b\u305d\u3046\u3060\u3002\u300d";
        this.strMessage[0][75] = "\"The sacred shield can defend you against magic attacks. But I heard this shield is hidden on a floor that doesn't exist.\"";
        this.objectAttribute[149][3] = 1;
        this.objectAttribute[149][1] = 55;
        this.objectAttribute[149][2] = 56;
        this.objectAttribute[149][5] = 76;
        this.strMessage[1][76] = "\u300c\uff14\uff11\u968e\u306f\u5b8c\u5168\u306b\u5de6\u53f3\u5bfe\u79f0\u306b\u306a\u3063\u3066\u304a\u308b\u3002\u3060\u304b\u3089\u2026\u2026\u3002\u300d";
        this.strMessage[0][76] = "\"The 41st floor is perfectly symmetrical, and therefore,\"";
        this.objectAttribute[171][3] = 1;
        this.objectAttribute[171][1] = 49;
        this.objectAttribute[171][2] = 50;
        this.objectAttribute[171][5] = 77;
        this.strMessage[1][77] = "\u300c\u30c9\u30e9\u30b4\u30f3\u3092\u5012\u3059\u6c17\u306a\u3089\u3001\u8056\u5263\u3068\u8056\u76fe\u3001\u305d\u308c\u306b\u30c9\u30e9\u30b4\u30f3\u30b9\u30ec\u30fc\u30e4\u30fc\u3092\u6301\u3063\u3066\u3001\u306a\u304a\u304b\u3064\u30ec\u30d9\u30eb\u304c\u9ad8\u304f\u306a\u3051\u308c\u3070\u306a\u3089\u306a\u3044\u3060\u308d\u3046\u3002\u300d";
        this.strMessage[0][77] = "\"If you want to beat the Dragon, you must have a holy sword, a holy shield, and a Dragon slayer, and also you must be high level.\"";
        this.objectAttribute[150][3] = 1;
        this.objectAttribute[150][1] = 55;
        this.objectAttribute[150][2] = 56;
        this.objectAttribute[150][5] = 78;
        this.strMessage[1][78] = "\u300c\u30b5\u30a4\u30b3\u30ed\u306e\uff15\u306e\u76ee\u306e\u5f62\u306b\u306f\u3001\u9b54\u3092\u5c01\u3058\u8fbc\u3081\u308b\u529b\u304c\u3042\u308b\u3068\u3044\u3046\u3002\u3053\u306e\u30d6\u30ed\u30c3\u30af\u306e\u30dc\u30b9\u3068\u6226\u3046\u6642\u306b\u306f\u3001\u3053\u306e\u3053\u3068\u3092\u982d\u306b\u3044\u308c\u3066\u304a\u304d\u306a\u3055\u308c\u3002\u300d";
        this.strMessage[0][78] = "\"It is said that the symbol of 5 on a pair of dice has the force of sealing magic. You had better memorize it till you fight the boss of this area.\"";
        this.objectAttribute[151][3] = 1;
        this.objectAttribute[151][1] = 55;
        this.objectAttribute[151][2] = 56;
        this.objectAttribute[151][5] = 79;
        this.strMessage[1][79] = "\u300c\u3082\u3046\u3001\u8a71\u306f\u7d42\u308f\u308a\u3058\u3083\u3002\u300d";
        this.strMessage[0][79] = "\"I have done what I can. Good luck!\"";
        this.objectAttribute[152][3] = 1;
        this.objectAttribute[152][1] = 55;
        this.objectAttribute[152][2] = 56;
        this.objectAttribute[152][5] = 80;
        this.strMessage[1][80] = "\u300c\u304a\u304a\u3001\u52a9\u3051\u3066\u304f\u308c\u3066\u3042\u308a\u304c\u3068\u3046\u3088\u3002\u304a\u793c\u306b\u3001\u305d\u306a\u305f\u306e\u653b\u6483\u529b\u3068\u9632\u5fa1\u529b\u3092\uff13\uff05\u3060\u3051\u3042\u3052\u3066\u3084\u308d\u3046\u300d\uff08\u653b\u6483\u529b\u3068\u9632\u5fa1\u529b\u304c\u4e0a\u304c\u3063\u305f!\uff09";
        this.strMessage[0][80] = "\"Oh, thank you for your help. I will raise your offensive and defensive power 3 percent as a token of my gratitude. [You begin feeling stronger]\"";
        this.objectAttribute[153][3] = 1;
        this.objectAttribute[153][1] = 55;
        this.objectAttribute[153][2] = 56;
        this.objectAttribute[153][5] = 81;
        this.strMessage[1][81] = "\u300c\u304a\u306c\u3057\u306b\u3053\u306e\u52c7\u8005\u306e\u30aa\u30fc\u30d6\u3092\u3055\u305a\u3051\u3088\u3046\u3002\u3053\u308c\u3092\u6301\u3063\u3066\u3044\u308c\u3070\u4eca\u3044\u308b\u968e\u306e\u30e2\u30f3\u30b9\u30bf\u30fc\u306e\u80fd\u529b\u3092\u8abf\u3079\u3066\u30c0\u30e1\u30fc\u30b8\u3092\u4e88\u6e2c\u3057\u3066\u304f\u308c\u308b\u3058\u3083\u308d\u3046\u3002\u6709\u52b9\u306b\u4f7f\u3046\u306e\u3058\u3083\u300d";
        this.strMessage[0][81] = "\"I will grant you the orb of the hero. It will forecast the results of fighting monsters on the current floor. Use it often.\"";
        this.objectAttribute[154][3] = 1;
        this.objectAttribute[154][1] = 55;
        this.objectAttribute[154][2] = 56;
        this.objectAttribute[154][5] = 82;
        this.strMessage[1][82] = "\u300c\u3084\u308c\u3084\u308c\u3001\u898b\u3064\u304b\u3063\u3066\u3057\u3082\u3046\u305f\u304b\u3002\u8912\u7f8e\u306b\u304a\u306c\u3057\u306b\u201d\u30a8\u30ea\u30af\u30b5\u30fc\u201d\u3092\u3084\u308d\u3046\u3002\u3053\u306e\u85ac\u3092\u4f7f\u3048\u3070\u3001\u305d\u306e\u6642\u306e\u653b\u6483\u529b\u3068\u9632\u5fa1\u529b\u306b\u5fdc\u3058\u305f\u5024\u3060\u3051\u751f\u547d\u529b\u304c\u56de\u5fa9\u3059\u308b\u3058\u3083\u308d\u3046\u3002\u3058\u3083\u304b\u3089\u3001\u5f53\u7136\u3001\u5f8c\u306e\u65b9\u3067\u4f7f\u3046\u65b9\u304c\u52b9\u679c\u306f\u5927\u304d\u3044\u305e\u3002\u300d";
        this.strMessage[0][82] = "\"Thank goodness, you found me. I will give you an elixir as a symbol of my gratitude. Using this medicine will cause you to gain life according to your offensive and defensive power. So naturally, the later you use, the more it will have an effect on you.\"";
        this.objectAttribute[172][3] = 1;
        this.objectAttribute[172][1] = 49;
        this.objectAttribute[172][2] = 50;
        this.objectAttribute[172][5] = 83;
        this.strMessage[1][83] = "\u300c\u3082\u3046\u3001\u8a71\u3059\u4e8b\u306f\u306a\u3044\u3088\u3002\u300d";
        this.strMessage[0][83] = "\"Be careful. I have nothing more to say.\"";
        this.objectAttribute[173][3] = 1;
        this.objectAttribute[173][1] = 49;
        this.objectAttribute[173][2] = 50;
        this.objectAttribute[173][5] = 84;
        this.strMessage[1][84] = "\u300c\u6709\u52b9\u306b\u4f7f\u3063\u3066\u306d!\u300d";
        this.strMessage[0][84] = "\"Please, use it wisely.\"";
        this.objectAttribute[174][3] = 1;
        this.objectAttribute[174][1] = 49;
        this.objectAttribute[174][2] = 50;
        this.objectAttribute[174][5] = 85;
        this.strMessage[1][85] = "\u300c\u3084\u3042\u3001\u52a9\u3051\u3066\u304f\u308c\u3066\u3042\u308a\u304c\u3068\u3046\u3002\u5c11\u306a\u3044\u3051\u308c\u3069\u3001\u304a\u793c\u306b\u3068\u3063\u3066\u304a\u3044\u3066\u304f\u308c\uff01\u300d\uff08\uff11\uff10\uff10\uff10\uff27\uff2f\uff2c\uff24\u3082\u3089\u3063\u305f!\uff09";
        this.strMessage[0][85] = "\"Thank you for your help. Please accept money as a small token of my gratitude. (Got 1000 Gold.)\"";
        this.objectAttribute[18][3] = 14;
        this.objectAttribute[18][1] = 49;
        this.objectAttribute[18][2] = 50;
        this.objectAttribute[18][5] = 86;
        this.objectAttribute[18][13] = 50;
        this.strMessage[1][86] = "\u300c\u7d2b\u306e\u9375\u3092\u5927\u7279\u4fa1\u306e\uff15\uff10\uff27\uff2f\uff2c\uff24\u3067\u58f2\u308b\u3088! \u8cb7\u308f\u306a\u3044\u304b\u3044?\u300d";
        this.strMessage[0][86] = "\"I will sell a blue key at very special price (50 gold)! Will you buy it?\"";
        this.objectAttribute[41][3] = 14;
        this.objectAttribute[41][1] = 49;
        this.objectAttribute[41][2] = 50;
        this.objectAttribute[41][5] = 87;
        this.objectAttribute[41][13] = 50;
        this.strMessage[1][87] = "\u300c\u9375\u3092\uff15\u500b\u30bb\u30c3\u30c8\u3067\uff15\uff10\uff27\uff2f\uff2c\uff24\u3067\u58f2\u308b\u3088! \u8cb7\u308f\u306a\u3044\u304b\u3044?\u300d";
        this.strMessage[0][87] = "\"I will sell five keys for 50 Gold! Will you buy them?\"";
        this.objectAttribute[156][3] = 14;
        this.objectAttribute[156][1] = 49;
        this.objectAttribute[156][2] = 50;
        this.objectAttribute[156][5] = 88;
        this.objectAttribute[156][13] = 800;
        this.strMessage[1][88] = "\u300c\u5e0c\u5c11\u54c1\u306e\u8d64\u3044\u9375\u3092\uff18\uff10\uff10\uff27\uff2f\uff2c\uff24\u3067\u58f2\u308b\u3088\uff01\u8cb7\u308f\u306a\u3044\u304b\u3044\uff1f\u300d";
        this.strMessage[0][88] = "\"I will sell the rare red key for 800 Gold! Will you buy it?\"";
        this.objectAttribute[17][3] = 14;
        this.objectAttribute[17][1] = 49;
        this.objectAttribute[17][2] = 50;
        this.objectAttribute[17][6] = 280;
        this.objectAttribute[17][7] = 200;
        this.objectAttribute[17][8] = 320;
        this.objectAttribute[17][9] = 200;
        this.objectAttribute[17][5] = 89;
        this.objectAttribute[17][13] = 1000;
        this.strMessage[1][89] = "\u300c\u3046\u3061\u306e\u5e97\u306f\u9375\u3092\u3044\u304f\u3089\u3067\u3082\u58f2\u308b\u3088\u3002\uff11\u3064\uff11\uff10\uff10\uff10\uff27\uff2f\uff2c\uff24\u3060\u304c\u8cb7\u3046\u304b\u3044\uff1f\u300d";
        this.strMessage[0][89] = "\"My store will sell as many keys as you need. They are 1000 Gold each. Will you buy them?\"";
        this.objectAttribute[159][3] = 14;
        this.objectAttribute[159][1] = 49;
        this.objectAttribute[159][2] = 50;
        this.objectAttribute[159][5] = 90;
        this.objectAttribute[159][13] = 200;
        this.strMessage[1][90] = "\u300c\u7d2b\u306e\u9375\u3092\uff12\uff10\uff10\uff27\uff2f\uff2c\uff24\u3067\u58f2\u308b\u3088\uff01\u8cb7\u308f\u306a\u3044\u304b\u3044\uff1f\u300d";
        this.strMessage[0][90] = "\"I will sell a blue key for 200 Gold! Will you buy it?\"";
        this.objectAttribute[161][3] = 15;
        this.objectAttribute[161][1] = 49;
        this.objectAttribute[161][2] = 50;
        this.objectAttribute[161][5] = 91;
        this.objectAttribute[161][13] = 100;
        this.strMessage[1][91] = "\u300c\u9375\uff11\u500b\u3092\uff11\uff10\uff10\uff27\uff2f\uff2c\uff24\u3067\u8cb7\u3046\u3088\u3002\u9375\u3092\u58f2\u308b\u304b\u3044\uff1f\u300d";
        this.strMessage[0][91] = "\"I will buy your keys at 100 Gold a piece. Will you sell me keys?\"";
        this.objectAttribute[162][3] = 14;
        this.objectAttribute[162][1] = 49;
        this.objectAttribute[162][2] = 50;
        this.objectAttribute[162][5] = 92;
        this.objectAttribute[162][13] = 1000;
        this.strMessage[1][92] = "\u300c\u9375\u3092\uff14\u500b\u3068\u7d2b\u306e\u9375\u3092\u30bb\u30c3\u30c8\u306b\u3057\u3066\uff11\uff10\uff10\uff10\uff27\uff2f\uff2c\uff24\u3060\uff01\u8cb7\u3046\u304b\u3044\uff1f\u300d";
        this.strMessage[0][92] = "\"I will sell four keys and a blue key for 1000 Gold! Will you buy them?\"";
        this.objectAttribute[164][3] = 14;
        this.objectAttribute[164][1] = 49;
        this.objectAttribute[164][2] = 50;
        this.objectAttribute[164][5] = 93;
        this.objectAttribute[164][13] = 200;
        this.strMessage[1][93] = "\u300c\u9375\uff13\u500b\u3092\u5927\u30b5\u30fc\u30d3\u30b9\u306e\uff12\uff10\uff10\uff27\uff2f\uff2c\uff24\u3067\u58f2\u308b\u3088\uff01\u65e9\u3044\u8005\u52dd\u3061\u3060\u3088\uff01\u300d";
        this.strMessage[0][93] = "\"I will sell three keys at special price (200 gold). First come, first served.\"";
        this.objectAttribute[166][3] = 14;
        this.objectAttribute[166][1] = 49;
        this.objectAttribute[166][2] = 50;
        this.objectAttribute[166][5] = 94;
        this.objectAttribute[166][13] = 2000;
        this.strMessage[1][94] = "\u300c\u7d2b\u306e\u9375\u304c\uff13\u500b\u3067\uff12\uff10\uff10\uff10\uff27\uff2f\uff2c\uff24\u3060\u304c\u3001\u8cb7\u3046\u304b\u3044\uff1f\u300d";
        this.strMessage[0][94] = "\"2000 Golds for three blue keys. Deal?\"";
        this.objectAttribute[168][3] = 14;
        this.objectAttribute[168][1] = 49;
        this.objectAttribute[168][2] = 50;
        this.objectAttribute[168][5] = 95;
        this.objectAttribute[168][13] = 1000;
        this.strMessage[1][95] = "\u300c\uff11\uff10\uff10\uff10\uff27\uff2f\uff2c\uff24\u3067\u751f\u547d\u529b\u3092\uff12\uff10\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u56de\u5fa9\u3057\u3066\u3042\u3052\u308b\u3088\u3002\u300d";
        this.strMessage[0][95] = "\"I will increase your life 2000 points at 1000 Gold.\"";
        this.objectAttribute[170][3] = 14;
        this.objectAttribute[170][1] = 49;
        this.objectAttribute[170][2] = 50;
        this.objectAttribute[170][5] = 96;
        this.objectAttribute[170][13] = 4000;
        this.strMessage[1][96] = "\u300c\u8d85\u5e0c\u5c11\u54c1\u306e\u30b9\u30fc\u30d1\u30fc\u30de\u30c8\u30c3\u30af\u3092\uff14\uff10\uff10\uff10\uff27\uff2f\uff2c\uff24\u3067\u8cb7\u308f\u306a\u3044\u304b\u3044\uff1f\u300d";
        this.strMessage[0][96] = "\"Would you like to buy a super mattock (it's very rare) for 4000 Gold?\"";
        this.strMessage[1][97] = "\u8868\u793a\u3059\u308b\u60c5\u5831\u304c\u3042\u308a\u307e\u305b\u3093\u3002";
        this.strMessage[0][97] = "You don't have an informations any more.";
        this.strMessage[1][98] = "\u300c\u307e\u3044\u3069\u30fc\u3063\uff01\u300d";
        this.strMessage[0][98] = "\"Thank you very much.\"";
        this.strMessage[1][99] = "\u76d7\u8cca\u300c\u3088\u3046\u307e\u305f\u3042\u3063\u305f\u306a\uff01\u7121\u4e8b\u3060\u3063\u305f\u304b\uff1f\u3053\u308c\u306f\u805e\u3044\u305f\u8a71\u306a\u3093\u3060\u304c\u3001\uff12\uff15\u968e\u306e\u30dc\u30b9\u3092\u5012\u3059\u3068\u300e\u6642\u7a7a\u306e\u9580\u300f\u304c\u3069\u3053\u304b\u306b\u3067\u304d\u308b\u3089\u3057\u3044\u305e\u3002\u300d";
        this.strMessage[0][99] = "The thief says \"Ah!, we meet again! Thank goodness you're alive! I heard that if you beat the boss of 25th floor, 'the gate of time and space' will appear somewhere.\"";
        this.objectAttribute[5][3] = 6;
        this.objectAttribute[5][1] = 91;
        this.objectAttribute[5][2] = 92;
        this.objectAttribute[5][6] = 360;
        this.objectAttribute[5][7] = 360;
        this.objectAttribute[5][8] = 0;
        this.objectAttribute[5][9] = 400;
        this.objectAttribute[5][5] = 100;
        this.objectAttribute[5][10] = 35;
        this.objectAttribute[5][11] = 18;
        this.objectAttribute[5][12] = 1;
        this.objectAttribute[5][13] = 1;
        this.strMessage[1][100] = "\uff27\u30b9\u30e9\u30a4\u30e0";
        this.strMessage[0][100] = "Green Slime";
        this.objectAttribute[6][3] = 6;
        this.objectAttribute[6][1] = 93;
        this.objectAttribute[6][2] = 94;
        this.objectAttribute[6][6] = 40;
        this.objectAttribute[6][7] = 400;
        this.objectAttribute[6][8] = 80;
        this.objectAttribute[6][9] = 400;
        this.objectAttribute[6][5] = 101;
        this.objectAttribute[6][10] = 45;
        this.objectAttribute[6][11] = 20;
        this.objectAttribute[6][12] = 2;
        this.objectAttribute[6][13] = 2;
        this.strMessage[1][101] = "\uff32\u30b9\u30e9\u30a4\u30e0";
        this.strMessage[0][101] = "Red Slime";
        this.objectAttribute[45][3] = 6;
        this.objectAttribute[45][1] = 95;
        this.objectAttribute[45][2] = 96;
        this.objectAttribute[45][6] = 120;
        this.objectAttribute[45][7] = 400;
        this.objectAttribute[45][8] = 160;
        this.objectAttribute[45][9] = 400;
        this.objectAttribute[45][5] = 102;
        this.objectAttribute[45][10] = 130;
        this.objectAttribute[45][11] = 60;
        this.objectAttribute[45][12] = 3;
        this.objectAttribute[45][13] = 8;
        this.strMessage[1][102] = "\uff22\u30b9\u30e9\u30a4\u30e0";
        this.strMessage[0][102] = "Big Slime";
        this.objectAttribute[7][3] = 6;
        this.objectAttribute[7][1] = 97;
        this.objectAttribute[7][2] = 98;
        this.objectAttribute[7][6] = 200;
        this.objectAttribute[7][7] = 400;
        this.objectAttribute[7][8] = 240;
        this.objectAttribute[7][9] = 400;
        this.objectAttribute[7][5] = 103;
        this.objectAttribute[7][10] = 35;
        this.objectAttribute[7][11] = 38;
        this.objectAttribute[7][12] = 3;
        this.objectAttribute[7][13] = 3;
        this.strMessage[1][103] = "\u30d0\u30c3\u30c8";
        this.strMessage[0][103] = "Bat";
        this.objectAttribute[8][3] = 6;
        this.objectAttribute[8][1] = 99;
        this.objectAttribute[8][2] = 100;
        this.objectAttribute[8][6] = 280;
        this.objectAttribute[8][7] = 400;
        this.objectAttribute[8][8] = 320;
        this.objectAttribute[8][9] = 400;
        this.objectAttribute[8][5] = 104;
        this.objectAttribute[8][10] = 60;
        this.objectAttribute[8][11] = 32;
        this.objectAttribute[8][12] = 8;
        this.objectAttribute[8][13] = 5;
        this.strMessage[1][104] = "\u50e7\u3000\u4fb6";
        this.strMessage[0][104] = "Priest";
        this.objectAttribute[46][3] = 6;
        this.objectAttribute[46][1] = 101;
        this.objectAttribute[46][2] = 102;
        this.objectAttribute[46][6] = 360;
        this.objectAttribute[46][7] = 400;
        this.objectAttribute[46][8] = 0;
        this.objectAttribute[46][9] = 440;
        this.objectAttribute[46][5] = 105;
        this.objectAttribute[46][10] = 100;
        this.objectAttribute[46][11] = 95;
        this.objectAttribute[46][12] = 30;
        this.objectAttribute[46][13] = 22;
        this.strMessage[1][105] = "\u4e0a\u7d1a\u50e7\u4fb6";
        this.strMessage[0][105] = "Superion Priest";
        this.objectAttribute[29][3] = 6;
        this.objectAttribute[29][1] = 103;
        this.objectAttribute[29][2] = 104;
        this.objectAttribute[29][6] = 40;
        this.objectAttribute[29][7] = 440;
        this.objectAttribute[29][8] = 80;
        this.objectAttribute[29][9] = 440;
        this.objectAttribute[29][5] = 106;
        this.objectAttribute[29][10] = 50;
        this.objectAttribute[29][11] = 48;
        this.objectAttribute[29][12] = 22;
        this.objectAttribute[29][13] = 12;
        this.strMessage[1][106] = "\u9580\u756a\uff23";
        this.strMessage[0][106] = "Gate-Keeper C";
        this.objectAttribute[15][3] = 6;
        this.objectAttribute[15][1] = 105;
        this.objectAttribute[15][2] = 106;
        this.objectAttribute[15][6] = 120;
        this.objectAttribute[15][7] = 440;
        this.objectAttribute[15][8] = 160;
        this.objectAttribute[15][9] = 440;
        this.objectAttribute[15][5] = 107;
        this.objectAttribute[15][10] = 100;
        this.objectAttribute[15][11] = 180;
        this.objectAttribute[15][12] = 110;
        this.objectAttribute[15][13] = 100;
        this.strMessage[1][107] = "\u9580\u756a\uff22";
        this.strMessage[0][107] = "Gate-Keeper B";
        this.objectAttribute[9][3] = 6;
        this.objectAttribute[9][1] = 107;
        this.objectAttribute[9][2] = 108;
        this.objectAttribute[9][6] = 200;
        this.objectAttribute[9][7] = 440;
        this.objectAttribute[9][8] = 240;
        this.objectAttribute[9][9] = 440;
        this.objectAttribute[9][5] = 108;
        this.objectAttribute[9][10] = 50;
        this.objectAttribute[9][11] = 42;
        this.objectAttribute[9][12] = 6;
        this.objectAttribute[9][13] = 6;
        this.strMessage[1][108] = "\u30b9\u30b1\u30eb\u30c8\u30f3\uff23";
        this.strMessage[0][108] = "Skeleton C";
        this.objectAttribute[10][3] = 6;
        this.objectAttribute[10][1] = 109;
        this.objectAttribute[10][2] = 110;
        this.objectAttribute[10][6] = 280;
        this.objectAttribute[10][7] = 440;
        this.objectAttribute[10][8] = 320;
        this.objectAttribute[10][9] = 440;
        this.objectAttribute[10][5] = 109;
        this.objectAttribute[10][10] = 55;
        this.objectAttribute[10][11] = 52;
        this.objectAttribute[10][12] = 12;
        this.objectAttribute[10][13] = 8;
        this.strMessage[1][109] = "\u30b9\u30b1\u30eb\u30c8\u30f3\uff22";
        this.strMessage[0][109] = "Skeleton B";
        this.objectAttribute[16][3] = 6;
        this.objectAttribute[16][1] = 111;
        this.objectAttribute[16][2] = 112;
        this.objectAttribute[16][6] = 360;
        this.objectAttribute[16][7] = 440;
        this.objectAttribute[16][8] = 0;
        this.objectAttribute[16][9] = 480;
        this.objectAttribute[16][5] = 110;
        this.objectAttribute[16][10] = 100;
        this.objectAttribute[16][11] = 65;
        this.objectAttribute[16][12] = 15;
        this.objectAttribute[16][13] = 30;
        this.strMessage[1][110] = "\u30b9\u30b1\u30eb\u30c8\u30f3\uff21";
        this.strMessage[0][110] = "Skeleton A";
        this.objectAttribute[47][3] = 6;
        this.objectAttribute[47][1] = 113;
        this.objectAttribute[47][2] = 114;
        this.objectAttribute[47][6] = 40;
        this.objectAttribute[47][7] = 480;
        this.objectAttribute[47][8] = 80;
        this.objectAttribute[47][9] = 480;
        this.objectAttribute[47][5] = 111;
        this.objectAttribute[47][10] = 60;
        this.objectAttribute[47][11] = 100;
        this.objectAttribute[47][12] = 8;
        this.objectAttribute[47][13] = 12;
        this.strMessage[1][111] = "\u5927\u30d0\u30c3\u30c8";
        this.strMessage[0][111] = "Big Bat";
        this.objectAttribute[48][3] = 6;
        this.objectAttribute[48][1] = 115;
        this.objectAttribute[48][2] = 116;
        this.objectAttribute[48][6] = 120;
        this.objectAttribute[48][7] = 480;
        this.objectAttribute[48][8] = 160;
        this.objectAttribute[48][9] = 480;
        this.objectAttribute[48][5] = 112;
        this.objectAttribute[48][10] = 260;
        this.objectAttribute[48][11] = 85;
        this.objectAttribute[48][12] = 5;
        this.objectAttribute[48][13] = 18;
        this.strMessage[1][112] = "\u30be\u30f3\u30d3";
        this.strMessage[0][112] = "Zombie";
        this.objectAttribute[49][3] = 6;
        this.objectAttribute[49][1] = 117;
        this.objectAttribute[49][2] = 118;
        this.objectAttribute[49][6] = 200;
        this.objectAttribute[49][7] = 480;
        this.objectAttribute[49][8] = 240;
        this.objectAttribute[49][9] = 480;
        this.objectAttribute[49][5] = 113;
        this.objectAttribute[49][10] = 320;
        this.objectAttribute[49][11] = 120;
        this.objectAttribute[49][12] = 15;
        this.objectAttribute[49][13] = 30;
        this.strMessage[1][113] = "\u30be\u30f3\u30d3\u30ca\u30a4\u30c8";
        this.strMessage[0][113] = "Zombie Knight";
        this.objectAttribute[56][3] = 6;
        this.objectAttribute[56][1] = 119;
        this.objectAttribute[56][2] = 120;
        this.objectAttribute[56][6] = 280;
        this.objectAttribute[56][7] = 480;
        this.objectAttribute[56][8] = 320;
        this.objectAttribute[56][9] = 480;
        this.objectAttribute[56][5] = 114;
        this.objectAttribute[56][10] = 20;
        this.objectAttribute[56][11] = 100;
        this.objectAttribute[56][12] = 68;
        this.objectAttribute[56][13] = 28;
        this.strMessage[1][114] = "\u30ed\u30c3\u30af";
        this.strMessage[0][114] = "Rock";
        this.objectAttribute[57][3] = 6;
        this.objectAttribute[57][1] = 121;
        this.objectAttribute[57][2] = 122;
        this.objectAttribute[57][6] = 360;
        this.objectAttribute[57][7] = 480;
        this.objectAttribute[57][8] = 0;
        this.objectAttribute[57][9] = 520;
        this.objectAttribute[57][5] = 115;
        this.objectAttribute[57][10] = 8000;
        this.objectAttribute[57][11] = 5000;
        this.objectAttribute[57][12] = 1000;
        this.objectAttribute[57][13] = 500;
        this.strMessage[1][115] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce";
        this.strMessage[0][115] = "Magic Serg. Zeno";
        this.objectAttribute[58][3] = 6;
        this.objectAttribute[58][1] = 123;
        this.objectAttribute[58][2] = 124;
        this.objectAttribute[58][6] = 40;
        this.objectAttribute[58][7] = 520;
        this.objectAttribute[58][8] = 80;
        this.objectAttribute[58][9] = 520;
        this.objectAttribute[58][5] = 116;
        this.objectAttribute[58][10] = 230;
        this.objectAttribute[58][11] = 450;
        this.objectAttribute[58][12] = 100;
        this.objectAttribute[58][13] = 100;
        this.strMessage[1][116] = "\u9b54\u5c0e\u5e2b";
        this.strMessage[0][116] = "Magic Sergeant";
        this.objectAttribute[59][3] = 6;
        this.objectAttribute[59][1] = 125;
        this.objectAttribute[59][2] = 126;
        this.objectAttribute[59][6] = 120;
        this.objectAttribute[59][7] = 520;
        this.objectAttribute[59][8] = 160;
        this.objectAttribute[59][9] = 520;
        this.objectAttribute[59][5] = 117;
        this.objectAttribute[59][10] = 444;
        this.objectAttribute[59][11] = 199;
        this.objectAttribute[59][12] = 66;
        this.objectAttribute[59][13] = 144;
        this.strMessage[1][117] = "\u30d0\u30f3\u30d1\u30a4\u30a2";
        this.strMessage[0][117] = "Vampire";
        this.objectAttribute[71][3] = 6;
        this.objectAttribute[71][1] = 141;
        this.objectAttribute[71][2] = 142;
        this.objectAttribute[71][6] = 80;
        this.objectAttribute[71][7] = 560;
        this.objectAttribute[71][8] = 40;
        this.objectAttribute[71][9] = 600;
        this.objectAttribute[71][5] = 118;
        this.objectAttribute[71][10] = 1200;
        this.objectAttribute[71][11] = 180;
        this.objectAttribute[71][12] = 20;
        this.objectAttribute[71][13] = 100;
        this.strMessage[1][118] = "\u5927\u30c0\u30b3";
        this.strMessage[0][118] = "Giant Octopus";
        this.objectAttribute[74][3] = 6;
        this.objectAttribute[74][1] = 159;
        this.objectAttribute[74][2] = 160;
        this.objectAttribute[74][6] = 0;
        this.objectAttribute[74][7] = 640;
        this.objectAttribute[74][8] = 360;
        this.objectAttribute[74][9] = 640;
        this.objectAttribute[74][5] = 119;
        this.objectAttribute[74][10] = 1500;
        this.objectAttribute[74][11] = 600;
        this.objectAttribute[74][12] = 250;
        this.objectAttribute[74][13] = 800;
        this.strMessage[1][119] = "\u30c9\u30e9\u30b4\u30f3";
        this.strMessage[0][119] = "Dragon";
        this.objectAttribute[90][3] = 6;
        this.objectAttribute[90][1] = 163;
        this.objectAttribute[90][2] = 164;
        this.objectAttribute[90][6] = 40;
        this.objectAttribute[90][7] = 680;
        this.objectAttribute[90][8] = 80;
        this.objectAttribute[90][9] = 680;
        this.objectAttribute[90][5] = 120;
        this.objectAttribute[90][10] = 120;
        this.objectAttribute[90][11] = 150;
        this.objectAttribute[90][12] = 50;
        this.objectAttribute[90][13] = 100;
        this.strMessage[1][120] = "\u91d1\u9a0e\u58eb";
        this.strMessage[0][120] = "Golden Knight";
        this.objectAttribute[91][3] = 6;
        this.objectAttribute[91][1] = 165;
        this.objectAttribute[91][2] = 166;
        this.objectAttribute[91][6] = 120;
        this.objectAttribute[91][7] = 680;
        this.objectAttribute[91][8] = 160;
        this.objectAttribute[91][9] = 680;
        this.objectAttribute[91][5] = 121;
        this.objectAttribute[91][10] = 160;
        this.objectAttribute[91][11] = 230;
        this.objectAttribute[91][12] = 105;
        this.objectAttribute[91][13] = 65;
        this.strMessage[1][121] = "\u9a0e\u3000\u58eb";
        this.strMessage[0][121] = "Knight";
        this.objectAttribute[92][3] = 6;
        this.objectAttribute[92][1] = 167;
        this.objectAttribute[92][2] = 168;
        this.objectAttribute[92][6] = 200;
        this.objectAttribute[92][7] = 680;
        this.objectAttribute[92][8] = 240;
        this.objectAttribute[92][9] = 680;
        this.objectAttribute[92][5] = 122;
        this.objectAttribute[92][10] = 100;
        this.objectAttribute[92][11] = 680;
        this.objectAttribute[92][12] = 50;
        this.objectAttribute[92][13] = 55;
        this.strMessage[1][122] = "\u5263\u3000\u58eb";
        this.strMessage[0][122] = "Swordsman";
        this.objectAttribute[93][3] = 6;
        this.objectAttribute[93][1] = 169;
        this.objectAttribute[93][2] = 170;
        this.objectAttribute[93][6] = 280;
        this.objectAttribute[93][7] = 680;
        this.objectAttribute[93][8] = 320;
        this.objectAttribute[93][9] = 680;
        this.objectAttribute[93][5] = 123;
        this.objectAttribute[93][10] = 210;
        this.objectAttribute[93][11] = 200;
        this.objectAttribute[93][12] = 65;
        this.objectAttribute[93][13] = 45;
        this.strMessage[1][123] = "\u5175\u3000\u58eb";
        this.strMessage[0][123] = "Soldier";
        this.objectAttribute[94][3] = 6;
        this.objectAttribute[94][1] = 171;
        this.objectAttribute[94][2] = 172;
        this.objectAttribute[94][6] = 360;
        this.objectAttribute[94][7] = 680;
        this.objectAttribute[94][8] = 0;
        this.objectAttribute[94][9] = 720;
        this.objectAttribute[94][5] = 124;
        this.objectAttribute[94][10] = 220;
        this.objectAttribute[94][11] = 180;
        this.objectAttribute[94][12] = 30;
        this.objectAttribute[94][13] = 35;
        this.strMessage[1][124] = "\u6b7b\u970a\u5175\u58eb";
        this.strMessage[0][124] = "Ghost Soldier";
        this.objectAttribute[95][3] = 6;
        this.objectAttribute[95][1] = 173;
        this.objectAttribute[95][2] = 174;
        this.objectAttribute[95][6] = 40;
        this.objectAttribute[95][7] = 720;
        this.objectAttribute[95][8] = 80;
        this.objectAttribute[95][9] = 720;
        this.objectAttribute[95][5] = 125;
        this.objectAttribute[95][10] = 320;
        this.objectAttribute[95][11] = 140;
        this.objectAttribute[95][12] = 20;
        this.objectAttribute[95][13] = 30;
        this.strMessage[1][125] = "\u30b9\u30e9\u30a4\u30e0\u30de\u30f3";
        this.strMessage[0][125] = "Slime Man";
        this.objectAttribute[96][3] = 6;
        this.objectAttribute[96][1] = 175;
        this.objectAttribute[96][2] = 176;
        this.objectAttribute[96][6] = 120;
        this.objectAttribute[96][7] = 720;
        this.objectAttribute[96][8] = 160;
        this.objectAttribute[96][9] = 720;
        this.objectAttribute[96][5] = 126;
        this.objectAttribute[96][10] = 4500;
        this.objectAttribute[96][11] = 560;
        this.objectAttribute[96][12] = 310;
        this.objectAttribute[96][13] = 1000;
        this.strMessage[1][126] = "\u5927\u9b54\u5c0e\u5e2b";
        this.strMessage[0][126] = "Great Magic Master";
        this.objectAttribute[97][3] = 6;
        this.objectAttribute[97][1] = 177;
        this.objectAttribute[97][2] = 178;
        this.objectAttribute[97][6] = 200;
        this.objectAttribute[97][7] = 720;
        this.objectAttribute[97][8] = 240;
        this.objectAttribute[97][9] = 720;
        this.objectAttribute[97][5] = 127;
        this.objectAttribute[97][10] = 200;
        this.objectAttribute[97][11] = 390;
        this.objectAttribute[97][12] = 90;
        this.objectAttribute[97][13] = 50;
        this.strMessage[1][127] = "\u5438\u8840\u30b3\u30a6\u30e2\u30ea";
        this.strMessage[0][127] = "Vampire Bat";
        this.objectAttribute[98][3] = 6;
        this.objectAttribute[98][1] = 179;
        this.objectAttribute[98][2] = 180;
        this.objectAttribute[98][6] = 280;
        this.objectAttribute[98][7] = 720;
        this.objectAttribute[98][8] = 320;
        this.objectAttribute[98][9] = 720;
        this.objectAttribute[98][5] = 128;
        this.objectAttribute[98][10] = 360;
        this.objectAttribute[98][11] = 310;
        this.objectAttribute[98][12] = 20;
        this.objectAttribute[98][13] = 40;
        this.strMessage[1][128] = "\uff2b\u30b9\u30e9\u30a4\u30e0";
        this.strMessage[0][128] = "SlimeLord";
        this.objectAttribute[99][3] = 6;
        this.objectAttribute[99][1] = 181;
        this.objectAttribute[99][2] = 182;
        this.objectAttribute[99][6] = 360;
        this.objectAttribute[99][7] = 720;
        this.objectAttribute[99][8] = 0;
        this.objectAttribute[99][9] = 760;
        this.objectAttribute[99][5] = 129;
        this.objectAttribute[99][10] = 200;
        this.objectAttribute[99][11] = 380;
        this.objectAttribute[99][12] = 130;
        this.objectAttribute[99][13] = 90;
        this.strMessage[1][129] = "\u9b54\u8853\u5e2b\uff21";
        this.strMessage[0][129] = "Magician A";
        this.objectAttribute[100][3] = 6;
        this.objectAttribute[100][1] = 183;
        this.objectAttribute[100][2] = 184;
        this.objectAttribute[100][6] = 40;
        this.objectAttribute[100][7] = 760;
        this.objectAttribute[100][8] = 80;
        this.objectAttribute[100][9] = 760;
        this.objectAttribute[100][5] = 130;
        this.objectAttribute[100][10] = 220;
        this.objectAttribute[100][11] = 370;
        this.objectAttribute[100][12] = 110;
        this.objectAttribute[100][13] = 80;
        this.strMessage[1][130] = "\u9b54\u8853\u5e2b\uff22";
        this.strMessage[0][130] = "Magician B";
        this.objectAttribute[101][3] = 6;
        this.objectAttribute[101][1] = 185;
        this.objectAttribute[101][2] = 186;
        this.objectAttribute[101][6] = 120;
        this.objectAttribute[101][7] = 760;
        this.objectAttribute[101][8] = 160;
        this.objectAttribute[101][9] = 760;
        this.objectAttribute[101][5] = 131;
        this.objectAttribute[101][10] = 180;
        this.objectAttribute[101][11] = 430;
        this.objectAttribute[101][12] = 210;
        this.objectAttribute[101][13] = 120;
        this.strMessage[1][131] = "\u9ed2\u9a0e\u58eb";
        this.strMessage[0][131] = "Dark Knight";
        this.objectAttribute[102][3] = 6;
        this.objectAttribute[102][1] = 187;
        this.objectAttribute[102][2] = 188;
        this.objectAttribute[102][6] = 200;
        this.objectAttribute[102][7] = 760;
        this.objectAttribute[102][8] = 240;
        this.objectAttribute[102][9] = 760;
        this.objectAttribute[102][5] = 132;
        this.objectAttribute[102][10] = 180;
        this.objectAttribute[102][11] = 460;
        this.objectAttribute[102][12] = 360;
        this.objectAttribute[102][13] = 200;
        this.strMessage[1][132] = "\u9580\u756a\uff21";
        this.strMessage[0][132] = "Gate-Keeper A";
        this.objectAttribute[1][3] = 8;
        this.objectAttribute[1][1] = 59;
        this.objectAttribute[1][2] = 0;
        this.objectAttribute[1][6] = 280;
        this.objectAttribute[1][7] = 240;
        this.objectAttribute[1][5] = 133;
        this.strMessage[1][133] = "\u6249\u306e\u9375\u3092\u624b\u306b\u5165\u308c\u305f\u3002";
        this.strMessage[0][133] = "Got a key.";
        this.objectAttribute[3][3] = 8;
        this.objectAttribute[3][1] = 60;
        this.objectAttribute[3][2] = 0;
        this.objectAttribute[3][6] = 360;
        this.objectAttribute[3][7] = 240;
        this.objectAttribute[3][5] = 134;
        this.strMessage[1][134] = "\u9752\u8272\u306e\u6249\u306e\u9375\u3092\u624b\u306b\u5165\u308c\u305f\u3002";
        this.strMessage[0][134] = "Got a blue key.";
        this.objectAttribute[28][3] = 8;
        this.objectAttribute[28][1] = 61;
        this.objectAttribute[28][2] = 0;
        this.objectAttribute[28][6] = 320;
        this.objectAttribute[28][7] = 240;
        this.objectAttribute[28][5] = 135;
        this.strMessage[1][135] = "\u8d64\u8272\u306e\u6249\u306e\u9375\u3092\u624b\u306b\u5165\u308c\u305f\u3002";
        this.strMessage[0][135] = "Got a red key.";
        this.strMessage[1][136] = "\u6249\u304c\u958b\u3044\u305f\u3002";
        this.strMessage[0][136] = "The door has opened.";
        this.strMessage[1][137] = "\u9752\u8272\u306e\u6249\u304c\u958b\u3044\u305f\u3002";
        this.strMessage[0][137] = "The blue door has opened.";
        this.strMessage[1][138] = "\u8d64\u8272\u306e\u6249\u304c\u958b\u3044\u305f\u3002";
        this.strMessage[0][138] = "The red door has opened.";
        this.mapAttribute[4][3] = 2;
        this.mapAttribute[4][1] = 34;
        this.mapAttribute[4][2] = 0;
        this.mapAttribute[4][6] = 280;
        this.mapAttribute[4][7] = 160;
        this.mapAttribute[4][5] = 139;
        this.mapAttribute[4][10] = 2;
        this.mapAttribute[4][16] = 14;
        this.mapAttribute[4][17] = 2;
        this.mapAttribute[6][3] = 2;
        this.mapAttribute[6][1] = 34;
        this.mapAttribute[6][2] = 0;
        this.mapAttribute[6][5] = 139;
        this.mapAttribute[6][10] = 6;
        this.mapAttribute[6][16] = 28;
        this.mapAttribute[6][17] = 11;
        this.mapAttribute[8][3] = 2;
        this.mapAttribute[8][1] = 34;
        this.mapAttribute[8][2] = 0;
        this.mapAttribute[8][5] = 139;
        this.mapAttribute[8][10] = 8;
        this.mapAttribute[8][16] = 50;
        this.mapAttribute[8][17] = 10;
        this.mapAttribute[10][3] = 2;
        this.mapAttribute[10][1] = 34;
        this.mapAttribute[10][2] = 0;
        this.mapAttribute[10][5] = 139;
        this.mapAttribute[10][10] = 6;
        this.mapAttribute[10][16] = 54;
        this.mapAttribute[10][17] = 11;
        this.mapAttribute[12][3] = 2;
        this.mapAttribute[12][1] = 34;
        this.mapAttribute[12][2] = 0;
        this.mapAttribute[12][5] = 139;
        this.mapAttribute[12][10] = 2;
        this.mapAttribute[12][16] = 66;
        this.mapAttribute[12][17] = 2;
        this.mapAttribute[14][3] = 2;
        this.mapAttribute[14][1] = 34;
        this.mapAttribute[14][2] = 0;
        this.mapAttribute[14][5] = 139;
        this.mapAttribute[14][10] = 8;
        this.mapAttribute[14][16] = 89;
        this.mapAttribute[14][17] = 10;
        this.mapAttribute[16][3] = 2;
        this.mapAttribute[16][1] = 34;
        this.mapAttribute[16][2] = 0;
        this.mapAttribute[16][5] = 139;
        this.mapAttribute[16][10] = 2;
        this.mapAttribute[16][16] = 92;
        this.mapAttribute[16][17] = 2;
        this.mapAttribute[18][3] = 2;
        this.mapAttribute[18][1] = 34;
        this.mapAttribute[18][2] = 0;
        this.mapAttribute[18][5] = 139;
        this.mapAttribute[18][10] = 2;
        this.mapAttribute[18][16] = 110;
        this.mapAttribute[18][17] = 2;
        this.mapAttribute[20][3] = 2;
        this.mapAttribute[20][1] = 34;
        this.mapAttribute[20][2] = 0;
        this.mapAttribute[20][5] = 139;
        this.mapAttribute[20][10] = 8;
        this.mapAttribute[20][16] = 118;
        this.mapAttribute[20][17] = 10;
        this.mapAttribute[22][3] = 2;
        this.mapAttribute[22][1] = 34;
        this.mapAttribute[22][2] = 0;
        this.mapAttribute[22][5] = 139;
        this.mapAttribute[22][10] = 8;
        this.mapAttribute[22][16] = 6;
        this.mapAttribute[22][17] = 23;
        this.mapAttribute[24][3] = 2;
        this.mapAttribute[24][1] = 34;
        this.mapAttribute[24][2] = 0;
        this.mapAttribute[24][5] = 139;
        this.mapAttribute[24][10] = 4;
        this.mapAttribute[24][16] = 23;
        this.mapAttribute[24][17] = 24;
        this.mapAttribute[26][3] = 2;
        this.mapAttribute[26][1] = 34;
        this.mapAttribute[26][2] = 0;
        this.mapAttribute[26][5] = 139;
        this.mapAttribute[26][10] = 6;
        this.mapAttribute[26][16] = 28;
        this.mapAttribute[26][17] = 24;
        this.mapAttribute[28][3] = 2;
        this.mapAttribute[28][1] = 34;
        this.mapAttribute[28][2] = 0;
        this.mapAttribute[28][5] = 139;
        this.mapAttribute[28][10] = 4;
        this.mapAttribute[28][16] = 49;
        this.mapAttribute[28][17] = 24;
        this.mapAttribute[38][3] = 2;
        this.mapAttribute[38][1] = 34;
        this.mapAttribute[38][2] = 0;
        this.mapAttribute[38][5] = 139;
        this.mapAttribute[38][10] = 8;
        this.mapAttribute[38][16] = 58;
        this.mapAttribute[38][17] = 23;
        this.mapAttribute[40][3] = 2;
        this.mapAttribute[40][1] = 34;
        this.mapAttribute[40][2] = 0;
        this.mapAttribute[40][5] = 139;
        this.mapAttribute[40][10] = 2;
        this.mapAttribute[40][16] = 71;
        this.mapAttribute[40][17] = 15;
        this.mapAttribute[42][3] = 2;
        this.mapAttribute[42][1] = 34;
        this.mapAttribute[42][2] = 0;
        this.mapAttribute[42][5] = 139;
        this.mapAttribute[42][10] = 8;
        this.mapAttribute[42][16] = 84;
        this.mapAttribute[42][17] = 23;
        this.mapAttribute[44][3] = 2;
        this.mapAttribute[44][1] = 34;
        this.mapAttribute[44][2] = 0;
        this.mapAttribute[44][5] = 139;
        this.mapAttribute[44][10] = 2;
        this.mapAttribute[44][16] = 97;
        this.mapAttribute[44][17] = 15;
        this.mapAttribute[46][3] = 2;
        this.mapAttribute[46][1] = 34;
        this.mapAttribute[46][2] = 0;
        this.mapAttribute[46][5] = 139;
        this.mapAttribute[46][10] = 2;
        this.mapAttribute[46][16] = 105;
        this.mapAttribute[46][17] = 15;
        this.mapAttribute[48][3] = 2;
        this.mapAttribute[48][1] = 34;
        this.mapAttribute[48][2] = 0;
        this.mapAttribute[48][5] = 139;
        this.mapAttribute[48][10] = 8;
        this.mapAttribute[48][16] = 123;
        this.mapAttribute[48][17] = 23;
        this.mapAttribute[50][3] = 2;
        this.mapAttribute[50][1] = 34;
        this.mapAttribute[50][2] = 0;
        this.mapAttribute[50][5] = 139;
        this.mapAttribute[50][10] = 2;
        this.mapAttribute[50][16] = 6;
        this.mapAttribute[50][17] = 28;
        this.mapAttribute[52][3] = 2;
        this.mapAttribute[52][1] = 34;
        this.mapAttribute[52][2] = 0;
        this.mapAttribute[52][5] = 139;
        this.mapAttribute[52][10] = 8;
        this.mapAttribute[52][16] = 19;
        this.mapAttribute[52][17] = 36;
        this.mapAttribute[54][3] = 2;
        this.mapAttribute[54][1] = 34;
        this.mapAttribute[54][2] = 0;
        this.mapAttribute[54][5] = 139;
        this.mapAttribute[54][10] = 2;
        this.mapAttribute[54][16] = 27;
        this.mapAttribute[54][17] = 28;
        this.mapAttribute[56][3] = 2;
        this.mapAttribute[56][1] = 34;
        this.mapAttribute[56][2] = 0;
        this.mapAttribute[56][5] = 139;
        this.mapAttribute[56][10] = 6;
        this.mapAttribute[56][16] = 41;
        this.mapAttribute[56][17] = 37;
        this.mapAttribute[58][3] = 2;
        this.mapAttribute[58][1] = 34;
        this.mapAttribute[58][2] = 0;
        this.mapAttribute[58][5] = 139;
        this.mapAttribute[58][10] = 2;
        this.mapAttribute[58][16] = 54;
        this.mapAttribute[58][17] = 37;
        this.mapAttribute[60][3] = 2;
        this.mapAttribute[60][1] = 34;
        this.mapAttribute[60][2] = 0;
        this.mapAttribute[60][5] = 139;
        this.mapAttribute[60][10] = 6;
        this.mapAttribute[60][16] = 67;
        this.mapAttribute[60][17] = 37;
        this.mapAttribute[62][3] = 2;
        this.mapAttribute[62][1] = 34;
        this.mapAttribute[62][2] = 0;
        this.mapAttribute[62][5] = 139;
        this.mapAttribute[62][10] = 6;
        this.mapAttribute[62][16] = 80;
        this.mapAttribute[62][17] = 37;
        this.mapAttribute[64][3] = 2;
        this.mapAttribute[64][1] = 34;
        this.mapAttribute[64][2] = 0;
        this.mapAttribute[64][5] = 139;
        this.mapAttribute[64][10] = 4;
        this.mapAttribute[64][16] = 101;
        this.mapAttribute[64][17] = 37;
        this.mapAttribute[66][3] = 2;
        this.mapAttribute[66][1] = 34;
        this.mapAttribute[66][2] = 0;
        this.mapAttribute[66][5] = 139;
        this.mapAttribute[66][10] = 8;
        this.mapAttribute[66][16] = 105;
        this.mapAttribute[66][17] = 36;
        this.mapAttribute[68][3] = 2;
        this.mapAttribute[68][1] = 34;
        this.mapAttribute[68][2] = 0;
        this.mapAttribute[68][5] = 139;
        this.mapAttribute[68][10] = 8;
        this.mapAttribute[68][16] = 123;
        this.mapAttribute[68][17] = 36;
        this.mapAttribute[70][3] = 2;
        this.mapAttribute[70][1] = 34;
        this.mapAttribute[70][2] = 0;
        this.mapAttribute[70][5] = 139;
        this.mapAttribute[70][10] = 2;
        this.mapAttribute[70][16] = 6;
        this.mapAttribute[70][17] = 41;
        this.mapAttribute[72][3] = 2;
        this.mapAttribute[72][1] = 34;
        this.mapAttribute[72][2] = 0;
        this.mapAttribute[72][5] = 139;
        this.mapAttribute[72][10] = 8;
        this.mapAttribute[72][16] = 19;
        this.mapAttribute[72][17] = 49;
        this.mapAttribute[74][3] = 2;
        this.mapAttribute[74][1] = 34;
        this.mapAttribute[74][2] = 0;
        this.mapAttribute[74][5] = 139;
        this.mapAttribute[74][10] = 4;
        this.mapAttribute[74][16] = 36;
        this.mapAttribute[74][17] = 40;
        this.mapAttribute[76][3] = 2;
        this.mapAttribute[76][1] = 34;
        this.mapAttribute[76][2] = 0;
        this.mapAttribute[76][5] = 139;
        this.mapAttribute[76][10] = 6;
        this.mapAttribute[76][16] = 41;
        this.mapAttribute[76][17] = 40;
        this.mapAttribute[78][3] = 2;
        this.mapAttribute[78][1] = 34;
        this.mapAttribute[78][2] = 0;
        this.mapAttribute[78][5] = 139;
        this.mapAttribute[78][10] = 8;
        this.mapAttribute[78][16] = 58;
        this.mapAttribute[78][17] = 49;
        this.mapAttribute[80][3] = 2;
        this.mapAttribute[80][1] = 34;
        this.mapAttribute[80][2] = 0;
        this.mapAttribute[80][5] = 139;
        this.mapAttribute[80][10] = 2;
        this.mapAttribute[80][16] = 76;
        this.mapAttribute[80][17] = 41;
        this.mapAttribute[82][3] = 2;
        this.mapAttribute[82][1] = 34;
        this.mapAttribute[82][2] = 0;
        this.mapAttribute[82][5] = 139;
        this.mapAttribute[82][10] = 8;
        this.mapAttribute[82][16] = 89;
        this.mapAttribute[82][17] = 49;
        this.mapAttribute[84][3] = 2;
        this.mapAttribute[84][1] = 34;
        this.mapAttribute[84][2] = 0;
        this.mapAttribute[84][5] = 139;
        this.mapAttribute[84][10] = 6;
        this.mapAttribute[84][16] = 93;
        this.mapAttribute[84][17] = 40;
        this.mapAttribute[86][3] = 2;
        this.mapAttribute[86][1] = 34;
        this.mapAttribute[86][2] = 0;
        this.mapAttribute[86][5] = 139;
        this.mapAttribute[86][10] = 2;
        this.mapAttribute[86][16] = 115;
        this.mapAttribute[86][17] = 41;
        this.mapAttribute[88][3] = 2;
        this.mapAttribute[88][1] = 34;
        this.mapAttribute[88][2] = 0;
        this.mapAttribute[88][5] = 139;
        this.mapAttribute[88][10] = 4;
        this.mapAttribute[88][16] = 127;
        this.mapAttribute[88][17] = 50;
        this.mapAttribute[90][3] = 2;
        this.mapAttribute[90][1] = 34;
        this.mapAttribute[90][2] = 0;
        this.mapAttribute[90][5] = 139;
        this.mapAttribute[90][10] = 2;
        this.mapAttribute[90][16] = 6;
        this.mapAttribute[90][17] = 54;
        this.mapAttribute[92][3] = 2;
        this.mapAttribute[92][1] = 34;
        this.mapAttribute[92][2] = 0;
        this.mapAttribute[92][5] = 139;
        this.mapAttribute[92][10] = 8;
        this.mapAttribute[92][16] = 19;
        this.mapAttribute[92][17] = 62;
        this.mapAttribute[94][3] = 2;
        this.mapAttribute[94][1] = 34;
        this.mapAttribute[94][2] = 0;
        this.mapAttribute[94][5] = 139;
        this.mapAttribute[94][10] = 2;
        this.mapAttribute[94][16] = 27;
        this.mapAttribute[94][17] = 54;
        this.mapAttribute[96][3] = 2;
        this.mapAttribute[96][1] = 34;
        this.mapAttribute[96][2] = 0;
        this.mapAttribute[96][5] = 139;
        this.mapAttribute[96][10] = 6;
        this.mapAttribute[96][16] = 54;
        this.mapAttribute[96][17] = 53;
        this.mapAttribute[98][3] = 2;
        this.mapAttribute[98][1] = 34;
        this.mapAttribute[98][2] = 0;
        this.mapAttribute[98][5] = 139;
        this.mapAttribute[98][10] = 6;
        this.mapAttribute[98][16] = 54;
        this.mapAttribute[98][17] = 53;
        this.mapAttribute[100][3] = 2;
        this.mapAttribute[100][1] = 34;
        this.mapAttribute[100][2] = 0;
        this.mapAttribute[100][5] = 139;
        this.mapAttribute[100][10] = 2;
        this.mapAttribute[100][16] = 76;
        this.mapAttribute[100][17] = 54;
        this.mapAttribute[102][3] = 2;
        this.mapAttribute[102][1] = 34;
        this.mapAttribute[102][2] = 0;
        this.mapAttribute[102][5] = 139;
        this.mapAttribute[102][10] = 4;
        this.mapAttribute[102][16] = 88;
        this.mapAttribute[102][17] = 63;
        this.mapAttribute[104][3] = 2;
        this.mapAttribute[104][1] = 34;
        this.mapAttribute[104][2] = 0;
        this.mapAttribute[104][5] = 139;
        this.mapAttribute[104][10] = 8;
        this.mapAttribute[104][16] = 102;
        this.mapAttribute[104][17] = 62;
        this.mapAttribute[106][3] = 2;
        this.mapAttribute[106][1] = 34;
        this.mapAttribute[106][2] = 0;
        this.mapAttribute[106][5] = 139;
        this.mapAttribute[106][10] = 6;
        this.mapAttribute[106][16] = 106;
        this.mapAttribute[106][17] = 63;
        this.mapAttribute[108][3] = 2;
        this.mapAttribute[108][1] = 34;
        this.mapAttribute[108][2] = 0;
        this.mapAttribute[108][5] = 139;
        this.mapAttribute[108][10] = 8;
        this.mapAttribute[108][16] = 123;
        this.mapAttribute[108][17] = 59;
        this.mapAttribute[110][3] = 2;
        this.mapAttribute[110][1] = 34;
        this.mapAttribute[110][2] = 0;
        this.mapAttribute[110][5] = 139;
        this.mapAttribute[110][10] = 2;
        this.mapAttribute[110][16] = 2;
        this.mapAttribute[110][17] = 1;
        this.strMessage[1][139] = "\u968e\u6bb5\u3092\u4e0a\u3063\u305f\u3002";
        this.strMessage[0][139] = "Went up the stairs.";
        this.mapAttribute[5][3] = 2;
        this.mapAttribute[5][1] = 35;
        this.mapAttribute[5][2] = 0;
        this.mapAttribute[5][6] = 320;
        this.mapAttribute[5][7] = 160;
        this.mapAttribute[5][5] = 140;
        this.mapAttribute[5][10] = 6;
        this.mapAttribute[5][16] = 2;
        this.mapAttribute[5][17] = 1;
        this.mapAttribute[7][3] = 2;
        this.mapAttribute[7][1] = 35;
        this.mapAttribute[7][2] = 0;
        this.mapAttribute[7][5] = 140;
        this.mapAttribute[7][10] = 8;
        this.mapAttribute[7][16] = 14;
        this.mapAttribute[7][17] = 10;
        this.mapAttribute[9][3] = 2;
        this.mapAttribute[9][1] = 35;
        this.mapAttribute[9][2] = 0;
        this.mapAttribute[9][5] = 140;
        this.mapAttribute[9][10] = 4;
        this.mapAttribute[9][16] = 36;
        this.mapAttribute[9][17] = 11;
        this.mapAttribute[11][3] = 2;
        this.mapAttribute[11][1] = 35;
        this.mapAttribute[11][2] = 0;
        this.mapAttribute[11][5] = 140;
        this.mapAttribute[11][10] = 8;
        this.mapAttribute[11][16] = 40;
        this.mapAttribute[11][17] = 10;
        this.mapAttribute[13][3] = 2;
        this.mapAttribute[13][1] = 35;
        this.mapAttribute[13][2] = 0;
        this.mapAttribute[13][5] = 140;
        this.mapAttribute[13][10] = 2;
        this.mapAttribute[13][16] = 53;
        this.mapAttribute[13][17] = 2;
        this.mapAttribute[15][3] = 2;
        this.mapAttribute[15][1] = 35;
        this.mapAttribute[15][2] = 0;
        this.mapAttribute[15][5] = 140;
        this.mapAttribute[15][10] = 8;
        this.mapAttribute[15][16] = 76;
        this.mapAttribute[15][17] = 10;
        this.mapAttribute[17][3] = 2;
        this.mapAttribute[17][1] = 35;
        this.mapAttribute[17][2] = 0;
        this.mapAttribute[17][5] = 140;
        this.mapAttribute[17][10] = 2;
        this.mapAttribute[17][16] = 79;
        this.mapAttribute[17][17] = 2;
        this.mapAttribute[19][3] = 2;
        this.mapAttribute[19][1] = 35;
        this.mapAttribute[19][2] = 0;
        this.mapAttribute[19][5] = 140;
        this.mapAttribute[19][10] = 2;
        this.mapAttribute[19][16] = 97;
        this.mapAttribute[19][17] = 2;
        this.mapAttribute[21][3] = 2;
        this.mapAttribute[21][1] = 35;
        this.mapAttribute[21][2] = 0;
        this.mapAttribute[21][5] = 140;
        this.mapAttribute[21][10] = 8;
        this.mapAttribute[21][16] = 105;
        this.mapAttribute[21][17] = 10;
        this.mapAttribute[23][3] = 2;
        this.mapAttribute[23][1] = 35;
        this.mapAttribute[23][2] = 0;
        this.mapAttribute[23][5] = 140;
        this.mapAttribute[23][10] = 8;
        this.mapAttribute[23][16] = 123;
        this.mapAttribute[23][17] = 10;
        this.mapAttribute[25][3] = 2;
        this.mapAttribute[25][1] = 35;
        this.mapAttribute[25][2] = 0;
        this.mapAttribute[25][5] = 140;
        this.mapAttribute[25][10] = 8;
        this.mapAttribute[25][16] = 11;
        this.mapAttribute[25][17] = 23;
        this.mapAttribute[27][3] = 2;
        this.mapAttribute[27][1] = 35;
        this.mapAttribute[27][2] = 0;
        this.mapAttribute[27][5] = 140;
        this.mapAttribute[27][10] = 6;
        this.mapAttribute[27][16] = 15;
        this.mapAttribute[27][17] = 24;
        this.mapAttribute[29][3] = 2;
        this.mapAttribute[29][1] = 35;
        this.mapAttribute[29][2] = 0;
        this.mapAttribute[29][5] = 140;
        this.mapAttribute[29][10] = 4;
        this.mapAttribute[29][16] = 36;
        this.mapAttribute[29][17] = 24;
        this.mapAttribute[39][3] = 2;
        this.mapAttribute[39][1] = 35;
        this.mapAttribute[39][2] = 0;
        this.mapAttribute[39][5] = 140;
        this.mapAttribute[39][10] = 8;
        this.mapAttribute[39][16] = 45;
        this.mapAttribute[39][17] = 23;
        this.mapAttribute[41][3] = 2;
        this.mapAttribute[41][1] = 35;
        this.mapAttribute[41][2] = 0;
        this.mapAttribute[41][5] = 140;
        this.mapAttribute[41][10] = 2;
        this.mapAttribute[41][16] = 58;
        this.mapAttribute[41][17] = 15;
        this.mapAttribute[43][3] = 2;
        this.mapAttribute[43][1] = 35;
        this.mapAttribute[43][2] = 0;
        this.mapAttribute[43][5] = 140;
        this.mapAttribute[43][10] = 8;
        this.mapAttribute[43][16] = 71;
        this.mapAttribute[43][17] = 23;
        this.mapAttribute[45][3] = 2;
        this.mapAttribute[45][1] = 35;
        this.mapAttribute[45][2] = 0;
        this.mapAttribute[45][5] = 140;
        this.mapAttribute[45][10] = 2;
        this.mapAttribute[45][16] = 84;
        this.mapAttribute[45][17] = 15;
        this.mapAttribute[47][3] = 2;
        this.mapAttribute[47][1] = 35;
        this.mapAttribute[47][2] = 0;
        this.mapAttribute[47][5] = 140;
        this.mapAttribute[47][10] = 2;
        this.mapAttribute[47][16] = 92;
        this.mapAttribute[47][17] = 15;
        this.mapAttribute[49][3] = 2;
        this.mapAttribute[49][1] = 35;
        this.mapAttribute[49][2] = 0;
        this.mapAttribute[49][5] = 140;
        this.mapAttribute[49][10] = 8;
        this.mapAttribute[49][16] = 110;
        this.mapAttribute[49][17] = 23;
        this.mapAttribute[51][3] = 2;
        this.mapAttribute[51][1] = 35;
        this.mapAttribute[51][2] = 0;
        this.mapAttribute[51][5] = 140;
        this.mapAttribute[51][10] = 2;
        this.mapAttribute[51][16] = 123;
        this.mapAttribute[51][17] = 15;
        this.mapAttribute[53][3] = 2;
        this.mapAttribute[53][1] = 35;
        this.mapAttribute[53][2] = 0;
        this.mapAttribute[53][5] = 140;
        this.mapAttribute[53][10] = 8;
        this.mapAttribute[53][16] = 6;
        this.mapAttribute[53][17] = 36;
        this.mapAttribute[55][3] = 2;
        this.mapAttribute[55][1] = 35;
        this.mapAttribute[55][2] = 0;
        this.mapAttribute[55][5] = 140;
        this.mapAttribute[55][10] = 2;
        this.mapAttribute[55][16] = 19;
        this.mapAttribute[55][17] = 33;
        this.mapAttribute[57][3] = 2;
        this.mapAttribute[57][1] = 35;
        this.mapAttribute[57][2] = 0;
        this.mapAttribute[57][5] = 140;
        this.mapAttribute[57][10] = 2;
        this.mapAttribute[57][16] = 37;
        this.mapAttribute[57][17] = 28;
        this.mapAttribute[59][3] = 2;
        this.mapAttribute[59][1] = 35;
        this.mapAttribute[59][2] = 0;
        this.mapAttribute[59][5] = 140;
        this.mapAttribute[59][10] = 2;
        this.mapAttribute[59][16] = 41;
        this.mapAttribute[59][17] = 37;
        this.mapAttribute[61][3] = 2;
        this.mapAttribute[61][1] = 35;
        this.mapAttribute[61][2] = 0;
        this.mapAttribute[61][5] = 140;
        this.mapAttribute[61][10] = 6;
        this.mapAttribute[61][16] = 54;
        this.mapAttribute[61][17] = 37;
        this.mapAttribute[63][3] = 2;
        this.mapAttribute[63][1] = 35;
        this.mapAttribute[63][2] = 0;
        this.mapAttribute[63][5] = 140;
        this.mapAttribute[63][10] = 2;
        this.mapAttribute[63][16] = 67;
        this.mapAttribute[63][17] = 37;
        this.mapAttribute[65][3] = 2;
        this.mapAttribute[65][1] = 35;
        this.mapAttribute[65][2] = 0;
        this.mapAttribute[65][5] = 140;
        this.mapAttribute[65][10] = 4;
        this.mapAttribute[65][16] = 88;
        this.mapAttribute[65][17] = 37;
        this.mapAttribute[67][3] = 2;
        this.mapAttribute[67][1] = 35;
        this.mapAttribute[67][2] = 0;
        this.mapAttribute[67][5] = 140;
        this.mapAttribute[67][10] = 6;
        this.mapAttribute[67][16] = 93;
        this.mapAttribute[67][17] = 37;
        this.mapAttribute[69][3] = 2;
        this.mapAttribute[69][1] = 35;
        this.mapAttribute[69][2] = 0;
        this.mapAttribute[69][5] = 140;
        this.mapAttribute[69][10] = 8;
        this.mapAttribute[69][16] = 110;
        this.mapAttribute[69][17] = 36;
        this.mapAttribute[71][3] = 2;
        this.mapAttribute[71][1] = 35;
        this.mapAttribute[71][2] = 0;
        this.mapAttribute[71][5] = 140;
        this.mapAttribute[71][10] = 2;
        this.mapAttribute[71][16] = 123;
        this.mapAttribute[71][17] = 28;
        this.mapAttribute[73][3] = 2;
        this.mapAttribute[73][1] = 35;
        this.mapAttribute[73][2] = 0;
        this.mapAttribute[73][5] = 140;
        this.mapAttribute[73][10] = 8;
        this.mapAttribute[73][16] = 6;
        this.mapAttribute[73][17] = 49;
        this.mapAttribute[75][3] = 2;
        this.mapAttribute[75][1] = 35;
        this.mapAttribute[75][2] = 0;
        this.mapAttribute[75][5] = 140;
        this.mapAttribute[75][10] = 4;
        this.mapAttribute[75][16] = 23;
        this.mapAttribute[75][17] = 40;
        this.mapAttribute[77][3] = 2;
        this.mapAttribute[77][1] = 35;
        this.mapAttribute[77][2] = 0;
        this.mapAttribute[77][5] = 140;
        this.mapAttribute[77][10] = 6;
        this.mapAttribute[77][16] = 28;
        this.mapAttribute[77][17] = 40;
        this.mapAttribute[79][3] = 2;
        this.mapAttribute[79][1] = 35;
        this.mapAttribute[79][2] = 0;
        this.mapAttribute[79][5] = 140;
        this.mapAttribute[79][10] = 8;
        this.mapAttribute[79][16] = 45;
        this.mapAttribute[79][17] = 49;
        this.mapAttribute[81][3] = 2;
        this.mapAttribute[81][1] = 35;
        this.mapAttribute[81][2] = 0;
        this.mapAttribute[81][5] = 140;
        this.mapAttribute[81][10] = 4;
        this.mapAttribute[81][16] = 62;
        this.mapAttribute[81][17] = 40;
        this.mapAttribute[83][3] = 2;
        this.mapAttribute[83][1] = 35;
        this.mapAttribute[83][2] = 0;
        this.mapAttribute[83][5] = 140;
        this.mapAttribute[83][10] = 8;
        this.mapAttribute[83][16] = 76;
        this.mapAttribute[83][17] = 49;
        this.mapAttribute[85][3] = 2;
        this.mapAttribute[85][1] = 35;
        this.mapAttribute[85][2] = 0;
        this.mapAttribute[85][5] = 140;
        this.mapAttribute[85][10] = 6;
        this.mapAttribute[85][16] = 80;
        this.mapAttribute[85][17] = 40;
        this.mapAttribute[87][3] = 2;
        this.mapAttribute[87][1] = 35;
        this.mapAttribute[87][2] = 0;
        this.mapAttribute[87][5] = 140;
        this.mapAttribute[87][10] = 4;
        this.mapAttribute[87][16] = 101;
        this.mapAttribute[87][17] = 40;
        this.mapAttribute[89][3] = 2;
        this.mapAttribute[89][1] = 35;
        this.mapAttribute[89][2] = 0;
        this.mapAttribute[89][5] = 140;
        this.mapAttribute[89][10] = 4;
        this.mapAttribute[89][16] = 114;
        this.mapAttribute[89][17] = 50;
        this.mapAttribute[91][3] = 2;
        this.mapAttribute[91][1] = 35;
        this.mapAttribute[91][2] = 0;
        this.mapAttribute[91][5] = 140;
        this.mapAttribute[91][10] = 2;
        this.mapAttribute[91][16] = 122;
        this.mapAttribute[91][17] = 40;
        this.mapAttribute[93][3] = 2;
        this.mapAttribute[93][1] = 35;
        this.mapAttribute[93][2] = 0;
        this.mapAttribute[93][5] = 140;
        this.mapAttribute[93][10] = 8;
        this.mapAttribute[93][16] = 6;
        this.mapAttribute[93][17] = 62;
        this.mapAttribute[95][3] = 2;
        this.mapAttribute[95][1] = 35;
        this.mapAttribute[95][2] = 0;
        this.mapAttribute[95][5] = 140;
        this.mapAttribute[95][10] = 6;
        this.mapAttribute[95][16] = 15;
        this.mapAttribute[95][17] = 53;
        this.mapAttribute[97][3] = 2;
        this.mapAttribute[97][1] = 35;
        this.mapAttribute[97][2] = 0;
        this.mapAttribute[97][5] = 140;
        this.mapAttribute[97][10] = 8;
        this.mapAttribute[97][16] = 27;
        this.mapAttribute[97][17] = 62;
        this.mapAttribute[99][3] = 2;
        this.mapAttribute[99][1] = 35;
        this.mapAttribute[99][2] = 0;
        this.mapAttribute[99][5] = 140;
        this.mapAttribute[99][10] = 8;
        this.mapAttribute[99][16] = 27;
        this.mapAttribute[99][17] = 62;
        this.mapAttribute[101][3] = 2;
        this.mapAttribute[101][1] = 35;
        this.mapAttribute[101][2] = 0;
        this.mapAttribute[101][5] = 140;
        this.mapAttribute[101][10] = 4;
        this.mapAttribute[101][16] = 62;
        this.mapAttribute[101][17] = 53;
        this.mapAttribute[103][3] = 2;
        this.mapAttribute[103][1] = 35;
        this.mapAttribute[103][2] = 0;
        this.mapAttribute[103][5] = 140;
        this.mapAttribute[103][10] = 8;
        this.mapAttribute[103][16] = 76;
        this.mapAttribute[103][17] = 62;
        this.mapAttribute[105][3] = 2;
        this.mapAttribute[105][1] = 35;
        this.mapAttribute[105][2] = 0;
        this.mapAttribute[105][5] = 140;
        this.mapAttribute[105][10] = 2;
        this.mapAttribute[105][16] = 79;
        this.mapAttribute[105][17] = 54;
        this.mapAttribute[107][3] = 2;
        this.mapAttribute[107][1] = 35;
        this.mapAttribute[107][2] = 0;
        this.mapAttribute[107][5] = 140;
        this.mapAttribute[107][10] = 8;
        this.mapAttribute[107][16] = 92;
        this.mapAttribute[107][17] = 62;
        this.mapAttribute[109][3] = 2;
        this.mapAttribute[109][1] = 35;
        this.mapAttribute[109][2] = 0;
        this.mapAttribute[109][5] = 140;
        this.mapAttribute[109][10] = 2;
        this.mapAttribute[109][16] = 105;
        this.mapAttribute[109][17] = 53;
        this.mapAttribute[116][3] = 2;
        this.mapAttribute[116][1] = 32;
        this.mapAttribute[116][2] = 0;
        this.mapAttribute[116][5] = 267;
        this.mapAttribute[116][10] = 0;
        this.mapAttribute[116][16] = 1;
        this.mapAttribute[116][17] = 66;
        this.mapAttribute[117][3] = 2;
        this.mapAttribute[117][1] = 188;
        this.mapAttribute[117][2] = 0;
        this.mapAttribute[117][6] = 0;
        this.mapAttribute[117][7] = 0;
        this.mapAttribute[117][5] = 267;
        this.mapAttribute[117][10] = 8;
        this.mapAttribute[117][16] = 17;
        this.mapAttribute[117][17] = 8;
        this.mapAttribute[118][3] = 0;
        this.mapAttribute[118][1] = 188;
        this.mapAttribute[118][2] = 0;
        this.mapAttribute[118][6] = 0;
        this.mapAttribute[118][7] = 0;
        this.strMessage[1][140] = "\u968e\u6bb5\u3092\u4e0b\u3063\u305f\u3002";
        this.strMessage[0][140] = "Went down the stairs.";
        this.objectAttribute[89][3] = 5;
        this.objectAttribute[89][1] = 33;
        this.objectAttribute[89][2] = 0;
        this.objectAttribute[89][5] = 141;
        this.strMessage[1][141] = "\u58c1\u304c\u304f\u305a\u308c\u305f\uff01";
        this.strMessage[0][141] = "The wall collapsed!";
        this.objectAttribute[24][3] = 4;
        this.objectAttribute[24][1] = 66;
        this.objectAttribute[24][2] = 0;
        this.objectAttribute[24][6] = 160;
        this.objectAttribute[24][7] = 280;
        this.objectAttribute[24][5] = 142;
        this.objectAttribute[24][15] = 1;
        this.strMessage[1][142] = "\u52c7\u8005\u306e\u30aa\u30fc\u30d6\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][142] = "Got the orb of the hero.";
        this.strMessage[1][143] = "\u8001\u4eba\u304c\u3044\u308b\u3002";
        this.strMessage[0][143] = "You see an old man.";
        this.strMessage[1][144] = "\u5546\u4eba\u304c\u3044\u308b\u3002";
        this.strMessage[0][144] = "You see a merchant.";
        this.strMessage[1][145] = "\u5996\u7cbe\u304c\u3044\u308b\u3002";
        this.strMessage[0][145] = "You see a fairy.";
        this.strMessage[1][146] = "\u76d7\u8cca\u304c\u3044\u308b\u3002";
        this.strMessage[0][146] = "You see a thief.";
        this.strMessage[1][147] = "\u6249\u306e\u9375\u304c\u306a\u3044\uff01";
        this.strMessage[0][147] = "Don't have the key.";
        this.strMessage[1][148] = "\u9752\u8272\u306e\u9375\u304c\u306a\u3044\uff01";
        this.strMessage[0][148] = "Don't have the blue key.";
        this.strMessage[1][149] = "\u8d64\u8272\u306e\u9375\u304c\u306a\u3044\uff01";
        this.strMessage[0][149] = "Don't have the red key.";
        this.strMessage[1][150] = "\u968e\u6bb5\u304c\u3042\u308b\u3002";
        this.strMessage[0][150] = "You see stairs.";
        this.strMessage[1][151] = "\u98db\u7fd4\u306e\u30aa\u30fc\u30d6\u306f\u968e\u6bb5\u306e\u3068\u306a\u308a\u3067\u306a\u304f\u3066\u306f\u4f7f\u3048\u306a\u3044\uff01";
        this.strMessage[0][151] = "You must be near the stairs to use the orb of flying!";
        this.objectAttribute[26][3] = 4;
        this.objectAttribute[26][1] = 68;
        this.objectAttribute[26][2] = 0;
        this.objectAttribute[26][6] = 240;
        this.objectAttribute[26][7] = 280;
        this.objectAttribute[26][5] = 152;
        this.objectAttribute[26][15] = 3;
        this.strMessage[1][152] = "\u98db\u7fd4\u306e\u30aa\u30fc\u30d6\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][152] = "Got the orb of flying.";
        this.objectAttribute[25][3] = 4;
        this.objectAttribute[25][1] = 67;
        this.objectAttribute[25][2] = 0;
        this.objectAttribute[25][6] = 200;
        this.objectAttribute[25][7] = 280;
        this.objectAttribute[25][5] = 153;
        this.objectAttribute[25][15] = 2;
        this.strMessage[1][153] = "\u77e5\u6075\u306e\u30aa\u30fc\u30d6\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][153] = "Got the orb of wisdom.";
        this.strMessage[1][154] = "\u98db\u7fd4\u306e\u30aa\u30fc\u30d6\u3092\u4f7f\u3063\u305f\uff01";
        this.strMessage[0][154] = "Used the orb of flying!";
        this.strMessage[1][155] = "\u796d\u58c7\u304c\u3042\u308b\u3002";
        this.strMessage[0][155] = "You see an altar.";
        this.objectAttribute[30][3] = 3;
        this.objectAttribute[30][1] = 81;
        this.objectAttribute[30][2] = 0;
        this.objectAttribute[30][6] = 360;
        this.objectAttribute[30][7] = 320;
        this.objectAttribute[30][5] = 156;
        this.objectAttribute[30][11] = 10;
        this.strMessage[1][156] = "\u9244\u306e\u5263\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u653b\u6483\u529b\u304c\uff11\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][156] = "Got an Iron Sword! Your offensive power was 10 points up!";
        this.objectAttribute[31][3] = 3;
        this.objectAttribute[31][1] = 82;
        this.objectAttribute[31][2] = 0;
        this.objectAttribute[31][6] = 0;
        this.objectAttribute[31][7] = 360;
        this.objectAttribute[31][5] = 157;
        this.objectAttribute[31][11] = 20;
        this.strMessage[1][157] = "\u9280\u306e\u5263\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u653b\u6483\u529b\u304c\uff12\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][157] = "Got a Silver Sword! Your offensive power was 20 points up!";
        this.objectAttribute[32][3] = 3;
        this.objectAttribute[32][1] = 83;
        this.objectAttribute[32][2] = 0;
        this.objectAttribute[32][6] = 40;
        this.objectAttribute[32][7] = 360;
        this.objectAttribute[32][5] = 158;
        this.objectAttribute[32][11] = 40;
        this.strMessage[1][158] = "\u9a0e\u58eb\u306e\u5263\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u653b\u6483\u529b\u304c\uff14\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][158] = "Got a Sword of Knight! Your offensive power was 40 points up!";
        this.objectAttribute[33][3] = 3;
        this.objectAttribute[33][1] = 84;
        this.objectAttribute[33][2] = 0;
        this.objectAttribute[33][6] = 80;
        this.objectAttribute[33][7] = 360;
        this.objectAttribute[33][5] = 159;
        this.objectAttribute[33][11] = 50;
        this.strMessage[1][159] = "\u8056\u3000\u5263\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u653b\u6483\u529b\u304c\uff15\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][159] = "Got a Holy Sword! Your offensive power was 50 points up!";
        this.objectAttribute[34][3] = 3;
        this.objectAttribute[34][1] = 85;
        this.objectAttribute[34][2] = 0;
        this.objectAttribute[34][6] = 120;
        this.objectAttribute[34][7] = 360;
        this.objectAttribute[34][5] = 160;
        this.objectAttribute[34][11] = 100;
        this.strMessage[1][160] = "\u795e\u3000\u5263\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u653b\u6483\u529b\u304c\uff11\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][160] = "Got a Sacred Sword! Your offensive power was 100 points up!";
        this.objectAttribute[35][3] = 3;
        this.objectAttribute[35][1] = 86;
        this.objectAttribute[35][2] = 0;
        this.objectAttribute[35][6] = 160;
        this.objectAttribute[35][7] = 360;
        this.objectAttribute[35][5] = 161;
        this.objectAttribute[35][12] = 10;
        this.strMessage[1][161] = "\u9244\u306e\u76fe\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u9632\u5fa1\u529b\u304c\uff11\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][161] = "Got an Iron Shield! Your defensive power was 10 points up!";
        this.objectAttribute[36][3] = 3;
        this.objectAttribute[36][1] = 87;
        this.objectAttribute[36][2] = 0;
        this.objectAttribute[36][6] = 200;
        this.objectAttribute[36][7] = 360;
        this.objectAttribute[36][5] = 162;
        this.objectAttribute[36][12] = 20;
        this.strMessage[1][162] = "\u9280\u306e\u76fe\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u9632\u5fa1\u529b\u304c\uff12\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][162] = "Got a Silver Shield! Your defensive power was 20 points up!";
        this.objectAttribute[37][3] = 3;
        this.objectAttribute[37][1] = 88;
        this.objectAttribute[37][2] = 0;
        this.objectAttribute[37][6] = 240;
        this.objectAttribute[37][7] = 360;
        this.objectAttribute[37][5] = 163;
        this.objectAttribute[37][12] = 40;
        this.strMessage[1][163] = "\u9a0e\u58eb\u306e\u76fe\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u9632\u5fa1\u529b\uff14\uff10\u304c\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][163] = "Got a Shield of Knight! Your defensive power was 40 points up!";
        this.objectAttribute[38][3] = 3;
        this.objectAttribute[38][1] = 89;
        this.objectAttribute[38][2] = 0;
        this.objectAttribute[38][6] = 280;
        this.objectAttribute[38][7] = 360;
        this.objectAttribute[38][5] = 164;
        this.objectAttribute[38][12] = 50;
        this.strMessage[1][164] = "\u8056\u3000\u76fe\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u9632\u5fa1\u529b\u304c\uff15\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][164] = "Got a Holy Shield! Your defensive power was 50 points up!";
        this.objectAttribute[39][3] = 3;
        this.objectAttribute[39][1] = 90;
        this.objectAttribute[39][2] = 0;
        this.objectAttribute[39][6] = 320;
        this.objectAttribute[39][7] = 360;
        this.objectAttribute[39][5] = 165;
        this.objectAttribute[39][12] = 100;
        this.strMessage[1][165] = "\u795e\u3000\u76fe\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u9632\u5fa1\u529b\u304c\uff11\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][165] = "Got a Sacred Shield! Your defensive power was 100 points up!";
        this.objectAttribute[11][3] = 3;
        this.objectAttribute[11][1] = 62;
        this.objectAttribute[11][2] = 0;
        this.objectAttribute[11][6] = 0;
        this.objectAttribute[11][7] = 280;
        this.objectAttribute[11][5] = 166;
        this.objectAttribute[11][10] = 50;
        this.strMessage[1][166] = "\u8d64\u3044\u56de\u5fa9\u85ac\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u751f\u547d\u529b\u304c\uff15\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][166] = "Got a red elixir. Your vital power was 50 points up!";
        this.objectAttribute[12][3] = 3;
        this.objectAttribute[12][1] = 63;
        this.objectAttribute[12][2] = 0;
        this.objectAttribute[12][6] = 40;
        this.objectAttribute[12][7] = 280;
        this.objectAttribute[12][5] = 167;
        this.objectAttribute[12][10] = 200;
        this.strMessage[1][167] = "\u9752\u3044\u56de\u5fa9\u85ac\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u751f\u547d\u529b\u304c\uff12\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][167] = "Got a blue elixir. Your vital power was 200 points up!";
        this.objectAttribute[13][3] = 3;
        this.objectAttribute[13][1] = 64;
        this.objectAttribute[13][2] = 0;
        this.objectAttribute[13][6] = 80;
        this.objectAttribute[13][7] = 280;
        this.objectAttribute[13][5] = 168;
        this.objectAttribute[13][11] = 1;
        this.strMessage[1][168] = "\u8d64\u306e\u30af\u30ea\u30b9\u30bf\u30eb\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u653b\u6483\u529b\u304c\uff11\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][168] = "Got a red crystal. Your offensive power was 1 point up!";
        this.objectAttribute[14][3] = 3;
        this.objectAttribute[14][1] = 65;
        this.objectAttribute[14][2] = 0;
        this.objectAttribute[14][6] = 120;
        this.objectAttribute[14][7] = 280;
        this.objectAttribute[14][5] = 169;
        this.objectAttribute[14][12] = 1;
        this.strMessage[1][169] = "\u9752\u306e\u30af\u30ea\u30b9\u30bf\u30eb\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u9632\u5fa1\u529b\u304c\uff11\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][169] = "Got a blue crystal. Your defensive power was 1 point up!";
        this.objectAttribute[103][3] = 4;
        this.objectAttribute[103][1] = 69;
        this.objectAttribute[103][2] = 0;
        this.objectAttribute[103][6] = 280;
        this.objectAttribute[103][7] = 280;
        this.objectAttribute[103][5] = 171;
        this.objectAttribute[103][15] = 4;
        this.strMessage[1][171] = "\u5341\u5b57\u67b6\u3092\u624b\u306b\u5165\u308c\u305f\uff01\u30d0\u30f3\u30d1\u30a4\u30a2\u3001\u30be\u30f3\u30d3\u306b\u5bfe\u3059\u308b\u653b\u6483\u529b\u304c\uff12\u500d\u306b\u306a\u3063\u305f\uff01";
        this.strMessage[0][171] = "Got a cross! Your offensive power against Vampires and Zombies has doubled.";
        this.objectAttribute[104][3] = 4;
        this.objectAttribute[104][1] = 70;
        this.objectAttribute[104][2] = 0;
        this.objectAttribute[104][6] = 320;
        this.objectAttribute[104][7] = 280;
        this.objectAttribute[104][5] = 172;
        this.objectAttribute[104][15] = 5;
        this.strMessage[1][172] = "\u30a8\u30ea\u30af\u30b5\u30fc\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][172] = "Recieved the Magic Elixir.";
        this.objectAttribute[114][3] = 4;
        this.objectAttribute[114][1] = 71;
        this.objectAttribute[114][2] = 0;
        this.objectAttribute[114][6] = 360;
        this.objectAttribute[114][7] = 280;
        this.objectAttribute[114][5] = 173;
        this.objectAttribute[114][15] = 6;
        this.strMessage[1][173] = "\u30de\u30c8\u30c3\u30af\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][173] = "Got the Magic Mattock.";
        this.objectAttribute[105][3] = 4;
        this.objectAttribute[105][1] = 72;
        this.objectAttribute[105][2] = 0;
        this.objectAttribute[105][6] = 0;
        this.objectAttribute[105][7] = 320;
        this.objectAttribute[105][5] = 174;
        this.objectAttribute[105][15] = 7;
        this.strMessage[1][174] = "\u7834\u58ca\u306e\u7389\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][174] = "Got the Destructible Ball!";
        this.objectAttribute[106][3] = 4;
        this.objectAttribute[106][1] = 73;
        this.objectAttribute[106][2] = 0;
        this.objectAttribute[106][6] = 40;
        this.objectAttribute[106][7] = 320;
        this.objectAttribute[106][5] = 175;
        this.objectAttribute[106][15] = 8;
        this.strMessage[1][175] = "\u7a7a\u9593\u8ee2\u79fb\u306e\u79d8\u5b9d\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][175] = "Got the Warp Staff!";
        this.objectAttribute[107][3] = 4;
        this.objectAttribute[107][1] = 74;
        this.objectAttribute[107][2] = 0;
        this.objectAttribute[107][6] = 80;
        this.objectAttribute[107][7] = 320;
        this.objectAttribute[107][5] = 176;
        this.objectAttribute[107][15] = 9;
        this.strMessage[1][176] = "\u6607\u83ef\u306e\u7ffc\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][176] = "Got wings to fly up!";
        this.objectAttribute[108][3] = 4;
        this.objectAttribute[108][1] = 75;
        this.objectAttribute[108][2] = 0;
        this.objectAttribute[108][6] = 120;
        this.objectAttribute[108][7] = 320;
        this.objectAttribute[108][5] = 177;
        this.objectAttribute[108][15] = 10;
        this.strMessage[1][177] = "\u964d\u81e8\u306e\u7ffc\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][177] = "Got wings to fly down!";
        this.objectAttribute[109][3] = 4;
        this.objectAttribute[109][1] = 76;
        this.objectAttribute[109][2] = 0;
        this.objectAttribute[109][6] = 160;
        this.objectAttribute[109][7] = 320;
        this.objectAttribute[109][5] = 178;
        this.objectAttribute[109][15] = 11;
        this.strMessage[1][178] = "\u30c9\u30e9\u30b4\u30f3\u30b9\u30ec\u30fc\u30e4\u30fc\u3092\u624b\u306b\u5165\u308c\u305f\uff01\u30c9\u30e9\u30b4\u30f3\u306b\u5bfe\u3059\u308b\u653b\u6483\u529b\u304c\uff12\u500d\u306b\u306a\u3063\u305f\uff01";
        this.strMessage[0][178] = "Got the Dragon Slayer! Your attack power against the Dragon has doubled!";
        this.objectAttribute[110][3] = 4;
        this.objectAttribute[110][1] = 77;
        this.objectAttribute[110][2] = 0;
        this.objectAttribute[110][6] = 200;
        this.objectAttribute[110][7] = 320;
        this.objectAttribute[110][5] = 179;
        this.objectAttribute[110][15] = 12;
        this.strMessage[1][179] = "\u96ea\u306e\u7d50\u6676\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][179] = "Got the snow crystal!";
        this.objectAttribute[111][3] = 4;
        this.objectAttribute[111][1] = 78;
        this.objectAttribute[111][2] = 0;
        this.objectAttribute[111][6] = 240;
        this.objectAttribute[111][7] = 320;
        this.objectAttribute[111][5] = 180;
        this.objectAttribute[111][15] = 13;
        this.strMessage[1][180] = "\u9b54\u6cd5\u306e\u9375\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][180] = "Got the magic key!";
        this.objectAttribute[112][3] = 4;
        this.objectAttribute[112][1] = 79;
        this.objectAttribute[112][2] = 0;
        this.objectAttribute[112][6] = 280;
        this.objectAttribute[112][7] = 320;
        this.objectAttribute[112][5] = 181;
        this.objectAttribute[112][15] = 14;
        this.strMessage[1][181] = "\u30b9\u30fc\u30d1\u30fc\u30de\u30c8\u30c3\u30af\u3092\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][181] = "Got the Super Magic Mattock!";
        this.objectAttribute[113][3] = 4;
        this.objectAttribute[113][1] = 80;
        this.objectAttribute[113][2] = 0;
        this.objectAttribute[113][6] = 320;
        this.objectAttribute[113][7] = 320;
        this.objectAttribute[113][5] = 182;
        this.objectAttribute[113][15] = 15;
        this.strMessage[1][182] = "\u5e78\u904b\u306e\u91d1\u8ca8\u3092\u624b\u306b\u5165\u308c\u305f\uff01\u6575\u304c\u6301\u3063\u3066\u3044\u308b\uff27\uff2f\uff2c\uff24\u6570\u304c\uff12\u500d\u306b\u306a\u308b\u3002";
        this.strMessage[0][182] = "Got the Lucky Gold! You can get twice gold which monster has from now.";
        this.objectAttribute[79][3] = 0;
        this.objectAttribute[79][1] = 41;
        this.objectAttribute[79][2] = 42;
        this.objectAttribute[79][6] = 360;
        this.objectAttribute[79][7] = 160;
        this.objectAttribute[79][8] = 0;
        this.objectAttribute[79][9] = 200;
        this.objectAttribute[79][5] = 183;
        this.strMessage[1][183] = "\u6eb6\u5ca9\u304c\u6d41\u308c\u3066\u3044\u308b\u3002";
        this.strMessage[0][183] = "The lava is really hot.";
        this.strMessage[1][184] = "\u3053\u306e\u968e\u306b\u3044\u308b\u30e2\u30f3\u30b9\u30bf\u30fc\u306e\u751f\u547d\u529b\u3001\u653b\u6483\u529b\u3001\u9632\u5fa1\u529b\u3001\u30d7\u30ec\u30fc\u30e4\u30fc\u306e\u53d7\u3051\u308b\u30c0\u30e1\u30fc\u30b8\u3092\u691c\u7d22";
        this.strMessage[0][184] = "Looking up the results of battling these monsters.";
        this.strMessage[1][185] = "\u547d";
        this.strMessage[0][185] = "Vital power:";
        this.strMessage[1][186] = "\u653b";
        this.strMessage[0][186] = "Offensive power:";
        this.strMessage[1][187] = "\u9632";
        this.strMessage[0][187] = "Defensive power:";
        this.strMessage[1][188] = "\u4e88\u60f3\u30c0\u30e1\u30fc\u30b8";
        this.strMessage[0][188] = "Expected damage:";
        this.strMessage[1][189] = "\u653b\u6483\u4e0d\u53ef\u80fd";
        this.strMessage[0][189] = "Attack is impossible!";
        this.strMessage[1][190] = "\u30a8\u30ea\u30af\u30b5\u30fc\u3092\u4f7f\u3063\u305f\uff01\u751f\u547d\u529b\u304c";
        this.strMessage[0][190] = "Used the Magic Elixir. Your vital power was ";
        this.strMessage[1][191] = "\u30de\u30c8\u30c3\u30af\u3092\u4f7f\u3063\u305f\uff01\u56db\u65b9\u306e\u58c1\u304c\u5d29\u308c\u305f\uff01";
        this.strMessage[0][191] = "Used the Magic Mattock! The walls fell down!";
        this.strMessage[1][192] = "\u7834\u58ca\u306e\u7389\u3092\u4f7f\u3063\u305f\uff01\u56db\u65b9\u306e\u6575\u304c\u5012\u308c\u305f\uff01";
        this.strMessage[0][192] = "Used The Destructible Ball! Enemies on all sides died!";
        this.strMessage[1][193] = "\u7a7a\u9593\u8ee2\u79fb\u3057\u305f\uff01";
        this.strMessage[0][193] = "Warped!";
        this.strMessage[1][194] = "\u6607\u83ef\u306e\u7ffc\u3092\u4f7f\u3063\u305f\uff01";
        this.strMessage[0][194] = "Used the wing to fly up!";
        this.strMessage[1][195] = "\u964d\u81e8\u306e\u7ffc\u3092\u4f7f\u3063\u305f\uff01";
        this.strMessage[0][195] = "Used the wing to fly down!";
        this.strMessage[1][196] = "\u96ea\u306e\u7d50\u6676\u3092\u4f7f\u3063\u305f\uff01";
        this.strMessage[0][196] = "Used the snow crystal!";
        this.strMessage[1][197] = "\u9b54\u6cd5\u306e\u9375\u3092\u4f7f\u3063\u305f\uff01\u3053\u306e\u968e\u306e\u6249\u304c\u3059\u3079\u3066\u958b\u3044\u305f\uff01";
        this.strMessage[0][197] = "Used the Magic Key! All these doors opened on this floor.";
        this.strMessage[1][198] = "\u30b9\u30fc\u30d1\u30fc\u30de\u30c8\u30c3\u30af\u3092\u4f7f\u3063\u305f\uff01\u3053\u306e\u968e\u306e\u58c1\u304c\u3059\u3079\u3066\u5d29\u308c\u305f\uff01";
        this.strMessage[0][198] = "Used the Super Magic Mattock! All the walls fell down on this floor!";
        this.strMessage[1][199] = "\u8ee2\u9001\u5148\u306b\u969c\u5bb3\u7269\u304c\u3042\u3063\u3066\u7a7a\u9593\u8ee2\u79fb\u304c\u3067\u304d\u306a\u3044\uff01";
        this.strMessage[0][199] = "Can't warp (There's an object in the way).";
        this.strMessage[1][200] = "\u4e0a\u306e\u968e\u306b\u969c\u5bb3\u7269\u304c\u3042\u3063\u3066\u8ee2\u79fb\u304c\u3067\u304d\u306a\u3044\uff01";
        this.strMessage[0][200] = "Can't go upstairs (it's blocked)!";
        this.strMessage[1][201] = "\u4e0b\u306e\u968e\u306b\u969c\u5bb3\u7269\u304c\u3042\u3063\u3066\u8ee2\u79fb\u304c\u3067\u304d\u306a\u3044\uff01";
        this.strMessage[0][201] = "Can't go downstairs (it's blocked)!";
        this.strMessage[1][202] = "\u6eb6\u5ca9\u304c\u56fa\u307e\u3063\u3066\u9053\u304c\u3067\u304d\u305f\uff01";
        this.strMessage[0][202] = "The lava cooled and turned to stone.";
        this.strMessage[1][203] = "\u3092\u305f\u304a\u3057\u305f\uff01";
        this.strMessage[0][203] = "You've beat ";
        this.strMessage[1][204] = "\uff27\uff2f\uff2c\uff24\u3092";
        this.strMessage[0][204] = ". Recieved ";
        this.strMessage[1][205] = "\u679a\u624b\u306b\u5165\u308c\u305f\uff01";
        this.strMessage[0][205] = " Gold.";
        this.objectAttribute[22][3] = 7;
        this.objectAttribute[22][1] = 46;
        this.objectAttribute[22][2] = 47;
        this.objectAttribute[22][6] = 160;
        this.objectAttribute[22][7] = 200;
        this.objectAttribute[22][8] = 240;
        this.objectAttribute[22][9] = 200;
        this.objectAttribute[22][5] = 206;
        this.strMessage[1][206] = "\u300c\u3053\u306e\u796d\u58c7\u306b";
        this.strMessage[0][206] = "\"If you offer me ";
        this.strMessage[1][207] = " \uff27\uff2f\uff2c\uff24\u5bc4\u9032\u3059\u308c\u3070\u671b\u307f\u3092\u304b\u306a\u3048\u3066\u3084\u308d\u3046\u3002\u5bc4\u9032\u3059\u308b\u304b\uff1f\u300d";
        this.strMessage[0][207] = " Gold, I will grant your request. Will you?\"";
        this.strMessage[1][208] = "\u300c\u3069\u306e\u671b\u307f\u3092\u304b\u306a\u3048\u3066\u6b32\u3057\u3044\u306e\u3060\uff1f\u300d";
        this.strMessage[0][208] = "\"What option shall you choose?\"";
        this.strMessage[1][209] = "\u30fb\u751f\u547d\u529b\u3092";
        this.strMessage[0][209] = "Your life recovers by ";
        this.strMessage[1][210] = "\u30dd\u30a4\u30f3\u30c8\u56de\u5fa9";
        this.strMessage[0][210] = " points.";
        this.strMessage[1][211] = "\u30fb\u653b\u6483\u529b\u3092";
        this.strMessage[0][211] = "The offensive power is raised ";
        this.strMessage[1][212] = "\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7";
        this.strMessage[0][212] = " points.";
        this.strMessage[1][213] = "\u30fb\u9632\u5fa1\u529b\u3092";
        this.strMessage[0][213] = "The defensive power is raised ";
        this.strMessage[1][214] = "\u30fb\u3084\u3063\u3071\u308a\u3084\u3081\u308b";
        this.strMessage[0][214] = "Then I won't do it after all.";
        this.strMessage[1][215] = "\u300c\u91d1\u304c\u305f\u3089\u3093\uff01\u300d";
        this.strMessage[0][215] = "\"You don't have enough money!\"";
        this.strMessage[1][216] = "\u5854";
        this.strMessage[0][216] = "Tower";
        this.strMessage[1][217] = "\u968e";
        this.strMessage[0][217] = " F";
        this.strMessage[1][218] = "\u751f\u547d\u529b";
        this.strMessage[0][218] = "Life";
        this.strMessage[1][219] = "\u653b\u6483\u529b";
        this.strMessage[0][219] = "Offense";
        this.strMessage[1][220] = "\u9632\u5fa1\u529b";
        this.strMessage[0][220] = "Defense";
        this.strMessage[1][221] = "\u76f8\u624b\u306e\u9632\u5fa1\u529b\u304c\u9ad8\u3059\u304e\u3066\u653b\u6483\u304c\u3067\u304d\u306a\u3044\uff01";
        this.strMessage[0][221] = "You can't battle him. Because his defensive power is too high!";
        this.strMessage[1][222] = "\u52c7\u8005\u300c\u306a\u3093\u3060\u3068\uff5e\uff01\u300d";
        this.strMessage[0][222] = "The brave man says \"What?\"";
        this.strMessage[1][223] = "\u52c7\u8005\u300c\u3042\uff5e\u3063\u300d";
        this.strMessage[0][223] = "The brave man says \"Hey!\"";
        this.objectAttribute[69][3] = 11;
        this.objectAttribute[69][1] = 53;
        this.objectAttribute[69][2] = 54;
        this.objectAttribute[69][6] = 40;
        this.objectAttribute[69][7] = 240;
        this.objectAttribute[69][8] = 80;
        this.objectAttribute[69][9] = 240;
        this.objectAttribute[69][5] = 224;
        this.strMessage[1][224] = "\u300c\u3053\u306e\u968e\u307e\u3067\u306e\u3042\u306a\u305f\u306e\u751f\u547d\u529b\u3001\u9632\u5fa1\u529b\u3001\u653b\u6483\u529b\u3001\u9375\u306e\u500b\u6570\u304b\u3089\u3042\u306a\u305f\u306e\u5b9f\u529b\u3092\u8a55\u4fa1\u3059\u308b\u3068\u30fb\u30fb\u30fb";
        this.strMessage[0][224] = "\"Judging by your vital power, offensive power, defensive power, and number of keys, you have ";
        this.strMessage[1][225] = "\u70b9\u3067\u3059\u3002";
        this.strMessage[0][225] = " points.";
        this.strMessage[1][226] = "\u3046\u30fc\u3093\u3001\u3053\u306e\u70b9\u6570\u3060\u3068\u3053\u308c\u304b\u3089\u5148\u3078\u9032\u3080\u306e\u306f\u3001\u304b\u306a\u308a\u7121\u7406\u304c\u3042\u308b\u3067\u3057\u3087\u3046\u3002\u300d";
        this.strMessage[0][226] = "If you have that many points, you might want to reconsider going higher...\"";
        this.strMessage[1][227] = "\u3044\u307e\u3072\u3068\u3064\u3067\u3059\u306d\u3002\u3053\u308c\u304b\u3089\u5148\u306f\u304b\u306a\u308a\u82e6\u6226\u3059\u308b\u3067\u3057\u3087\u3046\u3002\u300d";
        this.strMessage[0][227] = "A bit below average. Maybe you should try harder.\"";
        this.strMessage[1][228] = "\u307e\u3042\u307e\u3042\u3067\u3059\u306d\u3002\u3053\u306e\u70b9\u6570\u306a\u3089\u3053\u308c\u304b\u3089\u5148\u3082\u306a\u3093\u3068\u304b\u306a\u308b\u3067\u3057\u3087\u3046\u3002\u300d";
        this.strMessage[0][228] = "You are ordinary. You might get by okay!\"";
        this.strMessage[1][229] = "\u306a\u304b\u306a\u304b\u306e\u3082\u306e\u3067\u3059\u3002\u3082\u3046\u5c11\u3057\u9811\u5f35\u308c\u3070\u79f0\u53f7\u3092\u5dee\u3057\u4e0a\u3052\u307e\u3057\u3087\u3046\u3002\u300d";
        this.strMessage[0][229] = "Doing fine! If you wish to continue, I will give you a special rank...\"";
        this.strMessage[1][230] = "\u304a\u3081\u3067\u3068\u3046\uff01\u6e80\u70b9\u3067\u3059\u3002";
        this.strMessage[0][230] = "Congratulations! Your score is GREAT! ";
        this.strMessage[1][231] = "\u3088\u304f\u304c\u3093\u3070\u308a\u307e\u3057\u305f\u306d\u3002";
        this.strMessage[0][231] = "Do you wish to go on? ";
        this.strMessage[1][232] = "\u3042\u306a\u305f\u306b\u306f";
        this.strMessage[0][232] = "I give you the special rank of ";
        this.strMessage[1][233] = "\u300e\u6226\u58eb\u300f";
        this.strMessage[0][233] = "FIGHTER";
        this.strMessage[1][234] = "\u300e\u52c7\u8005\u300f";
        this.strMessage[0][234] = "BRAVE MAN";
        this.strMessage[1][235] = "\u300e\u82f1\u96c4\u300f";
        this.strMessage[0][235] = "HERO";
        this.strMessage[1][236] = "\u300e\u5263\u5e1d\u300f";
        this.strMessage[0][236] = "SWORD EMPEROR";
        this.strMessage[1][237] = "\u300e\u95d8\u795e\u300f";
        this.strMessage[0][237] = "FIGHTER GOD";
        this.strMessage[1][238] = "\u306e\u79f0\u53f7\u3092\u5dee\u3057\u4e0a\u3052\u307e\u3057\u3087\u3046\u3002";
        this.strMessage[0][238] = ". ";
        this.strMessage[1][239] = "\u3053\u308c\u304b\u3089\u5148\u3082\u3053\u306e\u8abf\u5b50\u3067\u306d\u3002\u300d";
        this.strMessage[0][239] = "You may as well play as good as you have from this point on.\"";
        this.strMessage[1][240] = "\u3053\u3053\u307e\u3067\u304a\u3064\u304b\u308c\u3055\u307e\u3067\u3057\u305f\u3002\u300d";
        this.strMessage[0][240] = "It was nice fight so far.\"";
        this.strMessage[1][241] = "\u9b54\u8853\u5e2b\uff21\u306e\u9b54\u6cd5\u653b\u6483\u3060\uff01\u751f\u547d\u529b\u304c\uff12\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u6e1b\u5c11\uff01";
        this.strMessage[0][241] = "Your vital power decreased 200 points by magic attack of Magician A!";
        this.strMessage[1][242] = "\u9b54\u8853\u5e2b\uff22\u306e\u9b54\u6cd5\u653b\u6483\u3060\uff01\u751f\u547d\u529b\u304c\uff11\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u6e1b\u5c11\uff01";
        this.strMessage[0][242] = "Your vital power decreased 100 points by magic attack of Magician B!";
        this.strMessage[1][243] = "\u9b54\u5c0e\u5e2b\u306e\u9b54\u6cd5\u653b\u6483\u3060\uff01\u751f\u547d\u529b\u304c\u534a\u6e1b\uff01";
        this.strMessage[0][243] = "Your vital power decreased in half by the magic attack of Magic Master!";
        this.objectAttribute[50][3] = 6;
        this.objectAttribute[50][1] = 127;
        this.objectAttribute[50][2] = 128;
        this.objectAttribute[50][6] = 200;
        this.objectAttribute[50][7] = 520;
        this.objectAttribute[50][8] = 160;
        this.objectAttribute[50][9] = 560;
        this.objectAttribute[50][5] = 244;
        this.objectAttribute[50][10] = 1200;
        this.objectAttribute[50][11] = 180;
        this.objectAttribute[50][12] = 20;
        this.objectAttribute[50][13] = 50;
        this.objectAttribute[51][3] = 6;
        this.objectAttribute[51][1] = 129;
        this.objectAttribute[51][2] = 130;
        this.objectAttribute[51][6] = 240;
        this.objectAttribute[51][7] = 520;
        this.objectAttribute[51][8] = 200;
        this.objectAttribute[51][9] = 560;
        this.objectAttribute[51][5] = 244;
        this.objectAttribute[51][10] = 1200;
        this.objectAttribute[51][11] = 180;
        this.objectAttribute[51][12] = 20;
        this.objectAttribute[51][13] = 50;
        this.objectAttribute[52][3] = 6;
        this.objectAttribute[52][1] = 131;
        this.objectAttribute[52][2] = 132;
        this.objectAttribute[52][6] = 280;
        this.objectAttribute[52][7] = 520;
        this.objectAttribute[52][8] = 240;
        this.objectAttribute[52][9] = 560;
        this.objectAttribute[52][5] = 244;
        this.objectAttribute[52][10] = 1200;
        this.objectAttribute[52][11] = 180;
        this.objectAttribute[52][12] = 20;
        this.objectAttribute[52][13] = 50;
        this.objectAttribute[60][3] = 6;
        this.objectAttribute[60][1] = 133;
        this.objectAttribute[60][2] = 134;
        this.objectAttribute[60][6] = 320;
        this.objectAttribute[60][7] = 520;
        this.objectAttribute[60][8] = 280;
        this.objectAttribute[60][9] = 560;
        this.objectAttribute[60][5] = 244;
        this.objectAttribute[60][10] = 1200;
        this.objectAttribute[60][11] = 180;
        this.objectAttribute[60][12] = 20;
        this.objectAttribute[60][13] = 50;
        this.objectAttribute[61][3] = 6;
        this.objectAttribute[61][1] = 135;
        this.objectAttribute[61][2] = 136;
        this.objectAttribute[61][6] = 360;
        this.objectAttribute[61][7] = 520;
        this.objectAttribute[61][8] = 320;
        this.objectAttribute[61][9] = 560;
        this.objectAttribute[61][5] = 244;
        this.objectAttribute[61][10] = 1200;
        this.objectAttribute[61][11] = 180;
        this.objectAttribute[61][12] = 20;
        this.objectAttribute[61][13] = 50;
        this.objectAttribute[62][3] = 6;
        this.objectAttribute[62][1] = 137;
        this.objectAttribute[62][2] = 138;
        this.objectAttribute[62][6] = 0;
        this.objectAttribute[62][7] = 560;
        this.objectAttribute[62][8] = 360;
        this.objectAttribute[62][9] = 560;
        this.objectAttribute[62][5] = 244;
        this.objectAttribute[62][10] = 1200;
        this.objectAttribute[62][11] = 180;
        this.objectAttribute[62][12] = 20;
        this.objectAttribute[62][13] = 50;
        this.objectAttribute[70][3] = 6;
        this.objectAttribute[70][1] = 139;
        this.objectAttribute[70][2] = 140;
        this.objectAttribute[70][6] = 40;
        this.objectAttribute[70][7] = 560;
        this.objectAttribute[70][8] = 0;
        this.objectAttribute[70][9] = 600;
        this.objectAttribute[70][5] = 244;
        this.objectAttribute[70][10] = 1200;
        this.objectAttribute[70][11] = 180;
        this.objectAttribute[70][12] = 20;
        this.objectAttribute[70][13] = 50;
        this.objectAttribute[72][3] = 6;
        this.objectAttribute[72][1] = 143;
        this.objectAttribute[72][2] = 144;
        this.objectAttribute[72][6] = 120;
        this.objectAttribute[72][7] = 560;
        this.objectAttribute[72][8] = 80;
        this.objectAttribute[72][9] = 600;
        this.objectAttribute[72][5] = 244;
        this.objectAttribute[72][10] = 1200;
        this.objectAttribute[72][11] = 180;
        this.objectAttribute[72][12] = 20;
        this.objectAttribute[72][13] = 50;
        this.strMessage[1][244] = "\u5927\u30c0\u30b3\u306e\u4e00\u90e8";
        this.strMessage[0][244] = "some of Giant Octopus";
        this.strMessage[1][245] = "\u9053\u304c\u58c1\u306b\u5909\u308f\u3063\u305f\uff01";
        this.strMessage[0][245] = "The road changed to the wall!";
        this.strMessage[1][246] = "\u30bb\u30fc\u30d6\u30c7\u30fc\u30bf\u304c\u3042\u308a\u307e\u305b\u3093\u3002";
        this.strMessage[0][246] = "Nobody saved that game yet.";
        this.strMessage[1][247] = "\u968e\u6bb5\u3092\u79fb\u52d5\u4e2d";
        this.strMessage[0][247] = "You are using the stairs.";
        this.strMessage[1][248] = "\u304a\u3081\u3067\u3068\u3046\uff01\u5f97\u70b9\u304c\u7b2c";
        this.strMessage[0][248] = "Congratulations! You win the ";
        this.strMessage[1][249] = "\u4f4d\u306e\u6210\u7e3e\u3067\u3057\u305f\u3002";
        this.strMessage[0][249] = " place with the points which you got.";
        this.strMessage[1][250] = " \u30c7\u30fc\u30bf\u3092\u30ed\u30fc\u30c9(\u8aad\u307f\u8fbc\u307f)\u3057\u307e\u3057\u305f\u3002";
        this.strMessage[0][250] = "Loaded the Game.";
        this.strMessage[1][251] = " \u30c7\u30fc\u30bf\u3092\u30bb\u30fc\u30d6(\u4fdd\u5b58)\u3057\u307e\u3057\u305f\u3002";
        this.strMessage[0][251] = "Saved the Game.";
        this.strMessage[1][252] = " \u9375\u3092\u6301\u3063\u3066\u306a\u3044\u3088\uff01";
        this.strMessage[0][252] = "You don't have a key!";
        this.strMessage[1][253] = "\u3053\u306e\u30c7\u30fc\u30bf\u306f\u30ed\u30fc\u30c9\u3067\u304d\u307e\u305b\u3093\u3002";
        this.strMessage[0][253] = "This Game can't load.";
        this.objectAttribute[66][3] = 3;
        this.objectAttribute[66][1] = 62;
        this.objectAttribute[66][2] = 0;
        this.objectAttribute[66][5] = 254;
        this.objectAttribute[66][19] = 11;
        this.objectAttribute[66][10] = 100;
        this.strMessage[1][254] = "\u8d64\u3044\u56de\u5fa9\u85ac\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u751f\u547d\u529b\u304c\uff11\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][254] = "Got a red elixir. Your vital power was 100 points up!";
        this.objectAttribute[67][3] = 3;
        this.objectAttribute[67][1] = 62;
        this.objectAttribute[67][2] = 0;
        this.objectAttribute[67][5] = 255;
        this.objectAttribute[67][10] = 200;
        this.strMessage[1][255] = "\u8d64\u3044\u56de\u5fa9\u85ac\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u751f\u547d\u529b\u304c\uff12\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][255] = "Got a red elixir. Your vital power was 200 points up!";
        this.objectAttribute[68][3] = 3;
        this.objectAttribute[68][1] = 62;
        this.objectAttribute[68][2] = 0;
        this.objectAttribute[68][5] = 256;
        this.objectAttribute[68][10] = 250;
        this.strMessage[1][256] = "\u8d64\u3044\u56de\u5fa9\u85ac\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u751f\u547d\u529b\u304c\uff12\uff15\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][256] = "Got a red elixir. Your vital power was 250 points up!";
        this.objectAttribute[76][3] = 3;
        this.objectAttribute[76][1] = 63;
        this.objectAttribute[76][2] = 0;
        this.objectAttribute[76][5] = 257;
        this.objectAttribute[76][10] = 400;
        this.strMessage[1][257] = "\u9752\u3044\u56de\u5fa9\u85ac\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u751f\u547d\u529b\u304c\uff14\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][257] = "Got a blue elixir. Your vital power was 400 points up!";
        this.objectAttribute[77][3] = 3;
        this.objectAttribute[77][1] = 63;
        this.objectAttribute[77][2] = 0;
        this.objectAttribute[77][5] = 258;
        this.objectAttribute[77][10] = 800;
        this.strMessage[1][258] = "\u9752\u3044\u56de\u5fa9\u85ac\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u751f\u547d\u529b\u304c\uff18\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][258] = "Got a blue elixir. Your vital power was 800 points up!";
        this.objectAttribute[78][3] = 3;
        this.objectAttribute[78][1] = 63;
        this.objectAttribute[78][2] = 0;
        this.objectAttribute[78][5] = 259;
        this.objectAttribute[78][10] = 1000;
        this.strMessage[1][259] = "\u9752\u3044\u56de\u5fa9\u85ac\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u751f\u547d\u529b\u304c\uff11\uff10\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][259] = "Got a blue elixir. Your vital power was 1000 points up!";
        this.objectAttribute[80][3] = 3;
        this.objectAttribute[80][1] = 64;
        this.objectAttribute[80][2] = 0;
        this.objectAttribute[80][5] = 260;
        this.objectAttribute[80][11] = 2;
        this.strMessage[1][260] = "\u8d64\u306e\u30af\u30ea\u30b9\u30bf\u30eb\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u653b\u6483\u529b\u304c\uff12\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][260] = "Got a red crystal. Your offensive power was 2 points up!";
        this.objectAttribute[81][3] = 3;
        this.objectAttribute[81][1] = 64;
        this.objectAttribute[81][2] = 0;
        this.objectAttribute[81][5] = 261;
        this.objectAttribute[81][11] = 4;
        this.strMessage[1][261] = "\u8d64\u306e\u30af\u30ea\u30b9\u30bf\u30eb\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u653b\u6483\u529b\u304c\uff14\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][261] = "Got a red crystal. Your offensive power was 4 points up!";
        this.objectAttribute[82][3] = 3;
        this.objectAttribute[82][1] = 64;
        this.objectAttribute[82][2] = 0;
        this.objectAttribute[82][5] = 262;
        this.objectAttribute[82][11] = 5;
        this.strMessage[1][262] = "\u8d64\u306e\u30af\u30ea\u30b9\u30bf\u30eb\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u653b\u6483\u529b\u304c\uff15\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][262] = "Got a red crystal. Your offensive power was 5 points up!";
        this.objectAttribute[83][3] = 3;
        this.objectAttribute[83][1] = 65;
        this.objectAttribute[83][2] = 0;
        this.objectAttribute[83][5] = 263;
        this.objectAttribute[83][12] = 2;
        this.strMessage[1][263] = "\u9752\u306e\u30af\u30ea\u30b9\u30bf\u30eb\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u9632\u5fa1\u529b\u304c\uff12\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][263] = "Got a blue crystal. Your defensive power was 2 points up!";
        this.objectAttribute[84][3] = 3;
        this.objectAttribute[84][1] = 65;
        this.objectAttribute[84][2] = 0;
        this.objectAttribute[84][5] = 264;
        this.objectAttribute[84][12] = 4;
        this.strMessage[1][264] = "\u9752\u306e\u30af\u30ea\u30b9\u30bf\u30eb\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u9632\u5fa1\u529b\u304c\uff14\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][264] = "Got a blue crystal. Your defensive power was 4 points up!";
        this.objectAttribute[85][3] = 3;
        this.objectAttribute[85][1] = 65;
        this.objectAttribute[85][2] = 0;
        this.objectAttribute[85][5] = 265;
        this.objectAttribute[85][12] = 5;
        this.strMessage[1][265] = "\u9752\u306e\u30af\u30ea\u30b9\u30bf\u30eb\u3092\u624b\u306b\u5165\u308c\u305f\u3002\u9632\u5fa1\u529b\u304c\uff15\u30dd\u30a4\u30f3\u30c8\u30a2\u30c3\u30d7\uff01";
        this.strMessage[0][265] = "Got a blue crystal. Your defensive power was 5 points up!";
        this.strMessage[1][266] = "\u300c\u30fb\u30fb\u30fb\u300d";
        this.strMessage[0][266] = "\"------\"";
        this.strMessage[1][267] = " ";
        this.strMessage[0][267] = " ";
        this.strMessage[1][268] = "Magic Tower Ver0.8a";
        this.strMessage[1][268] = "Magic Tower Ver0.8a";
        this.strMessage[1][269] = "\u30c9\u30e9\u30b4\u30f3\u304c\u706b\u3092\u5439\u3044\u305f\uff01\u751f\u547d\u529b\u304c\uff11\uff10\uff10\uff10\u30dd\u30a4\u30f3\u30c8\u6e1b\u5c11\uff01";
        this.strMessage[0][269] = "Dragon blew on the fire! Your vital power decreased 1000 points.";
        this.strMessage[1][270] = "\u9244\u306e\u5263";
        this.strMessage[0][270] = "Iron";
        this.strMessage[1][271] = "\u9280\u306e\u5263";
        this.strMessage[0][271] = "Silver";
        this.strMessage[1][272] = "\u9a0e\u58eb\u306e\u5263";
        this.strMessage[0][272] = "Knight";
        this.strMessage[1][273] = "\u8056\u3000\u5263";
        this.strMessage[0][273] = "Holy";
        this.strMessage[1][274] = "\u795e\u3000\u5263";
        this.strMessage[0][274] = "Sacred";
        this.strMessage[1][275] = "\u9244\u306e\u76fe";
        this.strMessage[0][275] = "Iron";
        this.strMessage[1][276] = "\u9280\u306e\u76fe";
        this.strMessage[0][276] = "Silver";
        this.strMessage[1][277] = "\u9a0e\u58eb\u306e\u76fe";
        this.strMessage[0][277] = "Knight";
        this.strMessage[1][278] = "\u8056\u3000\u76fe";
        this.strMessage[0][278] = "Holy";
        this.strMessage[1][279] = "\u795e\u3000\u76fe";
        this.strMessage[0][279] = "Sacred";
        this.strMessage[1][280] = "\u300c\u751f\u547d\u529b\u304c\u306a\u304f\u306a\u308a\u307e\u3057\u305f\u3002\u518d\u6311\u6226\u3057\u3066\u304f\u3060\u3055\u3044\u3002\u300d";
        this.strMessage[0][280] = "\"You have perished in Magic Tower. Please try again!\"";
        this.strMessage[1][281] = "\u4e0a\u66f8\u304d\u3057\u307e\u3059\u3002\u3088\u308d\u3057\u3044\u3067\u3059\u304b\uff1f";
        this.strMessage[0][281] = "Over write. Is it true ?";
        this.strMessage[1][282] = "\u60c5\u5831\u756a\u53f7\u3000";
        this.strMessage[0][282] = "Information No.";
        this.strMessage[1][283] = "\u300c\u9858\u3044\u3092\u304b\u306a\u3048\u305f\u305e\uff01\u300d";
        this.strMessage[0][283] = "\"Your wish came true.\"";
        this.strMessage[1][284] = "\u5b9f\u884c\u4e2d...";
        this.strMessage[0][284] = "Executing...";
        this.strMessage[1][285] = "\u30bb\u30fc\u30d6\u3067\u304d\u307e\u305b\u3093\u3002\u30dd\u30ea\u30b7\u30fc\u30c4\u30fc\u30eb\u3067\u5165\u51fa\u529b\u306e\u8a2d\u5b9a\u3092\u3057\u3066\u4e0b\u3055\u3044\u3002";
        this.strMessage[0][285] = "Can't save this game. Please set by policytool.";
        this.strMessage[1][286] = "\u30e9\u30f3\u30ad\u30f3\u30b0\u30c7\u30fc\u30bf\u3092\u521d\u671f\u5316\u3057\u307e\u3057\u305f\u3002";
        this.strMessage[0][286] = "Initialized Ranking data.";
        this.strMessage[1][287] = "\u30e9\u30f3\u30ad\u30f3\u30b0\u30c7\u30fc\u30bf\u3092\u521d\u671f\u5316\u3067\u304d\u307e\u305b\u3093\u3002\u30dd\u30ea\u30b7\u30fc\u30c4\u30fc\u30eb\u3067\u5165\u51fa\u529b\u306e\u8a2d\u5b9a\u3092\u3057\u3066\u4e0b\u3055\u3044\u3002";
        this.strMessage[0][287] = "Can't initialize this raning data. Please set by policytool.";
        this.strMessage[1][288] = "\u3053\u306e\u30c7\u30fc\u30bf\u306f\u30ed\u30fc\u30c9\u3067\u304d\u307e\u305b\u3093\u3002";
        this.strMessage[0][288] = "This data can't load.";
        this.strMessage[1][289] = "Wav \u30b5\u30a6\u30f3\u30c9\u30aa\u30f3\uff01";
        this.strMessage[0][289] = "Wav sound on.";
        this.strMessage[1][290] = "Midi\u30d0\u30c3\u30af\u30b0\u30e9\u30a6\u30f3\u30c9\u30df\u30e5\u30fc\u30b8\u30c3\u30af\u30aa\u30f3\uff01";
        this.strMessage[0][290] = "Midi Background music on.";
        this.strMessage[1][291] = "\u30b5\u30a6\u30f3\u30c9\u30aa\u30d5\uff01\u3000\uff22\uff27\uff2d\u30aa\u30d5\uff01";
        this.strMessage[0][291] = "Sound and Background music off.";
        this.strMessage[1][292] = "\u30b5\u30a6\u30f3\u30c9\u30aa\u30d5\uff01";
        this.strMessage[0][292] = "Sound off.";
        this.strMessage[1][293] = "\u30d0\u30c3\u30af\u30b0\u30e9\u30a6\u30f3\u30c9\u30df\u30e5\u30fc\u30b8\u30c3\u30af\u30aa\u30d5\uff01";
        this.strMessage[0][293] = "Background music off.";
        this.strMessage[1][294] = "Au \u30b5\u30a6\u30f3\u30c9\u30aa\u30f3\uff01";
        this.strMessage[0][294] = "Au sound on.";
        this.strMessage[1][295] = "Au\u30d0\u30c3\u30af\u30b0\u30e9\u30a6\u30f3\u30c9\u30df\u30e5\u30fc\u30b8\u30c3\u30af\u30aa\u30f3\uff01";
        this.strMessage[0][295] = "Au Background music on.";
        this.strMessage[1][296] = "\u300c\u904a\u3093\u3067\u304f\u308c\u3066\u3042\u308a\u304c\u3068\u3046\uff01\u3000\u307e\u3060\u5b8c\u6210\u3067\u304d\u3066\u3044\u307e\u305b\u3093\u3002\u3000\u697d\u3057\u307f\u306b\u5f85\u3063\u3066\u3044\u3066\u306d\uff01\u300d";
        this.strMessage[0][296] = "\"Thank you for playing this game. Please wait for completing.\"";
        this.strMessage[1][297] = "\u30dd\u30a4\u30f3\u30c8\u56de\u5fa9";
        this.strMessage[0][297] = " points up!";
        this.strMessage[1][298] = "\uff27\uff2f\uff2c\uff24\u3092";
        this.strMessage[0][298] = " Got ";
        this.strMessage[1][299] = "\u52c7\u8005\u306e\u30aa\u30fc\u30d6";
        this.strMessage[0][299] = "The orb of the hero";
        this.strMessage[1][300] = "\u77e5\u6075\u306e\u30aa\u30fc\u30d6";
        this.strMessage[0][300] = "The orb of wisdom";
        this.strMessage[1][301] = "\u98db\u7fd4\u306e\u30aa\u30fc\u30d6";
        this.strMessage[0][301] = "The orb of flying";
        this.strMessage[1][302] = "\u5341\u5b57\u67b6";
        this.strMessage[0][302] = "A cross";
        this.strMessage[1][303] = "\u30a8\u30ea\u30af\u30b5\u30fc";
        this.strMessage[0][303] = "The Magic Elixir";
        this.strMessage[1][304] = "\u30de\u30c8\u30c3\u30af";
        this.strMessage[0][304] = "The Magic Mattock";
        this.strMessage[1][305] = "\u7834\u58ca\u306e\u7389";
        this.strMessage[0][305] = "The Destructible Ball";
        this.strMessage[1][306] = "\u7a7a\u9593\u8ee2\u79fb\u306e\u79d8\u5b9d";
        this.strMessage[0][306] = "The Warp Staff";
        this.strMessage[1][307] = "\u6607\u83ef\u306e\u7ffc";
        this.strMessage[0][307] = "Wings to fly up";
        this.strMessage[1][308] = "\u964d\u81e8\u306e\u7ffc";
        this.strMessage[0][308] = "Wings to fly down";
        this.strMessage[1][309] = "\u30c9\u30e9\u30b4\u30f3\u30b9\u30ec\u30fc\u30e4\u30fc";
        this.strMessage[0][309] = "The Dragon Slayer";
        this.strMessage[1][310] = "\u96ea\u306e\u7d50\u6676";
        this.strMessage[0][310] = "The snow crystal";
        this.strMessage[1][311] = "\u9b54\u6cd5\u306e\u9375";
        this.strMessage[0][311] = "The magic key";
        this.strMessage[1][312] = "\u30b9\u30fc\u30d1\u30fc\u30de\u30c8\u30c3\u30af";
        this.strMessage[0][312] = "The Super Magic Mattock";
        this.strMessage[1][313] = "\u5e78\u904b\u306e\u91d1\u8ca8";
        this.strMessage[0][313] = "The Lucky Gold";
        this.strMessage[1][314] = "\u30a2\u30a4\u30c6\u30e0\u3092\u4f7f\u7528\u3057\u307e\u3059\u3002\u3088\u308d\u3057\u3044\u3067\u3059\u304b\uff1f";
        this.strMessage[0][314] = "Do you use this item?";
    }

    public void graphicLoading(Graphics graphics) {
        int n;
        int n2;
        this.showStatus("Now Loading CG data .....");
        this.imgMap = this.getImage(this.getDocumentBase(), "image/MTower.gif");
        this.tracker.addImage(this.imgMap, 0);
        try {
            this.tracker.waitForID(0);
        }
        catch (InterruptedException interruptedException) {
            System.out.println("Tracker Exception !!!");
        }
        this.showStatus("Now Loading CG data ..... Done.");
        this.showStatus("Now Making character CG .....");
        this.cropID = 0;
        while (this.cropID < 8) {
            this.imgCrop[this.cropID] = this.createImage(new FilteredImageSource(this.imgMap.getSource(), new CropImageFilter(this.cropID * 40 + 80, 0, 40, 40)));
            ++this.cropID;
        }
        int n3 = 0;
        while (n3 < 24) {
            this.imgCrop[this.cropID] = this.createImage(new FilteredImageSource(this.imgMap.getSource(), new CropImageFilter(this.mapFrame[n3][0], this.mapFrame[n3][1], 40, 40)));
            ++n3;
            ++this.cropID;
        }
        n3 = 1;
        while (n3 < 200) {
            n2 = this.mapAttribute[n3][6];
            n = this.mapAttribute[n3][7];
            if ((n2 != 0 || n != 0 || n3 == 118) && this.imgCrop[this.mapAttribute[n3][1]] == null) {
                this.imgCrop[this.mapAttribute[n3][1]] = this.createImage(new FilteredImageSource(this.imgMap.getSource(), new CropImageFilter(n2, n, 40, 40)));
            }
            ++n3;
        }
        n3 = 1;
        while (n3 < 200) {
            n2 = this.objectAttribute[n3][6];
            n = this.objectAttribute[n3][7];
            if ((n2 != 0 || n != 0) && this.imgCrop[this.objectAttribute[n3][1]] == null) {
                this.imgCrop[this.objectAttribute[n3][1]] = this.createImage(new FilteredImageSource(this.imgMap.getSource(), new CropImageFilter(n2, n, 40, 40)));
            }
            n2 = this.objectAttribute[n3][8];
            n = this.objectAttribute[n3][9];
            if ((n2 != 0 || n != 0) && this.imgCrop[this.objectAttribute[n3][2]] == null) {
                this.imgCrop[this.objectAttribute[n3][2]] = this.createImage(new FilteredImageSource(this.imgMap.getSource(), new CropImageFilter(n2, n, 40, 40)));
            }
            ++n3;
        }
        int n4 = 0;
        while (n4 < 189) {
            this.tracker.addImage(this.imgCrop[n4], 0);
            ++n4;
        }
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/door1.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/door2.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/door3.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/door4.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/door5.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/door6.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/door7.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/door8.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/door9.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/door10.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/key1.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/key2.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/key3.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/right1.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/right2.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/left.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/yusya.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/tkoma.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "image/image.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "data/open2.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "data/open3.gif"), 0);
        this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata01.gif"), 0);
        try {
            this.tracker.waitForID(0);
        }
        catch (InterruptedException interruptedException) {
            System.out.println("Tracker Exception !!!");
        }
        this.showStatus("Now Making character CG ..... Done.");
    }

    public void displayConfigWindow(Graphics graphics, boolean bl, boolean bl2, boolean bl3, boolean bl4) {
        int n;
        int n2;
        Object object;
        String string = "";
        if (!bl && this.monsflag == 0) {
            graphics.drawImage(this.imgBuffStatus2, 0, 0, this);
            graphics.drawImage(this.imgBuffStatus, 520 + this.xp, 0 + this.yp, this);
            return;
        }
        Font font = new Font(this.FontName, 1, this.mapObject[70][127] + 2);
        if (this.mapObject[69][127] == '\u0001') {
            font = new Font(this.FontName, 0, this.mapObject[70][127] + 2);
        } else if (this.mapObject[69][127] == '\u0003') {
            font = new Font(this.FontName, 2, this.mapObject[70][127] + 2);
        }
        this.gBuffStatus.setFont(font);
        this.gBuffStatus2.setFont(font);
        if (bl4) {
            if (this.monsflag == 0) {
                object = this.getImage(this.getDocumentBase(), "image/right1.gif");
                this.gBuffStatus.drawImage((Image)object, 0, 0, this);
                object = this.getImage(this.getDocumentBase(), "image/right2.gif");
                this.gBuffStatus.drawImage((Image)object, 0, 280, this);
            }
            this.gBuffStatus.setColor(Color.black);
        }
        if (bl2 || bl3) {
            int n3;
            font = new Font(this.FontName, 1, this.mapObject[70][127]);
            if (this.mapObject[69][127] == '\u0001') {
                font = new Font(this.FontName, 0, this.mapObject[70][127]);
            } else if (this.mapObject[69][127] == '\u0003') {
                font = new Font(this.FontName, 2, this.mapObject[70][127]);
            }
            this.gBuffStatus.setFont(font);
            this.gBuffStatus.setColor(Color.white);
            if (this.mapObject[69][119] != '\u0000') {
                n2 = this.objectAttribute[this.mapObject[69][119]][1];
                this.gBuffStatus.drawImage(this.imgCrop[n2], 94, 64, this);
                if (this.mapObject[69][119] == '\u001e') {
                    string = this.strMessage[this.mapObject[76][121]][270];
                } else if (this.mapObject[69][119] == '\u001f') {
                    string = this.strMessage[this.mapObject[76][121]][271];
                } else if (this.mapObject[69][119] == ' ') {
                    string = this.strMessage[this.mapObject[76][121]][272];
                } else if (this.mapObject[69][119] == '!') {
                    string = this.strMessage[this.mapObject[76][121]][273];
                } else if (this.mapObject[69][119] == '\"') {
                    string = this.strMessage[this.mapObject[76][121]][274];
                }
                object = this.getFontMetrics(font);
                n3 = ((FontMetrics)object).stringWidth(string);
                this.gBuffStatus.drawString(string, 52 - n3 / 2, 103);
            }
            if (this.mapObject[70][119] != '\u0000') {
                n2 = this.objectAttribute[this.mapObject[70][119]][1];
                this.gBuffStatus.drawImage(this.imgCrop[n2], 94, 127, this);
                if (this.mapObject[70][119] == '#') {
                    string = this.strMessage[this.mapObject[76][121]][275];
                } else if (this.mapObject[70][119] == '$') {
                    string = this.strMessage[this.mapObject[76][121]][276];
                } else if (this.mapObject[70][119] == '%') {
                    string = this.strMessage[this.mapObject[76][121]][277];
                } else if (this.mapObject[70][119] == '&') {
                    string = this.strMessage[this.mapObject[76][121]][278];
                } else if (this.mapObject[70][119] == '\'') {
                    string = this.strMessage[this.mapObject[76][121]][279];
                }
                object = this.getFontMetrics(font);
                n3 = ((FontMetrics)object).stringWidth(string);
                this.gBuffStatus.drawString(string, 52 - n3 / 2, 166);
            }
            int n4 = 0;
            Image image = this.getImage(this.getDocumentBase(), "image/key3.gif");
            if (this.mapObject[76][118] != '\u0000') {
                n = 0;
                while (n < this.mapObject[76][118]) {
                    this.gBuffStatus.drawImage(image, 14 + n4 % 6 * 20, 190 + n4 / 6 * 20, this);
                    if (++n4 >= 20) break;
                    ++n;
                }
            }
            image = this.getImage(this.getDocumentBase(), "image/key2.gif");
            if (this.mapObject[75][118] != '\u0000') {
                n = 0;
                while (n < this.mapObject[75][118]) {
                    this.gBuffStatus.drawImage(image, 14 + n4 % 6 * 20, 190 + n4 / 6 * 20, this);
                    if (++n4 >= 20) break;
                    ++n;
                }
            }
            image = this.getImage(this.getDocumentBase(), "image/key1.gif");
            if (this.mapObject[74][118] != '\u0000') {
                n = 0;
                while (n < this.mapObject[74][118]) {
                    this.gBuffStatus.drawImage(image, 14 + n4 % 6 * 20, 190 + n4 / 6 * 20, this);
                    if (++n4 >= 20) break;
                    ++n;
                }
            }
            image = this.getImage(this.getDocumentBase(), "image/left.gif");
            this.gBuffStatus2.drawImage(image, 0, 0, this);
            font = new Font(this.FontName, 1, this.mapObject[70][127] + 8);
            if (this.mapObject[69][127] == '\u0001') {
                font = new Font(this.FontName, 0, this.mapObject[70][127] + 8);
            } else if (this.mapObject[69][127] == '\u0003') {
                font = new Font(this.FontName, 2, this.mapObject[70][127] + 8);
            }
            this.gBuffStatus2.setFont(font);
            this.gBuffStatus2.setColor(Color.white);
            FontMetrics fontMetrics = this.getFontMetrics(font);
            n3 = fontMetrics.stringWidth("Tower " + String.valueOf(this.mapX + 1 + this.mapY * 10) + "F");
            if (this.mapX + 1 + this.mapY * 10 == 52) {
                n3 = fontMetrics.stringWidth("Tower " + String.valueOf(0) + "F");
            }
            if (this.mapX + 1 + this.mapY * 10 <= 50) {
                this.gBuffStatus2.drawString("Tower " + String.valueOf(this.mapX + 1 + this.mapY * 10) + "F", 135 - n3, 83);
            } else if (this.mapX + 1 + this.mapY * 10 == 52) {
                this.gBuffStatus2.drawString("Tower " + String.valueOf(0) + "F", 135 - n3, 83);
            }
            if (this.mapX + 1 + this.mapY * 10 == 51) {
                if (this.mapObject[74][126] == '\u0000') {
                    this.mapObject[74][126] = 6;
                } else if (this.mapObject[74][126] == '\u0006') {
                    this.mapObject[74][126] = 7;
                } else if (this.mapObject[74][126] == '\u0007') {
                    this.mapObject[74][126] = 8;
                } else if (this.mapObject[74][126] == '\b') {
                    this.mapObject[74][126] = 9;
                }
            }
            font = new Font(this.FontName, 1, this.mapObject[70][127] + 4);
            if (this.mapObject[69][127] == '\u0001') {
                font = new Font(this.FontName, 0, this.mapObject[70][127] + 4);
            } else if (this.mapObject[69][127] == '\u0003') {
                font = new Font(this.FontName, 2, this.mapObject[70][127] + 4);
            }
            fontMetrics = this.getFontMetrics(font);
            this.gBuffStatus2.setFont(font);
            this.gBuffStatus2.setColor(Color.white);
            n3 = fontMetrics.stringWidth(String.valueOf((int)this.mapObject[66][118])) - 16;
            this.gBuffStatus2.drawString(String.valueOf((int)this.mapObject[66][118]), 120 - n3, 122);
            n3 = fontMetrics.stringWidth(String.valueOf((int)this.mapObject[67][118])) - 16;
            this.gBuffStatus2.drawString(String.valueOf((int)this.mapObject[67][118]), 120 - n3, 154);
            n3 = fontMetrics.stringWidth(String.valueOf((int)this.mapObject[68][118])) - 16;
            this.gBuffStatus2.drawString(String.valueOf((int)this.mapObject[68][118]), 120 - n3, 185);
            n3 = fontMetrics.stringWidth(String.valueOf((int)this.mapObject[69][118])) - 16;
            this.gBuffStatus2.drawString(String.valueOf((int)this.mapObject[69][118]), 120 - n3, 216);
        }
        if (bl2 || bl3) {
            n = 0;
            while (n < 5) {
                int n5 = 0;
                while (n5 < 3) {
                    int n6;
                    this.gBuffStatus2.drawImage(this.imgCrop[12], n5 * 40 + 19, 254 + n * 40, this);
                    int n7 = 0;
                    if (n * 3 + n5 >= 6) {
                        n7 = 1;
                    }
                    if (this.mapObject[71 + n * 3 + n5 - n7 * 11][n6 = 119 + n7] != '\u0000') {
                        n2 = 0;
                        if (n * 3 + n5 == 0) {
                            n2 = this.objectAttribute[24][1];
                        } else if (n * 3 + n5 == 1) {
                            n2 = this.objectAttribute[25][1];
                        } else if (n * 3 + n5 == 2) {
                            n2 = this.objectAttribute[26][1];
                        } else if (n * 3 + n5 == 3) {
                            n2 = this.objectAttribute[103][1];
                        } else if (n * 3 + n5 == 4) {
                            n2 = this.objectAttribute[104][1];
                        } else if (n * 3 + n5 == 5) {
                            n2 = this.objectAttribute[114][1];
                        } else if (n * 3 + n5 == 6) {
                            n2 = this.objectAttribute[105][1];
                        } else if (n * 3 + n5 == 7) {
                            n2 = this.objectAttribute[106][1];
                        } else if (n * 3 + n5 == 8) {
                            n2 = this.objectAttribute[107][1];
                        } else if (n * 3 + n5 == 9) {
                            n2 = this.objectAttribute[108][1];
                        } else if (n * 3 + n5 == 10) {
                            n2 = this.objectAttribute[109][1];
                        } else if (n * 3 + n5 == 11) {
                            n2 = this.objectAttribute[110][1];
                        } else if (n * 3 + n5 == 12) {
                            n2 = this.objectAttribute[111][1];
                        } else if (n * 3 + n5 == 13) {
                            n2 = this.objectAttribute[112][1];
                        } else if (n * 3 + n5 == 14) {
                            n2 = this.objectAttribute[113][1];
                        }
                        this.gBuffStatus2.drawImage(this.imgCrop[n2], n5 * 40 + 19, 254 + n * 40, this);
                        if (this.itemFlag != 0) {
                            this.gBuffStatus2.drawImage(this.imgCrop[27], this.itemNUM % 3 * 40 + 19, 254 + this.itemNUM / 3 * 40, this);
                        } else if (this.itemKeyFlag) {
                            this.gBuffStatus2.drawImage(this.imgCrop[27], this.itemNUM % 3 * 40 + 19, 254 + this.itemNUM / 3 * 40, this);
                            if (this.itemFlag == 0) {
                                this.showStatus(this.strMessage[this.mapObject[76][121]][299 + this.itemNUM]);
                                this.messageFlag2 = true;
                            }
                        }
                    }
                    ++n5;
                }
                ++n;
            }
        }
        graphics.drawImage(this.imgBuffStatus, 520 + this.xp, 0 + this.yp, this);
        graphics.drawImage(this.imgBuffStatus2, 0, 0, this);
    }

    public void attackMonster(Graphics graphics, int n, int n2) {
        if (this.attackFlagTurn) {
            this.waitCounter = 150;
            this.waitCounterFlag = true;
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(11 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            this.attackMonsterSub1(graphics, n, n2);
            this.mdata = this.mapObject[n2][n];
            this.attackMonsterSub2(graphics, n, n2, true);
            int n3 = this.charaX / 5 * 40;
            int n4 = this.charaY / 5 * 40;
            if (this.mapObject[67][119] == '\b') {
                this.cropIDchara = 0;
            } else if (this.mapObject[67][119] == '\u0002') {
                this.cropIDchara = 2;
            } else if (this.mapObject[67][119] == '\u0004') {
                this.cropIDchara = 4;
            } else if (this.mapObject[67][119] == '\u0006') {
                this.cropIDchara = 6;
            }
            graphics.drawImage(this.imgCrop[this.cropIDchara], n3 + this.xp, n4, this);
            this.monsStatus(graphics, this.mdata);
            this.twait(200);
            if (this.mapObject[67][118] > this.monsterDefence) {
                if (this.monsterEnergy > this.mapObject[67][118] * this.attackDouble - this.monsterDefence) {
                    this.monsterEnergy -= this.mapObject[67][118] * this.attackDouble - this.monsterDefence;
                } else {
                    this.mdata = this.mapObject[n2][n];
                    if (this.mapObject[72][124] != '\u0000') {
                        this.AudioPlay(11 + (this.mapObject[72][124] - '\u0001') * 25);
                    }
                    this.messageFlag = false;
                    this.strNumber = this.objectAttribute[this.mdata][5];
                    if (this.mdata == 50 || this.mdata == 51 || this.mdata == 52 || this.mdata == 60 || this.mdata == 61 || this.mdata == 62 || this.mdata == 70 || this.mdata == 72) {
                        this.strNumber = 244;
                    }
                    if (this.mapObject[74][120] == '\u0001') {
                        this.monsterGold *= 2;
                    }
                    if (this.mapObject[76][121] == '\u0000') {
                        this.showStatus(this.strMessage[this.mapObject[76][121]][203] + this.strMessage[this.mapObject[76][121]][this.strNumber] + this.strMessage[this.mapObject[76][121]][204] + this.monsterGold + this.strMessage[this.mapObject[76][121]][205]);
                        this.messageFlag2 = true;
                    } else {
                        this.showStatus(this.strMessage[this.mapObject[76][121]][this.strNumber] + this.strMessage[this.mapObject[76][121]][203] + this.strMessage[this.mapObject[76][121]][204] + this.monsterGold + this.strMessage[this.mapObject[76][121]][205]);
                        this.messageFlag2 = true;
                    }
                    this.mapObject[69][118] = (char)(this.mapObject[69][118] + this.monsterGold);
                    this.flagDisplayStatus = true;
                    this.mapObject[n2][n] = (char)this.objectAttribute[this.mdata][14];
                    this.displayCharacter(graphics, n, n2);
                    this.monsterEnergy = 0;
                    this.monsStatus(graphics, this.mdata);
                    this.attackFlag = false;
                }
            }
            this.attackFlagTurn = false;
        } else if (!this.attackFlagTurn) {
            this.waitCounter = 150;
            this.waitCounterFlag = true;
            if (this.mapObject[72][124] != '\u0000') {
                this.audio[4].play();
            }
            this.attackMonsterSub1(graphics, n, n2);
            int n5 = this.charaX / 5 * 40;
            int n6 = this.charaY / 5 * 40;
            if (this.mapObject[67][119] == '\b') {
                this.cropIDchara = 0;
            } else if (this.mapObject[67][119] == '\u0002') {
                this.cropIDchara = 2;
            } else if (this.mapObject[67][119] == '\u0004') {
                this.cropIDchara = 4;
            } else if (this.mapObject[67][119] == '\u0006') {
                this.cropIDchara = 6;
            }
            ++this.cropIDchara;
            graphics.drawImage(this.imgCrop[this.cropIDchara], n5 + this.xp, n6, this);
            graphics.drawImage(this.imgCrop[25], n5 + this.xp, n6, this);
            this.attackMonsterSub2(graphics, n, n2, false);
            this.monsStatus(graphics, this.mdata);
            this.twait(200);
            if (this.monsterStrength > this.mapObject[68][118]) {
                if (this.mapObject[66][118] > this.monsterStrength - this.mapObject[68][118]) {
                    this.mapObject[66][118] = (char)(this.mapObject[66][118] - (this.monsterStrength - this.mapObject[68][118]));
                } else {
                    this.messageFlag = true;
                    this.strNumber = 1;
                    this.strMessage[this.mapObject[76][121]][this.strNumber] = this.strMessage[this.mapObject[76][121]][280];
                    this.mapObject[66][118] = '\u0000';
                    this.mapObject[67][119] = '\u0000';
                    if (this.mapObject[75][124] != '\u0000') {
                        this.AudioStop(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
                    }
                    this.mapObject[69][124] = 20;
                    if (this.mapObject[75][124] != '\u0000') {
                        this.AudioPlay(this.mapObject[69][124] + (this.mapObject[75][124] - '\u0001') * 25);
                    }
                    this.mapFlagAll = true;
                    this.mapFlagErase = false;
                    this.attackFlag = false;
                    this.twait(1000);
                }
            }
            this.attackFlagTurn = true;
        }
        this.displayConfigWindow(graphics, true, true, false, false);
    }

    public void attackMonsterSub1(Graphics graphics, int n, int n2) {
        char c = this.map[n2][n];
        this.cropID = this.mapAttribute[c][1];
        int n3 = n % 13 * 40;
        if (n / 13 != this.mapX) {
            n3 = 520;
        }
        int n4 = n2 % 13 * 40;
        if (n2 / 13 != this.mapY) {
            n4 = 520;
        }
        graphics.drawImage(this.imgCrop[this.cropID], n3 + this.xp, n4, this);
        c = this.map[this.charaY / 5 + this.mapY * 13][this.charaX / 5 + this.mapX * 13];
        this.cropID = this.mapAttribute[c][1];
        n3 = this.charaX / 5 * 40;
        n4 = this.charaY / 5 * 40;
        graphics.drawImage(this.imgCrop[this.cropID], n3 + this.xp, n4, this);
    }

    public void attackMonsterSub2(Graphics graphics, int n, int n2, boolean bl) {
        char c = this.mapObject[n2][n];
        this.cropID = this.objectAttribute[c][1];
        int n3 = n % 13 * 40;
        if (n / 13 != this.mapX) {
            n3 = 520;
        }
        int n4 = n2 % 13 * 40;
        if (n2 / 13 != this.mapY) {
            n4 = 520;
        }
        graphics.drawImage(this.imgCrop[this.cropID], n3 + this.xp, n4, this);
        if (bl) {
            graphics.drawImage(this.imgCrop[25], n3 + this.xp, n4, this);
        }
    }

    public void displayCharacter(Graphics graphics, int n, int n2) {
        if (n < this.mapX * 13 || n >= this.mapX * 13 + 13 || n2 < this.mapY * 13 || n2 >= this.mapY * 13 + 13) {
            return;
        }
        if (this.mapFlagAll) {
            return;
        }
        char c = this.map[n2][n];
        this.cropID = this.mapAttribute[c][1];
        int n3 = n % 13 * 40;
        if (n / 13 != this.mapX) {
            n3 = 520;
        }
        int n4 = n2 % 13 * 40;
        if (n2 / 13 != this.mapY) {
            n4 = 520;
        }
        this.gBuffMap.drawImage(this.imgCrop[this.cropID], 0, 0, this);
        c = this.mapObject[n2][n];
        if (c != '\u0000') {
            this.cropID = this.objectAttribute[c][1];
            this.gBuffMap.drawImage(this.imgCrop[this.cropID], 0, 0, this);
        }
        graphics.drawImage(this.imgBuffMap, n3 + this.xp, n4 + this.yp, this);
    }

    public void displayDoor(Graphics graphics, int n, int n2, int n3) {
        if (this.mapObject[72][124] != '\u0000') {
            this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            this.twait(100);
        }
        if (n3 == 1) {
            Image image = this.getImage(this.getDocumentBase(), "image/door1.gif");
            Image image2 = this.getImage(this.getDocumentBase(), "image/door2.gif");
            int n4 = 1;
            while (n4 <= 20) {
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n]][1]], 0, 0, this);
                if (n == 108 && n2 == 43 && this.mapObject[n2][n] != '\u0002') {
                    this.gBuffMap.drawImage(this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][1]], 0, 0, this);
                }
                this.gBuffMap.drawImage(image, -n4, 0, this);
                this.gBuffMap.drawImage(image2, 20 + n4, 0, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40 + this.yp, this);
                this.twait(30);
                ++n4;
            }
            this.showStatus(this.strMessage[this.mapObject[76][121]][136]);
            this.messageFlag2 = true;
        } else if (n3 == 2) {
            Image image = this.getImage(this.getDocumentBase(), "image/door3.gif");
            Image image3 = this.getImage(this.getDocumentBase(), "image/door4.gif");
            int n5 = 1;
            while (n5 <= 20) {
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n]][1]], 0, 0, this);
                this.gBuffMap.drawImage(image, -n5, 0, this);
                this.gBuffMap.drawImage(image3, 20 + n5, 0, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40 + this.yp, this);
                this.twait(30);
                ++n5;
            }
            this.showStatus(this.strMessage[this.mapObject[76][121]][137]);
            this.messageFlag2 = true;
        } else if (n3 == 3) {
            Image image = this.getImage(this.getDocumentBase(), "image/door5.gif");
            Image image4 = this.getImage(this.getDocumentBase(), "image/door6.gif");
            int n6 = 1;
            while (n6 <= 20) {
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n]][1]], 0, 0, this);
                this.gBuffMap.drawImage(image, -n6, 0, this);
                this.gBuffMap.drawImage(image4, 20 + n6, 0, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40, this);
                this.twait(30);
                ++n6;
            }
            this.showStatus(this.strMessage[this.mapObject[76][121]][138]);
            this.messageFlag2 = true;
        } else if (n3 == 4) {
            Image image = this.getImage(this.getDocumentBase(), "image/door7.gif");
            Image image5 = this.getImage(this.getDocumentBase(), "image/door8.gif");
            Image image6 = this.getImage(this.getDocumentBase(), "image/door9.gif");
            Image image7 = this.getImage(this.getDocumentBase(), "image/door10.gif");
            int n7 = 1;
            while (n7 <= 20) {
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n]][1]], 0, 0, this);
                this.gBuffMap.drawImage(image, n7 - 20, -20 + n7, this);
                this.gBuffMap.drawImage(image5, 40 - n7, -20 + n7, this);
                this.gBuffMap.drawImage(image6, n7 - 20, 40 - n7, this);
                this.gBuffMap.drawImage(image7, 40 - n7, 40 - n7, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40, this);
                this.twait(30);
                ++n7;
            }
        } else if (n3 == 5) {
            Image image = this.getImage(this.getDocumentBase(), "image/door7.gif");
            Image image8 = this.getImage(this.getDocumentBase(), "image/door8.gif");
            Image image9 = this.getImage(this.getDocumentBase(), "image/door9.gif");
            Image image10 = this.getImage(this.getDocumentBase(), "image/door10.gif");
            int n8 = 1;
            while (n8 <= 20) {
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n]][1]], 0, 0, this);
                this.gBuffMap.drawImage(image, -n8, -n8, this);
                this.gBuffMap.drawImage(image8, 20 + n8, -n8, this);
                this.gBuffMap.drawImage(image9, -n8, 20 + n8, this);
                this.gBuffMap.drawImage(image10, 20 + n8, 20 + n8, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40, this);
                this.twait(30);
                ++n8;
            }
        } else if (n3 == 6) {
            Image image = this.imgCrop[this.objectAttribute[19][1]];
            int n9 = 1;
            while (n9 <= 20) {
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n]][1]], 0, 0, this);
                this.gBuffMap.drawImage(image, 0, -n9 * 2, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40, this);
                this.twait(30);
                ++n9;
            }
        } else if (n3 == 7) {
            int n10 = 1;
            while (n10 <= 20) {
                Image image;
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, 0, this);
                if (n == 110 && n2 == 16) {
                    image = this.imgCrop[this.objectAttribute[103][1]];
                    this.gBuffMap.drawImage(image, 0, 0, this);
                } else if (this.mapObject[54][2] == '\u0000' && n == 10 && n2 == 54 && (n10 - 1) / 10 == 0) {
                    this.mapObject[68][125] = '\u0001';
                    image = this.imgCrop[this.objectAttribute[99][1]];
                    this.gBuffMap.drawImage(image, 0, 0, this);
                } else if (this.mapObject[54][2] == '\u0000' && n == 10 && n2 == 54 && (n10 - 1) / 10 == 1) {
                    image = this.imgCrop[this.objectAttribute[99][2]];
                    this.gBuffMap.drawImage(image, 0, 0, this);
                } else if (n == 76 && n2 == 24 && (n10 - 1) / 10 == 0) {
                    image = this.imgCrop[this.objectAttribute[154][1]];
                    this.gBuffMap.drawImage(image, 0, 0, this);
                } else if (n == 76 && n2 == 24 && (n10 - 1) / 10 == 1) {
                    image = this.imgCrop[this.objectAttribute[154][2]];
                    this.gBuffMap.drawImage(image, 0, 0, this);
                } else if (n == 24 && n2 == 14 && (n10 - 1) / 10 == 0) {
                    image = this.imgCrop[this.objectAttribute[17][1]];
                    this.gBuffMap.drawImage(image, 0, 0, this);
                } else if (n == 24 && n2 == 14 && (n10 - 1) / 10 == 1) {
                    image = this.imgCrop[this.objectAttribute[17][2]];
                    this.gBuffMap.drawImage(image, 0, 0, this);
                } else if (this.mapObject[n2][n] != '\u0000' && this.mapObject[n2][n] != 'Y') {
                    image = this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][1]];
                    this.gBuffMap.drawImage(image, 0, 0, this);
                }
                image = this.imgCrop[this.mapAttribute[3][1]];
                this.gBuffMap.drawImage(image, 0, n10 * 2, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40, this);
                this.twait(30);
                ++n10;
            }
            this.showStatus(this.strMessage[this.mapObject[76][121]][141]);
            this.messageFlag2 = true;
        } else if (n3 == 8) {
            Image image = this.mapObject[n2][n] == '\u0000' ? this.imgCrop[this.mapAttribute[this.map[n2][n]][1]] : this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][1]];
            int n11 = 1;
            while (n11 <= 20) {
                this.gBuffMap.drawImage(image, 0, 0, this);
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[3][1]], 0, 40 - n11 * 2, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40, this);
                this.twait(30);
                ++n11;
            }
            this.showStatus(this.strMessage[this.mapObject[76][121]][245]);
            this.messageFlag2 = true;
        } else if (n3 == 9) {
            Image image = this.mapObject[n2][n] == '\u0000' ? this.imgCrop[this.mapAttribute[this.map[n2][n]][1]] : this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][1]];
            int n12 = 1;
            while (n12 <= 20) {
                this.gBuffMap.drawImage(image, 0, 0, this);
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, 40 - n12 * 2, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40, this);
                this.twait(30);
                ++n12;
            }
            this.showStatus(this.strMessage[this.mapObject[76][121]][202]);
            this.messageFlag2 = true;
        } else if (n3 == 10) {
            Image image = this.mapObject[n2][n] == '\u0000' ? this.imgCrop[this.mapAttribute[this.map[n2][n]][1]] : this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][1]];
            int n13 = 1;
            while (n13 <= 20) {
                this.gBuffMap.drawImage(image, 0, 0, this);
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[1][1]], 40 - n13 * 2, 0, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40, this);
                this.twait(30);
                ++n13;
            }
            this.showStatus(this.strMessage[this.mapObject[76][121]][202]);
            this.messageFlag2 = true;
        } else if (n3 == 11) {
            Image image = this.mapObject[n2][n] == '\u0000' ? this.imgCrop[this.mapAttribute[this.map[n2][n]][1]] : this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][1]];
            int n14 = 1;
            while (n14 <= 20) {
                this.gBuffMap.drawImage(image, 0, 0, this);
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[1][1]], n14 * 2 - 40, 0, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40, this);
                this.twait(30);
                ++n14;
            }
            this.showStatus(this.strMessage[this.mapObject[76][121]][202]);
            this.messageFlag2 = true;
        } else if (n3 == 12) {
            Image image = this.mapObject[n2][n] == '\u0000' ? this.imgCrop[this.mapAttribute[this.map[n2][n]][1]] : this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][1]];
            int n15 = 1;
            while (n15 <= 20) {
                this.gBuffMap.drawImage(image, 0, 0, this);
                this.gBuffMap.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, n15 * 2 - 40, this);
                graphics.drawImage(this.imgBuffMap, n % 13 * 40 + this.xp, n2 % 13 * 40, this);
                this.twait(30);
                ++n15;
            }
            this.showStatus(this.strMessage[this.mapObject[76][121]][202]);
            this.messageFlag2 = true;
        }
    }

    public void moveChara(Graphics graphics, int n, int n2, int n3, int n4) {
        int n5 = 5;
        if (n4 == 0) {
            n5 = 15;
        } else if (n4 == 1) {
            n5 = 10;
        }
        char c = this.mapObject[n2][n];
        if (n3 == 1) {
            Image image = this.imgCrop[this.objectAttribute[c][1]];
            Image image2 = this.imgCrop[this.objectAttribute[c][2]];
            int n6 = 1;
            while (n6 <= 20) {
                this.gBuffCharaX.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n]][1]], 0, 0, this);
                this.gBuffCharaX.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n + 1]][1]], 40, 0, this);
                if (n6 % 10 == 1 || n6 % 10 == 2 || n6 % 10 == 3 || n6 % 10 == 4 || n6 % 10 == 5) {
                    this.gBuffCharaX.drawImage(image, n6 * 2, 0, this);
                } else {
                    this.gBuffCharaX.drawImage(image2, n6 * 2, 0, this);
                }
                graphics.drawImage(this.imgBuffCharaX, n % 13 * 40 + this.xp, n2 % 13 * 40 + this.yp, this);
                this.twait(n5);
                ++n6;
            }
            this.mapObject[n2][n] = '\u0000';
            this.displayCharacter(graphics, n, n2);
            this.mapObject[n2][n + 1] = c;
            this.displayCharacter(graphics, n + 1, n2);
        } else if (n3 == 2) {
            Image image = this.imgCrop[this.objectAttribute[c][1]];
            Image image3 = this.imgCrop[this.objectAttribute[c][2]];
            int n7 = 1;
            while (n7 <= 20) {
                this.gBuffCharaX.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n]][1]], 40, 0, this);
                this.gBuffCharaX.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n - 1]][1]], 0, 0, this);
                if (n7 % 10 == 1 || n7 % 10 == 2 || n7 % 10 == 3 || n7 % 10 == 4 || n7 % 10 == 5) {
                    this.gBuffCharaX.drawImage(image, 40 - n7 * 2, 0, this);
                } else {
                    this.gBuffCharaX.drawImage(image3, 40 - n7 * 2, 0, this);
                }
                graphics.drawImage(this.imgBuffCharaX, (n - 1) % 13 * 40 + this.xp, n2 % 13 * 40 + this.yp, this);
                this.twait(n5);
                ++n7;
            }
            this.mapObject[n2][n] = '\u0000';
            this.displayCharacter(graphics, n, n2);
            this.mapObject[n2][n - 1] = c;
            this.displayCharacter(graphics, n - 1, n2);
        } else if (n3 == 3) {
            Image image = this.imgCrop[this.objectAttribute[c][1]];
            Image image4 = this.imgCrop[this.objectAttribute[c][2]];
            int n8 = 1;
            while (n8 <= 20) {
                this.gBuffCharaY.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n]][1]], 0, 0, this);
                this.gBuffCharaY.drawImage(this.imgCrop[this.mapAttribute[this.map[n2 + 1][n]][1]], 0, 40, this);
                if (n8 % 10 == 1 || n8 % 10 == 2 || n8 % 10 == 3 || n8 % 10 == 4 || n8 % 10 == 5) {
                    this.gBuffCharaY.drawImage(image, 0, n8 * 2, this);
                } else {
                    this.gBuffCharaY.drawImage(image4, 0, n8 * 2, this);
                }
                graphics.drawImage(this.imgBuffCharaY, n % 13 * 40 + this.xp, n2 % 13 * 40 + this.yp, this);
                this.twait(n5);
                ++n8;
            }
            this.mapObject[n2][n] = '\u0000';
            this.displayCharacter(graphics, n, n2);
            this.mapObject[n2 + 1][n] = c;
            this.displayCharacter(graphics, n, n2 + 1);
        } else if (n3 == 4) {
            Image image = this.imgCrop[this.objectAttribute[c][1]];
            Image image5 = this.imgCrop[this.objectAttribute[c][2]];
            int n9 = 1;
            while (n9 <= 20) {
                this.gBuffCharaY.drawImage(this.imgCrop[this.mapAttribute[this.map[n2][n]][1]], 0, 40, this);
                this.gBuffCharaY.drawImage(this.imgCrop[this.mapAttribute[this.map[n2 - 1][n]][1]], 0, 0, this);
                if (n9 % 10 == 1 || n9 % 10 == 2 || n9 % 10 == 3 || n9 % 10 == 4 || n9 % 10 == 5) {
                    this.gBuffCharaY.drawImage(image, 0, 40 - n9 * 2, this);
                } else {
                    this.gBuffCharaY.drawImage(image5, 0, 40 - n9 * 2, this);
                }
                graphics.drawImage(this.imgBuffCharaY, n % 13 * 40 + this.xp, (n2 - 1) % 13 * 40 + this.yp, this);
                this.twait(n5);
                ++n9;
            }
            this.mapObject[n2][n] = '\u0000';
            this.displayCharacter(graphics, n, n2);
            this.mapObject[n2 - 1][n] = c;
            this.displayCharacter(graphics, n, n2 - 1);
        }
    }

    public void banpaia(Graphics graphics) {
        if (this.mapObject[72][124] != '\u0000') {
            this.AudioPlay(5 + (this.mapObject[72][124] - '\u0001') * 25);
            this.twait(100);
        }
        Image image = this.getImage(this.getDocumentBase(), "image/image.gif");
        Image image2 = this.imgCrop[this.objectAttribute[47][1]];
        Image image3 = this.imgCrop[this.objectAttribute[47][2]];
        this.gBuff3.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, 0, this);
        PixelGrabber pixelGrabber = new PixelGrabber(this.imgCrop[this.objectAttribute[59][1]], 0, 0, 40, 40, this.pixels1, 0, 40);
        PixelGrabber pixelGrabber2 = new PixelGrabber(this.imgCrop[this.objectAttribute[59][2]], 0, 0, 40, 40, this.pixels2, 0, 40);
        PixelGrabber pixelGrabber3 = new PixelGrabber(image, 0, 0, 40, 40, this.pixels3, 0, 40);
        try {
            pixelGrabber.grabPixels();
            pixelGrabber2.grabPixels();
            pixelGrabber3.grabPixels();
        }
        catch (InterruptedException interruptedException) {
            // empty catch block
        }
        int n = this.pixels3[0];
        int n2 = 1;
        while (n2 <= 19) {
            int n3;
            this.gBuff2.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, 0, this);
            this.gBuff2.drawImage(this.imgCrop[this.mapAttribute[1][1]], 40, 0, this);
            this.gBuff2.drawImage(this.imgCrop[this.mapAttribute[1][1]], 80, 0, this);
            this.gBuff2.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, 40, this);
            this.gBuff2.drawImage(this.imgCrop[this.mapAttribute[1][1]], 40, 40, this);
            this.gBuff2.drawImage(this.imgCrop[this.mapAttribute[1][1]], 80, 40, this);
            this.gBuff2.drawImage(this.imgCrop[this.mapAttribute[1][1]], 0, 80, this);
            this.gBuff2.drawImage(this.imgCrop[this.mapAttribute[1][1]], 40, 80, this);
            this.gBuff2.drawImage(this.imgCrop[this.mapAttribute[1][1]], 80, 80, this);
            if (n2 % 2 == 1) {
                this.gBuff2.drawImage(image2, 0 + n2 * 2, 0 + n2 * 2, this);
                this.gBuff3.drawImage(image2, 0 + n2 * 2 - 40, 0 + n2 * 2 - 40, this);
                this.gBuff2.drawImage(image2, 40, 0 + n2 * 2, this);
                this.gBuff3.drawImage(image2, 0, 0 + n2 * 2 - 40, this);
                this.gBuff2.drawImage(image2, 80 - n2 * 2, 0 + n2 * 2, this);
                this.gBuff3.drawImage(image2, 80 - n2 * 2 - 40, 0 + n2 * 2 - 40, this);
                this.gBuff2.drawImage(image2, 0 + n2 * 2, 40, this);
                this.gBuff3.drawImage(image2, 0 + n2 * 2 - 40, 0, this);
                this.gBuff2.drawImage(image2, 80 - n2 * 2, 40, this);
                this.gBuff3.drawImage(image2, 80 - n2 * 2 - 40, 0, this);
                this.gBuff2.drawImage(image2, 0 + n2 * 2, 80 - n2 * 2, this);
                this.gBuff3.drawImage(image2, 0 + n2 * 2 - 40, 80 - n2 * 2 - 40, this);
                this.gBuff2.drawImage(image2, 40, 80 - n2 * 2, this);
                this.gBuff3.drawImage(image2, 0, 80 - n2 * 2 - 40, this);
                this.gBuff2.drawImage(image2, 80 - n2 * 2, 80 - n2 * 2, this);
                this.gBuff3.drawImage(image2, 80 - n2 * 2 - 40, 80 - n2 * 2 - 40, this);
            } else {
                this.gBuff2.drawImage(image3, 0 + n2 * 2, 0 + n2 * 2, this);
                this.gBuff3.drawImage(image3, 0 + n2 * 2 - 40, 0 + n2 * 2 - 40, this);
                this.gBuff2.drawImage(image3, 40, 0 + n2 * 2, this);
                this.gBuff3.drawImage(image3, 0, 0 + n2 * 2 - 40, this);
                this.gBuff2.drawImage(image3, 80 - n2 * 2, 0 + n2 * 2, this);
                this.gBuff3.drawImage(image3, 80 - n2 * 2 - 40, 0 + n2 * 2 - 40, this);
                this.gBuff2.drawImage(image3, 0 + n2 * 2, 40, this);
                this.gBuff3.drawImage(image3, 0 + n2 * 2 - 40, 0, this);
                this.gBuff2.drawImage(image3, 80 - n2 * 2, 40, this);
                this.gBuff3.drawImage(image3, 80 - n2 * 2 - 40, 0, this);
                this.gBuff2.drawImage(image3, 0 + n2 * 2, 80 - n2 * 2, this);
                this.gBuff3.drawImage(image3, 0 + n2 * 2 - 40, 80 - n2 * 2 - 40, this);
                this.gBuff2.drawImage(image3, 40, 80 - n2 * 2, this);
                this.gBuff3.drawImage(image3, 0, 80 - n2 * 2 - 40, this);
                this.gBuff2.drawImage(image3, 80 - n2 * 2, 80 - n2 * 2, this);
                this.gBuff3.drawImage(image3, 80 - n2 * 2 - 40, 80 - n2 * 2 - 40, this);
            }
            PixelGrabber pixelGrabber4 = new PixelGrabber(this.imgBuff3, 0, 0, 40, 40, this.pixels4, 0, 40);
            try {
                pixelGrabber4.grabPixels();
            }
            catch (InterruptedException interruptedException) {
                // empty catch block
            }
            int n4 = n2;
            if (n2 <= 1) {
                n4 = 0;
            } else if (n2 <= 9) {
                n4 = n2 - 2;
            } else {
                n4 = n2 - 10;
                if (n2 > 17) {
                    n4 = 8;
                }
            }
            int n5 = 0;
            if (n2 > 9) {
                n5 = 1;
            }
            PixelGrabber pixelGrabber5 = new PixelGrabber(image, n4 * 40, n5 * 40, 40, 40, this.pixels5, 0, 40);
            try {
                pixelGrabber5.grabPixels();
            }
            catch (InterruptedException interruptedException) {
                // empty catch block
            }
            if (n2 < 9 || n2 % 2 == 0) {
                n3 = 0;
                while (n3 < 1600) {
                    this.pixels5[n3] = this.pixels5[n3] == n ? this.pixels4[n3] : this.pixels1[n3];
                    ++n3;
                }
            } else {
                n3 = 0;
                while (n3 < 1600) {
                    this.pixels5[n3] = this.pixels5[n3] == n ? this.pixels4[n3] : this.pixels2[n3];
                    ++n3;
                }
            }
            Image image4 = this.createImage(new MemoryImageSource(40, 40, this.pixels5, 0, 40));
            this.gBuff2.drawImage(image4, 40, 40, this);
            graphics.drawImage(this.imgBuff2, 200 + this.xp, 200 + this.yp, this);
            this.twait(400);
            ++n2;
        }
        this.mapObject[18][122] = '\u0000';
        this.displayCharacter(graphics, 122, 18);
        this.mapObject[18][123] = '\u0000';
        this.displayCharacter(graphics, 123, 18);
        this.mapObject[18][124] = '\u0000';
        this.displayCharacter(graphics, 124, 18);
        this.mapObject[19][122] = '\u0000';
        this.displayCharacter(graphics, 122, 19);
        this.mapObject[19][123] = 59;
        this.displayCharacter(graphics, 123, 19);
        this.mapObject[19][124] = '\u0000';
        this.displayCharacter(graphics, 124, 19);
        this.mapObject[20][122] = '\u0000';
        this.displayCharacter(graphics, 122, 20);
        this.mapObject[20][123] = '\u0000';
        this.displayCharacter(graphics, 123, 20);
        this.mapObject[20][124] = '\u0000';
        this.displayCharacter(graphics, 124, 20);
    }

    public void ending(Graphics graphics) {
        int n = 24;
        while (n <= 49) {
            this.mapY = n / 10;
            this.mapX = n % 10;
            this.mapFlagErase = false;
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(12 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            if (n == 49) {
                this.charaX = 30;
                this.charaY = 35;
                this.mapObject[72][118] = (char)this.mapX;
                this.mapObject[73][118] = (char)this.mapY;
                this.mapObject[70][124] = (char)this.charaX;
                this.mapObject[71][124] = (char)this.charaY;
                this.endFlag = false;
            }
            this.paintMapAll(graphics);
            this.twait(400);
            ++n;
        }
        this.map[26][45] = 31;
        this.map[27][44] = '\u0001';
        this.map[27][46] = '\u0001';
        this.map[28][45] = 3;
        this.map[29][45] = 3;
        this.map[30][45] = 3;
        this.mapObject[76][126] = '\u0001';
    }

    public void charaZeno(Graphics graphics, int n, int n2) {
        int n3 = n - this.mapX * 13;
        int n4 = n2 - this.mapY * 13;
        Image image = this.getImage(this.getDocumentBase(), "image/image.gif");
        Image image2 = this.imgCrop[this.mapAttribute[this.map[n2][n]][1]];
        Image image3 = this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][1]];
        this.gBuff3.drawImage(image2, 0, 0, this);
        Image image4 = this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][2]];
        PixelGrabber pixelGrabber = new PixelGrabber(image2, 0, 0, 40, 40, this.pixels1, 0, 40);
        PixelGrabber pixelGrabber2 = new PixelGrabber(image3, 0, 0, 40, 40, this.pixels2, 0, 40);
        PixelGrabber pixelGrabber3 = new PixelGrabber(image4, 0, 0, 40, 40, this.pixels5, 0, 40);
        PixelGrabber pixelGrabber4 = new PixelGrabber(image, 0, 0, 40, 40, this.pixels3, 0, 40);
        try {
            pixelGrabber.grabPixels();
            pixelGrabber2.grabPixels();
            pixelGrabber4.grabPixels();
            pixelGrabber3.grabPixels();
        }
        catch (InterruptedException interruptedException) {
            // empty catch block
        }
        int n5 = this.pixels3[0];
        int n6 = 15;
        while (n6 >= 1) {
            int n7;
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(10 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            int n8 = n6;
            if (n6 > 8) {
                n8 = n6 - 8;
            }
            int n9 = 0;
            if (n6 > 8) {
                n9 = 1;
            }
            PixelGrabber pixelGrabber5 = new PixelGrabber(image, n8 * 40, n9 * 40, 40, 40, this.pixels3, 0, 40);
            try {
                pixelGrabber5.grabPixels();
            }
            catch (InterruptedException interruptedException) {
                // empty catch block
            }
            if (n6 < 9 || n6 % 2 == 0) {
                n7 = 0;
                while (n7 < 1600) {
                    this.pixels4[n7] = this.pixels3[n7] == n5 ? this.pixels1[n7] : this.pixels2[n7];
                    ++n7;
                }
            } else {
                n7 = 0;
                while (n7 < 1600) {
                    this.pixels4[n7] = this.pixels3[n7] == n5 ? this.pixels1[n7] : this.pixels5[n7];
                    ++n7;
                }
            }
            image4 = this.createImage(new MemoryImageSource(40, 40, this.pixels4, 0, 40));
            this.gBuff3.drawImage(image4, 0, 0, this);
            graphics.drawImage(this.imgBuff3, n3 * 40 + this.xp, n4 * 40 + this.yp, this);
            this.twait(400);
            --n6;
        }
        this.mapObject[n2][n] = '\u0000';
        this.displayCharacter(graphics, n, n2);
    }

    public void Zeno(Graphics graphics, int n, int n2) {
        int n3 = n - this.mapX * 13;
        int n4 = n2 - this.mapY * 13;
        Image image = this.getImage(this.getDocumentBase(), "image/image.gif");
        Image image2 = this.imgCrop[this.mapAttribute[1][1]];
        Image image3 = this.imgCrop[this.objectAttribute[57][1]];
        this.gBuff3.drawImage(image2, 0, 0, this);
        Image image4 = this.imgCrop[this.objectAttribute[57][2]];
        PixelGrabber pixelGrabber = new PixelGrabber(image2, 0, 0, 40, 40, this.pixels1, 0, 40);
        PixelGrabber pixelGrabber2 = new PixelGrabber(image3, 0, 0, 40, 40, this.pixels2, 0, 40);
        PixelGrabber pixelGrabber3 = new PixelGrabber(image4, 0, 0, 40, 40, this.pixels5, 0, 40);
        PixelGrabber pixelGrabber4 = new PixelGrabber(image, 0, 0, 40, 40, this.pixels3, 0, 40);
        try {
            pixelGrabber.grabPixels();
            pixelGrabber2.grabPixels();
            pixelGrabber4.grabPixels();
            pixelGrabber3.grabPixels();
        }
        catch (InterruptedException interruptedException) {
            // empty catch block
        }
        int n5 = this.pixels3[0];
        if (this.mapObject[72][124] != '\u0000') {
            this.AudioPlay(6 + (this.mapObject[72][124] - '\u0001') * 25);
        }
        int n6 = 1;
        while (n6 <= 16) {
            int n7;
            int n8 = n6;
            if (n6 > 8) {
                n8 = n6 - 8;
            }
            int n9 = 0;
            if (n6 > 8) {
                n9 = 1;
            }
            PixelGrabber pixelGrabber5 = new PixelGrabber(image, n8 * 40, n9 * 40, 40, 40, this.pixels3, 0, 40);
            try {
                pixelGrabber5.grabPixels();
            }
            catch (InterruptedException interruptedException) {
                // empty catch block
            }
            if (n6 < 9 || n6 % 2 == 0) {
                n7 = 0;
                while (n7 < 1600) {
                    this.pixels4[n7] = this.pixels3[n7] == n5 ? this.pixels1[n7] : this.pixels2[n7];
                    ++n7;
                }
            } else {
                n7 = 0;
                while (n7 < 1600) {
                    this.pixels4[n7] = this.pixels3[n7] == n5 ? this.pixels1[n7] : this.pixels5[n7];
                    ++n7;
                }
            }
            image4 = this.createImage(new MemoryImageSource(40, 40, this.pixels4, 0, 40));
            this.gBuff3.drawImage(image4, 0, 0, this);
            graphics.drawImage(this.imgBuff3, n3 * 40 + this.xp, n4 * 40 + this.yp, this);
            this.twait(400);
            ++n6;
        }
        this.mapObject[n2][n] = 57;
        this.displayCharacter(graphics, n, n2);
    }

    public void Zeno2(Graphics graphics, int n, int n2) {
        int n3 = n - this.mapX * 13;
        int n4 = n2 - this.mapY * 13;
        Image image = this.getImage(this.getDocumentBase(), "image/image.gif");
        Image image2 = this.imgCrop[this.mapAttribute[1][1]];
        Image image3 = this.imgCrop[this.objectAttribute[57][1]];
        this.gBuff3.drawImage(image2, 0, 0, this);
        Image image4 = this.imgCrop[this.objectAttribute[57][2]];
        image2 = this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][1]];
        Image image5 = this.imgCrop[this.objectAttribute[this.mapObject[n2][n]][2]];
        PixelGrabber pixelGrabber = new PixelGrabber(image2, 0, 0, 40, 40, this.pixels1, 0, 40);
        PixelGrabber pixelGrabber2 = new PixelGrabber(image5, 0, 0, 40, 40, this.pixels4, 0, 40);
        PixelGrabber pixelGrabber3 = new PixelGrabber(image3, 0, 0, 40, 40, this.pixels2, 0, 40);
        PixelGrabber pixelGrabber4 = new PixelGrabber(image4, 0, 0, 40, 40, this.pixels5, 0, 40);
        PixelGrabber pixelGrabber5 = new PixelGrabber(image, 0, 0, 40, 40, this.pixels3, 0, 40);
        try {
            pixelGrabber.grabPixels();
            pixelGrabber3.grabPixels();
            pixelGrabber5.grabPixels();
            pixelGrabber2.grabPixels();
            pixelGrabber4.grabPixels();
        }
        catch (InterruptedException interruptedException) {
            // empty catch block
        }
        int n5 = this.pixels3[0];
        if (this.mapObject[72][124] != '\u0000') {
            this.AudioPlay(6 + (this.mapObject[72][124] - '\u0001') * 25);
        }
        int n6 = 1;
        while (n6 <= 16) {
            int n7;
            int n8 = n6;
            if (n6 > 8) {
                n8 = n6 - 8;
            }
            int n9 = 0;
            if (n6 > 8) {
                n9 = 1;
            }
            PixelGrabber pixelGrabber6 = new PixelGrabber(image, n8 * 40, n9 * 40, 40, 40, this.pixels3, 0, 40);
            try {
                pixelGrabber6.grabPixels();
            }
            catch (InterruptedException interruptedException) {
                // empty catch block
            }
            if (n6 % 2 == 0) {
                n7 = 0;
                while (n7 < 1600) {
                    this.pixels6[n7] = this.pixels3[n7] == n5 ? this.pixels1[n7] : this.pixels2[n7];
                    ++n7;
                }
            } else {
                n7 = 0;
                while (n7 < 1600) {
                    this.pixels6[n7] = this.pixels3[n7] == n5 ? this.pixels4[n7] : this.pixels5[n7];
                    ++n7;
                }
            }
            image4 = this.createImage(new MemoryImageSource(40, 40, this.pixels6, 0, 40));
            this.gBuff3.drawImage(image4, 0, 0, this);
            graphics.drawImage(this.imgBuff3, n3 * 40 + this.xp, n4 * 40 + this.yp, this);
            this.twait(400);
            ++n6;
        }
        this.mapObject[n2][n] = 57;
        this.displayCharacter(graphics, n, n2);
    }

    public void Madoushi(Graphics graphics, int n, int n2) {
        int n3 = n - this.mapX * 13;
        int n4 = n2 - this.mapY * 13;
        Image image = this.getImage(this.getDocumentBase(), "image/image.gif");
        Image image2 = this.imgCrop[this.mapAttribute[1][1]];
        Image image3 = this.imgCrop[this.objectAttribute[58][1]];
        this.gBuff3.drawImage(image2, 0, 0, this);
        Image image4 = this.imgCrop[this.objectAttribute[58][2]];
        PixelGrabber pixelGrabber = new PixelGrabber(image2, 0, 0, 40, 40, this.pixels1, 0, 40);
        PixelGrabber pixelGrabber2 = new PixelGrabber(image3, 0, 0, 40, 40, this.pixels2, 0, 40);
        PixelGrabber pixelGrabber3 = new PixelGrabber(image4, 0, 0, 40, 40, this.pixels5, 0, 40);
        PixelGrabber pixelGrabber4 = new PixelGrabber(image, 0, 0, 40, 40, this.pixels3, 0, 40);
        try {
            pixelGrabber.grabPixels();
            pixelGrabber2.grabPixels();
            pixelGrabber4.grabPixels();
            pixelGrabber3.grabPixels();
        }
        catch (InterruptedException interruptedException) {
            // empty catch block
        }
        int n5 = this.pixels3[0];
        if (this.mapObject[72][124] != '\u0000') {
            this.AudioPlay(6 + (this.mapObject[72][124] - '\u0001') * 25);
        }
        int n6 = 1;
        while (n6 <= 16) {
            int n7;
            int n8 = n6;
            if (n6 > 8) {
                n8 = n6 - 8;
            }
            int n9 = 0;
            if (n6 > 8) {
                n9 = 1;
            }
            PixelGrabber pixelGrabber5 = new PixelGrabber(image, n8 * 40, n9 * 40, 40, 40, this.pixels3, 0, 40);
            try {
                pixelGrabber5.grabPixels();
            }
            catch (InterruptedException interruptedException) {
                // empty catch block
            }
            if (n6 < 9 || n6 % 2 == 0) {
                n7 = 0;
                while (n7 < 1600) {
                    this.pixels4[n7] = this.pixels3[n7] == n5 ? this.pixels1[n7] : this.pixels2[n7];
                    ++n7;
                }
            } else {
                n7 = 0;
                while (n7 < 1600) {
                    this.pixels4[n7] = this.pixels3[n7] == n5 ? this.pixels1[n7] : this.pixels5[n7];
                    ++n7;
                }
            }
            image4 = this.createImage(new MemoryImageSource(40, 40, this.pixels4, 0, 40));
            this.gBuff3.drawImage(image4, 0, 0, this);
            graphics.drawImage(this.imgBuff3, n3 * 40 + this.xp, (n4 - 1) * 40 + this.yp, this);
            graphics.drawImage(this.imgBuff3, (n3 - 1) * 40 + this.xp, n4 * 40 + this.yp, this);
            graphics.drawImage(this.imgBuff3, (n3 + 1) * 40 + this.xp, n4 * 40 + this.yp, this);
            graphics.drawImage(this.imgBuff3, n3 * 40 + this.xp, (n4 + 1) * 40 + this.yp, this);
            this.twait(400);
            ++n6;
        }
    }

    public void Madoushi2(Graphics graphics, int n, int n2) {
        int n3 = n - this.mapX * 13;
        int n4 = n2 - this.mapY * 13;
        Image image = this.getImage(this.getDocumentBase(), "image/image.gif");
        Image image2 = this.imgCrop[this.mapAttribute[1][1]];
        Image image3 = this.imgCrop[this.objectAttribute[58][1]];
        Image image4 = this.imgCrop[this.objectAttribute[58][2]];
        PixelGrabber pixelGrabber = new PixelGrabber(image2, 0, 0, 40, 40, this.pixels1, 0, 40);
        PixelGrabber pixelGrabber2 = new PixelGrabber(image3, 0, 0, 40, 40, this.pixels2, 0, 40);
        PixelGrabber pixelGrabber3 = new PixelGrabber(image4, 0, 0, 40, 40, this.pixels5, 0, 40);
        PixelGrabber pixelGrabber4 = new PixelGrabber(image, 0, 0, 40, 40, this.pixels3, 0, 40);
        try {
            pixelGrabber.grabPixels();
            pixelGrabber2.grabPixels();
            pixelGrabber4.grabPixels();
            pixelGrabber3.grabPixels();
        }
        catch (InterruptedException interruptedException) {
            // empty catch block
        }
        int n5 = this.pixels3[0];
        if (this.mapObject[72][124] != '\u0000') {
            this.AudioPlay(6 + (this.mapObject[72][124] - '\u0001') * 25);
        }
        int n6 = 1;
        while (n6 <= 16) {
            int n7;
            int n8 = n6;
            if (n6 > 8) {
                n8 = n6 - 8;
            }
            int n9 = 0;
            if (n6 > 8) {
                n9 = 1;
            }
            PixelGrabber pixelGrabber5 = new PixelGrabber(image, n8 * 40, n9 * 40, 40, 40, this.pixels3, 0, 40);
            try {
                pixelGrabber5.grabPixels();
            }
            catch (InterruptedException interruptedException) {
                // empty catch block
            }
            if (n6 < 9 || n6 % 2 == 0) {
                n7 = 0;
                while (n7 < 1600) {
                    this.pixels4[n7] = this.pixels3[n7] == n5 ? this.pixels1[n7] : this.pixels2[n7];
                    ++n7;
                }
            } else {
                n7 = 0;
                while (n7 < 1600) {
                    this.pixels4[n7] = this.pixels3[n7] == n5 ? this.pixels1[n7] : this.pixels5[n7];
                    ++n7;
                }
            }
            image4 = this.createImage(new MemoryImageSource(40, 40, this.pixels4, 0, 40));
            this.gBuff3.drawImage(image4, 0, 0, this);
            graphics.drawImage(this.imgBuff3, (n3 - 1) * 40 + this.xp, (n4 - 1) * 40 + this.yp, this);
            graphics.drawImage(this.imgBuff3, n3 * 40 + this.xp, (n4 - 1) * 40 + this.yp, this);
            graphics.drawImage(this.imgBuff3, (n3 + 1) * 40 + this.xp, (n4 - 1) * 40 + this.yp, this);
            graphics.drawImage(this.imgBuff3, (n3 + 1) * 40 + this.xp, n4 * 40 + this.yp, this);
            graphics.drawImage(this.imgBuff3, (n3 + 1) * 40 + this.xp, (n4 + 1) * 40 + this.yp, this);
            graphics.drawImage(this.imgBuff3, n3 * 40 + this.xp, (n4 + 1) * 40 + this.yp, this);
            graphics.drawImage(this.imgBuff3, (n3 - 1) * 40 + this.xp, (n4 + 1) * 40 + this.yp, this);
            graphics.drawImage(this.imgBuff3, (n3 - 1) * 40 + this.xp, n4 * 40 + this.yp, this);
            this.twait(400);
            ++n6;
        }
    }

    public void OpenningZeno(Graphics graphics, int n) {
        Image image = this.createImage(640, 400);
        Graphics graphics2 = image.getGraphics();
        int[] nArray = new int[1600];
        int[] nArray2 = new int[1600];
        int[] nArray3 = new int[256000];
        int[] nArray4 = new int[256000];
        Image image2 = this.getImage(this.getDocumentBase(), "image/image.gif");
        Image image3 = n == 2 ? this.getImage(this.getDocumentBase(), "data/open2.gif") : (n == 3 ? this.getImage(this.getDocumentBase(), "data/open3.gif") : (n == 4 ? this.getImage(this.getDocumentBase(), "data2/edata01.gif") : (this.mapObject[76][121] == '\u0000' ? this.getImage(this.getDocumentBase(), "data2/edata16.gif") : this.getImage(this.getDocumentBase(), "data2/edata17.gif"))));
        Image image4 = this.imgCrop[1];
        PixelGrabber pixelGrabber = new PixelGrabber(image4, 0, 0, 40, 40, nArray, 0, 40);
        PixelGrabber pixelGrabber2 = new PixelGrabber(image3, 0, 0, 640, 400, nArray3, 0, 640);
        PixelGrabber pixelGrabber3 = new PixelGrabber(image2, 0, 0, 40, 40, nArray2, 0, 40);
        try {
            pixelGrabber2.grabPixels();
            pixelGrabber3.grabPixels();
        }
        catch (InterruptedException interruptedException) {
            // empty catch block
        }
        int n2 = nArray2[0];
        int n3 = nArray[0];
        int n4 = 1;
        while (n4 <= 16) {
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(12 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            int n5 = n4;
            if (n4 > 8) {
                n5 = n4 - 8;
            }
            int n6 = 0;
            if (n4 > 8) {
                n6 = 1;
            }
            PixelGrabber pixelGrabber4 = new PixelGrabber(image2, n5 * 40, n6 * 40, 40, 40, nArray2, 0, 40);
            try {
                pixelGrabber4.grabPixels();
            }
            catch (InterruptedException interruptedException) {
                // empty catch block
            }
            int n7 = 0;
            while (n7 < 400) {
                int n8 = 0;
                while (n8 < 40) {
                    int n9 = 0;
                    while (n9 < 640) {
                        int n10 = 0;
                        while (n10 < 40) {
                            int n11 = n10 + n9 + n8 * 640 + n7 * 640;
                            nArray4[n11] = nArray2[n10 + n8 * 40] != n2 ? nArray3[n11] : n3;
                            ++n10;
                        }
                        n9 += 40;
                    }
                    ++n8;
                }
                n7 += 40;
            }
            image4 = this.createImage(new MemoryImageSource(640, 400, nArray4, 0, 640));
            graphics.drawImage(image4, 0, 0, 820, 520, this);
            if (n == 4) {
                if (n4 == 1) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata02.gif"), 0);
                } else if (n4 == 2) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata03.gif"), 0);
                } else if (n4 == 3) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata04.gif"), 0);
                } else if (n4 == 4) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata05.gif"), 0);
                } else if (n4 == 5) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata06.gif"), 0);
                } else if (n4 == 6) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata07.gif"), 0);
                } else if (n4 == 7) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata08.gif"), 0);
                } else if (n4 == 8) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata09.gif"), 0);
                } else if (n4 == 9) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata10.gif"), 0);
                } else if (n4 == 10) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata11.gif"), 0);
                } else if (n4 == 11) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata12.gif"), 0);
                } else if (n4 == 12) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata13.gif"), 0);
                } else if (n4 == 13) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata14.gif"), 0);
                } else if (n4 == 14) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata15.gif"), 0);
                } else if (n4 == 15) {
                    this.tracker.addImage(this.getImage(this.getDocumentBase(), "data2/edata18.gif"), 0);
                } else if (n4 == 16) {
                    if (this.mapObject[76][121] == '\u0000') {
                        this.tracker.addImage(this.getImage(this.getDocumentBase(), "data/edata16.gif"), 0);
                    } else {
                        this.tracker.addImage(this.getImage(this.getDocumentBase(), "data/edata17.gif"), 0);
                    }
                }
                try {
                    this.tracker.waitForID(0);
                }
                catch (InterruptedException interruptedException) {
                    System.out.println("Tracker Exception !!!");
                }
            }
            if (n == 4) {
                this.twait(100);
            } else {
                this.twait(200);
            }
            ++n4;
        }
        if (n == 2) {
            image4 = this.getImage(this.getDocumentBase(), "data/open2.gif");
        } else if (n == 3) {
            image4 = this.getImage(this.getDocumentBase(), "data/open3.gif");
        } else if (n == 4) {
            image4 = this.getImage(this.getDocumentBase(), "data2/edata01.gif");
        }
        if (n <= 4) {
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(600);
        }
        if (n == 4) {
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata02.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata03.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata04.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata05.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata06.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata07.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata08.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata09.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata10.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata11.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata12.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata13.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata14.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
            if (this.mapObject[72][124] != '\u0000') {
                this.AudioPlay(9 + (this.mapObject[72][124] - '\u0001') * 25);
            }
            image4 = this.getImage(this.getDocumentBase(), "data2/edata15.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(300);
        } else if (n == 5) {
            this.twait(4000);
            image4 = this.getImage(this.getDocumentBase(), "data2/edata18.gif");
            graphics2.drawImage(image4, 0, 0, this);
            graphics.drawImage(image, 0, 0, 820, 520, this);
            this.twait(6000);
            this.inputKey = false;
            this.mapObject[67][119] = '\u0000';
        }
    }

    public void Openning(Graphics graphics) {
        Image image;
        Image image2;
        Image image3 = this.createImage(640, 400);
        Graphics graphics2 = image3.getGraphics();
        int[] nArray = new int[256000];
        int[] nArray2 = new int[525];
        if (this.mapObject[76][121] == '\u0000') {
            image2 = this.getImage(this.getDocumentBase(), "data/open4.gif");
            image = this.getImage(this.getDocumentBase(), "data/open3.gif");
        } else {
            image2 = this.getImage(this.getDocumentBase(), "data/open1.gif");
            image = this.getImage(this.getDocumentBase(), "data/open2.gif");
        }
        PixelGrabber pixelGrabber = new PixelGrabber(image, 0, 0, 640, 400, nArray, 0, 640);
        try {
            pixelGrabber.grabPixels();
        }
        catch (InterruptedException interruptedException) {
            // empty catch block
        }
        graphics2.drawImage(image2, 0, 0, 640, 400, this);
        graphics.drawImage(image3, 0, 0, 820, 520, this);
        if (this.mapObject[76][121] == '\u0000') {
            int n = 100;
            while (n < 300) {
                int n2 = 135;
                while (n2 < 535) {
                    nArray2[n2 - 135] = nArray[n2 + n * 640];
                    ++n2;
                }
                Image image4 = this.createImage(new MemoryImageSource(400, 1, nArray2, 0, 400));
                graphics2.drawImage(image4, 135, n, 400, 1, this);
                graphics.drawImage(image3, 0, 0, 820, 520, this);
                this.twait(50);
                ++n;
            }
        } else {
            Image image5;
            int n;
            int n3 = 100;
            while (n3 < 155) {
                n = 150;
                while (n < 450) {
                    nArray2[n - 150] = nArray[n + n3 * 640];
                    ++n;
                }
                image5 = this.createImage(new MemoryImageSource(300, 1, nArray2, 0, 300));
                graphics2.drawImage(image5, 150, n3, 300, 1, this);
                graphics.drawImage(image3, 0, 0, 820, 520, this);
                this.twait(50);
                ++n3;
            }
            n3 = 155;
            while (n3 < 200) {
                n = 55;
                while (n < 580) {
                    nArray2[n - 55] = nArray[n + n3 * 640];
                    ++n;
                }
                image5 = this.createImage(new MemoryImageSource(525, 1, nArray2, 0, 525));
                graphics2.drawImage(image5, 55, n3, 525, 1, this);
                graphics.drawImage(image3, 0, 0, 820, 520, this);
                this.twait(50);
                ++n3;
            }
            n3 = 200;
            while (n3 < 300) {
                n = 75;
                while (n < 550) {
                    nArray2[n - 75] = nArray[n + n3 * 640];
                    ++n;
                }
                image5 = this.createImage(new MemoryImageSource(475, 1, nArray2, 0, 475));
                graphics2.drawImage(image5, 75, n3, 475, 1, this);
                graphics.drawImage(image3, 0, 0, 820, 520, this);
                this.twait(50);
                ++n3;
            }
        }
    }

    public void ItemExe(int n) {
        switch (n) {
            case 2: {
                if (this.itemFlag == 3) {
                    if (this.mapObject[75][121] == '\u0001' && this.mapY * 10 + this.mapX + 1 == this.mapObject[71][118]) {
                        this.itemFlag = 0;
                        this.mapObject[75][121] = '\u0000';
                        break;
                    }
                    if (this.mapObject[75][121] == '\u0000' && this.mapY * 10 + this.mapX + 1 == 1) {
                        this.itemFlag = 0;
                        this.mapObject[75][121] = '\u0000';
                        break;
                    }
                    boolean bl = false;
                    int n2 = 0;
                    int n3 = 0;
                    int n4 = 0;
                    int n5 = 0;
                    int n6 = 1;
                    while (n6 < 12) {
                        int n7 = 1;
                        while (n7 < 12) {
                            if (this.mapAttribute[this.map[this.mapY * 13 + n6][this.mapX * 13 + n7]][3] == 2) {
                                n3 = this.mapAttribute[this.map[this.mapY * 13 + n6][this.mapX * 13 + n7]][17] / 13;
                                n2 = this.mapAttribute[this.map[this.mapY * 13 + n6][this.mapX * 13 + n7]][16] / 13;
                                if (n3 * 10 + n2 + 1 - (this.mapY * 10 + this.mapX + 1) > 0 && this.mapObject[75][121] == '\u0001') {
                                    bl = true;
                                    n4 = n7;
                                    n5 = n6;
                                }
                                if (n3 * 10 + n2 + 1 - (this.mapY * 10 + this.mapX + 1) < 0 && this.mapObject[75][121] == '\u0000') {
                                    bl = true;
                                    n4 = n7;
                                    n5 = n6;
                                }
                            }
                            ++n7;
                        }
                        ++n6;
                    }
                    if (bl) {
                        this.charaX = n4 * 5;
                        this.charaY = n5 * 5;
                        this.showStatus(this.strMessage[this.mapObject[76][121]][154]);
                        this.messageFlag2 = true;
                        break;
                    }
                    this.itemFlag = 0;
                    this.mapObject[75][121] = '\u0000';
                    break;
                }
                boolean bl = false;
                boolean bl2 = false;
                int n8 = 0;
                int n9 = 0;
                int n10 = 0;
                int n11 = 0;
                if (this.mapAttribute[this.map[this.charaY / 5 + this.mapY * 13 - 1][this.charaX / 5 + this.mapX * 13]][3] == 2) {
                    bl2 = true;
                    n11 = -1;
                }
                if (this.mapAttribute[this.map[this.charaY / 5 + this.mapY * 13][this.charaX / 5 + this.mapX * 13 - 1]][3] == 2) {
                    bl2 = true;
                    n10 = -1;
                }
                if (this.mapAttribute[this.map[this.charaY / 5 + this.mapY * 13][this.charaX / 5 + this.mapX * 13 + 1]][3] == 2) {
                    bl2 = true;
                    n10 = 1;
                }
                if (this.mapAttribute[this.map[this.charaY / 5 + this.mapY * 13 + 1][this.charaX / 5 + this.mapX * 13]][3] == 2) {
                    bl2 = true;
                    n11 = 1;
                }
                if (!bl2) {
                    this.showStatus(this.strMessage[this.mapObject[76][121]][151]);
                    this.messageFlag2 = true;
                    this.itemKeyFlag = false;
                    this.configFlag = true;
                    break;
                }
                n9 = this.mapAttribute[this.map[this.mapY * 13 + this.charaY / 5 + n11][this.mapX * 13 + this.charaX / 5 + n10]][17] / 13;
                n8 = this.mapAttribute[this.map[this.mapY * 13 + this.charaY / 5 + n11][this.mapX * 13 + this.charaX / 5 + n10]][16] / 13;
                if (n9 * 10 + n8 + 1 - (this.mapY * 10 + this.mapX + 1) > 0) {
                    bl = true;
                }
                if ((!bl || this.mapY * 10 + this.mapX + 1 == this.mapObject[71][118]) && (bl || this.mapY * 10 + this.mapX + 1 == 1)) break;
                this.charaX = (this.charaX / 5 + n10) * 5;
                this.charaY = (this.charaY / 5 + n11) * 5;
                this.mapObject[75][121] = (char)(bl ? 1 : 0);
                this.itemFlag = 3;
                this.showStatus(this.strMessage[this.mapObject[76][121]][154]);
                this.messageFlag2 = true;
                break;
            }
            case 0: {
                this.messageFlag = true;
                this.scoreFlag = true;
                this.itemFlag = 1;
                break;
            }
            case 1: {
                this.messageFlag = true;
                this.scoreFlag = true;
                if (this.itemFlag == 2) {
                    ++this.chieNum;
                    this.inputKey = true;
                    break;
                }
                if (this.itemFlag != 0) break;
                this.itemFlag = 2;
                int n12 = 0;
                this.chieNum = 0;
                int n13 = 0;
                while (n13 < 26) {
                    this.chieOrb[n13] = 0;
                    ++n13;
                }
                if (this.mapObject[66][122] == '\u0001') {
                    this.chieOrb[n12] = 1;
                    ++n12;
                }
                if (this.mapObject[67][122] == '\u0001') {
                    this.chieOrb[n12] = 2;
                    ++n12;
                }
                if (this.mapObject[68][122] == '\u0001') {
                    this.chieOrb[n12] = 3;
                    ++n12;
                }
                if (this.mapObject[69][122] == '\u0001') {
                    this.chieOrb[n12] = 4;
                    ++n12;
                }
                if (this.mapObject[70][122] == '\u0001') {
                    this.chieOrb[n12] = 5;
                    ++n12;
                }
                if (this.mapObject[71][122] == '\u0001') {
                    this.chieOrb[n12] = 6;
                    ++n12;
                }
                if (this.mapObject[72][122] == '\u0001') {
                    this.chieOrb[n12] = 7;
                    ++n12;
                }
                if (this.mapObject[73][122] == '\u0001') {
                    this.chieOrb[n12] = 8;
                    ++n12;
                }
                if (this.mapObject[74][122] == '\u0001') {
                    this.chieOrb[n12] = 9;
                    ++n12;
                }
                if (this.mapObject[75][122] == '\u0001') {
                    this.chieOrb[n12] = 10;
                    ++n12;
                }
                if (this.mapObject[76][122] == '\u0001') {
                    this.chieOrb[n12] = 11;
                    ++n12;
                }
                if (this.mapObject[66][123] == '\u0001') {
                    this.chieOrb[n12] = 12;
                    ++n12;
                }
                if (this.mapObject[67][123] == '\u0001') {
                    this.chieOrb[n12] = 13;
                    ++n12;
                }
                if (this.mapObject[68][123] == '\u0001') {
                    this.chieOrb[n12] = 14;
                    ++n12;
                }
                if (this.mapObject[69][123] == '\u0001') {
                    this.chieOrb[n12] = 15;
                    ++n12;
                }
                if (this.mapObject[70][123] == '\u0001') {
                    this.chieOrb[n12] = 16;
                    ++n12;
                }
                if (this.mapObject[71][123] == '\u0001') {
                    this.chieOrb[n12] = 17;
                    ++n12;
                }
                if (this.mapObject[72][123] == '\u0001') {
                    this.chieOrb[n12] = 18;
                    ++n12;
                }
                if (this.mapObject[73][123] == '\u0001') {
                    this.chieOrb[n12] = 19;
                    ++n12;
                }
                if (this.mapObject[74][123] == '\u0001') {
                    this.chieOrb[n12] = 20;
                    ++n12;
                }
                if (this.mapObject[75][123] == '\u0001') {
                    this.chieOrb[n12] = 21;
                    ++n12;
                }
                if (this.mapObject[76][123] == '\u0001') {
                    this.chieOrb[n12] = 22;
                    ++n12;
                }
                if (this.mapObject[66][124] == '\u0001') {
                    this.chieOrb[n12] = 23;
                    ++n12;
                }
                if (this.mapObject[67][124] != '\u0001') break;
                this.chieOrb[n12] = 24;
                ++n12;
            }
        }
    }

    public void Savedata(int n) {
        int n2;
        int n3;
        int n4;
        boolean bl = false;
        this.FileNo = n;
        this.mapObject[72][118] = (char)this.mapX;
        this.mapObject[73][118] = (char)this.mapY;
        this.mapObject[70][124] = (char)this.charaX;
        this.mapObject[71][124] = (char)this.charaY;
        this.mapObject[67][127] = (char)this.FileNo;
        int n5 = 0;
        while (n5 < 5) {
            n4 = 0;
            while (n4 < 10) {
                this.mapObject[66 + n4][92 + n5] = '\u0000';
                this.map[66 + n4][92 + n5] = '\u0000';
                n3 = 1;
                while (n3 < 12) {
                    n2 = 1;
                    while (n2 < 12) {
                        this.mapObject[66 + n4][92 + n5] = (char)(this.mapObject[66 + n4][92 + n5] + this.mapObject[n3 + n5 * 13][n2 + n4 * 13]);
                        this.map[66 + n4][92 + n5] = (char)(this.map[66 + n4][92 + n5] + this.map[n3 + n5 * 13][n2 + n4 * 13]);
                        ++n2;
                    }
                    ++n3;
                }
                ++n4;
            }
            ++n5;
        }
        n5 = 5;
        n4 = 0;
        while (n4 < 7) {
            this.mapObject[66 + n4][92 + n5] = '\u0000';
            this.map[66 + n4][92 + n5] = '\u0000';
            n3 = 1;
            while (n3 < 12) {
                n2 = 1;
                while (n2 < 12) {
                    this.mapObject[66 + n4][92 + n5] = (char)(this.mapObject[66 + n4][92 + n5] + this.mapObject[n3 + n5 * 13][n2 + n4 * 13]);
                    this.map[66 + n4][92 + n5] = (char)(this.map[66 + n4][92 + n5] + this.map[n3 + n5 * 13][n2 + n4 * 13]);
                    ++n2;
                }
                ++n3;
            }
            ++n4;
        }
        n5 = 5;
        n4 = 8;
        while (n4 < 10) {
            this.mapObject[66 + n4][92 + n5] = '\u0000';
            this.map[66 + n4][92 + n5] = '\u0000';
            n3 = 1;
            while (n3 < 12) {
                n2 = 1;
                while (n2 < 12) {
                    this.mapObject[66 + n4][92 + n5] = (char)(this.mapObject[66 + n4][92 + n5] + this.mapObject[n3 + n5 * 13][n2 + n4 * 13]);
                    this.map[66 + n4][92 + n5] = (char)(this.map[66 + n4][92 + n5] + this.map[n3 + n5 * 13][n2 + n4 * 13]);
                    ++n2;
                }
                ++n3;
            }
            ++n4;
        }
        n3 = 0;
        while (n3 < 6) {
            this.mapObject[76][92 + n3] = '\u0000';
            this.map[76][92 + n3] = '\u0000';
            n2 = 0;
            while (n2 < 10) {
                this.mapObject[76][92 + n3] = (char)(this.mapObject[76][92 + n3] + this.mapObject[66 + n2][92 + n3]);
                this.map[76][92 + n3] = (char)(this.map[76][92 + n3] + this.map[66 + n2][92 + n3]);
                ++n2;
            }
            ++n3;
        }
        n3 = 0;
        while (n3 < 10) {
            this.mapObject[66 + n3][98] = '\u0000';
            this.map[66 + n3][98] = '\u0000';
            n2 = 0;
            while (n2 < 6) {
                this.mapObject[66 + n3][98] = (char)(this.mapObject[66 + n3][98] + this.mapObject[66][92 + n2]);
                this.map[66 + n3][98] = (char)(this.map[66 + n3][98] + this.map[66][92 + n2]);
                ++n2;
            }
            ++n3;
        }
        this.FileName = "savedat/data";
        if (this.FileNo == 1) {
            this.FileName = this.FileName + "1.dat";
        } else if (this.FileNo == 2) {
            this.FileName = this.FileName + "2.dat";
        } else if (this.FileNo == 3) {
            this.FileName = this.FileName + "3.dat";
        } else if (this.FileNo == 4) {
            this.FileName = this.FileName + "4.dat";
        } else if (this.FileNo == 5) {
            this.FileName = this.FileName + "5.dat";
        } else if (this.FileNo == 6) {
            this.FileName = this.FileName + "6.dat";
        } else if (this.FileNo == 7) {
            this.FileName = this.FileName + "7.dat";
        } else if (this.FileNo == 8) {
            this.FileName = this.FileName + "8.dat";
        }
        boolean bl2 = false;
        try {
            InputStream inputStream = new URL(this.getDocumentBase(), this.FileName).openStream();
            bl2 = true;
        }
        catch (FileNotFoundException fileNotFoundException) {
        }
        catch (IOException iOException) {
            // empty catch block
        }
        if (bl2) {
            if (this.VerX + 300 > 820) {
                this.VerX = 520;
            }
            if (this.VerY + 150 > 520) {
                this.VerY = 370;
            }
            ((Component)this.d2).setLocation(this.VerX, this.VerY);
            this.d2.init(this.strMessage[this.mapObject[76][121]][281]);
        }
        if (!bl2 || this.d2.Ans) {
            this.saveFlag = true;
        }
    }

    public void dosave() {
        boolean bl = false;
        try {
            FileOutputStream fileOutputStream = this.FileNo == 1 ? new FileOutputStream("./savedat/data1.dat/") : (this.FileNo == 2 ? new FileOutputStream("./savedat/data2.dat/") : (this.FileNo == 3 ? new FileOutputStream("./savedat/data3.dat/") : (this.FileNo == 4 ? new FileOutputStream("./savedat/data4.dat/") : (this.FileNo == 5 ? new FileOutputStream("./savedat/data5.dat/") : (this.FileNo == 6 ? new FileOutputStream("./savedat/data6.dat/") : (this.FileNo == 7 ? new FileOutputStream("./savedat/data7.dat/") : new FileOutputStream("./savedat/data8.dat/")))))));
            DataOutputStream dataOutputStream = new DataOutputStream(fileOutputStream);
            this.showStatus(this.strMessage[this.mapObject[76][121]][284]);
            this.messageFlag2 = true;
            int n = 0;
            while (n < 78) {
                int n2 = 0;
                while (n2 < 130) {
                    dataOutputStream.writeChar(this.mapObject[n][n2]);
                    dataOutputStream.writeChar(this.map[n][n2]);
                    ++n2;
                }
                ++n;
            }
            bl = true;
            dataOutputStream.close();
        }
        catch (Exception exception) {
            System.out.println("Error:" + exception);
        }
        if (bl) {
            this.showStatus(this.strMessage[this.mapObject[76][121]][251]);
            this.messageFlag2 = true;
            if (this.mapObject[67][127] == '\u0001' && !this.subload1.isEnabled()) {
                this.subload1.setEnabled(true);
            } else if (this.mapObject[67][127] == '\u0002' && !this.subload2.isEnabled()) {
                this.subload2.setEnabled(true);
            } else if (this.mapObject[67][127] == '\u0003' && !this.subload3.isEnabled()) {
                this.subload3.setEnabled(true);
            } else if (this.mapObject[67][127] == '\u0004' && !this.subload4.isEnabled()) {
                this.subload4.setEnabled(true);
            } else if (this.mapObject[67][127] == '\u0005' && !this.subload5.isEnabled()) {
                this.subload5.setEnabled(true);
            } else if (this.mapObject[67][127] == '\u0006' && !this.subload6.isEnabled()) {
                this.subload6.setEnabled(true);
            } else if (this.mapObject[67][127] == '\u0007' && !this.subload7.isEnabled()) {
                this.subload7.setEnabled(true);
            } else if (this.mapObject[67][127] == '\b' && !this.subload8.isEnabled()) {
                this.subload8.setEnabled(true);
            }
        } else {
            this.showStatus(this.strMessage[this.mapObject[76][121]][285]);
            this.messageFlag2 = true;
        }
    }

    public void Loaddata(int n) {
        int n2;
        int n3;
        char[][] cArray = new char[78][130];
        char[][] cArray2 = new char[78][130];
        this.showStatus(this.strMessage[this.mapObject[76][121]][284]);
        this.messageFlag2 = true;
        this.FileName = "savedat/data";
        boolean bl = false;
        if (n == 1) {
            this.FileName = this.FileName + "1.dat";
        } else if (n == 2) {
            this.FileName = this.FileName + "2.dat";
        } else if (n == 3) {
            this.FileName = this.FileName + "3.dat";
        } else if (n == 4) {
            this.FileName = this.FileName + "4.dat";
        } else if (n == 5) {
            this.FileName = this.FileName + "5.dat";
        } else if (n == 6) {
            this.FileName = this.FileName + "6.dat";
        } else if (n == 7) {
            this.FileName = this.FileName + "7.dat";
        } else if (n == 8) {
            this.FileName = this.FileName + "8.dat";
        }
        try {
            InputStream inputStream = new URL(this.getDocumentBase(), this.FileName).openStream();
            DataInputStream dataInputStream = new DataInputStream(inputStream);
            n3 = 0;
            while (n3 < 78) {
                n2 = 0;
                while (n2 < 130) {
                    cArray2[n3][n2] = dataInputStream.readChar();
                    cArray[n3][n2] = dataInputStream.readChar();
                    ++n2;
                }
                ++n3;
            }
            bl = true;
            dataInputStream.close();
        }
        catch (MalformedURLException malformedURLException) {
            System.out.println("Error:MalformedURLException" + malformedURLException);
        }
        catch (FileNotFoundException fileNotFoundException) {
            System.out.println("Error:FileNotFoundException" + fileNotFoundException);
        }
        catch (IOException iOException) {
            System.out.println("Error:IOException" + iOException);
        }
        if (bl) {
            int n4;
            boolean bl2 = false;
            int n5 = 0;
            while (n5 < 5) {
                n4 = 0;
                while (n4 < 10) {
                    char c = '\u0000';
                    char c2 = '\u0000';
                    n3 = 1;
                    while (n3 < 12) {
                        n2 = 1;
                        while (n2 < 12) {
                            c = (char)(c + cArray2[n3 + n5 * 13][n2 + n4 * 13]);
                            c2 = (char)(c2 + cArray[n3 + n5 * 13][n2 + n4 * 13]);
                            ++n2;
                        }
                        ++n3;
                    }
                    if (cArray2[66 + n4][92 + n5] != c) {
                        bl2 = true;
                    }
                    if (cArray[66 + n4][92 + n5] != c2) {
                        bl2 = true;
                    }
                    ++n4;
                }
                ++n5;
            }
            n5 = 5;
            n4 = 0;
            while (n4 < 7) {
                char c = '\u0000';
                char c3 = '\u0000';
                n3 = 1;
                while (n3 < 12) {
                    n2 = 1;
                    while (n2 < 12) {
                        c = (char)(c + cArray2[n3 + n5 * 13][n2 + n4 * 13]);
                        c3 = (char)(c3 + cArray[n3 + n5 * 13][n2 + n4 * 13]);
                        ++n2;
                    }
                    ++n3;
                }
                if (cArray2[66 + n4][92 + n5] != c) {
                    bl2 = true;
                }
                if (cArray[66 + n4][92 + n5] != c3) {
                    bl2 = true;
                }
                ++n4;
            }
            n5 = 5;
            n4 = 8;
            while (n4 < 10) {
                char c = '\u0000';
                char c4 = '\u0000';
                n3 = 1;
                while (n3 < 12) {
                    n2 = 1;
                    while (n2 < 12) {
                        c = (char)(c + cArray2[n3 + n5 * 13][n2 + n4 * 13]);
                        c4 = (char)(c4 + cArray[n3 + n5 * 13][n2 + n4 * 13]);
                        ++n2;
                    }
                    ++n3;
                }
                if (cArray2[66 + n4][92 + n5] != c) {
                    bl2 = true;
                }
                if (cArray[66 + n4][92 + n5] != c4) {
                    bl2 = true;
                }
                ++n4;
            }
            n3 = 0;
            while (n3 < 6) {
                char c = '\u0000';
                char c5 = '\u0000';
                n2 = 0;
                while (n2 < 10) {
                    c = (char)(c + cArray2[66 + n2][92 + n3]);
                    c5 = (char)(c5 + cArray[66 + n2][92 + n3]);
                    ++n2;
                }
                if (cArray2[76][92 + n3] != c) {
                    bl2 = true;
                }
                if (cArray[76][92 + n3] != c5) {
                    bl2 = true;
                }
                ++n3;
            }
            n3 = 0;
            while (n3 < 10) {
                char c = '\u0000';
                char c6 = '\u0000';
                n2 = 0;
                while (n2 < 6) {
                    c = (char)(c + cArray2[66][92 + n2]);
                    c6 = (char)(c6 + cArray[66][92 + n2]);
                    ++n2;
                }
                if (cArray2[66 + n3][98] != c) {
                    bl2 = true;
                }
                if (cArray[66 + n3][98] != c6) {
                    bl2 = true;
                }
                ++n3;
            }
            if (bl2) {
                cArray2[74][124] = '\u0001';
            }
            if (cArray2[67][119] == '\u0000') {
                cArray2[67][119] = 2;
            }
            if (cArray2[72][124] == '\u0001') {
                this.subsound1.setEnabled(false);
                this.subsound3.setEnabled(true);
                this.subsound2.setEnabled(true);
            } else if (cArray2[72][124] == '\u0002') {
                this.subsound1.setEnabled(true);
                this.subsound3.setEnabled(false);
                this.subsound2.setEnabled(true);
            } else {
                this.subsound1.setEnabled(true);
                this.subsound3.setEnabled(true);
                this.subsound2.setEnabled(false);
            }
            if (cArray2[75][124] == '\u0001') {
                this.subBGM1.setEnabled(false);
                this.subBGM3.setEnabled(true);
                this.subBGM2.setEnabled(true);
            } else if (cArray2[75][124] == '\u0002') {
                this.subBGM1.setEnabled(true);
                this.subBGM3.setEnabled(false);
                this.subBGM2.setEnabled(true);
            } else {
                this.subBGM1.setEnabled(true);
                this.subBGM3.setEnabled(true);
                this.subBGM2.setEnabled(false);
            }
            if (cArray2[76][121] == '\u0000') {
                this.LangENG.setEnabled(false);
                this.LangJPN.setEnabled(true);
            } else if (cArray2[76][121] == '\u0001') {
                this.LangENG.setEnabled(true);
                this.LangJPN.setEnabled(false);
            }
            if (cArray2[68][127] == '\u0001') {
                this.subfont11.setEnabled(false);
                this.subfont12.setEnabled(true);
                this.subfont13.setEnabled(true);
                this.subfont14.setEnabled(true);
            } else if (cArray2[68][127] == '\u0002') {
                this.subfont11.setEnabled(true);
                this.subfont12.setEnabled(false);
                this.subfont13.setEnabled(true);
                this.subfont14.setEnabled(true);
            } else if (cArray2[68][127] == '\u0003') {
                this.subfont11.setEnabled(true);
                this.subfont12.setEnabled(true);
                this.subfont13.setEnabled(false);
                this.subfont14.setEnabled(true);
            } else if (cArray2[68][127] == '\u0004') {
                this.subfont11.setEnabled(true);
                this.subfont12.setEnabled(true);
                this.subfont13.setEnabled(true);
                this.subfont14.setEnabled(false);
            }
            if (cArray2[68][128] == '\u0001') {
                this.subfont21.setEnabled(false);
                this.subfont22.setEnabled(true);
                this.subfont23.setEnabled(true);
            } else if (cArray2[68][128] == '\u0002') {
                this.subfont21.setEnabled(true);
                this.subfont22.setEnabled(false);
                this.subfont23.setEnabled(true);
            } else if (cArray2[68][128] == '\u0003') {
                this.subfont21.setEnabled(true);
                this.subfont22.setEnabled(true);
                this.subfont23.setEnabled(false);
            }
            if (cArray2[67][126] == '\u0001') {
                this.objectAttribute[44][2] = 0;
            }
            this.showStatus(this.strMessage[this.mapObject[76][121]][250]);
            this.messageFlag2 = true;
            this.menulang();
            this.configFlag = true;
            if (cArray2[74][124] != '\u0000' || cArray2[75][127] != '\u0001') {
                this.showStatus(this.strMessage[this.mapObject[76][121]][288]);
                this.messageFlag2 = true;
            } else {
                n3 = 0;
                while (n3 < 78) {
                    n2 = 0;
                    while (n2 < 130) {
                        this.map[n3][n2] = cArray[n3][n2];
                        this.mapObject[n3][n2] = cArray2[n3][n2];
                        ++n2;
                    }
                    ++n3;
                }
                this.mapFlagAll = true;
                this.mapFlagErase = true;
                this.mapX = this.mapObject[72][118];
                this.mapY = this.mapObject[73][118];
                this.charaX = this.mapObject[70][124];
                this.charaY = this.mapObject[71][124];
            }
        }
    }

    public void scoreInit(int n) {
        String[][] stringArray = new String[10][5];
        if (n == 1) {
            if (this.mapObject[76][121] == '\u0000') {
                stringArray[0][1] = "Skeleton A";
                stringArray[1][1] = "Priest";
                stringArray[2][1] = "Skeleton B";
                stringArray[3][1] = "Gate-Keeper C";
                stringArray[4][1] = "Skeleton C";
                stringArray[5][1] = "Bat";
                stringArray[6][1] = "Red Slime";
                stringArray[7][1] = "Green Slime";
                stringArray[8][1] = "Iron Sword";
                stringArray[9][1] = "Iron Shield";
            } else {
                stringArray[0][1] = "\u30b9\u30b1\u30eb\u30c8\u30f3\uff21\u3000";
                stringArray[1][1] = "\u50e7\u4fb6\u3000\u3000\u3000\u3000\u3000";
                stringArray[2][1] = "\u30b9\u30b1\u30eb\u30c8\u30f3\uff22\u3000";
                stringArray[3][1] = "\u8001\u4eba\u3000\u3000\u3000\u3000\u3000";
                stringArray[4][1] = "\u30b9\u30b1\u30eb\u30c8\u30f3\uff23\u3000";
                stringArray[5][1] = "\u9580\u756a\uff23\u3000\u3000\u3000\u3000";
                stringArray[6][1] = "\u30d0\u30c3\u30c8\u3000\u3000\u3000\u3000";
                stringArray[7][1] = "\uff32\u30b9\u30e9\u30a4\u30e0\u3000\u3000";
                stringArray[8][1] = "\uff27\u30b9\u30e9\u30a4\u30e0\u3000\u3000";
                stringArray[9][1] = "\u76d7\u8cca\u3000\u3000\u3000\u3000\u3000";
            }
            stringArray[0][0] = "100";
            stringArray[1][0] = "90";
            stringArray[2][0] = "80";
            stringArray[3][0] = "70";
            stringArray[4][0] = "60";
            stringArray[5][0] = "50";
            stringArray[6][0] = "40";
            stringArray[7][0] = "30";
            stringArray[8][0] = "20";
            stringArray[9][0] = "10";
            stringArray[0][2] = "500";
            stringArray[1][2] = "450";
            stringArray[2][2] = "400";
            stringArray[3][2] = "350";
            stringArray[4][2] = "300";
            stringArray[5][2] = "250";
            stringArray[6][2] = "200";
            stringArray[7][2] = "150";
            stringArray[8][2] = "100";
            stringArray[9][2] = "50";
            stringArray[0][3] = "25";
            stringArray[1][3] = "24";
            stringArray[2][3] = "23";
            stringArray[3][3] = "22";
            stringArray[4][3] = "21";
            stringArray[5][3] = "20";
            stringArray[6][3] = "19";
            stringArray[7][3] = "18";
            stringArray[8][3] = "17";
            stringArray[9][3] = "16";
            stringArray[0][4] = "25";
            stringArray[1][4] = "24";
            stringArray[2][4] = "23";
            stringArray[3][4] = "22";
            stringArray[4][4] = "21";
            stringArray[5][4] = "20";
            stringArray[6][4] = "19";
            stringArray[7][4] = "18";
            stringArray[8][4] = "17";
            stringArray[9][4] = "16";
        } else if (n == 2) {
            if (this.mapObject[76][121] == '\u0000') {
                stringArray[0][1] = "Vampire";
                stringArray[1][1] = "Superion Priest";
                stringArray[2][1] = "Zombie Knight";
                stringArray[3][1] = "Gate-Keeper B";
                stringArray[4][1] = "Rock";
                stringArray[5][1] = "Big Octopus";
                stringArray[6][1] = "Zombie";
                stringArray[7][1] = "Big Bat";
                stringArray[8][1] = "Big Slime";
                stringArray[9][1] = "Blue Crystal";
            } else {
                stringArray[0][1] = "\u30d0\u30f3\u30d1\u30a4\u30a2\u3000\u3000";
                stringArray[1][1] = "\u4e0a\u7d1a\u50e7\u4fb6\u3000\u3000\u3000";
                stringArray[2][1] = "\u30be\u30f3\u30d3\u30ca\u30a4\u30c8\u3000";
                stringArray[3][1] = "\u9580\u756a\uff22\u3000\u3000\u3000\u3000";
                stringArray[4][1] = "\u30ed\u30c3\u30af\u3000\u3000\u3000\u3000";
                stringArray[5][1] = "\u5927\u30c0\u30b3\u3000\u3000\u3000\u3000";
                stringArray[6][1] = "\u30be\u30f3\u30d3\u3000\u3000\u3000\u3000";
                stringArray[7][1] = "\u5927\u30d0\u30c3\u30c8\u3000\u3000\u3000";
                stringArray[8][1] = "\uff22\u30b9\u30e9\u30a4\u30e0\u3000\u3000";
                stringArray[9][1] = "\u9752\u306e\u30af\u30ea\u30b9\u30bf\u30eb";
            }
            stringArray[0][0] = "100";
            stringArray[1][0] = "90";
            stringArray[2][0] = "80";
            stringArray[3][0] = "70";
            stringArray[4][0] = "60";
            stringArray[5][0] = "50";
            stringArray[6][0] = "40";
            stringArray[7][0] = "30";
            stringArray[8][0] = "20";
            stringArray[9][0] = "10";
            stringArray[0][2] = "1000";
            stringArray[1][2] = "900";
            stringArray[2][2] = "800";
            stringArray[3][2] = "700";
            stringArray[4][2] = "600";
            stringArray[5][2] = "500";
            stringArray[6][2] = "400";
            stringArray[7][2] = "300";
            stringArray[8][2] = "200";
            stringArray[9][2] = "100";
            stringArray[0][3] = "50";
            stringArray[1][3] = "45";
            stringArray[2][3] = "40";
            stringArray[3][3] = "35";
            stringArray[4][3] = "30";
            stringArray[5][3] = "25";
            stringArray[6][3] = "20";
            stringArray[7][3] = "15";
            stringArray[8][3] = "10";
            stringArray[9][3] = "5";
            stringArray[0][4] = "50";
            stringArray[1][4] = "45";
            stringArray[2][4] = "40";
            stringArray[3][4] = "35";
            stringArray[4][4] = "30";
            stringArray[5][4] = "25";
            stringArray[6][4] = "20";
            stringArray[7][4] = "15";
            stringArray[8][4] = "10";
            stringArray[9][4] = "5";
        } else if (n == 3) {
            if (this.mapObject[76][121] == '\u0000') {
                stringArray[0][1] = "Magic Master";
                stringArray[1][1] = "Thief";
                stringArray[2][1] = "Fairy";
                stringArray[3][1] = "Merchant";
                stringArray[4][1] = "Princess";
                stringArray[5][1] = "Old Man";
                stringArray[6][1] = "Brave Man";
                stringArray[7][1] = "Mattock";
                stringArray[8][1] = "Cross";
                stringArray[9][1] = "Lucky Gold";
            } else {
                stringArray[0][1] = "\u5927\u9b54\u5c0e\u5e2b\u3000\u3000\u3000";
                stringArray[1][1] = "\u76d7\u8cca\u3000\u3000\u3000\u3000\u3000";
                stringArray[2][1] = "\u5996\u7cbe\u3000\u3000\u3000\u3000\u3000";
                stringArray[3][1] = "\u5546\u4eba\u3000\u3000\u3000\u3000\u3000";
                stringArray[4][1] = "\u304a\u59eb\u69d8\u3000\u3000\u3000\u3000";
                stringArray[5][1] = "\u30de\u30c8\u30c3\u30af\u3000\u3000\u3000";
                stringArray[6][1] = "\u52c7\u8005\u3000\u3000\u3000\u3000\u3000";
                stringArray[7][1] = "\u5341\u5b57\u67b6\u3000\u3000\u3000\u3000";
                stringArray[8][1] = "\u5e78\u904b\u306e\u91d1\u8ca8\u3000\u3000";
                stringArray[9][1] = "\u9b54\u6cd5\u306e\u9375\u3000\u3000\u3000";
            }
            stringArray[0][0] = "100";
            stringArray[1][0] = "90";
            stringArray[2][0] = "80";
            stringArray[3][0] = "70";
            stringArray[4][0] = "60";
            stringArray[5][0] = "50";
            stringArray[6][0] = "40";
            stringArray[7][0] = "30";
            stringArray[8][0] = "20";
            stringArray[9][0] = "10";
            stringArray[0][2] = "10000";
            stringArray[1][2] = "9000";
            stringArray[2][2] = "8000";
            stringArray[3][2] = "7000";
            stringArray[4][2] = "6000";
            stringArray[5][2] = "5000";
            stringArray[6][2] = "4000";
            stringArray[7][2] = "3000";
            stringArray[8][2] = "2000";
            stringArray[9][2] = "1000";
            stringArray[0][3] = "500";
            stringArray[1][3] = "450";
            stringArray[2][3] = "400";
            stringArray[3][3] = "350";
            stringArray[4][3] = "300";
            stringArray[5][3] = "250";
            stringArray[6][3] = "200";
            stringArray[7][3] = "150";
            stringArray[8][3] = "100";
            stringArray[9][3] = "50";
            stringArray[0][4] = "500";
            stringArray[1][4] = "450";
            stringArray[2][4] = "400";
            stringArray[3][4] = "350";
            stringArray[4][4] = "300";
            stringArray[5][4] = "250";
            stringArray[6][4] = "200";
            stringArray[7][4] = "150";
            stringArray[8][4] = "100";
            stringArray[9][4] = "50";
        } else if (n == 4) {
            if (this.mapObject[76][121] == '\u0000') {
                stringArray[0][1] = "Golden Knight";
                stringArray[1][1] = "Knight";
                stringArray[2][1] = "Fancer";
                stringArray[3][1] = "Soldier";
                stringArray[4][1] = "Ghost Soldier";
                stringArray[5][1] = "Dragon";
                stringArray[6][1] = "Swordsman";
                stringArray[7][1] = "Slime Man";
                stringArray[8][1] = "Sword of Knight";
                stringArray[9][1] = "Shield of Knight";
            } else {
                stringArray[0][1] = "\u91d1\u9a0e\u58eb\u3000\u3000\u3000\u3000";
                stringArray[1][1] = "\u9a0e\u58eb\u3000\u3000\u3000\u3000\u3000";
                stringArray[2][1] = "\u5263\u58eb\u3000\u3000\u3000\u3000\u3000";
                stringArray[3][1] = "\u5175\u58eb\u3000\u3000\u3000\u3000\u3000";
                stringArray[4][1] = "\u6b7b\u970a\u5175\u58eb\u3000\u3000\u3000";
                stringArray[5][1] = "\u30c9\u30e9\u30b4\u30f3\u3000\u3000\u3000";
                stringArray[6][1] = "\u30b9\u30e9\u30a4\u30e0\u30de\u30f3\u3000";
                stringArray[7][1] = "\u30a8\u30ea\u30af\u30b5\u30fc\u3000\u3000";
                stringArray[8][1] = "\u9a0e\u58eb\u306e\u5263\u3000\u3000\u3000";
                stringArray[9][1] = "\u9a0e\u58eb\u306e\u76fe\u3000\u3000\u3000";
            }
            stringArray[0][0] = "100";
            stringArray[1][0] = "90";
            stringArray[2][0] = "80";
            stringArray[3][0] = "70";
            stringArray[4][0] = "60";
            stringArray[5][0] = "50";
            stringArray[6][0] = "40";
            stringArray[7][0] = "30";
            stringArray[8][0] = "20";
            stringArray[9][0] = "10";
            stringArray[0][2] = "5000";
            stringArray[1][2] = "4500";
            stringArray[2][2] = "4000";
            stringArray[3][2] = "3500";
            stringArray[4][2] = "3000";
            stringArray[5][2] = "2500";
            stringArray[6][2] = "2000";
            stringArray[7][2] = "1500";
            stringArray[8][2] = "1000";
            stringArray[9][2] = "500";
            stringArray[0][3] = "200";
            stringArray[1][3] = "190";
            stringArray[2][3] = "180";
            stringArray[3][3] = "170";
            stringArray[4][3] = "160";
            stringArray[5][3] = "150";
            stringArray[6][3] = "140";
            stringArray[7][3] = "130";
            stringArray[8][3] = "120";
            stringArray[9][3] = "110";
            stringArray[0][4] = "200";
            stringArray[1][4] = "190";
            stringArray[2][4] = "180";
            stringArray[3][4] = "170";
            stringArray[4][4] = "160";
            stringArray[5][4] = "150";
            stringArray[6][4] = "140";
            stringArray[7][4] = "130";
            stringArray[8][4] = "120";
            stringArray[9][4] = "110";
        } else {
            if (this.mapObject[76][121] == '\u0000') {
                stringArray[0][1] = "Zeno";
                stringArray[1][1] = "Magician A";
                stringArray[2][1] = "Black Knight";
                stringArray[3][1] = "Magic Sergeant";
                stringArray[4][1] = "Gate-Keeper A";
                stringArray[5][1] = "Bloodsucker Bat";
                stringArray[6][1] = "Magician B";
                stringArray[7][1] = "King Slime";
                stringArray[8][1] = "Holy Sword";
                stringArray[9][1] = "Holy Shield";
            } else {
                stringArray[0][1] = "\u9b54\u5c0e\u5e2b\u30bc\u30ce\u3000\u3000";
                stringArray[1][1] = "\u9b54\u8853\u5e2b\uff21\u3000\u3000\u3000";
                stringArray[2][1] = "\u9ed2\u9a0e\u58eb\u3000\u3000\u3000\u3000";
                stringArray[3][1] = "\u9b54\u5c0e\u5e2b\u3000\u3000\u3000\u3000";
                stringArray[4][1] = "\u9580\u756a\uff21\u3000\u3000\u3000\u3000";
                stringArray[5][1] = "\u5438\u8840\u30b3\u30a6\u30e2\u30ea\u3000";
                stringArray[6][1] = "\u9b54\u8853\u5e2b\uff22\u3000\u3000\u3000";
                stringArray[7][1] = "\uff2b\u30b9\u30e9\u30a4\u30e0\u3000\u3000";
                stringArray[8][1] = "\u8056\u5263\u3000\u3000\u3000\u3000\u3000";
                stringArray[9][1] = "\u8056\u76fe\u3000\u3000\u3000\u3000\u3000";
            }
            stringArray[0][0] = "100";
            stringArray[1][0] = "90";
            stringArray[2][0] = "80";
            stringArray[3][0] = "70";
            stringArray[4][0] = "60";
            stringArray[5][0] = "50";
            stringArray[6][0] = "40";
            stringArray[7][0] = "30";
            stringArray[8][0] = "20";
            stringArray[9][0] = "10";
            stringArray[0][2] = "10000";
            stringArray[1][2] = "9000";
            stringArray[2][2] = "8000";
            stringArray[3][2] = "7000";
            stringArray[4][2] = "6000";
            stringArray[5][2] = "5000";
            stringArray[6][2] = "4000";
            stringArray[7][2] = "3000";
            stringArray[8][2] = "2000";
            stringArray[9][2] = "1000";
            stringArray[0][3] = "500";
            stringArray[1][3] = "450";
            stringArray[2][3] = "400";
            stringArray[3][3] = "350";
            stringArray[4][3] = "300";
            stringArray[5][3] = "250";
            stringArray[6][3] = "200";
            stringArray[7][3] = "150";
            stringArray[8][3] = "100";
            stringArray[9][3] = "50";
            stringArray[0][4] = "500";
            stringArray[1][4] = "450";
            stringArray[2][4] = "400";
            stringArray[3][4] = "350";
            stringArray[4][4] = "300";
            stringArray[5][4] = "250";
            stringArray[6][4] = "200";
            stringArray[7][4] = "150";
            stringArray[8][4] = "100";
            stringArray[9][4] = "50";
        }
        boolean bl = false;
        boolean bl2 = false;
        this.FileName = "score/score";
        if (n == 1) {
            this.FileName = this.FileName + "1.dat";
            bl2 = true;
        } else if (n == 2) {
            this.FileName = this.FileName + "2.dat";
            bl2 = true;
        } else if (n == 3) {
            this.FileName = this.FileName + "3.dat";
            bl2 = true;
        } else if (n == 4) {
            this.FileName = this.FileName + "4.dat";
            bl2 = true;
        } else if (n == 5) {
            this.FileName = this.FileName + "5.dat";
            bl2 = true;
        }
        if (bl2) {
            try {
                FileOutputStream fileOutputStream = new FileOutputStream(this.FileName);
                DataOutputStream dataOutputStream = new DataOutputStream(fileOutputStream);
                this.showStatus(this.strMessage[this.mapObject[76][121]][284]);
                this.messageFlag2 = true;
                int n2 = 0;
                while (n2 < 10) {
                    int n3 = 0;
                    while (n3 < 5) {
                        dataOutputStream.writeUTF(stringArray[n2][n3]);
                        ++n3;
                    }
                    ++n2;
                }
                bl = true;
                dataOutputStream.close();
            }
            catch (Exception exception) {
                System.out.println("Error: " + exception);
            }
            if (bl) {
                this.showStatus(this.strMessage[this.mapObject[76][121]][286]);
                this.messageFlag2 = true;
            } else {
                this.showStatus(this.strMessage[this.mapObject[76][121]][287]);
                this.messageFlag2 = true;
            }
        }
    }
}
