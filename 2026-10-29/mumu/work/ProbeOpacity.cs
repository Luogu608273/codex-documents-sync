using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
public static class ProbeOpacity {
 [DllImport("user32.dll",EntryPoint="GetWindowLongPtrW",SetLastError=true)] public static extern IntPtr GetLong(IntPtr h,int i);
 [DllImport("user32.dll",EntryPoint="SetWindowLongPtrW",SetLastError=true)] public static extern IntPtr SetLong(IntPtr h,int i,IntPtr v);
 [DllImport("user32.dll",SetLastError=true)] public static extern bool SetLayeredWindowAttributes(IntPtr h,uint c,byte a,uint f);
 [DllImport("user32.dll",SetLastError=true)] public static extern bool GetLayeredWindowAttributes(IntPtr h,out uint c,out byte a,out uint f);
 [DllImport("user32.dll")] public static extern bool RedrawWindow(IntPtr h,IntPtr r,IntPtr region,uint flags);
 [DllImport("kernel32.dll")] public static extern void SetLastError(uint e);
 public static string Apply(long handle,byte alpha) {
  IntPtr h=new IntPtr(handle); long ex=GetLong(h,-20).ToInt64(); SetLastError(0);
  var old=SetLong(h,-20,new IntPtr(ex|0x80000)); int e=Marshal.GetLastWin32Error();
  if(old==IntPtr.Zero&&e!=0) throw new Win32Exception(e);
  if(!SetLayeredWindowAttributes(h,0,alpha,2)) throw new Win32Exception(Marshal.GetLastWin32Error());
  uint c,f; byte a; bool ok=GetLayeredWindowAttributes(h,out c,out a,out f);
  return String.Format("hwnd={0:X} previousEx={1:X} readback={2} alpha={3} flags={4}",handle,ex,ok,a,f);
 }
 public static string Restore(long handle,long ex) {
  IntPtr h=new IntPtr(handle); SetLastError(0); var old=SetLong(h,-20,new IntPtr(ex&~0x80000)); int e=Marshal.GetLastWin32Error();
  if(old==IntPtr.Zero&&e!=0)throw new Win32Exception(e);
  if((ex&0x80000)!=0)SetLong(h,-20,new IntPtr(ex));
  RedrawWindow(h,IntPtr.Zero,IntPtr.Zero,0x485);
  return "restored "+handle.ToString("X");
 }
}
