I want to understand who would actually choose this codebase's product over the dominant alternative in the same category, and why. From the codebase I pasted above, infer both:

- What this product IS (one sentence, what it does for an end user, not its tech stack).
- What the dominant alternative is. Name a real, well-known product that solves the same problem. If there isn't a single dominant one, pick the closest big-name competitor.

Then write a scene. Not a market analysis, not a feature comparison. One specific person with one specific day. The reader should remember this person next week.

## Output shape

```
**Product:** [one sentence]
**Dominant alternative:** [name]

---

[Name], [role, 8 words max].

[Paragraph 1: what they were trying to do. Specific. Not "build an ML pipeline" but "fine tune a small language model and log the attention weights at every checkpoint".]

[Paragraph 2: they reached for the alternative first. What broke. The exact file, abstraction, error message, or silent failure that made them give up. Name it. "Type error in modeling_gpt2.py line 1700, monkey-patched the method, then gradient checkpointing silently returned None." Not "it was too complex".]

[Paragraph 3: they switched to this codebase's product. What clicked. The exact action they took (the file they opened, the four lines they wrote) and how long it took. "Opened model.py, scrolled 330 lines, added four lines to save att to a list. 25 minutes."]
```

## Calibration

Bad: "Researchers and hackers who want hackable ML code choose nanoGPT because it's simple and readable."
Why bad: category words ("researchers", "hackers"), abstract benefits ("simple", "readable"), no scene, forgettable.

Good: "Priya, ML PhD student studying attention head specialization.

She wanted attention weights logged at every checkpoint. Started with HuggingFace Transformers. Set `output_attentions=True`. Worked in a notebook, broke the moment she wired it into the actual training loop: `TypeError: compute_loss() got an unexpected keyword argument 'output_attentions'`. Opened `modeling_gpt2.py`. 1700 lines, five nested `forward()` calls. Monkey-patched all five. Hit `RuntimeError: expected scalar type Float but found Half`. Fixed it. Turned on gradient checkpointing for the bigger run. `output_attentions` silently returned None. No error. No warning. A day and a half, gone.

Cloned nanoGPT. Opened `model.py`, scrolled: 330 lines, the entire model. Found `CausalSelfAttention.forward()`, read it line by line. Added four lines to save `att` to a list, dump at each checkpoint. Worked on the first try. 25 minutes."
Why good: name, exact role, specific tasks, real error messages, exact files, time costs you can feel.

## Rules

- If you can't name the file or the exact error that broke for the person, you're guessing. Pick a different example.
- "Easy", "simple", "complex", "powerful" are banned. Show the action, not the adjective.
- The pain has to be specific enough that switching to the new product would have *visibly* resolved it within an hour. Vague pain = vague switch.
- Use real, named, current products. No "Tool A" / "Tool B".
