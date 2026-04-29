# Eval Iterations — SAR Narrative Generator

## Grading Criteria

**Rule-based (automated):**
- All 6 sections present (SUSPICIOUS_ACTIVITY_DESCRIPTION, INDICATORS_OF_SUSPICION, PRIOR_RELATIONSHIP, RECOMMENDED_ACTION, THRESHOLD CHECK, ANALYST REMINDER)
- No crime conclusions ("committed fraud", "is guilty", etc.)
- No first person language
- Correct recommended action (freeze vs monitor)

**Model grading (Claude scores 1–10):**
- Regulatory language quality
- FraudSentinel flag → regulatory language mapping
- Insight quality (explains WHY, not just WHAT)
- Analyst notes incorporated correctly

**Combined score** = average of rule score + model score

---

## Iteration Log

### Iteration 1 — Baseline

**Date:** 2026-04-29
**Skill version:** 1.0  
**Changes:** None — baseline run

| Case | Rule | Model | Combined |
|------|------|-------|----------|
| case1_baseline | 7.8 | 7.5 | 7.6 |
| case2_borderline | 7.8 | 5.8 | 6.8 |
| case3_high_risk | 7.8 | 8.8 | 8.2 |
| **Average** | **7.8** | **7.4** | **7.54** |

**What failed:**
- Case 2 model score dragged down (5.8) — the self-learning prompt ("I'll store your preferences") was flagged as inappropriate in a compliance document
- Analyst notes handling introduced procedural confusion — the draft mixed filing recommendations into what should be a neutral evidentiary narrative

**What to improve:**
- Remove the self-learning ask from the SAR output itself — preferences.md is updated separately, not inside the draft
- Keep the SAR narrative purely evidentiary — no prompts, no threshold adjudication inside the document body

---

### Iteration 2

**Date:** 2026-04-29
**Change made to skill.md:** Moved self-learning prompt out of SAR document body — now triggers as a separate follow-up after the draft is complete. Added explicit instruction: do not embed preference prompts or data-collection language inside the SAR narrative.
**Why:** Model grader flagged the self-learning ask as inappropriate in a compliance document — mixing filing recommendations and preference harvesting into a neutral evidentiary record introduced procedural confusion and potential tipping-off risk.

| Case | Rule | Model | Combined |
|------|------|-------|----------|
| case1_baseline | — | — | — |
| case2_borderline | — | — | — |
| case3_high_risk | — | — | — |
| **Average** | | | **7.79** |

> **Note:** Per-case scores were not captured during this run — only the average was recorded. Individual case scores exist for Iterations 1 and 3.

**What improved:** Average score up from 7.54 → 7.79 (+0.25). Case 2 model score was the primary drag — fix directly addressed the flagged issue.

**What still needs work:** See Iteration 3.

---

### Iteration 3

**Date:** 2026-04-29
**Change made to skill.md:** Added strict content separation rule — SUSPICIOUS_ACTIVITY_DESCRIPTION, INDICATORS_OF_SUSPICION, and PRIOR_RELATIONSHIP must contain facts and observed behaviour only. Filing decisions and threshold guidance restricted to RECOMMENDED_ACTION. Procedural warnings restricted to ANALYST REMINDER.
**Why:** Model grader flagged that compliance adjudication (threshold commentary, filing recommendations) was leaking into the evidentiary narrative sections, weakening the document's regulatory integrity.

| Case | Rule | Model | Combined |
|------|------|-------|----------|
| case1_baseline | 7.8 | 8.5 | 8.1 |
| case2_borderline | 7.8 | 7.0 | 7.4 |
| case3_high_risk | 7.8 | 8.2 | 8.0 |
| **Average** | **7.8** | **7.9** | **7.83** |

**What improved:** Score up from 7.79 → 7.83 (+0.04). Incremental gain — the structural separation rule tightened the output.

**Final notes:** Total improvement across 3 iterations: 7.54 → 7.83 (+0.29). Two targeted prompt changes, both driven by model grader feedback. Eval pipeline complete.
