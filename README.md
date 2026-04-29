# Agentman Guild Application — Jibin Kunjumon

Pre-interview homework submission for the Agentman Guild program.

---

## Bonus Skill — SAR Narrative Generator

> The main deliverable. Paste a FraudSentinel REJECTED transaction and get a compliance-ready SAR narrative in seconds.

**What it does:** Turns raw fraud agent output into a structured Suspicious Activity Report (SAR) in FinCEN/FCA format — replacing 20–30 minutes of manual drafting per case. Handles threshold checks, maps detector flags to regulatory language, and recommends the correct action (file / freeze / monitor).

**Why:** Aligned with Agentman's Moneyman (fintech) vertical. SAR filing is legally mandatory — this directly removes bottleneck work for compliance officers.

**Eval results:** 3 iterations, score improved from 7.54 → 7.83 using rule-based + model grading.

**How to run:**
```bash
cd sar-skill
python main.py
```

→ [`sar-skill/`](sar-skill/) — skill prompt, CLI, example cases, eval pipeline with iteration log

---

## Required Courses (Part 1)

| # | Course | Certificate | Screenshot |
|---|--------|------------|------------|
| 1 | Introduction to Agent Skills | [PDF](certificates/certificate-introduction%20to%20skills.pdf) | [PNG](screenshots/Introduction%20to%20agent%20skills.png) |
| 2 | Introduction to Model Context Protocol | [PDF](certificates/certificate-Introduction%20to%20MCP.pdf) | [PNG](screenshots/Introduction%20to%20MCP.png) |
| 3 | Building with the Claude API | [PDF](certificates/certificate-building_with_Claude.pdf) | [PNG](screenshots/Building%20with%20claude%20API.png) |
| 4 | Claude Code in Action | [PDF](certificates/certificate-claude_code_in_action.pdf) | [PNG](screenshots/Claude%20Code%20in%20action.png) |

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
