// Independent replacement for Vitrite. No code is injected into other processes.
// Build: Framework64/v4.0.30319/csc.exe /target:winexe /platform:x64
//        /codepage:65001 /r:System.Windows.Forms.dll /r:System.Drawing.dll
//        /out:"Vitrite Fixed.exe" "Vitrite Fixed.cs"
using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

internal static class Native
{
    internal const long Layered = 0x80000, Topmost = 8;
    internal delegate IntPtr HookCallback(int code, IntPtr message, IntPtr data);
    [StructLayout(LayoutKind.Sequential)]
    internal struct KeyboardEvent
    {
        internal uint key, scan, flags, time;
        internal UIntPtr extra;
    }
    [DllImport("user32.dll", SetLastError = true)]
    internal static extern IntPtr SetWindowsHookEx(int type, HookCallback callback, IntPtr module, uint thread);
    [DllImport("user32.dll")]
    internal static extern bool UnhookWindowsHookEx(IntPtr hook);
    [DllImport("user32.dll")]
    internal static extern IntPtr CallNextHookEx(IntPtr hook, int code, IntPtr message, IntPtr data);
    [DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
    internal static extern IntPtr GetModuleHandle(string name);
    [DllImport("kernel32.dll")]
    internal static extern void SetLastError(uint error);
    [DllImport("user32.dll")]
    internal static extern short GetAsyncKeyState(int key);
    [DllImport("user32.dll")]
    internal static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")]
    internal static extern bool IsWindow(IntPtr window);
    [DllImport("user32.dll")]
    internal static extern uint GetWindowThreadProcessId(IntPtr window, out uint owner);
    [DllImport("user32.dll", EntryPoint = "GetWindowLongPtrW", SetLastError = true)]
    internal static extern IntPtr GetWindowLongPtr(IntPtr window, int index);
    [DllImport("user32.dll", EntryPoint = "SetWindowLongPtrW", SetLastError = true)]
    internal static extern IntPtr SetWindowLongPtr(IntPtr window, int index, IntPtr value);
    [DllImport("user32.dll", SetLastError = true)]
    internal static extern bool SetLayeredWindowAttributes(IntPtr window, uint color, byte alpha, uint flags);
    [DllImport("user32.dll", SetLastError = true)]
    internal static extern bool GetLayeredWindowAttributes(IntPtr window, out uint color, out byte alpha, out uint flags);
    [DllImport("user32.dll", SetLastError = true)]
    internal static extern bool SetWindowPos(IntPtr window, IntPtr after, int x, int y, int width, int height, uint flags);
}

internal static class WindowActions
{
    internal static void SetOpacity(IntPtr window, int level)
    {
        if (level < 0 || level > 9) throw new ArgumentOutOfRangeException("level");
        if (!Native.IsWindow(window)) throw new Exception("目标窗口已关闭。");
        long style = Native.GetWindowLongPtr(window, -20).ToInt64();
        // An ordinary, non-layered window already has no Vitrite alpha effect.
        if (level == 0 && (style & Native.Layered) == 0) return;
        if ((style & Native.Layered) == 0)
        {
            Native.SetLastError(0);
            IntPtr previous = Native.SetWindowLongPtr(window, -20, new IntPtr(style | Native.Layered));
            int error = Marshal.GetLastWin32Error();
            if (previous == IntPtr.Zero && error != 0) throw new Win32Exception(error);
        }
        byte alpha = level == 0 ? (byte)255 : (byte)(level * 255 / 10);
        if (!Native.SetLayeredWindowAttributes(window, 0, alpha, 2))
            throw new Win32Exception(Marshal.GetLastWin32Error());
        uint color, flags;
        byte actual;
        if (!Native.GetLayeredWindowAttributes(window, out color, out actual, out flags))
            throw new Win32Exception(Marshal.GetLastWin32Error());
        if (actual != alpha || (flags & 2) == 0) throw new Exception("窗口未保持所请求的不透明度。");
    }

    internal static void ToggleTopmost(IntPtr window)
    {
        if (!Native.IsWindow(window)) return;
        bool pinned = (Native.GetWindowLongPtr(window, -20).ToInt64() & Native.Topmost) != 0;
        if (!Native.SetWindowPos(window, new IntPtr(pinned ? -2 : -1), 0, 0, 0, 0, 0x13))
            throw new Win32Exception(Marshal.GetLastWin32Error());
    }
}

internal sealed class ShortcutState
{
    private readonly bool[] held = new bool[256];
    internal void Seed(int key, bool down) { held[key] = down; }
    // Return -2 for no action, -1 for always-on-top, or the transparency level.
    internal int Feed(int key, bool down)
    {
        if (key < 0 || key >= held.Length) return -2;
        bool repeated = held[key];
        held[key] = down;
        if (!down || repeated) return -2;
        bool ctrl = held[0xA2] || held[0xA3];
        bool shift = held[0xA0] || held[0xA1];
        bool alt = held[0xA4] || held[0xA5];
        bool win = held[0x5B] || held[0x5C];
        if (!ctrl || win) return -2;
        if (shift && !alt)
        {
            if (key >= 0x30 && key <= 0x39) return key - 0x30;
            if (key == 0xBB) return -1;
        }
        if (alt && !shift && key == 0x30) return 0;
        return -2;
    }
}

internal sealed class TrayContext : ApplicationContext
{
    private readonly Control dispatch = new Control();
    private readonly NotifyIcon icon = new NotifyIcon();
    private readonly ContextMenuStrip menu = new ContextMenuStrip();
    private readonly ShortcutState keys = new ShortcutState();
    private readonly Native.HookCallback callback;
    private IntPtr hook;
    private DateTime lastError = DateTime.MinValue;

    internal TrayContext()
    {
        IntPtr ignored = dispatch.Handle;
        foreach (int key in new int[] { 0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0x5B, 0x5C })
            keys.Seed(key, Native.GetAsyncKeyState(key) < 0);
        callback = OnKeyboard;
        hook = Native.SetWindowsHookEx(13, callback, Native.GetModuleHandle(null), 0);
        if (hook == IntPtr.Zero)
        {
            int error = Marshal.GetLastWin32Error();
            dispatch.Dispose();
            icon.Dispose();
            menu.Dispose();
            throw new Win32Exception(error);
        }
        menu.Items.Add("使用说明", null, delegate { ShowHelp(); });
        menu.Items.Add("退出", null, delegate { ExitThread(); });
        icon.Icon = SystemIcons.Application;
        icon.Text = "Vitrite Fixed — Ctrl+Shift+0 恢复不透明";
        icon.ContextMenuStrip = menu;
        icon.DoubleClick += delegate { ShowHelp(); };
        icon.Visible = true;
        icon.ShowBalloonTip(3000, "Vitrite Fixed 已启动", "Ctrl+Shift+1～9 调节；Ctrl+Shift+0 恢复。备用恢复键：Ctrl+Alt+0。", ToolTipIcon.Info);
    }

    private void ShowHelp()
    {
        MessageBox.Show("点击目标窗口后操作：\n\nCtrl + Shift + 1～9：10%～90% 不透明度\nCtrl + Shift + 0：100% 不透明\nCtrl + Alt + 0：备用恢复键\nCtrl + Shift + 加号所在键：切换置顶\n\n使用主键盘数字键。请先退出原版 Vitrite。\n右键托盘图标可退出本程序。", "Vitrite Fixed");
    }

    private IntPtr OnKeyboard(int code, IntPtr message, IntPtr data)
    {
        if (code >= 0)
        {
            int msg = message.ToInt32();
            if (msg == 0x100 || msg == 0x104 || msg == 0x101 || msg == 0x105)
            {
                Native.KeyboardEvent input = (Native.KeyboardEvent)Marshal.PtrToStructure(data, typeof(Native.KeyboardEvent));
                int action = keys.Feed((int)input.key, msg == 0x100 || msg == 0x104);
                if (action >= -1)
                {
                    IntPtr window = Native.GetForegroundWindow();
                    uint owner;
                    Native.GetWindowThreadProcessId(window, out owner);
                    uint expectedOwner = owner;
                    if (window != IntPtr.Zero && owner != (uint)Process.GetCurrentProcess().Id)
                    {
                        // Window operations run after the hook returns, keeping keyboard input responsive.
                        dispatch.BeginInvoke((MethodInvoker)delegate
                        {
                            uint currentOwner;
                            Native.GetWindowThreadProcessId(window, out currentOwner);
                            if (!Native.IsWindow(window) || currentOwner != expectedOwner) return;
                            try
                            {
                                if (action == -1) WindowActions.ToggleTopmost(window);
                                else WindowActions.SetOpacity(window, action);
                            }
                            catch (Exception error)
                            {
                                if ((DateTime.UtcNow - lastError).TotalSeconds >= 5)
                                {
                                    lastError = DateTime.UtcNow;
                                    icon.ShowBalloonTip(4000, "无法更改该窗口", error.Message, ToolTipIcon.Warning);
                                }
                            }
                        });
                    }
                }
            }
        }
        // Preserve the original program's pass-through keyboard behavior.
        return Native.CallNextHookEx(hook, code, message, data);
    }

    protected override void ExitThreadCore()
    {
        if (hook != IntPtr.Zero) { Native.UnhookWindowsHookEx(hook); hook = IntPtr.Zero; }
        icon.Visible = false;
        icon.Dispose();
        menu.Dispose();
        dispatch.Dispose();
        base.ExitThreadCore();
    }
}

internal static class Program
{
    private static void Require(bool success, string label)
    {
        if (!success) throw new Exception(label);
    }

    private static void SelfTest(string report)
    {
        ShortcutState state = new ShortcutState();
        Require(state.Feed(0x30, true) == -2, "Bare 0 must not trigger");
        state.Feed(0x30, false);
        state.Feed(0xA2, true);
        state.Feed(0xA1, true);
        for (int i = 0; i <= 9; i++)
        {
            Require(state.Feed(0x30 + i, true) == i, "Digit hotkey " + i);
            Require(state.Feed(0x30 + i, true) == -2, "No repeated action");
            state.Feed(0x30 + i, false);
        }
        Require(state.Feed(0x60, true) == -2, "Ignore numpad");
        Require(state.Feed(0xBB, true) == -1, "Topmost hotkey");
        state.Feed(0xA1, false);
        state.Feed(0xA4, true);
        Require(state.Feed(0x30, true) == 0, "Fallback restore");
        state.Feed(0x30, false);
        state.Feed(0x5B, true);
        Require(state.Feed(0x30, true) == -2, "Ignore Windows-key combinations");
        using (Form form = new Form())
        {
            IntPtr window = form.Handle;
            for (int i = 1; i <= 9; i++)
            {
                WindowActions.SetOpacity(window, i);
                WindowActions.SetOpacity(window, 0);
                uint color, flags;
                byte alpha;
                Require(Native.GetLayeredWindowAttributes(window, out color, out alpha, out flags) && alpha == 255, "Restore after level " + i);
                Require((Native.GetWindowLongPtr(window, -20).ToInt64() & Native.Layered) != 0, "Restore preserves layered style");
            }
            WindowActions.ToggleTopmost(window);
            Require((Native.GetWindowLongPtr(window, -20).ToInt64() & Native.Topmost) != 0, "Pin window");
            WindowActions.ToggleTopmost(window);
            Require((Native.GetWindowLongPtr(window, -20).ToInt64() & Native.Topmost) == 0, "Unpin window");
        }
        File.WriteAllText(report, "PASS: shortcut decoding, fallback, repeat filtering, opacity 1-9 -> 0 with native readback, layered style preserved, topmost toggle.\r\n");
    }

    [STAThread]
    private static int Main(string[] args)
    {
        Application.EnableVisualStyles();
        try
        {
            if (args.Length == 2 && args[0] == "--self-test")
            {
                try { SelfTest(args[1]); return 0; }
                catch (Exception error) { File.WriteAllText(args[1], "FAIL: " + error); return 1; }
            }
            if (args.Length == 1 && args[0] == "--restore-milthm")
            {
                Process[] targets = Process.GetProcessesByName("Milthm");
                if (targets.Length != 1) throw new Exception("请保持恰好一个 Milthm 正在运行。");
                using (Process target = targets[0]) WindowActions.SetOpacity(target.MainWindowHandle, 0);
                return 0;
            }
            bool created;
            using (Mutex instance = new Mutex(true, "Local\\VitriteFixed.20261014", out created))
            {
                if (!created) { MessageBox.Show("Vitrite Fixed 已在运行，请查看系统托盘。", "Vitrite Fixed"); return 0; }
                if (Process.GetProcessesByName("Vitrite").Length != 0)
                {
                    MessageBox.Show("请先右键原版 Vitrite 的托盘图标并选择 Exit，然后重新打开本程序。", "Vitrite Fixed");
                    return 2;
                }
                using (TrayContext context = new TrayContext()) Application.Run(context);
                instance.ReleaseMutex();
            }
            return 0;
        }
        catch (Exception error)
        {
            MessageBox.Show(error.Message, "Vitrite Fixed", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return 1;
        }
    }
}
