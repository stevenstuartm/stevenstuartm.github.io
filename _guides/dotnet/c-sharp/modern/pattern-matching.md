---
title: "C# Pattern Matching"
layout: guide
category: ".NET & C#"
subcategory: "Modern Features"
description: "Comprehensive guide to pattern matching in C# from type patterns to list patterns, with practical examples and best practices."
tags: [c-sharp, dotnet, modern-csharp, pattern-matching, functional-programming, practical]
---

## What is Pattern Matching

Pattern matching allows you to test whether a value has a particular shape and extract information from it. It's more expressive than traditional if-else chains and produces cleaner, more declarative code.

```csharp
// Traditional approach
if (shape is Circle)
{
    var circle = (Circle)shape;
    return Math.PI * circle.Radius * circle.Radius;
}
else if (shape is Rectangle)
{
    var rect = (Rectangle)shape;
    return rect.Width * rect.Height;
}

// Pattern matching approach
return shape switch
{
    Circle c => Math.PI * c.Radius * c.Radius,
    Rectangle r => r.Width * r.Height,
    _ => 0
};
```

## Type Patterns

Test whether a value is of a specific type and optionally capture it.

### is Expression (C# 7.0)

```csharp
object value = GetValue();

// Type pattern with variable
if (value is string text)
{
    Console.WriteLine($"String: {text.ToUpper()}");
}
else if (value is int number)
{
    Console.WriteLine($"Integer: {number * 2}");
}
else if (value is IEnumerable<int> numbers)
{
    Console.WriteLine($"Count: {numbers.Count()}");
}

// Combined with other conditions
if (value is string s && s.Length > 10)
{
    Console.WriteLine($"Long string: {s}");
}
```

### Switch Statement with Type Patterns

```csharp
public double CalculateArea(object shape)
{
    switch (shape)
    {
        case Circle c:
            return Math.PI * c.Radius * c.Radius;
        case Rectangle r:
            return r.Width * r.Height;
        case Triangle t:
            return 0.5 * t.Base * t.Height;
        case null:
            throw new ArgumentNullException(nameof(shape));
        default:
            throw new ArgumentException($"Unknown shape: {shape.GetType()}");
    }
}
```

### Switch Expression (C# 8.0)

```csharp
public double CalculateArea(object shape) => shape switch
{
    Circle c => Math.PI * c.Radius * c.Radius,
    Rectangle r => r.Width * r.Height,
    Triangle t => 0.5 * t.Base * t.Height,
    null => throw new ArgumentNullException(nameof(shape)),
    _ => throw new ArgumentException($"Unknown shape: {shape.GetType()}")
};
```

## Constant Patterns

Match against constant values.

```csharp
public string Classify(int value) => value switch
{
    0 => "Zero",
    1 => "One",
    2 => "Two",
    42 => "The Answer",
    _ => "Other"
};

// With null
public string Describe(object? obj) => obj switch
{
    null => "Nothing",
    "" => "Empty string",
    0 => "Zero",
    _ => obj.ToString() ?? "Unknown"
};
```

## Relational Patterns (C# 9.0)

Compare values using <, >, <=, >=.

```csharp
public string GetTemperatureDescription(int temp) => temp switch
{
    < 0 => "Freezing",
    >= 0 and < 10 => "Cold",
    >= 10 and < 20 => "Cool",
    >= 20 and < 30 => "Warm",
    >= 30 => "Hot"
};

public decimal CalculateShipping(decimal orderTotal) => orderTotal switch
{
    < 25 => 5.99m,
    < 50 => 3.99m,
    < 100 => 1.99m,
    _ => 0m // Free shipping
};

public char GetGrade(int score) => score switch
{
    >= 90 => 'A',
    >= 80 => 'B',
    >= 70 => 'C',
    >= 60 => 'D',
    _ => 'F'
};
```

## Logical Patterns (C# 9.0)

Combine patterns with `and`, `or`, and `not`.

### and Pattern

```csharp
public bool IsValidAge(int age) => age is >= 0 and <= 120;

public string Classify(int value) => value switch
{
    > 0 and < 10 => "Single digit positive",
    >= 10 and < 100 => "Double digit",
    >= 100 and < 1000 => "Triple digit",
    _ => "Other"
};
```

### or Pattern

```csharp
public bool IsWeekend(DayOfWeek day) =>
    day is DayOfWeek.Saturday or DayOfWeek.Sunday;

public decimal GetDiscount(string customerType) => customerType switch
{
    "gold" or "platinum" => 0.20m,
    "silver" => 0.10m,
    _ => 0m
};

// Combine multiple values
public bool IsVowel(char c) =>
    c is 'a' or 'e' or 'i' or 'o' or 'u'
       or 'A' or 'E' or 'I' or 'O' or 'U';
```

### not Pattern

```csharp
// Null checking
if (customer is not null)
{
    ProcessCustomer(customer);
}

// Negating conditions
if (input is not "")
{
    Process(input);
}

// Combined negation
if (status is not (Status.Cancelled or Status.Failed))
{
    Continue();
}

// In switch
public string Describe(object obj) => obj switch
{
    null => "null",
    not string => "not a string",
    string s => $"string: {s}"
};
```

## Property Patterns (C# 8.0)

Match on property values of an object.

### Basic Property Pattern

```csharp
public decimal CalculateDiscount(Customer customer) => customer switch
{
    { IsPremium: true } => 0.20m,
    { YearsActive: > 5 } => 0.10m,
    { TotalPurchases: > 1000 } => 0.05m,
    _ => 0m
};

// Multiple properties
public string Classify(Customer customer) => customer switch
{
    { IsPremium: true, YearsActive: > 5 } => "VIP",
    { IsPremium: true } => "Premium",
    { YearsActive: > 10 } => "Loyal",
    _ => "Regular"
};
```

### Nested Property Patterns

```csharp
public decimal CalculateShipping(Order order) => order switch
{
    { Customer: { IsPremium: true } } => 0m,  // Free for premium
    { ShippingAddress: { Country: "US" } } => 5.99m,
    { ShippingAddress: { Country: "CA" or "MX" } } => 9.99m,
    _ => 19.99m
};

// Deep nesting
public bool IsLocalCustomer(Order order) => order is
{
    Customer:
    {
        Address:
        {
            City: "Seattle",
            State: "WA"
        }
    }
};
```

### Extended Property Patterns (C# 10)

Simplified syntax for nested properties.

```csharp
// Before C# 10
public bool IsLocal(Order o) => o is { Customer: { Address: { City: "Seattle" } } };

// C# 10 - dot notation
public bool IsLocal(Order o) => o is { Customer.Address.City: "Seattle" };

public decimal GetTax(Order order) => order switch
{
    { Customer.Address.State: "WA" } => order.Total * 0.10m,
    { Customer.Address.State: "OR" } => 0m,
    { Customer.Address.Country: "US" } => order.Total * 0.08m,
    _ => order.Total * 0.15m
};
```

### Property Patterns with Capture

```csharp
public string Describe(Customer customer) => customer switch
{
    { Name: var name, IsPremium: true } => $"Premium customer: {name}",
    { Name: var name, YearsActive: var years } when years > 5 => $"Loyal customer: {name} ({years} years)",
    { Name: var name } => $"Customer: {name}"
};
```

## Tuple Patterns (C# 8.0)

Match multiple values simultaneously.

```csharp
public string GetQuadrant(int x, int y) => (x, y) switch
{
    (0, 0) => "Origin",
    (> 0, > 0) => "Quadrant 1",
    (< 0, > 0) => "Quadrant 2",
    (< 0, < 0) => "Quadrant 3",
    (> 0, < 0) => "Quadrant 4",
    (0, _) => "Y-axis",
    (_, 0) => "X-axis"
};

// State machine logic
public State GetNextState(State current, Event evt) => (current, evt) switch
{
    (State.Idle, Event.Start) => State.Running,
    (State.Running, Event.Pause) => State.Paused,
    (State.Running, Event.Stop) => State.Stopped,
    (State.Paused, Event.Resume) => State.Running,
    (State.Paused, Event.Stop) => State.Stopped,
    _ => current // No state change
};

// Rock-Paper-Scissors
public string GetWinner(string p1, string p2) => (p1, p2) switch
{
    ("rock", "scissors") or ("scissors", "paper") or ("paper", "rock") => "Player 1",
    ("scissors", "rock") or ("paper", "scissors") or ("rock", "paper") => "Player 2",
    _ => "Tie"
};
```

## Positional Patterns

Match based on Deconstruct method or positional record properties.

```csharp
public record Point(int X, int Y);

public string Classify(Point point) => point switch
{
    (0, 0) => "Origin",
    (var x, 0) => $"On X-axis at {x}",
    (0, var y) => $"On Y-axis at {y}",
    (var x, var y) when x == y => $"On diagonal at ({x}, {y})",
    (var x, var y) => $"Point at ({x}, {y})"
};

// With classes that have Deconstruct
public class Rectangle
{
    public double Width { get; }
    public double Height { get; }

    public Rectangle(double width, double height)
    {
        Width = width;
        Height = height;
    }

    public void Deconstruct(out double width, out double height)
    {
        width = Width;
        height = Height;
    }
}

public string DescribeRectangle(Rectangle rect) => rect switch
{
    (0, _) or (_, 0) => "Line or point",
    (var w, var h) when w == h => $"Square with side {w}",
    (var w, var h) when w > h => $"Wide rectangle {w}x{h}",
    (var w, var h) => $"Tall rectangle {w}x{h}"
};
```

## List Patterns (C# 11)

Match arrays, lists, and spans based on their elements.

### Basic List Patterns

```csharp
int[] numbers = { 1, 2, 3 };

// Exact match
bool isOneTwoThree = numbers is [1, 2, 3];  // true

// Length check
bool hasThreeElements = numbers is [_, _, _];  // true

// First element check
bool startsWithOne = numbers is [1, ..];  // true

// Last element check
bool endsWithThree = numbers is [.., 3];  // true

// First and last
bool bookends = numbers is [1, .., 3];  // true
```

### Capturing Elements

```csharp
if (numbers is [var first, .., var last])
{
    Console.WriteLine($"First: {first}, Last: {last}");
}

// Capture middle elements
if (numbers is [var head, .. var middle, var tail])
{
    Console.WriteLine($"Head: {head}, Tail: {tail}");
    Console.WriteLine($"Middle: [{string.Join(", ", middle)}]");
}
```

### Switch with List Patterns

```csharp
public string DescribeList(int[] arr) => arr switch
{
    [] => "Empty",
    [var single] => $"Single element: {single}",
    [var first, var second] => $"Pair: {first}, {second}",
    [var first, .., var last] => $"Multiple: {first}...{last} ({arr.Length} items)",
};

// Processing commands
public string ProcessCommand(string[] args) => args switch
{
    ["help"] => ShowHelp(),
    ["version"] => ShowVersion(),
    ["add", var item] => AddItem(item),
    ["remove", var item] => RemoveItem(item),
    ["config", var key, var value] => SetConfig(key, value),
    [var cmd, ..] => $"Unknown command: {cmd}",
    [] => "No command provided"
};
```

### Nested List Patterns

```csharp
public string AnalyzeData(int[][] matrix) => matrix switch
{
    [[]] => "Empty row",
    [[var single]] => $"Single value: {single}",
    [[1, 0], [0, 1]] => "Identity matrix 2x2",
    [[var a, var b], [var c, var d]] => $"2x2 matrix",
    _ => "Other matrix"
};
```

## var Pattern

Always matches and captures the value.

```csharp
// Useful with when clause
public string Process(object obj) => obj switch
{
    string s when s.Length > 100 => "Long string",
    string s => $"String: {s}",
    int n when n < 0 => "Negative",
    var x => $"Other: {x}"  // var always matches
};

// Decomposition
if (GetPoint() is var (x, y))
{
    Console.WriteLine($"Point: ({x}, {y})");
}
```

## Discard Pattern (_)

Match anything without capturing.

```csharp
// Ignore specific positions
public string Describe((int, int, int) tuple) => tuple switch
{
    (0, 0, 0) => "Origin",
    (_, 0, 0) => "On X-axis",
    (0, _, 0) => "On Y-axis",
    (0, 0, _) => "On Z-axis",
    _ => "Somewhere else"
};

// Default case in switch
public string GetCategory(int code) => code switch
{
    >= 100 and < 200 => "Informational",
    >= 200 and < 300 => "Success",
    >= 300 and < 400 => "Redirect",
    >= 400 and < 500 => "Client Error",
    >= 500 and < 600 => "Server Error",
    _ => "Unknown"  // Default
};
```

## When Clause

Add additional conditions to patterns.

```csharp
public decimal CalculateTax(Order order) => order switch
{
    { Total: var t } when t < 0 => throw new ArgumentException("Invalid total"),
    { Customer.Address.State: "WA" } when order.Total > 100 => order.Total * 0.10m,
    { Customer.Address.State: "WA" } => order.Total * 0.08m,
    { Customer.IsTaxExempt: true } => 0m,
    _ => order.Total * 0.07m
};

// Complex conditions
public bool ShouldProcess(Order order) => order switch
{
    { Status: OrderStatus.Pending } when DateTime.Now - order.CreatedAt > TimeSpan.FromDays(7) => false,
    { Status: OrderStatus.Pending, Items.Count: > 0 } => true,
    _ => false
};
```

## Practical Examples

### Command Handler

```csharp
public record Command;
public record CreateUser(string Name, string Email) : Command;
public record DeleteUser(int UserId) : Command;
public record UpdateEmail(int UserId, string NewEmail) : Command;

public async Task<Result> HandleCommand(Command command) => command switch
{
    CreateUser(var name, var email) => await CreateUserAsync(name, email),
    DeleteUser(var id) => await DeleteUserAsync(id),
    UpdateEmail(var id, var email) => await UpdateEmailAsync(id, email),
    null => Result.Error("Command cannot be null"),
    _ => Result.Error($"Unknown command: {command.GetType().Name}")
};
```

### Response Handler

```csharp
public async Task<T?> HandleResponse<T>(HttpResponseMessage response) => response switch
{
    { IsSuccessStatusCode: true } => await response.Content.ReadFromJsonAsync<T>(),
    { StatusCode: HttpStatusCode.NotFound } => default,
    { StatusCode: HttpStatusCode.Unauthorized } => throw new UnauthorizedException(),
    { StatusCode: var code } => throw new HttpException($"HTTP {(int)code}")
};
```

### Validation

```csharp
public IEnumerable<string> Validate(Customer customer) => customer switch
{
    null => new[] { "Customer is required" },
    { Name: null or "" } => new[] { "Name is required" },
    { Email: null or "" } => new[] { "Email is required" },
    { Email: var e } when !e.Contains('@') => new[] { "Invalid email format" },
    { Age: < 0 or > 150 } => new[] { "Invalid age" },
    _ => Enumerable.Empty<string>()
};
```

## Version History

| Feature | Version | Significance |
|---------|---------|--------------|
| Type patterns with is | C# 7.0 | Basic pattern matching |
| Switch with patterns | C# 7.0 | Pattern-based switch |
| Property patterns | C# 8.0 | Match object properties |
| Tuple patterns | C# 8.0 | Match multiple values |
| Switch expressions | C# 8.0 | Expression-based switching |
| Relational patterns | C# 9.0 | Comparison operators |
| Logical patterns | C# 9.0 | and, or, not combinators |
| Extended property patterns | C# 10 | Dot notation for nested |
| List patterns | C# 11 | Array/list matching |

## Key Takeaways

**Use switch expressions for transformations**: When mapping input to output, switch expressions are clearer than if-else chains.

**Property patterns for object inspection**: Match on object state without casting or temporary variables.

**Combine patterns for expressive conditions**: Logical patterns (`and`, `or`, `not`) and relational patterns (`<`, `>`) reduce nested conditions.

**List patterns for sequences**: Match array structure, extract elements, and handle different lengths elegantly.

**When clauses for complex logic**: Add conditions that can't be expressed with patterns alone.

**Discard (_) for completeness**: Always handle the default case to make switch expressions exhaustive.
