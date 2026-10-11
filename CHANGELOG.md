# Changelog

All notable changes to this project are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow the
documentation/testbed versions used in the project (suite v0.3.1, CAA testbed v0.3.2).

## [Unreleased]

### Added
- `ROADMAP.md`: work done, planned work and pending owner actions.
- Community and repository files: `LICENSE` (Apache-2.0), `LICENSE-DOCS` (CC BY 4.0), `NOTICE`,
  `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CITATION.cff`, `CHANGELOG.md`,
  `AGENTS.md` / `CLAUDE.md` (guidance for LLM coding agents), issue and PR templates, CODEOWNERS,
  Dependabot config, CI workflow, `Makefile`, `.editorconfig`, `.gitattributes`,
  `requirements-whitebox.txt`.

## [0.3.2] - 2026-10-11

### Added
- GPU-free black-box pipeline (`code/run_blackbox.py`, `code/blackbox/`): conditions C1/C2/C3,
  blind LLM judges, HMAC blind IDs and hash-chain audit, ICC(2,k), bootstrap contrasts,
  resumable runs, cost estimate, offline mock client, 22 offline tests.
- The 30 Binary B tasks extracted from `BENCH-001` into `code/blackbox/data/tasks_b.json`
  (`tools/build_tasks.py`).
- Colab notebook `.ipynb` generated from the `.py` source (`tools/build_notebook.py`), reading
  `HF_TOKEN` from Colab Secrets and zipping results.
- White-box CAA smoke test now includes norm-matched random-vector controls, multiple seeds, a
  baseline noise floor and 7 success criteria.
- English `README.md` with Italian `README.it.md`; guide `docs/howto-blackbox.md`.

### Changed
- Restored the full original documents and scripts as the canonical `docs/` and `code/` files
  (the earlier condensed rewrites had dropped code, task specifications and procedures).
- `IMPL-001`: steerer aligned to v0.3.2; verifier on an internal Docker network with an
  `expected` (`sat`/`unsat`) outcome field.
- `EVAL-001`: ICC restricted to samples rated by all raters; referee form covers all five domains.
- `THEORY-001`: corrected confidence interval for 0/168, power analysis (N >= 159, planned 165-180).
- `BENCH-001`: threshold written as `Sim_max < tau` (provisional 0.60); unverifiable F1 claim removed.
- `META-001`: readiness reflects documentation completeness, not executed validation.
- Refactor notes moved to `archive/`.

### Fixed
- `howto.md`: removed the invalid `.py` to `.ipynb` rename instructions.
- Notebook dependency check now covers all required packages.

## [0.3.1]

- Documentation suite release (theory, implementation guide, benchmark, protocol, suite analysis).
  See `docs/` and `archive/` for history.
