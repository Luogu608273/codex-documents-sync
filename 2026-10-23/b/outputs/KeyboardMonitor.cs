using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Runtime.InteropServices;
using System.Windows.Forms;

// Windows 桌面键盘状态查看器。只显示当前状态，不保存按键历史。
public sealed class KeyboardMonitor : Form
{
    [DllImport("user32.dll")]
    private static extern short GetAsyncKeyState(int key);

    private sealed class KeyCap
    {
        public int Code;
        public string Label;
        public RectangleF Bounds;
        public KeyCap(int code, string label, float x, float y, float width)
        {
            Code = code;
            Label = label;
            Bounds = new RectangleF(x, y, width, 43);
        }
    }

    private readonly List<KeyCap> caps = new List<KeyCap>();
    private readonly Dictionary<int, string> names = new Dictionary<int, string>();
    private HashSet<int> pressed = new HashSet<int>();
    private readonly Timer timer = new Timer();
    private readonly Label active = new Label();
    private readonly CheckBox pin = new CheckBox();
    private readonly Font headingFont = new Font("Microsoft YaHei UI", 18, FontStyle.Bold);
    private readonly Font captionFont = new Font("Microsoft YaHei UI", 9);
    private readonly Font keyFont = new Font("Segoe UI", 9, FontStyle.Bold);
    private readonly Font smallKeyFont = new Font("Segoe UI", 7.5f, FontStyle.Bold);
    private static readonly Color BackgroundColor = Color.FromArgb(19, 25, 36);
    private static readonly Color TextColor = Color.FromArgb(232, 238, 247);
    private static readonly Color MutedColor = Color.FromArgb(152, 168, 189);

    public KeyboardMonitor()
    {
        Text = "键盘按键监测";
        ClientSize = new Size(1120, 560);
        FormBorderStyle = FormBorderStyle.FixedSingle;
        MaximizeBox = false;
        StartPosition = FormStartPosition.CenterScreen;
        BackColor = BackgroundColor;
        ForeColor = TextColor;
        AutoScaleMode = AutoScaleMode.Dpi;
        DoubleBuffered = true;

        active.SetBounds(26, 91, 1068, 75);
        active.Font = new Font("Microsoft YaHei UI", 18, FontStyle.Bold);
        active.ForeColor = Color.FromArgb(91, 225, 189);
        active.BackColor = Color.FromArgb(28, 37, 52);
        active.Padding = new Padding(15, 8, 15, 8);
        active.TextAlign = ContentAlignment.MiddleLeft;
        active.AutoEllipsis = true;
        active.Text = "当前没有按键按下";
        Controls.Add(active);

        pin.SetBounds(991, 30, 105, 27);
        pin.Text = "窗口置顶";
        pin.Font = captionFont;
        pin.CheckedChanged += delegate { TopMost = pin.Checked; };
        Controls.Add(pin);

        BuildKeyboard();
        timer.Interval = 16;
        timer.Tick += delegate { PollKeyboard(); };
        timer.Start();
    }

    private void Add(int code, string label, float x, float y, float width)
    {
        caps.Add(new KeyCap(code, label, x, y, width));
        names[code] = label;
    }

    private void Row(float y, int[] codes, string[] labels, float[] widths)
    {
        float x = 26;
        for (int i = 0; i < codes.Length; i++)
        {
            float w = widths == null ? 45 : widths[i];
            Add(codes[i], labels[i], x, y, w);
            x += w + 5;
        }
    }

    private void BuildKeyboard()
    {
        Add(0x1B, "Esc", 26, 196, 45);
        for (int i = 0; i < 12; i++)
            Add(0x70 + i, "F" + (i + 1), 96 + i * 49, 196, 44);

        Row(251,
            new int[] {0xC0,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x30,0xBD,0xBB,0x08},
            new string[] {"`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"},
            new float[] {45,45,45,45,45,45,45,45,45,45,45,45,45,75});
        Row(299,
            new int[] {0x09,0x51,0x57,0x45,0x52,0x54,0x59,0x55,0x49,0x4F,0x50,0xDB,0xDD,0xDC},
            new string[] {"Tab","Q","W","E","R","T","Y","U","I","O","P","[","]","\\"},
            new float[] {60,45,45,45,45,45,45,45,45,45,45,45,45,60});
        Row(347,
            new int[] {0x14,0x41,0x53,0x44,0x46,0x47,0x48,0x4A,0x4B,0x4C,0xBA,0xDE,0x0D},
            new string[] {"Caps","A","S","D","F","G","H","J","K","L",";","'","Enter"},
            new float[] {75,45,45,45,45,45,45,45,45,45,45,45,95});
        Row(395,
            new int[] {0xA0,0x5A,0x58,0x43,0x56,0x42,0x4E,0x4D,0xBC,0xBE,0xBF,0xA1},
            new string[] {"L Shift","Z","X","C","V","B","N","M",",",".","/","R Shift"},
            new float[] {100,45,45,45,45,45,45,45,45,45,45,120});
        Row(443,
            new int[] {0xA2,0x5B,0xA4,0x20,0xA5,0x5C,0x5D,0xA3},
            new string[] {"L Ctrl","L Win","L Alt","Space","R Alt","R Win","Menu","R Ctrl"},
            new float[] {60,50,55,270,55,50,50,70});

        int[] navCodes = {0x2C,0x91,0x13,0x2D,0x24,0x21,0x2E,0x23,0x22};
        string[] navLabels = {"PrtSc","Scroll","Pause","Insert","Home","PgUp","Delete","End","PgDn"};
        for (int i = 0; i < navCodes.Length; i++)
            Add(navCodes[i], navLabels[i], 764 + (i % 3) * 50, 196 + (i / 3) * 55, 45);
        Add(0x26, "Up", 814, 395, 45);
        Add(0x25, "Left", 764, 443, 45);
        Add(0x28, "Down", 814, 443, 45);
        Add(0x27, "Right", 864, 443, 45);

        int[] numCodes = {0x90,0x6F,0x6A,0x6D,0x67,0x68,0x69,0x6B,0x64,0x65,0x66,0x61,0x62,0x63,0x60,0x6E};
        string[] numLabels = {"Num","/","*","-","7","8","9","+","4","5","6","1","2","3","0","."};
        int[] numRows = {0,0,0,0,1,1,1,1,2,2,2,3,3,3,4,4};
        int[] numCols = {0,1,2,3,0,1,2,3,0,1,2,0,1,2,0,2};
        for (int i = 0; i < numCodes.Length; i++)
        {
            Add(numCodes[i], numLabels[i], 930 + numCols[i] * 41, 251 + numRows[i] * 48, numCodes[i] == 0x60 ? 77 : 36);
            names[numCodes[i]] = "Num " + numLabels[i];
        }
        // GetAsyncKeyState 按虚拟键码区分按键；主回车与小键盘回车共享 Enter。
        Add(0x0D, "Enter", 1053, 395, 36);
        names[0x0D] = "Enter";
        names[0xAD] = "静音";
        names[0xAE] = "音量减";
        names[0xAF] = "音量加";
        names[0xB0] = "下一曲";
        names[0xB1] = "上一曲";
        names[0xB2] = "停止播放";
        names[0xB3] = "播放 / 暂停";
    }

    private void PollKeyboard()
    {
        HashSet<int> current = new HashSet<int>();
        for (int code = 8; code < 255; code++)
        {
            // 只读取高位（当前是否按住），忽略通用修饰键的重复状态。
            if (code == 0x10 || code == 0x11 || code == 0x12) continue;
            if ((GetAsyncKeyState(code) & 0x8000) != 0) current.Add(code);
        }
        SetPressed(current);
    }

    private void SetPressed(HashSet<int> current)
    {
        if (pressed.SetEquals(current)) return;
        pressed = new HashSet<int>(current);
        List<int> ordered = new List<int>(current);
        ordered.Sort(delegate(int a, int b) {
            bool am = a >= 0xA0 && a <= 0xA5 || a == 0x5B || a == 0x5C;
            bool bm = b >= 0xA0 && b <= 0xA5 || b == 0x5B || b == 0x5C;
            return am == bm ? a.CompareTo(b) : (am ? -1 : 1);
        });
        List<string> labels = new List<string>();
        foreach (int code in ordered)
        {
            string name;
            if (!names.TryGetValue(code, out name)) name = ((Keys)code).ToString();
            labels.Add(name);
        }
        active.Text = labels.Count == 0 ? "当前没有按键按下" : string.Join("  +  ", labels.ToArray());
        Invalidate();
    }

    protected override void OnPaint(PaintEventArgs e)
    {
        base.OnPaint(e);
        Graphics g = e.Graphics;
        // 绘图和控件使用同一个 DPI 比例。
        g.ScaleTransform(ClientSize.Width / 1120f, ClientSize.Height / 560f);
        g.SmoothingMode = SmoothingMode.AntiAlias;
        using (Brush text = new SolidBrush(TextColor))
        using (Brush muted = new SolidBrush(MutedColor))
        {
            g.DrawString("键盘按键监测", headingFont, text, 24, 23);
            g.DrawString("实时显示按住的键 · 切换到其他窗口后仍可查看", captionFont, muted, 26, 61);
            g.DrawString("按下任意键试试，多键同时按下会一起显示。", captionFont, muted, 26, 170);
            g.DrawString("仅显示当前状态，不记录历史。键位按常见美式布局显示。", captionFont, muted, 26, 507);
            g.DrawString("Fn 键通常由硬件处理，无法检测；两处 Enter 共享状态。", captionFont, muted, 26, 530);
        }
        using (StringFormat format = new StringFormat())
        {
            format.Alignment = StringAlignment.Center;
            format.LineAlignment = StringAlignment.Center;
            foreach (KeyCap cap in caps)
            {
                bool down = pressed.Contains(cap.Code);
                using (Brush fill = new SolidBrush(down ? Color.FromArgb(70, 211, 175) : Color.FromArgb(37, 48, 66)))
                using (Brush ink = new SolidBrush(down ? BackgroundColor : TextColor))
                using (Pen edge = new Pen(down ? Color.FromArgb(123, 255, 218) : Color.FromArgb(56, 72, 94)))
                {
                    g.FillRectangle(fill, cap.Bounds);
                    g.DrawRectangle(edge, cap.Bounds.X, cap.Bounds.Y, cap.Bounds.Width, cap.Bounds.Height);
                    Font font = cap.Label.Length > 5 || cap.Bounds.Width < 40 ? smallKeyFont : keyFont;
                    g.DrawString(cap.Label, font, ink, cap.Bounds, format);
                }
            }
        }
    }

    protected override void Dispose(bool disposing)
    {
        if (disposing)
        {
            timer.Dispose();
            active.Dispose();
            pin.Dispose();
            headingFont.Dispose();
            captionFont.Dispose();
            keyFont.Dispose();
            smallKeyFont.Dispose();
        }
        base.Dispose(disposing);
    }

    [STAThread]
    public static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        Application.Run(new KeyboardMonitor());
    }
}
