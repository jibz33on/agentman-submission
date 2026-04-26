# Course 1: Introduction to Agent Skills

## Key takeaways

- Skills are dormant until their description matches a request — the description does all the triggering work, not the skill name
- SKILL.md is a runbook written in English, not code. Claude reads it and executes the steps. Scripts live in `scripts/` and get called by the runbook.
- Progressive disclosure: keep SKILL.md under 500 lines, link to references that load on-demand
- One skill = one user capability. Internal complexity (multiple scripts, multiple steps) is fine, but the user only triggers once.

## What surprised me

- I expected skills to be Python code that Claude runs. They're actually instructions Claude follows while using its normal tools.
- The restart requirement — skills load at startup, so edits don't apply until you restart Claude Code.

## Still fuzzy on

- How exactly does semantic matching work in descriptions? Is it keyword-based or something smarter?
- When would I use `allowed-tools` in real life?o
