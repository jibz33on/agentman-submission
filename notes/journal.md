# Agentman Submission — Learning Journal

## Day 1 — April 26, 2026

### Completed
- ✅ Course 1: Introduction to Agent Skills
- ✅ Course 2: Introduction to Model Context Protocol

---

### Course 1: Agent Skills

**The core insight:**

> "One skill = one user-facing capability. That capability can require multiple internal steps (scripts, checks, reports), but the user just triggers it once with one request."

Building the `journal-entry` practice skill made this concrete. The user says "add a journal entry" — they don't care that it internally reads a file, formats content, appends to disk, and confirms success. One trigger, multiple internal steps.

**What I was still fuzzy on:**
How to structure a long SKILL.md — best practices for patterns, example usage format, and how Claude's semantic matching actually works under the hood.

---

### Course 2: Model Context Protocol (MCP)

**Key takeaways:**
- MCP is a communication protocol between Claude and external services
- Three primitives solve three different problems: Tools (actions), Resources (data), Prompts (templates)
- FastMCP makes server building simple — Python decorators replace manual JSON schemas
- The client is a thin wrapper around the SDK's `ClientSession`
- Tested a full CLI chat app with `@mention` document loading and `/command` prompt dispatch

**What I built:**
A document management CLI with an MCP server (tools + resources + prompts) and a client that connects to it, backed by Claude for natural language interaction.

---

### Claude's Extension System at a Glance

| Mechanism | When It Activates | Purpose |
|-----------|-------------------|---------|
| `CLAUDE.md` | Every message (always-on) | Persistent rules and project context |
| Skills | On-demand when triggered | Request-driven workflows and knowledge |
| Hooks | On events (tool calls, session end) | Automated side effects and checks |
| Subagents | When explicitly spawned | Isolated workers for parallel tasks |
| MCP | When connected to a server | External tool access and data retrieval |

**The practical difference:**
CLAUDE.md is for rules you always want applied. Skills load specific expertise when needed. Hooks run automatically on events. Subagents handle independent parallel work. MCP gives Claude access to external systems without you wiring up each integration yourself.

---

### What's Next
- Implement MCP prompts: rewrite-as-markdown and summarize
- Test full CLI chat with `@mentions` and `/commands`
- Continue remaining course videos
