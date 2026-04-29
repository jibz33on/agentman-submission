# Agentman Guild Application — Jibin Kunjumon

AI engineer building agent skills for fintech compliance. This repo showcases work across the Agentman Guild learning track — from MCP integrations and prompt evaluation pipelines to a production-ready SAR narrative skill built on top of a fraud detection system.

---

## SAR Narrative Generator

> A **Suspicious Activity Report (SAR)** is a legal document that banks and fintech companies must file with financial regulators — FinCEN in the US, the FCA in the UK — whenever a transaction shows signs of fraud, money laundering, or financial crime. Filing one isn't optional: missing it carries serious regulatory penalties. This skill takes a FraudSentinel REJECTED transaction and generates a compliance-ready SAR narrative in seconds.

### Context: FraudSentinel

FraudSentinel is an autonomous multi-agent system that analyses financial transactions in real time and delivers an **APPROVED / REVIEW / REJECTED** verdict before a human ever sees the alert. It runs three agents in sequence:

**1. Detector** — pure rules, no LLM, fires on every transaction. Checks 12 signals including amount anomaly (>3× user average), unfamiliar location, unusual hour (00:00–04:59), high-risk merchant category (crypto, casino, forex, wire transfer), velocity (3+ transactions in 24h), new account (<30 days), foreign transaction, IP/location mismatch, and new device. Each triggered rule appends a flag and adds weighted points toward a score capped at 100. Verdicts: ≤30 → APPROVED, 31–69 → REVIEW, ≥70 → REJECTED.

**2. Investigator** — behavioural deviation analysis, runs after the Detector. Skipped entirely if the user has fewer than 5 transactions (no baseline exists). Otherwise scores four signals: amount vs baseline (up to 25pts), country deviation (25pts), hour deviation (20pts), and merchant deviation (15pts). When deviation ≥ 10, an LLM fires and writes a three-line PATTERN / DEVIATION / RISK narrative.

**3. Decision** — combines both agents: `combined_score = (detector × 0.6) + (investigator × 0.4)`. Hard override: detector ≥ 90 always REJECTED. An LLM always runs here, writing a DECISION / SIGNALS / BEHAVIOUR / ACTION reasoning block alongside the final verdict, confidence score, and combined score.

Two teams use FraudSentinel's output: **fraud analysts** who work the REVIEW queue day-to-day, and **compliance / ops** who handle REJECTED verdicts that cross regulatory reporting thresholds. For compliance, FraudSentinel gives them the decision and the reasoning — but producing the SAR document is still entirely manual.

### The Problem

When FraudSentinel rejects a transaction above reporting thresholds, the compliance team must file a **Suspicious Activity Report (SAR)** — a legally mandatory document required by FinCEN (US) and the FCA (UK). SARs must be written in precise regulatory language, cite specific fraud typologies, remain strictly neutral (no crime conclusions), and clearly separate evidentiary facts from filing recommendations.

In practice this means a compliance officer reads the raw agent JSON, manually translates detector flags into regulatory terminology, drafts 4–6 structured sections in the correct tone, checks the filing threshold, and signs off — all before moving to the next case. That process takes **20–30 minutes per rejection**, every time.

### How This Skill Helps

The SAR Narrative Generator takes FraudSentinel's raw REJECTED output and produces a complete, compliance-ready SAR draft in seconds. It:

- Maps every detector flag to its regulatory equivalent (`ip_location_mismatch` → *geolocation inconsistency suggesting account compromise*)
- Structures the output into the required FinCEN/FCA sections with strict content separation
- Checks the reporting threshold and flags high-risk categories that trigger mandatory filing regardless of amount
- Recommends the correct action — file, freeze and file, or monitor — based on confidence and risk score
- Incorporates analyst notes without resolving contradictions (flags them instead)

The compliance officer gets a first draft they can review, edit, and file — instead of starting from a blank page.

### Eval Results

To make sure the skill produces reliable, regulator-ready output every time, it was tested against three realistic FraudSentinel cases — a high-confidence crypto fraud, a borderline gambling transaction with analyst notes, and a maximum-risk wire transfer through a Tor exit node.

Each output was graded two ways:

- **Rule-based checks** — automated pass/fail on things that must always be true: all 6 required sections present, no crime conclusions ("is guilty", "committed fraud"), no first-person language, and the correct recommended action (freeze vs monitor)
- **Model grading** — Claude scores the output 1–10 on regulatory language quality, how accurately detector flags were translated into regulatory terminology, and the depth of reasoning (explaining *why* something is suspicious, not just *what* happened)

The final score is the average of both. The skill was then refined across 3 iterations, with one targeted change per round:

| Iteration | Change | Score |
|-----------|--------|-------|
| 1 — Baseline | No changes | 7.54 |
| 2 | Moved self-learning prompt out of SAR document body | 7.79 |
| 3 | Added strict content separation rule for evidentiary vs filing sections | 7.83 |

**How to run:**
```bash
cd sar-skill
python main.py
```

→ [`sar-skill/`](sar-skill/) — skill prompt, CLI, example cases, eval pipeline with iteration log

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

## Author

Jibin Kunjumon — jibz33on@gmail.com
