Write me the skeleton of a personal learning note for the codebase I'm about to paste. This is not documentation for someone else. It is a study aid for me, the reader, to revisit in a month and instantly re-load the architecture into my head.

Assume I can read code in any mainstream language but I'm new to the domain this codebase operates in. Define domain specific terms inline the first time they appear.

## Output shape

Three sections, in this order. Use markdown tables where shown.

### Section 1. Concepts I need to know

A table of **the 5 to 8 most load-bearing ideas in this codebase**. Not every concept. The ones a newcomer cannot understand the system without.

| # | Concept | Plain English (one sentence, no jargon) | Where in the code |
| - | ------- | --------------------------------------- | ----------------- |

Rules:

- Max 8 rows. Eight fits on one screen and forces you to prioritize.
- "Plain English" means a sentence a smart undergraduate could follow. If you must use a domain term, define it inline the first time.
- "Where in the code" is a file path AND a function or class name. Not just `model.py`. Use `model.py:CausalSelfAttention.forward`.
- Order from foundational to derived. If concept B depends on concept A, A comes first.

### Section 2. The important files

A table of **5 to 8 files**. Same priority rule.

| # | File | What it does (one sentence) | Imports from (other files in this list) |
| - | ---- | --------------------------- | --------------------------------------- |

Rules:

- Max 8 rows.
- "Imports from" only counts cross-references inside this list, not stdlib or third party. That column is what builds the dependency chain in section 3.
- Don't include test files, lock files, configs, or one-shot scripts. Files the architecture depends on.

### Section 3. Dependency chain

A single line showing how the files in section 2 connect, top down:

```
entry_point.py
    -> file_a.py -> file_b.py
    -> file_c.py
```

This makes the import column from section 2 visually scannable.

## Calibration examples

Bad concept row: `Model | A neural network | model.py`
Why bad: "neural network" is jargon undefined, "model.py" is a path with no function pin.

Good concept row: `CausalSelfAttention | Each token only sees tokens to its left, which is what makes this "GPT" instead of "BERT" | model.py:CausalSelfAttention.forward`
Why good: plain English definition, concrete file and function.

Bad file row: `train.py | Trains the model | model.py`
Why bad: "trains the model" is a tautology of the name.

Good file row: `train.py | Reads packed token shards from disk, runs the optimizer loop, writes checkpoints every N steps | model.py, dataloader.py`
Why good: tells me what actually happens, names the specific concrete files it pulls from.

## What to skip

- Don't write a project summary at the top. The README has one. This note is for things the README *can't* tell me.
- Don't list every concept you spot. The point of "max 8" is to force you to argue with yourself about what matters most.
- Don't add a "future work" or "improvements" section. This is a learning note, not a planning doc.

Codebase follows.
