# OKF v0.2 — Guida all'Implementazione Computazionale: ONTO-PROBE (v0.3.1)

> This document translates the theoretical requirements into an implementation blueprint for low-spec and consumer hardware execution.

## 1. Objective

The implementation is designed for a dual path:

- white-box mode via Contrastive Activation Addition on open-weight models
- black-box mode via controlled semantic generation constraints

## 2. Execution model

### 2.1 White-box steering

The residual stream at an intermediate layer is modified with a directional vector extracted from positive/negative contrast pairs:

$$h^{(L)}_{steered} = h^{(L)} + \alpha \cdot v_{onto}, \quad \alpha \in [1.0, 2.0]$$

### 2.2 Black-box generation

A constrained prompt layer is used to prevent fallback to conventional physical or ontological templates.

## 3. Operational stack

- 4-bit quantized open-weight model (e.g., Llama-3.1-8B-Instruct)
- PyTorch hooks for residual-stream injection
- Dockerized formal verification backend (Z3 / ProVerif)
- optional vector store for archetype comparison
- HMAC-based blinding for reviewer separation

## 4. Safety gate

Before processing, the payload is checked against:

1. CBRN hazards
2. cyber-exploit patterns
3. cognitive manipulation vectors

If triggered, execution halts with `HALT_TRIGGERED`.

## 5. Example PyTorch pattern

```python
import torch

class LowVramOntologicalSteerer:
    def __init__(self, model, layer_idx=16):
        self.model = model
        self.layer_idx = layer_idx

    def attach_steering(self, strength, vec):
        target_layer = self.model.model.layers[self.layer_idx]

        def hook(module, args):
            hidden = args[0].clone()
            hidden[:, -1, :] = hidden[:, -1, :] + strength * vec
            return (hidden,) + args[1:]

        return target_layer.register_forward_pre_hook(hook)
```

## 6. Implementation notes

- keep the chat template aligned between contrast extraction and generation
- use `.clone()` before mutation in pre-hooks
- install `pyarrow` if Parquet export is used
- validate all outputs with consistent metrics for baseline comparison
