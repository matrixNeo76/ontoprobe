# Legacy File Mapping

This document tracks the correspondence between old filenames (from main branch) and canonical names in the reorganized structure.

## Mapping

| Legacy File (main branch) | Canonical Name (reorg branch) | Category |
|---|---|---|
| `research_framework_onto_probe_v0_3_0.md` | `docs/THEORY-001.md` | Core documentation |
| `guida_all_implementazione_computazionale_onto_probe.md` | `docs/IMPL-001.md` | Core documentation |
| `catalogo_dei_task_e_specifiche_del_benchmark_o_novel.md` | `docs/BENCH-001.md` | Core documentation |
| `protocollo_sperimentale_e_human_evaluation_runbook.md` | `docs/EVAL-001.md` | Core documentation |
| `analisi_della_suite_documentale_onto_probe.md` | `docs/META-001.md` | Core documentation |
| `guida_operativa_collaudo_caa.md` | `docs/howto.md` | Execution guide |
| `notebook/notebook_caa_smoke_test_v0_3_2.py` | `code/notebook_caa_smoke_test_v0_3_2.py` | Code |
| `notebook/script_di_ispezione_qualitativa_e_comparatore_caa.py` | `code/inspect_smoke_test_outputs.py` | Code |
| `notebook/revisione_tecnica_e_patch_del_notebook_caa_smoke_test.md` | `archive/IMPLEMENTATION-NOTES.md` | Historical review |
| `dossier_di_validazione_finale_e_audit_operativo.md` | `archive/VALIDATION-AUDIT.md` | Historical review |

## Content note

The canonical files in `docs/` and `code/` are the full original documents and scripts, renamed. A first reorganization had replaced them with condensed rewrites that dropped code, task specs and procedures; those rewrites were discarded.

## Rationale

- **Canonical names**: Short, uniform prefixes (THEORY, IMPL, BENCH, EVAL, META) following OKF v0.2 standard
- **Clear structure**: `docs/` for official, `code/` for executable, `archive/` for historical
- **Reduced clutter**: Eliminates long descriptive filenames from root and nested directories

## Migration Strategy

1. All references in `README.md` point to new canonical locations
2. Cross-document references updated to reflect new paths
3. Legacy files archived for audit trail
4. Single PR/merge to consolidate structure
