---
title: "The Result Pattern"
category: Object-Oriented Programming
---

---

**Purpose**: Provide a functional alternative to throwing exceptions for error handling, making failure cases explicit in the return type.

## Basic Result Pattern

```csharp
// Basic Result class
public class Result<T>
{
    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public T Value { get; }
    public string Error { get; }

    private Result(bool isSuccess, T value, string error)
    {
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
    }

    public static Result<T> Success(T value) => new(true, value, null);
    public static Result<T> Failure(string error) => new(false, default(T), error);

    // Implicit conversion from T to Result<T>
    public static implicit operator Result<T>(T value) => Success(value);

    // Pattern matching support
    public void Match(Action<T> onSuccess, Action<string> onFailure)
    {
        if (IsSuccess)
            onSuccess(Value);
        else
            onFailure(Error);
    }

    public TResult Match<TResult>(Func<T, TResult> onSuccess, Func<string, TResult> onFailure)
    {
        return IsSuccess ? onSuccess(Value) : onFailure(Error);
    }
}

// Non-generic Result for operations that don't return a value
public class Result
{
    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public string Error { get; }

    private Result(bool isSuccess, string error)
    {
        IsSuccess = isSuccess;
        Error = error;
    }

    public static Result Success() => new(true, null);
    public static Result Failure(string error) => new(false, error);

    public void Match(Action onSuccess, Action<string> onFailure)
    {
        if (IsSuccess)
            onSuccess();
        else
            onFailure(Error);
    }
}
```

## Enhanced Result Pattern with Multiple Errors

```csharp
public class Result<T>
{
    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public T Value { get; }
    public IReadOnlyList<string> Errors { get; }

    private Result(bool isSuccess, T value, IEnumerable<string> errors)
    {
        IsSuccess = isSuccess;
        Value = value;
        Errors = errors?.ToList().AsReadOnly() ?? new List<string>().AsReadOnly();
    }

    public static Result<T> Success(T value) => new(true, value, null);
    public static Result<T> Failure(string error) => new(false, default(T), new[] { error });
    public static Result<T> Failure(IEnumerable<string> errors) => new(false, default(T), errors);

    // Combine multiple results
    public static Result<IEnumerable<T>> Combine(params Result<T>[] results)
    {
        var failures = results.Where(r => r.IsFailure).ToList();
        if (failures.Any())
        {
            var allErrors = failures.SelectMany(f => f.Errors);
            return Result<IEnumerable<T>>.Failure(allErrors);
        }

        var values = results.Select(r => r.Value);
        return Result<IEnumerable<T>>.Success(values);
    }

    // Functional operations
    public Result<TResult> Map<TResult>(Func<T, TResult> func)
    {
        if (IsFailure)
            return Result<TResult>.Failure(Errors);

        try
        {
            return Result<TResult>.Success(func(Value));
        }
        catch (Exception ex)
        {
            return Result<TResult>.Failure(ex.Message);
        }
    }

    public Result<TResult> Bind<TResult>(Func<T, Result<TResult>> func)
    {
        if (IsFailure)
            return Result<TResult>.Failure(Errors);

        return func(Value);
    }
}
```

## Real-World Usage Examples

```csharp
public class UserService
{
    private readonly IUserRepository userRepository;
    private readonly IEmailService emailService;

    public UserService(IUserRepository userRepository, IEmailService emailService)
    {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }

    public Result<User> CreateUser(CreateUserRequest request)
    {
        // Validation
        var validationResult = ValidateCreateUserRequest(request);
        if (validationResult.IsFailure)
            return Result<User>.Failure(validationResult.Errors);

        // Check if user already exists
        var existingUser = userRepository.FindByEmail(request.Email);
        if (existingUser != null)
            return Result<User>.Failure("User with this email already exists");

        // Create user
        var user = new User
        {
            Id = Guid.NewGuid(),
            Email = request.Email,
            Name = request.Name,
            CreatedAt = DateTime.UtcNow
        };

        // Save to database
        var saveResult = userRepository.Save(user);
        if (saveResult.IsFailure)
            return Result<User>.Failure(saveResult.Error);

        // Send welcome email (failure here doesn't fail the whole operation)
        emailService.SendWelcomeEmail(user.Email, user.Name);

        return Result<User>.Success(user);
    }

    private Result ValidateCreateUserRequest(CreateUserRequest request)
    {
        var errors = new List<string>();

        if (string.IsNullOrWhiteSpace(request.Email))
            errors.Add("Email is required");
        else if (!IsValidEmail(request.Email))
            errors.Add("Email format is invalid");

        if (string.IsNullOrWhiteSpace(request.Name))
            errors.Add("Name is required");
        else if (request.Name.Length < 2)
            errors.Add("Name must be at least 2 characters");

        return errors.Any()
            ? Result.Failure(string.Join("; ", errors))
            : Result.Success();
    }

    private bool IsValidEmail(string email)
    {
        try
        {
            var addr = new System.Net.Mail.MailAddress(email);
            return addr.Address == email;
        }
        catch
        {
            return false;
        }
    }
}

// Usage
public class UserController
{
    private readonly UserService userService;

    public UserController(UserService userService)
    {
        this.userService = userService;
    }

    public IActionResult CreateUser(CreateUserRequest request)
    {
        var result = userService.CreateUser(request);

        return result.Match<IActionResult>(
            onSuccess: user => Ok(new { UserId = user.Id, Message = "User created successfully" }),
            onFailure: error => BadRequest(new { Error = error })
        );
    }
}
```

## Railway-Oriented Programming with Results

```csharp
public static class ResultExtensions
{
    // Chain operations together - continues only if all succeed
    public static Result<TResult> Then<T, TResult>(this Result<T> result, Func<T, Result<TResult>> next)
    {
        return result.IsSuccess ? next(result.Value) : Result<TResult>.Failure(result.Errors);
    }

    // Transform the value if successful
    public static Result<TResult> Select<T, TResult>(this Result<T> result, Func<T, TResult> selector)
    {
        return result.Map(selector);
    }

    // Tap - perform side effects without changing the result
    public static Result<T> Tap<T>(this Result<T> result, Action<T> action)
    {
        if (result.IsSuccess)
            action(result.Value);
        return result;
    }

    // Ensure - add additional validation
    public static Result<T> Ensure<T>(this Result<T> result, Func<T, bool> predicate, string error)
    {
        if (result.IsFailure)
            return result;

        return predicate(result.Value)
            ? result
            : Result<T>.Failure(error);
    }
}

// Railway-oriented example
public Result<string> ProcessOrder(CreateOrderRequest request)
{
    return ValidateOrderRequest(request)
        .Then(req => CreateOrder(req))
        .Then(order => ReserveInventory(order))
        .Then(order => ProcessPayment(order))
        .Tap(order => SendConfirmationEmail(order.CustomerEmail))
        .Then(order => Result<string>.Success($"Order {order.Id} processed successfully"));
}
```

## Benefits of Result Pattern

**Explicit Error Handling**
- Makes failure cases explicit in method signatures
- Forces callers to handle potential failures
- Reduces unexpected runtime exceptions

**Functional Composition**
- Enables railway-oriented programming
- Allows chaining operations that can fail
- Provides clean separation between success and failure paths

**Better Testing**
- Easier to test error conditions
- No need to catch exceptions in tests
- Clear assertion of success vs failure states

**Performance**
- Avoids expensive exception throwing and stack unwinding
- More predictable performance characteristics
- Better for hot code paths

## When to Use Result Pattern vs Exceptions

**Use Result Pattern for:**
- Expected failure cases (validation errors, business rule violations)
- Operations where failure is part of normal flow
- High-performance scenarios where exceptions are costly
- Functional programming approaches
- API boundaries where you want explicit error contracts

**Use Exceptions for:**
- Truly exceptional conditions (system failures, programming errors)
- Unrecoverable errors
- Third-party library integration where exceptions are expected
- When integrating with existing exception-based codebases

---