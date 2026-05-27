# Skill: Product Story

Agent equivalent of Chapter 5's product story workflow. Drop into `.claude/skills/product-story/SKILL.md` (Claude Code) or paste into a Cursor rule.

---
name: product-story
description: Reverse engineer a product story from a codebase. Pain scene, variant sentence, competitive positioning, surprises and absences. Read the product, not the code.
---

When the user asks "what does this codebase do" or anything about product intent, run these four prompts in order. Use the exact rules in each (the prompts are the chapter).

## Pipeline

### 1. Pain scene

Use [`../prompts/pain-scene.md`](../prompts/pain-scene.md). Output: 2 sentences. One specific person, one specific moment of frustration *before* this product existed. Name the surprising real competitor (often a manual workaround, not another product).

### 2. Variant sentence (Paul Graham's reproduce-it test)

Use [`../prompts/variant-sentence.md`](../prompts/variant-sentence.md). Output: "It's X, but Y." X is a product a non engineer would recognize. Y reveals the bet, not just the category.

### 3. Competitive positioning

Use [`../prompts/competitive-positioning.md`](../prompts/competitive-positioning.md). Output: a 4-dimension table comparing this product to 3 to 4 competitors, plus a counter-positioning analysis. Pick dimensions that ACTUALLY SPLIT the field. Look for what the product does *less* than others.

### 4. Surprises and absences

Use [`../prompts/surprises-and-absences.md`](../prompts/surprises-and-absences.md). Two tables. Surprisingly present features hiding in the code (each is a bet about the future). Deliberately absent features (each is a tradeoff).

## Output format

Write to `docs/product-story.md` in the target repo. Then ask the user if they want any section refined.

## Cardinal rules

- **No marketing words.** No "platform", "ecosystem", "leverages", "seamless", "scalable", "modern".
- **Cite the code for every claim.** File path or table name in backticks.
- **Write for a non engineer.** Gloss any developer concept in 5 words ("Firebase, the all in one backend Google sells to developers").
- **The pain must be a scene, not a summary.** "Scheduling is hard" is a summary. "Nine emails, four days, still no meeting" is a scene.
