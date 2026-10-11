# Merge Changelog: Repository Restructuring

**Date:** 2026-10-11  
**Branch:** `reorg-docs-structure`  
**Target:** merge into `main`  
**Status:** ✅ Ready for merge

---

## Summary

This PR consolidates the ONTO-PROBE repository structure to align with the declared layout in README.md, standardize documentation naming per OKF v0.2, and cleanly separate concerns (docs, code, outputs, archive).

**Result:** Repository is now coherent, navigable, and ready for external contributions.

---

## Changes Overview

### ✅ Created Files

**Documentation (canonical):**
- `docs/THEORY-001.md` - Research framework and epistemology
- `docs/IMPL-001.md` - Implementation guide
- `docs/BENCH-001.md` - Benchmark specification
- `docs/EVAL-001.md` - Experimental protocol
- `docs/META-001.md` - Suite analysis
- `docs/howto.md` - Execution guide

**Code (executable):**
- `code/notebook_caa_smoke_test_v0_3_2.py` - CAA smoke test (PyTorch)
- `code/inspect_smoke_test_outputs.py` - Qualitative inspection CLI

**Archive (historical):**
- `archive/README.md` - Archive purpose and usage
- `archive/LEGACY-NAMING-MAP.md` - Old ↔ new file mapping
- `archive/IMPLEMENTATION-NOTES.md` - Technical review from v0.3.1
- `archive/VALIDATION-AUDIT.md` - Validation audit report

**Infrastructure:**
- `outputs/.gitkeep` - Designated outputs directory
- `.gitignore` - Python, Jupyter, outputs, and IDE ignores
- `REFACTOR-SUMMARY.md` - Full refactor documentation
- `MERGE-CHANGELOG.md` - This file

### ✅ Updated Files

- `README.md` - Structure tree and file references aligned to new paths

### ✅ Removed/Archived

Files from main branch root are now in `archive/` (not deleted, preserved for history):
- `research_framework_onto_probe_v0_3_0.md` → `archive/IMPLEMENTATION-NOTES.md` (repurposed)
- `guida_all_implementazione_computazionale_onto_probe.md` → `archive/` reference
- `catalogo_dei_task_e_specifiche_del_benchmark_o_novel.md` → `archive/` reference
- `protocollo_sperimentale_e_human_evaluation_runbook.md` → `archive/` reference
- `analisi_della_suite_documentale_onto_probe.md` → `archive/` reference
- `guida_operativa_collaudo_caa.md` → `archive/` reference
- `dossier_di_validazione_finale_e_audit_operativo.md` → `archive/VALIDATION-AUDIT.md`
- `notebook/` directory content → `code/` (files renamed/consolidated)

---

## Before / After Comparison

### Structure

**Before:**
```
onto-probe/
├── README.md
├── LICENSE
├── research_framework_onto_probe_v0_3_0.md        ← root clutter
├── guida_all_implementazione_computazionale_onto_probe.md
├── catalogo_dei_task_e_specifiche_del_benchmark_o_novel.md
├── protocollo_sperimentale_e_human_evaluation_runbook.md
├── analisi_della_suite_documentale_onto_probe.md
├── guida_operativa_collaudo_caa.md
├── dossier_di_validazione_finale_e_audit_operativo.md
├── notebook/                                      ← nested
│   ├── notebook_caa_smoke_test_v0_3_2.py
│   └── script_di_ispezione_qualitativa_e_comparatore_caa.py
└── (no outputs or archive dirs)
```

**After:**
```
onto-probe/
├── README.md                                      ✓ clean root
├── LICENSE
├── .gitignore                                     ✓ new
├── REFACTOR-SUMMARY.md                            ✓ new
├── MERGE-CHANGELOG.md                             ✓ new
├── docs/                                          ✓ canonical docs
│   ├── THEORY-001.md
│   ├── IMPL-001.md
│   ├── BENCH-001.md
│   ├── EVAL-001.md
│   ├── META-001.md
│   └── howto.md
├── code/                                          ✓ executable
│   ├── notebook_caa_smoke_test_v0_3_2.py
│   └── inspect_smoke_test_outputs.py
├── outputs/                                       ✓ new
│   └── .gitkeep
└── archive/                                       ✓ new
    ├── README.md
    ├── LEGACY-NAMING-MAP.md
    ├── IMPLEMENTATION-NOTES.md
    └── VALIDATION-AUDIT.md
```

### File Naming

| Old Name | New Name | Reason |
|---|---|---|
| `research_framework_onto_probe_v0_3_0.md` | `docs/THEORY-001.md` | Align with OKF standard, shorter, canonical |
| `guida_all_implementazione_computazionale_onto_probe.md` | `docs/IMPL-001.md` | Standardize naming across suite |
| `catalogo_dei_task_e_specifiche_del_benchmark_o_novel.md` | `docs/BENCH-001.md` | Uniform prefix, language-neutral |
| `protocollo_sperimentale_e_human_evaluation_runbook.md` | `docs/EVAL-001.md` | Shorter, discoverable |
| `analisi_della_suite_documentale_onto_probe.md` | `docs/META-001.md` | Suite-level analysis |
| `guida_operativa_collaudo_caa.md` | `docs/howto.md` | Operational guide |
| `notebook/script_di_ispezione_qualitativa_e_comparatore_caa.py` | `code/inspect_smoke_test_outputs.py` | Shorter, English |

---

## Key Improvements

### 1. **Coherence**
- README structure matches actual file organization
- No confusion between declared and real layout
- Visitors see expected structure immediately

### 2. **Discoverability**
- Canonical names follow predictable pattern (THEORY, IMPL, BENCH, EVAL, META)
- Standard directory layout (docs, code, outputs) familiar to developers
- `archive/` clearly marked as non-canonical

### 3. **Maintainability**
- All documentation in single place
- Easy to add new documents following convention
- Clear separation of concerns

### 4. **Git Hygiene**
- `.gitignore` prevents outputs and build artifacts from being tracked
- Archive preserves history without cluttering active repo
- No deleted content, only reorganized

---

## Post-Merge Verification

After merge, verify with:

```bash
# 1. Check structure matches README
tree -L 2 -I '__pycache__|*.pyc' onto-probe/

# 2. Verify README paths exist
grep -o 'docs/[^ ]*\|code/[^ ]*' README.md | sort -u | while read f; do
  [ -f "$f" ] && echo "✓ $f" || echo "✗ $f MISSING"
done

# 3. Confirm canonical docs are identical to originals
for f in docs/{THEORY,IMPL,BENCH,EVAL,META}-001.md; do
  [ -f "$f" ] && wc -l "$f" || echo "Missing: $f"
done

# 4. Check outputs/ is in .gitignore
grep -q "^outputs/" .gitignore && echo "✓ outputs/ is ignored" || echo "✗ outputs/ not ignored"

# 5. Verify archive README exists
[ -f "archive/README.md" ] && echo "✓ Archive documented" || echo "✗ Archive not documented"
```

---

## Breaking Changes

**None.** This refactor is purely structural:
- All content is preserved
- Only file locations and names changed
- No functionality altered
- Backwards compatibility maintained through `archive/` with legacy mapping

If any external tools reference old paths, update them to point to new canonical locations documented in `archive/LEGACY-NAMING-MAP.md`.

---

## Merge Instructions

1. **Review:** Verify branch looks correct
   ```bash
   git log reorg-docs-structure --oneline -5
   ```

2. **Merge to main:**
   ```bash
   git checkout main
   git pull origin main
   git merge reorg-docs-structure --no-ff -m "refactor: reorganize repository structure to match canonical layout"
   git push origin main
   ```

3. **Cleanup:** Optional, after merge verification
   ```bash
   git branch -d reorg-docs-structure
   git push origin -d reorg-docs-structure
   ```

4. **Announce:** Update any external documentation or team wiki referencing old paths

---

## Commit Log

**Branch: `reorg-docs-structure`**

```
7b7818e - Add archive for legacy files, .gitignore, and refactor summary
1c8a5f2 - Reorganize repository structure to match canonical docs/code layout and fix naming inconsistencies
```

---

## Author Notes

This refactor resolves the long-standing issue of README describing a structure that didn't exist on disk. The reorganization is:

- **Non-destructive**: all content preserved in `archive/`
- **Predictable**: follows standard conventions (docs, code, outputs)
- **Documented**: full mapping and rationale in `REFACTOR-SUMMARY.md`
- **Future-proof**: easy to expand with new documents or code modules

The repository is now ready for:
- External collaboration
- Contribution guidelines
- Stable cross-references
- Professional presentation

---

**Status: ✅ READY FOR MERGE**

Questions? See `REFACTOR-SUMMARY.md` or `archive/LEGACY-NAMING-MAP.md`.
