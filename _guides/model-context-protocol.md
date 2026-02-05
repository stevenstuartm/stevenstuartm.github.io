---
title: "Model Context Protocol (MCP)"
layout: guide
category: AI & Machine Learning
subcategory: Generative AI
description: "Understanding MCP: the open protocol for connecting AI models to external data sources and tools, enabling richer context and agentic capabilities."
tags: [ai, generative-ai, llm, mcp, integration, tools, practical]
---

## What Is MCP?

Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to large language models. Think of it as a universal adapter between AI models and the data sources, tools, and services they need to access.

**The core problem MCP solves**: Every AI application needs to connect to external systems (databases, APIs, file systems, services). Without a standard protocol, each integration is custom-built, creating fragmentation and duplication of effort.

### The Analogy

MCP is to AI context what USB is to peripherals. Before USB, every device needed its own connector and driver. USB standardized the interface, and suddenly any device could work with any computer. MCP aims to do the same for AI-to-tool connections.

### Key Benefits

| Benefit | Description |
|---------|-------------|
| **Standardization** | One protocol instead of custom integrations per tool |
| **Portability** | Switch LLM providers without rewriting integrations |
| **Security** | Controlled, auditable access to external resources |
| **Ecosystem** | Pre-built servers for common data sources |
| **Separation of concerns** | Context providers don't need to understand AI models |

---

## MCP Architecture

MCP uses a client-server architecture where AI applications (clients) connect to context servers that provide access to specific resources.

### Components

```
┌─────────────────────────────────────────────────────┐
│                   Host Application                   │
│              (Claude Desktop, IDE, etc.)             │
├─────────────────────────────────────────────────────┤
│                     MCP Client                       │
└───────────┬─────────────────┬─────────────────┬─────┘
            │                 │                 │
     ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
     │ MCP Server  │   │ MCP Server  │   │ MCP Server  │
     │  (GitHub)   │   │ (Database)  │   │   (Slack)   │
     └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
            │                 │                 │
     ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
     │  GitHub API │   │  PostgreSQL │   │  Slack API  │
     └─────────────┘   └─────────────┘   └─────────────┘
```

**Host Application**: The AI-powered application (Claude Desktop, an IDE, a custom app)

**MCP Client**: Embedded in the host, manages connections to servers

**MCP Servers**: Standalone processes that expose resources, tools, and prompts

**External Resources**: The actual data sources and services

### Communication

MCP uses JSON-RPC 2.0 over standard I/O (stdio) or HTTP with Server-Sent Events (SSE). This keeps the protocol simple and transport-agnostic.

---

## Core Primitives

MCP defines three core primitives that servers can expose to clients.

### Resources

Resources are data that the AI can read. They're identified by URIs and can represent files, database records, API responses, or any other content.

```json
{
  "uri": "file:///projects/myapp/README.md",
  "name": "Project README",
  "mimeType": "text/markdown"
}
```

**Use cases**: Documents, code files, database rows, configuration files, log entries

**Characteristics**:
- Read-only from the AI's perspective
- Can be listed and retrieved
- Support for text and binary content
- Can include metadata

### Tools

Tools are actions the AI can perform. They're functions with defined inputs and outputs that let the model interact with external systems.

```json
{
  "name": "create_github_issue",
  "description": "Create a new issue in a GitHub repository",
  "inputSchema": {
    "type": "object",
    "properties": {
      "repo": { "type": "string" },
      "title": { "type": "string" },
      "body": { "type": "string" }
    },
    "required": ["repo", "title"]
  }
}
```

**Use cases**: Create records, send messages, execute commands, trigger workflows

**Characteristics**:
- Require explicit user approval (in well-designed clients)
- Have defined input schemas
- Return results to the model
- Can have side effects

### Prompts

Prompts are reusable templates that servers can expose. They help standardize common interactions and can include dynamic content.

```json
{
  "name": "explain_code",
  "description": "Get an explanation of code in a file",
  "arguments": [
    { "name": "file_path", "required": true }
  ]
}
```

**Use cases**: Code review templates, analysis workflows, report generation

**Characteristics**:
- Can accept arguments
- Return messages that can be added to conversation
- Help standardize common tasks

---

## Common MCP Servers

The MCP ecosystem includes pre-built servers for common integrations.

### Official Reference Servers

| Server | Resources | Tools | Description |
|--------|-----------|-------|-------------|
| **Filesystem** | Files, directories | Read, write, search | Access local file system |
| **GitHub** | Repos, issues, PRs | Create issues, PRs | GitHub integration |
| **GitLab** | Repos, issues, MRs | Create issues, MRs | GitLab integration |
| **Slack** | Channels, messages | Send messages | Slack workspace access |
| **Google Drive** | Files, folders | Search, read | Google Drive access |
| **PostgreSQL** | Schema, query results | Execute queries | Database access |
| **SQLite** | Schema, query results | Execute queries | Local database access |
| **Puppeteer** | Web page content | Navigate, interact | Browser automation |

### Community Servers

The community has built servers for:
- Notion, Confluence, and other documentation platforms
- Jira, Linear, and project management tools
- AWS, GCP, and cloud services
- Monitoring and observability platforms
- Custom internal systems

### Finding Servers

- Official MCP servers repository
- Community server directories
- Build custom servers for specific needs

---

## Using MCP in Practice

### Setting Up MCP (Claude Desktop Example)

Claude Desktop supports MCP servers through its configuration file:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/directory"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

Once configured, the AI can access files and GitHub resources during conversations.

### Workflow Example

**Without MCP**:
1. User asks about code issue
2. User manually copies relevant code into chat
3. AI analyzes and responds
4. User manually creates GitHub issue
5. User pastes AI's suggestion into issue

**With MCP**:
1. User asks about code issue
2. AI reads relevant files directly via MCP
3. AI analyzes and proposes solution
4. AI creates GitHub issue via MCP tool
5. Done in one conversation

### When to Use MCP

| Scenario | MCP Value |
|----------|-----------|
| **Frequent context needs** | High: Eliminates copy-paste |
| **Multi-step workflows** | High: Tools enable automation |
| **Sensitive data** | Medium: Controlled access, but consider security |
| **One-off queries** | Low: Manual context may be faster |
| **Simple conversations** | Low: No external access needed |

---

## Building Custom MCP Servers

When pre-built servers don't meet your needs, you can build custom servers.

### Server Implementation

MCP servers can be built in any language. Official SDKs exist for:
- **TypeScript/JavaScript** (most mature)
- **Python**

### Basic Server Structure (TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio";

const server = new Server({
  name: "my-custom-server",
  version: "1.0.0"
});

// Define available tools
server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "my_tool",
    description: "Does something useful",
    inputSchema: {
      type: "object",
      properties: {
        input: { type: "string" }
      }
    }
  }]
}));

// Handle tool calls
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "my_tool") {
    const result = doSomething(request.params.arguments.input);
    return { content: [{ type: "text", text: result }] };
  }
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### What to Expose

**As Resources**:
- Content the AI should read and reference
- Data that changes over time
- Information needed for context

**As Tools**:
- Actions with side effects
- Operations that modify state
- Queries that need parameters

**As Prompts**:
- Common workflows you want standardized
- Complex tasks with multiple steps
- Templates that benefit from consistency

### Design Considerations

| Consideration | Guidance |
|---------------|----------|
| **Granularity** | Prefer focused servers over monolithic ones |
| **Naming** | Use clear, descriptive names for tools and resources |
| **Documentation** | Write detailed descriptions; the AI uses them |
| **Error handling** | Return meaningful errors the AI can act on |
| **Idempotency** | Design tools to be safely retryable |

---

## Security Considerations

MCP enables powerful capabilities, which requires careful security thinking.

### Authentication

MCP servers handle their own authentication to external services:
- API keys and tokens in environment variables
- OAuth flows for user-specific access
- Service accounts for server-to-server auth

**Never expose credentials to the AI model.** Credentials should be configured in the server, not passed through the protocol.

### Authorization

Consider what the AI should be allowed to access:

| Level | Example | Consideration |
|-------|---------|---------------|
| **Read-only** | View files, query databases | Lower risk, start here |
| **Limited write** | Create issues, send messages | Require user approval |
| **Full access** | Delete files, modify data | High risk, careful controls |

### Sandboxing

MCP servers should implement appropriate sandboxing:
- Filesystem servers should restrict to allowed directories
- Database servers should use read-only connections when possible
- Network access should be scoped to necessary endpoints

### Audit Logging

Log all tool invocations for security and debugging:
- What tool was called
- What arguments were provided
- What result was returned
- When and by whom

### User Approval

Well-designed MCP clients require user approval before executing tools with side effects. This is a critical security boundary.

---

## MCP vs. Alternatives

### MCP vs. Function Calling

| Aspect | MCP | Function Calling |
|--------|-----|------------------|
| **Scope** | Protocol for context and tools | Model-specific tool interface |
| **Portability** | Works across LLM providers | Provider-specific |
| **Architecture** | Separate server processes | In-application functions |
| **Ecosystem** | Shared servers | Custom per application |

MCP and function calling are complementary. MCP servers can be exposed as functions to models that support function calling.

### MCP vs. LangChain Tools

| Aspect | MCP | LangChain Tools |
|--------|-----|-----------------|
| **Design** | Protocol-first, language-agnostic | Library-specific |
| **Isolation** | Separate processes | In-process |
| **Reusability** | Across any MCP client | Within LangChain apps |

LangChain has an MCP integration, allowing MCP servers to be used as LangChain tools.

### When to Use What

- **MCP**: When you want reusable context providers that work across applications
- **Function calling**: When tools are application-specific and tightly integrated
- **Both**: MCP for shared infrastructure, function calling for app-specific logic

---

## Practical Patterns

### Development Workflow Integration

Connect MCP servers for your development tools:

```
IDE ─── MCP Client
         ├── Filesystem (project files)
         ├── GitHub (issues, PRs)
         ├── Jira (tickets)
         └── Database (local dev DB)
```

The AI can now read code, understand tickets, and check database state without manual context copying.

### Documentation Q&A

Build a documentation assistant:

```
Chat App ─── MCP Client
              ├── Confluence (docs)
              ├── Notion (runbooks)
              └── GitHub (README files)
```

Questions about processes or procedures can be answered by retrieving relevant documentation automatically.

### Workflow Automation

Combine reading and writing capabilities:

1. AI reads ticket from Jira (resource)
2. AI analyzes related code (resource)
3. AI creates GitHub PR (tool)
4. AI updates Jira ticket (tool)
5. AI notifies team in Slack (tool)

### Multi-Environment Access

Different servers for different environments:

```json
{
  "mcpServers": {
    "prod-db": { "command": "...", "env": { "DB_URL": "prod-url" } },
    "staging-db": { "command": "...", "env": { "DB_URL": "staging-url" } }
  }
}
```

The AI can compare data across environments safely.

---

## Limitations and Considerations

### Current Limitations

| Limitation | Implication |
|------------|-------------|
| **Ecosystem maturity** | Not all integrations exist yet |
| **Client support** | Not all AI applications support MCP |
| **Complexity** | Running servers adds operational overhead |
| **Latency** | Server communication adds response time |

### When MCP Might Not Be Right

- Simple, one-off tasks where manual context is faster
- Highly sensitive environments where any external access is risky
- Applications where latency is critical
- Teams without capacity to operate additional services

### Future Direction

MCP is actively evolving. Expected developments include:
- Broader client support across AI applications
- More pre-built servers for common services
- Improved authentication and authorization patterns
- Better tooling for server development and debugging

---

## Quick Reference

### MCP Primitives Summary

| Primitive | Purpose | Example |
|-----------|---------|---------|
| **Resources** | Data to read | Files, DB records, API responses |
| **Tools** | Actions to perform | Create issue, send message |
| **Prompts** | Reusable templates | Code review workflow |

### Getting Started Checklist

1. [ ] Identify what external context your AI needs
2. [ ] Find existing MCP servers for those sources
3. [ ] Configure servers in your MCP client
4. [ ] Test with simple queries
5. [ ] Add tools for write operations (carefully)
6. [ ] Build custom servers for unique needs

### Security Checklist

1. [ ] Credentials stored in environment variables, not in protocol
2. [ ] Read-only access where possible
3. [ ] User approval required for side-effect tools
4. [ ] Audit logging enabled
5. [ ] Sandboxing configured (directories, network)
6. [ ] Regular review of granted permissions
