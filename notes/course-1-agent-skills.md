# Course 1: Introduction to Agent Skills

## Key takeaways

- Skills are NOT Python code that runs automatically — they're English instructions that Claude reads and follows step-by-step
- SKILL.md is a runbook. Claude executes it by using its normal tools (bash, file writes, etc.)
- The description field does two jobs: explains WHAT the skill does + lists WHEN to trigger it (trigger phrases matter)
- One skill = one user-facing capability. Multiple internal steps are fine, but user triggers once.
- Progressive disclosure: SKILL.md stays under 500 lines, heavy content goes in separate files that load on-demand

## What the practice skill taught me

- The description needs concrete trigger phrases ("log today's progress", "journal entry") — vague descriptions won't match
- Skills load at startup, so you have to restart Claude Code after editing
- Watching Claude follow the runbook step-by-step (check file → ask questions → append entry) made it click that SKILL.md is literally a checklist, not magic

## Still fuzzy on

- How to structure a long SKILL.md — what's the pattern for linking to external references?
- Best practices for writing example usage (should examples be in SKILL.md or separate files?)
- How semantic matching actually works under the hood (is it just keyword overlap or something smarter?)
