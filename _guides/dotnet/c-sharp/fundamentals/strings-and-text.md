---
title: "C# Strings and Text Processing"
layout: guide
category: ".NET & C#"
subcategory: "Language Fundamentals"
description: "String manipulation, StringBuilder, string interpolation, formatting, parsing, and high-performance text processing."
tags: [c-sharp, dotnet, fundamentals, strings, text-processing, performance, practical]
---

## String Fundamentals

<blockquote class="pull-quote">
<p>Strings are immutable, so every modification creates a new string object. Use StringBuilder for building strings in loops.</p>
</blockquote>

Strings in C# are immutable reference types. Every modification creates a new string object.

```csharp
string greeting = "Hello";
string modified = greeting + " World";  // Creates new string
// greeting is still "Hello"

// String interning - identical literals share memory
string a = "hello";
string b = "hello";
bool same = ReferenceEquals(a, b);  // true - same object

// Runtime strings not interned by default
string c = new string(new[] { 'h', 'e', 'l', 'l', 'o' });
bool notSame = ReferenceEquals(a, c);  // false
```

## String Creation

### Literals and Verbatim Strings

```csharp
// Regular string - escape sequences processed
string path = "C:\\Users\\Name\\Documents";
string newline = "Line 1\nLine 2";
string tab = "Col1\tCol2";

// Verbatim string @ - escape sequences not processed
string verbatimPath = @"C:\Users\Name\Documents";
string multiLine = @"First line
Second line
Third line";

// Double quotes in verbatim
string quoted = @"She said ""Hello""";
```

### Raw String Literals (C# 11)

```csharp
// Raw strings - preserve whitespace and quotes
string json = """
    {
        "name": "Alice",
        "age": 30
    }
    """;

// Number of quotes determines delimiter
string withQuotes = """"
    He said """Hello"""
    """";

// With interpolation
int age = 30;
string interpolated = $"""
    {
        "name": "Alice",
        "age": {age}
    }
    """;
```

### UTF-8 String Literals (C# 11)

The `u8` suffix creates UTF-8 encoded byte sequences directly, avoiding runtime encoding overhead.

```csharp
// UTF-8 literal produces ReadOnlySpan<byte>
ReadOnlySpan<byte> utf8 = "Hello"u8;

// Useful for HTTP headers, protocols, and APIs expecting UTF-8
stream.Write("Content-Type: application/json\r\n"u8);

// Convert to byte array when needed
byte[] jsonBytes = """{"name":"test"}"""u8.ToArray();

// Combine with raw strings for multi-line UTF-8
ReadOnlySpan<byte> httpResponse = """
    HTTP/1.1 200 OK
    Content-Type: text/plain

    Hello, World!
    """u8;
```

UTF-8 literals are particularly valuable in network programming, serialization, and any code that communicates with systems expecting UTF-8 encoding.

### String Interpolation

```csharp
string name = "Alice";
int age = 30;

// Basic interpolation
string message = $"Hello, {name}! You are {age} years old.";

// With formatting
decimal price = 19.99m;
string formatted = $"Price: {price:C2}";  // Price: $19.99

DateTime date = DateTime.Now;
string dateStr = $"Date: {date:yyyy-MM-dd}";

// Alignment
string aligned = $"|{name,-10}|{age,5}|";  // |Alice     |   30|

// Expressions
string expr = $"Next year: {age + 1}";
string conditional = $"Status: {(age >= 18 ? "Adult" : "Minor")}";

// Raw interpolation for JSON (C# 11)
string jsonTemplate = $$"""
    {
        "name": "{{name}}",
        "age": {{age}}
    }
    """;
```

## String Comparison

<div class="callout callout--tip">
<p class="callout__title">Choosing the Right String Comparison</p>
<ul>
<li><strong>For identifiers, paths, keys</strong>: Use <code>Ordinal</code> or <code>OrdinalIgnoreCase</code> (fastest)</li>
<li><strong>For user-facing text</strong>: Use <code>CurrentCulture</code></li>
<li><strong>For persisted data</strong>: Use <code>InvariantCulture</code></li>
</ul>
</div>

### Comparison Types

```csharp
string a = "hello";
string b = "Hello";

// Ordinal (byte-by-byte) - fastest, case-sensitive
bool ordinal = string.Equals(a, b, StringComparison.Ordinal);  // false

// OrdinalIgnoreCase - fast, case-insensitive
bool ordinalIgnore = string.Equals(a, b, StringComparison.OrdinalIgnoreCase);  // true

// CurrentCulture - culture-aware
bool culture = string.Equals(a, b, StringComparison.CurrentCulture);

// InvariantCulture - consistent across cultures
bool invariant = string.Equals(a, b, StringComparison.InvariantCultureIgnoreCase);
```

### Comparison Methods

```csharp
// Equality
bool equal = string.Equals(a, b, StringComparison.OrdinalIgnoreCase);
bool opEqual = a == b;  // Uses Ordinal

// Comparison (for sorting)
int result = string.Compare(a, b, StringComparison.OrdinalIgnoreCase);
// < 0: a before b, = 0: equal, > 0: a after b

// Contains, StartsWith, EndsWith
bool contains = a.Contains("ell", StringComparison.OrdinalIgnoreCase);
bool starts = a.StartsWith("he", StringComparison.OrdinalIgnoreCase);
bool ends = a.EndsWith("lo", StringComparison.OrdinalIgnoreCase);
```

## String Manipulation

### Basic Operations

```csharp
string text = "  Hello, World!  ";

// Case conversion
string upper = text.ToUpper();           // "  HELLO, WORLD!  "
string lower = text.ToLower();           // "  hello, world!  "
string upperInvariant = text.ToUpperInvariant();  // Culture-independent

// Trimming
string trimmed = text.Trim();            // "Hello, World!"
string trimStart = text.TrimStart();     // "Hello, World!  "
string trimEnd = text.TrimEnd();         // "  Hello, World!"
string trimChars = "###Hello###".Trim('#');  // "Hello"

// Padding
string padLeft = "42".PadLeft(5, '0');   // "00042"
string padRight = "Hi".PadRight(5);      // "Hi   "

// Substring
string sub = "Hello, World!".Substring(7, 5);  // "World"
string fromIndex = "Hello, World!"[7..];       // "World!" (range)

// Replace
string replaced = text.Replace("World", "Universe");
string charReplace = text.Replace(',', ';');
```

### Splitting and Joining

```csharp
// Split
string csv = "apple,banana,cherry";
string[] parts = csv.Split(',');  // ["apple", "banana", "cherry"]

// Split with options
string spaced = "a  b   c";
string[] noEmpty = spaced.Split(' ', StringSplitOptions.RemoveEmptyEntries);
// ["a", "b", "c"]

// Split with multiple separators
string mixed = "a,b;c|d";
string[] mixedParts = mixed.Split(new[] { ',', ';', '|' });

// Split with limit
string limited = "a,b,c,d,e".Split(',', 3);  // ["a", "b", "c,d,e"]

// Join
string joined = string.Join(", ", parts);  // "apple, banana, cherry"
string joinedArray = string.Join("-", new[] { 1, 2, 3 });  // "1-2-3"

// Concat
string concat = string.Concat("Hello", " ", "World");
string concatArray = string.Concat(new[] { "a", "b", "c" });  // "abc"
```

### Searching

```csharp
string text = "Hello, World! Hello again!";

// Index of
int index = text.IndexOf("Hello");           // 0
int lastIndex = text.LastIndexOf("Hello");   // 14
int indexIgnoreCase = text.IndexOf("hello", StringComparison.OrdinalIgnoreCase);

// Index of any
int anyIndex = text.IndexOfAny(new[] { 'o', 'e' });  // 1

// Contains
bool contains = text.Contains("World");
bool containsIgnoreCase = text.Contains("world", StringComparison.OrdinalIgnoreCase);
```

## StringBuilder

For building strings incrementally, especially in loops.

```csharp
var sb = new StringBuilder();

// Append
sb.Append("Hello");
sb.Append(' ');
sb.Append("World");
sb.AppendLine("!");
sb.AppendLine("Second line");

// Append formatted
sb.AppendFormat("Price: {0:C2}", 19.99);
sb.Append($"Date: {DateTime.Now:d}");

// Insert
sb.Insert(0, "Greeting: ");

// Replace
sb.Replace("World", "Universe");

// Remove
sb.Remove(0, 10);  // Remove first 10 characters

// Clear
sb.Clear();

// Get result
string result = sb.ToString();

// Capacity management
var sbCapacity = new StringBuilder(initialCapacity: 1000);
sbCapacity.EnsureCapacity(2000);

// Chaining
var chained = new StringBuilder()
    .Append("Hello")
    .Append(' ')
    .Append("World")
    .ToString();
```

### When to Use StringBuilder

```csharp
// BAD - creates many intermediate strings
string result = "";
for (int i = 0; i < 1000; i++)
{
    result += i.ToString();  // O(n²) - each += creates new string
}

// GOOD - efficient
var sb = new StringBuilder();
for (int i = 0; i < 1000; i++)
{
    sb.Append(i);  // O(n)
}
string result = sb.ToString();

// Single concatenation is fine
string simple = a + b + c;  // Compiler optimizes this

// Use string.Join for collections
string joined = string.Join(",", items);  // Better than loop
```

## Formatting

### Composite Formatting

```csharp
// Format with placeholders
string formatted = string.Format("Hello, {0}! You are {1} years old.", name, age);

// With format specifiers
string currency = string.Format("{0:C}", 1234.56);      // $1,234.56
string number = string.Format("{0:N2}", 1234.5678);     // 1,234.57
string percent = string.Format("{0:P1}", 0.1234);       // 12.3%
string hex = string.Format("{0:X}", 255);               // FF
string date = string.Format("{0:yyyy-MM-dd}", DateTime.Now);

// Alignment
string left = string.Format("{0,-10}", "Hi");    // "Hi        "
string right = string.Format("{0,10}", "Hi");    // "        Hi"
```

### Custom Format Strings

```csharp
// Numeric
double value = 1234.5678;
value.ToString("F2");        // "1234.57" - fixed point
value.ToString("N2");        // "1,234.57" - number with separators
value.ToString("E2");        // "1.23E+003" - scientific
value.ToString("0.00");      // "1234.57" - custom
value.ToString("#,##0.00");  // "1,234.57" - custom with grouping

// Date/Time
DateTime dt = DateTime.Now;
dt.ToString("yyyy-MM-dd");           // "2024-01-15"
dt.ToString("HH:mm:ss");             // "14:30:45"
dt.ToString("MMMM dd, yyyy");        // "January 15, 2024"
dt.ToString("dddd");                 // "Monday"
dt.ToString("o");                    // ISO 8601

// TimeSpan
TimeSpan ts = TimeSpan.FromHours(2.5);
ts.ToString(@"hh\:mm\:ss");          // "02:30:00"
```

### IFormattable

```csharp
public class Temperature : IFormattable
{
    public double Celsius { get; }

    public Temperature(double celsius) => Celsius = celsius;

    public string ToString(string? format, IFormatProvider? formatProvider)
    {
        return format?.ToUpperInvariant() switch
        {
            "C" => $"{Celsius:F1}°C",
            "F" => $"{Celsius * 9 / 5 + 32:F1}°F",
            "K" => $"{Celsius + 273.15:F1}K",
            _ => $"{Celsius:F1}°C"
        };
    }
}

var temp = new Temperature(25);
Console.WriteLine($"{temp:C}");  // "25.0°C"
Console.WriteLine($"{temp:F}");  // "77.0°F"
```

## Parsing

### Basic Parsing

```csharp
// Parse - throws on failure
int number = int.Parse("42");
double d = double.Parse("3.14");
DateTime date = DateTime.Parse("2024-01-15");

// TryParse - safe, returns bool
if (int.TryParse(input, out int result))
{
    Console.WriteLine($"Parsed: {result}");
}
else
{
    Console.WriteLine("Invalid input");
}

// With format provider
decimal price = decimal.Parse("1,234.56", CultureInfo.InvariantCulture);

// Exact date parsing
DateTime exact = DateTime.ParseExact(
    "15/01/2024",
    "dd/MM/yyyy",
    CultureInfo.InvariantCulture);
```

### Span-Based Parsing (High Performance)

```csharp
ReadOnlySpan<char> input = "42".AsSpan();

// No allocation parsing
if (int.TryParse(input, out int value))
{
    Console.WriteLine(value);
}

// Parse from middle of string without substring
string text = "Value: 42 units";
ReadOnlySpan<char> numberSpan = text.AsSpan(7, 2);
int parsed = int.Parse(numberSpan);
```

## High-Performance String Operations

### Span-Based String Manipulation

```csharp
string text = "Hello, World!";
ReadOnlySpan<char> span = text.AsSpan();

// Slice without allocation
ReadOnlySpan<char> hello = span[..5];       // "Hello"
ReadOnlySpan<char> world = span[7..12];     // "World"

// Searching
int index = span.IndexOf(',');
int lastIndex = span.LastIndexOf('o');

// Comparison
bool equals = span.SequenceEqual("Hello, World!");
bool startsWith = span.StartsWith("Hello");

// Trimming (returns span, no allocation)
ReadOnlySpan<char> trimmed = "  hello  ".AsSpan().Trim();
```

### string.Create

Create strings efficiently with a buffer.

```csharp
// Create string with exact length, populate via span
string result = string.Create(10, 42, (chars, state) =>
{
    state.TryFormat(chars, out int written);
    chars[written..].Fill('0');
});

// More complex example
string formatted = string.Create(20, (name: "Alice", age: 30), (chars, state) =>
{
    int pos = 0;
    state.name.AsSpan().CopyTo(chars);
    pos += state.name.Length;
    chars[pos++] = ':';
    state.age.TryFormat(chars[pos..], out int written);
});
```

### SearchValues (C# 8.0 / .NET 8)

Optimized searching for multiple values.

```csharp
// Create once, reuse for multiple searches
private static readonly SearchValues<char> Vowels =
    SearchValues.Create("aeiouAEIOU");

public int CountVowels(ReadOnlySpan<char> text)
{
    int count = 0;
    int index;
    while ((index = text.IndexOfAny(Vowels)) >= 0)
    {
        count++;
        text = text[(index + 1)..];
    }
    return count;
}
```

### CompositeFormat (C# 10 / .NET 6)

Pre-parsed format strings for repeated use.

```csharp
private static readonly CompositeFormat LogFormat =
    CompositeFormat.Parse("[{0:HH:mm:ss}] {1}: {2}");

public void Log(string level, string message)
{
    string formatted = string.Format(null, LogFormat, DateTime.Now, level, message);
    Console.WriteLine(formatted);
}
```

## Regular Expressions

### Basic Patterns

```csharp
using System.Text.RegularExpressions;

string text = "Contact: john@example.com or jane@test.org";

// Simple match
bool hasEmail = Regex.IsMatch(text, @"\w+@\w+\.\w+");

// Find match
Match match = Regex.Match(text, @"\w+@\w+\.\w+");
if (match.Success)
{
    Console.WriteLine(match.Value);  // john@example.com
}

// Find all matches
MatchCollection matches = Regex.Matches(text, @"\w+@\w+\.\w+");
foreach (Match m in matches)
{
    Console.WriteLine(m.Value);
}

// Replace
string replaced = Regex.Replace(text, @"\w+@\w+\.\w+", "[EMAIL]");
```

### Compiled and Source-Generated Regex

```csharp
// Compiled regex - faster for repeated use
private static readonly Regex EmailRegex = new(
    @"\w+@\w+\.\w+",
    RegexOptions.Compiled);

// Source-generated regex (C# 11 / .NET 7) - best performance
[GeneratedRegex(@"\w+@\w+\.\w+", RegexOptions.IgnoreCase)]
private static partial Regex EmailRegexGenerated();

// Usage
bool hasEmail = EmailRegexGenerated().IsMatch(text);
```

### Groups and Captures

```csharp
string input = "John Doe (john@example.com)";
var pattern = @"(?<name>\w+ \w+) \((?<email>\w+@\w+\.\w+)\)";

Match match = Regex.Match(input, pattern);
if (match.Success)
{
    string name = match.Groups["name"].Value;   // "John Doe"
    string email = match.Groups["email"].Value; // "john@example.com"
}
```

## String Interning

```csharp
// Manual interning for frequently used runtime strings
string interned = string.Intern(computedString);

// Check if interned
string? existing = string.IsInterned(someString);

// Use cases:
// - Large number of duplicate strings
// - Strings used as dictionary keys repeatedly
// - Configuration values accessed frequently

// Caution: interned strings live for app lifetime
```

## Version History

| Feature | Version | Significance |
|---------|---------|--------------|
| String interpolation | C# 6.0 | $ prefix |
| Span<char> | C# 7.2 | Zero-allocation slicing |
| Index/Range | C# 8.0 | String slicing syntax |
| Interpolated verbatim | C# 8.0 | $@"..." |
| string.Create | .NET Core 2.1 | Buffer-based creation |
| Raw string literals | C# 11 | """ syntax |
| UTF-8 string literals | C# 11 | "text"u8 for direct UTF-8 bytes |
| Source-generated regex | C# 11 | Compile-time regex |
| SearchValues | .NET 8 | Optimized multi-value search |

## Key Takeaways

**Strings are immutable**: Every modification creates a new string. Use StringBuilder for building strings in loops.

**Use the right comparison**: Ordinal for identifiers and paths, CurrentCulture for user-facing text.

**Prefer Span for parsing**: Use `ReadOnlySpan<char>` to avoid allocations when processing substrings.

**string.Join over concatenation loops**: More efficient and readable.

**Compiled regex for hot paths**: Use `RegexOptions.Compiled` or source-generated regex for performance.

**Raw strings for embedded content**: Use `"""` for JSON, SQL, or other content with quotes.
