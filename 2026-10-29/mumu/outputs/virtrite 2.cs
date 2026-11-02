// Windows x64 / .NET Framework 4.x. See Build.ps1 for build instructions.
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Windows.Forms;

[assembly: System.Reflection.AssemblyTitle("virtrite 2")]
[assembly: System.Reflection.AssemblyProduct("virtrite 2")]
[assembly: System.Reflection.AssemblyVersion("2.0.0.0")]
[assembly: System.Reflection.AssemblyFileVersion("2.0.2.0")]

internal static class Native
{
    internal const long Layered = 0x80000;
    internal delegate bool EnumCallback(IntPtr window, IntPtr data);
    internal delegate IntPtr HookCallback(int code, IntPtr message, IntPtr data);
    [StructLayout(LayoutKind.Sequential)]
    internal struct KeyboardEvent { internal uint key, scan, flags, time; internal UIntPtr extra; }
    [DllImport("user32.dll")] internal static extern bool EnumWindows(EnumCallback callback, IntPtr data);
    [DllImport("user32.dll")] internal static extern bool IsWindow(IntPtr window);
    [DllImport("user32.dll")] internal static extern bool IsWindowVisible(IntPtr window);
    [DllImport("user32.dll")] internal static extern bool IsIconic(IntPtr window);
    [DllImport("user32.dll")] internal static extern IntPtr GetAncestor(IntPtr window, uint flags);
    [DllImport("user32.dll")] internal static extern IntPtr GetWindow(IntPtr window, uint command);
    [DllImport("user32.dll")] internal static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] internal static extern uint GetWindowThreadProcessId(IntPtr window, out uint owner);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] internal static extern int GetClassName(IntPtr window, StringBuilder text, int count);
    [DllImport("user32.dll", EntryPoint = "GetWindowLongPtrW", SetLastError = true)] internal static extern IntPtr GetWindowLongPtr(IntPtr window, int index);
    [DllImport("user32.dll", EntryPoint = "SetWindowLongPtrW", SetLastError = true)] internal static extern IntPtr SetWindowLongPtr(IntPtr window, int index, IntPtr value);
    [DllImport("user32.dll", SetLastError = true)] internal static extern bool SetLayeredWindowAttributes(IntPtr window, uint color, byte alpha, uint flags);
    [DllImport("user32.dll", SetLastError = true)] internal static extern bool GetLayeredWindowAttributes(IntPtr window, out uint color, out byte alpha, out uint flags);
    [DllImport("user32.dll", SetLastError = true)] internal static extern bool SetWindowPos(IntPtr window, IntPtr after, int x, int y, int width, int height, uint flags);
    [DllImport("kernel32.dll")] internal static extern void SetLastError(uint error);
    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)] internal static extern IntPtr LoadLibrary(string file);
    [DllImport("kernel32.dll", CharSet = CharSet.Ansi, SetLastError = true)] internal static extern IntPtr GetProcAddress(IntPtr module, string name);
    [DllImport("kernel32.dll")] internal static extern bool FreeLibrary(IntPtr module);
    [DllImport("kernel32.dll", CharSet = CharSet.Unicode)] internal static extern IntPtr GetModuleHandle(string name);
    [DllImport("user32.dll", SetLastError = true)] internal static extern IntPtr SetWindowsHookEx(int type, IntPtr callback, IntPtr module, uint thread);
    [DllImport("user32.dll", SetLastError = true)] internal static extern IntPtr SetWindowsHookEx(int type, HookCallback callback, IntPtr module, uint thread);
    [DllImport("user32.dll")] internal static extern bool UnhookWindowsHookEx(IntPtr hook);
    [DllImport("user32.dll")] internal static extern IntPtr CallNextHookEx(IntPtr hook, int code, IntPtr message, IntPtr data);
    [DllImport("user32.dll")] internal static extern short GetAsyncKeyState(int key);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] internal static extern uint RegisterWindowMessage(string text);
    [DllImport("user32.dll", SetLastError = true)] internal static extern IntPtr SendMessageTimeout(IntPtr window, uint message, UIntPtr wParam, IntPtr lParam, uint flags, uint timeout, out UIntPtr result);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] internal static extern IntPtr GetProp(IntPtr window, string name);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] internal static extern IntPtr RemoveProp(IntPtr window, string name);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] internal static extern IntPtr FindWindowEx(IntPtr parent, IntPtr after, string className, string title);
}

internal static class Log
{
    internal static readonly string DirectoryPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "virtrite 2");
    internal static void Write(string message)
    {
        try
        {
            Directory.CreateDirectory(DirectoryPath);
            string path = Path.Combine(DirectoryPath, "virtrite 2.log");
            if (File.Exists(path) && new FileInfo(path).Length > 1024 * 1024) File.WriteAllText(path, "");
            File.AppendAllText(path, DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss ") + message + Environment.NewLine);
        }
        catch { }
    }
    internal static string Explain(Exception error)
    {
        Win32Exception native = error as Win32Exception;
        if (native != null && native.NativeErrorCode == 5)
            return "拒绝访问：目标窗口权限更高。请手动以管理员身份启动 virtrite 2 后重试。";
        return error.Message;
    }
}

internal static class MuMuWindows
{
    internal static uint Owner(IntPtr window)
    {
        uint owner;
        Native.GetWindowThreadProcessId(window, out owner);
        return owner;
    }
    internal static bool IsMuMu(IntPtr window)
    {
        if (!Native.IsWindow(window)) return false;
        try
        {
            using (Process process = Process.GetProcessById((int)Owner(window)))
                return string.Equals(process.ProcessName, "MuMuPlayer", StringComparison.OrdinalIgnoreCase);
        }
        catch { return false; }
    }
    internal static IntPtr Resolve(IntPtr window)
    {
        IntPtr root = Native.GetAncestor(window, 3); // GA_ROOTOWNER also follows MuMu's owned overlays.
        if (root != IntPtr.Zero && IsMuMu(root)) return root;
        return IntPtr.Zero;
    }
    internal static List<IntPtr> Roots(bool includeHidden = true)
    {
        HashSet<uint> owners = new HashSet<uint>();
        foreach (Process process in Process.GetProcessesByName("MuMuPlayer"))
        {
            using (process) owners.Add((uint)process.Id);
        }
        List<IntPtr> windows = new List<IntPtr>();
        Native.EnumWindows(delegate(IntPtr window, IntPtr data)
        {
            if (!owners.Contains(Owner(window)) || Native.GetWindow(window, 4) != IntPtr.Zero) return true;
            if ((Native.GetWindowLongPtr(window, -16).ToInt64() & 0x40000000) != 0) return true;
            StringBuilder name = new StringBuilder(256);
            Native.GetClassName(window, name, name.Capacity);
            string className = name.ToString();
            if (!Native.IsWindowVisible(window) && (!includeHidden || !className.EndsWith("QWindowIcon", StringComparison.Ordinal))) return true;
            if (className.StartsWith("Qt", StringComparison.Ordinal)) windows.Add(window);
            return true;
        }, IntPtr.Zero);
        return windows;
    }
}

internal static class QtBridge
{
    private const string StatusName = "Codex.MuMuOpacity.QtBridge.Status.20261030";
    private sealed class Session
    {
        internal uint Owner;
        internal IntPtr Library, Before, After;
        internal void Dispose()
        {
            if (Before != IntPtr.Zero) Native.UnhookWindowsHookEx(Before);
            if (After != IntPtr.Zero) Native.UnhookWindowsHookEx(After);
            if (Library != IntPtr.Zero) Native.FreeLibrary(Library);
        }
    }
    private static readonly Dictionary<uint, Session> sessions = new Dictionary<uint, Session>();
    private static Session GetSession(uint thread, uint owner)
    {
        Session session;
        if (sessions.TryGetValue(thread, out session))
        {
            if (session.Owner == owner) return session;
            session.Dispose();
            sessions.Remove(thread);
        }
        string path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "MuMuQtBridge.dll");
        session = new Session { Owner = owner, Library = Native.LoadLibrary(path) };
        if (session.Library == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error(), "无法加载 MuMuQtBridge.dll，请将它与程序放在同一目录。");
        try
        {
            IntPtr before = Native.GetProcAddress(session.Library, "MuMuOpacityHook");
            IntPtr after = Native.GetProcAddress(session.Library, "MuMuOpacityAfterHook");
            if (before == IntPtr.Zero || after == IntPtr.Zero) throw new Exception("MuMuQtBridge.dll 版本不匹配。");
            session.After = Native.SetWindowsHookEx(12, after, session.Library, thread);
            if (session.After == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error());
            session.Before = Native.SetWindowsHookEx(4, before, session.Library, thread);
            if (session.Before == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error());
            sessions[thread] = session;
            return session;
        }
        catch { session.Dispose(); throw; }
    }
    internal static void ReleaseAll()
    {
        foreach (Session session in sessions.Values) session.Dispose();
        sessions.Clear();
    }
    internal static void SetOpacity(IntPtr window, byte alpha)
    {
        // Set Qt's own opacity on its GUI thread. Setting WS_EX_LAYERED from outside
        // gets undone by Qt and a repeated style-enforcement loop causes flicker.
        if (!MuMuWindows.IsMuMu(window)) throw new Exception("目标不是 MuMuPlayer 窗口。");
        uint owner;
        uint thread = Native.GetWindowThreadProcessId(window, out owner);
        GetSession(thread, owner);
            uint command = Native.RegisterWindowMessage("Codex.MuMuOpacity.QtBridge.Apply.20261030");
            Native.RemoveProp(window, StatusName);
            UIntPtr result;
            if (Native.SendMessageTimeout(window, command, new UIntPtr(0x4D550000u | alpha), IntPtr.Zero, 2, 2000, out result) == IntPtr.Zero)
                throw new Win32Exception(Marshal.GetLastWin32Error(), "MuMu 窗口未及时响应，请稍后重试。");
            long status = Native.GetProp(window, StatusName).ToInt64();
            Native.RemoveProp(window, StatusName);
            if (status != 1) throw new Exception("当前 MuMu 窗口不支持此 Qt 适配接口（状态 " + status + "）。");
            uint color, flags;
            byte actual;
            bool layered = (Native.GetWindowLongPtr(window, -20).ToInt64() & Native.Layered) != 0;
            // Qt normally removes its own layered style at opacity 1.0. That is
            // correct here; generic-window restore below always writes alpha 255.
            if (alpha == 255 && !layered) return;
            if (!Native.GetLayeredWindowAttributes(window, out color, out actual, out flags) || actual != alpha || (flags & 2) == 0)
                throw new Exception("MuMu 未保持所请求的不透明度。");
    }
}

internal static class WindowActions
{
    internal static byte Alpha(int level)
    {
        if (level < 0 || level > 9) throw new ArgumentOutOfRangeException("level");
        return level == 0 ? (byte)255 : (byte)Math.Round(level * 255.0 / 10.0);
    }
    internal static bool MatchesOpacity(IntPtr window, byte expected)
    {
        if (!Native.IsWindow(window)) return false;
        long style = Native.GetWindowLongPtr(window, -20).ToInt64();
        if ((style & Native.Layered) == 0) return expected == 255;
        uint color, flags; byte actual;
        return Native.GetLayeredWindowAttributes(window, out color, out actual, out flags) && (flags & 2) != 0 && actual == expected;
    }
    internal static IntPtr SetOpacity(IntPtr window, int level)
    {
        byte alpha = Alpha(level);
        if (!Native.IsWindow(window)) throw new Exception("目标窗口已关闭。");
        IntPtr mumu = MuMuWindows.Resolve(window);
        if (mumu != IntPtr.Zero)
        {
            QtBridge.SetOpacity(mumu, alpha);
            return mumu;
        }
        long style = Native.GetWindowLongPtr(window, -20).ToInt64();
        uint color = 0, flags = 0;
        byte previous;
        Native.GetLayeredWindowAttributes(window, out color, out previous, out flags);
        if ((style & Native.Layered) == 0)
        {
            Native.SetLastError(0);
            IntPtr old = Native.SetWindowLongPtr(window, -20, new IntPtr(style | Native.Layered));
            int error = Marshal.GetLastWin32Error();
            if (old == IntPtr.Zero && error != 0) throw new Win32Exception(error);
        }
        // Ctrl+Shift+0 explicitly sets alpha=255. Do not toggle/remove layered style.
        // Preserve an existing color key, which may define the shape of a window.
        if (!Native.SetLayeredWindowAttributes(window, color, alpha, 2 | (flags & 1)))
            throw new Win32Exception(Marshal.GetLastWin32Error());
        uint actualColor, actualFlags;
        byte actualAlpha;
        if (!Native.GetLayeredWindowAttributes(window, out actualColor, out actualAlpha, out actualFlags))
            throw new Win32Exception(Marshal.GetLastWin32Error());
        if (actualAlpha != alpha || (actualFlags & 2) == 0) throw new Exception("窗口未保持所请求的不透明度。");
        return window;
    }
    internal static void ToggleTopmost(IntPtr window)
    {
        bool pinned = (Native.GetWindowLongPtr(window, -20).ToInt64() & 8) != 0;
        if (!Native.SetWindowPos(window, new IntPtr(pinned ? -2 : -1), 0, 0, 0, 0, 0x13))
            throw new Win32Exception(Marshal.GetLastWin32Error());
    }
}

internal sealed class ShortcutState
{
    private readonly bool[] held = new bool[256];
    internal void Seed(int key, bool down) { held[key] = down; }
    // -2: no action; -1: pin; 0..9: foreground opacity; 100..109: all MuMu.
    internal int Feed(int key, bool down)
    {
        if (key < 0 || key >= held.Length) return -2;
        bool repeated = held[key];
        held[key] = down;
        if (!down || repeated) return -2;
        bool ctrl = held[0xA2] || held[0xA3];
        bool shift = held[0xA0] || held[0xA1];
        bool alt = held[0xA4] || held[0xA5];
        if (!ctrl || held[0x5B] || held[0x5C]) return -2;
        if (shift && !alt)
        {
            if (key >= 0x30 && key <= 0x39) return key - 0x30;
            if (key == 0xBB) return -1;
        }
        if (alt && !shift && key == 0x30) return 0;
        if (alt && shift && key >= 0x30 && key <= 0x39) return 100 + key - 0x30;
        return -2;
    }
}

internal sealed class CommandWindow : NativeWindow, IDisposable
{
    internal const uint MessageId = 0x8061;
    internal const string Caption = "virtrite 2.CommandWindow.20261030";
    private readonly Action<int, int> action;
    internal CommandWindow(Action<int, int> action, string caption = Caption)
    {
        this.action = action;
        CreateHandle(new CreateParams { Caption = caption, Parent = new IntPtr(-3) });
    }
    protected override void WndProc(ref Message message)
    {
        if ((uint)message.Msg == MessageId)
        {
            action(message.WParam.ToInt32(), message.LParam.ToInt32());
            message.Result = new IntPtr(1);
            return;
        }
        base.WndProc(ref message);
    }
    public void Dispose() { DestroyHandle(); }
}

internal sealed class TrayContext : ApplicationContext
{
    private sealed class MuMuPreference
    {
        internal int Level;
        internal long ProcessStarted;
        internal DateTime RetryAfter;
        internal bool Suspended;
        internal readonly Queue<DateTime> RecentRepairs = new Queue<DateTime>();
    }
    private readonly Control dispatch = new Control();
    private readonly NotifyIcon icon = new NotifyIcon();
    private readonly ContextMenuStrip menu = new ContextMenuStrip();
    private readonly ShortcutState keys = new ShortcutState();
    private readonly Dictionary<IntPtr, uint> touched = new Dictionary<IntPtr, uint>();
    private readonly Dictionary<uint, MuMuPreference> mumuPreferences = new Dictionary<uint, MuMuPreference>();
    private readonly System.Windows.Forms.Timer timer = new System.Windows.Forms.Timer();
    private readonly Native.HookCallback callback;
    private readonly CommandWindow commands;
    private IntPtr hook;
    private int? allMuMuLevel;
    private DateTime lastError = DateTime.MinValue;

    internal TrayContext(int? initialMuMuLevel)
    {
        IntPtr ignored = dispatch.Handle;
        foreach (int key in new int[] { 0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0x5B, 0x5C }) keys.Seed(key, Native.GetAsyncKeyState(key) < 0);
        callback = OnKeyboard;
        hook = Native.SetWindowsHookEx(13, callback, Native.GetModuleHandle(null), 0);
        if (hook == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error());
        commands = new CommandWindow(OnCommand);
        menu.Items.Add("使用说明", null, delegate { ShowHelp(); });
        ToolStripMenuItem mumu = new ToolStripMenuItem("MuMu 不透明度");
        foreach (int level in new int[] { 1, 3, 5, 7, 9, 0 })
        {
            int selected = level;
            mumu.DropDownItems.Add((level == 0 ? 100 : level * 10) + "%", null, delegate { TryAction(delegate { SetAllMuMu(selected); }); });
        }
        menu.Items.Add(mumu);
        menu.Items.Add("全部恢复不透明", null, delegate { RestoreAll(); });
        menu.Items.Add("恢复并退出", null, delegate { ExitThread(); });
        icon.Icon = SystemIcons.Application;
        icon.Text = "virtrite 2";
        icon.ContextMenuStrip = menu;
        icon.DoubleClick += delegate { ShowHelp(); };
        icon.Visible = true;
        timer.Interval = 300;
        timer.Tick += delegate { TryAction(KeepMuMuOpacity); };
        timer.Start();
        if (initialMuMuLevel.HasValue) TryAction(delegate { SetAllMuMu(initialMuMuLevel.Value); });
        Log.Write("Started. Keyboard hook installed; no window was activated.");
    }
    private void ShowHelp()
    {
        MessageBox.Show("点击目标窗口后操作：\n\nCtrl + Shift + 1～9：10%～90% 不透明度\nCtrl + Shift + 0：100% 不透明\nCtrl + Alt + 0：备用恢复键\nCtrl + Shift + 加号所在键：切换置顶\n\nCtrl + Alt + Shift + 1～9：后台调节全部 MuMu\nCtrl + Alt + Shift + 0：全部 MuMu 恢复不透明\n\n使用主键盘数字键。请先退出原版 Vitrite。\n右键托盘图标可恢复并退出本程序。", "virtrite 2");
    }
    private void TryAction(Action action)
    {
        try { action(); }
        catch (Exception error)
        {
            string explanation = Log.Explain(error);
            Log.Write("ERROR: " + explanation);
            if ((DateTime.UtcNow - lastError).TotalSeconds >= 5)
            {
                lastError = DateTime.UtcNow;
                icon.ShowBalloonTip(4000, "virtrite 2：无法更改该窗口", explanation, ToolTipIcon.Warning);
            }
        }
    }
    private void Apply(IntPtr window, int level)
    {
        IntPtr actual = WindowActions.SetOpacity(window, level);
        touched[actual] = MuMuWindows.Owner(actual);
        if (MuMuWindows.IsMuMu(actual)) RememberMuMu(actual, level);
        Log.Write("Opacity hwnd=" + actual.ToInt64().ToString("X") + " alpha=" + WindowActions.Alpha(level));
    }
    private MuMuPreference RememberMuMu(IntPtr window, int level)
    {
        uint owner = MuMuWindows.Owner(window);
        using (Process process = Process.GetProcessById((int)owner))
        {
            MuMuPreference preference = new MuMuPreference { Level = level, ProcessStarted = process.StartTime.ToUniversalTime().Ticks };
            mumuPreferences[owner] = preference;
            return preference;
        }
    }
    private void KeepMuMuOpacity()
    {
        if (mumuPreferences.Count == 0 && !allMuMuLevel.HasValue) return;
        foreach (IntPtr window in MuMuWindows.Roots())
        {
            if (Native.IsIconic(window)) continue;
            uint owner = MuMuWindows.Owner(window);
            MuMuPreference preference;
            if (mumuPreferences.TryGetValue(owner, out preference))
            {
                try
                {
                    using (Process process = Process.GetProcessById((int)owner))
                    {
                        if (process.StartTime.ToUniversalTime().Ticks != preference.ProcessStarted)
                        {
                            mumuPreferences.Remove(owner);
                            preference = null;
                        }
                    }
                }
                catch { continue; }
            }
            if (preference == null)
            {
                if (!allMuMuLevel.HasValue) continue;
                preference = RememberMuMu(window, allMuMuLevel.Value);
            }
            DateTime now = DateTime.UtcNow;
            if (preference.Suspended || now < preference.RetryAfter || WindowActions.MatchesOpacity(window, WindowActions.Alpha(preference.Level))) continue;
            while (preference.RecentRepairs.Count != 0 && (now - preference.RecentRepairs.Peek()).TotalSeconds > 5) preference.RecentRepairs.Dequeue();
            if (preference.RecentRepairs.Count >= 5)
            {
                preference.Suspended = true;
                TryAction(delegate { throw new Exception("MuMu 持续重置透明度，已暂停自动恢复以避免闪屏。再次使用透明化快捷键可重试。"); });
                continue;
            }
            try
            {
                // Read-only checks run periodically. Write through Qt only when the
                // actual value drifted (e.g. after MuMu's boss key restored it).
                QtBridge.SetOpacity(window, WindowActions.Alpha(preference.Level));
                touched[window] = owner;
                preference.RecentRepairs.Enqueue(now);
                Log.Write("Restored MuMu opacity after reset hwnd=" + window.ToInt64().ToString("X") + " alpha=" + WindowActions.Alpha(preference.Level));
            }
            catch (Exception error)
            {
                preference.RetryAfter = now.AddSeconds(5);
                TryAction(delegate { throw error; });
            }
        }
    }
    private void SetAllMuMu(int level)
    {
        WindowActions.Alpha(level);
        allMuMuLevel = level == 0 ? (int?)null : level;
        List<IntPtr> roots = MuMuWindows.Roots();
        foreach (IntPtr window in roots) TryAction(delegate { Apply(window, level); });
        if (roots.Count == 0) Log.Write("No visible MuMuPlayer window; waiting for it to open.");
    }
    private void RestoreAll()
    {
        allMuMuLevel = null;
        mumuPreferences.Clear();
        foreach (KeyValuePair<IntPtr, uint> item in new Dictionary<IntPtr, uint>(touched))
            if (Native.IsWindow(item.Key) && MuMuWindows.Owner(item.Key) == item.Value)
                TryAction(delegate { WindowActions.SetOpacity(item.Key, 0); });
        // Also catches a MuMu handle recreated since the previous command.
        foreach (IntPtr window in MuMuWindows.Roots()) TryAction(delegate { WindowActions.SetOpacity(window, 0); });
        touched.Clear();
    }
    private void OnCommand(int command, int value)
    {
        if (command == 1 && value >= 0 && value <= 9) TryAction(delegate { SetAllMuMu(value); });
        if (command == 2) RestoreAll();
        if (command == 3) dispatch.BeginInvoke((MethodInvoker)delegate { ExitThread(); });
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
                    uint owner = MuMuWindows.Owner(window);
                    if (action >= 100 || (window != IntPtr.Zero && owner != (uint)Process.GetCurrentProcess().Id))
                    {
                        dispatch.BeginInvoke((MethodInvoker)delegate
                        {
                            if (action < 100 && (!Native.IsWindow(window) || MuMuWindows.Owner(window) != owner)) return;
                            TryAction(delegate
                            {
                                if (action >= 100) SetAllMuMu(action - 100);
                                else if (action == -1) WindowActions.ToggleTopmost(window);
                                else Apply(window, action);
                            });
                        });
                    }
                }
            }
        }
        return Native.CallNextHookEx(hook, code, message, data);
    }
    protected override void ExitThreadCore()
    {
        timer.Stop();
        if (hook != IntPtr.Zero) { Native.UnhookWindowsHookEx(hook); hook = IntPtr.Zero; }
        RestoreAll();
        QtBridge.ReleaseAll();
        commands.Dispose();
        icon.Visible = false;
        icon.Dispose();
        menu.Dispose();
        timer.Dispose();
        dispatch.Dispose();
        Log.Write("Restored opacity to 100%; stopped.");
        base.ExitThreadCore();
    }
}

internal static class Program
{
    private static void Require(bool condition, string message) { if (!condition) throw new Exception(message); }
    private static void SelfTest(string report)
    {
        List<string> passed = new List<string>();
        ShortcutState keys = new ShortcutState();
        Require(keys.Feed(0x30, true) == -2, "Bare zero");
        keys.Feed(0x30, false);
        keys.Feed(0xA2, true); keys.Feed(0xA1, true);
        for (int i = 0; i <= 9; i++)
        {
            Require(keys.Feed(0x30 + i, true) == i, "Ctrl+Shift+" + i);
            Require(keys.Feed(0x30 + i, true) == -2, "Repeated key");
            keys.Feed(0x30 + i, false);
        }
        Require(keys.Feed(0xBB, true) == -1, "Topmost shortcut"); keys.Feed(0xBB, false);
        keys.Feed(0xA1, false); keys.Feed(0xA4, true);
        Require(keys.Feed(0x30, true) == 0, "Ctrl+Alt+0 fallback"); keys.Feed(0x30, false);
        keys.Feed(0xA1, true);
        Require(keys.Feed(0x35, true) == 105, "Background MuMu hotkey"); keys.Feed(0x35, false);
        keys.Feed(0x5B, true);
        Require(keys.Feed(0x35, true) == -2, "Windows key ignored");
        passed.Add("PASS: all hotkeys, fallback, repeat filtering and MuMu shortcuts.");
        int receivedCommand = 0, receivedValue = 0;
        string testCaption = CommandWindow.Caption + ".SelfTest." + Process.GetCurrentProcess().Id;
        using (CommandWindow receiver = new CommandWindow(delegate(int command, int value) { receivedCommand = command; receivedValue = value; }, testCaption))
        {
            IntPtr target = Native.FindWindowEx(new IntPtr(-3), IntPtr.Zero, null, testCaption);
            Require(target == receiver.Handle, "Find background command receiver");
            UIntPtr result;
            Require(Native.SendMessageTimeout(target, CommandWindow.MessageId, new UIntPtr(1), new IntPtr(5), 2, 1000, out result) != IntPtr.Zero && result.ToUInt64() == 1, "Background command delivered");
            Require(receivedCommand == 1 && receivedValue == 5, "Background command arguments");
        }
        passed.Add("PASS: hidden command window lookup and command delivery.");
        using (Form window = new Form())
        {
            IntPtr handle = window.Handle; // Never shown or activated.
            WindowActions.SetOpacity(handle, 0);
            for (int level = 1; level <= 9; level++)
            {
                WindowActions.SetOpacity(handle, level);
                uint color, flags; byte alpha;
                Require(Native.GetLayeredWindowAttributes(handle, out color, out alpha, out flags) && alpha == WindowActions.Alpha(level), "Opacity level " + level);
                WindowActions.SetOpacity(handle, 0);
                Require(Native.GetLayeredWindowAttributes(handle, out color, out alpha, out flags) && alpha == 255 && (flags & 2) != 0, "Restore alpha=255");
                Require((Native.GetWindowLongPtr(handle, -20).ToInt64() & Native.Layered) != 0, "Keep layered style");
            }
            Native.SetLayeredWindowAttributes(handle, 0x010203, 90, 3);
            WindowActions.SetOpacity(handle, 0);
            uint restoredColor, restoredFlags; byte restoredAlpha;
            Require(Native.GetLayeredWindowAttributes(handle, out restoredColor, out restoredAlpha, out restoredFlags) && restoredAlpha == 255 && restoredColor == 0x010203 && restoredFlags == 3, "Preserve window color key");
        }
        passed.Add("PASS: native opacity 10%-90% -> alpha 255, layered style and color key; no visible test window. Native topmost is not asserted on an invisible window.");
        File.WriteAllLines(report, passed.ToArray());
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
            int command = 0, value = 0;
            int? initial = null;
            if (args.Length == 2 && args[0] == "--mumu-level")
            {
                value = int.Parse(args[1]); WindowActions.Alpha(value); command = 1; initial = value;
            }
            else if (args.Length == 1 && args[0] == "--restore-all") command = 2;
            else if (args.Length == 1 && args[0] == "--quit") command = 3;
            else if (args.Length != 0) throw new Exception("参数无效。");
            bool created;
            using (Mutex instance = new Mutex(true, "Local\\virtrite2.20261030", out created))
            {
                if (!created)
                {
                    if (command == 0) return 0;
                    IntPtr receiver = Native.FindWindowEx(new IntPtr(-3), IntPtr.Zero, null, CommandWindow.Caption);
                    if (receiver == IntPtr.Zero) throw new Exception("程序正在启动，请稍后重试。");
                    UIntPtr result;
                    if (Native.SendMessageTimeout(receiver, CommandWindow.MessageId, new UIntPtr((uint)command), new IntPtr(value), 2, 10000, out result) == IntPtr.Zero || result.ToUInt64() != 1)
                        throw new Exception("后台程序未响应，请稍后重试。");
                    return 0;
                }
                if (command == 2 || command == 3)
                {
                    foreach (IntPtr window in MuMuWindows.Roots()) WindowActions.SetOpacity(window, 0);
                    return 0;
                }
                if (Process.GetProcessesByName("Vitrite").Length != 0 || Process.GetProcessesByName("Vitrite Fixed").Length != 0)
                {
                    Log.Write("ERROR: 请先手动退出旧版 Vitrite / Vitrite Fixed，避免快捷键互相覆盖，再启动 virtrite 2。");
                    return 2;
                }
                using (TrayContext context = new TrayContext(initial)) Application.Run(context);
                instance.ReleaseMutex();
            }
            return 0;
        }
        catch (Exception error) { Log.Write("ERROR: " + Log.Explain(error)); return 1; }
        finally { QtBridge.ReleaseAll(); }
    }
}
