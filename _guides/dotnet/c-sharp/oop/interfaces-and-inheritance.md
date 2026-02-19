---
title: "C# Interfaces and Inheritance"
layout: guide
category: ".NET & C#"
subcategory: "Object-Oriented Programming"
description: "Interfaces, inheritance hierarchies, polymorphism, and default interface implementations in modern C#."
tags: [c-sharp, dotnet, oop, interfaces, inheritance, polymorphism, practical]
---

## Interfaces

Interfaces define contracts that types can implement. They specify what a type can do, not how it does it.

### Basic Interface Definition

```csharp
public interface IRepository<T> where T : class
{
    T? GetById(int id);
    IEnumerable<T> GetAll();
    void Add(T entity);
    void Update(T entity);
    void Delete(int id);
}

public interface IEmailService
{
    Task SendAsync(string to, string subject, string body);
    Task SendBulkAsync(IEnumerable<string> recipients, string subject, string body);
}
```

### Implementing Interfaces

```csharp
public class CustomerRepository : IRepository<Customer>
{
    private readonly DbContext context;

    public CustomerRepository(DbContext context)
    {
        this.context = context;
    }

    public Customer? GetById(int id) =>
        context.Customers.Find(id);

    public IEnumerable<Customer> GetAll() =>
        context.Customers.ToList();

    public void Add(Customer entity) =>
        context.Customers.Add(entity);

    public void Update(Customer entity) =>
        context.Customers.Update(entity);

    public void Delete(int id)
    {
        var entity = GetById(id);
        if (entity != null)
            context.Customers.Remove(entity);
    }
}
```

### Multiple Interface Implementation

```csharp
public interface IComparable<T>
{
    int CompareTo(T other);
}

public interface IEquatable<T>
{
    bool Equals(T other);
}

public interface IFormattable
{
    string ToString(string format, IFormatProvider formatProvider);
}

public class Money : IComparable<Money>, IEquatable<Money>, IFormattable
{
    public decimal Amount { get; }
    public string Currency { get; }

    public Money(decimal amount, string currency)
    {
        Amount = amount;
        Currency = currency;
    }

    public int CompareTo(Money? other)
    {
        if (other is null) return 1;
        if (Currency != other.Currency)
            throw new InvalidOperationException("Cannot compare different currencies");
        return Amount.CompareTo(other.Amount);
    }

    public bool Equals(Money? other) =>
        other is not null &&
        Amount == other.Amount &&
        Currency == other.Currency;

    public string ToString(string? format, IFormatProvider? formatProvider)
    {
        return format switch
        {
            "C" => $"{Currency} {Amount:N2}",
            "S" => $"{Amount:N2}",
            _ => $"{Amount} {Currency}"
        };
    }
}
```

### Explicit Interface Implementation

When two interfaces have conflicting members, or you want to hide interface members from the class's public API.

```csharp
public interface IDrawable
{
    void Draw();
}

public interface IPrintable
{
    void Draw(); // Same name, different meaning
}

public class Document : IDrawable, IPrintable
{
    // Explicit implementation - only accessible through interface
    void IDrawable.Draw()
    {
        Console.WriteLine("Drawing to screen");
    }

    void IPrintable.Draw()
    {
        Console.WriteLine("Drawing to printer");
    }

    // Public method available on the class itself
    public void Display()
    {
        Console.WriteLine("Displaying document");
    }
}

// Usage
var doc = new Document();
doc.Display();           // OK
// doc.Draw();           // Error - not accessible directly

IDrawable drawable = doc;
drawable.Draw();         // "Drawing to screen"

IPrintable printable = doc;
printable.Draw();        // "Drawing to printer"
```

### Default Interface Methods (C# 8.0)

Add methods with implementations to interfaces without breaking existing implementers.

```csharp
public interface ILogger
{
    void Log(string message);

    // Default implementation - existing implementers don't break
    void LogWarning(string message) =>
        Log($"WARNING: {message}");

    void LogError(string message) =>
        Log($"ERROR: {message}");

    void LogError(Exception ex) =>
        LogError($"{ex.GetType().Name}: {ex.Message}");
}

public class ConsoleLogger : ILogger
{
    public void Log(string message) =>
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] {message}");

    // Can override default implementations
    public void LogError(string message)
    {
        Console.ForegroundColor = ConsoleColor.Red;
        Log($"ERROR: {message}");
        Console.ResetColor();
    }
}

// Usage
ILogger logger = new ConsoleLogger();
logger.Log("Info");           // Custom implementation
logger.LogWarning("Careful"); // Default implementation
logger.LogError("Oops");      // Overridden implementation
```

### Static Abstract Members (C# 11)

Define static members in interfaces for generic math and factory patterns.

```csharp
public interface IAddable<T> where T : IAddable<T>
{
    static abstract T operator +(T left, T right);
    static abstract T Zero { get; }
}

public readonly struct Fraction : IAddable<Fraction>
{
    public int Numerator { get; }
    public int Denominator { get; }

    public Fraction(int numerator, int denominator)
    {
        Numerator = numerator;
        Denominator = denominator;
    }

    public static Fraction Zero => new(0, 1);

    public static Fraction operator +(Fraction left, Fraction right) =>
        new(
            left.Numerator * right.Denominator + right.Numerator * left.Denominator,
            left.Denominator * right.Denominator);
}

// Generic method using static interface members
public static T Sum<T>(IEnumerable<T> values) where T : IAddable<T>
{
    T result = T.Zero;
    foreach (var value in values)
    {
        result = result + value;
    }
    return result;
}
```

## Inheritance

### Basic Inheritance

```csharp
public class Animal
{
    public string Name { get; set; }

    public virtual void Speak()
    {
        Console.WriteLine("Some sound");
    }

    public void Eat()
    {
        Console.WriteLine($"{Name} is eating");
    }
}

public class Dog : Animal
{
    public string Breed { get; set; }

    public override void Speak()
    {
        Console.WriteLine("Woof!");
    }

    public void Fetch()
    {
        Console.WriteLine($"{Name} is fetching");
    }
}

public class Cat : Animal
{
    public override void Speak()
    {
        Console.WriteLine("Meow!");
    }
}
```

### Virtual, Override, and New

```csharp
public class BaseClass
{
    public virtual void VirtualMethod()
    {
        Console.WriteLine("Base virtual");
    }

    public void NonVirtualMethod()
    {
        Console.WriteLine("Base non-virtual");
    }
}

public class DerivedClass : BaseClass
{
    // Override - replaces base implementation polymorphically
    public override void VirtualMethod()
    {
        Console.WriteLine("Derived override");
    }

    // New - hides base member (not polymorphic)
    public new void NonVirtualMethod()
    {
        Console.WriteLine("Derived new");
    }
}

// Demonstration
BaseClass b = new DerivedClass();
b.VirtualMethod();    // "Derived override" (polymorphic)
b.NonVirtualMethod(); // "Base non-virtual" (hidden, not replaced)

DerivedClass d = new DerivedClass();
d.VirtualMethod();    // "Derived override"
d.NonVirtualMethod(); // "Derived new"
```

### Abstract Classes and Methods

```csharp
public abstract class Shape
{
    public string Color { get; set; }

    // Abstract - must be implemented by derived class
    public abstract double Area { get; }
    public abstract double Perimeter { get; }

    // Virtual - can be overridden
    public virtual void Draw()
    {
        Console.WriteLine($"Drawing {Color} shape");
    }

    // Regular - inherited as-is
    public void Describe()
    {
        Console.WriteLine($"{Color} shape: Area={Area:F2}, Perimeter={Perimeter:F2}");
    }
}

public class Rectangle : Shape
{
    public double Width { get; set; }
    public double Height { get; set; }

    public override double Area => Width * Height;
    public override double Perimeter => 2 * (Width + Height);
}

public class Circle : Shape
{
    public double Radius { get; set; }

    public override double Area => Math.PI * Radius * Radius;
    public override double Perimeter => 2 * Math.PI * Radius;

    public override void Draw()
    {
        base.Draw(); // Call base implementation
        Console.WriteLine($"Circle with radius {Radius}");
    }
}
```

### Sealed Methods and Classes

```csharp
public class Animal
{
    public virtual void Move() { }
}

public class Bird : Animal
{
    // Seal to prevent further overriding
    public sealed override void Move()
    {
        Console.WriteLine("Flying");
    }
}

public class Penguin : Bird
{
    // Error: cannot override sealed method
    // public override void Move() { }
}

// Sealed class - cannot be inherited
public sealed class String { }
```

### Constructor Chaining

```csharp
public class Person
{
    public string Name { get; }
    public int Age { get; }

    public Person(string name) : this(name, 0) { }

    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
}

public class Employee : Person
{
    public string Department { get; }

    // Call base constructor
    public Employee(string name, string department)
        : base(name)
    {
        Department = department;
    }

    public Employee(string name, int age, string department)
        : base(name, age)
    {
        Department = department;
    }
}
```

## Polymorphism

### Runtime Polymorphism

```csharp
public abstract class PaymentProcessor
{
    public abstract Task<bool> ProcessAsync(decimal amount);
    public abstract decimal CalculateFee(decimal amount);
}

public class CreditCardProcessor : PaymentProcessor
{
    public override async Task<bool> ProcessAsync(decimal amount)
    {
        // Credit card processing logic
        await Task.Delay(100);
        return true;
    }

    public override decimal CalculateFee(decimal amount) =>
        amount * 0.029m + 0.30m; // 2.9% + $0.30
}

public class BankTransferProcessor : PaymentProcessor
{
    public override async Task<bool> ProcessAsync(decimal amount)
    {
        // Bank transfer processing logic
        await Task.Delay(200);
        return true;
    }

    public override decimal CalculateFee(decimal amount) =>
        Math.Min(amount * 0.01m, 5.00m); // 1% max $5
}

// Polymorphic usage
public class PaymentService
{
    public async Task<bool> ProcessPayment(
        PaymentProcessor processor,
        decimal amount)
    {
        decimal fee = processor.CalculateFee(amount);
        decimal total = amount + fee;
        return await processor.ProcessAsync(total);
    }
}
```

### Interface-Based Polymorphism

Prefer interfaces over inheritance for polymorphism.

```csharp
public interface INotificationSender
{
    Task SendAsync(string recipient, string message);
}

public class EmailSender : INotificationSender
{
    public async Task SendAsync(string recipient, string message)
    {
        // Send email
        await Task.CompletedTask;
    }
}

public class SmsSender : INotificationSender
{
    public async Task SendAsync(string recipient, string message)
    {
        // Send SMS
        await Task.CompletedTask;
    }
}

public class PushNotificationSender : INotificationSender
{
    public async Task SendAsync(string recipient, string message)
    {
        // Send push notification
        await Task.CompletedTask;
    }
}

// Polymorphic usage
public class NotificationService
{
    private readonly IEnumerable<INotificationSender> senders;

    public NotificationService(IEnumerable<INotificationSender> senders)
    {
        this.senders = senders;
    }

    public async Task NotifyAllAsync(string recipient, string message)
    {
        var tasks = senders.Select(s => s.SendAsync(recipient, message));
        await Task.WhenAll(tasks);
    }
}
```

## Choosing Between Interfaces and Abstract Classes

Both define contracts, but they serve different purposes.

**Use an interface when**:
- Multiple unrelated types need to share a capability (like `IDisposable`, `IComparable`)
- You want a type to support multiple contracts (a class can implement many interfaces)
- The contract is purely about behavior, not about shared implementation
- You want to enable dependency injection and testability

**Use an abstract class when**:
- Types share both behavior AND implementation
- You need to define state (fields) that derived classes inherit
- You want to provide a partial implementation as a starting point
- The relationship is truly "is-a" (a Dog IS an Animal)

**Why this matters**: Inheritance creates tight coupling. When you inherit from a class, you take on its implementation details and any changes to the base class can break derived classes. Interfaces are pure contracts; implementing `IComparable` doesn't tie you to any specific implementation.

**Common pattern**: Use an interface for the public contract and an abstract class for shared implementation among related types.

```csharp
// Interface for the contract
public interface IPaymentProcessor
{
    Task<PaymentResult> ProcessAsync(Payment payment);
}

// Abstract class for shared implementation among similar processors
public abstract class BasePaymentProcessor : IPaymentProcessor
{
    protected abstract string ProviderName { get; }

    public async Task<PaymentResult> ProcessAsync(Payment payment)
    {
        ValidatePayment(payment); // Shared logic
        return await ProcessWithProviderAsync(payment); // Provider-specific
    }

    protected abstract Task<PaymentResult> ProcessWithProviderAsync(Payment payment);

    protected virtual void ValidatePayment(Payment payment)
    {
        // Shared validation logic
    }
}
```

## Composition Over Inheritance

Favor object composition for code reuse.

```csharp
// Inheritance approach - tight coupling
public class LoggingRepository<T> : Repository<T>
{
    private readonly ILogger logger;

    protected override void Add(T entity)
    {
        logger.Log($"Adding {typeof(T).Name}");
        base.Add(entity);
    }
}

// Composition approach - flexible
public class Repository<T>
{
    private readonly IDataStore<T> dataStore;
    private readonly ILogger? logger;

    public Repository(IDataStore<T> dataStore, ILogger? logger = null)
    {
        this.dataStore = dataStore;
        this.logger = logger;
    }

    public void Add(T entity)
    {
        logger?.Log($"Adding {typeof(T).Name}");
        dataStore.Save(entity);
    }
}

// Decorator pattern for cross-cutting concerns
public class LoggingRepositoryDecorator<T> : IRepository<T>
{
    private readonly IRepository<T> inner;
    private readonly ILogger logger;

    public LoggingRepositoryDecorator(IRepository<T> inner, ILogger logger)
    {
        this.inner = inner;
        this.logger = logger;
    }

    public void Add(T entity)
    {
        logger.Log($"Adding {typeof(T).Name}");
        inner.Add(entity);
    }

    // Delegate other methods...
}
```

## Type Checking and Casting

```csharp
object obj = GetSomething();

// Type checking with pattern matching
if (obj is string text)
{
    Console.WriteLine(text.ToUpper());
}

// Multiple type patterns
string result = obj switch
{
    string s => s.ToUpper(),
    int i => i.ToString(),
    null => "null",
    _ => obj.ToString() ?? ""
};

// is with negation
if (obj is not null)
{
    Console.WriteLine(obj.ToString());
}

// as operator (returns null if cast fails)
var customer = obj as Customer;
if (customer != null)
{
    customer.ProcessOrder();
}
```

## Covariance and Contravariance

```csharp
// Covariance (out) - can use derived where base is expected
public interface IReadOnlyRepository<out T>
{
    T GetById(int id);
    IEnumerable<T> GetAll();
}

// Can assign IReadOnlyRepository<Dog> to IReadOnlyRepository<Animal>
IReadOnlyRepository<Animal> animals = new AnimalRepository();
IReadOnlyRepository<Animal> dogs = new DogRepository(); // Covariant

// Contravariance (in) - can use base where derived is expected
public interface IComparer<in T>
{
    int Compare(T x, T y);
}

// Can use IComparer<Animal> where IComparer<Dog> expected
IComparer<Animal> animalComparer = new AnimalComparer();
IComparer<Dog> dogComparer = animalComparer; // Contravariant
```
## Key Takeaways

**Program to interfaces, not implementations**: Define behavior through interfaces and inject dependencies.

**Favor composition over inheritance**: Inheritance creates tight coupling. Use composition and delegation for flexibility.

**Keep inheritance hierarchies shallow**: Deep hierarchies become hard to understand and maintain.

**Use sealed by default**: Unless a class is designed for inheritance, seal it to communicate intent and enable optimizations.

**Default interface methods for evolution**: Add new members to interfaces with default implementations to avoid breaking existing implementers.

**Explicit implementation for conflicts**: When interface members conflict or shouldn't be part of the public API, use explicit implementation.
