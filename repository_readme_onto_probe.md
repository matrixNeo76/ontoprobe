# ONTO-PROBE

Research framework for probing the limits of ontological innovation in large language models.

**Status:** v0.3.1 (documentation) / v0.3.2 (CAA smoke testbed) — pre-execution.

---

## Overview

ONTO-PROBE investigates whether large language models can generate genuinely novel conceptual structures — new causal relations, predicates, and explanatory frameworks not reducible by interpolation or homomorphism to the training distribution — or whether they are structurally confined to a fixed conceptual closure.

The framework adopts a **falsificationist posture**: if the geometric closure of the transformer architecture is insurmountable, the protocol empirically measures the maximum divergence reachable before syntactic degeneration, documenting the operational limits of autoregressive neural networks.

Empirical literature on the subject (Matarmaa 2026, $N=168$ proposals across seven frontier models) reports a strict ontological novelty rate of $\hat{p} = 0.000$ ($95\%$ CI: $[0.000, 0.000]$), with $98.2\%$ of outputs traceable to pre-existing frameworks.

---

## Repository structure

```
onto-probe/
├── README.md                       # this file
├── LICENSE                         # CC BY 4.0 (docs) + Apache 2.0 (code)
├── docs/
│   ├── THEORY-001.md               # Research framework and epistemology
│   ├── IMPL-001.md                 # Computational implementation guide
│   ├── BENCH-001.md                # Benchmark O-Novel: task catalog
│   ├── EVAL-001.md                 # Experimental protocol and evaluation runbook
│   ├── META-001.md                 # Suite analysis, readiness matrix, glossary
│   └── howto.md                    # Step-by-step execution guide
├── code/
│   ├── notebook_caa_smoke_test_v0_3_2.py      # CAA smoke test (PyTorch)
│   └── inspect_smoke_test_outputs.py          # Qualitative inspection CLI
└── outputs/                        # Empirical results (populated after execution)
```

---

## Documentation

| Document | Role |
|---|---|
| **THEORY-001** | Theoretical framework, the *No New Basis Principle*, the *double-binary* validation architecture, and the ontological novelty metric. |
| **IMPL-001** | Computational implementation: 4-bit Contrastive Activation Addition on residual stream, Docker sandboxing for formal verifiers, HMAC-blinding protocol, and cost profile for consumer hardware. |
| **BENCH-001** | Benchmark **O-Novel v0.1**: 50 open problems across 5 domains, split into 20 formally verifiable tasks (Z3, ProVerif) and 30 open-domain tasks with semantic taboos. |
| **EVAL-001** | Experimental protocol: double-blind evaluation with HMAC-separated blind IDs, multi-LLM judge template, human referee rubric, and Python statistical harness (ICC, ANOVA). |
| **META-001** | Suite-level analysis: readiness matrix, gap tracking, and operational glossary. |
| **howto.md** | Operational guide for executing the first empirical smoke test on Google Colab (T4 GPU). |

---

## Code

### `notebook_caa_smoke_test_v0_3_2.py`

Collaudo of the **LowVramOntologicalSteerer** class. Extracts three ontological steering vectors via Contrastive Activation Addition on `meta-llama/Llama-3.1-8B-Instruct`, applies them across a grid of $\alpha \in [0.0, 3.0]$, and evaluates four success criteria:

1. Vector extraction without crash or NaN (chat template assistant-aligned)
2. Grammatical and coherent generation for $\alpha \in [1.0, 2.0]$ (with `.clone()` tensor isolation)
3. Monotonic dose-response between $\alpha$ and structural distance from baseline
4. Qualitative distinction between ontological axes

Runtime: ~30 minutes on Colab T4. Zero local installation required.

### `inspect_smoke_test_outputs.py`

Command-line tool for qualitative inspection of the smoke test outputs. Produces:

- Dose-response progression per ontological axis
- Cross-axis comparison at a fixed $\alpha$
- Vocabulary divergence extraction (with Italian stopword filtering)
- Markdown export for archival

---

## Quick start

```bash
# 1. Read the operational guide
cat docs/howto.md

# 2. Execute the smoke test on Colab (T4 GPU)
# Follow Passi 1–7 of howto.md

# 3. Inspect the results
python code/inspect_smoke_test_outputs.py --alpha 1.5
```

---

## Scope

**This repository does not claim** that LLMs can or cannot achieve genuine ontological innovation. It provides:

- A theoretical framework for operationalizing the question
- A reproducible benchmark for empirical testing
- A low-cost testbed (consumer GPU or API-only) for running the experiment
- A rigorous evaluation protocol with blinding and inter-rater reliability metrics

An informative negative result — empirical validation of the *No New Basis Principle* — constitutes a publication-grade contribution in itself.

---

## License

- **Documentation** (`docs/`): CC BY 4.0
- **Code** (`code/`): Apache 2.0

See `LICENSE` for details.

---

## Citation

If you reference this framework, please cite the ONTO-PROBE research suite (v0.3.1).

```bibtex
@misc{ontoprobe2026,
  title  = {ONTO-PROBE: A Research Framework for Probing the Limits of Ontological Innovation in LLMs},
  year   = {2026},
  note   = {Version 0.3.1},
  url    = {https://github.com/[your-username]/onto-probe}
}
```

---

## Contact

For questions, issues, or collaboration proposals, open an issue in this repository.