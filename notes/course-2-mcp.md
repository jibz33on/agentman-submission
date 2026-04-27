# Course 2: Introduction to Model Context Protocol

## Overview

MCP (Model Context Protocol) is a communication layer between your app and external services. Instead of writing tool schemas and API integration code yourself, you connect to an MCP Server that has those tools already built.

**The architecture:**
```
Your App (MCP Client) → MCP Server → External Service (GitHub, Slack, database, etc.)
```

**Key distinction:**
| Concept | What it means |
|---------|---------------|
| Tool Use | HOW Claude calls functions |
| MCP | WHO provides those functions (you vs. a pre-built server) |

MCP doesn't replace tool use — it standardizes where tools come from.

---

## Video 1: What is MCP?

**The problem it solves:**
Before MCP, every app had to write its own integration code: custom tool schemas, API wiring, error handling. MCP standardizes this so servers can be built once and reused by any client.

**Three primitives — three different jobs:**

| Primitive | What it is | When to use it |
|-----------|-----------|----------------|
| **Tools** | Functions Claude can call | Actions that change state or fetch data on demand |
| **Resources** | Data Claude can read | Context you want injected directly into the prompt |
| **Prompts** | Message templates | Pre-built, tested instructions for complex workflows |

**Key insight:**
The same Claude SDK you already know (tool use, message params) is still doing the work. MCP just standardizes how tools and data are exposed so different clients can share the same server.

---

## Video 2: The MCP Client

The client sits between your app and the MCP server. It sends requests and returns results.

**What the client does:**
- Sends `ListToolsRequest` → asks the server "what tools do you have?"
- Sends `CallToolRequest` → asks the server "run this tool with these inputs"
- Returns results to your application

**The full request flow:**
```
User → Your App → Claude (decides which tool) → Your App
     → MCP Client → MCP Server → External API
     → back through the chain → Claude → User
```

**Transport:** The client/server communicate over stdio, HTTP, or WebSockets. For local development, stdio is standard — the client spawns the server as a subprocess.

---

## Video 3: Setting Up a FastMCP Server

FastMCP is the Python library for building MCP servers. It uses decorators so you write normal Python functions instead of constructing JSON schemas by hand.

**Basic setup:**
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")

# In-memory document store (replace with real DB in production)
docs = {
    "deposition.md": "This deposition covers Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**Why `log_level="ERROR"`?**
The MCP server communicates with the client over stdout. Any debug logs written to stdout would corrupt the protocol messages. Setting `log_level="ERROR"` keeps the channel clean.

---

## Video 4: Defining Tools

Tools are functions Claude can call. FastMCP turns Python functions into MCP tools with a decorator.

**The pattern:**
```python
from pydantic import Field

@mcp.tool(
    name="tool_name",
    description="What this tool does — Claude reads this to decide when to use it"
)
def function_name(
    param: str = Field(description="What this parameter means")
):
    return result
```

**What FastMCP does automatically:**
- Generates the JSON schema from Python type hints
- Validates inputs using Pydantic
- Converts Python exceptions into MCP error responses
- Registers the tool so clients can discover it

**Two tools implemented in the project:**

```python
@mcp.tool(name="read_doc_contents", description="Read the contents of a document")
def read_doc_contents(doc_id: str = Field(description="The document ID")):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    return docs[doc_id]

@mcp.tool(name="edit_document", description="Replace text in a document")
def edit_document(
    doc_id: str = Field(description="The document ID"),
    old_str: str = Field(description="Text to replace (exact match)"),
    new_str: str = Field(description="Replacement text")
):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return docs[doc_id]
```

**Why `Field()` matters:**
The description inside `Field()` is what Claude reads to understand each parameter. Good descriptions = Claude uses tools correctly.

---

## Video 5: Testing with MCP Inspector

MCP Inspector is a browser-based tool for testing your server before wiring it into an application.

```bash
uv run mcp dev mcp_server.py
```

This starts a local web server. Open the URL in your browser to:
- See all registered tools with their schemas
- Call tools manually with test inputs
- Browse resources and resource templates
- Test prompts and see the raw messages they generate

**Useful for:** Verifying your server works correctly before debugging client code.

---

## Video 6: Implementing the Client

The client wraps the MCP SDK's `ClientSession` to give your app a clean API and ensure connections are properly cleaned up.

**Client architecture:**
- `MCPClient` — your custom wrapper class (easier API, resource cleanup)
- `ClientSession` — the actual SDK connection to the server

**Core implementation:**
```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

class MCPClient:
    def __init__(self, command: str, args: list[str]):
        self._command = command
        self._args = args
        self._session = None
        self._exit_stack = AsyncExitStack()

    async def connect(self):
        server_params = StdioServerParameters(command=self._command, args=self._args)
        stdio_transport = await self._exit_stack.enter_async_context(stdio_client(server_params))
        _stdio, _write = stdio_transport
        self._session = await self._exit_stack.enter_async_context(ClientSession(_stdio, _write))
        await self._session.initialize()

    async def list_tools(self) -> list[types.Tool]:
        result = await self.session().list_tools()
        return result.tools

    async def call_tool(self, tool_name: str, tool_input: dict) -> types.CallToolResult:
        return await self.session().call_tool(tool_name, tool_input)

    async def cleanup(self):
        await self._exit_stack.aclose()
```

**Why `AsyncExitStack`?**
The client spawns a subprocess (the server) and opens a connection. Both need to be shut down cleanly when the app exits. `AsyncExitStack` tracks both and closes them in reverse order automatically.

**Testing:**
```bash
uv run mcp_client.py  # should print available tools
uv run main.py        # full app: ask "what is in report.pdf?"
```

---

## Video 7: Defining Resources

Resources expose read-only data that clients can fetch by URI. There are two kinds:

### Static Resources (fixed URI, no parameters)
```python
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> str:
    return json.dumps(list(docs.keys()))
```
- The URI never changes
- Good for listings and configuration

### Templated Resources (URI contains a variable)
```python
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    return docs[doc_id]
```
- `{doc_id}` in the URI becomes a function parameter
- The SDK parses the variable from the URI and passes it as a keyword argument
- Good for fetching specific items by ID

**MIME types tell the client how to parse the response:**
| MIME type | Use for |
|-----------|---------|
| `application/json` | Structured data (lists, dicts) |
| `text/plain` | Plain text |

**Important:** FastMCP resource functions must return `str`, not a list or dict. Use `json.dumps()` for structured data.

In MCP Inspector, resources appear under two tabs:
- **Resources** — static resources
- **Resource Templates** — templated resources (enter a value to test)

---

## Video 8: Accessing Resources from the Client

Resources are better than tools for loading context because the content goes directly into the prompt — no extra Claude round-trip needed.

**When to use resources vs tools:**
| | Resources (`@`) | Tools |
|---|---|---|
| How it works | Content injected into prompt upfront | Claude calls the tool mid-conversation |
| Speed | Immediate | Requires an extra LLM call |
| Best for | Context Claude needs from the start | Actions, writes, or conditional fetches |

**Client implementation:**
```python
import json
from pydantic import AnyUrl

async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]

    if isinstance(resource, types.TextResourceContents):
        if resource.mimeType == "application/json":   # Note: camelCase
            return json.loads(resource.text)
        return resource.text
```

**Watch out:** The SDK model uses `mimeType` (camelCase), not `mime_type`. Using the wrong attribute raises `AttributeError`.

**The `@mention` user experience:**
1. User types `@` in the CLI
2. Autocomplete shows available document IDs (fetched from `docs://documents`)
3. User selects one
4. Client fetches `docs://documents/{doc_id}` and injects content into the prompt
5. Claude receives full document context immediately — no tool calls needed

---

## Video 9: Defining Prompts

Prompts are pre-written, tested instruction templates stored on the server. They're better than letting users write their own instructions because the server author crafts them once and everyone benefits.

**Example: a document formatting prompt**
```python
from mcp.server.fastmcp.prompts import base

@mcp.prompt(
    name="format",
    description="Rewrite the contents of a document in markdown format"
)
def format_document(
    doc_id: str = Field(description="The ID of the document to format")
) -> list[base.Message]:
    prompt = f"""
Your goal is to rewrite the contents of a document in markdown format.

The id of the document you need to reformat is:
<document_id>
{doc_id}
</document_id>

Add headers, bullet points, tables as needed. Use the 'edit_document' tool to save changes.
"""
    return [base.UserMessage(prompt)]
```

**How prompts work:**
- The function receives arguments (like `doc_id`)
- It interpolates them into a template string
- It returns a list of `Message` objects (user/assistant turns)
- The client requests the prompt with specific argument values and gets back the filled-in messages

**Why prompts beat ad-hoc instructions:**
- **Consistency** — same quality every time, tested and refined by the server author
- **Expertise** — encode domain knowledge users wouldn't think to include
- **Reusability** — any client connecting to this server gets the same high-quality prompts
- **Maintenance** — improve the prompt once, all clients benefit immediately

---

## Video 10: Accessing Prompts from the Client

Two functions complete the client:

```python
# List all prompts the server has defined
async def list_prompts(self) -> list[types.Prompt]:
    result = await self.session().list_prompts()
    return result.prompts

# Fetch a specific prompt with argument values filled in
async def get_prompt(self, prompt_name: str, args: dict[str, str]):
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

**What `get_prompt` does:**
You call it with a prompt name and a dict of argument values. The server runs your prompt function with those values, interpolates them into the template, and returns the filled-in messages ready to send to Claude.

**The `/command` user experience:**
1. User types `/format` in the CLI
2. Autocomplete shows available commands (fetched from `list_prompts`)
3. CLI prompts for a document ID
4. Client calls `get_prompt("format", {"doc_id": "plan.md"})`
5. Server returns formatted messages with the doc ID interpolated
6. Messages sent to Claude, which uses tools to fetch and reformat the document

**Full prompt workflow summary:**

```
Server author: write prompt template → test it → deploy
Client user:   type /command → select args → get expert-crafted instructions
Claude:        receives properly structured instructions → uses tools → delivers results
```

---

## Key Takeaways

**The three primitives in one sentence each:**
- **Tools** — let Claude take action (fetch data, make changes, call APIs)
- **Resources** — let Claude read context directly (injected into prompt, no tool call needed)
- **Prompts** — let server authors package expert instructions that any client can reuse

**The MCP value proposition:**
You write a server once. Any client — CLI app, web app, IDE extension — connects to it and gets all three capabilities automatically. No duplication, no custom integration code per client.

**FastMCP reduces friction:**
| Without FastMCP | With FastMCP |
|----------------|--------------|
| Write JSON schema by hand | Python type hints → schema auto-generated |
| Manual input validation | Pydantic validates automatically |
| Register tools manually | `@mcp.tool()` decorator handles registration |
| Custom error format | Raise Python exceptions, SDK converts them |
