param([switch]$ValidateOnly)
$ErrorActionPreference = 'Stop'
Add-Type -TypeDefinition @"
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
public static class ScheduledSleep {
    [StructLayout(LayoutKind.Sequential)] struct LUID { public uint LowPart; public int HighPart; }
    [StructLayout(LayoutKind.Sequential)] struct TOKEN_PRIVILEGES { public uint Count; public LUID Luid; public uint Attributes; }
    [DllImport("kernel32.dll")] static extern IntPtr GetCurrentProcess();
    [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr handle);
    [DllImport("advapi32.dll", SetLastError=true)] static extern bool OpenProcessToken(IntPtr process, uint access, out IntPtr token);
    [DllImport("advapi32.dll", CharSet=CharSet.Unicode, SetLastError=true)] static extern bool LookupPrivilegeValue(string system, string name, out LUID luid);
    [DllImport("advapi32.dll", SetLastError=true)] static extern bool AdjustTokenPrivileges(IntPtr token, bool disableAll, ref TOKEN_PRIVILEGES privileges, uint length, IntPtr previous, IntPtr returnedLength);
    [DllImport("powrprof.dll", SetLastError=true)] [return:MarshalAs(UnmanagedType.U1)] static extern bool SetSuspendState([MarshalAs(UnmanagedType.U1)] bool hibernate, [MarshalAs(UnmanagedType.U1)] bool force, [MarshalAs(UnmanagedType.U1)] bool disableWake);
    public static void EnablePrivilege() {
        IntPtr token;
        if (!OpenProcessToken(GetCurrentProcess(), 0x28, out token)) throw new Win32Exception();
        try {
            LUID luid;
            if (!LookupPrivilegeValue(null, "SeShutdownPrivilege", out luid)) throw new Win32Exception();
            TOKEN_PRIVILEGES tp = new TOKEN_PRIVILEGES { Count=1, Luid=luid, Attributes=2 };
            if (!AdjustTokenPrivileges(token, false, ref tp, 0, IntPtr.Zero, IntPtr.Zero)) throw new Win32Exception();
            int error = Marshal.GetLastWin32Error();
            if (error != 0) throw new Win32Exception(error);
        } finally { CloseHandle(token); }
    }
    public static void Sleep() {
        if (!SetSuspendState(false, false, false)) throw new Win32Exception();
    }
}
"@
[ScheduledSleep]::EnablePrivilege()
if ($ValidateOnly) { Write-Output 'Compilation and sleep privilege validated; no sleep performed.'; exit 0 }
$scheduledTime = [DateTimeOffset]::Parse('2026-10-18T22:00:00+08:00')
$now = [DateTimeOffset]::Now
if ($now -lt $scheduledTime -or $now -gt $scheduledTime.AddMinutes(5)) { throw 'Outside the authorized sleep time window.' }
[ScheduledSleep]::Sleep()
