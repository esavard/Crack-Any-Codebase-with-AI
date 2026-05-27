# Chapter 4. Agent

> Stop telling AI what to read. Let it decide. Then write down what it learned so the next session starts from knowledge, not amnesia.

## What this chapter ships

```
ch04-agent/
├── experiments/                # 3 paste-and-go prompts for your agent
│   ├── flow-trace.md
│   ├── understanding-test.md
│   └── build-and-run.md
├── codebase-skill/             # the "this codebase" skill file (per project)
│   ├── CLAUDE.md.template      # for Claude Code
│   └── .cursorrules.template   # for Cursor (same content, different filename)
└── domain-skill/               # the "any codebase" skill file (global)
    └── AGENTS.md.template
```

No `workflow/`, no scripts. The chapter argues agents are interactive and the repo follows.

## The three experiments

Each file under `experiments/` is a complete prompt. Open your agent (Claude Code, Cursor, Codex, Aider), pick the right experiment, copy the file's contents, paste, send. The agent picks the specific action / claim / target itself; you don't fill in anything.

| File | When to reach for it |
| ---- | -------------------- |
| [`experiments/flow-trace.md`](experiments/flow-trace.md) | You want to understand one specific user action end to end. Click, save, submit, send. The agent crosses 5 to 15 files and tells you the gateway where many entry points converge. |
| [`experiments/understanding-test.md`](experiments/understanding-test.md) | You have a belief about runtime behavior and you want to know if it's actually true. The agent writes a tiny test, runs it, and reports what's surprising. The failing tests are the valuable ones. |
| [`experiments/build-and-run.md`](experiments/build-and-run.md) | You need ground truth, not guesses. The agent eats the yak-shaving (language version mismatches, native module errors, missing system deps) and gets you to a running build. |

After each experiment, ask the agent: *"Add what you just learned to CLAUDE.md."* Every session ends with a one-line entry. Understanding compounds instead of evaporating.

## Why we don't ship a "give me the 10 abstractions" prompt

Agents share one context window for navigation, comprehension, and reasoning. A broad prompt spreads that budget thin: the agent skims 25 files and comes back with class signatures dressed as descriptions. The same `$0.02` of LLM time produces a far better overview when you run [Chapter 3's workflow](../ch03-workflow/) first and feed the result into your agent session. **Workflow once for the map, agent every day for the long tail.**

## The two skill files

The chapter's punchline (§4.5): you need TWO skill files, not one.

| File | Where it lives | What it holds |
| ---- | -------------- | ------------- |
| [`codebase-skill/CLAUDE.md.template`](codebase-skill/CLAUDE.md.template) (or [`.cursorrules.template`](codebase-skill/.cursorrules.template)) | `path/to/repo/CLAUDE.md` (Claude Code) or `path/to/repo/.cursorrules` (Cursor) | Build commands, gateway functions, gotchas, conventions discovered by running the experiments above. |
| [`domain-skill/AGENTS.md.template`](domain-skill/AGENTS.md.template) | `~/.claude/CLAUDE.md` (global) | Layer-specific rules from Parts 2 to 5 of the book. Carries from project to project. |

Both templates in `codebase-skill/` hold the same content. Pick the one that matches your agent.

Without these, the next session starts with "what is this codebase?" and burns ten turns rediscovering the obvious. With both, the agent walks in with the project's gotchas AND a playbook for how to think.

## Quickstart

1. Run the [Ch3 workflow](../ch03-workflow/) once on the target repo. Save the index to `path/to/repo/docs/architecture/`.
2. Copy [`codebase-skill/CLAUDE.md.template`](codebase-skill/CLAUDE.md.template) into the repo as `CLAUDE.md` (or `.cursorrules`).
3. Copy [`domain-skill/AGENTS.md.template`](domain-skill/AGENTS.md.template) into your home directory's agent config.
4. Open the repo in your agent. Run the three experiments in any order as questions come up.
5. End each session with *"Add what you just learned to CLAUDE.md."*

By the end of week one, your `CLAUDE.md` is a tight one-pager full of real discoveries. Every future session loads it for free.
