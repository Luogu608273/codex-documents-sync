Add-Type @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public class WindowProbe {
 public delegate bool Callback(IntPtr w,IntPtr p);
 [DllImport("user32.dll")] public static extern bool EnumWindows(Callback c,IntPtr p);
 [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr w,Callback c,IntPtr p);
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr w,out uint p);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr w,StringBuilder s,int n);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern int GetClassName(IntPtr w,StringBuilder s,int n);
 [DllImport("user32.dll")] public static extern IntPtr GetWindowLongPtrW(IntPtr w,int n);
 [DllImport("user32.dll")] public static extern IntPtr GetClassLongPtrW(IntPtr w,int n);
 [DllImport("user32.dll")] public static extern IntPtr GetWindow(IntPtr w,uint n);
 [DllImport("user32.dll")] public static extern IntPtr GetParent(IntPtr w);
 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr w);
 [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr w);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr w,out Rect r);
 [DllImport("user32.dll")] public static extern bool GetLayeredWindowAttributes(IntPtr w,out uint color,out byte alpha,out uint flags);
 public struct Rect {public int l,t,r,b;}
}
'@
$script:ids = @(Get-Process | Where-Object {$_.ProcessName -match 'mumu|nemu|vitrite'} | Select-Object -ExpandProperty Id)
$script:rows = [System.Collections.Generic.List[object]]::new()
function Read-Window([IntPtr]$w, [string]$kind) {
 [uint32]$ownerId=0
 [void][WindowProbe]::GetWindowThreadProcessId($w,[ref]$ownerId)
 if ($ownerId -notin $script:ids) {return}
 $title=[System.Text.StringBuilder]::new(512); $cls=[System.Text.StringBuilder]::new(256)
 [void][WindowProbe]::GetWindowText($w,$title,512); [void][WindowProbe]::GetClassName($w,$cls,256)
 $r=[WindowProbe+Rect]::new(); [void][WindowProbe]::GetWindowRect($w,[ref]$r)
 [uint32]$color=0; [byte]$alpha=0; [uint32]$flags=0
 $layer=[WindowProbe]::GetLayeredWindowAttributes($w,[ref]$color,[ref]$alpha,[ref]$flags)
 $script:rows.Add([pscustomobject]@{handle=$w.ToInt64();pid=$ownerId;kind=$kind;title=$title.ToString();class=$cls.ToString();visible=[WindowProbe]::IsWindowVisible($w);minimized=[WindowProbe]::IsIconic($w);parent=[WindowProbe]::GetParent($w).ToInt64();owner=[WindowProbe]::GetWindow($w,4).ToInt64();style=('{0:X}' -f [WindowProbe]::GetWindowLongPtrW($w,-16).ToInt64());ex=('{0:X}' -f [WindowProbe]::GetWindowLongPtrW($w,-20).ToInt64());cs=('{0:X}' -f [WindowProbe]::GetClassLongPtrW($w,-26).ToInt64());rect="$($r.l),$($r.t),$($r.r),$($r.b)";layer=$layer;alpha=$alpha;flags=$flags})
}
$cb=[WindowProbe+Callback]{param($w,$p) Read-Window $w 'top'; [void][WindowProbe]::EnumChildWindows($w,[WindowProbe+Callback]{param($c,$p) Read-Window $c 'child'; return $true},[IntPtr]::Zero); return $true}
[void][WindowProbe]::EnumWindows($cb,[IntPtr]::Zero)
$script:rows | ConvertTo-Json -Depth 3
