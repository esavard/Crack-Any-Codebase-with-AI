Most beliefs about how a codebase behaves are wrong in some specific way. Find one such belief in THIS codebase, write a small test that would distinguish "true" from "wrong", run it, and tell me what we learned.

## How to pick the claim to test

Don't ask me. Look at the code yourself and pick a claim where:

- **Two functions touch the same value and ordering matters.** ("Validation runs before normalization." "The cache check happens before the network call." "The lint hook runs after format, not before.")
- **There's a silent fallback or skip.** ("If the config file is missing, X is used as the default" — is it really? Does the missing-file path get hit?)
- **A README claim or comment contradicts the runtime behavior.** Comments rot. Tests catch the rot.
- **A common assumption would silently produce wrong results.** ("Setting `output_attentions=True` returns attention weights" — does it really, with gradient checkpointing on?)

If you find several candidates, pick the one whose answer would change how someone uses or modifies the code.

## What to do

1. State the claim explicitly. One sentence I can quote.
2. Write a small focused test (10 to 30 lines). Use the project's existing test runner. Pick the smallest concrete input that would distinguish the two cases.
3. Actually run it. Don't just write it.
4. Report what happened.

## Output shape

```
## The claim

[One specific sentence. Quote the file or doc it came from if it's anchored somewhere.]

## Why this might be wrong

[1 to 2 sentences. What would have to be true for the claim to break? What's the failure mode I'd see in the wild if it does break?]

## The test

```language
[10 to 30 lines, runnable with the project's test command]
```

## Run output

```
[The actual stdout from running the test. Don't paraphrase.]
```

## What we learned

[If the test passed: one sentence + one edge case I should also test before fully trusting the claim.]
[If the test failed: a paragraph. What actually happened. Why the original claim was wrong. The code path that produced the surprise, with file:line.]

## For CLAUDE.md

[One-line gotcha to add to my skill file. Only if the test surfaced a surprise. If everything matched expectations, write "none".]
```

## Calibration

Bad claim to test: "The code works correctly."
Why bad: too vague to test. Pass means nothing. Fail means nothing.

Good claim to test: "`URI.from()` validates that paths starting without `/` are rejected, per the assertion at uri.ts:38."
Why good: specific, anchored to a line in the code, and the test is "construct a URI without a leading slash and see if it throws." A failing test produces a real learning: it turns out a cleanup function runs BEFORE the validator, silently adding the slash. The validator never sees the violation.

## Rules

- The failing test is the valuable one. If everything passes on the first hypothesis, you probably picked an obvious claim. Try a sharper one.
- Don't write a test for "does the project build." That's the next experiment ([`build-and-run.md`](build-and-run.md)).
- Don't write a property-based test. One concrete value that distinguishes the cases is enough.
- If you can't get the project's test runner working, say so. Don't fake the run output.
