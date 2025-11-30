---
title: "C# Types and Variables"
layout: guide
category: ".NET & C#"
subcategory: "Language Fundamentals"
description: "Understanding C#'s type system including value types, reference types, type inference, and memory behavior."
tags: [c-sharp, dotnet, fundamentals, types, memory-management, practical]
---

## The Type System

C# is a statically-typed language where every variable and expression has a type known at compile time. The type system divides into two fundamental categories: value types (stored on the stack or inline) and reference types (stored on the heap with stack-based references).

Understanding this distinction matters because it affects performance, equality semantics, and how data flows through your application.

## Value Types

Value types hold their data directly. When you assign a value type to another variable or pass it to a method, you create a copy of the data.

### Built-in Value Types

| Type | .NET Type | Size | Range |
|------|-----------|------|-------|
| `bool` | Boolean | 1 byte | true/false |
| `byte` | Byte | 1 byte | 0 to 255 |
| `sbyte` | SByte | 1 byte | -128 to 127 |
| `short` | Int16 | 2 bytes | -32,768 to 32,767 |
| `ushort` | UInt16 | 2 bytes | 0 to 65,535 |
| `int` | Int32 | 4 bytes | -2.1B to 2.1B |
| `uint` | UInt32 | 4 bytes | 0 to 4.3B |
| `long` | Int64 | 8 bytes | ±9.2 quintillion |
| `ulong` | UInt64 | 8 bytes | 0 to 18.4 quintillion |
| `float` | Single | 4 bytes | ~6-9 digits precision |
| `double` | Double | 8 bytes | ~15-17 digits precision |
| `decimal` | Decimal | 16 bytes | 28-29 digits precision |
| `char` | Char | 2 bytes | Unicode character |

**When to use each numeric type**:

```csharp
// int: General-purpose integers (loop counters, counts, IDs)
int count = 42;
int userId = 12345;

// long: Large numbers, timestamps, file sizes
long fileSize = 1_073_741_824; // 1 GB in bytes
long timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();

// double: Scientific calculations, general floating-point math
double distance = 384_400.5; // km to the moon
double velocity = 299_792.458; // km/s speed of light

// decimal: Financial calculations where precision matters
decimal price = 19.99m;
decimal taxRate = 0.0825m;
decimal total = price * (1 + taxRate); // 21.6389175m - exact
```

The `decimal` type exists specifically because `float` and `double` use binary floating-point representation, which cannot precisely represent base-10 fractions. Financial applications require exact decimal arithmetic.

```csharp
// Why decimal matters for money
double priceDouble = 0.1 + 0.2;  // 0.30000000000000004 (unexpected)
decimal priceDecimal = 0.1m + 0.2m;  // 0.3 (exact)
```

### Structs

Structs are custom value types. Use them for small, data-centric types that represent a single value or a small group of related values.

```csharp
public struct Point
{
    public double X { get; init; }
    public double Y { get; init; }

    public Point(double x, double y)
    {
        X = x;
        Y = y;
    }

    public double DistanceTo(Point other)
    {
        double dx = X - other.X;
        double dy = Y - other.Y;
        return Math.Sqrt(dx * dx + dy * dy);
    }
}

// Usage - value semantics mean copies are independent
var p1 = new Point(0, 0);
var p2 = p1; // Creates a copy
// Modifying p2 would not affect p1 (if Point were mutable)
```

**Struct guidelines**:
- Keep structs small (16 bytes or less for best performance)
- Make structs immutable when possible (use `init` or `readonly`)
- Implement `Equals` and `GetHashCode` if used in collections
- Don't inherit from structs (they're implicitly sealed)

### Enums

Enums define a set of named constants. By default, the underlying type is `int`.

```csharp
public enum OrderStatus
{
    Pending,      // 0
    Processing,   // 1
    Shipped,      // 2
    Delivered,    // 3
    Cancelled     // 4
}

// Explicit values when persistence or interop matters
public enum HttpStatusCode : short
{
    OK = 200,
    Created = 201,
    BadRequest = 400,
    NotFound = 404,
    InternalServerError = 500
}

// Flags for combinable options
[Flags]
public enum FilePermissions
{
    None = 0,
    Read = 1,
    Write = 2,
    Execute = 4,
    ReadWrite = Read | Write,
    All = Read | Write | Execute
}

// Using flags
var permissions = FilePermissions.Read | FilePermissions.Write;
bool canWrite = permissions.HasFlag(FilePermissions.Write); // true
```

## Reference Types

Reference types store a reference (memory address) to their data. Multiple variables can reference the same object.

### Classes

Classes are the primary reference type for modeling complex entities and behaviors.

```csharp
public class Customer
{
    public int Id { get; init; }
    public string Name { get; set; }
    public string Email { get; set; }

    public Customer(int id, string name)
    {
        Id = id;
        Name = name;
    }
}

// Reference semantics - both variables point to the same object
var customer1 = new Customer(1, "Alice");
var customer2 = customer1;
customer2.Name = "Bob";
Console.WriteLine(customer1.Name); // "Bob" - same object
```

### Strings

Strings are reference types but behave like value types due to immutability.

```csharp
string greeting = "Hello";
string modified = greeting + " World"; // Creates a new string
// greeting is still "Hello"

// String interning - identical literals share memory
string a = "hello";
string b = "hello";
bool same = ReferenceEquals(a, b); // true - interned

// For building strings in loops, use StringBuilder
var sb = new StringBuilder();
for (int i = 0; i < 1000; i++)
{
    sb.Append(i).Append(", ");
}
string result = sb.ToString();
```

### Arrays

Arrays are fixed-size collections of elements of the same type.

```csharp
// Array creation
int[] numbers = new int[5];           // 5 zeros
int[] primes = { 2, 3, 5, 7, 11 };    // Initialized
int[] squares = new int[] { 1, 4, 9 }; // Explicit type

// Multi-dimensional arrays
int[,] matrix = new int[3, 3];        // 3x3 grid
int[,] identity = { { 1, 0 }, { 0, 1 } };

// Jagged arrays (array of arrays)
int[][] jagged = new int[3][];
jagged[0] = new int[] { 1, 2 };
jagged[1] = new int[] { 3, 4, 5 };
```

## Type Inference with var

The `var` keyword lets the compiler infer the type from the right-hand side expression. The variable is still statically typed.

```csharp
var count = 42;                    // int
var name = "Alice";                // string
var prices = new List<decimal>();  // List<decimal>
var lookup = new Dictionary<string, int>(); // Dictionary<string, int>

// Required for anonymous types
var anon = new { Name = "Alice", Age = 30 };

// var makes complex generic types readable
var customersByCity = customers
    .GroupBy(c => c.City)
    .ToDictionary(g => g.Key, g => g.ToList());
// Type: Dictionary<string, List<Customer>>
```

**When to use var**:
- When the type is obvious from the right side (`var list = new List<string>()`)
- With LINQ queries that return complex types
- With anonymous types
- To reduce noise when the type is clear from context

**When to avoid var**:
- When the type isn't obvious (`var result = GetResult()` - what type?)
- For simple types where explicit naming aids readability

## Constants and Read-Only

### const

Compile-time constants. The value must be known at compile time and is embedded directly into the IL.

```csharp
public class MathConstants
{
    public const double Pi = 3.14159265358979;
    public const int MaxRetries = 3;
    public const string DefaultCurrency = "USD";
}

// Usage - value is substituted at compile time
double area = MathConstants.Pi * radius * radius;
```

**const limitations**:
- Only primitive types, string, and null
- Value embedded in consuming assemblies (recompilation needed if changed)
- Cannot be computed at runtime

### readonly

Runtime constants. Value set at declaration or in constructor.

```csharp
public class Configuration
{
    public readonly string ConnectionString;
    public readonly DateTime StartTime = DateTime.UtcNow;

    public Configuration(string connectionString)
    {
        ConnectionString = connectionString;
    }
}

// Static readonly for runtime-computed constants
public static class AppSettings
{
    public static readonly string MachineName = Environment.MachineName;
    public static readonly TimeSpan DefaultTimeout = TimeSpan.FromSeconds(30);
}
```

**readonly vs const**:

| Aspect | const | readonly |
|--------|-------|----------|
| Evaluation | Compile-time | Runtime |
| Types | Primitives, string, null | Any type |
| Storage | Embedded in IL | Field in memory |
| Change propagation | Requires recompilation | Automatic |
| Instance vs static | Always static | Either |

## Nullable Value Types

Value types cannot normally be null. The `?` suffix creates a nullable value type that can represent the absence of a value.

```csharp
int? maybeAge = null;
int? definitelyAge = 25;

// Checking for value
if (maybeAge.HasValue)
{
    int actualAge = maybeAge.Value;
}

// Null-coalescing operator
int displayAge = maybeAge ?? 0; // 0 if null

// Null-conditional with coalescing
int length = someString?.Length ?? 0;

// Pattern matching
if (maybeAge is int age)
{
    Console.WriteLine($"Age is {age}");
}
```

Nullable value types are implemented as `Nullable<T>` - a generic struct that wraps the underlying value type.

## Default Values

All types have a default value. For value types, it's typically zero or equivalent. For reference types, it's null.

```csharp
default(int)      // 0
default(bool)     // false
default(double)   // 0.0
default(string)   // null
default(DateTime) // DateTime.MinValue (0001-01-01)

// default literal (C# 7.1+)
int count = default;           // 0
string name = default;         // null
List<int> list = default;      // null

// Useful in generics
public T GetOrDefault<T>(string key) =>
    cache.TryGetValue(key, out T value) ? value : default;
```

## Type Conversions

### Implicit Conversions

Safe conversions that cannot lose data happen automatically.

```csharp
int i = 100;
long l = i;        // int to long - safe
double d = i;      // int to double - safe
decimal m = i;     // int to decimal - safe

// Base class assignment
object obj = "hello";  // string to object
IEnumerable<int> seq = new List<int>();  // List to interface
```

### Explicit Conversions (Casts)

Conversions that might lose data or fail require explicit casting.

```csharp
double d = 3.14;
int i = (int)d;    // 3 - truncates decimal

long l = 100;
int j = (int)l;    // Safe here, but could overflow

// Reference type casts can fail
object obj = "hello";
string s = (string)obj;  // Works
int n = (int)obj;        // InvalidCastException
```

### Safe Casting with as and is

```csharp
object obj = GetSomething();

// 'as' returns null if cast fails
string s = obj as string;
if (s != null)
{
    Console.WriteLine(s.Length);
}

// 'is' with pattern matching (preferred)
if (obj is string str)
{
    Console.WriteLine(str.Length);
}

// Negated pattern
if (obj is not string)
{
    Console.WriteLine("Not a string");
}
```

### Conversion Methods

```csharp
// Convert class - handles null and type conversions
string input = "42";
int value = Convert.ToInt32(input);
double d = Convert.ToDouble(input);

// Parse - for strings, throws on failure
int parsed = int.Parse("42");
DateTime date = DateTime.Parse("2024-01-15");

// TryParse - safe parsing, returns success bool
if (int.TryParse(userInput, out int result))
{
    Console.WriteLine($"Parsed: {result}");
}
else
{
    Console.WriteLine("Invalid input");
}

// Culture-aware parsing
decimal price = decimal.Parse("1,234.56", CultureInfo.InvariantCulture);
```

## Boxing and Unboxing

Boxing converts a value type to object (or interface it implements). Unboxing extracts the value type from the object. Both have performance costs.

```csharp
int value = 42;
object boxed = value;    // Boxing - allocates on heap
int unboxed = (int)boxed; // Unboxing - copies back to stack

// Common boxing scenarios to avoid
ArrayList oldList = new ArrayList();
oldList.Add(42);  // Boxing occurs
oldList.Add(99);  // Boxing again

// Use generic collections instead
List<int> newList = new List<int>();
newList.Add(42);  // No boxing
newList.Add(99);  // No boxing
```

## Namespaces and Using Directives

### File-Scoped Namespaces (C# 10)

Traditional namespace declarations require an extra level of indentation for all code within the file. File-scoped namespaces eliminate this nesting when a file contains only one namespace.

```csharp
// Traditional (still valid)
namespace MyApp.Services
{
    public class UserService
    {
        // Code indented inside namespace
    }
}

// File-scoped (C# 10+) - no extra indentation
namespace MyApp.Services;

public class UserService
{
    // Code at file root level
}

public class OrderService
{
    // Also in MyApp.Services namespace
}
```

File-scoped namespaces reduce visual noise and save horizontal space. Most modern C# projects use this style by default. You can enforce a project-wide preference through `.editorconfig`:

```ini
[*.cs]
csharp_style_namespace_declarations = file_scoped
```

### Global Using Directives (C# 10)

Instead of repeating common using statements in every file, global usings declare them once for the entire project.

```csharp
// In any file (commonly GlobalUsings.cs or at top of Program.cs)
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading.Tasks;

// Global using static for extension methods and static members
global using static System.Console;
global using static System.Math;

// After declaring these, all files in the project can use
// List<T>, LINQ methods, Task, and WriteLine() without imports
```

You can also declare global usings in the project file:

```xml
<ItemGroup>
  <Using Include="System.Collections.Generic" />
  <Using Include="System.Console" Static="true" />
  <Using Include="MyApp.Common" Alias="Common" />
</ItemGroup>
```

.NET 6+ projects enable **implicit usings** by default, which automatically includes common namespaces based on project type:

```xml
<PropertyGroup>
  <ImplicitUsings>enable</ImplicitUsings>
</PropertyGroup>
```

For console and class library projects, implicit usings include `System`, `System.Collections.Generic`, `System.IO`, `System.Linq`, `System.Threading.Tasks`, and others.

### Type Aliases (C# 12)

The `using` directive can create aliases for any type, including tuples, arrays, and nullable types:

```csharp
// Alias for tuple types
using Point = (int X, int Y);
using Person = (string Name, int Age);

Point origin = (0, 0);
Point target = (100, 200);
Person alice = ("Alice", 30);

// Alias for generic types
using IntList = System.Collections.Generic.List<int>;
using StringDict = System.Collections.Generic.Dictionary<string, string>;

IntList numbers = [1, 2, 3, 4, 5];
StringDict headers = new() { ["Content-Type"] = "application/json" };

// Alias for arrays and nullable types
using Matrix = int[][];
using OptionalInt = int?;

Matrix grid = [[1, 2], [3, 4]];
OptionalInt maybeValue = null;
```

Type aliases reduce repetition when working with complex generic types and provide semantic names for tuple structures that would otherwise be anonymous.

## Tuples

Tuples group multiple values without defining a formal type. C# 7.0 introduced value tuples with named elements.

```csharp
// Value tuples (C# 7.0+) - recommended
(string Name, int Age) person = ("Alice", 30);
Console.WriteLine(person.Name); // "Alice"

// Returning multiple values
public (bool Success, string Message, int Code) ValidateUser(string input)
{
    if (string.IsNullOrEmpty(input))
        return (false, "Input required", 400);
    return (true, "Valid", 200);
}

var result = ValidateUser("test");
if (result.Success)
{
    Console.WriteLine(result.Message);
}

// Deconstruction
var (success, message, _) = ValidateUser("test"); // _ discards Code

// Tuple comparison
var t1 = (1, "hello");
var t2 = (1, "hello");
bool equal = t1 == t2; // true - value comparison
```

## Version History

| Feature | Version | Significance |
|---------|---------|--------------|
| Nullable value types | C# 2.0 | Represented absence of value types |
| var keyword | C# 3.0 | Enabled LINQ and reduced verbosity |
| Value tuples | C# 7.0 | Lightweight multiple return values |
| Tuples with names | C# 7.0 | Readable tuple members |
| Default literal | C# 7.1 | Simplified default value syntax |
| Readonly structs | C# 7.2 | Guaranteed immutable value types |
| in parameter | C# 7.2 | Pass value types by reference without copying |
| Nullable reference types | C# 8.0 | Compiler warnings for null reference issues |
| Init-only setters | C# 9.0 | Immutable property initialization |
| Record types | C# 9.0 | Value semantics for reference types |
| File-scoped namespaces | C# 10 | Reduced nesting in source files |
| Global usings | C# 10 | Project-wide using directives |
| Required members | C# 11 | Enforced initialization |
| Type aliases for any type | C# 12 | Aliases for tuples, arrays, generics |
| Primary constructors | C# 12 | Simplified constructor syntax |

## Key Takeaways

**Value vs Reference**: Value types copy data; reference types share data. This affects equality comparison, parameter passing, and memory behavior.

**Choose the right numeric type**: Use `int` for general integers, `decimal` for financial calculations, and `double` for scientific computing.

**Prefer type inference when types are obvious**: `var` reduces noise but shouldn't obscure what you're working with.

**Use nullable types intentionally**: Nullable value types (`int?`) explicitly model optional values. Combined with nullable reference types (C# 8+), you can eliminate most null reference exceptions.

**Avoid boxing**: Use generic collections and methods to prevent unnecessary heap allocations from value type boxing.

**Embrace modern namespace features**: File-scoped namespaces reduce indentation noise, global usings eliminate repetitive imports, and type aliases provide semantic names for complex types like tuples.
