Look back at your previous answer. Pick the **single most abstract claim** you made: a sentence I'd nod at and forget. Quote it.

Then prove it with the smallest possible worked example: real arithmetic, integers where possible, every intermediate value shown. End with a one-sentence punchline that says what the arithmetic proved.

## How to pick the claim

Look for:

- Anything with "because [vague principle]". Prove the principle.
- Anything with "equivalent to" or "approximately the same as". Show that they actually are.
- Anything with "for performance reasons" or "this is optimized". Show the cheaper path actually costs less.
- Anything I'd struggle to whiteboard for a teammate.

## Sizing rules

- **One scalar weight (not a vector, not a matrix). Two to four data points.**
- **Inputs and outputs are integers or simple fractions.** No floats with five decimals.
- **Show every intermediate value.** Not "the gradient is computed", but "gradient = 2 * (0 - 1) * 1 = -2".
- **At most 20 lines of arithmetic.** If you need more, your scenario isn't small enough.

## Output shape

```
## Claim under the microscope

> [verbatim quote of the abstract claim from your previous answer]

## Setup
- Model: ŷ = w * x
- One weight w = 0
- Loss: (ŷ - y)^2
- Learning rate: 0.1
- Data: (1, 1), (2, 2), (3, 3), (4, 4)

## Path 1: [name the first approach]
- Prediction for each x: ...
- Per-sample gradient: ...
- Mean gradient: ...
- Weight update: w = ...

## Path 2: [name the second approach]
- ...

## Punchline
[One sentence. What the arithmetic just proved.]
```

## Calibration

Bad: "Gradient accumulation works because gradients are linear, so summing them across mini-batches gives the same result as a single large batch."
Why bad: I could have read that in the docstring. It tells me the rule, not why it's true.

Good: walks through the worked example above and ends with "Same gradient (-15). Same weight update (1.5). Works because mean of means equals overall mean."
Why good: I just did the math myself. The punchline is now obvious instead of mysterious.

## Rules

- If you write "approximately" or "roughly", restart with smaller numbers.
- If the example takes more than one screen to walk through, your scenario is too big.
- The punchline must be one sentence. If you need a paragraph, the example didn't do its job.
