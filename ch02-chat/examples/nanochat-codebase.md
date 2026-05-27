# Learning note: nanochat

> nanochat is karpathy's minimal harness for training a small ChatGPT-style LLM end to end on a single 8xH100 node, for under $100. One repo covers tokenizer, base pretrain, supervised finetune, reinforcement learning, evals, inference, and a chat UI. The whole stack is configured by one dial: `--depth`.

This is what my learning note looked like after one pass through the four step cycle (skeleton, follow up, edit, quiz). The interesting bits are the things I got *wrong* on the quiz, near the bottom.

## Concepts I need to know

| # | Concept | Plain English | Where in the code |
| - | ------- | ------------- | ----------------- |
| 1 | Tokenizer (BPE) | Splits text into integer chunks the model can ingest. Trained with a GPT-4 inspired regex split pattern. | `nanochat/tokenizer.py`, trained by `scripts/tok_train.py` |
| 2 | GPT (the model) | The transformer itself. Rotary embeddings, QK norm, ReLU squared MLP, no biases. Untied embedding and lm_head. | `nanochat/gpt.py` |
| 3 | Engine | The inference path: prefill, decode, KV cache, optional speculative decoding, optional tool use (Python calculator). | `nanochat/engine.py` |
| 4 | Base train | The pretrain loop. Reads packed token shards from `nanochat/dataloader.py`, optimizes the LM head with `nanochat/optim.py`. Optional FP8 via `nanochat/fp8.py`. | `scripts/base_train.py` |
| 5 | SFT (supervised fine tune) | Re-train on conversation traces so the base model learns the chat format. | `scripts/chat_sft.py` |
| 6 | RL (reinforcement learning) | A small RL loop on top of SFT. Currently shines on GSM8K (math reasoning) via the task definitions in `tasks/`. | `scripts/chat_rl.py`, reward tasks in `tasks/*.py` |
| 7 | Evals | Two flavors. Base evals (loss, CORE score, bits per byte) and chat evals (MMLU, ARC, GSM8K, HumanEval, SpellingBee). | `scripts/base_eval.py`, `scripts/chat_eval.py`, `nanochat/core_eval.py`, `nanochat/loss_eval.py` |
| 8 | Report | After a full training run, emits a single markdown report with config, environment, and every eval result. | `nanochat/report.py` |

## The important files

| # | File | What it does | Imports from |
| - | ---- | ------------ | ------------ |
| 1 | `runs/speedrun.sh` | The reference run. Tokenizer + base + SFT + RL + chat web. This is the entry point. | shell, calls every `scripts/*.py` |
| 2 | `scripts/base_train.py` | Pretrain loop. Auto sizes hyperparams from `--depth`. | `nanochat.{dataloader,gpt,optim,common}` |
| 3 | `scripts/chat_sft.py` | SFT loop. Takes a base checkpoint, fine tunes on conversation JSONL. | `nanochat.{gpt,tokenizer,engine}` |
| 4 | `scripts/chat_rl.py` | RL loop. Reward comes from `tasks/`. | `nanochat.{gpt,engine}`, `tasks.*` |
| 5 | `nanochat/gpt.py` | The transformer. ~600 lines. The whole model. | `nanochat.flash_attention` |
| 6 | `nanochat/engine.py` | Inference engine: prefill, decode, KV cache, tool use. | `nanochat.gpt` |
| 7 | `nanochat/tokenizer.py` | BPE tokenizer + the special chat format renderer. | (standalone) |
| 8 | `scripts/chat_web.py` | FastAPI server. Loads a checkpoint, serves `nanochat/ui.html`, streams chat completions. | `nanochat.{engine,tokenizer}` |

## Dependency chain

```
runs/speedrun.sh
    -> scripts/tok_train.py     (tokenizer)
    -> scripts/base_train.py    -> nanochat/gpt.py, dataloader.py, optim.py, fp8.py
    -> scripts/chat_sft.py      -> nanochat/gpt.py, engine.py, tokenizer.py
    -> scripts/chat_rl.py       -> tasks/*.py (rewards)
    -> scripts/chat_web.py      -> nanochat/engine.py, ui.html
    -> nanochat/report.py       (final markdown report)
```

## Questions I followed up on

- **Q**: nanochat advertises GPT-2 capability for $48. Where does that number come from?
  **A**: 8xH100 spot pricing at roughly $3/GPU/hour, times 2 hours, equals $48. The `runs/speedrun.sh` script is the canonical recipe. The leaderboard in the README tracks wall clock progress.

- **Q**: How is the chat format encoded? OpenAI uses `<|im_start|>` etc. What does nanochat do?
  **A**: `nanochat/tokenizer.py:render_conversation` adds the special tokens. The format is BPE plus a small set of role markers. The base model sees raw text; SFT teaches the role markers. Read `render_conversation` first if you want to fine tune on a custom dataset.

- **Q**: Why is FP8 a separate module (`nanochat/fp8.py`) instead of a flag inside `gpt.py`?
  **A**: FP8 needs scale tracking on each matmul. Bolting that into `gpt.py` would muddy the model definition. Keeping it as a wrapper means the architecture file stays readable, and FP8 is an opt in via `scripts/base_train --fp8`. The trade off: the FP8 path has its own bugs that the base path doesn't (per the leaderboard note "FP16 training not yet supported for RL").

## Things I got wrong on the quiz

- **Q**: If I change `--depth` from 26 to 12 on `scripts/base_train.py`, what *else* changes automatically?
  **What I guessed**: just the number of transformer layers.
  **Actually**: depth is the only dial, and the script auto computes width (`n_embd`), number of heads, learning rate schedule, training horizon, and weight decay. The README is loud about this ("All other hyperparameters are calculated automatically"). Lesson: when the codebase advertises one dial, every related hyperparam is downstream of that dial. Don't try to set them by hand.

- **Q**: Which file owns the `~/.cache/nanochat/` directory layout (checkpoints, tokenized shards, eval caches)?
  **What I guessed**: `nanochat/common.py`.
  **Actually**: I was half right. `common.py` defines `BASE_DIR` and `COMPUTE_DTYPE`, but the checkpoint dance lives in `nanochat/checkpoint_manager.py`. Convention: anything called `common.py` in this repo is constants and dtype/device picking, not state management.

- **Q**: Where does the chat UI run when I `python -m scripts.chat_web`?
  **What I guessed**: a Gradio app.
  **Actually**: a small custom FastAPI server that serves `nanochat/ui.html` as a static file and streams completions over an SSE endpoint. No Gradio dependency. If I want to swap the UI, I edit one HTML file; I don't fight a framework.

## When I read this in a month, the one thing to remember is

> nanochat is one dial (`--depth`) over a fixed recipe (`runs/speedrun.sh`). Everything else, hyperparameters, eval suite, report format, is downstream of that dial. Don't touch the hyperparameters; touch the depth.
