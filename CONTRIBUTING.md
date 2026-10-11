# Contributing to ONTO-PROBE

Thanks for your interest. ONTO-PROBE is a research protocol first and a code base second, so the most valuable contributions are often **scrutiny of the method** rather than new features. Both are welcome.

Please read the [Code of Conduct](CODE_OF_CONDUCT.md) first. Documentation guides and theory documents are written in Italian; issues and pull requests may be in English or Italian.

## Ways to contribute

- **Challenge the methodology**: inconsistencies, unsupported numbers, flawed metrics or thresholds. Use the *Protocol or methodology question* issue template and quote the passage.
- **Report bugs** in the black-box pipeline, notebook or tooling (*Bug report* template).
- **Run the experiments** and share the `report.md` of your runs (remove anything sensitive first). Null results are valuable.
- **Improve documentation**, including translations of the guides in `docs/`.
- **Propose features** (*Feature request* template).

## Development setup

Python 3.9+ is enough; the black-box pipeline and its tests use only the standard library.

```bash
git clone https://github.com/matrixNeo76/ontoprobe.git
cd ontoprobe
make test        # offline unit tests
make mock        # offline dry run of the whole black-box pipeline (random numbers)
```

The white-box notebook needs a GPU and extra packages (`requirements-whitebox.txt`); you do not need them to contribute to the rest.

## Single sources of truth

Two files are **generated**; edit the source, never the artifact:

| Generated file | Source | Regenerate with |
|---|---|---|
| `code/notebook_caa_smoke_test_v0_3_2.ipynb` | `code/notebook_caa_smoke_test_v0_3_2.py` | `make build` |
| `code/blackbox/data/tasks_b.json` | `docs/BENCH-001.md` | `make build` |

CI fails if these are stale. Run `make check` before pushing.

## Research-integrity rules

These matter more than style:

1. **Do not tune thresholds, prompts, rubrics or task wording after looking at results.** If a change is needed, state the reason in the PR and make it independently of any observed outcome. Anything that could influence results is flagged in the PR template.
2. **Never present simulated (`--mock`) numbers as results.** Mock runs are random by design.
3. **Do not overstate.** The pipeline measures novelty *as perceived by LLM judges*, not demonstrated ontological novelty. Keep claims in docs consistent with that.
4. **Report null and negative results** in the same way as positive ones.
5. **No fabricated data or citations.** If a number or source cannot be verified, say so in the text.

## Pull requests

1. Branch from `main`; keep each PR focused.
2. Run `make check` (tests and generated-file check).
3. Never commit secrets, API keys, `.hmac_key` or anything under `outputs/`.
4. Update the relevant document and `CHANGELOG.md` when behaviour or protocol changes.
5. Fill in the PR template. CI must be green.

Commit messages: a short imperative summary line, then a body explaining *why* when it is not obvious.

## Licensing of contributions

By contributing you agree that your code contributions are licensed under Apache-2.0 and your documentation contributions under CC BY 4.0, matching the project (see `LICENSE` and `LICENSE-DOCS`).
