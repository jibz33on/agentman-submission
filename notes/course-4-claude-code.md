# Course 4: Claude Code in Action

## What is Claude Code?

An AI coding assistant that lives in your terminal. You describe what you want in plain English and Claude reads your files, writes code, runs commands, and makes changes — all inside your actual project.

Unlike chat-based AI tools where you copy-paste code back and forth, Claude Code works directly in your codebase. It can read any file, edit multiple files at once, run tests, and use git — all in one conversation.

**What is a coding assistant?**
A tool that understands your codebase and helps you build, fix, and explore it using natural language. The key difference from a regular chatbot: it has access to your actual files and can take real actions, not just give suggestions.

---

## Getting Hands On

### Setup
Install Claude Code via npm, authenticate with your Anthropic API key, and run it from any project directory. Works in the terminal, VS Code, and JetBrains IDEs.

### Project Setup
Claude Code reads your project files automatically. You can also create a `CLAUDE.md` file in the root of your project — this is a special file Claude always reads first. Use it to describe the project, coding conventions, commands to run, and anything Claude should always know.

### Adding Context

Too much irrelevant context hurts Claude's performance — guide it to the right files instead of letting it read everything.

**`/init`** — run this when starting on a new project. Claude analyses the codebase and creates a `CLAUDE.md` file summarising the architecture, key commands, and coding patterns.

**CLAUDE.md locations — three levels:**

| File | Scope | Shared? |
|------|-------|---------|
| `CLAUDE.md` | Current project | Yes — commit to git, shared with team |
| `CLAUDE.local.md` | Current project | No — personal instructions only |
| `~/.claude/CLAUDE.md` | All projects on your machine | No — global personal rules |

**Adding custom instructions** — use the `#` command to enter memory mode. Type a rule (e.g. "Use comments sparingly") and Claude merges it into your CLAUDE.md automatically.

**@ file mentions** — type `@filename` in your message to include that file's contents in the request. Claude shows matching files to pick from.

**@ in CLAUDE.md** — reference a file inside CLAUDE.md itself and its contents are automatically included in every request. Good for things like a database schema that's relevant to everything.

### Making Changes
Describe what you want and Claude will read the relevant files, propose changes, and ask for approval before writing anything. You can accept, reject, or ask it to adjust. Changes are shown as diffs so you can see exactly what's changing.

### Controlling Context

| Tool | What it does | When to use |
|------|-------------|-------------|
| `Escape` | Stops Claude mid-response | Claude is going in the wrong direction or doing too much at once |
| `Escape` twice | Shows all your messages — jump back to any point | Long conversation with irrelevant back-and-forth you want to skip |
| `/compact` | Summarises the full conversation, keeps key knowledge | Claude has learned a lot and you want to continue a related task |
| `/clear` | Wipes the conversation completely | Switching to a totally different task |

**Escape + memory trick** — if Claude keeps making the same mistake across conversations: press Escape to stop it, use `#` to add a rule to CLAUDE.md, then continue. It won't repeat the mistake in future sessions.

### Custom Commands
You can create your own slash commands that trigger pre-written prompts. Stored as markdown files in `.claude/commands/`. Useful for repeating tasks like "run my test suite and summarise failures" or "write a PR description for these changes."

### MCP Servers with Claude Code
MCP (Model Context Protocol) lets you connect Claude Code to external tools and data sources — databases, APIs, web search, internal systems. Once connected, Claude can call these tools mid-conversation just like any other action. Configure them in Claude Code settings.

### GitHub Integration
Claude Code can interact with GitHub via the `gh` CLI — create PRs, read issues, check CI status, and more. You can also run Claude Code as a GitHub Action to automate tasks like reviewing PRs or fixing failing tests on push.

---

## Hooks and the SDK

### What are Hooks?
Hooks let you run your own shell commands automatically when Claude Code does something — before or after tool use, or when the session ends. Think of them as triggers: "whenever Claude tries to edit a file, first run my linter."

### Types of Hooks

| Hook | When it runs |
|------|-------------|
| PreToolUse | Before Claude uses a tool (read, edit, bash, etc.) |
| PostToolUse | After a tool completes |
| Stop | When the session ends |

### Defining Hooks
Hooks are configured in your Claude Code settings. Each hook specifies: which event triggers it, optionally which tool to match, and the shell command to run.

### Implementing a Hook
The shell command receives context about what Claude is doing as JSON via stdin. Your script can read that, do something (log it, validate it, block it), and return a response. If the hook exits with a non-zero code and returns a message, Claude sees that message and can adjust its behaviour.

### Gotchas
- Hooks run on every matching event — keep them fast or they slow everything down
- A hook that always blocks will make Claude Code unusable
- Test hooks carefully before enabling them globally
- Hooks have access to file paths and inputs — don't log sensitive data carelessly

### Useful Hook Examples
- **Auto-format** — run a formatter after every file edit
- **Test runner** — run relevant tests after code changes
- **Safety check** — block edits to certain files or directories
- **Logger** — record every command Claude runs for auditing

### The Claude Code SDK

Lets you run Claude Code from inside your own scripts and applications — same tools, same behaviour as the terminal version, but fully automated.

Available in TypeScript, Python, and CLI. You give it a prompt, it streams back messages as it works, and the final message has the complete response.

**Permissions:**
- Read-only by default (can read files, search, grep — cannot write or edit)
- Enable write access by specifying allowed tools explicitly, or via project settings

**Best used for:**
- Git hooks that auto-review code before a commit
- CI/CD pipelines that check code quality on every push
- Build scripts that analyse or optimise code automatically
- Automated documentation generation

The key point: it's not for interactive use — it's for plugging Claude's intelligence into a pipeline that runs without you.
