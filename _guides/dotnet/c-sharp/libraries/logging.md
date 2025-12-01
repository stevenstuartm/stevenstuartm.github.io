---
title: "C# Logging with Microsoft.Extensions.Logging"
layout: guide
category: ".NET & C#"
subcategory: "Core Libraries"
description: "Structured logging with ILogger, log levels, scopes, providers, and high-performance logging patterns."
tags: [c-sharp, dotnet, logging, observability, debugging, practical]
---

## Logging Overview

Microsoft.Extensions.Logging provides a unified logging abstraction used across .NET applications. It supports structured logging, multiple output providers, and integrates with dependency injection.

```csharp
public class OrderService
{
    private readonly ILogger<OrderService> _logger;

    public OrderService(ILogger<OrderService> logger)
    {
        _logger = logger;
    }

    public void ProcessOrder(int orderId)
    {
        _logger.LogInformation("Processing order {OrderId}", orderId);

        try
        {
            // Process...
            _logger.LogInformation("Order {OrderId} completed successfully", orderId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to process order {OrderId}", orderId);
            throw;
        }
    }
}
```

## Log Levels

```csharp
// Levels from least to most severe
_logger.LogTrace("Detailed diagnostic info");      // 0 - Trace
_logger.LogDebug("Debugging information");         // 1 - Debug
_logger.LogInformation("General information");     // 2 - Information
_logger.LogWarning("Something unexpected");        // 3 - Warning
_logger.LogError(ex, "An error occurred");        // 4 - Error
_logger.LogCritical(ex, "System failure");        // 5 - Critical

// Check if level is enabled (avoid expensive operations)
if (_logger.IsEnabled(LogLevel.Debug))
{
    var expensiveData = ComputeDebugInfo();
    _logger.LogDebug("Debug info: {Data}", expensiveData);
}
```

### Log Level Guidelines

| Level | When to Use |
|-------|-------------|
| Trace | Detailed diagnostic info, method entry/exit |
| Debug | Information useful during development |
| Information | General operational events |
| Warning | Unexpected but handled situations |
| Error | Errors that prevent specific operations |
| Critical | Failures requiring immediate attention |

## Structured Logging

Log data as structured properties, not just text.

```csharp
// BAD: Interpolated strings lose structure
_logger.LogInformation($"User {userId} purchased product {productId}");

// GOOD: Structured with named parameters
_logger.LogInformation(
    "User {UserId} purchased product {ProductId}",
    userId, productId);

// Properties become searchable in log systems:
// { "UserId": 123, "ProductId": "SKU-456", "Message": "User 123 purchased..." }

// Complex objects
_logger.LogInformation("Order created: {@Order}", order);  // @ for destructuring
_logger.LogInformation("Order created: {$Order}", order);  // $ for ToString()
```

## Logging Configuration

### appsettings.json

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information",
      "MyApp.Services": "Debug"
    },
    "Console": {
      "LogLevel": {
        "Default": "Information"
      },
      "FormatterName": "json"
    },
    "Debug": {
      "LogLevel": {
        "Default": "Debug"
      }
    }
  }
}
```

### Programmatic Configuration

```csharp
builder.Logging
    .ClearProviders()
    .AddConsole()
    .AddDebug()
    .SetMinimumLevel(LogLevel.Debug)
    .AddFilter("Microsoft", LogLevel.Warning)
    .AddFilter<ConsoleLoggerProvider>("MyApp", LogLevel.Debug);
```

## Log Scopes

<div class="callout callout--tip">
<p class="callout__title">Use Scopes for Correlation</p>
<p>Log scopes add context to all log entries within a block, such as request IDs, user IDs, or transaction IDs. This makes correlated events searchable across distributed systems.</p>
</div>

Add contextual information to a group of log entries.

```csharp
public async Task ProcessOrderAsync(Order order)
{
    using (_logger.BeginScope(new Dictionary<string, object>
    {
        ["OrderId"] = order.Id,
        ["CustomerId"] = order.CustomerId
    }))
    {
        _logger.LogInformation("Starting order processing");
        await ValidateOrderAsync(order);
        await ChargePaymentAsync(order);
        await FulfillOrderAsync(order);
        _logger.LogInformation("Order processing complete");
    }
    // All logs within scope include OrderId and CustomerId
}

// Simpler scope syntax
using (_logger.BeginScope("Processing order {OrderId}", orderId))
{
    // Logs include OrderId
}
```

### Enable Scope Logging

```json
{
  "Logging": {
    "Console": {
      "IncludeScopes": true
    }
  }
}
```

## Built-in Providers

### Console

```csharp
builder.Logging.AddConsole(options =>
{
    options.FormatterName = "json";  // or "simple", "systemd"
});

// Custom formatter
builder.Logging.AddConsole(options =>
{
    options.FormatterName = "custom";
}).AddConsoleFormatter<CustomFormatter, CustomFormatterOptions>();
```

### Debug

```csharp
// Outputs to System.Diagnostics.Debug
builder.Logging.AddDebug();
```

### EventSource

```csharp
// For ETW/EventPipe integration
builder.Logging.AddEventSourceLogger();
```

### EventLog (Windows)

```csharp
builder.Logging.AddEventLog(settings =>
{
    settings.SourceName = "MyApplication";
});
```

## High-Performance Logging

### Source-Generated Logging (C# 9+)

<blockquote class="pull-quote">
<p>Source-generated logging eliminates all reflection, boxing, and string parsing at runtime. For high-throughput applications, this dramatically reduces allocation pressure.</p>
</blockquote>

Eliminates boxing and parsing overhead at runtime.

```csharp
public static partial class LogMessages
{
    [LoggerMessage(
        EventId = 1000,
        Level = LogLevel.Information,
        Message = "Processing order {OrderId} for customer {CustomerId}")]
    public static partial void OrderProcessing(
        ILogger logger,
        int orderId,
        string customerId);

    [LoggerMessage(
        EventId = 1001,
        Level = LogLevel.Warning,
        Message = "Order {OrderId} has {ItemCount} items exceeding limit")]
    public static partial void OrderItemsExceeded(
        ILogger logger,
        int orderId,
        int itemCount);

    [LoggerMessage(
        EventId = 1002,
        Level = LogLevel.Error,
        Message = "Failed to process order {OrderId}")]
    public static partial void OrderFailed(
        ILogger logger,
        int orderId,
        Exception exception);
}

// Usage
LogMessages.OrderProcessing(_logger, order.Id, order.CustomerId);
LogMessages.OrderFailed(_logger, order.Id, ex);
```

Benefits:
- No boxing of value types
- No string parsing at runtime
- Compile-time validation of parameters
- Better performance when log level is disabled

### Avoid Expensive Operations

```csharp
// BAD: Always evaluates ToString() even if level disabled
_logger.LogDebug("Complex data: " + complexObject.ToString());

// GOOD: Only evaluated if Debug is enabled
_logger.LogDebug("Complex data: {Data}", complexObject);

// BEST: Check level for expensive operations
if (_logger.IsEnabled(LogLevel.Debug))
{
    var debugData = GenerateExpensiveDebugData();
    _logger.LogDebug("Debug data: {Data}", debugData);
}
```

## Third-Party Providers

### Serilog

```csharp
// Install: Serilog.AspNetCore
builder.Host.UseSerilog((context, config) =>
{
    config
        .ReadFrom.Configuration(context.Configuration)
        .WriteTo.Console()
        .WriteTo.File("logs/log-.txt", rollingInterval: RollingInterval.Day)
        .WriteTo.Seq("http://localhost:5341")
        .Enrich.FromLogContext()
        .Enrich.WithMachineName()
        .Enrich.WithThreadId();
});
```

```json
// appsettings.json for Serilog
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning"
      }
    },
    "WriteTo": [
      { "Name": "Console" },
      {
        "Name": "File",
        "Args": {
          "path": "logs/log-.txt",
          "rollingInterval": "Day"
        }
      }
    ]
  }
}
```

### NLog

```csharp
// Install: NLog.Web.AspNetCore
builder.Logging.ClearProviders();
builder.Host.UseNLog();
```

## Correlation and Distributed Tracing

### Activity and Trace Context

```csharp
public class OrderService
{
    private readonly ILogger<OrderService> _logger;

    public async Task ProcessOrderAsync(Order order)
    {
        // Activity provides TraceId and SpanId automatically
        using var activity = new Activity("ProcessOrder").Start();

        _logger.LogInformation("Processing order {OrderId}", order.Id);
        // Log includes Activity.Current.TraceId

        await _paymentService.ChargeAsync(order);
        // Payment service logs will share the same TraceId
    }
}
```

### Manual Correlation

```csharp
public async Task HandleRequestAsync(HttpContext context)
{
    var correlationId = context.Request.Headers["X-Correlation-Id"]
        .FirstOrDefault() ?? Guid.NewGuid().ToString();

    using (_logger.BeginScope(new Dictionary<string, object>
    {
        ["CorrelationId"] = correlationId
    }))
    {
        _logger.LogInformation("Handling request");
        // Process request...
    }
}
```

## Logging in Different Contexts

### Static/Startup Logging

```csharp
// Before DI is available
var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.AddConsole();
    builder.SetMinimumLevel(LogLevel.Debug);
});

var logger = loggerFactory.CreateLogger<Program>();
logger.LogInformation("Application starting");
```

### Background Services

```csharp
public class WorkerService : BackgroundService
{
    private readonly ILogger<WorkerService> _logger;

    public WorkerService(ILogger<WorkerService> logger)
    {
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        _logger.LogInformation("Worker started");

        while (!ct.IsCancellationRequested)
        {
            using (_logger.BeginScope("Iteration at {Time}", DateTime.UtcNow))
            {
                try
                {
                    await DoWorkAsync(ct);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error during work iteration");
                }
            }

            await Task.Delay(TimeSpan.FromMinutes(1), ct);
        }

        _logger.LogInformation("Worker stopped");
    }
}
```

### Testing with Logging

```csharp
public class OrderServiceTests
{
    [Fact]
    public void ProcessOrder_LogsInformation()
    {
        // Arrange
        var logger = new FakeLogger<OrderService>();
        var service = new OrderService(logger);

        // Act
        service.ProcessOrder(123);

        // Assert
        Assert.Contains(logger.LogEntries,
            e => e.LogLevel == LogLevel.Information
              && e.Message.Contains("123"));
    }
}

// Simple fake logger
public class FakeLogger<T> : ILogger<T>
{
    public List<LogEntry> LogEntries { get; } = new();

    public void Log<TState>(LogLevel logLevel, EventId eventId, TState state,
        Exception? exception, Func<TState, Exception?, string> formatter)
    {
        LogEntries.Add(new LogEntry
        {
            LogLevel = logLevel,
            Message = formatter(state, exception),
            Exception = exception
        });
    }

    public bool IsEnabled(LogLevel logLevel) => true;
    public IDisposable? BeginScope<TState>(TState state) where TState : notnull
        => null;
}
```

## Best Practices

### Message Templates

```csharp
// Use consistent naming
_logger.LogInformation("User {UserId} logged in from {IpAddress}", userId, ip);

// PascalCase for property names
_logger.LogInformation("Processing {ItemCount} items", items.Count);

// Be specific
_logger.LogError(ex, "Failed to save user {UserId} to database {Database}",
    userId, databaseName);
```

### What to Log

```csharp
public async Task<Order> CreateOrderAsync(CreateOrderRequest request)
{
    _logger.LogInformation("Creating order for customer {CustomerId}", request.CustomerId);

    // Log important business events
    var order = new Order(request);
    _logger.LogInformation("Order {OrderId} created with {ItemCount} items, total {Total}",
        order.Id, order.Items.Count, order.Total);

    // Log integration points
    _logger.LogDebug("Sending order {OrderId} to fulfillment service", order.Id);
    await _fulfillmentService.QueueOrderAsync(order);

    // Log completion
    _logger.LogInformation("Order {OrderId} queued for fulfillment", order.Id);

    return order;
}
```

### What NOT to Log

```csharp
// DON'T log sensitive data
_logger.LogInformation("User {Email} with password {Password}");  // NO!
_logger.LogInformation("Credit card {CardNumber}");  // NO!

// DON'T log at wrong levels
_logger.LogError("User not found");  // Should be Warning or Info
_logger.LogInformation("Exception: " + ex);  // Should be Error with exception

// DON'T log too much in hot paths
foreach (var item in millionsOfItems)
{
    _logger.LogDebug("Processing {Item}", item);  // Too much logging
}
```

## Version History

| Feature | Version | Significance |
|---------|---------|--------------|
| ILogger abstraction | .NET Core 1.0 | Unified logging API |
| Log scopes | .NET Core 1.0 | Contextual grouping |
| Configuration integration | .NET Core 1.0 | appsettings.json support |
| Source generators | .NET 6 | High-performance logging |
| JSON console formatter | .NET 5 | Structured console output |
| W3C trace context | .NET Core 3.0 | Distributed tracing |

## Key Takeaways

**Use structured logging**: Pass parameters separately, don't interpolate into message strings.

**Choose appropriate levels**: Information for business events, Warning for handled issues, Error for failures.

**Use source-generated logging**: For high-performance scenarios, eliminate runtime overhead.

**Add context with scopes**: Group related logs with correlation IDs and contextual data.

**Don't log sensitive data**: Never log passwords, tokens, credit cards, or PII.

**Consider log volume**: Trace and Debug levels can be extremely verbose. Use IsEnabled checks for expensive operations.

**Test your logging**: Verify critical events are logged correctly with fake loggers in tests.
