---
layout: post
title: "Let the Results Speak for Themselves: Exceptions vs Result types"
date: 2025-10-29
description: "Evaluating arguments for Result types versus exceptions for handling expected failures in modern distributed C# systems, examining which claims have measurable backing and which are subjective preference."
series: "Architecture Insights"
tags: [error-handling, patterns, security, performance]
---

I prefer the clean code that exceptions produce. The happy path uncluttered by error handling, implicit propagation to appropriate layers, separation of concerns. It's aesthetically cleaner.

But when Rust's approach to error handling gained cultural influence and C# developers began exploring Result types through community libraries, I examined the question honestly: Do the arguments for Results hold up under scrutiny for expected failures in modern systems?

This isn't advocacy. It's critical analysis of the arguments from both camps, examining which ones have measurable backing and which are subjective preference.

## Choosing Between Results and Exceptions

When validating a payment request that might fail for multiple reasons (insufficient funds, expired card, fraud detection, network timeout), should your code:

```csharp
// Option 1: Throw exceptions
public PaymentConfirmation ProcessPayment(PaymentRequest request)
{
    ValidateRequest(request); // Throws ValidationException
    var charge = _paymentService.Charge(request); // Throws PaymentDeclinedException
    var confirmation = _repository.SaveTransaction(charge); // Throws DatabaseException
    return confirmation;
}

// Option 2: Return Results
public Result<PaymentConfirmation> ProcessPayment(PaymentRequest request)
{
    var validationResult = ValidateRequest(request);
    if (validationResult.IsFailure)
        return Result.Failure<PaymentConfirmation>(validationResult.Error);

    var chargeResult = _paymentService.Charge(request);
    if (chargeResult.IsFailure)
        return Result.Failure<PaymentConfirmation>(chargeResult.Error);

    var saveResult = _repository.SaveTransaction(chargeResult.Value);
    return saveResult; // Already Result<PaymentConfirmation>
}
```

This applies to all operations where failure is expected and valid: validation, business rules, external service calls, data persistence, network operations.

## What We're NOT Debating

Programming errors like null references or array index violations. Those are bugs that should crash during development, not states to handle in production.

## Why This Matters Now More Than Ever

The Result vs Exception debate has existed for decades. So why does it matter more now?

**Distributed systems made expected failures more frequent**. In monolithic applications, exceptions for validation or not-found scenarios were tolerable. In modern distributed systems with microservices and service meshes, expected failures happen constantly at scale: circuit breaker fallbacks, timeout retries, validation of user input, partial batch results. Treating these frequent outcomes as exceptions creates friction. Exceptions serialize across service boundaries as HTTP errors, generate stack traces for telemetry systems, and require try-catch blocks at every service call. Results are just data; they compose, serialize cleanly, and don't trigger observability overhead.

**Offline-first architecture became standard**. Progressive web apps, mobile applications, and desktop clients operate in environments where "no network" isn't exceptional - it's expected. Sync conflicts, partial data availability, and intermittent connectivity are normal operating conditions, not rare anomalies. These applications need error handling mechanisms designed for frequent expected states, not mechanisms optimized for rare exceptional cases.

**Observability systems make exception costs visible**. Every exception generates a stack trace that gets captured, stored, and transmitted through distributed tracing. At scale, exception-heavy architectures create measurable storage costs and noise in observability platforms. Results avoid this entirely.

**Functional architecture became standard**. Even OOP codebases now use stateless services, immutable data pipelines, and event-driven patterns. These are functional problems, and Results fit functional architectures better than exceptions, which were designed for imperative control flow.

### The Language Comparison

Both Rust and C# are pragmatic, multi-paradigm languages that evolved from different starting points.

**Rust** emerged with strong functional influences and a systems programming focus. It enforces a clear split - expected failures return `Result<T, E>` types (compiler-enforced handling), while unexpected failures trigger panics that unwind the stack like exceptions.

**C#** started heavily OOP-dominant and progressively adopted functional features (LINQ, pattern matching, immutability) to solve real problems. It historically used exceptions for all failures - both expected and unexpected.

Both ecosystems now support the same error handling split: Results for expected failures, exceptions or panics for programming errors.

In Rust, this is built-in and enforced. `Result<T, E>` types must be handled (compiler error if ignored), while panics are reserved for bugs.

In C#, this is now possible through pattern matching (C# 7+) and community Result libraries, but relies on discipline rather than compiler enforcement. Nothing stops you from ignoring a returned Result or using exceptions for expected failures.

Microsoft hasn't adopted Results officially. The Result pattern adoption is **community-driven** through library authors choosing this despite Microsoft's silence. Community libraries exist ([LanguageExt](https://github.com/louthy/language-ext){:target="_blank" rel="noopener noreferrer"} with 26M downloads, [FluentResults](https://github.com/altmann/FluentResults){:target="_blank" rel="noopener noreferrer"} with 3.3M downloads, [ErrorOr](https://github.com/amantinband/error-or){:target="_blank" rel="noopener noreferrer"}), but these aren't mainstream. Popular .NET libraries have hundreds of millions of downloads.

Still, when a pragmatic developer community independently moves toward patterns from another ecosystem, that's a signal worth examining.

## Arguments for Result Types

**Argument 1: Performance for frequent expected failures**

When cache misses, validation failures, and timeouts happen thousands of times per second, exception overhead creates degradation. Results are simple branches while exceptions require stack unwinding. Calling these failures "exceptional" doesn't change the performance characteristics.

**Strength**: Measurable at scale in systems with high-frequency expected failures.

**Argument 2: Information disclosure prevention by default**

Stack traces leak automatically unless actively prevented at every boundary. Results can't leak stack traces because there are no stack traces. Safe boundaries are the default, not something you must remember to enforce.

**Strength**: Security by default beats security through discipline.

**Argument 3: Type signatures as reliable documentation**

`Result<Order>` tells you immediately that getting an order can fail. `Order` tells you nothing without reading implementation or relying on potentially outdated XML comments. Refactoring tools update type signatures automatically; they don't update documentation.

**Strength**: Types can't lie about whether failure is possible.

**Argument 4: Natural composition for partial success and iteration**

Batch operations, parallel workflows, and offline sync scenarios often have partial success. Results compose naturally through filtering and mapping. In offline-first applications syncing local changes to servers, some records succeed while others fail due to conflicts or validation. This is expected behavior, not an exceptional case.

More critically: **exceptions force iteration at the wrong layer**. When processing a collection where some items might fail, you must iterate at the orchestration layer (where you can catch exceptions) even if iteration logically belongs in the service layer.

```csharp
// Exception approach - iteration forced into controller
public async Task ProcessOrders(List<string> orderIds)
{
    foreach (var id in orderIds) // Must iterate here
    {
        try { await _orderService.Process(id); }
        catch (Exception ex) { /* handle */ }
    }
}

// Result approach - iteration lives in service layer
public async Task<List<Result<Order>>> ProcessAll(List<string> orderIds)
{
    var tasks = orderIds.Select(id => Process(id));
    return await Task.WhenAll(tasks); // Parallel, natural
}
```

With parallel processing, `Task.WhenAll` with exceptions is awkward because one exception fails the entire batch. `Task.WhenAll` with Results naturally preserves all outcomes.

**Strength**: Results allow iteration and parallelism at appropriate abstraction levels.

## Arguments for Exceptions

**Argument 1: Implicit propagation to appropriate handlers**

Exceptions bubble to orchestration layers without code at each level. Throw once, catch at the boundary. The happy path stays clean; error handling lives at boundaries.

Results require explicit propagation. Return `Result<T>`, check it, propagate it. This threads error handling through intermediate functions that don't care about the specific error.

**Strength**: Separation of concerns. Domain logic stays focused on domain, not error threading.

**Argument 2: Framework integration without friction**

The .NET ecosystem uses exceptions. Entity Framework throws `DbUpdateException`. HttpClient throws `HttpRequestException`. Wrapping every framework call in try-catch to convert to Results creates boilerplate at every boundary.

**Strength**: Working with the ecosystem, not against it.

**Argument 3: C# doesn't enforce Result handling**

Unlike Rust where ignoring a `Result` is a compiler error, C# lets you completely ignore returned Results. You can access `.Value` without checking `.IsSuccess` and get runtime exceptions anyway.

```csharp
public Result<Order> GetOrder(string id) { /* ... */ }

GetOrder("123"); // Completely ignored, no compiler error
```

The "compiler safety" argument assumes static analyzers and discipline; the same discipline proper exception handling requires.

**Strength**: Results in C# provide discoverability, not enforcement.

**Argument 4: Orchestration layers solve the same problems**

Proper architecture already requires orchestration layers that catch domain exceptions, translate them to appropriate responses, and control what information crosses boundaries. These layers also make consistent logging decisions. Results don't eliminate the need for this architecture; they just change what propagates upward.

**Strength**: Architecture matters more than mechanism.

**Argument 5: Exception documentation is sufficient with discipline**

XML comments document exceptions, appear in IntelliSense, and provide discoverability at call sites:

```csharp
/// <exception cref="OrderNotFoundException">When the order doesn't exist</exception>
public Order GetOrder(string id)
```

Well-maintained codebases keep documentation current through code reviews. If you have discipline to maintain exception documentation, you have discipline to handle Results properly.

**Strength**: Documentation works if teams maintain it.

**Argument 6: Results encourage scattered error handling**

Making it syntactically easy to handle errors inline encourages developers to scatter error-handling logic across call sites instead of centralizing it in orchestration layers. The path of least resistance becomes handling each Result immediately rather than propagating it to appropriate boundaries.

**Strength**: Results can create worse maintainability if misused.

## Which Arguments Hold Up?

**Result arguments that stand:**
- Performance impact is measurable and matters at scale
- Information leakage is default behavior with exceptions, requires prevention with Results
- Type signatures are more reliable than documentation for indicating failure
- Iteration and parallelism can live at appropriate abstraction levels

**Result arguments that weaken:**
- Good architecture required either way (orchestration layers needed for both approaches)
- Scattered error handling risk remains (centralizing error logic is a discipline issue for both)

**Exception arguments that stand:**
- Implicit propagation reduces boilerplate in intermediate layers
- Framework integration is smoother without constant translation
- Orchestration layers remain valuable for consolidating error handling decisions for both Results and exceptions

**Exception arguments that weaken:**
- Documentation requires discipline to maintain (documentation rots in practice)
- Clean happy-path code hides what can fail (invisible failure modes in method signatures)
- Performance overhead is real even if labeled "exceptional" (definitions don't change costs)

## What the Evidence Says

The arguments that favor Results are structural, not cultural. When 30-40% of operations fail expectedly (cache misses, validation), treating these as exceptions creates measurable overhead at scale. Information disclosure through stack traces is default behavior with exceptions and requires active prevention. Type signatures (`Result<Order>`) are more reliable than documentation because XML comments rot. Iteration and parallelism work naturally with Results but require awkward patterns with exceptions.

The exception camp's strongest argument is implicit propagation. Exceptions bubble naturally while Results require explicit threading through intermediate layers. This is real convenience, but it comes at a cost of invisible failure modes. When a method returns `Order`, the signature doesn't reveal whether it throws, what it throws, or why.

The concerns about Results are valid: C# doesn't enforce handling, scattered error logic is possible, and framework integration creates friction. But these are execution risks, not structural flaws. With discipline and static analyzers, Results provide better defaults for high-frequency expected failures.

Use Results for domain operations (validation, business rules, service calls) and exceptions for programming errors (null references, contract violations). Framework exceptions can still be handled by orchestration layers. Use `Task.WhenAll` with Results for parallel operations. Centralize error handling decisions in orchestration layers that handle both Results and framework exceptions.

## Why the Resistance?

If structural arguments favor Results, why does the exception camp remain strong?

**Paradigm friction** explains part of the resistance. OOP treats errors as exceptional control flow that interrupts normal execution. Functional programming treats errors as data, another value to transform. C# developers gravitating toward exceptions reflects paradigm alignment, not just familiarity. But modern distributed systems are functional problems (stateless services, data pipelines), even when written in OOP languages. Results fit these architectures better.

**The Frozen Caveman pattern** also contributes: "Exceptions work if done correctly, and I've learned how to do them correctly." This solves yesterday's problem (poor exception handling) rather than today's problem. When 30-40% of operations return expected failures (distributed system timeouts, offline-first sync conflicts, parallel batch processing), exceptions require working around their design, not just using them correctly.

## Where the Evidence Points

I started preferring exceptions. The evidence led me to Results for domain operations. Not because Results are perfect (C# doesn't enforce them, they create framework friction, and misuse can scatter error handling), but because the structural advantages outweigh the execution risks. Performance at scale, safe boundaries by default, visible failure modes, and natural iteration patterns matter more than implicit propagation convenience.

The resistance is understandable. Paradigm friction is real, and "do exceptions correctly this time" reflects discipline. But when 30-40% of operations return expected failures, you need mechanisms designed for common outcomes, not rare anomalies.

Use Results for expected failures. Reserve exceptions for bugs. Build the discipline and tooling to use them well.
