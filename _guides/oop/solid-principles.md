---
title: "SOLID Principles"
category: Object-Oriented Programming
---

---

> **SOLID** principles create maintainable, scalable, and flexible software systems that are easier to understand, modify, and extend over time.

## S - Single Responsibility Principle (SRP)

**Definition**: A class should have only one reason to change, meaning it should have only one job or responsibility.

**Benefits**:
- Easier to test and maintain
- Reduces coupling between components
- Simplifies debugging and troubleshooting

**Example Violation**:
```csharp
// BAD: Multiple responsibilities
public class Employee
{
    public void CalculateSalary() { /* salary logic */ }
    public void GeneratePayrollReport() { /* reporting logic */ }
    public void SaveToDatabase() { /* persistence logic */ }
}
```

**Better Approach**:
```csharp
// GOOD: Single responsibilities
public class Employee { /* employee data only */ }
public class SalaryCalculator { /* salary logic */ }
public class PayrollReporter { /* reporting logic */ }
public class EmployeeRepository { /* persistence logic */ }
```

## O - Open-Closed Principle (OCP)

**Definition**: Software entities should be open for extension but closed for modification.

**Benefits**:
- Add new features without changing existing code
- Reduces risk of introducing bugs in working code
- Promotes code reusability

**Implementation**: Use abstractions, interfaces, and inheritance to enable extension points.

## L - Liskov Substitution Principle (LSP)

**Definition**: Objects of a superclass should be replaceable with objects of a subclass without altering the correctness of the program.

**Benefits**:
- Ensures polymorphism works correctly
- Maintains contract integrity
- Enables reliable inheritance hierarchies

**Key Rule**: Subclasses must strengthen postconditions and weaken preconditions.

## I - Interface Segregation Principle (ISP)

**Definition**: Clients should not be forced to depend on interfaces they don't use.

**Benefits**:
- Reduces coupling between components
- Avoids unnecessary dependencies
- Enables more targeted implementations

**Modern Examples**:
- **Specification Pattern**: `ISpecification<T>` with `bool IsSatisfied(T item)`
- **Extension Methods**: Add functionality without modifying existing interfaces
- **Small, Focused Interfaces**: Prefer multiple specific interfaces over large general ones

## D - Dependency Inversion Principle (DIP)

**Definition**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

**Benefits**:
- Improves testability through dependency injection
- Reduces coupling between layers
- Enables flexible architecture

**Implementation**: Use dependency injection containers and inversion of control (IoC).

---