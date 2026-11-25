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
[assembly: System.Reflection.AssemblyFileVersion("2.0.4.0")]

internal static class Native
{
    internal const long Layered = 0x80000;
    internal delegate bool EnumCallback(IntPtr window, IntPtr data);
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
    [DllImport("user32.dll", SetLastError = true)] internal static extern IntPtr SetWindowsHookEx(int type, IntPtr callback, IntPtr module, uint thread);
    [DllImport("user32.dll")] internal static extern bool UnhookWindowsHookEx(IntPtr hook);
    [DllImport("user32.dll", SetLastError = true)] internal static extern bool RegisterHotKey(IntPtr window, int id, uint modifiers, uint key);
    [DllImport("user32.dll", SetLastError = true)] internal static extern bool UnregisterHotKey(IntPtr window, int id);
    [DllImport("user32.dll", SetLastError = true)] internal static extern bool PostMessage(IntPtr window, uint message, IntPtr wParam, IntPtr lParam);
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

internal sealed class HotkeyListener : NativeWindow, IDisposable
{
    internal const int HotkeyMessage = 0x312;
    private const int PowerBroadcast = 0x218;
    private const int ResumeAutomatic = 0x12, ResumeInteractive = 0x07, ResumeCritical = 0x06;
    private const uint StopMessage = 0x8062;
    private const uint Alt = 1, Control = 2, Shift = 4, NoRepeat = 0x4000;
    internal sealed class Binding
    {
        internal readonly uint Modifiers, Key;
        internal readonly int Action;
        internal readonly string Label;

        internal Binding(uint modifiers, uint key, int action, string label)
        {
            Modifiers = modifiers;
            Key = key;
            Action = action;
            Label = label;
        }
    }

    internal static List<Binding> DefaultBindings()
    {
        List<Binding> result = new List<Binding>();
        for (uint digit = 0; digit <= 9; digit++)
            result.Add(new Binding(Control | Shift, 0x30 + digit, (int)digit, "Ctrl+Shift+" + digit));
        result.Add(new Binding(Control | Shift, 0xBB, -1, "Ctrl+Shift+加号"));
        result.Add(new Binding(Control | Alt, 0x30, 0, "Ctrl+Alt+0"));
        for (uint digit = 0; digit <= 9; digit++)
            result.Add(new Binding(Control | Alt | Shift, 0x30 + digit, 100 + (int)digit, "Ctrl+Alt+Shift+" + digit));
        return result;
    }

    private readonly IList<Binding> bindings;
    private readonly bool[] registered;
    private readonly Action<int> shortcut;
    private readonly Action resumed;
    private readonly Thread worker;
    private readonly ManualResetEvent ready = new ManualResetEvent(false);
    private Exception startupError;
    internal string MissingShortcuts { get; private set; }
    internal int RegisteredCount { get; private set; }

    internal HotkeyListener(IList<Binding> bindings, Action<int> shortcut, Action resumed)
    {
        this.bindings = bindings;
        registered = new bool[bindings.Count];
        this.shortcut = shortcut;
        this.resumed = resumed;
        worker = new Thread(Run) { IsBackground = true, Name = "virtrite 2 hotkeys" };
        worker.SetApartmentState(ApartmentState.STA);
        worker.Start();
        ready.WaitOne();
        ready.Dispose();
        if (startupError != null) throw new InvalidOperationException("无法启动快捷键。", startupError);
    }

    private void Run()
    {
        try
        {
            // A hidden top-level window receives system broadcasts. Message-only windows do not.
            CreateHandle(new CreateParams { Caption = "virtrite 2.PowerNotifications", Style = unchecked((int)0x80000000) });
            RegisterMissing();
        }
        catch (Exception error) { startupError = error; }
        finally { ready.Set(); }
        try { if (startupError == null) Application.Run(); }
        finally
        {
            for (int id = 0; id < registered.Length; id++)
                if (registered[id]) Native.UnregisterHotKey(Handle, id);
            if (Handle != IntPtr.Zero) DestroyHandle();
        }
    }

    private void RegisterMissing()
    {
        List<string> missing = new List<string>();
        for (int id = 0; id < bindings.Count; id++)
        {
            if (registered[id]) continue;
            Binding binding = bindings[id];
            if (Native.RegisterHotKey(Handle, id, binding.Modifiers | NoRepeat, binding.Key))
            {
                registered[id] = true;
                RegisteredCount++;
            }
            else missing.Add(binding.Label + " (" + Marshal.GetLastWin32Error() + ")");
        }
        MissingShortcuts = string.Join("、", missing.ToArray());
    }

    protected override void WndProc(ref Message message)
    {
        if (message.Msg == PowerBroadcast)
        {
            int state = message.WParam.ToInt32();
            if (state == ResumeAutomatic || state == ResumeInteractive || state == ResumeCritical)
            {
                RegisterMissing();
                resumed();
            }
            message.Result = new IntPtr(1);
            return;
        }
        if (message.Msg == HotkeyMessage)
        {
            int id = message.WParam.ToInt32();
            if (id >= 0 && id < registered.Length && registered[id]) shortcut(bindings[id].Action);
            return;
        }
        if (message.Msg == StopMessage) { Application.ExitThread(); return; }
        base.WndProc(ref message);
    }

    public void Dispose()
    {
        if (worker.IsAlive && Native.PostMessage(Handle, StopMessage, IntPtr.Zero, IntPtr.Zero))
            worker.Join(2000);
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
    private readonly Dictionary<IntPtr, uint> touched = new Dictionary<IntPtr, uint>();
    private readonly Dictionary<uint, MuMuPreference> mumuPreferences = new Dictionary<uint, MuMuPreference>();
    private readonly System.Windows.Forms.Timer timer = new System.Windows.Forms.Timer();
    private readonly HotkeyListener keyboard;
    private readonly CommandWindow commands;
    private readonly uint ownProcess = (uint)Process.GetCurrentProcess().Id;
    private int? allMuMuLevel;
    private DateTime lastError = DateTime.MinValue;

    internal TrayContext(int? initialMuMuLevel)
    {
        IntPtr ignored = dispatch.Handle;
        keyboard = new HotkeyListener(HotkeyListener.DefaultBindings(), QueueShortcut, delegate { OnUiThread(ResumeMuMuOpacity); });
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
        Log.Write("Started. Windows global hotkeys registered: " + keyboard.RegisteredCount + "/22.");
        if (keyboard.MissingShortcuts.Length != 0)
        {
            Log.Write("Hotkey registration failed: " + keyboard.MissingShortcuts);
            icon.ShowBalloonTip(5000, "virtrite 2", "以下快捷键未能注册：" + keyboard.MissingShortcuts, ToolTipIcon.Warning);
        }
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
    private void ResumeMuMuOpacity()
    {
        Log.Write("Resume: Windows global hotkeys registered: " + keyboard.RegisteredCount + "/22. " + keyboard.MissingShortcuts);
        DateTime retryAfter = DateTime.UtcNow.AddSeconds(1);
        foreach (MuMuPreference preference in mumuPreferences.Values)
        {
            preference.RetryAfter = retryAfter;
            preference.Suspended = false;
            preference.RecentRepairs.Clear();
        }
    }
    private void OnUiThread(MethodInvoker action)
    {
        try { dispatch.BeginInvoke(action); }
        catch (InvalidOperationException) { } // The UI may already be closing.
    }
    private void QueueShortcut(int action)
    {
        IntPtr window = Native.GetForegroundWindow();
        uint owner = MuMuWindows.Owner(window);
        OnUiThread(delegate
        {
            if (action < 100 && (window == IntPtr.Zero || owner == ownProcess || !Native.IsWindow(window) || MuMuWindows.Owner(window) != owner))
            {
                Log.Write("Hotkey received, but no eligible foreground window. action=" + action);
                return;
            }
            TryAction(delegate
            {
                if (action >= 100) SetAllMuMu(action - 100);
                else if (action == -1) WindowActions.ToggleTopmost(window);
                else Apply(window, action);
            });
        });
    }
    protected override void ExitThreadCore()
    {
        timer.Stop();
        keyboard.Dispose();
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
    [DllImport("user32.dll")] private static extern void keybd_event(byte key, byte scan, uint flags, UIntPtr extra);

    private static void Require(bool condition, string message) { if (!condition) throw new Exception(message); }
    private static void SelfTest(string report)
    {
        List<string> passed = new List<string>();
        List<HotkeyListener.Binding> defaults = HotkeyListener.DefaultBindings();
        Require(defaults.Count == 22 && defaults[0].Action == 0 && defaults[11].Action == 0 && defaults[21].Action == 109, "Retain default shortcut actions");
        const byte testKey = 0x87; // F24 is used only by the test and changes no windows.
        int receivedAction = -100;
        using (AutoResetEvent triggered = new AutoResetEvent(false))
        using (AutoResetEvent recovered = new AutoResetEvent(false))
        using (HotkeyListener listener = new HotkeyListener(new[] { new HotkeyListener.Binding(0, testKey, 5, "F24") },
            delegate(int action) { receivedAction = action; triggered.Set(); }, delegate { recovered.Set(); }))
        {
            Require(listener.RegisteredCount == 1, "Register test hotkey: " + listener.MissingShortcuts);
            UIntPtr result;
            for (int i = 0; i < 3; i++)
            {
                if (i > 0)
                {
                    Require(Native.SendMessageTimeout(listener.Handle, 0x218, new UIntPtr(0x12), IntPtr.Zero, 2, 3000, out result) != IntPtr.Zero && result.ToUInt64() == 1, "Resume message accepted");
                    Require(recovered.WaitOne(3000), "Received resume callback");
                }
                keybd_event(testKey, 0, 0, UIntPtr.Zero);
                keybd_event(testKey, 0, 2, UIntPtr.Zero);
                Require(triggered.WaitOne(3000) && receivedAction == 5, "Windows delivered registered shortcut on attempt " + i);
            }
        }
        passed.Add("PASS: Windows delivered registered hotkey before and after two simulated resume notifications.");
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
