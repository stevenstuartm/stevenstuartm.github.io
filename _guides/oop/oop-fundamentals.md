---
title: "OOP Fundamentals"
category: Object-Oriented Programming
---

---

## Core OOP Pillars

**Abstraction**
- Hide complex implementation details while exposing a simple interface
- Focus on what an object does rather than how it does it
- Use abstract classes and interfaces to define contracts

**Encapsulation**
- Bundle data and methods that operate on that data within a single unit
- Control access through visibility modifiers (private, protected, public)
- Protect internal state from external interference

**Inheritance**
- Create new classes based on existing classes
- Enables code reuse and establishes "is-a" relationships
- Use composition over inheritance when possible (modern best practice)

**Polymorphism**
- Objects of different types can be treated as instances of the same type
- Method overriding enables runtime behavior selection
- Interfaces enable compile-time polymorphism

## Key Concepts

**Covariance**
- Use a more derived type than originally specified
- Example: `IEnumerable<Derived>` can be assigned to `IEnumerable<Base>`

**Contravariance**
- Use a more generic type than originally specified
- Example: `Action<Base>` can be assigned to `Action<Derived>`

**Invariance**
- Use only the originally specified type
- Example: `List<Base>` cannot be assigned to `List<Derived>` or vice versa

---