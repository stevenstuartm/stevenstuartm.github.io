---
title: "OOP Quick Reference"
category: Object-Oriented Programming
---

---

## When to Use Each Pattern

**Creational (5 patterns)**
- **Factory Method**: Multiple ways to create objects
- **Abstract Factory**: Families of related objects
- **Builder**: Complex object construction
- **Prototype**: Object cloning
- **Singleton**: Shared resources (use DI instead)

**Structural (7 patterns)**
- **Adapter**: Interface compatibility
- **Bridge**: Separate abstraction from implementation
- **Composite**: Tree structures
- **Decorator**: Dynamic behavior addition
- **Facade**: Simplify complex subsystems
- **Flyweight**: Memory optimization through sharing
- **Proxy**: Control object access

**Behavioral (11 patterns)**
- **Chain of Responsibility**: Request handling chain
- **Command**: Action encapsulation
- **Interpreter**: Language processing
- **Iterator**: Collection traversal
- **Mediator**: Object communication
- **Memento**: State capture and restore
- **Observer**: Event notifications
- **State**: Behavior changes with state
- **Strategy**: Algorithm selection
- **Template Method**: Algorithm skeleton
- **Visitor**: Operations on object hierarchies

## Common Anti-Patterns to Avoid

- **God Object**: Classes that do too much
- **Spaghetti Code**: Tangled dependencies
- **Tight Coupling**: Direct dependencies instead of abstractions
- **Premature Optimization**: Complex patterns without justification
- **Pattern Overuse**: Using patterns where simple code suffices

## Modern Framework Integration

**ASP.NET Core**: Extensive use of dependency injection, middleware (decorator), and options pattern
**Entity Framework**: Unit of work, repository, and lazy loading (proxy) patterns
**SignalR**: Observer pattern for real-time communication
**MediatR**: Command and mediator patterns for CQRS

---

> **Remember**: Patterns are tools, not goals. Use them to solve specific problems, not because they exist. Modern development emphasizes simplicity, testability, and maintainability over pattern implementation.

---