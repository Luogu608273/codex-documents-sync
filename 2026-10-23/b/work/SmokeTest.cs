using System;
using System.Collections.Generic;
using System.Drawing;
using System.Reflection;
using System.Windows.Forms;

static class SmokeTest
{
    [STAThread]
    static int Main(string[] args)
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        Type type = Assembly.LoadFrom(args[0]).GetType("KeyboardMonitor", true);
        using (Form form = (Form)Activator.CreateInstance(type))
        {
            form.Show();
            Application.DoEvents();
            ((Timer)type.GetField("timer", BindingFlags.NonPublic | BindingFlags.Instance).GetValue(form)).Stop();
            IntPtr handle = form.Handle;
            Label label = (Label)type.GetField("active", BindingFlags.NonPublic | BindingFlags.Instance).GetValue(form);
            MethodInfo set = type.GetMethod("SetPressed", BindingFlags.NonPublic | BindingFlags.Instance);
            set.Invoke(form, new object[] { new HashSet<int>() });
            if (label.Text != "当前没有按键按下") throw new Exception("Initial state");
            set.Invoke(form, new object[] { new HashSet<int> { 0x41 } });
            if (label.Text != "A") throw new Exception("Single key");
            set.Invoke(form, new object[] { new HashSet<int> { 0x41, 0xA2 } });
            if (label.Text != "L Ctrl  +  A") throw new Exception("Combination");
            using (Bitmap preview = new Bitmap(form.Width, form.Height))
            {
                form.DrawToBitmap(preview, new Rectangle(0, 0, form.Width, form.Height));
                preview.Save(args[1], System.Drawing.Imaging.ImageFormat.Png);
            }
            set.Invoke(form, new object[] { new HashSet<int> { 0x41 } });
            if (label.Text != "A") throw new Exception("Partial release");
            set.Invoke(form, new object[] { new HashSet<int>() });
            if (label.Text != "当前没有按键按下") throw new Exception("Full release");
            CheckBox pin = (CheckBox)type.GetField("pin", BindingFlags.NonPublic | BindingFlags.Instance).GetValue(form);
            pin.Checked = true;
            if (!form.TopMost) throw new Exception("Pin state");
            pin.Checked = false;
            type.GetMethod("PollKeyboard", BindingFlags.NonPublic | BindingFlags.Instance).Invoke(form, null);
            Console.WriteLine("PASS: startup, single key, combination, partial/full release, pin, native polling, rendering.");
        }
        return 0;
    }
}
