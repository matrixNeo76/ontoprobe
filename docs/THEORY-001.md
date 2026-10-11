# OKF v0.2 — Research Framework: Innovazione Ontologica negli LLM (v0.3.1)

> Alignment note: this document is the theoretical and epistemological foundation of the ONTO-PROBE suite.

## 0. Changelog

### 0.1 Transition v0.1 → v0.2
- Initial multi-agent ONTO-PROBE architecture
- Definition of O-Novel benchmark and initial DMP

### 0.2 Transition v0.2 → v0.2.1
- Falsificationist reframing of statistical learning limits
- Replacement of a scalar threshold with multi-criteria validity gates

### 0.3 Transition v0.2.1 → v0.3.0
- No New Basis Principle formalized
- Contrastive Activation Addition (CAA) defined canonically
- Power analysis ANOVA with moderate effect ($f = 0.25$)
- Multi-embedder protocol added to guard OOD distortion

### 0.4 Release v0.3.1
- HMAC blinding introduced
- Safety triad extended to include cognitive manipulation
- Runtime bugs fixed around API roles and empty steering vectors

## 1. Executive summary

ONTO-PROBE investigates whether large language models can generate genuine ontological innovation: new causal relations, predicates, and explanatory frameworks not reducible by interpolation over known archetypes.

The project assumes a falsificationist posture: if the geometric closure of the transformer architecture is insurmountable, the protocol measures the maximum divergence reachable under isolated generation and validated steering.

## 2. Epistemic limits

The framework distinguishes several layers of limitation:

1. Representational: closure of the convex hull of training data
2. Mechanical: diversity collapse in multi-agent loops
3. Evaluative: OOD distortions in embedding models
4. Functional: trade-off between conceptual divergence and coherence
5. Operational: review overload for human evaluators

## 3. Ontological novelty

A candidate output is considered ontologically novel when it introduces a structure that cannot be mapped through direct structural isomorphism to known archetypes and still passes a validity gate.

## 4. Architecture

The core workflow is:

- seed generation via activation steering or semantic tabu constraints
- world-building by isolated agents
- blind solving under constraints
- invariant extraction across world models
- formal or human validation

## 5. Key formulas

Steering vector:

$$v_{onto} = \frac{1}{|P|} \sum_{p \in P} a_L(p) - \frac{1}{|N|} \sum_{n \in N} a_L(n)$$

Activation update:

$$h^{(L)}_{steered} = h^{(L)} + \alpha \cdot v_{onto}, \quad \alpha \in [1.0, 2.0]$$

## 6. Practical interpretation

The project does not promise a breakthrough in genuine ontological creativity. Instead, it attempts to measure the boundary of what LLMs can do under rigorously controlled conditions.

This makes it useful as a negative-result research program, where a validated null result is itself scientifically meaningful.
