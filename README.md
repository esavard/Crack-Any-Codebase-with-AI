# Crack Any Codebase with AI

Companion repo for the book. Each chapter directory is self-contained; start anywhere.

## Setup

Install once from the repo root. Choose the LLM provider you want to use:

**pip**

```bash
pip install -e .               # Anthropic Claude (default)
pip install -e ".[openai]"     # OpenAI
pip install -e ".[google]"     # Google Gemini
```

**uv**

```bash
uv sync                        # Anthropic Claude (default)
uv sync --extra openai         # OpenAI
uv sync --extra google         # Google Gemini
```

Then export the matching API key:

```bash
export ANTHROPIC_API_KEY=...   # Claude
export OPENAI_API_KEY=...      # OpenAI
export GEMINI_API_KEY=...      # Gemini
export OLLAMA_HOST=http://localhost:11434   # local Ollama (no key needed)
```

The `utils/call_llm.py` wrapper picks the provider automatically from whichever key/host is set.
To force a specific provider regardless of which keys are present, set `LLM_PROVIDER=anthropic|openai|gemini|ollama`.
To override the model, set `ANTHROPIC_MODEL`, `OPENAI_MODEL`, `GEMINI_MODEL`, or `OLLAMA_MODEL`.

**Ollama** uses the OpenAI-compatible endpoint (`/v1/chat/completions`) — no extra dependency required.
Default host: `http://localhost:11434`. Override the model with `OLLAMA_MODEL=your-model`.

## Chapters

| Chapter | What it builds |
| ------- | -------------- |
| [ch02-chat](ch02-chat/) | Prompt templates for manual codebase exploration in a chat window |
| [ch03-workflow](ch03-workflow/) | Automated codebase tour generator (PocketFlow pipeline) |
| [ch04-agent](ch04-agent/) | Agent experiments + skill file templates |
| [ch05-product-intent](ch05-product-intent/) | Reverse-engineer the PRD from the code |
| ch06–ch18 | _(coming soon)_ |
