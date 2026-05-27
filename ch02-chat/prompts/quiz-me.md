I just spent an hour reading the codebase I pasted above. I'm going to feel like I understand it. I probably don't. Quiz me.

## What I want

Three multiple choice questions. Four options each. The goal is to surface the gaps in my mental model, not to give me a confidence boost. Hard but fair.

## What makes a good question

A good question **connects two specific code locations**: "what happens in file A when you change value B in file C." Single-file questions test recall ("what does function foo return?"). Cross-file questions test understanding ("if you change X in foo, what breaks in bar?"). I want the second kind.

Three things I should be tested on:

1. **Cause and effect across files.** Change a config or constant in one file. What downstream code breaks, silently degrades, or starts behaving differently? Use the real variable name from the real file.
2. **Ordering and assumptions.** Two functions both touch the same value. Which one runs first? What does the second one assume the first one did? Where would a bug hide if that assumption broke?
3. **Counterfactuals.** Pick a real design choice in the code (a constant, a default, a missing feature). What would happen if it were the other way? This forces me to articulate why the current choice exists.

## Output shape

```
**Q1.** [Setup: one or two sentences naming the specific files and values involved. Reference real file paths and variable names from the codebase.]

[Question: a "what happens if" or "which file would you change" prompt.]

A) [plausible wrong answer]
B) [plausible wrong answer]
C) [correct answer]
D) [plausible wrong answer]

---

**Q2.** ...

---

**Q3.** ...

---

## Answer key

Don't reveal until I ask. When I ask, give:

**Q1:** [letter]. [One paragraph explanation. Walk through the actual code path. Cite the file and function. Name what the wrong answers each got subtly wrong, because the wrong answers are where I'll learn the most.]
```

## Calibration

Bad question: "What does the `Block` class do in `model.py`?"
Why bad: single file, tests recall, the answer is a paragraph from the file's top docstring.

Good question: "In `train.py`, `gradient_accumulation_steps` defaults to 40 and `tokens_per_iter` is calculated as `gradient_accumulation_steps * ddp_world_size * batch_size * block_size`. You change `gradient_accumulation_steps` from 40 to 20 on a single GPU. What is the *most direct* consequence? A) `tokens_per_iter` halves; effective batch size shrinks; training stability may suffer. B) `tokens_per_iter` halves but it's just a log variable, no effect. C) Nothing changes; `ddp_world_size` compensates. D) `tokens_per_iter` doubles because the optimizer steps twice as often."
Why good: cross-file (config touched, training behavior affected), specific variable names, plausible distractors that each correspond to a real misunderstanding someone could have.

## Rules

- Use ONLY variable names, file names, and constants that actually exist in the codebase I gave you. No invented "Project Phoenix" examples.
- Wrong answers must be wrong for a *specific reason* I could learn from, not silly.
- Don't go easy. I'd rather fail now than discover the gaps in production.

Codebase follows.
