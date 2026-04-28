# context-mode — MANDATORY routing rules

You have context-mode MCP tools available. These rules are NOT optional — they protect your context window from flooding. A single unrouted command can dump 56 KB into context and waste the entire session.

## BLOCKED commands — do NOT attempt these

### curl / wget — BLOCKED
Any Bash command containing `curl` or `wget` is intercepted and replaced with an error message. Do NOT retry.
Instead use:
- `ctx_fetch_and_index(url, source)` to fetch and index web pages
- `ctx_execute(language: "javascript", code: "const r = await fetch(...)")` to run HTTP calls in sandbox

### Inline HTTP — BLOCKED
Any Bash command containing `fetch('http`, `requests.get(`, `requests.post(`, `http.get(`, or `http.request(` is intercepted and replaced with an error message. Do NOT retry with Bash.
Instead use:
- `ctx_execute(language, code)` to run HTTP calls in sandbox — only stdout enters context

### WebFetch — BLOCKED
WebFetch calls are denied entirely. The URL is extracted and you are told to use `ctx_fetch_and_index` instead.
Instead use:
- `ctx_fetch_and_index(url, source)` then `ctx_search(queries)` to query the indexed content

## REDIRECTED tools — use sandbox equivalents

### Bash (>20 lines output)
Bash is ONLY for: `git`, `mkdir`, `rm`, `mv`, `cd`, `ls`, `npm install`, `pip install`, and other short-output commands.
For everything else, use:
- `ctx_batch_execute(commands, queries)` — run multiple commands + search in ONE call
- `ctx_execute(language: "shell", code: "...")` — run in sandbox, only stdout enters context

### Read (for analysis)
If you are reading a file to **Edit** it → Read is correct (Edit needs content in context).
If you are reading to **analyze, explore, or summarize** → use `ctx_execute_file(path, language, code)` instead. Only your printed summary enters context. The raw file content stays in the sandbox.

### Grep (large results)
Grep results can flood context. Use `ctx_execute(language: "shell", code: "grep ...")` to run searches in sandbox. Only your printed summary enters context.

## Tool selection hierarchy

1. **GATHER**: `ctx_batch_execute(commands, queries)` — Primary tool. Runs all commands, auto-indexes output, returns search results. ONE call replaces 30+ individual calls.
2. **FOLLOW-UP**: `ctx_search(queries: ["q1", "q2", ...])` — Query indexed content. Pass ALL questions as array in ONE call.
3. **PROCESSING**: `ctx_execute(language, code)` | `ctx_execute_file(path, language, code)` — Sandbox execution. Only stdout enters context.
4. **WEB**: `ctx_fetch_and_index(url, source)` then `ctx_search(queries)` — Fetch, chunk, index, query. Raw HTML never enters context.
5. **INDEX**: `ctx_index(content, source)` — Store content in FTS5 knowledge base for later search.

## Subagent routing

When spawning subagents (Agent/Task tool), the routing block is automatically injected into their prompt. Bash-type subagents are upgraded to general-purpose so they have access to MCP tools. You do NOT need to manually instruct subagents about context-mode.

## Output constraints

- Keep responses under 500 words.
- Write artifacts (code, configs, PRDs) to FILES — never return them as inline text. Return only: file path + 1-line description.
- When indexing content, use descriptive source labels so others can `ctx_search(source: "label")` later.

## ctx commands

| Command | Action |
|---------|--------|
| `ctx stats` | Call the `ctx_stats` MCP tool and display the full output verbatim |
| `ctx doctor` | Call the `ctx_doctor` MCP tool, run the returned shell command, display as checklist |
| `ctx upgrade` | Call the `ctx_upgrade` MCP tool, run the returned shell command, display as checklist |

---

# Project: Agentman Guild Application

## What This Is

Pre-interview homework for the Agentman Guild. Completing all parts unlocks the interview.
Submitted by Jibin Kunjumon (jibz33on@gmail.com).

## Structure

```
agentman-submission/
├── bonus-skill/                  # Bonus skill: earnings call transcript summariser
│   ├── skill.md                  # Skill prompt and output format
│   ├── main.py                   # CLI entry point
│   ├── helpers.py                # Claude API helpers
│   ├── examples/                 # Sample transcripts for demo
│   └── eval/                     # Evaluation dataset, grading, iteration log (to build)
├── course-2-mcp-cli/             # Course 2: MCP CLI chat app
├── course-3-eval-pipeline/       # Course 3: Prompt evaluation pipeline
├── certificates/                 # Course completion certificates
└── notes/                        # Course notes (1–4)
```

## Courses

| # | Course | Status |
|---|--------|--------|
| 1 | Introduction to Agent Skills | ✅ Complete |
| 2 | Introduction to MCP | ✅ Complete |
| 3 | Building with the Claude API | ✅ Complete |
| 4 | Claude Code in Action | ✅ Complete |

## Bonus Skill — Earnings Call Summarizer

Paste a public company earnings call transcript → get a structured briefing with key metrics, highlights, risks, outlook, and analyst Q&A themes.

Target output format:
- Company / Quarter / Year
- Key Metrics (revenue, EPS, guidance)
- Highlights (3–5 bullets)
- Risks & Challenges (3–5 bullets)
- Outlook (management forward guidance)
- Analyst Q&A Themes (2–3 recurring topics)

The eval/ folder will contain test cases, gold standards, grading script, and iteration log showing prompt improvement scores.

## Key Commands

```bash
# Run the earnings call summarizer
cd bonus-skill && uv run --with anthropic --with python-dotenv main.py

# Run the evaluation pipeline
cd course-3-eval-pipeline && uv run --with anthropic --with python-dotenv run_eval.py

# Run the MCP CLI chat app
cd course-2-mcp-cli && uv run main.py
```

## Important Files

- @bonus-skill/skill.md — the core skill prompt
- @course-3-eval-pipeline/run_eval.py — evaluation and grading pipeline
- @notes/course-3-claude-api.md — Claude API reference notes
- @notes/course-4-claude-code.md — Claude Code reference notes

## Coding Style

- Python throughout
- Use uv for running scripts
- No hardcoded API keys — always use .env
- Keep files small and focused
- No unnecessary comments
