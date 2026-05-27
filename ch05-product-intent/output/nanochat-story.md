# nanochat

_A product story reverse engineered from the codebase._

## The pitch

> It's like building your own ChatGPT, but it's a minimal codebase that allows individual developers to train a GPT-2 capability chat AI from scratch for under $100.

## The pain

> An ambitious student, Kai, wants to train his own LLM to explore cutting-edge research, but each Google search reveals projects costing tens of thousands of dollars and requiring massive, complex setups. His real competitor isn't another coding framework, it's the financial barrier and the overwhelming feeling that this field is only for tech giants.

## Where it sits

### What it gives up

- nanochat sacrifices state-of-the-art model scale and raw capability by focusing on micro models up to GPT-2 level.
- It trades plug-and-play ease of use for requiring users to set up a Python environment, manage GPUs, and run scripts directly.
- The project is an experimental harness, not a robust, managed production platform with enterprise-grade features or scalability.
- nanochat prioritizes minimalism, which means it may lack the comprehensive features or alternative architectures found in broader frameworks.

### What it gets in return

- It achieves unparalleled cost-efficiency, allowing users to train a full GPT-2 model for less than $100.
- Users gain full ownership and control over the code, the trained models, and the entire AI pipeline.
- It serves as an excellent educational tool for deeply understanding LLM internals, training processes, and systems optimizations.
- The codebase is extremely hackable, making it simple to modify, experiment with, and adapt to specific research ideas.
- The project is highly optimized for 'time to GPT-2', allowing for rapid iteration and quick achievement of a functional model.

### Why incumbents can't copy this

OpenAI and other API providers cannot copy nanochat's core value proposition without destroying their business model. Their revenue comes from selling access to proprietary, large-scale models, not from empowering users to build and own entire training pipelines for cheap. Offering nanochat's fully open-source, self-hosted training for sub-$100 would directly cannibalize their primary revenue stream and expose their core intellectual property. HuggingFace, while open-source, operates as a general-purpose hub supporting a vast ecosystem. Adopting nanochat's extreme minimalism and single-node, sub-$100 focus would require sacrificing the platform's broad flexibility and its capacity for complex, distributed research, which is central to its brand and utility.

### Side by side

**Dimensions**

- **Code is Public?**: Can you see and change how the software works, or is it a secret paid service?
- **Train Small Model Price?**: How much does it cost to train a basic AI from scratch, like a GPT-2 level model, to talk to?
- **Full AI Process?**: Does it handle all steps of making an AI, from raw data to a working chat bot, or just parts?
- **Easy to Change?**: Can you easily change the inner workings of the AI code to experiment, or is it a fixed tool?

| Product | Code is Public? | Train Small Model Price? | Full AI Process? | Easy to Change? |
| --- | --- | --- | --- | --- |
| **nanochat** | **Open**. Every file is plain Python you can fork, with an MIT license for full transparency and modification. | **<$100**. The README documents a $48 training run to achieve GPT-2 level capability on an 8xH100 node. | **Yes**. It covers the entire pipeline: tokenization, pretraining, finetuning, evaluation, inference, and a web chat UI. | **Very**. It is explicitly designed to be minimal, hackable, and controlled by a single complexity dial for easy experimentation. |
| **OpenAI ChatGPT/GPT-4 API** | **Closed**. Access is API-only, meaning the core model code and architecture are proprietary and hidden. | **Per token**. Costs scale by usage (tokens), not by a one-time training investment, and training your own small model isn't offered. | **None**. Users interact with a finished, pre-trained model; there is no access to the foundational training or model-building stages. | **No**. Customization is limited to prompt engineering or API-level fine-tuning of a pre-existing model. |
| **HuggingFace Transformers** | **Open**. The library and many of its models are open source under permissive licenses for broad use. | **High**. Training a full model from scratch typically requires significant cloud GPU resources and considerable expertise. | **Parts**. It provides components (models, datasets, tokenizers, trainers), but integrating them into a complete chat system requires significant development effort. | **Some**. Highly flexible for research, but navigating and modifying the extensive framework can be complex. |
| **Lit-GPT (from Lightning AI)** | **Open**. It is designed for transparency and hackability, offering minimal, readable implementations, often MIT licensed. | **Moderate**. While more accessible than large-scale corporate training, achieving full training on a personal budget often exceeds $100. | **Parts**. It focuses heavily on core model architecture and pretraining, often requiring additional setup for chat UIs, full evaluation, and finetuning integration. | **Good**. It is built for education and experimentation, providing clear code that is relatively easy to modify. |

## Hiding in the code

### Sandboxed Python Tool Execution
_nanochat/execution.py, nanochat/engine.py_

The product is betting on agentic LLMs that can use external tools to verify their own reasoning and solve complex problems, moving beyond just text generation. This feature is crucial for advanced reasoning tasks and agents.

### Custom Tuned BPE Tokenizer
_nanochat/tokenizer.py, scripts/tok_train.py_

Optimizing tokenization for specific model sizes and datasets is a key lever for efficiency and performance, suggesting a deep commitment to squeezing performance out of smaller models, even going beyond standard models like GPT-4's tokenization split pattern.

### Hybrid Muon/AdamW Optimizer
_nanochat/optim.py, scripts/base_train.py_

Custom, bleeding-edge optimization strategies are crucial for pushing the boundaries of micro-model training efficiency. This hybrid approach enables competitive results on commodity hardware by selectively applying different optimization techniques to different parameter groups.

### Best-Fit Data Packing for Training
_nanochat/dataloader.py_

Training efficiency is paramount; optimizing data loading to minimize padding and maximize full document context for every token is a critical, unglamorous detail. This significantly impacts compute time and model quality by increasing GPU utilization and providing richer training signals.

### Adaptive Residual Scaling
_nanochat/gpt.py_

Small, learnable architectural components, like per-layer `resid_lambdas` and `x0_lambdas`, can provide significant performance gains. This gives the model more control over information flow and shortcut connections, indicating a focus on fine-grained architectural optimization for better convergence.

### Dynamic Flash Attention 3 Integration
_nanochat/flash_attention.py_

Cutting-edge GPU-specific optimizations are necessary for competitive training speeds, but broad hardware compatibility through intelligent fallback is also a priority for accessibility. This ensures the best performance on modern hardware while remaining functional on older GPUs.

### Automated Training Report Generation
_nanochat/report.py, scripts/base_train.py_

Reproducibility and comprehensive logging are foundational to iterative LLM research and improvement. This built-in reporting system speaks to a scientific-first approach, enabling deep analysis of experimental results and changes.

## Missing on purpose

### No Multi-User Accounts
_nanochat/ui.html, scripts/chat_web.py (no authentication, user management, or user-specific data storage models or logic)_

Stays focused on a local, experimental harness for a single researcher or team. This avoids the significant complexity, security overhead, and privacy concerns associated with user management and data isolation in a multi-tenant environment.

### No Third-Party Plugin System
_Absence of plugin directories, manifest files, dynamic loading mechanisms, or an exposed API for external tool integration beyond the specific Python sandbox._

Prioritizes minimalism and control over the codebase. This sidesteps the security risks, maintenance burden, and compatibility challenges of a dynamic plugin ecosystem, keeping the core product lean and predictable.

### No Persistent Conversation History
_No database schema for storing past chats (e.g., no `Conversation` table), `chat_web.py` uses in-memory `messages` array, cleared on `newConversation()`._

Keeps the system stateless and focused on immediate interaction for research and demonstration. This avoids the storage, retrieval, privacy, and scalability complexities associated with managing large volumes of user dialogue history.

### No In-App Analytics Dashboard
_Absence of `/api/analytics` endpoints, database tables for usage metrics (e.g., `ChatLog`, `UserActivity`), or custom UI components for dashboards in `nanochat/ui.html`._

Leans on mature, specialized external tools like Weights & Biases (`wandb`) for detailed metric tracking. This avoids building and maintaining complex analytics infrastructure, keeping the project focused on LLM training and inference mechanics.

### No Multimedia Capabilities
_Absence of libraries for audio/video processing, no `VideoCall` or `AudioStream` components, no references to multimedia APIs like Daily.co or Zoom._

Stays laser-focused on core text-based LLM functionality. This avoids the significant complexity, data requirements, and computational overhead of multi-modal AI, which would drastically change the project's scope and resource demands.

### No Native Mobile App
_No iOS/Android project files, no mentions of mobile SDKs, mobile-specific UI/API considerations, or push notification services._

Prioritizes web accessibility and rapid iteration for a desktop/server-centric development workflow. This avoids the significant development, maintenance, and distribution overhead of native mobile applications, which cater to a different user base and require specialized skills.
