---
title: "Networking and Remote Communication"
layout: guide
category: "WinUI 3"
subcategory: "Platform Integration"
description: "Making HTTP requests, calling gRPC services, and establishing WebSocket connections in WinUI 3 desktop applications using standard .NET networking libraries."
tags: [winui, winui-3, networking, http, grpc, websocket, desktop, practical]
---

## Networking in WinUI 3

WinUI 3 runs on full .NET, which means every networking library available to a console app or ASP.NET service is equally available to your desktop application. This is a significant departure from UWP, which imposed a capability model and sandbox restrictions that limited what networking operations were possible without explicit declarations in the app manifest. A WinUI 3 application can open raw sockets, use `HttpClient` freely, establish WebSocket connections, and connect to gRPC services without any special configuration beyond adding the relevant NuGet packages.

The practical implication is that patterns and libraries that .NET developers are already familiar with from server-side work translate directly. If you have written `HttpClient` code in ASP.NET Core, that code works in WinUI 3 without modification. The same applies to Polly for resilience, `Grpc.Net.Client` for remote procedure calls, and `ClientWebSocket` for persistent connections. Desktop-specific concerns, such as thread marshaling to update the UI from network callbacks, are real but manageable with `async/await` and `DispatcherQueue`.

---

## Making HTTP Requests with HttpClient

[HttpClient](https://learn.microsoft.com/en-us/dotnet/api/system.net.http.httpclient){:target="_blank" rel="noopener noreferrer"} is the standard class for making HTTP requests in .NET. The most important thing to understand about `HttpClient` is its intended lifetime: it is designed to be long-lived and reused across many requests, not created and disposed per-request. Creating a new `HttpClient` for each request exhausts socket connections due to TIME_WAIT states and degrades performance under load.

The correct way to manage `HttpClient` lifetime in a WinUI 3 application is through `IHttpClientFactory`, which is part of [Microsoft.Extensions.Http](https://www.nuget.org/packages/Microsoft.Extensions.Http){:target="_blank" rel="noopener noreferrer"}. The factory manages a pool of `HttpMessageHandler` instances, handles their lifecycle to avoid socket exhaustion, and allows you to configure named or typed clients with base addresses and default headers.

```csharp
// Register in App.xaml.cs or with the generic host
services.AddHttpClient("WeatherApi", client =>
{
    client.BaseAddress = new Uri("https://api.weather.example.com/");
    client.DefaultRequestHeaders.Add("Accept", "application/json");
    client.Timeout = TimeSpan.FromSeconds(30);
});

// Or use a typed client
services.AddHttpClient<IWeatherService, WeatherService>(client =>
{
    client.BaseAddress = new Uri("https://api.weather.example.com/");
});
```

A typed client wraps `HttpClient` and is registered as a transient service, though the underlying handler is pooled. This is the cleanest pattern for WinUI 3 because it integrates with the DI container and keeps networking logic out of ViewModels.

```csharp
public class WeatherService : IWeatherService
{
    private readonly HttpClient _client;

    public WeatherService(HttpClient client)
    {
        _client = client;
    }

    public async Task<WeatherForecast?> GetForecastAsync(string city, CancellationToken ct = default)
    {
        var response = await _client.GetAsync($"forecast?city={Uri.EscapeDataString(city)}", ct);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<WeatherForecast>(cancellationToken: ct);
    }
}
```

`ReadFromJsonAsync` is an extension method from [System.Net.Http.Json](https://learn.microsoft.com/en-us/dotnet/api/system.net.http.json){:target="_blank" rel="noopener noreferrer"} that deserializes the response body using `System.Text.Json`. For POST requests with a JSON body, the equivalent is `PostAsJsonAsync`, which serializes the object and sets the `Content-Type` header automatically.

For authentication, the standard approach is to add an `Authorization` header. Bearer token authentication is common when calling APIs that use OAuth 2.0 or JWT tokens.

```csharp
public async Task<T?> GetAuthorizedAsync<T>(string path, string bearerToken, CancellationToken ct = default)
{
    using var request = new HttpRequestMessage(HttpMethod.Get, path);
    request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", bearerToken);
    var response = await _client.SendAsync(request, ct);
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadFromJsonAsync<T>(cancellationToken: ct);
}
```

For APIs that use API keys, you can either set a default header when configuring the client in the factory, or add the key as a query parameter per request depending on the API's requirements.

---

## Resilience and Retry Policies

Network calls fail. Servers return 503 responses under load, connections time out in flaky Wi-Fi environments, and transient faults resolve themselves if retried after a short delay. Building retry logic directly into service methods produces repetitive, inconsistent code that is hard to test and easy to get wrong.

[Polly](https://github.com/App-vNext/Polly){:target="_blank" rel="noopener noreferrer"} is the standard library for resilience in the .NET ecosystem. It provides composable policies for retries with exponential backoff, circuit breakers that stop calling a failing service, timeouts, and bulkheads that limit concurrency. Polly integrates cleanly with `IHttpClientFactory` through the `Microsoft.Extensions.Http.Polly` package.

```csharp
services.AddHttpClient<IWeatherService, WeatherService>(client =>
{
    client.BaseAddress = new Uri("https://api.weather.example.com/");
})
.AddTransientHttpErrorPolicy(builder =>
    builder.WaitAndRetryAsync(
        retryCount: 3,
        sleepDurationProvider: attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)),
        onRetry: (outcome, timeSpan, retryCount, context) =>
        {
            Debug.WriteLine($"Retry {retryCount} after {timeSpan.TotalSeconds}s");
        }))
.AddTransientHttpErrorPolicy(builder =>
    builder.CircuitBreakerAsync(
        handledEventsAllowedBeforeBreaking: 5,
        durationOfBreak: TimeSpan.FromSeconds(30)));
```

`AddTransientHttpErrorPolicy` applies the policy to responses that represent transient failures: HTTP 5xx responses and network-level exceptions. The circuit breaker pattern is particularly useful in desktop applications because it prevents the UI from hanging on repeated calls to a service that is down; after five consecutive failures the circuit opens and subsequent calls fail fast without attempting the network operation.

Microsoft also ships [Microsoft.Extensions.Http.Resilience](https://www.nuget.org/packages/Microsoft.Extensions.Http.Resilience){:target="_blank" rel="noopener noreferrer"}, which provides a higher-level API built on top of Polly through the `AddStandardResilienceHandler()` extension. This applies a sensible default configuration including rate limiters, retries, and circuit breaking with a single method call, which is appropriate when you want consistent behavior without tuning each policy individually.

```csharp
services.AddHttpClient<IWeatherService, WeatherService>()
    .AddStandardResilienceHandler();
```

---

## gRPC Services

[gRPC](https://grpc.io){:target="_blank" rel="noopener noreferrer"} is a high-performance remote procedure call framework that uses Protocol Buffers for serialization and HTTP/2 for transport. Compared to REST, gRPC provides strongly-typed contracts defined in `.proto` files, efficient binary serialization, and built-in support for streaming scenarios. It is well suited for communication with backend microservices where performance matters and the schema is shared between client and server.

WinUI 3 applications use gRPC through [Grpc.Net.Client](https://www.nuget.org/packages/Grpc.Net.Client){:target="_blank" rel="noopener noreferrer"}, which is the .NET implementation of the gRPC client. You define the service contract in a `.proto` file, add the file to the project with a `<Protobuf>` build item, and the Grpc tooling generates C# client classes at build time.

```protobuf
// weather.proto
syntax = "proto3";
option csharp_namespace = "WeatherApp.Grpc";

service WeatherService {
  rpc GetForecast (ForecastRequest) returns (ForecastReply);
  rpc StreamForecasts (ForecastRequest) returns (stream ForecastReply);
}

message ForecastRequest {
  string city = 1;
}

message ForecastReply {
  string summary = 1;
  float temperature_c = 2;
}
```

```xml
<!-- In the .csproj file -->
<ItemGroup>
  <Protobuf Include="Protos\weather.proto" GrpcServices="Client" />
</ItemGroup>
```

After building, the generated `WeatherService.WeatherServiceClient` class is available. You create a channel to the server address and instantiate the client from that channel.

```csharp
using Grpc.Net.Client;
using WeatherApp.Grpc;

public class GrpcWeatherService : IWeatherService
{
    private readonly WeatherServiceClient _client;

    public GrpcWeatherService(GrpcChannel channel)
    {
        _client = new WeatherServiceClient(channel);
    }

    public async Task<ForecastReply> GetForecastAsync(string city, CancellationToken ct = default)
    {
        return await _client.GetForecastAsync(
            new ForecastRequest { City = city },
            cancellationToken: ct);
    }
}
```

Streaming scenarios are where gRPC demonstrates its advantage over request-response HTTP. A server-streaming RPC allows the server to push multiple messages to the client after a single request, which is useful for progressively loading large datasets or receiving live updates.

```csharp
public async IAsyncEnumerable<ForecastReply> StreamForecastsAsync(
    string city,
    [EnumeratorCancellation] CancellationToken ct = default)
{
    using var call = _client.StreamForecasts(new ForecastRequest { City = city });
    await foreach (var reply in call.ResponseStream.ReadAllAsync(ct))
    {
        yield return reply;
    }
}
```

The `GrpcChannel` is expensive to create and should be registered as a singleton in the DI container. If the server address is known at startup, create the channel once during service registration and inject it into the client service.

```csharp
services.AddSingleton(GrpcChannel.ForAddress("https://api.example.com"));
services.AddSingleton<IWeatherService, GrpcWeatherService>();
```

---

## WebSocket Connections

WebSockets provide a persistent, full-duplex communication channel over a single TCP connection. Unlike HTTP, where each request-response pair is independent, a WebSocket connection stays open and allows either side to send messages at any time. This makes WebSockets appropriate for scenarios like chat, live dashboards displaying real-time metrics, multiplayer game state, and collaborative document editing.

The .NET standard library includes [ClientWebSocket](https://learn.microsoft.com/en-us/dotnet/api/system.net.websockets.clientwebsocket){:target="_blank" rel="noopener noreferrer"}, which handles connection lifecycle, message sending, and receiving.

```csharp
public class WebSocketClient : IAsyncDisposable
{
    private readonly ClientWebSocket _socket = new();

    public async Task ConnectAsync(Uri serverUri, CancellationToken ct = default)
    {
        await _socket.ConnectAsync(serverUri, ct);
    }

    public async Task SendAsync(string message, CancellationToken ct = default)
    {
        var buffer = Encoding.UTF8.GetBytes(message);
        await _socket.SendAsync(
            new ArraySegment<byte>(buffer),
            WebSocketMessageType.Text,
            endOfMessage: true,
            ct);
    }

    public async IAsyncEnumerable<string> ReceiveAsync(
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        var buffer = new byte[4096];
        while (_socket.State == WebSocketState.Open)
        {
            var result = await _socket.ReceiveAsync(new ArraySegment<byte>(buffer), ct);
            if (result.MessageType == WebSocketMessageType.Close)
            {
                await _socket.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, ct);
                yield break;
            }
            yield return Encoding.UTF8.GetString(buffer, 0, result.Count);
        }
    }

    public async ValueTask DisposeAsync()
    {
        if (_socket.State == WebSocketState.Open)
        {
            await _socket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", CancellationToken.None);
        }
        _socket.Dispose();
    }
}
```

The receive loop runs continuously until the connection closes or the cancellation token is triggered. In a WinUI 3 application, you typically start this loop as a background operation when the user opens a page that requires live data, and cancel it when they navigate away.

One practical consideration is reconnection. WebSocket connections drop due to network interruptions, server restarts, and timeouts from idle connections. Building reconnection logic into the client service, with exponential backoff similar to the HTTP retry pattern, prevents the application from silently losing its live data feed.

---

## SignalR Client

[SignalR](https://learn.microsoft.com/en-us/aspnet/core/signalr/introduction){:target="_blank" rel="noopener noreferrer"} is an ASP.NET Core library that abstracts real-time communication behind a Hub concept. From the client perspective, SignalR handles transport negotiation (preferring WebSockets but falling back to Server-Sent Events or long polling), connection management, and serialization. If your backend uses SignalR, the client library provides a more ergonomic API than working with raw WebSockets.

The client package is [Microsoft.AspNetCore.SignalR.Client](https://www.nuget.org/packages/Microsoft.AspNetCore.SignalR.Client){:target="_blank" rel="noopener noreferrer"}. You build a connection with `HubConnectionBuilder`, specifying the hub URL and any authentication or retry configuration.

```csharp
var connection = new HubConnectionBuilder()
    .WithUrl("https://api.example.com/hubs/dashboard", options =>
    {
        options.AccessTokenProvider = () => Task.FromResult<string?>(GetAccessToken());
    })
    .WithAutomaticReconnect()
    .Build();
```

`WithAutomaticReconnect()` handles the reconnection loop transparently, retrying with delays of 0, 2, 10, and 30 seconds by default. You can supply a custom retry policy through an `IRetryPolicy` implementation if you need different intervals.

Subscribing to messages from the hub uses the `On` method, which registers a handler for a named method the server can invoke on connected clients.

```csharp
connection.On<DashboardUpdate>("ReceiveUpdate", update =>
{
    // This callback may run on a thread pool thread; dispatch to the UI thread before updating bindings
    _dispatcherQueue.TryEnqueue(() =>
    {
        MetricValue = update.Value;
        LastUpdated = update.Timestamp;
    });
});

await connection.StartAsync();
```

To invoke methods on the hub from the client, use `InvokeAsync` for calls that return a result or `SendAsync` for fire-and-forget operations.

```csharp
// Invoke and wait for a result
var history = await connection.InvokeAsync<List<DataPoint>>("GetHistory", "cpu");

// Send without waiting for a return value
await connection.SendAsync("Subscribe", "cpu", "memory");
```

The connection object should be held for the lifetime of the feature using it. Register it as a singleton if the hub connection spans the entire application, or manage it as a per-page resource that connects on `OnNavigatedTo` and disconnects on `OnNavigatedFrom`.

---

## Thread Marshaling for UI Updates

Networking calls in .NET are asynchronous and complete on thread pool threads. In WinUI 3, UI elements can only be accessed from the thread they were created on, which is the UI thread. Accessing a data-bound property or modifying a collection from a thread pool thread throws an `InvalidOperationException`.

The good news is that `async/await` handles the common case automatically. When you `await` an async method inside a page or ViewModel that was created on the UI thread, execution resumes on the UI thread after the awaited call completes, provided there is a synchronization context installed. WinUI 3 installs a `DispatcherQueueSynchronizationContext` on the UI thread, so the following works without any additional marshaling.

```csharp
// This runs on the UI thread; await returns to the UI thread automatically
private async Task LoadDataAsync()
{
    IsLoading = true;
    var results = await _weatherService.GetForecastAsync("Seattle"); // thread pool
    Forecasts = new ObservableCollection<Forecast>(results);         // back on UI thread
    IsLoading = false;
}
```

Manual marshaling is necessary when callbacks arrive outside the `async/await` chain, such as in event handlers registered with `ClientWebSocket.ReceiveAsync` results, SignalR hub message handlers, or timer callbacks. In these cases, use `DispatcherQueue.TryEnqueue` to schedule work on the UI thread.

```csharp
// Obtaining DispatcherQueue in a ViewModel
private readonly DispatcherQueue _dispatcherQueue = DispatcherQueue.GetForCurrentThread();

// Marshaling from a background callback
_webSocketClient.OnMessage += message =>
{
    _dispatcherQueue.TryEnqueue(() =>
    {
        Messages.Add(message);
    });
};
```

`DispatcherQueue.GetForCurrentThread()` must be called from the UI thread to capture the correct queue. Call it in the ViewModel constructor or in the Page constructor and store it as a field. Calling it from a background thread returns null or an unrelated queue.

For ObservableCollections specifically, modifications from a background thread throw even when using `async/await`, because collections fire change notifications synchronously. If you need to populate a collection from a streaming source, batch the updates and marshal them through `TryEnqueue`.

---

## Connectivity Detection and Offline Design

A desktop application running on a laptop faces intermittent connectivity as a normal operating condition, not an edge case. Users disconnect from Wi-Fi, switch between networks, and resume from sleep with the application still running. Designing for this requires both detecting connectivity changes and choosing how the application behaves when the network is unavailable.

[NetworkInformation](https://learn.microsoft.com/en-us/dotnet/api/windows.networking.connectivity.networkinformation){:target="_blank" rel="noopener noreferrer"} is a Windows Runtime API available to WinUI 3 applications that reports the current connectivity state and fires events when it changes.

```csharp
public class ConnectivityService : IConnectivityService
{
    public bool IsConnected => GetIsConnected();

    public ConnectivityService()
    {
        NetworkInformation.NetworkStatusChanged += OnNetworkStatusChanged;
    }

    private static bool GetIsConnected()
    {
        var profile = NetworkInformation.GetInternetConnectionProfile();
        return profile?.GetNetworkConnectivityLevel() == NetworkConnectivityLevel.InternetAccess;
    }

    private void OnNetworkStatusChanged(object sender)
    {
        var connected = GetIsConnected();
        ConnectivityChanged?.Invoke(this, connected);
    }

    public event EventHandler<bool>? ConnectivityChanged;
}
```

Note that `NetworkStatusChanged` fires on an arbitrary thread, so handlers that update the UI must marshal to the UI thread through `DispatcherQueue`.

Beyond detection, the design question is what the application should do when connectivity is lost. For applications with local data, continuing to display cached content while showing a subtle offline indicator is preferable to blocking the UI entirely. Queue writes and sync operations for when connectivity is restored, rather than surfacing errors that the user cannot act on. If the application makes a network call during an offline period, catching `HttpRequestException` or `SocketException` and returning a cached or empty result allows the UI to remain functional.

Cancellation tokens connect the connectivity story to the request lifecycle. Passing a `CancellationToken` to every async network call and canceling that token when the application loses connectivity, or when the user navigates away, prevents background requests from continuing unnecessarily and avoids the complexity of racing callbacks that arrive after the relevant UI has been torn down.
