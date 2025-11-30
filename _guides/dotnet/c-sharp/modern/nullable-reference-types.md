---
title: "C# Nullable Reference Types"
layout: guide
category: ".NET & C#"
subcategory: "Modern Features"
description: "Nullable reference types, null safety annotations, and patterns for eliminating null reference exceptions in C#."
tags: [c-sharp, dotnet, modern-csharp, nullable, null-safety, practical]
---

## The Null Problem

<blockquote class="pull-quote">
<p>Null reference exceptions are one of the most common runtime errors.</p>
</blockquote>

Before C# 8.0, any reference type could be null, and the compiler couldn't help identify potential null dereferences.

```csharp
// Without nullable reference types - compiles but crashes
string name = GetName(); // Might return null
int length = name.Length; // NullReferenceException if null
```

Nullable reference types (NRT) enable the compiler to track nullability and warn about potential null issues at compile time.

## Enabling Nullable Reference Types

### Project-Wide (Recommended)

```xml
<!-- In .csproj file -->
<PropertyGroup>
    <Nullable>enable</Nullable>
</PropertyGroup>
```

### File-Level

```csharp
#nullable enable  // Enable for this file
// ... code ...
#nullable disable // Disable for rest of file

#nullable restore // Return to project default
```

### Contextual Control

```csharp
#nullable enable annotations  // Enable annotations only
#nullable enable warnings     // Enable warnings only
```

## Nullable Annotations

### Non-Nullable Reference Types (Default)

When NRT is enabled, reference types are non-nullable by default.

```csharp
#nullable enable

public class Customer
{
    public string Name { get; set; }  // Cannot be null
    public string Email { get; set; } // Cannot be null

    public Customer(string name, string email)
    {
        Name = name;   // OK
        Email = email; // OK
    }
}

// Compiler warnings
Customer c = null;           // Warning: assigning null to non-nullable
string name = c.Name;        // Warning: possible null reference
```

### Nullable Reference Types (?)

Use `?` to indicate a reference type can be null.

```csharp
#nullable enable

public class Customer
{
    public string Name { get; set; }         // Required - cannot be null
    public string? MiddleName { get; set; }  // Optional - can be null
    public string? Email { get; set; }       // Optional - can be null

    public Customer(string name)
    {
        Name = name;
        // MiddleName and Email are null by default
    }
}

// Usage
var customer = new Customer("Alice");
customer.MiddleName = null;  // OK - explicitly nullable

// Must check before using nullable types
if (customer.MiddleName != null)
{
    int length = customer.MiddleName.Length; // Safe - null checked
}

// Or use null-conditional
int? length = customer.MiddleName?.Length;
```

## Null State Analysis

The compiler tracks whether a variable might be null and warns on unsafe access.

```csharp
#nullable enable

public void ProcessCustomer(Customer? customer)
{
    // customer might be null here
    Console.WriteLine(customer.Name);  // Warning: possible null dereference

    if (customer == null)
        return;

    // compiler knows customer is not null after the check
    Console.WriteLine(customer.Name);  // OK - no warning

    // Pattern matching also establishes null state
    if (customer is { Name: var name })
    {
        Console.WriteLine(name); // OK - name is not null
    }
}
```

### Null Guard Patterns

```csharp
public void Process(Customer? customer)
{
    // Guard clause with throw
    if (customer is null)
        throw new ArgumentNullException(nameof(customer));
    // customer is not null here

    // Guard with return
    if (customer is null) return;
    // customer is not null here

    // Pattern matching
    if (customer is not null)
    {
        // customer is not null in this block
    }

    // Null-coalescing throw (C# 7.0+)
    var validCustomer = customer ?? throw new ArgumentNullException(nameof(customer));
}
```

## Null-Forgiving Operator (!)

Tell the compiler you know a value isn't null when it can't determine this.

```csharp
#nullable enable

public class Service
{
    private string? connectionString;

    public void Initialize(string connection)
    {
        connectionString = connection;
    }

    public void DoWork()
    {
        // Compiler doesn't know connectionString was set
        // Use ! to suppress warning when you're certain
        var conn = connectionString!;
    }
}

// Common scenarios for !
// After validation you know isn't tracked
var item = dictionary.TryGetValue(key, out var value) ? value! : default;

// After external initialization
[SetUp]
public void Setup()
{
    service = CreateService(); // Test framework initializes
}
private IService service = null!; // Will be set in Setup
```

<div class="callout callout--warning">
<p class="callout__title">Use ! Sparingly</p>
<p>Overuse defeats the purpose of null safety. Prefer proper null checks or restructuring code.</p>
</div>

## Attributes for Advanced Scenarios

### MemberNotNull

```csharp
public class LazyService
{
    private ILogger? logger;

    [MemberNotNull(nameof(logger))]
    private void EnsureInitialized()
    {
        logger ??= CreateLogger();
    }

    public void Log(string message)
    {
        EnsureInitialized();
        logger.Log(message); // OK - compiler trusts attribute
    }
}
```

### NotNull

```csharp
public static class Guard
{
    public static void NotNull<T>([NotNull] T? value, string paramName) where T : class
    {
        if (value is null)
            throw new ArgumentNullException(paramName);
    }
}

public void Process(Customer? customer)
{
    Guard.NotNull(customer, nameof(customer));
    // customer is not null after this call
    Console.WriteLine(customer.Name);
}
```

### MaybeNull and NotNullWhen

```csharp
// Return value might be null even when T is non-nullable
[return: MaybeNull]
public T Find<T>(string key) where T : class
{
    return cache.ContainsKey(key) ? (T)cache[key] : null;
}

// Parameter is not null when method returns true
public bool TryGetValue(string key, [NotNullWhen(true)] out string? value)
{
    return dictionary.TryGetValue(key, out value);
}

// Usage
if (TryGetValue("key", out var value))
{
    Console.WriteLine(value.Length); // OK - value is not null
}
```

### AllowNull and DisallowNull

```csharp
public class Person
{
    private string name = "Unknown";

    [AllowNull] // Allow null in setter even though property is non-nullable
    public string Name
    {
        get => name;
        set => name = value ?? "Unknown";
    }

    private string? notes;

    [DisallowNull] // Don't allow null in setter even though property is nullable
    public string? Notes
    {
        get => notes;
        set => notes = value ?? throw new ArgumentNullException(nameof(value));
    }
}
```

### NotNullIfNotNull

```csharp
// Return is not null if input is not null
[return: NotNullIfNotNull(nameof(path))]
public string? NormalizePath(string? path)
{
    return path?.Replace("\\", "/");
}

// Usage
string? nullable = GetPath();
string? result1 = NormalizePath(nullable); // Result is nullable

string nonNull = "/some/path";
string result2 = NormalizePath(nonNull); // Result is non-nullable
```

## Nullable Value Types vs Nullable Reference Types

<div class="comparison">
<div class="content-card content-card--accent">
<h4>Nullable Value Types (pre-C# 8.0)</h4>
<ul>
<li>Uses <code>Nullable&lt;T&gt;</code> wrapper struct</li>
<li>Example: <code>int? nullableInt = null;</code></li>
<li>Provides <code>HasValue</code> and <code>Value</code> properties</li>
<li>Runtime overhead: extra struct wrapping</li>
</ul>
</div>
<div class="content-card content-card--accent-secondary">
<h4>Nullable Reference Types (C# 8.0+)</h4>
<ul>
<li>Compile-time annotation only</li>
<li>Example: <code>string? nullableString = null;</code></li>
<li>No runtime overhead or wrapper type</li>
<li>At runtime, still just the reference type (or null)</li>
</ul>
</div>
</div>

```csharp
#nullable enable

// Nullable value type (struct) - always been in C#
int? nullableInt = null;
DateTime? nullableDate = null;

// These are Nullable<T> - a struct wrapper
int? a = 5;
bool hasValue = a.HasValue;  // true
int value = a.Value;         // 5
int valueOrDefault = a.GetValueOrDefault(); // 5

// Nullable reference type - C# 8.0+
string? nullableString = null;

// Not Nullable<T> - just annotated reference
// At runtime, still just a string (or null)
```

## Common Patterns

### Null Object Pattern

```csharp
public interface ILogger
{
    void Log(string message);
}

public class NullLogger : ILogger
{
    public static readonly ILogger Instance = new NullLogger();
    private NullLogger() { }
    public void Log(string message) { /* Do nothing */ }
}

public class Service
{
    private readonly ILogger logger;

    // Never null - use NullLogger instead
    public Service(ILogger? logger = null)
    {
        this.logger = logger ?? NullLogger.Instance;
    }

    public void DoWork()
    {
        logger.Log("Working"); // Always safe
    }
}
```

### Optional Return Values

```csharp
// Clear intent: might not find anything
public Customer? FindCustomer(int id)
{
    return customers.FirstOrDefault(c => c.Id == id);
}

// Usage forces handling the null case
var customer = FindCustomer(123);
if (customer is not null)
{
    ProcessCustomer(customer);
}

// Or with null-coalescing
var customer = FindCustomer(123) ?? CreateGuestCustomer();
```

### Constructor Initialization

```csharp
public class Order
{
    // Non-nullable - must be set
    public string OrderNumber { get; }
    public Customer Customer { get; }

    // Nullable - optional
    public string? Notes { get; set; }
    public DateTime? ShippedDate { get; set; }

    public Order(string orderNumber, Customer customer)
    {
        OrderNumber = orderNumber ?? throw new ArgumentNullException(nameof(orderNumber));
        Customer = customer ?? throw new ArgumentNullException(nameof(customer));
    }
}
```

### Working with Legacy Code

```csharp
// When calling code without nullable annotations
public string? GetValueFromLegacy()
{
    // Legacy method might return null but isn't annotated
    string result = LegacyLibrary.GetValue();

    // Treat as potentially null
    return result;
}

// Or when you know it's safe
public string GetValueFromLegacySafe()
{
    // You've verified this never returns null
    return LegacyLibrary.GetValue()!;
}
```

## Migration Strategy

### Gradual Adoption

1. **Enable annotations only first**
   ```xml
   <Nullable>annotations</Nullable>
   ```
   Add `?` to intentionally nullable types without getting warnings.

2. **Enable warnings on new code**
   Use `#nullable enable` in new files.

3. **Enable project-wide**
   ```xml
   <Nullable>enable</Nullable>
   ```
   Fix warnings incrementally.

### Common Migration Fixes

```csharp
// Before: warning on uninitialized non-nullable
public string Name { get; set; }  // Warning

// Fix 1: Make nullable if truly optional
public string? Name { get; set; }

// Fix 2: Add default value
public string Name { get; set; } = "";

// Fix 3: Use required (C# 11)
public required string Name { get; set; }

// Fix 4: Initialize in constructor
public string Name { get; }
public Customer(string name) => Name = name;
```

## Version History

| Feature | Version | Significance |
|---------|---------|--------------|
| Nullable reference types | C# 8.0 | Compile-time null safety |
| Null parameter checking (!) | C# 8.0 | Suppress null warnings |
| MemberNotNull attribute | C# 9.0 | Flow analysis for members |
| Required members | C# 11 | Ensure initialization |

## Key Takeaways

**Enable NRT for new projects**: Start with `<Nullable>enable</Nullable>` for null safety from the beginning.

**Use ? intentionally**: Mark types nullable only when null is a valid state, not as a way to silence warnings.

**Avoid overusing !**: The null-forgiving operator should be rare. If you need it often, reconsider your design.

**Prefer guards to !**: Null checks are self-documenting and catch bugs; `!` hides them.

**Use attributes for complex flows**: When the compiler can't track nullability through method calls, attributes like `NotNull` and `MemberNotNull` help.

**Migrate gradually**: Enable annotations first, then warnings, fixing issues incrementally rather than all at once.
