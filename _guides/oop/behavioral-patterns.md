---
title: "Behavioral Patterns"
category: Object-Oriented Programming
---

---

> Behavioral patterns focus on communication between objects and define how objects interact and distribute responsibilities.

## Observer Pattern

**Purpose**: Define one-to-many dependency between objects so that state changes are automatically communicated.

**Traditional Observer**
```csharp
public interface IObserver
{
    void Update(string message);
}

public interface ISubject
{
    void Attach(IObserver observer);
    void Detach(IObserver observer);
    void Notify(string message);
}

public class NewsAgency : ISubject
{
    private readonly List<IObserver> observers = new();
    private string news;

    public string News
    {
        get => news;
        set
        {
            news = value;
            Notify(news);
        }
    }

    public void Attach(IObserver observer)
    {
        observers.Add(observer);
    }

    public void Detach(IObserver observer)
    {
        observers.Remove(observer);
    }

    public void Notify(string message)
    {
        foreach (var observer in observers)
        {
            observer.Update(message);
        }
    }
}

public class NewsChannel : IObserver
{
    private string channelName;

    public NewsChannel(string channelName)
    {
        this.channelName = channelName;
    }

    public void Update(string message)
    {
        Console.WriteLine($"{channelName} received news: {message}");
    }
}

// Usage:
var agency = new NewsAgency();
var cnn = new NewsChannel("CNN");
var bbc = new NewsChannel("BBC");

agency.Attach(cnn);
agency.Attach(bbc);

agency.News = "Breaking news: New technology announced!";
```

**Modern Event-Based Observer**
```csharp
public class ModernNewsAgency
{
    public event Action<string> NewsPublished;

    private string news;
    public string News
    {
        get => news;
        set
        {
            news = value;
            NewsPublished?.Invoke(news);
        }
    }
}

public class ModernNewsChannel
{
    private string channelName;

    public ModernNewsChannel(string channelName, ModernNewsAgency agency)
    {
        this.channelName = channelName;
        agency.NewsPublished += HandleNews;
    }

    private void HandleNews(string news)
    {
        Console.WriteLine($"{channelName} received news: {news}");
    }
}

// Usage:
var agency = new ModernNewsAgency();
var cnn = new ModernNewsChannel("CNN", agency);
var bbc = new ModernNewsChannel("BBC", agency);

agency.News = "Breaking news: Modern events working!";
```

## Strategy Pattern

**Purpose**: Define algorithms as interchangeable objects, enabling runtime selection.

**Dynamic Strategy**
```csharp
public enum OutputFormat
{
    Html,
    Markdown
}

public interface IListStrategy
{
    void Start(StringBuilder sb);
    void End(StringBuilder sb);
    void AddListItem(StringBuilder sb, string item);
}

public class HtmlListStrategy : IListStrategy
{
    public void Start(StringBuilder sb) => sb.AppendLine("<ul>");
    public void End(StringBuilder sb) => sb.AppendLine("</ul>");
    public void AddListItem(StringBuilder sb, string item) => sb.AppendLine($"  <li>{item}</li>");
}

public class MarkdownListStrategy : IListStrategy
{
    public void Start(StringBuilder sb) { } // No special start for markdown
    public void End(StringBuilder sb) { }   // No special end for markdown
    public void AddListItem(StringBuilder sb, string item) => sb.AppendLine($"- {item}");
}

public class TextProcessor
{
    private readonly StringBuilder sb = new();
    private IListStrategy listStrategy;

    public void SetOutputFormat(OutputFormat format)
    {
        listStrategy = format switch
        {
            OutputFormat.Html => new HtmlListStrategy(),
            OutputFormat.Markdown => new MarkdownListStrategy(),
            _ => throw new ArgumentException("Invalid format")
        };
    }

    public void AppendList(IEnumerable<string> items)
    {
        listStrategy.Start(sb);
        foreach (var item in items)
        {
            listStrategy.AddListItem(sb, item);
        }
        listStrategy.End(sb);
    }

    public override string ToString() => sb.ToString();
}

// Usage:
var processor = new TextProcessor();
processor.SetOutputFormat(OutputFormat.Html);
processor.AppendList(new[] { "Item 1", "Item 2", "Item 3" });
Console.WriteLine(processor.ToString());
```

## Command Pattern

**Purpose**: Encapsulate requests as objects, enabling queuing, logging, and undo operations.

```csharp
public interface ICommand
{
    void Execute();
    void Undo();
}

public class BankAccount
{
    public int Balance { get; private set; }

    public void Deposit(int amount)
    {
        Balance += amount;
        Console.WriteLine($"Deposited ${amount}, balance is now ${Balance}");
    }

    public void Withdraw(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            Console.WriteLine($"Withdrew ${amount}, balance is now ${Balance}");
        }
        else
        {
            Console.WriteLine("Insufficient funds");
        }
    }
}

public enum Action
{
    Deposit,
    Withdraw
}

public class BankAccountCommand : ICommand
{
    private BankAccount account;
    private Action action;
    private int amount;
    private bool succeeded;

    public BankAccountCommand(BankAccount account, Action action, int amount)
    {
        this.account = account;
        this.action = action;
        this.amount = amount;
    }

    public void Execute()
    {
        switch (action)
        {
            case Action.Deposit:
                account.Deposit(amount);
                succeeded = true;
                break;
            case Action.Withdraw:
                int balanceBefore = account.Balance;
                account.Withdraw(amount);
                succeeded = account.Balance != balanceBefore;
                break;
        }
    }

    public void Undo()
    {
        if (!succeeded) return;

        switch (action)
        {
            case Action.Deposit:
                account.Withdraw(amount);
                break;
            case Action.Withdraw:
                account.Deposit(amount);
                break;
        }
    }
}

// Command processor with undo/redo
public class CommandProcessor
{
    private readonly List<ICommand> commands = new();
    private int current = 0;

    public void Execute(ICommand command)
    {
        // Remove any commands after current position
        if (current < commands.Count)
        {
            commands.RemoveRange(current, commands.Count - current);
        }

        commands.Add(command);
        command.Execute();
        current++;
    }

    public void Undo()
    {
        if (current > 0)
        {
            current--;
            commands[current].Undo();
        }
    }

    public void Redo()
    {
        if (current < commands.Count)
        {
            commands[current].Execute();
            current++;
        }
    }
}

// Usage:
var account = new BankAccount();
var processor = new CommandProcessor();

processor.Execute(new BankAccountCommand(account, Action.Deposit, 100));
processor.Execute(new BankAccountCommand(account, Action.Withdraw, 50));
processor.Execute(new BankAccountCommand(account, Action.Withdraw, 25));

Console.WriteLine($"Final balance: ${account.Balance}");

processor.Undo(); // Undo last withdrawal
processor.Undo(); // Undo second withdrawal
processor.Redo(); // Redo second withdrawal
```

## State Pattern

**Purpose**: Allow objects to alter behavior when internal state changes.

**Modern Switch Expression Approach**
```csharp
public enum LightState
{
    Off,
    Low,
    High
}

public enum LightAction
{
    TurnOn,
    TurnOff,
    Brighten
}

public class ModernLight
{
    public LightState State { get; private set; } = LightState.Off;

    public void PerformAction(LightAction action)
    {
        var previousState = State;

        State = (State, action) switch
        {
            (LightState.Off, LightAction.TurnOn) => LightState.Low,
            (LightState.Low, LightAction.TurnOff) => LightState.Off,
            (LightState.Low, LightAction.Brighten) => LightState.High,
            (LightState.High, LightAction.TurnOff) => LightState.Off,
            (LightState.High, LightAction.Brighten) => LightState.High, // Stay high
            _ => State // No state change
        };

        if (previousState != State)
        {
            Console.WriteLine($"Light state changed from {previousState} to {State}");
        }
    }
}

// Usage:
var light = new ModernLight();
light.PerformAction(LightAction.TurnOn);  // Off -> Low
light.PerformAction(LightAction.Brighten); // Low -> High
light.PerformAction(LightAction.TurnOff);  // High -> Off
```

## Template Method Pattern

**Purpose**: Define algorithm skeleton in base class, allowing subclasses to override specific steps.

```csharp
public abstract class Game
{
    protected readonly int NumberOfPlayers;
    protected int CurrentPlayer = 0;

    protected Game(int numberOfPlayers)
    {
        NumberOfPlayers = numberOfPlayers;
    }

    // Template method
    public void Run()
    {
        Start();
        while (!HasWinner)
        {
            TakeTurn();
            CurrentPlayer = (CurrentPlayer + 1) % NumberOfPlayers;
        }
        Console.WriteLine($"Player {WinningPlayer} wins!");
    }

    protected abstract void Start();
    protected abstract void TakeTurn();
    protected abstract bool HasWinner { get; }
    protected abstract int WinningPlayer { get; }
}

public class Chess : Game
{
    private int turn = 1;
    private const int maxTurns = 10; // Simplified for example

    public Chess() : base(2) { }

    protected override void Start()
    {
        Console.WriteLine($"Starting a game of chess with {NumberOfPlayers} players");
    }

    protected override void TakeTurn()
    {
        Console.WriteLine($"Turn {turn++}: Player {CurrentPlayer} is thinking...");
    }

    protected override bool HasWinner => turn >= maxTurns;

    protected override int WinningPlayer => CurrentPlayer;
}

// Usage:
var chess = new Chess();
chess.Run();
```

## Chain of Responsibility Pattern

**Purpose**: Pass requests along a chain of handlers until one processes it.

```csharp
public abstract class Handler
{
    protected Handler nextHandler;

    public Handler SetNext(Handler handler)
    {
        nextHandler = handler;
        return handler;
    }

    public virtual string Handle(string request)
    {
        if (nextHandler != null)
        {
            return nextHandler.Handle(request);
        }

        return null;
    }
}

public class AuthenticationHandler : Handler
{
    public override string Handle(string request)
    {
        if (request == "authenticate")
        {
            return "Authentication handled";
        }

        return base.Handle(request);
    }
}

public class AuthorizationHandler : Handler
{
    public override string Handle(string request)
    {
        if (request == "authorize")
        {
            return "Authorization handled";
        }

        return base.Handle(request);
    }
}

public class ValidationHandler : Handler
{
    public override string Handle(string request)
    {
        if (request == "validate")
        {
            return "Validation handled";
        }

        return base.Handle(request);
    }
}

// Usage:
var auth = new AuthenticationHandler();
var authz = new AuthorizationHandler();
var validation = new ValidationHandler();

auth.SetNext(authz).SetNext(validation);

Console.WriteLine(auth.Handle("authenticate")); // "Authentication handled"
Console.WriteLine(auth.Handle("authorize"));    // "Authorization handled"
Console.WriteLine(auth.Handle("validate"));     // "Validation handled"
Console.WriteLine(auth.Handle("unknown"));      // null
```

## Mediator Pattern

**Purpose**: Define how objects interact through a mediator, reducing direct dependencies.

```csharp
public interface IChatRoom
{
    void SendMessage(string message, User user);
    void AddUser(User user);
    void RemoveUser(User user);
}

public class ChatRoom : IChatRoom
{
    private readonly List<User> users = new();

    public void AddUser(User user)
    {
        users.Add(user);
        Console.WriteLine($"{user.Name} joined the chat");
    }

    public void RemoveUser(User user)
    {
        users.Remove(user);
        Console.WriteLine($"{user.Name} left the chat");
    }

    public void SendMessage(string message, User sender)
    {
        foreach (var user in users.Where(u => u != sender))
        {
            user.Receive(message, sender.Name);
        }
    }
}

public abstract class User
{
    protected IChatRoom chatRoom;
    public string Name { get; }

    protected User(IChatRoom chatRoom, string name)
    {
        this.chatRoom = chatRoom;
        Name = name;
    }

    public abstract void Send(string message);
    public abstract void Receive(string message, string senderName);
}

public class ConcreteUser : User
{
    public ConcreteUser(IChatRoom chatRoom, string name) : base(chatRoom, name) { }

    public override void Send(string message)
    {
        Console.WriteLine($"{Name} sends: {message}");
        chatRoom.SendMessage(message, this);
    }

    public override void Receive(string message, string senderName)
    {
        Console.WriteLine($"{Name} receives from {senderName}: {message}");
    }
}

// Usage:
var chatRoom = new ChatRoom();
var john = new ConcreteUser(chatRoom, "John");
var jane = new ConcreteUser(chatRoom, "Jane");
var bob = new ConcreteUser(chatRoom, "Bob");

chatRoom.AddUser(john);
chatRoom.AddUser(jane);
chatRoom.AddUser(bob);

john.Send("Hello everyone!");
jane.Send("Hi John!");
```

## Iterator Pattern

**Purpose**: Provide a way to access elements of a collection sequentially without exposing its underlying representation.

```csharp
// Custom collection
public class WordCollection : IEnumerable<string>
{
    private readonly List<string> words = new();

    public void Add(string word) => words.Add(word);

    // Standard IEnumerable implementation
    public IEnumerator<string> GetEnumerator() => words.GetEnumerator();
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    // Custom iterator methods
    public IEnumerable<string> GetWordsStartingWith(char letter)
    {
        foreach (var word in words)
        {
            if (word.StartsWith(letter))
                yield return word;
        }
    }

    public IEnumerable<string> GetWordsInReverse()
    {
        for (int i = words.Count - 1; i >= 0; i--)
        {
            yield return words[i];
        }
    }
}

// Usage:
var collection = new WordCollection();
collection.Add("Apple");
collection.Add("Banana");
collection.Add("Cherry");
collection.Add("Avocado");

// Standard iteration
foreach (var word in collection)
{
    Console.WriteLine(word);
}

// Custom iterations
Console.WriteLine("Words starting with 'A':");
foreach (var word in collection.GetWordsStartingWith('A'))
{
    Console.WriteLine(word);
}
```

## Visitor Pattern

**Purpose**: Define operations on object hierarchies without modifying the objects themselves.

**⚠️ Complexity Warning**: Often indicates design issues that could be solved with simpler approaches.

**Modern Pattern Matching Approach (C# 8+)**
```csharp
public abstract record Expression;
public record Number(double Value) : Expression;
public record Addition(Expression Left, Expression Right) : Expression;

public static class ExpressionExtensions
{
    public static string Print(this Expression expression) =>
        expression switch
        {
            Number n => n.Value.ToString(),
            Addition a => $"({a.Left.Print()} + {a.Right.Print()})",
            _ => throw new ArgumentException("Unknown expression type")
        };

    public static double Evaluate(this Expression expression) =>
        expression switch
        {
            Number n => n.Value,
            Addition a => a.Left.Evaluate() + a.Right.Evaluate(),
            _ => throw new ArgumentException("Unknown expression type")
        };
}

// Usage:
var expression = new Addition(
    new Number(2),
    new Addition(new Number(3), new Number(4))
);

Console.WriteLine($"Expression: {expression.Print()}"); // (2 + (3 + 4))
Console.WriteLine($"Result: {expression.Evaluate()}");  // 9
```

## Memento Pattern

**Purpose**: Capture object state to enable rollback without violating encapsulation.

```csharp
// Memento
public class EditorMemento
{
    public string Content { get; }
    public int CursorPosition { get; }
    public DateTime Timestamp { get; }

    internal EditorMemento(string content, int cursorPosition)
    {
        Content = content;
        CursorPosition = cursorPosition;
        Timestamp = DateTime.Now;
    }
}

// Originator
public class TextEditor
{
    public string Content { get; private set; } = "";
    public int CursorPosition { get; private set; } = 0;

    public void Write(string text)
    {
        Content = Content.Insert(CursorPosition, text);
        CursorPosition += text.Length;
    }

    public void MoveCursor(int position)
    {
        CursorPosition = Math.Max(0, Math.Min(position, Content.Length));
    }

    public EditorMemento CreateMemento()
    {
        return new EditorMemento(Content, CursorPosition);
    }

    public void RestoreFromMemento(EditorMemento memento)
    {
        Content = memento.Content;
        CursorPosition = memento.CursorPosition;
    }
}

// Caretaker
public class EditorHistory
{
    private readonly Stack<EditorMemento> history = new();
    private readonly Stack<EditorMemento> redoStack = new();

    public void Save(EditorMemento memento)
    {
        history.Push(memento);
        redoStack.Clear(); // Clear redo stack when new state is saved
    }

    public EditorMemento Undo()
    {
        if (history.Count > 1) // Keep at least one state
        {
            var current = history.Pop();
            redoStack.Push(current);
            return history.Peek();
        }
        return null;
    }

    public EditorMemento Redo()
    {
        if (redoStack.Count > 0)
        {
            var memento = redoStack.Pop();
            history.Push(memento);
            return memento;
        }
        return null;
    }
}

// Usage:
var editor = new TextEditor();
var history = new EditorHistory();

// Save initial state
history.Save(editor.CreateMemento());

editor.Write("Hello ");
history.Save(editor.CreateMemento());

editor.Write("World");
history.Save(editor.CreateMemento());

editor.Write("!");
Console.WriteLine($"Current: '{editor.Content}'"); // Current: 'Hello World!'

// Undo
var previousState = history.Undo();
if (previousState != null)
{
    editor.RestoreFromMemento(previousState);
    Console.WriteLine($"After undo: '{editor.Content}'"); // After undo: 'Hello World'
}
```

## Interpreter Pattern

**Purpose**: Define a grammar for a language and provide an interpreter to process sentences in that language.

```csharp
// Abstract expression
public interface IExpression
{
    int Interpret(Dictionary<char, int> variables);
}

// Terminal expressions
public class NumberExpression : IExpression
{
    private readonly int number;

    public NumberExpression(int number)
    {
        this.number = number;
    }

    public int Interpret(Dictionary<char, int> variables) => number;
}

public class VariableExpression : IExpression
{
    private readonly char variable;

    public VariableExpression(char variable)
    {
        this.variable = variable;
    }

    public int Interpret(Dictionary<char, int> variables) =>
        variables.ContainsKey(variable) ? variables[variable] : 0;
}

// Non-terminal expressions
public class AddExpression : IExpression
{
    private readonly IExpression left;
    private readonly IExpression right;

    public AddExpression(IExpression left, IExpression right)
    {
        this.left = left;
        this.right = right;
    }

    public int Interpret(Dictionary<char, int> variables) =>
        left.Interpret(variables) + right.Interpret(variables);
}

public class SubtractExpression : IExpression
{
    private readonly IExpression left;
    private readonly IExpression right;

    public SubtractExpression(IExpression left, IExpression right)
    {
        this.left = left;
        this.right = right;
    }

    public int Interpret(Dictionary<char, int> variables) =>
        left.Interpret(variables) - right.Interpret(variables);
}

// Usage:
var variables = new Dictionary<char, int>
{
    { 'x', 10 },
    { 'y', 5 }
};

// Create expression: x + y - 3
var expression = new SubtractExpression(
    new AddExpression(
        new VariableExpression('x'),
        new VariableExpression('y')
    ),
    new NumberExpression(3)
);

var result = expression.Interpret(variables);
Console.WriteLine($"Result: {result}"); // Result: 12 (10 + 5 - 3)
```

## Null Object Pattern

**Purpose**: Provide a default object that exhibits neutral behavior instead of using null references.

```csharp
// Abstract interface
public interface ILogger
{
    void Log(string message);
    void LogError(string error);
}

// Real implementation
public class FileLogger : ILogger
{
    private readonly string filePath;

    public FileLogger(string filePath)
    {
        this.filePath = filePath;
    }

    public void Log(string message)
    {
        File.AppendAllText(filePath, $"{DateTime.Now}: {message}\n");
    }

    public void LogError(string error)
    {
        File.AppendAllText(filePath, $"{DateTime.Now} ERROR: {error}\n");
    }
}

// Null object implementation
public class NullLogger : ILogger
{
    public void Log(string message)
    {
        // Do nothing
    }

    public void LogError(string error)
    {
        // Do nothing
    }
}

// Service that uses logger
public class UserService
{
    private readonly ILogger logger;

    public UserService(ILogger logger = null)
    {
        // Use null object instead of null checks
        this.logger = logger ?? new NullLogger();
    }

    public void CreateUser(string userName)
    {
        // No null checks needed
        logger.Log($"Creating user: {userName}");

        try
        {
            // User creation logic
            Console.WriteLine($"User {userName} created");
            logger.Log($"User {userName} created successfully");
        }
        catch (Exception ex)
        {
            logger.LogError($"Failed to create user {userName}: {ex.Message}");
            throw;
        }
    }
}

// Usage:
var userServiceWithLogger = new UserService(new FileLogger("app.log"));
userServiceWithLogger.CreateUser("John");

var userServiceWithoutLogger = new UserService(); // Uses NullLogger
userServiceWithoutLogger.CreateUser("Jane");
```

---