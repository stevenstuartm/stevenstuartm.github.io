---
title: "C# Span, Memory, and High-Performance Patterns"
layout: guide
category: ".NET & C#"
subcategory: "Collections & Data"
description: "Zero-allocation programming with Span<T>, Memory<T>, ArrayPool, and performance optimization techniques."
tags: [c-sharp, dotnet, performance, span, memory, optimization, advanced]
---

<blockquote class="pull-quote">
<p>In high-throughput scenarios, allocation is the enemy. A string.Substring() that allocates on every call can generate gigabytes of garbage per minute. Span eliminates this entirely by providing zero-allocation views into existing memory.</p>
</blockquote>

## Why Span and Memory

```csharp
// Traditional - allocates new string
string text = "Hello, World!";
string world = text.Substring(7, 5);  // Allocates new string

// Span - no allocation
ReadOnlySpan<char> span = text.AsSpan();
ReadOnlySpan<char> worldSpan = span.Slice(7, 5);  // Just a view
```

## Span<T>

A stack-only view into contiguous memory. Cannot be stored on the heap (in fields, captured in lambdas, or used in async methods).

### Creating Spans

```csharp
// From array
int[] array = { 1, 2, 3, 4, 5 };
Span<int> span = array;
Span<int> slice = array.AsSpan(1, 3);  // [2, 3, 4]

// From string (read-only)
string text = "Hello";
ReadOnlySpan<char> chars = text.AsSpan();

// Stack allocation
Span<int> stackSpan = stackalloc int[10];

// From pointer (unsafe)
unsafe
{
    int* ptr = stackalloc int[10];
    Span<int> fromPtr = new Span<int>(ptr, 10);
}
```

### Span Operations

```csharp
Span<int> span = new int[] { 1, 2, 3, 4, 5 };

// Access and modify
span[0] = 10;
ref int first = ref span[0];  // Get reference

// Slice (no allocation)
Span<int> middle = span[1..4];  // [2, 3, 4]
Span<int> last = span[^2..];    // [4, 5]

// Fill
span.Fill(0);  // All zeros

// Clear
span.Clear();  // All default

// Copy
Span<int> dest = new int[5];
span.CopyTo(dest);
bool copied = span.TryCopyTo(dest);

// Reverse
span.Reverse();

// Sort (requires System.MemoryExtensions)
span.Sort();

// Search
int index = span.IndexOf(3);
bool contains = span.Contains(3);

// Comparison
bool equal = span.SequenceEqual(other);
```

### Iterating Spans

```csharp
Span<int> span = new int[] { 1, 2, 3, 4, 5 };

// foreach (read-only)
foreach (var item in span)
{
    Console.WriteLine(item);
}

// foreach with ref (modify in place)
foreach (ref int item in span)
{
    item *= 2;
}

// Index-based
for (int i = 0; i < span.Length; i++)
{
    span[i] = i * 10;
}
```

## ReadOnlySpan<T>

Immutable view - can read but not modify.

```csharp
// String is always ReadOnlySpan
ReadOnlySpan<char> text = "Hello".AsSpan();

// Convert writable to read-only
Span<int> writable = new int[] { 1, 2, 3 };
ReadOnlySpan<int> readOnly = writable;

// Methods accepting ReadOnlySpan can take Span
void ProcessData(ReadOnlySpan<int> data) { }
ProcessData(writable);  // Implicit conversion
```

## Memory<T>

Like Span but can be stored on the heap. Use when you need to:
- Store the reference in a field
- Use in async methods
- Capture in lambdas

```csharp
public class DataBuffer
{
    private Memory<byte> buffer;  // Can be a field

    public DataBuffer(int size)
    {
        buffer = new byte[size];
    }

    // Can be used in async
    public async Task ProcessAsync()
    {
        Memory<byte> slice = buffer.Slice(0, 100);
        await ProcessSliceAsync(slice);
    }

    public void Process()
    {
        // Convert to Span when actually processing
        Span<byte> span = buffer.Span;
        ProcessSpan(span);
    }
}
```

### Memory vs Span

| Feature | Span<T> | Memory<T> |
|---------|---------|-----------|
| Stack allocation | Yes | No |
| Can be field | No | Yes |
| In async methods | No | Yes |
| In lambdas | No | Yes |
| Performance | Fastest | Slightly slower |
| Use case | Local processing | Storage, async |

```csharp
// Convert Memory to Span for processing
Memory<int> memory = new int[100];
Span<int> span = memory.Span;  // For actual operations
```

## ArrayPool<T>

Rent arrays from a shared pool to avoid allocations.

```csharp
// Rent an array
byte[] buffer = ArrayPool<byte>.Shared.Rent(minimumLength: 1024);
try
{
    // Use buffer...
    // Note: returned array may be larger than requested
    int actualLength = buffer.Length;

    ProcessData(buffer.AsSpan(0, 1024));
}
finally
{
    // Always return to pool
    ArrayPool<byte>.Shared.Return(buffer);
    // Optionally clear: ArrayPool<byte>.Shared.Return(buffer, clearArray: true);
}

// With using pattern
public ref struct RentedArray<T>
{
    private T[] array;
    private readonly int length;

    public RentedArray(int length)
    {
        array = ArrayPool<T>.Shared.Rent(length);
        this.length = length;
    }

    public Span<T> Span => array.AsSpan(0, length);

    public void Dispose()
    {
        if (array != null)
        {
            ArrayPool<T>.Shared.Return(array);
            array = null!;
        }
    }
}

// Usage
using var rented = new RentedArray<byte>(1024);
ProcessData(rented.Span);
```

### Custom Array Pool

```csharp
// Create pool with custom settings
var pool = ArrayPool<byte>.Create(
    maxArrayLength: 1024 * 1024,  // 1MB max
    maxArraysPerBucket: 50);

// Use custom pool
byte[] buffer = pool.Rent(4096);
pool.Return(buffer);
```

## MemoryPool<T>

Pool for `Memory<T>` instances.

```csharp
using IMemoryOwner<byte> owner = MemoryPool<byte>.Shared.Rent(1024);
Memory<byte> memory = owner.Memory;

// Use memory...
await ProcessAsync(memory.Slice(0, actualSize));

// Disposed automatically, returned to pool
```

## stackalloc

Allocate on the stack for small, short-lived buffers.

```csharp
// Traditional stackalloc (unsafe context required)
unsafe
{
    int* ptr = stackalloc int[10];
}

// Span-based stackalloc (no unsafe needed)
Span<int> buffer = stackalloc int[10];

// Conditional stackalloc (stack for small, heap for large)
const int StackAllocThreshold = 256;
Span<byte> buffer = length <= StackAllocThreshold
    ? stackalloc byte[length]
    : new byte[length];

// Pattern for parsing
public static int ParseNumbers(ReadOnlySpan<char> input)
{
    Span<int> numbers = input.Length <= 128
        ? stackalloc int[input.Length]
        : new int[input.Length];

    // Parse into buffer...
    return numbers.Length;
}
```

## Inline Arrays (C# 12)

Inline arrays provide fixed-size buffers without unsafe code, combining the performance of fixed buffers with type safety.

```csharp
// Define an inline array type
[System.Runtime.CompilerServices.InlineArray(10)]
public struct Buffer10<T>
{
    private T _element0;  // Only declare first element
}

// Usage
var buffer = new Buffer10<int>();
buffer[0] = 1;
buffer[9] = 10;

// Iterate
foreach (var item in buffer)
{
    Console.WriteLine(item);
}

// Convert to Span for processing
Span<int> span = buffer;
span.Fill(42);

// Practical example: fixed-size lookup table
[InlineArray(256)]
public struct CharLookup
{
    private byte _element0;
}

public class FastCharClassifier
{
    private CharLookup lookup;

    public FastCharClassifier()
    {
        Span<byte> span = lookup;
        for (int i = 'a'; i <= 'z'; i++) span[i] = 1;  // Letters
        for (int i = 'A'; i <= 'Z'; i++) span[i] = 1;
        for (int i = '0'; i <= '9'; i++) span[i] = 2;  // Digits
    }

    public bool IsAlphanumeric(char c) => c < 256 && lookup[c] > 0;
}
```

Inline arrays are useful for performance-critical code that needs fixed-size buffers embedded directly in structs without heap allocation.

## High-Performance Patterns

### Zero-Copy Parsing

```csharp
public static (int Key, int Value) ParseKeyValue(ReadOnlySpan<char> line)
{
    int colonIndex = line.IndexOf(':');
    if (colonIndex < 0)
        throw new FormatException();

    // No allocations - just views into original string
    ReadOnlySpan<char> keySpan = line[..colonIndex].Trim();
    ReadOnlySpan<char> valueSpan = line[(colonIndex + 1)..].Trim();

    int key = int.Parse(keySpan);
    int value = int.Parse(valueSpan);

    return (key, value);
}

// Usage
string line = "42: 100";
var (key, value) = ParseKeyValue(line);
```

### Efficient String Building

```csharp
public static string FormatData(int id, string name, decimal amount)
{
    // Calculate exact length
    int length = 10 + name.Length + 20;  // Approximate

    return string.Create(length, (id, name, amount), (chars, state) =>
    {
        int pos = 0;

        // Write ID
        "ID: ".AsSpan().CopyTo(chars);
        pos += 4;
        state.id.TryFormat(chars[pos..], out int written);
        pos += written;

        // Write separator
        ", ".AsSpan().CopyTo(chars[pos..]);
        pos += 2;

        // Write name
        state.name.AsSpan().CopyTo(chars[pos..]);
        pos += state.name.Length;

        // Write amount
        ", $".AsSpan().CopyTo(chars[pos..]);
        pos += 3;
        state.amount.TryFormat(chars[pos..], out written, "F2");
    });
}
```

### Buffer-Based Processing

```csharp
public async Task ProcessLargeFileAsync(string path)
{
    const int BufferSize = 4096;
    byte[] buffer = ArrayPool<byte>.Shared.Rent(BufferSize);

    try
    {
        await using var stream = File.OpenRead(path);
        int bytesRead;

        while ((bytesRead = await stream.ReadAsync(buffer.AsMemory(0, BufferSize))) > 0)
        {
            ProcessChunk(buffer.AsSpan(0, bytesRead));
        }
    }
    finally
    {
        ArrayPool<byte>.Shared.Return(buffer);
    }
}
```

### Ref Structs

Create stack-only types that can contain Span.

```csharp
public ref struct SpanReader
{
    private ReadOnlySpan<char> remaining;

    public SpanReader(ReadOnlySpan<char> text)
    {
        remaining = text;
    }

    public ReadOnlySpan<char> ReadLine()
    {
        int newline = remaining.IndexOf('\n');
        if (newline < 0)
        {
            var line = remaining;
            remaining = default;
            return line;
        }

        var result = remaining[..newline];
        remaining = remaining[(newline + 1)..];
        return result;
    }

    public bool HasMore => !remaining.IsEmpty;
}

// Usage
var reader = new SpanReader("line1\nline2\nline3");
while (reader.HasMore)
{
    var line = reader.ReadLine();
    ProcessLine(line);
}
```

## IMemoryOwner and Memory Management

```csharp
public class BufferManager : IDisposable
{
    private readonly List<IMemoryOwner<byte>> rentedBuffers = new();

    public Memory<byte> GetBuffer(int size)
    {
        var owner = MemoryPool<byte>.Shared.Rent(size);
        rentedBuffers.Add(owner);
        return owner.Memory[..size];
    }

    public void Dispose()
    {
        foreach (var owner in rentedBuffers)
        {
            owner.Dispose();
        }
        rentedBuffers.Clear();
    }
}
```

## Span-Based APIs

### File I/O

```csharp
// Read into span
await using var stream = File.OpenRead(path);
Memory<byte> buffer = new byte[4096];
int bytesRead = await stream.ReadAsync(buffer);
ProcessData(buffer.Span[..bytesRead]);

// Write from span
await using var output = File.Create(outputPath);
ReadOnlyMemory<byte> data = GetData();
await output.WriteAsync(data);
```

### Encoding

```csharp
// Encode to span (no allocation)
Span<byte> buffer = stackalloc byte[256];
int bytesWritten = Encoding.UTF8.GetBytes("Hello", buffer);
ReadOnlySpan<byte> encoded = buffer[..bytesWritten];

// Decode from span
ReadOnlySpan<byte> utf8 = GetUtf8Data();
Span<char> chars = stackalloc char[256];
int charsWritten = Encoding.UTF8.GetChars(utf8, chars);
```

### Numeric Formatting

```csharp
Span<char> buffer = stackalloc char[32];

// Integer formatting
int value = 12345;
value.TryFormat(buffer, out int charsWritten);
ReadOnlySpan<char> formatted = buffer[..charsWritten];

// With format specifier
decimal price = 1234.56m;
price.TryFormat(buffer, out charsWritten, "C2", CultureInfo.CurrentCulture);

// DateTime
DateTime now = DateTime.Now;
now.TryFormat(buffer, out charsWritten, "yyyy-MM-dd HH:mm:ss");
```

## Performance Comparison

```csharp
// Benchmark: Parse CSV line

// Traditional (allocates strings)
public (string Name, int Value) ParseTraditional(string line)
{
    string[] parts = line.Split(',');  // Allocates array + strings
    return (parts[0], int.Parse(parts[1]));
}

// Span-based (zero allocation)
public (string Name, int Value) ParseSpan(ReadOnlySpan<char> line)
{
    int comma = line.IndexOf(',');
    ReadOnlySpan<char> nameSpan = line[..comma];
    ReadOnlySpan<char> valueSpan = line[(comma + 1)..];

    // Only allocate the string we need to return
    return (nameSpan.ToString(), int.Parse(valueSpan));
}

// If returning Span (no allocation at all)
public void ProcessLine(ReadOnlySpan<char> line, out ReadOnlySpan<char> name, out int value)
{
    int comma = line.IndexOf(',');
    name = line[..comma];
    value = int.Parse(line[(comma + 1)..]);
}
```

## Guidelines

### When to Use Span

- Parsing strings or binary data
- Buffer manipulation
- High-frequency operations
- Avoiding substring allocations
- Stack-allocated temporary buffers

### When to Use Memory

- Storing buffer references in fields
- Async operations with buffers
- Passing buffers to callbacks
- API boundaries that need to store data

### When to Use ArrayPool

- Repeated allocation of similar-sized arrays
- Buffer reuse in I/O operations
- Reducing GC pressure in loops

### When NOT to Use

- Simple, infrequent operations
- When code clarity is more important than performance
- When the allocation cost is negligible

## Version History

| Feature | Version | Significance |
|---------|---------|--------------|
| Span<T> | C# 7.2 | Stack-only memory view |
| ReadOnlySpan<T> | C# 7.2 | Immutable span |
| Memory<T> | C# 7.2 | Heap-storable memory |
| stackalloc in expressions | C# 7.2 | Safe stack allocation |
| ref structs | C# 7.2 | Span-containing types |
| Index/Range | C# 8.0 | Slicing syntax |
| MemoryMarshal | .NET Core 2.1 | Low-level memory ops |
| Inline arrays | C# 12 | Fixed-size buffers without unsafe |

## Key Takeaways

**Span for local processing**: Use `Span<T>` when processing data within a method without storing references.

**Memory for async and storage**: Use `Memory<T>` when you need to store buffers or use them in async methods.

**ArrayPool for repeated allocations**: Rent and return arrays instead of allocating new ones repeatedly.

**stackalloc for small buffers**: Use stack allocation for small, short-lived buffers (typically < 1KB).

**Zero-copy parsing**: Parse data directly from spans without creating intermediate strings.

**Profile first**: These optimizations add complexity. Only use when profiling shows allocation is a bottleneck.
