---
title: "C# Classes and Structs"
layout: guide
category: ".NET & C#"
subcategory: "Object-Oriented Programming"
description: "Understanding classes, structs, and records in C# including when to use each, initialization patterns, and best practices."
tags: [c-sharp, dotnet, oop, classes, structs, records, practical]
---

## Classes

Classes are reference types that encapsulate data and behavior. They support inheritance and can be allocated on the heap.

### Basic Class Structure

```csharp
public class Customer
{
    // Fields (private by default)
    private readonly int id;
    private string name;

    // Constructor
    public Customer(int id, string name)
    {
        this.id = id;
        this.name = name ?? throw new ArgumentNullException(nameof(name));
    }

    // Properties
    public int Id => id;

    public string Name
    {
        get => name;
        set => name = value ?? throw new ArgumentNullException(nameof(value));
    }

    // Methods
    public void DisplayInfo()
    {
        Console.WriteLine($"Customer {Id}: {Name}");
    }
}
```

### Constructors

```csharp
public class Order
{
    public int Id { get; }
    public DateTime CreatedAt { get; }
    public string CustomerName { get; set; }
    public OrderStatus Status { get; private set; }

    // Primary constructor (parameterless)
    public Order()
    {
        CreatedAt = DateTime.UtcNow;
        Status = OrderStatus.Pending;
    }

    // Parameterized constructor
    public Order(int id, string customerName) : this()
    {
        Id = id;
        CustomerName = customerName;
    }

    // Constructor chaining with 'this'
    public Order(int id) : this(id, "Unknown")
    {
    }

    // Static constructor - runs once per type
    static Order()
    {
        Console.WriteLine("Order type initialized");
    }
}
```

### Primary Constructors (C# 12)

Simplified syntax for capturing constructor parameters directly in the class declaration.

```csharp
// Traditional approach
public class Product
{
    private readonly string name;
    private readonly decimal price;

    public Product(string name, decimal price)
    {
        this.name = name;
        this.price = price;
    }

    public string Name => name;
    public decimal Price => price;
}

// Primary constructor (C# 12)
public class Product(string name, decimal price)
{
    public string Name => name;
    public decimal Price => price;

    public decimal CalculateDiscount(decimal percentage) =>
        price * (1 - percentage);
}

// Primary constructor parameters are available throughout the class
public class OrderProcessor(ILogger logger, IEmailService emailService)
{
    public async Task ProcessAsync(Order order)
    {
        logger.LogInformation("Processing order {Id}", order.Id);
        await emailService.SendConfirmationAsync(order);
    }
}
```

### Properties

```csharp
public class Product
{
    // Auto-implemented property
    public string Name { get; set; }

    // Read-only auto-property
    public int Id { get; }

    // Init-only setter (C# 9.0) - settable only during initialization
    public string Sku { get; init; }

    // Computed property
    public decimal Price { get; set; }
    public decimal Tax => Price * 0.08m;
    public decimal TotalPrice => Price + Tax;

    // Property with backing field
    private string description;
    public string Description
    {
        get => description ?? "";
        set => description = value?.Trim();
    }

    // Property with validation
    private int quantity;
    public int Quantity
    {
        get => quantity;
        set
        {
            if (value < 0)
                throw new ArgumentOutOfRangeException(nameof(value));
            quantity = value;
        }
    }

    // Required property (C# 11)
    public required string Category { get; set; }
}

// Using init-only and required
var product = new Product
{
    Id = 1,           // Error: read-only
    Sku = "ABC123",   // OK: init-only
    Name = "Widget",
    Category = "Hardware"  // Required: must be set
};
```

### Object Initializers

```csharp
public class Address
{
    public string Street { get; set; }
    public string City { get; set; }
    public string PostalCode { get; set; }
    public string Country { get; set; } = "USA";
}

// Object initializer syntax
var address = new Address
{
    Street = "123 Main St",
    City = "Seattle",
    PostalCode = "98101"
    // Country uses default
};

// Nested object initializers
public class Customer
{
    public string Name { get; set; }
    public Address Address { get; set; } = new();
}

var customer = new Customer
{
    Name = "Alice",
    Address =
    {
        Street = "456 Oak Ave",
        City = "Portland"
    }
};

// Collection initializers
public class OrderList
{
    public List<string> Items { get; } = new();
}

var orderList = new OrderList
{
    Items = { "Item1", "Item2", "Item3" }
};
```

## Structs

Structs are value types allocated on the stack (when local) or inline (when in arrays or as fields). They're copied on assignment.

### Basic Struct

```csharp
public struct Point
{
    public double X { get; }
    public double Y { get; }

    public Point(double x, double y)
    {
        X = x;
        Y = y;
    }

    public double DistanceFromOrigin() =>
        Math.Sqrt(X * X + Y * Y);

    public Point Translate(double dx, double dy) =>
        new Point(X + dx, Y + dy);
}

// Value semantics
var p1 = new Point(3, 4);
var p2 = p1;  // Copy
// Modifying p2 doesn't affect p1
```

### Readonly Structs (C# 7.2)

Enforce immutability at compile time.

```csharp
public readonly struct Vector3
{
    public double X { get; }
    public double Y { get; }
    public double Z { get; }

    public Vector3(double x, double y, double z)
    {
        X = x;
        Y = y;
        Z = z;
    }

    // All methods must be readonly (implicit in readonly struct)
    public double Magnitude() =>
        Math.Sqrt(X * X + Y * Y + Z * Z);

    public Vector3 Normalize()
    {
        var mag = Magnitude();
        return new Vector3(X / mag, Y / mag, Z / mag);
    }

    // Operator overloading
    public static Vector3 operator +(Vector3 a, Vector3 b) =>
        new Vector3(a.X + b.X, a.Y + b.Y, a.Z + b.Z);
}
```

### Record Structs (C# 10)

Value types with record semantics.

```csharp
// Record struct - value type with value equality
public readonly record struct Coordinate(double Latitude, double Longitude);

var coord1 = new Coordinate(47.6062, -122.3321);
var coord2 = new Coordinate(47.6062, -122.3321);
Console.WriteLine(coord1 == coord2);  // true - value equality

// With expressions for non-destructive mutation
var coord3 = coord1 with { Longitude = -122.5 };
```

### Choosing Between Structs and Classes

The decision hinges on semantics, size, and identity.

**Use a struct when**:
- The type represents a single value (like a number or coordinate)
- Instances are small (16 bytes or less)
- The type is immutable (or should be)
- You're creating many short-lived instances in performance-critical code
- Identity doesn't matter—two instances with the same values should be considered equal

**Use a class when**:
- Identity matters—two objects with the same data are still distinct entities
- The type manages resources or has complex lifecycle
- Inheritance is needed
- The type has many fields or contains reference type fields
- Instances will be passed around extensively (avoiding copy overhead)

**Why 16 bytes matters**: Value types are copied on assignment and when passed to methods. A struct larger than 16 bytes often performs worse than a class because the copying overhead exceeds heap allocation cost. The runtime can also pass small structs in registers.

**Why identity matters**: A `Customer` with ID 42 is a specific entity. Even if you create another object with the same data, they represent different things conceptually. A `Point(3, 4)` is just a value, and any `Point(3, 4)` is interchangeable with any other.

| Factor | Struct | Class |
|--------|--------|-------|
| Size | Small (≤16 bytes ideal) | Any size |
| Semantics | Value (copy on assign) | Reference (share) |
| Mutability | Prefer immutable | Either |
| Inheritance | Cannot inherit | Can inherit |
| Allocation | Stack/inline | Heap |
| Nullability | Not null by default | Can be null |
| Use case | Coordinates, colors, small data | Entities, services, complex objects |

```csharp
// Good struct candidates
public readonly struct Color(byte R, byte G, byte B);
public readonly struct DateRange(DateTime Start, DateTime End);
public readonly struct Money(decimal Amount, string Currency);

// Should be classes
public class Customer { }     // Identity matters
public class OrderService { } // Has behavior/dependencies
public class FileStream { }   // Manages resources
```

## Records (C# 9.0+)

Records provide value-based equality and immutability by default.

### Record Classes

```csharp
// Positional record - generates constructor, properties, deconstruction
public record Person(string FirstName, string LastName);

var person1 = new Person("John", "Doe");
var person2 = new Person("John", "Doe");
Console.WriteLine(person1 == person2);  // true - value equality

// Deconstruction
var (first, last) = person1;

// With expression for non-destructive mutation
var person3 = person1 with { LastName = "Smith" };
// person1 unchanged, person3 is "John Smith"

// Record with additional members
public record Employee(string Name, string Department)
{
    public DateTime HireDate { get; init; }

    public int YearsEmployed =>
        (DateTime.Now - HireDate).Days / 365;
}

// Inheritance
public record Manager(string Name, string Department, int TeamSize)
    : Employee(Name, Department);
```

### Record Classes vs Record Structs

```csharp
// Record class (reference type)
public record Customer(int Id, string Name);

// Record struct (value type) - C# 10
public record struct Point(double X, double Y);

// Readonly record struct
public readonly record struct ImmutablePoint(double X, double Y);
```

| Feature | Record Class | Record Struct |
|---------|--------------|---------------|
| Type | Reference | Value |
| Inheritance | Yes | No |
| Null | Can be null | Not null |
| Allocation | Heap | Stack/inline |
| Default mutability | Immutable (init) | Mutable |
| With expressions | Yes | Yes |

## Sealed Classes

Prevent inheritance.

```csharp
public sealed class Configuration
{
    public string ConnectionString { get; init; }
    public int Timeout { get; init; }
}

// Cannot inherit from Configuration
// public class ExtendedConfig : Configuration { } // Error

// Sealing improves performance (enables devirtualization)
// Seal classes when inheritance isn't intended
```

## Abstract Classes

Cannot be instantiated; provide base for derived classes.

```csharp
public abstract class Shape
{
    public string Color { get; set; }

    // Abstract method - must be implemented
    public abstract double CalculateArea();

    // Virtual method - can be overridden
    public virtual void Draw()
    {
        Console.WriteLine($"Drawing {Color} shape");
    }

    // Regular method - inherited as-is
    public void Describe()
    {
        Console.WriteLine($"A {Color} shape with area {CalculateArea()}");
    }
}

public class Circle : Shape
{
    public double Radius { get; set; }

    public override double CalculateArea() =>
        Math.PI * Radius * Radius;

    public override void Draw()
    {
        base.Draw();  // Call base implementation
        Console.WriteLine($"Circle with radius {Radius}");
    }
}
```

## Partial Classes

Split a class across multiple files.

```csharp
// Customer.cs
public partial class Customer
{
    public int Id { get; set; }
    public string Name { get; set; }
}

// Customer.Validation.cs
public partial class Customer
{
    public bool IsValid() =>
        Id > 0 && !string.IsNullOrEmpty(Name);
}

// Customer.Persistence.cs (generated code often uses partial)
public partial class Customer
{
    public void Save() { /* ... */ }
}
```

## Static Classes

Cannot be instantiated; contain only static members.

```csharp
public static class MathHelper
{
    public const double Pi = 3.14159265358979;

    public static double Square(double x) => x * x;

    public static double Cube(double x) => x * x * x;

    public static bool IsEven(int n) => n % 2 == 0;
}

// Usage
double area = MathHelper.Pi * MathHelper.Square(radius);
```

## Nested Classes

Classes defined within other classes.

```csharp
public class LinkedList<T>
{
    private Node? head;

    public void Add(T value)
    {
        var newNode = new Node(value);
        newNode.Next = head;
        head = newNode;
    }

    // Private nested class - implementation detail
    private class Node
    {
        public T Value { get; }
        public Node? Next { get; set; }

        public Node(T value)
        {
            Value = value;
        }
    }
}

// Public nested class for related types
public class Order
{
    public List<LineItem> Items { get; } = new();

    public class LineItem
    {
        public string ProductName { get; set; }
        public int Quantity { get; set; }
        public decimal Price { get; set; }
    }
}

var item = new Order.LineItem { ProductName = "Widget" };
```

## Version History

| Feature | Version | Significance |
|---------|---------|--------------|
| Auto-properties | C# 3.0 | Simplified property syntax |
| Object initializers | C# 3.0 | Declarative object creation |
| Readonly structs | C# 7.2 | Enforced immutability |
| Init-only setters | C# 9.0 | Immutable after construction |
| Records | C# 9.0 | Value equality for reference types |
| Record structs | C# 10 | Value equality for value types |
| Required members | C# 11 | Enforced initialization |
| Primary constructors | C# 12 | Simplified class definitions |

## Key Takeaways

**Default to classes**: Use classes for most types. Use structs only for small, immutable value objects.

**Prefer immutability**: Use `init` setters, readonly structs, and records to create types that can't be accidentally modified.

**Use records for DTOs and value objects**: Records provide value equality, `with` expressions, and clean syntax for data-carrying types.

**Seal classes intentionally**: If a class isn't designed for inheritance, seal it. This documents intent and enables compiler optimizations.

**Keep structs small**: The copy-on-assignment semantics of structs make large structs expensive to pass around.
