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
│   ├── howto.md                   # execution guide (white-box CAA, GPU)
│   └── howto-blackbox.md          # execution guide (black-box API, no GPU)
├── code/
│   ├── notebook_caa_smoke_test_v0_3_2.ipynb  # CAA smoke test per Colab (generato)
│   ├── notebook_caa_smoke_test_v0_3_2.py     # sorgente del notebook (PyTorch)
│   ├── inspect_smoke_test_outputs.py      # qualitative inspection CLI
│   ├── run_blackbox.py                    # black-box experiment via API (no GPU)
│   ├── blackbox/                          # conditions, judges, stats, audit
│   └── tests/                             # offline tests
├── tools/                         # generators (notebook, task list)
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

### notebook_caa_smoke_test_v0_3_2.ipynb

Colab notebook (generated from `notebook_caa_smoke_test_v0_3_2.py` with `python tools/build_notebook.py`). Smoke test for the LowVramOntologicalSteerer class. It extracts three ontological steering vectors via Contrastive Activation Addition on meta-llama/Llama-3.1-8B-Instruct, applies them across a generation grid with multiple seeds, compares each axis against a norm-matched random-vector control and the baseline sampling noise, and produces quantitative diagnostics.

[Open in Colab](https://colab.research.google.com/github/matrixNeo76/ontoprobe/blob/main/code/notebook_caa_smoke_test_v0_3_2.ipynb)

### inspect_smoke_test_outputs.py

Command-line tool for qualitative inspection of smoke-test outputs. Produces dose-response views by ontological axis and Markdown exports.

### run_blackbox.py

GPU-free experiment on the Binary B tasks (30 open-domain problems). Generates solutions under three conditions (single agent, shared-memory multi-agent, ONTO-PROBE isolated pipeline) via an OpenAI-compatible API, has three heterogeneous LLM judges score them blind, and reports condition contrasts with bootstrap confidence intervals and inter-judge ICC. See `docs/howto-blackbox.md`.

## Quick start

```bash
# 1a. No GPU: black-box via API (see docs/howto-blackbox.md)
python code/run_blackbox.py all --run-id prova --limit 6 --mock   # offline dry run

# 1b. With a GPU: read the white-box CAA guide
cat docs/howto.md

# 2. Open the notebook in Colab (T4 GPU) and run all cells
# Follow steps 1–8 of docs/howto.md

# 3. Re-inspect downloaded results locally
python code/inspect_smoke_test_outputs.py --input path/to/results_with_metrics.csv --alpha 1.5
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
