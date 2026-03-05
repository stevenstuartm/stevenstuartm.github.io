---
title: "C# Configuration and Options Pattern"
layout: guide
category: ".NET & C#"
subcategory: "Core Libraries"
description: "Application configuration strategies organized by local vs remote and secure vs non-secure sources, with strongly-typed options and validation."
tags: [c-sharp, dotnet, configuration, options-pattern, dependency-injection, practical]
---

## How .NET Configuration Works

.NET's configuration system loads settings from multiple providers into a unified `IConfiguration` interface. Providers are added in order, and later sources override earlier ones. This layering is what makes the system powerful: you define safe defaults locally, then override with environment-specific or secret values from secure remote sources.

```csharp
var builder = WebApplication.CreateBuilder(args);

// Providers are added in order - later sources win
builder.Configuration
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json",
        optional: true, reloadOnChange: true)
    .AddEnvironmentVariables()
    .AddAzureKeyVault(vaultUri, new DefaultAzureCredential());
```

The rest of this guide is organized around two questions: where does the configuration live (local files vs remote services), and does it contain sensitive data?

## Configuration Strategies

### Local, Non-Secure: JSON Files and Environment Overrides

Use local JSON files for application defaults, feature flags, logging levels, page sizes, and anything safe to commit to source control.

```json
// appsettings.json - safe defaults, committed to source control
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning"
    }
  },
  "AppSettings": {
    "PageSize": 25,
    "Features": {
      "EnableCaching": true,
      "EnableMetrics": false
    }
  }
}
```

Environment-specific overrides use the `appsettings.{Environment}.json` convention. These files only need to contain the values that differ from the base file.

```json
// appsettings.Development.json - overrides for local dev
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
```

```json
// appsettings.Production.json - overrides for production
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning"
    }
  }
}
```

**Environment variables** work well for container deployments where you want to override configuration without rebuilding images. Use double underscores to represent hierarchy.

```csharp
builder.Configuration.AddEnvironmentVariables("MYAPP_");

// MYAPP_ConnectionStrings__DefaultDb="Server=prod"
// Maps to configuration["ConnectionStrings:DefaultDb"]
```

**Command-line arguments** are useful for one-off overrides during local development or CI.

```csharp
builder.Configuration.AddCommandLine(args);
// dotnet run --Settings:MaxRetries=5
```

**When to use local non-secure configuration**: application behavior settings, feature toggles, logging configuration, UI defaults, timeouts, and retry policies. Anything that is not sensitive and benefits from being version-controlled alongside the application.

### Local, Secure: User Secrets (Development Only)

User Secrets store sensitive values on the developer's machine outside the project directory, so they never end up in source control. This is strictly a development-time solution.

```bash
# Initialize secrets for the project
dotnet user-secrets init

# Set secrets
dotnet user-secrets set "Database:Password" "dev-password"
dotnet user-secrets set "Api:SecretKey" "my-dev-key"

# List what's stored
dotnet user-secrets list
```

```csharp
// Added automatically in Development environment
if (builder.Environment.IsDevelopment())
{
    builder.Configuration.AddUserSecrets<Program>();
}
```

Secrets are stored in `%APPDATA%\Microsoft\UserSecrets\{guid}\secrets.json` on Windows and `~/.microsoft/usersecrets/{guid}/secrets.json` on Linux/macOS.

**When to use User Secrets**: local development only, for connection strings, API keys, and passwords that you need on your machine but must never commit. This is not a production solution.

### Remote, Secure: Cloud Secret Stores

For production, secrets should live in a dedicated secret management service. A configuration provider loads them into `IConfiguration` at startup, so the rest of the application accesses secrets the same way it accesses any other configuration value. The level of integration varies significantly by cloud provider.

**Azure Key Vault** has the smoothest experience because Microsoft provides a first-party NuGet package (`Azure.Extensions.AspNetCore.Configuration.Secrets`) that plugs directly into the configuration pipeline.

```csharp
// NuGet: Azure.Extensions.AspNetCore.Configuration.Secrets
// NuGet: Azure.Identity
builder.Configuration.AddAzureKeyVault(
    new Uri("https://myapp-vault.vault.azure.net/"),
    new DefaultAzureCredential());
```

Key Vault secret names use `--` as a hierarchy separator. A secret named `Database--ConnectionString` maps to `configuration["Database:ConnectionString"]`. Authentication is handled by `DefaultAzureCredential`, which automatically picks the right identity (managed identity in Azure, your developer credentials locally).

**AWS Systems Manager Parameter Store** has an official AWS-maintained package (`Amazon.Extensions.Configuration.SystemsManager`) that works as an `IConfiguration` provider. This is the closest AWS equivalent to the Azure Key Vault experience.

```csharp
// NuGet: Amazon.Extensions.Configuration.SystemsManager
builder.Configuration.AddSystemsManager("/myapp/production/");
```

Parameter Store organizes secrets by path, so `/myapp/production/Database/ConnectionString` maps to `configuration["Database:ConnectionString"]`. Parameter Store supports both plain strings and SecureString parameters (encrypted with KMS), but the provider treats them the same way since decryption happens server-side.

**AWS Secrets Manager** does not have a first-party `IConfiguration` provider from AWS or Microsoft. The options are:

- Use the community NuGet package `Kralizek.Extensions.Configuration.AWSSecretsManager`, which provides an `AddSecretsManager()` extension
- Write a custom `ConfigurationProvider` (see the custom provider pattern in the next section)
- Load secrets directly via the `AWSSDK.SecretsManager` SDK and register them manually

```csharp
// NuGet: Kralizek.Extensions.Configuration.AWSSecretsManager (community package)
builder.Configuration.AddSecretsManager(configurator: options =>
{
    options.SecretFilter = entry => entry.Name.StartsWith("myapp/");
    options.KeyGenerator = (entry, key) => key.Replace("/", ":");
});
```

The trade-off between Parameter Store and Secrets Manager on AWS is worth understanding. Parameter Store is simpler, cheaper (free tier for standard parameters), and has native `IConfiguration` support. Secrets Manager adds automatic rotation, cross-account access, and replication, but costs per-secret and lacks an official configuration provider.

**HashiCorp Vault** also requires a custom provider or community package since there is no first-party integration.

**When to use remote secret stores**: all non-development environments. Connection strings, API keys, certificates, database credentials, and any value that would cause damage if exposed. This should be the default for production workloads.

### Remote, Non-Secure: Centralized Configuration Services

For distributed systems where many services share configuration, a centralized configuration store removes the need to redeploy applications when settings change.

**Azure App Configuration** provides centralized management with feature flags, labeling, and change notifications.

```csharp
builder.Configuration.AddAzureAppConfiguration(options =>
{
    options.Connect(connectionString)
        .Select(KeyFilter.Any, LabelFilter.Null)
        .Select(KeyFilter.Any, builder.Environment.EnvironmentName);
});
```

**Custom providers** load configuration from a database, API, or any other source. Implement `ConfigurationProvider` and `IConfigurationSource` to plug into the standard pipeline.

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

        var data = new Dictionary<string, string?>(
            StringComparer.OrdinalIgnoreCase);
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
        => new DatabaseConfigurationProvider(ConnectionString);
}

// Extension method for clean registration
public static class ConfigurationExtensions
{
    public static IConfigurationBuilder AddDatabase(
        this IConfigurationBuilder builder, string connectionString)
        => builder.Add(new DatabaseConfigurationSource
        {
            ConnectionString = connectionString
        });
}
```

**When to use centralized configuration**: when multiple services need shared settings, when you need to change configuration without redeploying, or when configuration needs audit trails and approval workflows.

### In-Memory Configuration (Testing)

For unit and integration tests, in-memory configuration avoids any dependency on files or external services.

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

## Reading Configuration Values

Regardless of where configuration comes from, access is the same through `IConfiguration`.

```csharp
// Direct key access with colon-separated hierarchy
string? connectionString = configuration["ConnectionStrings:DefaultDb"];
string? logLevel = configuration["Logging:LogLevel:Default"];

// Typed access with defaults
int maxRetries = configuration.GetValue<int>("Settings:MaxRetries", 3);
bool enableFeature = configuration.GetValue<bool>("Features:NewDashboard");

// Section access
IConfigurationSection section = configuration.GetSection("Logging");
if (section.Exists())
{
    string? level = section["LogLevel:Default"];
}
```

## The Options Pattern

The Options Pattern binds configuration sections to strongly-typed classes and integrates with dependency injection. This is the preferred way to consume configuration in application code because it provides compile-time safety, validation, and clean separation of concerns.

### Defining and Registering Options

```csharp
public class EmailOptions
{
    public const string SectionName = "Email";

    public string SmtpServer { get; set; } = "";
    public int Port { get; set; } = 587;
    public string FromAddress { get; set; } = "";
    public bool UseSsl { get; set; } = true;
}

// Register in Program.cs
builder.Services.Configure<EmailOptions>(
    builder.Configuration.GetSection(EmailOptions.SectionName));
```

### Choosing the Right Options Interface

The three interfaces serve different lifetime and update needs.

| Interface | Lifetime | Picks Up Changes | Best For |
|-----------|----------|------------------|----------|
| `IOptions<T>` | Singleton | No | Static configuration that never changes at runtime |
| `IOptionsSnapshot<T>` | Scoped | Per request | Web apps where config might change between requests |
| `IOptionsMonitor<T>` | Singleton | Yes, with callback | Background services and long-running processes |

```csharp
// IOptions<T> - simplest, read once at startup
public class EmailService
{
    private readonly EmailOptions _options;

    public EmailService(IOptions<EmailOptions> options)
    {
        _options = options.Value;
    }
}

// IOptionsMonitor<T> - live updates for background services
public class BackgroundWorker : BackgroundService
{
    private readonly IOptionsMonitor<WorkerOptions> _optionsMonitor;

    public BackgroundWorker(IOptionsMonitor<WorkerOptions> optionsMonitor)
    {
        _optionsMonitor = optionsMonitor;

        _optionsMonitor.OnChange(options =>
        {
            Console.WriteLine($"Options changed: Interval = {options.Interval}");
        });
    }

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            var options = _optionsMonitor.CurrentValue;
            await DoWorkAsync(options);
            await Task.Delay(options.Interval, ct);
        }
    }
}
```

### Named Options

When you need multiple configurations of the same type, named options let you register and retrieve them by name.

```csharp
// Register named options
builder.Services.Configure<HttpClientOptions>("GitHub",
    builder.Configuration.GetSection("HttpClients:GitHub"));
builder.Services.Configure<HttpClientOptions>("Stripe",
    builder.Configuration.GetSection("HttpClients:Stripe"));

// Resolve by name
public class ApiClientFactory
{
    private readonly IOptionsSnapshot<HttpClientOptions> _options;

    public ApiClientFactory(IOptionsSnapshot<HttpClientOptions> options)
    {
        _options = options;
    }

    public HttpClient CreateClient(string name)
    {
        var options = _options.Get(name);
        return new HttpClient
        {
            BaseAddress = new Uri(options.BaseUrl),
            Timeout = TimeSpan.FromSeconds(options.Timeout)
        };
    }
}
```

## Validation

Validation catches configuration errors before they cause runtime failures. Always use `ValidateOnStart()` so the application fails fast on misconfiguration rather than failing later in production.

### Data Annotations

```csharp
public class DatabaseOptions
{
    [Required]
    public string ConnectionString { get; set; } = "";

    [Range(1, 100)]
    public int MaxConnections { get; set; } = 10;
}

builder.Services.AddOptions<DatabaseOptions>()
    .Bind(builder.Configuration.GetSection("Database"))
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

### Custom Validation

```csharp
// Inline validation
builder.Services.AddOptions<ApiOptions>()
    .Bind(builder.Configuration.GetSection("Api"))
    .Validate(options =>
    {
        if (string.IsNullOrEmpty(options.ApiKey)) return false;
        if (options.Timeout <= TimeSpan.Zero) return false;
        return true;
    }, "API configuration is invalid")
    .ValidateOnStart();

// Complex validation with IValidateOptions<T>
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

builder.Services.AddSingleton<
    IValidateOptions<ApiOptions>, ApiOptionsValidator>();
```

## Post-Configuration

Post-configuration runs after all other configuration sources have been applied. Use it to enforce defaults or normalize values.

```csharp
builder.Services.PostConfigure<EmailOptions>(options =>
{
    if (string.IsNullOrEmpty(options.FromAddress))
    {
        options.FromAddress = "default@example.com";
    }
});

// PostConfigureAll applies to all named instances
builder.Services.PostConfigureAll<HttpClientOptions>(options =>
{
    if (options.Timeout == default)
    {
        options.Timeout = 30;
    }
});
```

## Choosing the Right Strategy

| Scenario | Strategy | Provider | Integration Quality |
|----------|----------|----------|---------------------|
| App defaults, feature flags, logging levels | Local, non-secure | JSON files | Built-in |
| Container/Kubernetes overrides | Local, non-secure | Environment variables | Built-in |
| Dev-only secrets like API keys and passwords | Local, secure | User Secrets | Built-in |
| Production secrets (Azure) | Remote, secure | Azure Key Vault | First-party NuGet |
| Production secrets (AWS) | Remote, secure | AWS Parameter Store | AWS-maintained NuGet |
| Production secrets (AWS, with rotation) | Remote, secure | AWS Secrets Manager | Community NuGet or custom |
| Shared config across many services | Remote, non-secure | Azure App Configuration, custom DB provider | First-party / custom |
| Unit and integration tests | In-memory | `AddInMemoryCollection` | Built-in |

For most production applications, the right combination is JSON files for non-sensitive defaults, environment variables for deployment-specific overrides, and a remote secret store like Azure Key Vault for anything sensitive. The provider ordering ensures that secrets from the remote store override any placeholder values in local files.
