# Course 3: Claude API

## API Basics

To talk to Claude, you send a request with four things: your API key, which model to use, the conversation messages, and a max token limit. The response gives you back the text, how many tokens were used, and why Claude stopped.

- Generate keys in the Anthropic Console — one per project
- Store as an environment variable, never hardcode it

---

## Multi-Turn Conversations

The API has no memory. Every request must include the full conversation history — every user and assistant message from the beginning. Claude doesn't remember anything between calls.

---

## System Prompts

A special instruction you set once that applies to every reply. Use it to define Claude's role, set the output format, or add rules. It carries more weight than regular user messages.

---

## Temperature

Controls how predictable or creative Claude's responses are.

| Value | Behavior | Best for |
|-------|----------|---------|
| 0 | Always the same answer | Code, data extraction |
| 0.1–0.3 | Slight variation | Most production use |
| 0.7–1.0 | More creative and varied | Brainstorming, writing |

---

## Streaming

Instead of waiting for the full response, streaming sends it word by word as it's generated — like watching someone type in real time. Makes the app feel much faster.

---

## Prefilling

You can start Claude's reply for it by adding an assistant message at the end of the conversation. Claude will continue from exactly where you left off — useful for forcing a specific output format and skipping unnecessary preamble.

Not all models support this — Haiku 4.5 does, Sonnet 4.6 does not.

---

## Stop Sequences

Tell Claude to stop generating as soon as it hits a specific word or symbol. The stop word itself is not included in the output. Useful for extracting clean output without extra text at the end.

Tip: pair with prefilling to get clean JSON — start the reply with the opening fence, stop at the closing fence, and you get raw JSON with nothing to strip.

---

## Model Selection

| Model | Best for |
|-------|---------|
| Haiku 4.5 | High-volume, cheap, fast tasks |
| Sonnet 4.6 | Main work, complex tasks |
| Opus 4.5 | Deepest reasoning |

In pipelines: use Haiku for generating datasets and repetitive tasks, Sonnet where quality matters.

---

## Structured Outputs (JSON)

Tell Claude exactly what fields you want, what type each field is, and give an example. Always validate the response after the call — if it's malformed, retry.

---

## Prompt Evaluation

**The problem:** Testing a prompt a couple of times and assuming it works. Real users will always find inputs you didn't think of.

**The fix — evaluation loop:**

1. Write a prompt
2. Generate a dataset of test tasks
3. Run every task through the prompt
4. Grade each output (quality + format correctness)
5. Read the reasoning to understand what's failing
6. Tweak the prompt and repeat

Two types of grading combined:
- **Model grading** — Claude scores 1–10 for quality and explains why
- **Syntax grading** — deterministic check: is the output valid code/JSON/regex? 10 if yes, 1 if no
- Final score = average of both

If syntax scores are consistently low, the prompt isn't being specific enough about the output format.

---

## Tool Use (Function Calling)

Lets Claude call external functions — search engines, databases, APIs — and use the results in its response.

**How it works:**

1. You define tools (name, what it does, what inputs it takes)
2. You send the tools along with your message
3. Claude either replies normally, or asks to call one of the tools
4. Your code runs the function and sends the result back
5. Claude uses the result to finish its reply

You can give Claude multiple tools and it will pick the right one. You can also force it to always use a specific tool, or let it decide.

Built-in tools available: text editing and web search.

---

## RAG (Retrieval-Augmented Generation)

Solves the problem of Claude not knowing your private or up-to-date data. Instead of retraining the model, you retrieve relevant documents at query time and inject them into the prompt as context.

### Text Chunking Strategies

Documents are too long to send to Claude all at once, so you split them into smaller pieces called chunks. How you split them directly affects the quality of answers — bad chunking means Claude gets the wrong context.

| Strategy | How it works | Best for |
|----------|-------------|---------|
| **Size-based** | Split by fixed character count, with some overlap between chunks | Any document type — reliable default |
| **Structure-based** | Split on headers or sections | Markdown or well-formatted documents you control |
| **Sentence-based** | Split on sentence endings, group N sentences together | Most plain-text documents |
| **Semantic-based** | Group sentences by how related they are in meaning | Highest quality, but slow and complex |

**Overlap** — each chunk includes a few characters or sentences from the chunk before it, so context isn't lost at the boundary.

**Production default:** size-based with overlap — simple, works with any content type.

---

### Text Embeddings

After chunking, you need a way to find which chunks are most relevant to a user's question. Embeddings do this by converting text into a list of numbers that represent its meaning — so you can compare meaning mathematically, not just by matching keywords.

- Anthropic doesn't provide embeddings — use **VoyageAI** (free to start)
- The same model must embed both the chunks and the user's question for comparison to work
- When embedding chunks, use document mode; when embedding a query, use query mode

Think of it like GPS coordinates for meaning — two texts about the same topic will have numbers close to each other, even if they use different words.

---

## Workflows vs Agents

Two ways to build AI applications — choose based on how predictable the task is.

**Workflow** — you design the steps in advance. Claude follows a fixed sequence, each step focused on one small task. Like a recipe.

**Agent** — Claude gets a set of tools and figures out the steps itself. You don't know the exact sequence ahead of time.

| | Workflow | Agent |
|---|----------|-------|
| Best for | Well-defined, repeatable tasks | Unpredictable, open-ended tasks |
| Accuracy | Higher — focused on one subtask at a time | Lower — more decisions, more chances to go wrong |
| Testability | Easy — you know every step | Hard — steps vary each run |
| Flexibility | Low — built for specific inputs | High — handles novel situations |
| Predictability | High | Low |

**Default to workflows.** Users want reliability, not fancy AI. Only use agents when the task genuinely can't be broken into predictable steps upfront.

---

## Prompt Engineering Techniques

Start simple, measure the score, improve one thing at a time, repeat.

**Loop:** write baseline → evaluate → apply one technique → re-evaluate → repeat

### Techniques (in order of impact)

| # | Technique | What it does | Score |
|---|-----------|-------------|-------|
| 0 | Baseline | Vague instruction | 5.9 |
| 1 | **Clear & direct** | Start with an action verb, state the task and constraints upfront | 4.4 |
| 2 | **Output guidelines** | List exactly what the response must look like | 6.3 |
| 3 | **XML tags** | Wrap input content in descriptive tags to remove ambiguity | 6.7 |
| 4 | **One-shot example** | Show one perfect input/output pair | 8.2 |
| 5 | **Multi-shot examples** | Add more examples | 8.2 |

**Key takeaways:**
- Being clear and direct alone can hurt if the format isn't also specified
- Output guidelines are the real lever — especially "no markdown fences, raw output only"
- Examples are the most powerful technique: showing beats telling
- More examples have diminishing returns once Claude gets the pattern from one
- Change one thing at a time so you know what moved the score
