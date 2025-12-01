---
title: "Compilation and Runtime"
layout: guide
category: ".NET & C#"
subcategory: "Foundations"
description: "How .NET compiles and executes code: IL, JIT, AOT, tiered compilation, trimming, and deployment models"
tags: [dotnet, compilation, jit, aot, clr, runtime, performance, deployment, fundamentals]
---

Understanding how .NET compiles and runs code helps you make informed decisions about performance, deployment, and compatibility. This guide covers the compilation pipeline from source code to execution, including the tradeoffs between different compilation strategies.

## The .NET Compilation Pipeline

<blockquote class="pull-quote">
<p>The two-stage compilation model (C# to IL, then IL to native code) is what enables .NET's cross-platform portability and runtime optimization capabilities.</p>
</blockquote>

When you build a C# project, the compiler does not produce machine code directly. Instead, it produces an intermediate representation that the runtime later converts to native code. This two-stage process enables cross-platform compatibility and runtime optimizations.

```
C# Source → C# Compiler → IL + Metadata (Assembly) → Runtime → Native Code → Execution
```

### Intermediate Language (IL)

The C# compiler produces **Intermediate Language** (IL), also called MSIL or CIL. IL is a CPU-independent instruction set that describes operations at a higher level than machine code but lower than C#.

An assembly (`.dll` or `.exe`) contains IL bytecode plus metadata describing types, methods, and references. This metadata enables reflection, debugging, and cross-language interoperability.

IL has several advantages over compiling directly to machine code:

- **Platform independence**: The same assembly runs on Windows, Linux, and macOS
- **Runtime optimization**: The JIT compiler can optimize for the specific CPU running the code
- **Security verification**: The runtime can verify IL is type-safe before execution
- **Reflection**: Metadata enables runtime type inspection

You can examine IL using tools like `ildasm` (IL Disassembler) or ILSpy. Understanding IL helps when debugging performance issues or understanding what the compiler actually generates.

### The Common Language Runtime (CLR)

The **Common Language Runtime** is the execution engine that runs .NET code. It provides:

- **Memory management**: Garbage collection, stack allocation, object layout
- **Type safety**: Verifies IL before execution, enforces type rules
- **Exception handling**: Structured exception propagation across method boundaries
- **Security**: Code access security, stack walking for permission checks
- **JIT compilation**: Converts IL to native code at runtime
- **Interop**: Marshalling between managed and unmanaged code

The CLR abstracts the underlying operating system, providing a consistent execution environment across platforms. CoreCLR is the runtime used by modern .NET (5+), while the legacy .NET Framework uses a different CLR implementation.

## Just-In-Time (JIT) Compilation

**JIT compilation** converts IL to native machine code at runtime, just before execution. When a method is first called, the JIT compiler translates its IL to native instructions for the current CPU.

### How JIT Works

1. Application starts; CLR loads assemblies
2. First call to a method triggers JIT compilation
3. JIT analyzes the IL and generates optimized native code
4. Native code is cached in memory for subsequent calls
5. Future calls execute the cached native code directly

The JIT compiler has access to runtime information unavailable at build time: the exact CPU model, available instruction sets (AVX, SSE), and actual runtime behavior. This enables optimizations that ahead-of-time compilers cannot perform.

<div class="comparison">
<div class="content-card content-card--accent">
<h4>JIT Advantages</h4>
<ul>
<li>Optimizes for the exact hardware running the code</li>
<li>Can inline methods based on actual runtime types</li>
<li>No need to ship platform-specific binaries</li>
<li>Enables dynamic code generation and reflection</li>
</ul>
</div>
<div class="content-card content-card--accent-secondary">
<h4>JIT Disadvantages</h4>
<ul>
<li>Startup cost: first execution of each method incurs compilation time</li>
<li>Memory overhead: native code cache consumes RAM</li>
<li>Cannot optimize across assembly boundaries in some cases</li>
</ul>
</div>
</div>

For long-running applications like web servers, JIT startup cost is amortized over many requests. For short-lived processes like CLI tools, startup time dominates total execution time.

### Tiered Compilation

Modern .NET uses **tiered compilation** to balance startup speed with steady-state performance. Methods compile in stages:

**Tier 0 (Quick JIT)**: Fast compilation with minimal optimization. Gets code running quickly. Methods are instrumented to track call frequency.

**Tier 1 (Optimizing JIT)**: After a method is called enough times (typically 30 calls or 30 iterations of a loop), it recompiles with full optimizations. The optimized version replaces the tier 0 code.

This approach provides fast startup (tier 0) while eventually achieving peak performance (tier 1) for hot paths. Cold code that runs rarely never pays the cost of aggressive optimization.

You can observe tiered compilation through diagnostics:

```csharp
// Environment variable to see JIT events
// DOTNET_JitDisasm=MethodName
// Shows disassembly when methods are JIT compiled
```

Tiered compilation is enabled by default. For benchmarking, you may want to disable it to measure steady-state performance consistently:

```xml
<PropertyGroup>
  <TieredCompilation>false</TieredCompilation>
</PropertyGroup>
```

## Ahead-of-Time (AOT) Compilation

**AOT compilation** generates native code at build time rather than runtime. The published application contains machine code directly, eliminating JIT compilation at startup.

### Why AOT Matters

AOT addresses specific scenarios where JIT compilation is problematic:

**Startup time**: Applications start faster because no JIT compilation occurs. This matters for serverless functions, CLI tools, and mobile apps.

**Deployment size**: AOT enables aggressive trimming since the compiler knows exactly what code is reachable at build time.

**Platforms without JIT**: iOS prohibits JIT compilation for security reasons. Game consoles and some embedded systems have similar restrictions.

**Predictable performance**: No JIT compilation pauses during execution. Latency-sensitive applications benefit from consistent timing.

### Native AOT in .NET

.NET 7+ provides **Native AOT** publishing, which produces a fully native executable with no IL and no JIT:

```xml
<PropertyGroup>
  <PublishAot>true</PublishAot>
</PropertyGroup>
```

```bash
dotnet publish -c Release
```

The output is a single native executable for the target platform. No .NET runtime installation is required on the target machine.

<div class="callout callout--warning">
<p class="callout__title">AOT Limitations</p>
<p>Native AOT imposes constraints because the compiler must know the complete program at build time:</p>
<ul>
<li><strong>No dynamic code generation</strong>: <code>Reflection.Emit</code>, <code>Expression.Compile()</code>, and similar APIs that generate code at runtime do not work.</li>
<li><strong>Limited reflection</strong>: Reflection that relies on runtime metadata discovery may fail. Types and members must be statically reachable or explicitly preserved.</li>
<li><strong>No dynamic assembly loading</strong>: <code>Assembly.LoadFrom()</code> and similar APIs cannot load arbitrary assemblies at runtime.</li>
<li><strong>Platform-specific output</strong>: Each target platform requires a separate build. You cannot build once and run everywhere.</li>
</ul>
</div>

These limitations require using source generators instead of reflection for serialization, dependency injection, and similar concerns. The [Source Generators](source-generators.html) guide covers this topic in detail.

### ReadyToRun (R2R)

**ReadyToRun** is a hybrid approach: assemblies contain both IL and precompiled native code. At runtime, the precompiled code runs immediately while the JIT can still recompile hot methods with better optimizations.

```xml
<PropertyGroup>
  <PublishReadyToRun>true</PublishReadyToRun>
</PropertyGroup>
```

R2R provides faster startup than pure JIT without the restrictions of full AOT:
- Reflection works normally
- Dynamic code generation works
- Cross-platform IL remains available

The tradeoff is larger deployment size (both IL and native code) and less aggressive optimization than either pure JIT or pure AOT.

## Trimming

**Trimming** removes unused code from published applications, reducing deployment size. The trimmer analyzes the application to determine which types and methods are reachable, then excludes everything else.

### How Trimming Works

The trimmer performs static analysis starting from entry points:

1. Identify entry points (Main method, exported APIs)
2. Trace all reachable code paths
3. Mark all types, methods, and fields that might be used
4. Remove everything not marked

```xml
<PropertyGroup>
  <PublishTrimmed>true</PublishTrimmed>
</PropertyGroup>
```

### Trimming Challenges

Trimming struggles with patterns that hide code dependencies from static analysis:

**Reflection**: `Type.GetType("MyNamespace.MyClass")` loads a type by string. The trimmer cannot know this string value at build time, so it might remove the type.

**Serialization**: JSON or XML serialization often discovers types through reflection. Without explicit hints, serialized types may be trimmed.

**Dependency injection**: Container frameworks that scan assemblies for types face similar issues.

### Trim Warnings and Annotations

.NET provides attributes to communicate trimming intent:

```csharp
// This method uses reflection and cannot be safely trimmed
[RequiresUnreferencedCode("Uses reflection to discover types")]
public void DiscoverPlugins() { /* ... */ }

// Preserve this type even if not statically reachable
[DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.All)]
public class PluginBase { }
```

When you build with trimming enabled, the compiler reports warnings for code patterns that may break. Addressing these warnings (either by restructuring code or adding annotations) ensures trimmed applications work correctly.

Source generators help by replacing reflection with static code generation. The JSON source generator, for example, produces trim-compatible serialization code.

## Deployment Models

How you deploy a .NET application affects what must be installed on target machines and how your application starts.

### Framework-Dependent Deployment

**Framework-dependent** applications require the .NET runtime to be installed on the target machine. The published output contains only your application code and dependencies.

```bash
dotnet publish -c Release
```

**Advantages:**
- Small deployment size
- Automatic security updates when the runtime is patched
- Shared runtime reduces disk and memory usage across applications

**Disadvantages:**
- Target machine must have compatible runtime installed
- Runtime version mismatches can cause issues

### Self-Contained Deployment

**Self-contained** applications include the .NET runtime with the published output. No runtime installation is required on the target machine.

```bash
dotnet publish -c Release --self-contained
```

**Advantages:**
- Works without runtime installation
- Isolates application from system runtime updates
- Full control over which runtime version runs

**Disadvantages:**
- Larger deployment size (~60MB+)
- Application is responsible for runtime security updates

### Single-File Deployment

**Single-file** publishing bundles the application and its dependencies into one executable:

```bash
dotnet publish -c Release --self-contained -p:PublishSingleFile=true
```

On first run, the single file extracts to a temporary directory. The application runs from extracted files.

Add `IncludeNativeLibrariesForSelfExtract=true` to include native libraries in the bundle:

```xml
<PropertyGroup>
  <PublishSingleFile>true</PublishSingleFile>
  <IncludeNativeLibrariesForSelfExtract>true</IncludeNativeLibrariesForSelfExtract>
</PropertyGroup>
```

Combine with Native AOT for a true single-file native executable with no extraction.

## Choosing a Compilation Strategy

Different scenarios favor different approaches:

| Scenario | Recommended Approach |
|----------|---------------------|
| Long-running server | JIT with tiered compilation (default) |
| Serverless / cold start sensitive | Native AOT or ReadyToRun |
| CLI tools | Native AOT for instant startup |
| Mobile apps | AOT (required on iOS) |
| Desktop apps | Framework-dependent or R2R |
| Microservices in containers | Trimmed + R2R or Native AOT |
| Plugins/extensibility needed | JIT (AOT cannot load dynamic assemblies) |

### Decision Factors

**Startup time**: How critical is cold start latency? AOT and R2R help; pure JIT is slowest.

**Peak throughput**: JIT tiered compilation achieves best steady-state performance through runtime optimization.

**Deployment size**: Native AOT with trimming produces smallest executables. Self-contained JIT is largest.

**Reflection requirements**: Heavy reflection use requires JIT or careful AOT annotation work.

**Target platforms**: iOS requires AOT. Some embedded systems prohibit JIT.

## Runtime Configuration

Several runtime settings affect compilation and execution:

### Environment Variables

```bash
# Disable tiered compilation
DOTNET_TieredCompilation=0

# Disable ReadyToRun precompiled code
DOTNET_ReadyToRun=0

# Enable JIT stress modes for testing
DOTNET_JitStress=2
```

### Runtime Configuration Files

`runtimeconfig.json` controls runtime behavior for published applications:

```json
{
  "runtimeOptions": {
    "configProperties": {
      "System.GC.Concurrent": true,
      "System.GC.Server": true,
      "System.Runtime.TieredCompilation": true
    }
  }
}
```

### Debugging and Diagnostics

To observe JIT behavior:

```bash
# See what methods are JIT compiled
DOTNET_JitDisasm=*

# Dump compilation timing
DOTNET_JitTimeLogFile=jit-timing.log
```

These diagnostics help identify methods with high JIT time or unexpected compilation patterns.

## Key Takeaways

- .NET compiles to **IL first**, then to **native code** either at runtime (JIT) or build time (AOT)
- **JIT compilation** enables runtime optimization but incurs startup cost
- **Tiered compilation** balances startup speed with steady-state performance by compiling methods in stages
- **Native AOT** eliminates JIT overhead but restricts reflection and dynamic code
- **ReadyToRun** provides a middle ground: precompiled native code with JIT fallback
- **Trimming** reduces deployment size but requires care with reflection-heavy code
- **Source generators** enable AOT-compatible patterns that traditionally required reflection

Understanding these compilation modes helps you choose the right tradeoffs for your application's performance, size, and platform requirements.
