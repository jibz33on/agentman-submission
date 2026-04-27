# Course 3: Claude API

## API Basics

Send a `POST` to `/v1/messages` with these four fields:

| Field | What it is |
|-------|-----------|
| `x-api-key` | Your API key (in the header) |
| `model` | Which Claude version to use |
| `messages` | The conversation content |
| `max_tokens` | Cap on response length |

- Generate keys in the [Anthropic Console](https://console.anthropic.com) — one per project
- Store as an environment variable, never hardcode
- Response includes: text, token usage, stop reason, model used

---

## Multi-Turn Conversations

The API is stateless. Send the full message history with every request — Claude has no memory between calls.

```python
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "What's the capital of France?"},
]
```

---

## System Prompts

Sit outside `messages`, apply to every response. Use for role definitions, output format requirements, and behavioral constraints. More authoritative than user messages.

---

## Temperature

| Value | Behavior | Best for |
|-------|----------|---------|
| `0` | Deterministic | Code, data extraction |
| `0.1–0.3` | Slight variation | Most production use |
| `0.7–1.0` | Creative | Brainstorming, writing |

Default for production: `0–0.3`.

---

## Streaming

Delivers the response incrementally via Server-Sent Events — user sees text appear in real time instead of waiting for the full response. Significant latency improvement for conversational interfaces.

---

## Prefilling

Add an `assistant` message at the end of `messages` to seed Claude's response. Claude continues from there.

```python
messages = [
    {"role": "user", "content": "Generate tasks in JSON"},
    {"role": "assistant", "content": "```json"},  # Claude continues here
]
```

Use to skip preamble and force a specific output structure. **Not all models support it** — Haiku 4.5 does, Sonnet 4.6 does not.

---

## Stop Sequences

Stop generation when Claude hits a specific string (string excluded from output).

```python
client.messages.create(..., stop_sequences=["```"])
```

**Pair with prefilling for clean JSON:** prefill with ` ```json `, stop at ` ``` ` → raw JSON, no fences to strip.

---

## Model Selection

| Model | ID | Best for |
|-------|-----|---------|
| Haiku 4.5 | `claude-haiku-4-5-20251001` | High-volume, cheap/fast tasks |
| Sonnet 4.6 | `claude-sonnet-4-6` | Main work, complex tasks |
| Opus 4.5 | `claude-opus-4-5` | Deepest reasoning |

In pipelines: use Haiku for dataset generation and workers, Sonnet where quality matters.

---

## Structured Outputs (JSON)

Prompt Claude explicitly with field names, types, and an example schema. Validate the response after the call — retry if malformed.

---

## Prompt Evaluation

**The problem:** Testing a prompt once or twice, then shipping. Production users always find inputs you didn't consider.

**The fix — evaluation-first loop:**

| Step | What happens | Script |
|------|-------------|--------|
| Draft | Write/edit the prompt | `run_eval.py` |
| Dataset | Generate test tasks with format tags | `generate_dataset.py` → `dataset.json` |
| Generate | Run each task through Claude | `run_prompt()` |
| Grade | Score quality + syntax validity | `grade_by_model()` + `grade_syntax()` |
| Iterate | Tweak prompt, re-run, compare avg scores | repeat |

Dataset generation uses Haiku + prefilling + stop sequences for cheap, clean JSON. Each task has a `"format"` field (`"python"`, `"json"`, `"regex"`) so the syntax grader knows what to validate.

**Grading — two scores combined:**
- `grade_by_model()` — Claude scores 1–10 for quality + returns reasoning
- `grade_syntax()` — deterministic: `ast.parse` / `json.loads` / `re.compile` → 10 if valid, 1 if not
- `score = (model_score + syntax_score) / 2`

Model grading catches quality issues; code grading catches structural failures (markdown fences, truncated output). If syntax scores are consistently low, tighten the prompt: "Return raw code only, no markdown fences."

```bash
uv run --with anthropic --with python-dotenv generate_dataset.py  # once
uv run --with anthropic --with python-dotenv run_eval.py          # every iteration
```

---

## Prompt Engineering Techniques

Iterative refinement: start simple, measure, improve one thing at a time, repeat.

**Loop:** goal → baseline prompt → evaluate → apply one technique → re-evaluate → repeat

- Start with a naive prompt (~2–3/10 is expected) — gives you a baseline to beat
- Pass `extra_criteria` to the grader so it knows what a good response requires
- Read the `reasoning` field to understand *why* scores are low before picking your next change

### Techniques (in order of impact)

| # | Technique | What it does | Score |
|---|-----------|-------------|-------|
| 0 | Baseline | `Please solve the following task` | 5.9 |
| 1 | **Clear & direct** | Start with an action verb, state task + constraints upfront | 4.4 |
| 2 | **Output guidelines** | List explicit requirements for the response format | 6.3 |
| 3 | **XML tags** | Wrap content in descriptive tags to remove ambiguity | 6.7 |
| 4 | **One-shot example** | Show one ideal input/output pair using `<sample_input>` / `<ideal_output>` | 8.2 |
| 5 | **Multi-shot examples** | Add more examples per format type | 8.2 |

**Key takeaways:**
- Clear & direct alone can hurt if the output format isn't also specified
- Output guidelines are the real lever — especially for format constraints like "no markdown fences"
- Examples are the most powerful technique: showing beats telling
- Multi-shot has diminishing returns once Claude understands the pattern from one example
- Always make one change at a time so you know what moved the score
