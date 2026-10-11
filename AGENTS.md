# AGENTS.md — guidance for LLM coding agents

This file tells AI coding agents (Claude Code, Codex, Cursor, Copilot, etc.) how to work in this repository.
Humans should read [`README.md`](README.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## What this project is

ONTO-PROBE is a **research protocol** testing whether LLMs can generate genuinely novel conceptual structures or only recombine known archetypes. **No real experiment has been run yet; there are no results.** Never write text that implies otherwise.

Two execution paths:
- **Black-box (no GPU)**: `code/run_blackbox.py` + `code/blackbox/` — generates solutions under three conditions via an OpenAI-compatible API and scores them with blind LLM judges. Python standard library only.
- **White-box CAA (GPU)**: `code/notebook_caa_smoke_test_v0_3_2.py` (→ generated `.ipynb`) — Contrastive Activation Addition smoke test on Llama-3.1-8B-Instruct. Needs an NVIDIA GPU; do not try to run it in a CPU sandbox.

## Commands

```bash
make test        # offline unit tests (python -m unittest discover -s code/tests)
make build       # regenerate the .ipynb and tasks_b.json from their sources
make check       # test + fail if generated files are stale (this is what CI does)
make mock        # offline dry run of the black-box pipeline (random numbers)
make estimate    # estimate calls/cost of the pilot
```

All tests are offline and need no network, API key or GPU. Run `make check` before declaring work done.

## Repository map

```text
docs/        theory & protocol (Italian, OKF v0.2 front matter): THEORY-001, IMPL-001, BENCH-001, EVAL-001, META-001, howto*.md
code/        run_blackbox.py, blackbox/ (client, conditions, judges, stats, audit, pipeline), tests/, CAA notebook + inspector
tools/       build_notebook.py, build_tasks.py (generators)
outputs/     generated results (git-ignored; never commit)
archive/     historical material; do not link to it from canonical docs
```

## Source-of-truth rules (important)

- `code/notebook_caa_smoke_test_v0_3_2.ipynb` is **generated** from the `.py` file. Edit the `.py`, then `make build`.
- `code/blackbox/data/tasks_b.json` is **generated** from `docs/BENCH-001.md`. Edit the document, then `make build`.
- `docs/IMPL-001.md` §3.3 mirrors the steerer class in the notebook `.py`; keep them in sync.
- Thresholds (ICC ≥ 0.60, appropriateness ≥ 2.5, τ, power parameters) appear in several documents and in `code/blackbox/stats.py`; change them together or not at all.

## Research-integrity rules (do not violate)

1. **Never tune thresholds, prompts, rubrics or task wording to improve an outcome.** Changes must be justified independently of observed results and flagged in the PR.
2. **Never present `--mock` output as results.** Mock runs are random; `report.md` carries a banner for them.
3. **Do not invent data, numbers or citations.** If a figure cannot be verified (e.g. Matarmaa 2026, the F1 of the τ calibration), say it is unverified.
4. **Keep claims scoped**: the pipeline measures novelty *as perceived by LLM judges*, not demonstrated ontological novelty.
5. Report null or negative results with the same prominence as positive ones.

## Safety and cost rules

- **Do not call paid APIs without explicit user consent.** Use `--mock` for development and `estimate` before any real run.
- **Never commit or print secrets**: `ONTO_API_KEY`, `HF_TOKEN`, `.hmac_key`, `ONTO_HMAC_KEY`, anything under `outputs/`.
- Do not weaken blinding: judges must receive only the problem, taboo list and candidate text — never condition labels, agent roles or model names.
- The formal verifier is designed to run network-isolated; do not expose it or give it egress.

## Conventions

- Python 3.9+ compatible; standard library only in `code/blackbox/`. Do not add runtime dependencies without discussing it.
- Docs in `docs/` are in Italian; `README.md` is English (Italian in `README.it.md`); code, comments and repo-meta files are English unless they follow an existing Italian file.
- Keep comments sparse and match the surrounding style. Prefer small, focused changes.
- Commit messages: short imperative summary, then the *why*.
- Branch from `main` and open a pull request; do not push to `main` directly. Fill in `.github/PULL_REQUEST_TEMPLATE.md`.

## Known open issues (good first targets)

- No archetype database (2,000 entries) and τ is provisional — `Sim_max` is not used by the black-box report.
- Binary A tasks (20 formal tasks, Z3/ProVerif) are not in the black-box pipeline.
- Original empirical premises (Matarmaa 2026) are unverified against the source.
- White-box CAA notebook and the real-API black-box path have never been executed end to end.
