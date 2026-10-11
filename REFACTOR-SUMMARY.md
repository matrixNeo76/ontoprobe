# Repository Restructuring Summary

**Date:** 2026-10-11  
**Branch:** `reorg-docs-structure`  
**Status:** Ready for review and merge

---

## Overview

This refactor reorganizes the ONTO-PROBE repository to align with:
- The official structure declared in `README.md`
- Standard layout conventions (docs, code, outputs)
- OKF v0.2 documentation standards
- Clear separation of concerns

## Problems Solved

### 1. Structure-Documentation Mismatch
**Before:** README declared `docs/` and `code/` directories, but files were scattered in root and `notebook/`.  
**After:** All files now match README structure exactly.

### 2. Inconsistent Naming
**Before:** Files had long descriptive names (`research_framework_onto_probe_v0_3_0.md`).  
**After:** Canonical names follow OKF standard (`THEORY-001.md`, `IMPL-001.md`, etc.).

### 3. Mixed Concerns
**Before:** Documentation, code, and legacy reviews mixed in root and nested folders.  
**After:** Clear separation:
- `docs/` → official documentation only
- `code/` → executable code
- `outputs/` → generated artifacts
- `archive/` → historical and review material

### 4. No Trash Folder
**Before:** Legacy audit and review files were buried in root without clear status.  
**After:** Dedicated `archive/` with README explaining historical context.

---

## File Mapping

### Documentation (docs/)

```
THEORY-001.md        ← research_framework_onto_probe_v0_3_0.md
IMPL-001.md          ← guida_all_implementazione_computazionale_onto_probe.md
BENCH-001.md         ← catalogo_dei_task_e_specifiche_del_benchmark_o_novel.md
EVAL-001.md          ← protocollo_sperimentale_e_human_evaluation_runbook.md
META-001.md          ← analisi_della_suite_documentale_onto_probe.md
howto.md             ← guida_operativa_collaudo_caa.md
```

### Code (code/)

```
notebook_caa_smoke_test_v0_3_2.py           ← notebook/notebook_caa_smoke_test_v0_3_2.py
inspect_smoke_test_outputs.py                ← notebook/script_di_ispezione_qualitativa_e_comparatore_caa.py
```

### Archive (archive/)

```
README.md                    # Explanation of archive purpose
LEGACY-NAMING-MAP.md         # Complete mapping of old → new names
IMPLEMENTATION-NOTES.md      # ← notebook/revisione_tecnica_e_patch_del_notebook_caa_smoke_test.md
VALIDATION-AUDIT.md          # ← dossier_di_validazione_finale_e_audit_operativo.md
```

---

## Key Improvements

### Clarity
- Visitors immediately see the canonical structure
- README matches actual file locations
- No confusion about which files to use

### Maintainability
- All documentation in one place
- Standardized naming across documents
- Clear boundaries between active and archival material

### Discoverability
- Standard layout familiar to developers
- Reduced cognitive load when navigating
- Cross-references in docs now use stable canonical names

### Scalability
- Ready for expansion (future docs, benchmarks, code modules)
- Archive grows without cluttering the active repository
- Easy to add new documents following the naming convention

---

## Integration Checklist

- [x] Canonical documentation files created in `docs/`
- [x] Code files moved to `code/`
- [x] Output directory created with `.gitkeep`
- [x] Archive directory created with historical files
- [x] `.gitignore` added for outputs and build artifacts
- [x] `README.md` updated to reflect new structure
- [x] All cross-document references validated
- [x] Legacy file mapping documented in `archive/`

---

## Next Steps

1. **Review:** Check the branch for completeness and accuracy
2. **Merge:** PR to consolidate changes into main
3. **Verify:** Confirm all links and paths work after merge
4. **Communicate:** Update any external references if applicable

---

## Files Modified/Created

**Created:**
- `docs/THEORY-001.md`
- `docs/IMPL-001.md`
- `docs/BENCH-001.md`
- `docs/EVAL-001.md`
- `docs/META-001.md`
- `docs/howto.md`
- `code/notebook_caa_smoke_test_v0_3_2.py`
- `code/inspect_smoke_test_outputs.py`
- `outputs/.gitkeep`
- `archive/README.md`
- `archive/LEGACY-NAMING-MAP.md`
- `.gitignore`
- `REFACTOR-SUMMARY.md` (this file)

**Updated:**
- `README.md` (path references aligned)

---

## Validation

To verify the refactor is complete:

```bash
# Check structure matches README
tree -L 2 -I '__pycache__|*.pyc'

# Verify all links in README point to existing files
grep -r "docs/\|code/\|outputs/" README.md | while read line; do
  file=$(echo $line | grep -oP '(docs|code|outputs)/[^ ]*' | head -1)
  [ -f "$file" ] && echo "✓ $file" || echo "✗ $file MISSING"
done

# Confirm no broken cross-references
grep -r "http\|/mnt\|file://" docs/ code/ | grep -v "https://github.com\|https://arxiv\|https://" || echo "✓ No broken local references"
```

---

## Rollback

If needed, the previous structure can be recovered from the `main` branch.

To revert this reorganization:
```bash
git revert <commit-sha-of-merge>
```

---

**End of Summary**
