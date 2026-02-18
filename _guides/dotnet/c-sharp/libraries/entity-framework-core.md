---
title: "Entity Framework Core"
layout: guide
category: ".NET & C#"
subcategory: "Core Libraries"
description: "Entity Framework Core fundamentals including DbContext, queries, relationships, migrations, and performance best practices."
tags: [c-sharp, dotnet, entity-framework, orm, database, data-access, practical]
---

## What is Entity Framework Core

Entity Framework Core (EF Core) is an object-relational mapper (ORM) that enables .NET developers to work with databases using .NET objects. It eliminates most data-access code that developers typically need to write.

```csharp
// Traditional SQL
var sql = "SELECT * FROM Customers WHERE Country = @Country";
var customers = connection.Query<Customer>(sql, new { Country = "USA" });

// EF Core - type-safe, refactor-friendly
var customers = await context.Customers
    .Where(c => c.Country == "USA")
    .ToListAsync();
```

## DbContext

The `DbContext` is the primary class for interacting with the database.

### Basic DbContext

```csharp
public class ApplicationDbContext : DbContext
{
    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<Product> Products => Set<Product>();

    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Configure entities
        modelBuilder.Entity<Customer>(entity =>
        {
            entity.HasKey(c => c.Id);
            entity.Property(c => c.Name).IsRequired().HasMaxLength(100);
            entity.HasIndex(c => c.Email).IsUnique();
        });
    }
}
```

### Registration (Dependency Injection)

```csharp
// Program.cs or Startup.cs
services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));

// With additional configuration
services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        sqlOptions.EnableRetryOnFailure(3);
        sqlOptions.CommandTimeout(30);
    });

    if (environment.IsDevelopment())
    {
        options.EnableSensitiveDataLogging();
        options.EnableDetailedErrors();
    }
});
```

## Entity Configuration

EF Core provides three ways to configure your model, listed here in order of precedence (highest to lowest):

1. **Fluent API**: Configuration in `OnModelCreating` or `IEntityTypeConfiguration<T>` classes
2. **Data Annotations**: Attributes applied directly to entity classes
3. **Conventions**: Automatic rules EF Core applies by default

When configurations conflict, higher precedence wins. For example, a Fluent API configuration overrides any Data Annotation on the same property.

<div class="comparison">
<div class="content-card content-card--accent">
<h4>Fluent API (Recommended)</h4>
<ul>
<li>Keeps domain models clean (POCOs)</li>
<li>More powerful (filtered indexes, cascade behavior)</li>
<li>Centralized configuration</li>
<li>Configuration classes can be unit tested</li>
</ul>
</div>
<div class="content-card content-card--accent-secondary">
<h4>Data Annotations</h4>
<ul>
<li>Dual-purpose validation (EF + ASP.NET)</li>
<li>Self-documenting entities</li>
<li>Less boilerplate for simple scenarios</li>
<li>Suitable for prototypes and simple CRUD apps</li>
</ul>
</div>
</div>

### Why Fluent API is Recommended

Microsoft recommends Fluent API as the primary configuration approach for several reasons:

**Keeps domain models clean**: Entity classes remain plain C# objects (POCOs) without infrastructure attributes. This matters when your domain layer shouldn't depend on EF Core or when the same classes are used across multiple contexts.

**More powerful**: Fluent API supports configurations that Data Annotations cannot express, including filtered indexes, cascade delete behavior, inheritance mapping strategies, and complex relationship configurations.

**Centralized configuration**: All database mapping lives in one place rather than scattered across entity classes. This makes it easier to review, modify, and understand the complete data model.

**Testability**: Configuration classes can be unit tested independently of the entities they configure.

### When Data Annotations Make Sense

Data Annotations still have valid uses:

**Dual-purpose validation**: Attributes like `[Required]` and `[MaxLength]` work with both EF Core and ASP.NET model validation. If you need the same constraint enforced at both layers, annotations avoid duplication.

**Self-documenting entities**: Seeing `[MaxLength(100)]` directly on a property communicates the constraint without looking elsewhere. This can help when entities are shared across teams.

**Simple scenarios**: For quick prototypes or straightforward CRUD applications where architectural purity isn't a priority, annotations reduce boilerplate.

### Data Annotations

```csharp
public class Customer
{
    public int Id { get; set; }

    [Required]
    [MaxLength(100)]
    public string Name { get; set; } = "";

    [EmailAddress]
    public string? Email { get; set; }

    [Column(TypeName = "decimal(18,2)")]
    public decimal CreditLimit { get; set; }

    [NotMapped]
    public string DisplayName => $"{Name} ({Email})";
}
```

### Fluent API

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Customer>(entity =>
    {
        entity.ToTable("Customers");
        entity.HasKey(c => c.Id);

        entity.Property(c => c.Name)
            .IsRequired()
            .HasMaxLength(100);

        entity.Property(c => c.Email)
            .HasMaxLength(255);

        entity.Property(c => c.CreditLimit)
            .HasPrecision(18, 2);

        entity.HasIndex(c => c.Email)
            .IsUnique()
            .HasFilter("[Email] IS NOT NULL");

        entity.Ignore(c => c.DisplayName);
    });
}
```

### Entity Type Configuration Classes

```csharp
public class CustomerConfiguration : IEntityTypeConfiguration<Customer>
{
    public void Configure(EntityTypeBuilder<Customer> builder)
    {
        builder.ToTable("Customers");
        builder.HasKey(c => c.Id);
        builder.Property(c => c.Name).IsRequired().HasMaxLength(100);
        builder.HasIndex(c => c.Email).IsUnique();
    }
}

// In OnModelCreating
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.ApplyConfiguration(new CustomerConfiguration());

    // Or apply all configurations from assembly
    modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
}
```

## Relationships

### One-to-Many

```csharp
public class Customer
{
    public int Id { get; set; }
    public string Name { get; set; }

    // Navigation property
    public ICollection<Order> Orders { get; set; } = new List<Order>();
}

public class Order
{
    public int Id { get; set; }
    public DateTime OrderDate { get; set; }

    // Foreign key
    public int CustomerId { get; set; }

    // Navigation property
    public Customer Customer { get; set; } = null!;
}

// Configuration
modelBuilder.Entity<Order>()
    .HasOne(o => o.Customer)
    .WithMany(c => c.Orders)
    .HasForeignKey(o => o.CustomerId)
    .OnDelete(DeleteBehavior.Cascade);
```

### One-to-One

```csharp
public class Customer
{
    public int Id { get; set; }
    public CustomerAddress? Address { get; set; }
}

public class CustomerAddress
{
    public int Id { get; set; }
    public string Street { get; set; }
    public int CustomerId { get; set; }
    public Customer Customer { get; set; } = null!;
}

// Configuration
modelBuilder.Entity<Customer>()
    .HasOne(c => c.Address)
    .WithOne(a => a.Customer)
    .HasForeignKey<CustomerAddress>(a => a.CustomerId);
```

### Many-to-Many

```csharp
public class Student
{
    public int Id { get; set; }
    public string Name { get; set; }
    public ICollection<Course> Courses { get; set; } = new List<Course>();
}

public class Course
{
    public int Id { get; set; }
    public string Title { get; set; }
    public ICollection<Student> Students { get; set; } = new List<Student>();
}

// EF Core 5+ automatically creates join table
// Or explicit join entity:
public class StudentCourse
{
    public int StudentId { get; set; }
    public Student Student { get; set; } = null!;
    public int CourseId { get; set; }
    public Course Course { get; set; } = null!;
    public DateTime EnrollmentDate { get; set; }
}
```

## Querying Data

### Basic Queries

```csharp
// Get all
var customers = await context.Customers.ToListAsync();

// Filter
var activeCustomers = await context.Customers
    .Where(c => c.IsActive)
    .ToListAsync();

// Find by primary key (cached if already tracked)
var customer = await context.Customers.FindAsync(id);

// Single result
var customer = await context.Customers
    .FirstOrDefaultAsync(c => c.Email == email);

// Projection
var names = await context.Customers
    .Select(c => c.Name)
    .ToListAsync();

// Anonymous type projection
var summaries = await context.Customers
    .Select(c => new { c.Id, c.Name, OrderCount = c.Orders.Count })
    .ToListAsync();
```

### Loading Related Data

```csharp
// Eager loading - single query with JOIN
var customers = await context.Customers
    .Include(c => c.Orders)
    .ThenInclude(o => o.OrderItems)
    .ToListAsync();

// Filtered include (EF Core 5+)
var customers = await context.Customers
    .Include(c => c.Orders.Where(o => o.Status == OrderStatus.Active))
    .ToListAsync();

// Explicit loading
var customer = await context.Customers.FindAsync(id);
await context.Entry(customer)
    .Collection(c => c.Orders)
    .LoadAsync();

// Lazy loading (requires proxy package)
// Navigation properties auto-load when accessed
```

### Pagination

```csharp
public async Task<PagedResult<Customer>> GetPagedAsync(int page, int pageSize)
{
    var query = context.Customers.AsQueryable();

    var totalCount = await query.CountAsync();
    var items = await query
        .OrderBy(c => c.Name)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();

    return new PagedResult<Customer>
    {
        Items = items,
        TotalCount = totalCount,
        Page = page,
        PageSize = pageSize
    };
}
```

### Raw SQL

```csharp
// Query with FromSqlRaw
var customers = await context.Customers
    .FromSqlRaw("SELECT * FROM Customers WHERE Country = {0}", country)
    .ToListAsync();

// Interpolated (parameterized)
var customers = await context.Customers
    .FromSqlInterpolated($"SELECT * FROM Customers WHERE Country = {country}")
    .ToListAsync();

// Non-query execution
await context.Database.ExecuteSqlRawAsync(
    "UPDATE Customers SET IsActive = 0 WHERE LastOrderDate < {0}",
    cutoffDate);
```

## Saving Data

### Adding Entities

```csharp
// Single entity
var customer = new Customer { Name = "Alice", Email = "alice@example.com" };
context.Customers.Add(customer);
await context.SaveChangesAsync();

// Multiple entities
var customers = new List<Customer>
{
    new() { Name = "Bob" },
    new() { Name = "Charlie" }
};
context.Customers.AddRange(customers);
await context.SaveChangesAsync();

// With related entities
var order = new Order
{
    Customer = new Customer { Name = "Alice" },
    Items = new List<OrderItem>
    {
        new() { ProductId = 1, Quantity = 2 }
    }
};
context.Orders.Add(order);
await context.SaveChangesAsync();
```

### Updating Entities

```csharp
// Tracked entity
var customer = await context.Customers.FindAsync(id);
customer.Name = "Updated Name";
await context.SaveChangesAsync();

// Disconnected entity
public async Task UpdateCustomerAsync(Customer customer)
{
    context.Customers.Update(customer);
    await context.SaveChangesAsync();
}

// Partial update
var customer = await context.Customers.FindAsync(id);
context.Entry(customer).Property(c => c.Name).IsModified = true;
await context.SaveChangesAsync();

// ExecuteUpdate (EF Core 7+) - bulk update without loading
await context.Customers
    .Where(c => c.IsActive == false)
    .ExecuteUpdateAsync(s => s
        .SetProperty(c => c.Status, "Archived")
        .SetProperty(c => c.ArchivedAt, DateTime.UtcNow));
```

### Deleting Entities

```csharp
// Tracked entity
var customer = await context.Customers.FindAsync(id);
context.Customers.Remove(customer);
await context.SaveChangesAsync();

// Without loading
var customer = new Customer { Id = id };
context.Customers.Remove(customer);
await context.SaveChangesAsync();

// ExecuteDelete (EF Core 7+) - bulk delete without loading
await context.Customers
    .Where(c => c.LastOrderDate < cutoffDate)
    .ExecuteDeleteAsync();
```

## Transactions

```csharp
// Implicit transaction (SaveChanges is transactional)
context.Customers.Add(new Customer { Name = "Alice" });
context.Orders.Add(new Order { CustomerId = 1 });
await context.SaveChangesAsync(); // Both or neither

// Explicit transaction
using var transaction = await context.Database.BeginTransactionAsync();
try
{
    var customer = new Customer { Name = "Alice" };
    context.Customers.Add(customer);
    await context.SaveChangesAsync();

    var order = new Order { CustomerId = customer.Id };
    context.Orders.Add(order);
    await context.SaveChangesAsync();

    await transaction.CommitAsync();
}
catch
{
    await transaction.RollbackAsync();
    throw;
}

// Transaction with execution strategy (for retries)
var strategy = context.Database.CreateExecutionStrategy();
await strategy.ExecuteAsync(async () =>
{
    using var transaction = await context.Database.BeginTransactionAsync();
    // ... operations
    await transaction.CommitAsync();
});
```

## Migrations

### Creating Migrations

```bash
# Create migration
dotnet ef migrations add InitialCreate

# With specific context
dotnet ef migrations add AddCustomerEmail -c ApplicationDbContext

# Generate SQL script
dotnet ef migrations script

# Apply migrations
dotnet ef database update
```

### Migration in Code

```csharp
// Apply pending migrations at startup
using var scope = app.Services.CreateScope();
var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
await context.Database.MigrateAsync();

// Or ensure database exists
await context.Database.EnsureCreatedAsync();
```

### Custom Migration Operations

```csharp
public partial class AddFullTextIndex : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql(@"
            CREATE FULLTEXT INDEX ON Products(Name, Description)
            KEY INDEX PK_Products");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql("DROP FULLTEXT INDEX ON Products");
    }
}
```

## Performance Best Practices

### No-Tracking Queries

```csharp
// When you don't need to modify entities
var customers = await context.Customers
    .AsNoTracking()
    .Where(c => c.IsActive)
    .ToListAsync();

// Global no-tracking
services.AddDbContext<ApplicationDbContext>(options =>
    options.UseQueryTrackingBehavior(QueryTrackingBehavior.NoTracking)
           .UseSqlServer(connectionString));
```

### Split Queries

```csharp
// Single query with Include can have Cartesian explosion
// Split into multiple queries
var customers = await context.Customers
    .Include(c => c.Orders)
    .ThenInclude(o => o.Items)
    .AsSplitQuery() // Generates multiple SQL queries
    .ToListAsync();

// Global split query behavior
modelBuilder.Entity<Customer>()
    .Navigation(c => c.Orders)
    .AutoInclude()
    .UsePropertyAccessMode(PropertyAccessMode.Property);
```

### Select Only What You Need

```csharp
// BAD - loads entire entity
var emails = await context.Customers
    .ToListAsync()
    .Select(c => c.Email);

// GOOD - SQL only selects Email
var emails = await context.Customers
    .Select(c => c.Email)
    .ToListAsync();

// DTO projection
var dtos = await context.Customers
    .Select(c => new CustomerDto
    {
        Id = c.Id,
        Name = c.Name,
        OrderCount = c.Orders.Count
    })
    .ToListAsync();
```

### Compiled Queries

```csharp
private static readonly Func<ApplicationDbContext, int, Task<Customer?>> GetCustomerById =
    EF.CompileAsyncQuery((ApplicationDbContext context, int id) =>
        context.Customers.FirstOrDefault(c => c.Id == id));

// Usage
var customer = await GetCustomerById(context, customerId);
```

### Avoid N+1 Problems

<div class="comparison">
<div class="content-card content-card--accent">
<h4>N+1 Problem (Bad)</h4>
<pre><code>// Triggers N+1 queries
var customers = await context.Customers
    .ToListAsync();
foreach (var customer in customers)
{
    // Each iteration = 1 query
    var orders = customer.Orders.ToList();
}</code></pre>
<p>Results in 1 query for customers + N queries for orders (one per customer).</p>
</div>
<div class="content-card content-card--accent-secondary">
<h4>Eager Loading (Good)</h4>
<pre><code>// Single query with JOIN
var customers = await context.Customers
    .Include(c => c.Orders)
    .ToListAsync();</code></pre>
<p>Results in 1 query that joins customers with orders.</p>
</div>
</div>

```csharp
// BAD - N+1 queries
var customers = await context.Customers.ToListAsync();
foreach (var customer in customers)
{
    // Each iteration triggers a query
    var orders = customer.Orders.ToList();
}

// GOOD - Single query with Include
var customers = await context.Customers
    .Include(c => c.Orders)
    .ToListAsync();

// Or explicit projection
var customerOrders = await context.Customers
    .Select(c => new
    {
        Customer = c,
        Orders = c.Orders.ToList()
    })
    .ToListAsync();
```

## Concurrency

```csharp
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public int Stock { get; set; }

    [Timestamp]
    public byte[] RowVersion { get; set; } = null!;
}

// Handling concurrency conflicts
try
{
    await context.SaveChangesAsync();
}
catch (DbUpdateConcurrencyException ex)
{
    foreach (var entry in ex.Entries)
    {
        var proposedValues = entry.CurrentValues;
        var databaseValues = await entry.GetDatabaseValuesAsync();

        // Client wins
        entry.OriginalValues.SetValues(databaseValues);

        // Or database wins
        entry.Reload();
    }
}
```

## Value Conversions

```csharp
modelBuilder.Entity<Order>()
    .Property(o => o.Status)
    .HasConversion(
        v => v.ToString(),           // To database
        v => Enum.Parse<OrderStatus>(v)); // From database

// Built-in converters
modelBuilder.Entity<Customer>()
    .Property(c => c.Tags)
    .HasConversion(
        v => JsonSerializer.Serialize(v, default(JsonSerializerOptions)),
        v => JsonSerializer.Deserialize<List<string>>(v, default(JsonSerializerOptions))!);

// Reusable converter
public class JsonValueConverter<T> : ValueConverter<T, string>
{
    public JsonValueConverter()
        : base(
            v => JsonSerializer.Serialize(v, default(JsonSerializerOptions)),
            v => JsonSerializer.Deserialize<T>(v, default(JsonSerializerOptions))!)
    {
    }
}
```

## Version History

| Feature | Version | Significance |
|---------|---------|--------------|
| EF Core | 1.0 | Cross-platform ORM |
| Global query filters | 2.0 | Automatic filtering |
| Owned entities | 2.0 | Value objects |
| Lazy loading | 2.1 | Automatic relation loading |
| Many-to-many | 5.0 | Skip navigation properties |
| Filtered includes | 5.0 | Include with Where |
| Split queries | 5.0 | Avoid Cartesian explosion |
| Compiled models | 6.0 | Faster startup |
| ExecuteUpdate/Delete | 7.0 | Bulk operations |
| JSON columns | 7.0 | Native JSON support |

## Key Takeaways

**Use AsNoTracking for read-only queries**: Significant performance improvement when you don't need to modify entities.

**Select projections over full entities**: Only load the columns you need.

**Use Include for related data**: Avoid N+1 queries by eagerly loading relationships.

**Understand change tracking**: EF tracks entities retrieved from the database and detects changes automatically.

**Use migrations for schema changes**: Migrations provide version control for your database schema.

**Handle concurrency**: Use row versions for optimistic concurrency in multi-user scenarios.

**Consider bulk operations**: ExecuteUpdate/Delete for large-scale changes without loading entities.
