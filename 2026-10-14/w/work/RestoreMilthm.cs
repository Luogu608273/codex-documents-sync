using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Windows.Forms;

internal static class RestoreMilthm
{
    [DllImport("user32.dll", SetLastError = true)]
    private static extern int GetWindowLong(IntPtr window, int index);
    [DllImport("user32.dll", SetLastError = true)]
    private static extern bool SetLayeredWindowAttributes(IntPtr window, uint color, byte alpha, uint flags);
    [DllImport("user32.dll", SetLastError = true)]
    private static extern bool GetLayeredWindowAttributes(IntPtr window, out uint color, out byte alpha, out uint flags);
    [DllImport("user32.dll")]
    private static extern uint GetWindowThreadProcessId(IntPtr window, out uint processId);

    [STAThread]
    private static int Main()
    {
        try
        {
            Process[] processes = Process.GetProcessesByName("Milthm");
            if (processes.Length != 1)
                throw new Exception("请保持恰好一个 Milthm 正在运行，然后重试。");
            using (Process process = processes[0])
            {
                IntPtr window = process.MainWindowHandle;
                uint owner;
                GetWindowThreadProcessId(window, out owner);
                if (window == IntPtr.Zero || owner != (uint)process.Id)
                    throw new Exception("没有找到 Milthm 游戏窗口，请等待游戏启动后重试。");
                if ((GetWindowLong(window, -20) & 0x80000) == 0)
                    return 0;
                if (!SetLayeredWindowAttributes(window, 0, 255, 2))
                    throw new Exception("无法恢复窗口不透明度。Windows 错误码：" + Marshal.GetLastWin32Error());
                uint color, flags;
                byte alpha;
                if (!GetLayeredWindowAttributes(window, out color, out alpha, out flags) || alpha != 255 || (flags & 2) == 0)
                    throw new Exception("已尝试恢复，但未能核实窗口的不透明度，请重试。");
            }
            return 0;
        }
        catch (Exception error)
        {
            MessageBox.Show(error.Message, "恢复 Milthm 不透明", MessageBoxButtons.OK, MessageBoxIcon.Information);
            return 1;
        }
    }
}
