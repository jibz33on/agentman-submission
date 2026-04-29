# SAR Narrative Generator

**Version:** 1.0  
**Author:** Jibin Kunjumon  
**Category:** Fintech / Compliance (Moneyman)

## Description

Drafts a Suspicious Activity Report (SAR) narrative from a REJECTED transaction and its FraudSentinel agent output. Produces compliance-ready prose in FinCEN / FCA format that a compliance officer can review, edit, and file.

Writing SARs is legally mandatory for transactions above regulatory thresholds. This skill turns raw fraud agent output into a structured regulatory document in seconds — replacing 20–30 minutes of manual drafting per case.

---

## When to Use This Skill

- FraudSentinel has issued a REJECTED verdict on a transaction
- The transaction meets or may meet SAR filing thresholds (typically >$5,000 / £3,000, or any amount involving known high-risk categories)
- A compliance officer needs a first-draft SAR narrative to review and file
- You want consistent, regulator-ready language across all filings

---

## Procedure

Follow these steps in order:

### Step 1 — Parse the Input

Extract and organise the following from the pasted input:

**Transaction data:**
- Amount, currency, merchant name, merchant location
- Date and time of transaction
- Device type, IP address

**User profile:**
- Account identifier (anonymised ID or reference — never use real name in draft)
- Account age in days
- Transaction count and average spend
- Known countries, known merchants, typical hours

**FraudSentinel agent output:**
- Detector flags triggered (list)
- Detector score (0–100)
- Investigator deviation score (0–100) and summary
- Final verdict (REJECTED), confidence %, decision reason

**Analyst notes** (if provided — optional)

If any of the above are missing, note the gap in the output rather than inventing values.

### Step 2 — Check Reporting Threshold

Before drafting:
- If amount < $5,000 / £3,000 AND no high-risk category flag is present → add a threshold warning at the top of the output
- If amount ≥ threshold OR high-risk category flag is present (crypto, wire transfer, casino, forex) → proceed with full SAR draft
- Always remind the analyst: thresholds vary by jurisdiction and institution — they must confirm before filing

### Step 3 — Draft the SAR Narrative

Produce the narrative in the output format below. Write in:
- Past tense
- Third person
- Factual, neutral language — describe behaviour, never conclusions
- Regulatory tone: "activity consistent with...", "deviates significantly from established pattern", "warrants further review"

Never state the subject committed a crime. Never invent facts not present in the input.

Strict separation of content:
- `SUSPICIOUS_ACTIVITY_DESCRIPTION`, `INDICATORS_OF_SUSPICION`, `PRIOR_RELATIONSHIP` — facts and observed behaviour only. No filing recommendations, no threshold commentary, no compliance adjudication.
- `RECOMMENDED_ACTION` — the only section where filing decisions and threshold guidance belong.
- `ANALYST REMINDER` — the only section for procedural warnings.

### Step 4 — Map Agent Flags to Regulatory Language

Translate FraudSentinel detector flags into regulator-recognisable terminology:

| FraudSentinel Flag | Regulatory Language |
|---|---|
| velocity | Structuring / rapid sequential transactions |
| high_risk_merchant | Transaction involving high-risk merchant category |
| foreign_transaction | Cross-border activity inconsistent with profile |
| ip_location_mismatch | Geolocation inconsistency suggesting account compromise |
| new_device | Access from previously unregistered device |
| amount_vs_baseline | Transaction amount significantly exceeding established baseline |
| new_account | Limited transaction history; insufficient behavioural baseline |

### Step 5 — Suggest Next Action

Based on confidence % and detector score, recommend one of:
- **File SAR** — high confidence, clear indicators
- **Freeze account and file SAR** — critical risk score or multiple high-risk flags
- **Monitor and file if repeated** — borderline case, first anomaly

---

## Output Format

```
SUBJECT: [Account reference] | Transaction Ref: [TX ID or timestamp]

⚠️ THRESHOLD CHECK: [ABOVE THRESHOLD — proceed with filing / BELOW THRESHOLD — confirm with compliance before filing]

---

SUSPICIOUS_ACTIVITY_DESCRIPTION:
[3–5 sentences. Past tense, third person. What happened: amount, merchant, 
location, time, device. How it deviates from the account's established pattern. 
No conclusions — facts only.]

INDICATORS_OF_SUSPICION:
[2–4 sentences. Map the specific agent flags to regulatory language. 
Explain why each indicator is significant in fraud typology terms.]

PRIOR_RELATIONSHIP:
[1–2 sentences. Account age, typical behaviour, transaction history. 
Is this an isolated anomaly or part of a pattern?]

RECOMMENDED_ACTION:
[One sentence: file SAR / freeze account and file SAR / monitor and file if repeated]

---
⚠️ ANALYST REMINDER: Review all figures against source data before filing. 
Thresholds vary by jurisdiction. This is a first draft — do not file without review.
```

---

## Edge Cases

| Situation | How to handle |
|---|---|
| New account (<5 transactions) | Note investigator was blind; weight detector flags more heavily; flag to analyst |
| Multiple flags but low amount | Note below threshold but recommend monitoring; flag high-risk category if present |
| Investigator deviation = 0 | Note baseline match; contrast with detector signal; let analyst decide |
| Missing transaction amount | Do not estimate; note the gap; flag to analyst before filing |
| Analyst notes contradict agent output | Include both perspectives; do not resolve the contradiction — flag it |
| Confidence < 60% | Add a low-confidence warning; recommend monitor rather than immediate filing |

---

## Self-Learning

After delivering the SAR draft, ask this as a separate follow-up — never inside the document body:

> "Was this draft accurate? Anything I missed, overstated, or should phrase differently next time?"

Only ask this after the full SAR output is complete. Do not embed this question, any preference prompts, or any data-collection language inside the SAR narrative itself — the document must remain a neutral evidentiary record.

Store corrections in `preferences.md`. Useful things to capture:
- "Always include the investigator deviation score in the indicators section"
- "Our jurisdiction threshold is £5,000 not £3,000 — always use that"
- "Always recommend account freeze when ip_location_mismatch + foreign_transaction both fire"

Read `preferences.md` at the start of every session if it exists.

---

## Example

**Input:**

```
Transaction: £4,200 | Merchant: CryptoSwap Pro | Location: Lagos, Nigeria
Date/Time: 2024-03-15 03:42 | Device: Mobile (new) | IP: 102.89.33.201

User: ACC-00847 | Account age: 23 days | Tx count: 4 | Avg spend: £180
Known countries: UK | Known merchants: Tesco, Netflix, Amazon
Typical hours: 08:00–22:00

Detector flags: foreign_transaction, high_risk_merchant, new_device, new_account
Detector score: 87
Investigator: SKIPPED (< 5 transactions)
Verdict: REJECTED | Confidence: 91% | Reason: High-risk merchant + foreign IP on new account with no behavioural baseline
```

**Output:**

```
SUBJECT: ACC-00847 | Transaction Ref: 2024-03-15T03:42

⚠️ THRESHOLD CHECK: BELOW £5,000 THRESHOLD — confirm with compliance before filing. 
Note: high-risk merchant category (crypto) may trigger mandatory reporting regardless of amount.

---

SUSPICIOUS_ACTIVITY_DESCRIPTION:
On 15 March 2024 at 03:42, account ACC-00847 initiated a transaction of £4,200 to 
CryptoSwap Pro, a cryptocurrency exchange, from a location in Lagos, Nigeria. The 
account, opened 23 days prior, had recorded only four previous transactions totalling 
approximately £720, all to established UK retail merchants during daytime hours. 
The transaction was conducted via a previously unregistered mobile device and originated 
from an IP address inconsistent with the account's known geography.

INDICATORS_OF_SUSPICION:
The transaction exhibits multiple indicators consistent with account takeover or 
money laundering activity. The merchant category (cryptocurrency exchange) represents 
a high-risk typology associated with layering of illicit funds. The transaction amount 
of £4,200 exceeds the account's established average spend of £180 by a factor of 23, 
representing a significant deviation from baseline behaviour. Access from an unregistered 
device combined with a foreign IP address is consistent with unauthorised account access.

PRIOR_RELATIONSHIP:
Account ACC-00847 was opened 23 days ago and has a limited transaction history of four 
transactions. The account has shown no prior international activity and no prior 
transactions to high-risk merchant categories. Insufficient history exists to establish 
a reliable behavioural baseline.

RECOMMENDED_ACTION:
Freeze account pending investigation and file SAR if amount or merchant category meets 
jurisdictional reporting threshold — confirm with compliance officer before filing.

---
⚠️ ANALYST REMINDER: Review all figures against source data before filing. 
Thresholds vary by jurisdiction. This is a first draft — do not file without review.
```
