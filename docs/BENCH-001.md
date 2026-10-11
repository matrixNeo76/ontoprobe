# OKF v0.2 — Benchmark O-Novel: Catalogo dei Task e Specifiche Esecutive (v0.3.1)

> This benchmark is designed to test whether a model can generate conceptually open solutions while avoiding trivial recombination or masked hallucination.

## 1. Benchmark objective

The suite includes 50 tasks across 5 domains, split into:

- Binary A: 20 formally verifiable tasks
- Binary B: 30 open-domain tasks with semantic taboos

## 2. Domains

1. Cryptography and security protocols
2. Boolean logic, SMT, graph constraints
3. Systems design and engineering
4. Public policy and institutional mechanisms
5. Scientific epistemology and information theory

## 3. Sample tasks

### Binary A examples
- ONTO-A01: secure key exchange with forward secrecy
- ONTO-A11: graph partitioning with exclusion constraints
- ONTO-A20: CNF minimization under topological constraints

### Binary B examples
- ONTO-B21: passive cooling without conventional heat pipes
- ONTO-B35: mitigation of polarization in civic forums
- ONTO-B50: formalization of retroactive causality in simulation

## 4. Evaluation contract

Each task includes a target problem, taboo archetypes, and an evaluation contract. Tasks that pass the validity gate may then be compared against background archetypes and scored for structural displacement.

## 5. Scoring logic

The benchmark uses a conservative logic: if a candidate fails validity and coherence, it receives a zero score regardless of lexical novelty.

This prevents the common error of mistaking jargon for genuine novelty.
