# ONTO-PROBE

Research framework for probing the limits of ontological innovation in large language models.

Status: v0.3.1 (documentation) / v0.3.2 (CAA smoke testbed) — pre-execution.

## Overview

ONTO-PROBE investigates whether large language models can generate genuinely novel conceptual structures — new causal relations, predicates, and explanatory frameworks not reducible by interpolation or by mere recombination of known archetypes.

The framework adopts a falsificationist posture: if the geometric closure of the transformer architecture is insurmountable, the protocol empirically measures the maximum divergence reachable under constrained generation.

## Repository structure

```text
onto-probe/
├── README.md                       # project overview
├── LICENSE                         # license terms
├── docs/
│   ├── THEORY-001.md              # research framework and epistemology
│   ├── IMPL-001.md                # implementation guide
│   ├── BENCH-001.md               # benchmark task catalog
│   ├── EVAL-001.md                # experimental protocol
│   ├── META-001.md                # suite analysis and readiness matrix
│   └── howto.md                   # execution guide
├── code/
│   ├── notebook_caa_smoke_test_v0_3_2.py  # CAA smoke test (PyTorch)
│   └── inspect_smoke_test_outputs.py      # qualitative inspection CLI
├── outputs/
│   └── .gitkeep                   # generated results directory
├── archive/                       # legacy or review-only material
└── .gitignore                     # optional local ignores
```

## Documentation

| Document | Role |
|---|---|
| THEORY-001 | Theoretical framework, the No New Basis Principle, and the ontological novelty metric |
| IMPL-001 | Computational implementation and low-spec architecture |
| BENCH-001 | Benchmark O-Novel task catalog |
| EVAL-001 | Experimental protocol and evaluation runbook |
| META-001 | Suite assessment, readiness matrix, and glossary |
| howto.md | Operational guide for the first empirical smoke test |

## Code

### notebook_caa_smoke_test_v0_3_2.py

Smoke test for the LowVramOntologicalSteerer class. It extracts three ontological steering vectors via Contrastive Activation Addition on meta-llama/Llama-3.1-8B-Instruct, applies them across a generation grid, and produces quantitative diagnostics.

### inspect_smoke_test_outputs.py

Command-line tool for qualitative inspection of smoke-test outputs. Produces dose-response views by ontological axis and Markdown exports.

## Quick start

```bash
# 1. Read the operational guide
cat docs/howto.md

# 2. Execute the smoke test on Colab (T4 GPU)
# Follow steps 1–8 of docs/howto.md

# 3. Inspect results
python code/inspect_smoke_test_outputs.py --alpha 1.5
```

## Scope

This repository does not claim that LLMs can or cannot achieve genuine ontological innovation. It provides:

- a theoretical framework for operationalizing the question
- a reproducible benchmark for empirical testing
- a low-cost testbed for execution in consumer GPU environments
- a rigorous evaluation protocol with blinding and inter-rater reliability metrics

## License

- Documentation (`docs/`): CC BY 4.0
- Code (`code/`): Apache 2.0

See `LICENSE` for details.
