# OKF v0.2 — Protocollo Sperimentale e Human Evaluation Runbook: ONTO-PROBE (v0.3.1)

> This document standardizes the experimental procedure for double-blind evaluation, inter-rater reliability, and downstream statistical analysis.

## 1. Purpose

The evaluation pipeline is intended to eliminate subjective drift and provide a reproducible scientific protocol.

## 2. Experimental design

The evaluation matrix uses 3 conditions across 5 domains:

- control 1: single-agent baseline
- control 2: standard multi-agent interaction
- treatment: ONTO-PROBE pipeline

## 3. Blinding

Each dossier is assigned a blind identifier derived through HMAC, so that reviewers never see any internal traceability metadata.

## 4. Human scoring rubric

Reviewers score outputs on dimensions such as:

- functional validity
- reduction to known archetypes
- semantic integrity vs. lexical illusion
- transferability and abstract isomorphism

## 5. Statistics

The statistical harness computes agreement metrics and repeated-measures ANOVA once rating data has been cleaned and pairwise deletion is applied for missing values.

## 6. Decision gate

If LLM-based judges disagree strongly or if appropriateness is below threshold, the case is escalated to human review or rejected.
