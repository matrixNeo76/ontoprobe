# Security Policy

## Supported versions

Only the latest state of the `main` branch is supported.

## Reporting a vulnerability

Please **do not open a public issue** for security problems. Use GitHub's private vulnerability reporting:
[Report a vulnerability](https://github.com/matrixNeo76/ontoprobe/security/advisories/new).

Include what you found, how to reproduce it, and its impact. You can expect an acknowledgement, and a fix or a clear explanation if the report is out of scope. This is an individual research project, so response times are best-effort.

## What is in scope

- Leakage or unsafe handling of credentials: `ONTO_API_KEY`, the HMAC blinding key (`.hmac_key` / `ONTO_HMAC_KEY`), HuggingFace tokens.
- Weaknesses that break the integrity of the blind evaluation (e.g. de-anonymisation of dossiers through the audit chain or file layout).
- Unsafe execution in the formal-verification sandbox described in `docs/IMPL-001.md` (Docker network isolation, capabilities, resource limits).
- Code injection or path traversal in the scripts under `code/` and `tools/`.

Out of scope: scientific disagreements about the protocol (open a *Protocol or methodology question* issue instead), and the behaviour of third-party APIs or models.

## Notes for users

- Never commit API keys. `.env`, `.hmac_key` and `outputs/` are git-ignored; keep it that way.
- For a real double-blind study, keep the HMAC key **outside** any folder shared with human referees (see `docs/howto-blackbox.md`).
- API runs cost money. Use `estimate` first and set spending limits with your provider.
- The Binary A verifier is designed to run in an isolated container with no network egress. Do not expose it publicly.
