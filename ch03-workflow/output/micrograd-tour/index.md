# micrograd

_Lens: beginner-tutorial_

Micrograd is a lightweight automatic differentiation engine that builds a computational graph using scalar `Value` objects to enable reverse-mode backpropagation. On top of this engine, it provides a small library for constructing neural networks, including `Neuron`s, `Layer`s, and Multi-Layer Perceptrons (MLPs).


## Architecture

```mermaid
flowchart TD
    A0["Value"]
    A1["backward"]
    A2["Module"]
    A3["Neuron"]
    A4["Layer"]
    A5["MLP"]
    A0 -- "links to form computational gr" --> A0
    A0 -- "provides method" --> A1
    A1 -- "traverses computational graph " --> A0
    A3 -- "inherits from" --> A2
    A4 -- "inherits from" --> A2
    A5 -- "inherits from" --> A2
    A2 -- "manages parameters as" --> A0
    A3 -- "uses for internal state and ou" --> A0
    A4 -- "comprises multiple" --> A3
    A5 -- "comprises multiple" --> A4
```

## Chapters

- [Value](01_value.md)
- [backward](02_backward.md)
- [Module](03_module.md)
- [Neuron](04_neuron.md)
- [Layer](05_layer.md)
- [MLP](06_mlp.md)