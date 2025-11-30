---
title: "C# Configuration and Options Pattern"
layout: guide
category: ".NET & C#"
subcategory: "Core Libraries"
description: "Application configuration with IConfiguration, strongly-typed options, secrets management, and configuration providers."
tags: [c-sharp, dotnet, configuration, options-pattern, dependency-injection, practical]
---

## Configuration Overview

.NET's configuration system provides a unified API for reading settings from multiple sources with support for hierarchical data, environment-specific overrides, and strongly-typed access.

```csharp
// Configuration flows from multiple sources, later sources override earlier
// 1. appsettings.json
// 2. appsettings.{Environment}.json
// 3. User secrets (Development only)
// 4. Environment variables
// 5. Command-line arguments
```

## IConfiguration Basics

### Reading Configuration Values

```csharp
// Direct value access
string? connectionString = configuration["ConnectionStrings:DefaultDb"];
string? apiKey = configuration["ExternalServices:ApiKey"];

// GetValue with type conversion and default
int maxRetries = configuration.GetValue<int>("Settings:MaxRetries", 3);
bool enableFeature = configuration.GetValue<bool>("Features:NewDashboard");

// GetSection for hierarchical access
IConfigurationSection section = configuration.GetSection("Logging");
string? logLevel = section["LogLevel:Default"];

// Check if section exists
if (configuration.GetSection("OptionalFeature").Exists())
{
    // Configure optional feature
}
```

### Configuration Hierarchy

```json
// appsettings.json
{
  "ConnectionStrings": {
    "DefaultDb": "Server=localhost;Database=MyApp",
    "Redis": "localhost:6379"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning"
    }
  },
  "AppSettings": {
    "ApiBaseUrl": "https://api.example.com",
    "PageSize": 25,
    "Features": {
      "EnableCaching": true,
      "EnableMetrics": false
    }
  }
}
```

```csharp
// Access nested values with colon separator
var defaultDb = configuration["ConnectionStrings:DefaultDb"];
var defaultLogLevel = configuration["Logging:LogLevel:Default"];
var enableCaching = configuration.GetValue<bool>("AppSettings:Features:EnableCaching");
```

## The Options Pattern

Strongly-typed configuration that integrates with dependency injection.

### Basic Options Setup

```csharp
// Define options class
public class EmailOptions
{
    public const string SectionName = "Email";

    public string SmtpServer { get; set; } = "";
    public int Port { get; set; } = 587;
    public string FromAddress { get; set; } = "";
    public bool UseSsl { get; set; } = true;
}
```

```json
// appsettings.json
{
  "Email": {
    "SmtpServer": "smtp.example.com",
    "Port": 587,
    "FromAddress": "noreply@example.com",
    "UseSsl": true
  }
}
```

```csharp
// Register in Program.cs
builder.Services.Configure<EmailOptions>(
    builder.Configuration.GetSection(EmailOptions.SectionName));

// Or bind manually
builder.Services.Configure<EmailOptions>(options =>
{
    options.SmtpServer = "smtp.custom.com";
    options.Port = 25;
});
```

### Consuming Options

```csharp
public class EmailService
{
    private readonly EmailOptions _options;

    // IOptions<T> - singleton, read at startup
    public EmailService(IOptions<EmailOptions> options)
    {
        _options = options.Value;
    }

    public void SendEmail(string to, string subject, string body)
    {
        using var client = new SmtpClient(_options.SmtpServer, _options.Port);
        client.EnableSsl = _options.UseSsl;
        // ...
    }
}
```

### Options Interfaces

<div class="comparison">
<div class="content-card content-card--accent">
<h4>IOptions&lt;T&gt;</h4>
<ul>
<li>Lifetime: Singleton</li>
<li>Updates: No</li>
<li>Use for: Static configuration</li>
</ul>
</div>
<div class="content-card content-card--accent-secondary">
<h4>IOptionsSnapshot&lt;T&gt;</h4>
<ul>
<li>Lifetime: Scoped</li>
<li>Updates: Per request</li>
<li>Use for: Config that changes between requests</li>
</ul>
</div>
<div class="content-card content-card--accent">
<h4>IOptionsMonitor&lt;T&gt;</h4>
<ul>
<li>Lifetime: Singleton</li>
<li>Updates: Yes, with callback</li>
<li>Use for: Live updates, long-running services</li>
</ul>
</div>
</div>

| Interface | Lifetime | Updates | Use Case |
|-----------|----------|---------|----------|
| `IOptions<T>` | Singleton | No | Static configuration |
| `IOptionsSnapshot<T>` | Scoped | Per request | Config that changes between requests |
| `IOptionsMonitor<T>` | Singleton | Yes, with callback | Live updates, long-running services |

```csharp
// IOptionsSnapshot - picks up changes per request
public class FeatureService
{
    private readonly FeatureOptions _options;

    public FeatureService(IOptionsSnapshot<FeatureOptions> options)
    {
        _options = options.Value;  // Fresh value each request
    }
}

// IOptionsMonitor - live updates with change notification
public class BackgroundWorker : BackgroundService
{
    private readonly IOptionsMonitor<WorkerOptions> _optionsMonitor;

    public BackgroundWorker(IOptionsMonitor<WorkerOptions> optionsMonitor)
    {
        _optionsMonitor = optionsMonitor;

        // Subscribe to changes
        _optionsMonitor.OnChange(options =>
        {
            Console.WriteLine($"Options changed: Interval = {options.Interval}");
        });
    }

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            var options = _optionsMonitor.CurrentValue;  // Always current
            await DoWorkAsync(options);
            await Task.Delay(options.Interval, ct);
        }
    }
}
```

### Named Options

For multiple configurations of the same type.

```csharp
// appsettings.json
{
  "HttpClients": {
    "GitHub": {
      "BaseUrl": "https://api.github.com",
      "Timeout": 30
    },
    "Stripe": {
      "BaseUrl": "https://api.stripe.com",
      "Timeout": 60
    }
  }
}

// Register named options
builder.Services.Configure<HttpClientOptions>("GitHub",
    builder.Configuration.GetSection("HttpClients:GitHub"));
builder.Services.Configure<HttpClientOptions>("Stripe",
    builder.Configuration.GetSection("HttpClients:Stripe"));

// Consume with IOptionsSnapshot or IOptionsMonitor
public class ApiClientFactory
{
    private readonly IOptionsSnapshot<HttpClientOptions> _options;

    public ApiClientFactory(IOptionsSnapshot<HttpClientOptions> options)
    {
        _options = options;
    }

    public HttpClient CreateClient(string name)
    {
        var options = _options.Get(name);  // Get by name
        return new HttpClient
        {
            BaseAddress = new Uri(options.BaseUrl),
            Timeout = TimeSpan.FromSeconds(options.Timeout)
        };
    }
}
```

## Options Validation

### Data Annotations

```csharp
using System.ComponentModel.DataAnnotations;

public class DatabaseOptions
{
    [Required]
    public string ConnectionString { get; set; } = "";

    [Range(1, 100)]
    public int MaxConnections { get; set; } = 10;

    [RegularExpression(@"^\d+$")]
    public string PoolSize { get; set; } = "5";
}

// Enable validation
builder.Services.AddOptions<DatabaseOptions>()
    .Bind(builder.Configuration.GetSection("Database"))
    .ValidateDataAnnotations()
    .ValidateOnStart();  // Fail fast at startup
```

### Custom Validation

```csharp
builder.Services.AddOptions<ApiOptions>()
    .Bind(builder.Configuration.GetSection("Api"))
    .Validate(options =>
    {
        if (string.IsNullOrEmpty(options.ApiKey))
            return false;
        if (options.Timeout <= TimeSpan.Zero)
            return false;
        return true;
    }, "API configuration is invalid")
    .ValidateOnStart();

// Complex validation with IValidateOptions
public class ApiOptionsValidator : IValidateOptions<ApiOptions>
{
    public ValidateOptionsResult Validate(string? name, ApiOptions options)
    {
        var failures = new List<string>();

        if (string.IsNullOrEmpty(options.BaseUrl))
            failures.Add("BaseUrl is required");

        if (!Uri.TryCreate(options.BaseUrl, UriKind.Absolute, out _))
            failures.Add("BaseUrl must be a valid URL");

        if (options.RetryCount < 0 || options.RetryCount > 10)
            failures.Add("RetryCount must be between 0 and 10");

        return failures.Count > 0
            ? ValidateOptionsResult.Fail(failures)
            : ValidateOptionsResult.Success;
    }
}

// Register validator
builder.Services.AddSingleton<IValidateOptions<ApiOptions>, ApiOptionsValidator>();
```

## Configuration Providers

### JSON Files

```csharp
builder.Configuration
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json",
        optional: true, reloadOnChange: true);
```

### Environment Variables

<div class="callout callout--tip">
<p class="callout__title">Environment Variable Naming Convention</p>
<p>Use double underscores (<code>__</code>) to represent nesting in hierarchical configuration. Example: <code>MYAPP_ConnectionStrings__DefaultDb</code> maps to <code>configuration["ConnectionStrings:DefaultDb"]</code></p>
</div>

```csharp
// Automatic in Host builder
builder.Configuration.AddEnvironmentVariables();

// With prefix filter
builder.Configuration.AddEnvironmentVariables("MYAPP_");

// Environment variable naming (double underscore for nesting)
// MYAPP_ConnectionStrings__DefaultDb = "Server=..."
// Maps to configuration["ConnectionStrings:DefaultDb"]
```

### User Secrets (Development)

```bash
# Initialize secrets for project
dotnet user-secrets init

# Set a secret
dotnet user-secrets set "Api:SecretKey" "my-secret-key"

# List secrets
dotnet user-secrets list
```

```csharp
// Added automatically in Development
if (builder.Environment.IsDevelopment())
{
    builder.Configuration.AddUserSecrets<Program>();
}
```

### Command Line

```csharp
builder.Configuration.AddCommandLine(args);

// Usage
// dotnet run --ConnectionStrings:DefaultDb="Server=prod"
// dotnet run /Settings:MaxRetries=5
```

### In-Memory (Testing)

```csharp
var config = new Dictionary<string, string?>
{
    ["Database:ConnectionString"] = "Server=test",
    ["Features:EnableNewUI"] = "true"
};

var configuration = new ConfigurationBuilder()
    .AddInMemoryCollection(config)
    .Build();
```

### Custom Provider

```csharp
public class DatabaseConfigurationProvider : ConfigurationProvider
{
    private readonly string _connectionString;

    public DatabaseConfigurationProvider(string connectionString)
    {
        _connectionString = connectionString;
    }

    public override void Load()
    {
        using var connection = new SqlConnection(_connectionString);
        connection.Open();

        using var command = new SqlCommand(
            "SELECT [Key], [Value] FROM Configuration", connection);
        using var reader = command.ExecuteReader();

        var data = new Dictionary<string, string?>(StringComparer.OrdinalIgnoreCase);
        while (reader.Read())
        {
            data[reader.GetString(0)] = reader.GetString(1);
        }

        Data = data;
    }
}

public class DatabaseConfigurationSource : IConfigurationSource
{
    public string ConnectionString { get; set; } = "";

    public IConfigurationProvider Build(IConfigurationBuilder builder)
    {
        return new DatabaseConfigurationProvider(ConnectionString);
    }
}

// Extension method
public static class ConfigurationExtensions
{
    public static IConfigurationBuilder AddDatabase(
        this IConfigurationBuilder builder,
        string connectionString)
    {
        return builder.Add(new DatabaseConfigurationSource
        {
            ConnectionString = connectionString
        });
    }
}

// Usage
builder.Configuration.AddDatabase(connectionString);
```

## Environment-Specific Configuration

### Detecting Environment

```csharp
// In Program.cs
if (builder.Environment.IsDevelopment())
{
    builder.Services.AddDatabaseDeveloperPageExceptionFilter();
}

if (builder.Environment.IsProduction())
{
    builder.Services.AddApplicationInsightsTelemetry();
}

// Custom environments
if (builder.Environment.IsEnvironment("Staging"))
{
    // Staging-specific configuration
}
```

### Environment Override Pattern

```json
// appsettings.json (defaults)
{
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  },
  "Features": {
    "EnableDebugEndpoints": false
  }
}

// appsettings.Development.json (overrides)
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  },
  "Features": {
    "EnableDebugEndpoints": true
  }
}

// appsettings.Production.json (overrides)
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning"
    }
  }
}
```

## Secrets Management

### Development Secrets

```csharp
// User secrets - never committed to source control
// Stored in: %APPDATA%\Microsoft\UserSecrets\{guid}\secrets.json (Windows)
// Stored in: ~/.microsoft/usersecrets/{guid}/secrets.json (Linux/macOS)

dotnet user-secrets set "Database:Password" "dev-password"
```

### Production Secrets

```csharp
// Azure Key Vault
builder.Configuration.AddAzureKeyVault(
    new Uri("https://myapp-vault.vault.azure.net/"),
    new DefaultAzureCredential());

// AWS Secrets Manager (via custom provider or SDK)
// HashiCorp Vault (via custom provider)
```

### Secret Reference Pattern

```json
// appsettings.json - reference, not value
{
  "Database": {
    "ConnectionString": "from-keyvault"
  }
}

// Key Vault secret named "Database--ConnectionString"
// Automatically mapped to configuration["Database:ConnectionString"]
```

## Post-Configuration

Modify options after binding.

```csharp
builder.Services.PostConfigure<EmailOptions>(options =>
{
    // Always apply these after any other configuration
    if (string.IsNullOrEmpty(options.FromAddress))
    {
        options.FromAddress = "default@example.com";
    }
});

// Named post-configuration
builder.Services.PostConfigure<HttpClientOptions>("GitHub", options =>
{
    options.BaseUrl = options.BaseUrl.TrimEnd('/');
});

// PostConfigureAll - applies to all named options
builder.Services.PostConfigureAll<HttpClientOptions>(options =>
{
    if (options.Timeout == default)
    {
        options.Timeout = 30;
    }
});
```

## Configuration Binding

### Bind to Existing Object

```csharp
var settings = new AppSettings();
configuration.GetSection("AppSettings").Bind(settings);

// Or create and bind
var settings = configuration.GetSection("AppSettings").Get<AppSettings>();
```

### Binding Options

```csharp
builder.Services.Configure<ComplexOptions>(
    builder.Configuration.GetSection("Complex"),
    options =>
    {
        options.BindNonPublicProperties = true;
        options.ErrorOnUnknownConfiguration = true;  // Catch typos
    });
```

## Version History

| Feature | Version | Significance |
|---------|---------|--------------|
| IConfiguration | .NET Core 1.0 | Unified configuration API |
| Options pattern | .NET Core 1.0 | Strongly-typed configuration |
| IOptionsSnapshot | .NET Core 1.1 | Scoped options with reload |
| IOptionsMonitor | .NET Core 2.0 | Live options with change tokens |
| ValidateOnStart | .NET 6 | Fail-fast validation |
| Options validation | .NET Core 2.1 | Data annotations support |

## Key Takeaways

**Use the options pattern**: Strongly-typed options integrate with DI and enable validation.

**Layer configuration sources**: Base settings in appsettings.json, environment-specific overrides, secrets from secure sources.

**Never store secrets in code or appsettings.json**: Use User Secrets for development, Key Vault or similar for production.

**Validate early**: Use `ValidateOnStart()` to catch configuration errors at startup, not at runtime.

**Choose the right interface**: `IOptions<T>` for static config, `IOptionsSnapshot<T>` for per-request, `IOptionsMonitor<T>` for live updates.

**Environment variables for containers**: Override configuration in Docker/Kubernetes via environment variables without rebuilding images.
