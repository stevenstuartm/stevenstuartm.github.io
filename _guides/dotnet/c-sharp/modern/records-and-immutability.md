---
title: "C# Records and Immutability"
layout: guide
category: ".NET & C#"
subcategory: "Modern Features"
description: "Records, immutable patterns, with expressions, and designing for immutability in modern C#."
tags: [c-sharp, dotnet, modern-csharp, records, immutability, functional-programming, practical]
---

## Why Immutability

Immutable objects cannot be changed after creation. This makes code easier to reason about and thread-safe by default.

```csharp
// Mutable - can lead to bugs
public class MutablePerson
{
    public string Name { get; set; }
    public int Age { get; set; }
}

var person = new MutablePerson { Name = "Alice", Age = 30 };
SomeMethod(person);
// Did SomeMethod change person? We can't know without reading it.

// Immutable - safe
public record Person(string Name, int Age);

var person = new Person("Alice", 30);
SomeMethod(person);
// person is unchanged - guaranteed
```

## Records (C# 9.0)

Records are reference types designed for immutable data with value-based equality.

### Positional Records

The most concise syntax, generating constructor, properties, deconstruction, and equality.

```csharp
// One line defines a complete type
public record Person(string FirstName, string LastName);

// Equivalent to (simplified):
public class Person
{
    public string FirstName { get; init; }
    public string LastName { get; init; }

    public Person(string firstName, string lastName)
    {
        FirstName = firstName;
        LastName = lastName;
    }

    public void Deconstruct(out string firstName, out string lastName)
    {
        firstName = FirstName;
        lastName = LastName;
    }

    // Plus Equals, GetHashCode, ==, !=, ToString...
}
```

### Using Records

```csharp
public record Person(string FirstName, string LastName);

// Creation
var person = new Person("John", "Doe");

// Value equality
var person2 = new Person("John", "Doe");
Console.WriteLine(person == person2);  // true
Console.WriteLine(ReferenceEquals(person, person2));  // false

// Deconstruction
var (first, last) = person;

// ToString is automatically implemented
Console.WriteLine(person);  // Person { FirstName = John, LastName = Doe }
```

### With Expressions

Create a copy with modified properties.

```csharp
public record Person(string FirstName, string LastName, int Age);

var original = new Person("John", "Doe", 30);

// Create modified copy - original unchanged
var older = original with { Age = 31 };
var renamed = original with { FirstName = "Jane", LastName = "Smith" };

// Chain modifications
var updated = original with { FirstName = "Jane" } with { Age = 25 };

// Copy with no changes (shallow clone)
var copy = original with { };
```

### Records with Additional Members

```csharp
public record Employee(string Name, string Department, decimal Salary)
{
    // Additional property
    public DateTime HireDate { get; init; } = DateTime.Now;

    // Computed property
    public int YearsEmployed => (DateTime.Now - HireDate).Days / 365;

    // Methods
    public decimal CalculateBonus(decimal percentage) =>
        Salary * percentage;

    // Override generated methods if needed
    public override string ToString() =>
        $"{Name} ({Department})";
}
```

### Non-Positional Records

When you need more control over property definitions.

```csharp
public record Product
{
    public int Id { get; init; }
    public string Name { get; init; } = "";
    public decimal Price { get; init; }

    // Mutable property (unusual in records but allowed)
    public int StockCount { get; set; }
}

var product = new Product
{
    Id = 1,
    Name = "Widget",
    Price = 9.99m,
    StockCount = 100
};
```

### Record Inheritance

```csharp
public record Person(string Name);
public record Employee(string Name, string Department) : Person(Name);
public record Manager(string Name, string Department, int TeamSize)
    : Employee(Name, Department);

var manager = new Manager("Alice", "Engineering", 5);
Console.WriteLine(manager);
// Manager { Name = Alice, Department = Engineering, TeamSize = 5 }

// With expressions work with inheritance
Employee employee = manager with { Department = "Product" };
```

### Sealed Records

```csharp
// Prevent inheritance
public sealed record Configuration(string Key, string Value);

// Records are sealed by default in positional syntax
// To allow inheritance, don't use sealed
```

## Record Structs (C# 10)

Value type records for when you need stack allocation and value semantics.

```csharp
// Record struct - mutable by default
public record struct Point(double X, double Y);

var p = new Point(1, 2);
p.X = 3;  // Allowed - mutable

// Readonly record struct - immutable
public readonly record struct ImmutablePoint(double X, double Y);

var ip = new ImmutablePoint(1, 2);
// ip.X = 3;  // Error - immutable

// With expressions work
var ip2 = ip with { X = 3 };
```

### Record Class vs Record Struct

| Aspect | Record Class | Record Struct |
|--------|--------------|---------------|
| Type | Reference | Value |
| Allocation | Heap | Stack/inline |
| Inheritance | Yes | No |
| Null | Can be null | Not null |
| Default mutability | Immutable (init) | Mutable |
| with expression | Shallow copy | Copy |
| Performance | One allocation | Zero allocation |

### Choosing Between Them

<div class="comparison">
<div class="content-card content-card--accent">
<h4>Use Record Class When</h4>
<ul>
<li>Type contains 3+ fields or references other objects</li>
<li>You need inheritance hierarchies</li>
<li>Null is a meaningful state</li>
<li>Object passed around extensively (avoids copying)</li>
</ul>
</div>
<div class="content-card content-card--accent-secondary">
<h4>Use Record Struct When</h4>
<ul>
<li>Small, primitive-like values (coordinates, money)</li>
<li>Creating many short-lived instances</li>
<li>Stack allocation benefits matter (GC pressure)</li>
<li>Type should never be null</li>
</ul>
</div>
</div>

<div class="callout callout--note">
<p class="callout__title">Why Size Matters</p>
<p>Value types are copied on assignment and when passed to methods. A record struct with 10 fields copies all 10 fields every time. For small types (16-24 bytes), copying is cheap. For larger types, the copying overhead exceeds the benefit of avoiding heap allocation.</p>
</div>

```csharp
// Use record class for:
public record Order(int Id, Customer Customer, List<LineItem> Items);
// - Complex types with references
// - Types used in collections and passed between methods frequently
// - Domain entities

// Use record struct for:
public readonly record struct Coordinate(double Latitude, double Longitude);
// - Small value objects (2-3 primitive fields)
// - Types created frequently in loops or calculations
// - Mathematical types, identifiers, measurements
```

## Immutability Patterns

### Init-Only Properties

Properties settable only during object initialization.

```csharp
public class Configuration
{
    public string Environment { get; init; }
    public string ConnectionString { get; init; }
    public int Timeout { get; init; } = 30;
}

var config = new Configuration
{
    Environment = "Production",
    ConnectionString = "Server=..."
};

// config.Environment = "Development";  // Error after initialization
```

### Readonly Structs

```csharp
public readonly struct Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    public Money(decimal amount, string currency)
    {
        Amount = amount;
        Currency = currency;
    }

    // Methods must not modify state
    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException("Currency mismatch");
        return new Money(Amount + other.Amount, Currency);
    }

    public Money MultiplyBy(decimal factor) =>
        new Money(Amount * factor, Currency);
}
```

### Immutable Collections

```csharp
using System.Collections.Immutable;

// Create immutable list
var list = ImmutableList<int>.Empty
    .Add(1)
    .Add(2)
    .Add(3);

// Operations return new collections
var newList = list.Add(4);
// list still has 3 items, newList has 4

// From existing collection
var numbers = new[] { 1, 2, 3 };
var immutableNumbers = numbers.ToImmutableArray();

// Builders for bulk operations
var builder = ImmutableList.CreateBuilder<string>();
builder.Add("one");
builder.Add("two");
builder.Add("three");
ImmutableList<string> result = builder.ToImmutable();

// Common immutable collections
ImmutableArray<T>       // Best performance for readonly scenarios
ImmutableList<T>        // Efficient modifications
ImmutableDictionary<K,V>
ImmutableHashSet<T>
ImmutableSortedSet<T>
ImmutableQueue<T>
ImmutableStack<T>
```

### Defensive Copies

When you must work with mutable types in an immutable context.

```csharp
public class Order
{
    private readonly List<LineItem> items;

    public Order(IEnumerable<LineItem> items)
    {
        // Defensive copy - don't store reference to mutable input
        this.items = items.ToList();
    }

    // Return copy - don't expose internal mutable state
    public IReadOnlyList<LineItem> Items => items.AsReadOnly();

    // Or use immutable collection
    public ImmutableList<LineItem> ItemsImmutable =>
        items.ToImmutableList();
}
```

### Builder Pattern for Immutable Objects

```csharp
public record Configuration(
    string Environment,
    string ConnectionString,
    int Timeout,
    bool EnableLogging);

public class ConfigurationBuilder
{
    private string environment = "Development";
    private string connectionString = "";
    private int timeout = 30;
    private bool enableLogging = false;

    public ConfigurationBuilder WithEnvironment(string env)
    {
        environment = env;
        return this;
    }

    public ConfigurationBuilder WithConnection(string conn)
    {
        connectionString = conn;
        return this;
    }

    public ConfigurationBuilder WithTimeout(int seconds)
    {
        timeout = seconds;
        return this;
    }

    public ConfigurationBuilder WithLogging(bool enable = true)
    {
        enableLogging = enable;
        return this;
    }

    public Configuration Build() =>
        new(environment, connectionString, timeout, enableLogging);
}

// Usage
var config = new ConfigurationBuilder()
    .WithEnvironment("Production")
    .WithConnection("Server=...")
    .WithTimeout(60)
    .WithLogging()
    .Build();
```

## Equality in Records

Records provide value equality by default.

```csharp
public record Person(string Name, int Age);

var p1 = new Person("Alice", 30);
var p2 = new Person("Alice", 30);
var p3 = new Person("Bob", 30);

Console.WriteLine(p1 == p2);     // true - same values
Console.WriteLine(p1 == p3);     // false - different Name
Console.WriteLine(p1.Equals(p2)); // true

// HashCode based on values
var set = new HashSet<Person> { p1 };
Console.WriteLine(set.Contains(p2));  // true - same hash
```

### Custom Equality

```csharp
public record Person(string FirstName, string LastName, int Age)
{
    // Compare only by name, ignore age
    public virtual bool Equals(Person? other) =>
        other is not null &&
        FirstName == other.FirstName &&
        LastName == other.LastName;

    public override int GetHashCode() =>
        HashCode.Combine(FirstName, LastName);
}
```

### Reference Members in Records

Be careful with mutable reference types in records.

```csharp
public record Order(int Id, List<string> Items);

var order1 = new Order(1, new List<string> { "A", "B" });
var order2 = order1 with { };  // Shallow copy!

order2.Items.Add("C");  // Modifies both!
Console.WriteLine(order1.Items.Count);  // 3 - unexpected

// Solution: Use immutable collections
public record SafeOrder(int Id, ImmutableList<string> Items);

var safe1 = new SafeOrder(1, ImmutableList.Create("A", "B"));
var safe2 = safe1 with { Items = safe1.Items.Add("C") };
Console.WriteLine(safe1.Items.Count);  // 2 - unchanged
Console.WriteLine(safe2.Items.Count);  // 3
```

## Practical Examples

### Domain Value Objects

```csharp
public readonly record struct EmailAddress
{
    public string Value { get; }

    public EmailAddress(string value)
    {
        if (string.IsNullOrWhiteSpace(value) || !value.Contains('@'))
            throw new ArgumentException("Invalid email address", nameof(value));
        Value = value.ToLowerInvariant();
    }

    public static implicit operator string(EmailAddress email) => email.Value;
    public override string ToString() => Value;
}

public readonly record struct Money(decimal Amount, string Currency)
{
    public static Money USD(decimal amount) => new(amount, "USD");
    public static Money EUR(decimal amount) => new(amount, "EUR");

    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException("Cannot add different currencies");
        return this with { Amount = Amount + other.Amount };
    }
}
```

### DTOs and API Models

```csharp
public record CreateUserRequest(
    string Email,
    string Password,
    string DisplayName);

public record UserResponse(
    int Id,
    string Email,
    string DisplayName,
    DateTime CreatedAt);

public record ApiError(
    string Code,
    string Message,
    ImmutableList<string>? Details = null);
```

### Event Sourcing Events

```csharp
public abstract record DomainEvent(DateTime OccurredAt);

public record OrderCreated(
    Guid OrderId,
    Guid CustomerId,
    DateTime OccurredAt) : DomainEvent(OccurredAt);

public record ItemAdded(
    Guid OrderId,
    string ProductCode,
    int Quantity,
    DateTime OccurredAt) : DomainEvent(OccurredAt);

public record OrderCompleted(
    Guid OrderId,
    decimal Total,
    DateTime OccurredAt) : DomainEvent(OccurredAt);
```

### Configuration

```csharp
public record DatabaseConfig(
    string Server,
    string Database,
    int Port = 5432,
    int MaxPoolSize = 100,
    TimeSpan ConnectionTimeout = default)
{
    public TimeSpan ConnectionTimeout { get; init; } =
        ConnectionTimeout == default ? TimeSpan.FromSeconds(30) : ConnectionTimeout;

    public string ConnectionString =>
        $"Server={Server};Database={Database};Port={Port};Pooling=true;MaxPoolSize={MaxPoolSize}";
}
```
## Key Takeaways

**Use records for data transfer**: DTOs, API models, events, and value objects are ideal record use cases.

**Prefer immutability by default**: Mutable state is a common source of bugs. Start immutable and add mutability only when necessary.

**with expressions for modifications**: Don't mutate records; create new instances with desired changes.

**Readonly record structs for small values**: Use for coordinates, money, dates, and other small value objects that benefit from stack allocation.

**Be careful with reference members**: Records do shallow copies. Use immutable collections inside records or implement custom copying.

**Init-only for non-record immutability**: When you need immutable classes but not all record features, use init-only setters.
