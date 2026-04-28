# Course 2: Introduction to Model Context Protocol

## What is MCP?

MCP (Model Context Protocol) is a standard way for AI apps to connect to external tools and data. Instead of every app writing its own integration code, you connect to an MCP server that already has those tools built.

```
Your App → MCP Server → External Service (GitHub, database, Slack, etc.)
```

**Tool Use vs MCP:**
- Tool Use = HOW Claude calls functions
- MCP = WHO provides those functions (you vs. a pre-built server)

MCP doesn't replace tool use — it standardises where tools come from.

---

## The Three Primitives

| Primitive | What it is | Use when |
|-----------|-----------|---------|
| **Tools** | Functions Claude can call | Taking actions, fetching data on demand |
| **Resources** | Read-only data | You want context injected into the prompt upfront |
| **Prompts** | Pre-written instruction templates | Packaging expert instructions for reuse |

---

## How It Works

**The flow:**
1. User sends a message
2. Your app asks the MCP server "what tools do you have?"
3. Claude decides which tool to call
4. Your app calls the tool via the MCP client
5. Result comes back through the chain to Claude
6. Claude responds to the user

**Transport:** Client and server talk over stdio (standard for local dev), HTTP, or WebSockets.

---

## Tools

Functions Claude can call to take action or fetch data. You define them with a decorator — FastMCP auto-generates the JSON schema from your Python type hints.

- Good descriptions on each parameter are critical — Claude reads them to decide how to use the tool
- Raise a Python exception if something goes wrong — the SDK converts it to a proper error response

---

## Resources

Read-only data exposed by URI. Two types:

- **Static** — fixed URI, good for listings and config (e.g. `docs://documents`)
- **Templated** — URI contains a variable (e.g. `docs://documents/{doc_id}`), good for fetching a specific item

**Resources vs Tools:**

| | Resources | Tools |
|---|-----------|-------|
| How | Content injected into prompt upfront | Claude calls it mid-conversation |
| Speed | Immediate | Requires an extra round-trip |
| Best for | Context Claude needs from the start | Actions, writes, conditional fetches |

---

## Prompts

Pre-written instruction templates stored on the server. The server author writes and tests them once — every client that connects gets the same high-quality instructions automatically.

- Takes arguments (e.g. a document ID), fills them into a template, returns messages ready to send to Claude
- Better than letting users write their own instructions — encodes expertise they wouldn't think to include
- Improve the prompt once on the server, all clients benefit immediately

---

## Testing — MCP Inspector

Run `uv run mcp dev mcp_server.py` to open a browser-based tool where you can:
- See all registered tools, resources, and prompts
- Call them manually with test inputs before wiring up the full app

---

## Key Takeaways

- **Write the server once** — any client (CLI, web app, IDE) connects and gets all three primitives automatically
- **FastMCP** removes boilerplate — decorators replace hand-written JSON schemas and manual registration
- **Resources** are faster than tools for loading context — no extra LLM call needed
- **Prompts** are reusable expertise — encode the right instructions once, not per user per session
