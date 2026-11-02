using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
public static class TestQtBridge {
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern IntPtr LoadLibrary(string path);
 [DllImport("kernel32.dll",CharSet=CharSet.Ansi,SetLastError=true)] public static extern IntPtr GetProcAddress(IntPtr m,string n);
 [DllImport("kernel32.dll")] public static extern bool FreeLibrary(IntPtr m);
 [DllImport("user32.dll",SetLastError=true)] public static extern IntPtr SetWindowsHookEx(int id,IntPtr proc,IntPtr module,uint tid);
 [DllImport("user32.dll")] public static extern bool UnhookWindowsHookEx(IntPtr hook);
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,out uint p);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern uint RegisterWindowMessage(string s);
 [DllImport("user32.dll",SetLastError=true)] public static extern IntPtr SendMessageTimeout(IntPtr h,uint msg,UIntPtr w,IntPtr l,uint flags,uint timeout,out UIntPtr result);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern IntPtr GetProp(IntPtr h,string s);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern IntPtr RemoveProp(IntPtr h,string s);
 public static string Apply(string path,long handle,byte alpha) {
  IntPtr h=new IntPtr(handle); uint pid; uint tid=GetWindowThreadProcessId(h,out pid);
  IntPtr lib=LoadLibrary(path);if(lib==IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error());
  IntPtr hook=IntPtr.Zero;
  try {
   IntPtr proc=GetProcAddress(lib,"MuMuOpacityHook"); if(proc==IntPtr.Zero) throw new Exception("Missing export");
   hook=SetWindowsHookEx(4,proc,lib,tid);if(hook==IntPtr.Zero)throw new Win32Exception(Marshal.GetLastWin32Error());
   uint msg=RegisterWindowMessage("Codex.MuMuOpacity.QtBridge.Apply.20261030");
   RemoveProp(h,"Codex.MuMuOpacity.QtBridge.Status.20261030"); UIntPtr result;
   if(SendMessageTimeout(h,msg,new UIntPtr(0x4D550000u|alpha),IntPtr.Zero,2,2000,out result)==IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error());
   long status=GetProp(h,"Codex.MuMuOpacity.QtBridge.Status.20261030").ToInt64(); RemoveProp(h,"Codex.MuMuOpacity.QtBridge.Status.20261030");
   return "Qt bridge status="+status+" hwnd="+handle.ToString("X")+" alpha="+alpha;
  } finally { if(hook!=IntPtr.Zero) UnhookWindowsHookEx(hook); FreeLibrary(lib); }
 }
}
