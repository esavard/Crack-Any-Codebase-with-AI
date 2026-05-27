# nanochat

_Lens: beginner-tutorial_

nanochat is an experimental harness for training large language models on a single GPU node. It simplifies the entire LLM lifecycle, from tokenization and pretraining to finetuning, evaluation, and inference, aiming for minimal, hackable code.


## Architecture

```mermaid
flowchart TD
    A0["Tokenizer"]
    A1["GPTConfig"]
    A2["GPT"]
    A3["DataLoader"]
    A4["Optimizer"]
    A5["Checkpoint"]
    A6["Training Script"]
    A7["Task"]
    A8["Engine"]
    A1 -- "defines blueprint for" --> A2
    A2 -- "is adjusted by" --> A4
    A2 -- "receives data from" --> A3
    A2 -- "is evaluated by" --> A7
    A2 -- "is run by" --> A8
    A0 -- "converts text for" --> A3
    A0 -- "decodes output for" --> A8
    A4 -- "state is saved to" --> A5
    A5 -- "stores state of" --> A2
    A6 -- "orchestrates training of" --> A2
    A6 -- "controls data flow for" --> A3
    A6 -- "configures" --> A4
    A6 -- "manages" --> A5
    A6 -- "uses for evaluation" --> A7
    A6 -- "adjusts parameters via" --> A1
    A6 -- "trains and evaluates" --> A0
    A6 -- "uses for sampling" --> A8
    A8 -- "solves problems for" --> A7
```

## Chapters

- [Tokenizer](01_tokenizer.md)
- [GPTConfig](02_gptconfig.md)
- [GPT](03_gpt.md)
- [DataLoader](04_dataloader.md)
- [Optimizer](05_optimizer.md)
- [Checkpoint](06_checkpoint.md)
- [Training Script](07_training_script.md)
- [Task](08_task.md)
- [Engine](09_engine.md)