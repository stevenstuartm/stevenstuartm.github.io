---
title: "C# Native Interop (P/Invoke and COM)"
layout: guide
category: ".NET & C#"
subcategory: "Advanced Topics"
description: "Calling native code from C# with P/Invoke, LibraryImport, COM interop, and marshaling techniques."
tags: [c-sharp, dotnet, interop, pinvoke, com, native-code, advanced]
---

## Why Native Interop

Native interop bridges managed .NET code with unmanaged code:
- **System APIs**: Windows API, Linux syscalls, macOS frameworks
- **Legacy libraries**: Existing C/C++ libraries without managed wrappers
- **Hardware access**: Drivers, embedded devices, specialized hardware
- **Performance**: Critical algorithms in optimized native code
- **COM components**: Office automation, Windows Shell, DirectX

## P/Invoke Basics

Platform Invocation Services (P/Invoke) calls functions in native DLLs.

### Basic Declaration

```csharp
using System.Runtime.InteropServices;

public static partial class NativeMethods
{
    // Declare external function
    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool MessageBox(
        IntPtr hWnd,
        string text,
        string caption,
        uint type);

    // With explicit entry point
    [DllImport("kernel32.dll", EntryPoint = "GetCurrentThreadId")]
    public static extern uint GetThreadId();
}

// Usage
NativeMethods.MessageBox(IntPtr.Zero, "Hello", "Title", 0);
```

### DllImport Attributes

```csharp
[DllImport(
    "mylib.dll",
    EntryPoint = "native_function",     // Function name in DLL
    CallingConvention = CallingConvention.Cdecl,  // Calling convention
    CharSet = CharSet.Unicode,          // String encoding
    SetLastError = true,                // Capture GetLastError
    ExactSpelling = true,               // Don't search for A/W variants
    PreserveSig = true)]                // Keep native signature
public static extern int NativeFunction(int param);
```

### Calling Conventions

| Convention | Description | Use |
|------------|-------------|-----|
| `StdCall` | Default for Windows API | Most Windows APIs |
| `Cdecl` | C default, caller cleans stack | C libraries |
| `ThisCall` | C++ member functions | COM methods |
| `FastCall` | Registers for first args | Performance APIs |

## LibraryImport (C# 12 / .NET 7+)

Source-generated P/Invoke with better performance and AOT support.

```csharp
using System.Runtime.InteropServices;

public static partial class NativeMethods
{
    // Source generator creates marshaling code at compile time
    [LibraryImport("user32.dll", SetLastError = true, StringMarshalling = StringMarshalling.Utf16)]
    public static partial int MessageBoxW(
        IntPtr hWnd,
        [MarshalAs(UnmanagedType.LPWStr)] string text,
        [MarshalAs(UnmanagedType.LPWStr)] string caption,
        uint type);

    [LibraryImport("kernel32.dll")]
    public static partial uint GetCurrentThreadId();

    // Boolean marshaling (explicit since default differs from DllImport)
    [LibraryImport("kernel32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static partial bool CloseHandle(IntPtr handle);
}
```

### LibraryImport Benefits

- Compile-time generated marshaling (no runtime reflection)
- Native AOT compatible
- Better trimming support
- Type-safe boolean handling
- Explicit marshaling requirements

## Marshaling Types

### Primitive Types

```csharp
// Direct mapping (blittable)
int    → int      (4 bytes)
uint   → unsigned int
long   → int64_t
float  → float
double → double
IntPtr → void*
byte   → unsigned char
```

### Strings

```csharp
// Automatic marshaling
[DllImport("mylib.dll", CharSet = CharSet.Unicode)]
public static extern void ProcessString(string input);

// Explicit marshaling
[DllImport("mylib.dll")]
public static extern void ProcessAnsi(
    [MarshalAs(UnmanagedType.LPStr)] string input);    // ANSI

[DllImport("mylib.dll")]
public static extern void ProcessWide(
    [MarshalAs(UnmanagedType.LPWStr)] string input);   // UTF-16

[DllImport("mylib.dll")]
public static extern void ProcessUtf8(
    [MarshalAs(UnmanagedType.LPUTF8Str)] string input); // UTF-8

// Output string
[DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
public static extern uint GetWindowsDirectory(
    StringBuilder buffer,
    uint size);
```

### Arrays

```csharp
// Array as pointer
[DllImport("mylib.dll")]
public static extern void ProcessArray(
    int[] data,
    int length);

// Fixed-size array
[DllImport("mylib.dll")]
public static extern void ProcessFixed(
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 10)]
    int[] data);

// Byte array
[DllImport("mylib.dll")]
public static extern int ReadData(
    byte[] buffer,
    int bufferSize);

// Usage
byte[] buffer = new byte[1024];
int bytesRead = NativeMethods.ReadData(buffer, buffer.Length);
```

### Structures

```csharp
// Sequential layout matches C struct
[StructLayout(LayoutKind.Sequential)]
public struct Point
{
    public int X;
    public int Y;
}

// With packing
[StructLayout(LayoutKind.Sequential, Pack = 1)]
public struct PackedData
{
    public byte A;
    public int B;   // No padding before B
}

// Explicit layout for unions
[StructLayout(LayoutKind.Explicit)]
public struct Variant
{
    [FieldOffset(0)] public int IntValue;
    [FieldOffset(0)] public float FloatValue;
    [FieldOffset(0)] public double DoubleValue;
}

// Character arrays in structs
[StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
public struct FileInfo
{
    public int Size;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 260)]
    public string FileName;
}
```

### Callbacks (Function Pointers)

```csharp
// Delegate matching native callback signature
[UnmanagedFunctionPointer(CallingConvention.StdCall)]
public delegate bool EnumWindowsProc(IntPtr hwnd, IntPtr lParam);

[DllImport("user32.dll")]
public static extern bool EnumWindows(
    EnumWindowsProc callback,
    IntPtr lParam);

// Usage
bool HandleWindow(IntPtr hwnd, IntPtr lParam)
{
    Console.WriteLine($"Window: {hwnd}");
    return true;  // Continue enumeration
}

NativeMethods.EnumWindows(HandleWindow, IntPtr.Zero);

// Modern: Function pointers (C# 9+)
[DllImport("mylib.dll")]
public static extern unsafe void RegisterCallback(
    delegate* unmanaged[Stdcall]<int, int, int> callback);
```

## SafeHandle and Resource Management

```csharp
// SafeHandle for automatic cleanup
public class SafeFileHandle : SafeHandleZeroOrMinusOneIsInvalid
{
    public SafeFileHandle() : base(ownsHandle: true) { }

    protected override bool ReleaseHandle()
    {
        return NativeMethods.CloseHandle(handle);
    }
}

[DllImport("kernel32.dll", SetLastError = true)]
public static extern SafeFileHandle CreateFile(
    string fileName,
    uint desiredAccess,
    uint shareMode,
    IntPtr securityAttributes,
    uint creationDisposition,
    uint flagsAndAttributes,
    IntPtr templateFile);

// Usage - automatically closes handle
using SafeFileHandle handle = NativeMethods.CreateFile(...);
if (handle.IsInvalid)
{
    int error = Marshal.GetLastWin32Error();
    throw new Win32Exception(error);
}
```

## Error Handling

```csharp
[DllImport("kernel32.dll", SetLastError = true)]
public static extern bool CloseHandle(IntPtr handle);

// Check error after call
bool success = NativeMethods.CloseHandle(handle);
if (!success)
{
    int errorCode = Marshal.GetLastWin32Error();
    throw new Win32Exception(errorCode);
}

// Or use ThrowExceptionForHR
[DllImport("ole32.dll")]
public static extern int CoCreateInstance(
    ref Guid rclsid,
    IntPtr pUnkOuter,
    uint dwClsContext,
    ref Guid riid,
    out IntPtr ppv);

int hr = NativeMethods.CoCreateInstance(...);
Marshal.ThrowExceptionForHR(hr);
```

## Memory Pinning

```csharp
// Pin managed memory to prevent GC movement
byte[] data = new byte[1024];

// Using fixed statement
unsafe
{
    fixed (byte* ptr = data)
    {
        NativeMethods.ProcessBuffer(ptr, data.Length);
    }
}

// Using GCHandle
GCHandle handle = GCHandle.Alloc(data, GCHandleType.Pinned);
try
{
    IntPtr ptr = handle.AddrOfPinnedObject();
    NativeMethods.ProcessBuffer(ptr, data.Length);
}
finally
{
    handle.Free();
}
```

## COM Interop

### Importing COM Types

```csharp
// Using type library importer (tlbimp)
// tlbimp Interop.Office.dll /out:Office.Interop.dll

// Or use Primary Interop Assemblies (PIAs)
// Reference Microsoft.Office.Interop.Excel

using Excel = Microsoft.Office.Interop.Excel;

var app = new Excel.Application();
app.Visible = true;
var workbook = app.Workbooks.Add();
var sheet = (Excel.Worksheet)workbook.Sheets[1];
sheet.Cells[1, 1] = "Hello from C#";
workbook.SaveAs("test.xlsx");
app.Quit();

// Clean up COM objects
Marshal.ReleaseComObject(sheet);
Marshal.ReleaseComObject(workbook);
Marshal.ReleaseComObject(app);
```

### Manual COM Declaration

```csharp
[ComImport]
[Guid("00000000-0000-0000-C000-000000000046")]
[InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IUnknown
{
    void QueryInterface(ref Guid riid, out IntPtr ppvObject);
    uint AddRef();
    uint Release();
}

[ComImport]
[Guid("your-interface-guid-here")]
[InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IMyComInterface
{
    void DoSomething(int value);
    int GetValue();
}

// Create instance
var guid = new Guid("your-coclass-guid");
var type = Type.GetTypeFromCLSID(guid);
var instance = (IMyComInterface)Activator.CreateInstance(type)!;
```

### COM Callable Wrapper (CCW)

Expose .NET to COM.

```csharp
[ComVisible(true)]
[Guid("your-guid-here")]
[ClassInterface(ClassInterfaceType.None)]
public class MyComClass : IMyComInterface
{
    public void DoSomething(int value)
    {
        Console.WriteLine($"Called with {value}");
    }

    public int GetValue() => 42;
}

// Register with regasm
// regasm MyAssembly.dll /codebase /tlb
```

## Native AOT Considerations

```csharp
// For Native AOT, prefer LibraryImport over DllImport
// DllImport uses runtime code generation which isn't AOT-compatible

// AOT-compatible
[LibraryImport("mylib")]
public static partial int NativeFunction(int param);

// May not work in AOT
[DllImport("mylib")]
public static extern int LegacyFunction(int param);

// Avoid dynamic COM
// Use ComWrappers instead of Activator.CreateInstance for COM
```

## Cross-Platform Native Interop

```csharp
public static class NativeMethods
{
    // Platform-specific library names
    private const string LibraryName =
#if WINDOWS
        "mylib.dll";
#elif LINUX
        "libmylib.so";
#elif MACOS
        "libmylib.dylib";
#endif

    [LibraryImport(LibraryName)]
    public static partial int NativeFunction(int param);
}

// Or use NativeLibrary for runtime resolution
public static class CrossPlatformNative
{
    private static readonly IntPtr LibHandle;

    static CrossPlatformNative()
    {
        string libName = RuntimeInformation.IsOSPlatform(OSPlatform.Windows)
            ? "mylib.dll"
            : RuntimeInformation.IsOSPlatform(OSPlatform.Linux)
                ? "libmylib.so"
                : "libmylib.dylib";

        LibHandle = NativeLibrary.Load(libName);
    }

    public static int CallFunction(int param)
    {
        var funcPtr = NativeLibrary.GetExport(LibHandle, "NativeFunction");
        var func = Marshal.GetDelegateForFunctionPointer<NativeFunctionDelegate>(funcPtr);
        return func(param);
    }

    private delegate int NativeFunctionDelegate(int param);
}
```

## Best Practices

### Do

```csharp
// Use SafeHandle for native handles
public static extern SafeFileHandle CreateFile(...);

// Set SetLastError when API uses it
[DllImport("kernel32.dll", SetLastError = true)]

// Use LibraryImport for new code
[LibraryImport("mylib")]

// Pin memory when passing pointers
fixed (byte* ptr = buffer) { ... }
```

### Don't

```csharp
// Don't ignore return values
CreateFile(...);  // Check for invalid handle!

// Don't forget to release COM objects
var app = new Excel.Application();
// ... must call Marshal.ReleaseComObject(app)

// Don't use string for output without StringBuilder
[DllImport("kernel32.dll")]
extern void GetPath(string output);  // Wrong - use StringBuilder
```

## Version History

| Feature | Version | Significance |
|---------|---------|--------------|
| P/Invoke | .NET 1.0 | Basic native interop |
| COM Interop | .NET 1.0 | COM component access |
| SafeHandle | .NET 2.0 | Reliable resource cleanup |
| Span<T> marshaling | .NET Core 2.1 | Efficient buffer passing |
| LibraryImport | .NET 7 | Source-generated P/Invoke |
| NativeLibrary | .NET Core 3.0 | Runtime library loading |
| ComWrappers | .NET 5 | AOT-compatible COM |
| Function pointers | C# 9 | Type-safe native callbacks |

## Key Takeaways

**Prefer LibraryImport**: For .NET 7+, use source-generated interop for better performance and AOT compatibility.

**Use SafeHandle**: Always wrap native handles in SafeHandle for proper cleanup.

**Check errors**: Use `SetLastError = true` and check `Marshal.GetLastWin32Error()` after calls.

**Pin when needed**: Managed memory must be pinned when passing to native code that stores pointers.

**Release COM objects**: Call `Marshal.ReleaseComObject` to release COM references promptly.

**Consider platform**: Use conditional compilation or `NativeLibrary` for cross-platform native code.
