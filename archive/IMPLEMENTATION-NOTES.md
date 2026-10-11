# Implementation Notes: CAA Smoke Test Notebook (ONTO-PROBE v0.3.1)

> **Archive Notice:** This document is historical review material. For current implementation details, see `docs/IMPL-001.md`.

---

## Overview

This notebook translates a complex mechanistic interpretability protocol into a linear, self-contained, and executable empirical workflow on consumer hardware.

**Competence Level Detected:** Outstanding.

---

## Technical Context

- **Domain:** Language model engineering, mechanistic interpretability (Activation Engineering)
- **Reference Standards:** Reproducibility guidelines for top-tier ML conferences (NeurIPS/ICLR)
- **Diagnostic Criteria:**
  1. Runtime stability: crash-free, VRAM management, memory leak prevention
  2. Methodological fidelity: correct residual stream interception, CAA consistency
  3. Metric discriminability: reliability of automatic abort criteria
  4. Operational readiness: prepared for human qualitative inspection

---

## Key Technical Issues Resolved in v0.3.2

### Issue 1: Tokenization Misalignment
**Problem:** Contrast pair prompts were tokenized without chat template, while generation prompts used the template, causing vector extraction to be misaligned.  
**Solution:** Apply chat template uniformly to all contrast pairs to ensure the steering vector captures the exact latent state being targeted.

### Issue 2: Parquet Serialization Dependency
**Problem:** Setup installs core libraries but omits `pyarrow`, causing ImportError when Parquet export is triggered.  
**Solution:** Explicitly add `pyarrow` to the dependency list or provide immediate CSV fallback.

### Issue 3: Tensor Isolation in Pre-Hook
**Problem:** In-place mutation on `args[0]` slices could corrupt KV-cache references during autoregressive generation.  
**Solution:** Apply explicit `.clone()` before mutation to isolate the injected state from contiguous memory buffers.

---

## Operational Guidance

For the smoke test, the priority sequence is:

1. **First:** Verify vector extraction without NaN or crash
2. **Second:** Validate coherent generation across alpha range [1.0, 2.0]
3. **Third:** Check monotonic dose-response relationship
4. **Fourth:** Inspect qualitative distinctiveness of ontological axes

---

## Downstream Steps

Once the smoke test passes, the next phase is qualitative inspection using `code/inspect_smoke_test_outputs.py`.

This tool extracts vocabulary divergence, dose-response progression, and cross-axis comparisons for human judgment.
