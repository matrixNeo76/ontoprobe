# ONTO-PROBE

🌐 **English** · [Italiano](README.it.md)

A research project built around one question: **can a large language model (LLM) invent genuinely new ideas, or does it only recombine what it has already seen during training?**

"New ideas" here means new causal relations, new predicates and new explanatory structures that are not mere interpolations or recombinations of known models (the *archetypes*).

> **Status: pre-execution.** Documentation and code are complete and tested offline, but **no real experiment has been run yet**, so there are no results. Today this repository is a ready-to-run protocol, not a confirmation of any hypothesis.

## The idea in brief

The project starts from a hypothesis to test, not a thesis to defend. The hypothesis is the *No New Basis Principle*: a model trained on a fixed vocabulary cannot generate conceptual dimensions that are truly orthogonal to those of its corpus. If it holds, the experiment will show it by measuring how far divergence can be pushed before the output turns incoherent. If it does not, valid solutions far from the archetypes will emerge. Either outcome is informative.

To measure this, the project combines:

- **a 50-problem benchmark** (O-Novel): 20 with an answer a program can verify (Z3, ProVerif) and 30 open-ended, with bans on the obvious solutions (*semantic taboos*);
- **three conditions compared**: a single agent, several agents sharing memory, and the ONTO-PROBE pipeline with isolated agents and generation constraints;
- **blind evaluation**: heterogeneous LLM judges and, where they disagree, human referees, with masked identifiers (HMAC) and an audit chain;
- **statistical controls**: inter-judge agreement (ICC), confidence intervals, and a check that the effect exceeds noise.

## Two ways to run it

| | **Black-box via API** | **White-box CAA** |
|---|---|---|
| What it does | Asks commercial models for solutions and has other models score them blind | Reaches into Llama-3.1-8B's activations and shifts them along ontological axes (*Contrastive Activation Addition*) |
| Hardware | None: Python and an API key are enough | NVIDIA GPU with at least 8 GB (e.g. free Colab T4) |
| Cost | A few cents for the pilot (estimate, check real prices) | Free on Colab, about 45 minutes |
| Status | Full pipeline, tested offline; never run against a real API | Notebook ready; never run |
| Guide | [`docs/howto-blackbox.md`](docs/howto-blackbox.md) | [`docs/howto.md`](docs/howto.md) |

**If you have no GPU, start with black-box.** The white-box smoke test is a preliminary check on the steering technique, not a prerequisite for the rest.

The guides in `docs/` are written in Italian.

## Getting started

### Without a GPU (black-box)

```bash
# 1. Dry run: offline, free; numbers are random but it checks that everything runs
python code/run_blackbox.py all --run-id prova --limit 6 --mock

# 2. Estimate calls and cost
python code/run_blackbox.py estimate --limit 6

# 3. Real pilot (needs an API key, see the guide)
export ONTO_API_KEY="your-key"
python code/run_blackbox.py all --run-id pilot --limit 6
```

The result is `outputs/blackbox/pilot/report.md`. Requirements: Python 3.9+, no libraries to install.

### With a GPU (white-box)

Open the notebook in Colab and choose "Runtime → Run all":
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/matrixNeo76/ontoprobe/blob/main/code/notebook_caa_smoke_test_v0_3_2.ipynb)

You need a HuggingFace account with access to Llama-3.1-8B-Instruct and the token saved in Colab Secrets (`HF_TOKEN`). All steps are in [`docs/howto.md`](docs/howto.md).

### Tests

```bash
python -m unittest discover -s code/tests
```

22 tests, all offline.

## What's inside

```text
├── docs/            project documentation (see table below)
├── code/
│   ├── run_blackbox.py                       black-box experiment entry point
│   ├── blackbox/                             conditions, judges, statistics, audit
│   ├── notebook_caa_smoke_test_v0_3_2.ipynb  CAA smoke test for Colab (generated)
│   ├── notebook_caa_smoke_test_v0_3_2.py     notebook source
│   ├── inspect_smoke_test_outputs.py         qualitative inspection of CAA results
│   └── tests/                                offline tests
├── tools/           generators: .ipynb notebook and task list
├── outputs/         generated results (git-ignored)
└── archive/         historical material and review notes
```

| Document | Purpose |
|---|---|
| [`THEORY-001`](docs/THEORY-001.md) | Theoretical framework, definition of ontological novelty, methodology, risks |
| [`IMPL-001`](docs/IMPL-001.md) | Technical architecture and reference code |
| [`BENCH-001`](docs/BENCH-001.md) | Catalog of the 50 tasks and benchmark specifications |
| [`EVAL-001`](docs/EVAL-001.md) | Experimental protocol, judge rubrics, human referee form, statistics |
| [`META-001`](docs/META-001.md) | Suite assessment, glossary, roadmap |
| [`howto-blackbox.md`](docs/howto-blackbox.md) | Step-by-step guide to the API path |
| [`howto.md`](docs/howto.md) | Step-by-step guide to the CAA smoke test on Colab |

The theory documents are in Italian and follow the OKF v0.2 format.

## Known limitations

- **It measures novelty as perceived by LLM judges**, not demonstrated ontological novelty. A positive result must be confirmed with human referees.
- **Black-box does no internal steering**: the syntactic seed is a surrogate for what CAA would do on the activations.
- **The archetype distance is missing**: the 2,000-entry database has not been built and the threshold τ is provisional.
- **The 20 formal tasks (Track A)** are not yet part of the black-box path.
- **Few tasks, wide intervals**: the 6-task pilot checks the pipeline and estimates noise; it is not enough to draw conclusions.
- **Premises to verify**: the starting empirical data (Matarmaa 2026) has not been checked against the source.

## Roadmap

What is done, what is next, and the actions pending for the owner: [`ROADMAP.md`](ROADMAP.md) (in Italian).

## Contributing and citing

See [`CONTRIBUTING.md`](CONTRIBUTING.md), the [Code of Conduct](CODE_OF_CONDUCT.md) and [`SECURITY.md`](SECURITY.md). To cite the project use [`CITATION.cff`](CITATION.cff) (GitHub shows a "Cite this repository" button). Guidance for LLM coding agents is in [`AGENTS.md`](AGENTS.md).

## What this repository does not claim

It does not claim that LLMs can or cannot achieve genuine ontological innovation. It provides a way to pose the question in a verifiable form.

## License

- Documentation (`docs/`): CC BY 4.0
- Code (`code/`): Apache 2.0

Full texts: [`LICENSE`](LICENSE) (Apache-2.0) and [`LICENSE-DOCS`](LICENSE-DOCS) (CC BY 4.0).
