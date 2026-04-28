# Agentman Guild Application — Jibin Kunjumon

Pre-interview homework submission for the Agentman Guild program.

---

## Bonus Skill — Earnings Call Summarizer

> The main deliverable. Paste any public earnings call transcript and get a structured briefing in seconds.

**What it does:** Extracts key metrics, highlights, risks, outlook, and analyst Q&A themes from earnings call transcripts — the kind of dense 60-minute calls that usually take an analyst 30 minutes to digest.

**Why:** Aligned with Agentman's Moneyman (fintech) vertical. Solves a real, recurring problem.

**How to run:**
```bash
cd bonus-skill
uv run --with anthropic --with python-dotenv main.py
```

→ [`bonus-skill/`](bonus-skill/) — skill prompt, CLI, demo transcript, eval pipeline

---

## Required Courses (Part 1)

| # | Course | Certificate |
|---|--------|------------|
| 1 | Introduction to Agent Skills | [PDF](certificates/certificate-introduction%20to%20skills.pdf) |
| 2 | Introduction to Model Context Protocol | [PDF](certificates/certificate-Introduction%20to%20MCP.pdf) |
| 3 | Building with the Claude API | [PDF](certificates/certificate-building_with_Claude.pdf) |
| 4 | Claude Code in Action | [PDF](certificates/certificate-claude_code_in_action.pdf) |

---

## Projects Built

### Course 2 — MCP CLI Chat App
A command-line chat app backed by an MCP server with tools, resources, and prompts. Supports `@mention` document loading and `/command` prompt dispatch.

→ [`course-2-mcp-cli/`](course-2-mcp-cli/)

### Course 3 — Prompt Evaluation Pipeline
A Python pipeline that generates test datasets, runs prompts through Claude, and scores outputs using model grading + syntax validation. Used to iteratively improve prompts from a 5.9 baseline to 8.2.

→ [`course-3-eval-pipeline/`](course-3-eval-pipeline/)

---

## Course Notes

Concise, plain-English notes for each course — no code, just the concepts.

→ [`notes/`](notes/)

---

## Submission

- Form: https://forms.gle/ohhwmZ5HYB9SDrsv8
- Contact: jibz33on@gmail.com
