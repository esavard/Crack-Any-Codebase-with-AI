Look back at the learning note you just gave me. Pick the **single line that's most likely to be wrong, hand-wavy, or hiding a sibling concept I'd confuse it with**. Quote it verbatim.

Then put it under a microscope: compare what it says against the closest concept it's NOT (the sibling I might mix it up with). Use a concrete worked example, not abstractions.

## Output shape

```
## Line under microscope

> [verbatim quote of the line you picked]

## What it actually means: [thing] vs [sibling thing]

Input: [one concrete example, e.g. the sentence "The bank by the river"]

### What [thing] does with it
1. Step 1...
2. Step 2...
3. Result: ...

### What [sibling thing] would do with it
1. Step 1...
2. Step 2...
3. Result: ...

### Why this codebase chose [thing]
One sentence. Cite the file or line that proves the choice.
```

## How to pick the line

Look for:

- Lines that use a jargon term without saying which sibling concept it's *not*.
- Lines that say what something IS but not what would happen if you changed it.
- Lines you'd be tempted to hand-wave past in a code review.

If everything in the note feels solid, pick the most foundational concept anyway. Foundational lines are where the biggest mental model bugs hide.

## Calibration

Bad: "Self-attention is when a token attends to other tokens in the same sequence. Cross-attention is when it attends to a different sequence."
Why bad: I could have read that on Wikipedia. It tells me what the words mean, not what happens.

Good: "Take the sentence 'The bank by the river'. In self-attention, when the model processes 'river', it looks back at 'The', 'bank', 'by', 'the'. The score for 'bank' is high, which is what disambiguates 'bank' as riverbank, not financial. In cross-attention, when generating 'rivière' in French, the model looks at the entire English sentence as a separate sequence. nanoGPT only uses self-attention because it's decoder-only: one sequence in, next token out. (`model.py:CausalSelfAttention`)"
Why good: walks through one concrete example, shows the mechanism, ties the choice to a real file.

## Rule

If you find yourself writing a definition, stop and start over with an example.
