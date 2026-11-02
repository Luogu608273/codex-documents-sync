using System;
using System.Text;
using System.Diagnostics;
using System.Runtime.InteropServices;
public static class InspectWindows {
 public delegate bool Callback(IntPtr h, IntPtr l);
 [DllImport("user32.dll")] public static extern bool EnumWindows(Callback cb, IntPtr l);
 [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr h, Callback cb, IntPtr l);
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,out uint p);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h,StringBuilder s,int n);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern int GetClassName(IntPtr h,StringBuilder s,int n);
 [DllImport("user32.dll")] public static extern IntPtr GetParent(IntPtr h);
 [DllImport("user32.dll")] public static extern IntPtr GetWindow(IntPtr h,uint cmd);
 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
 [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
 [DllImport("user32.dll",EntryPoint="GetWindowLongPtrW")] public static extern IntPtr GetLong(IntPtr h,int index);
 [DllImport("user32.dll",EntryPoint="GetClassLongPtrW")] public static extern IntPtr GetClassLong(IntPtr h,int index);
 [DllImport("user32.dll")] public static extern bool GetLayeredWindowAttributes(IntPtr h,out uint color,out byte alpha,out uint flags);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out Rect r);
 [StructLayout(LayoutKind.Sequential)] public struct Rect {public int L,T,R,B;}
 public static string Describe(IntPtr h) {
  uint p,c,f; byte a; Rect r; GetWindowThreadProcessId(h,out p); GetWindowRect(h,out r);
  var t=new StringBuilder(512); var cls=new StringBuilder(256); GetWindowText(h,t,t.Capacity); GetClassName(h,cls,cls.Capacity);
  bool la=GetLayeredWindowAttributes(h,out c,out a,out f);
  return String.Format("hwnd={0:X} pid={1} parent={2:X} owner={3:X} visible={4} minimized={5} style={6:X} ex={7:X} classStyle={8:X} alpha={9} flags={10:X} rect={11},{12},{13},{14} class={15} title={16}",h.ToInt64(),p,GetParent(h).ToInt64(),GetWindow(h,4).ToInt64(),IsWindowVisible(h),IsIconic(h),GetLong(h,-16).ToInt64(),GetLong(h,-20).ToInt64(),GetClassLong(h,-26).ToInt64(),la?a.ToString():"n/a",f,r.L,r.T,r.R,r.B,cls,t);
 }
 public static string Run() {
  var s=new StringBuilder(); EnumWindows(delegate(IntPtr h,IntPtr l){uint p; GetWindowThreadProcessId(h,out p); string n="";try {n=Process.GetProcessById((int)p).ProcessName;}catch{}
   if(n.IndexOf("mumu",StringComparison.OrdinalIgnoreCase)>=0 || n.IndexOf("nemu",StringComparison.OrdinalIgnoreCase)>=0) {
    s.AppendLine(Describe(h)); EnumChildWindows(h,delegate(IntPtr ch,IntPtr x){s.AppendLine("  "+Describe(ch));return true;},IntPtr.Zero);
   } return true;},IntPtr.Zero); return s.ToString();
 }
}
