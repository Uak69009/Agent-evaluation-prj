# Research Log — AgentEvalOps

This document tracks hypotheses, baselines, evaluation benchmarks, random seeds, experiment configurations, dataset versions, and statistical findings.

---

## Research Program & Hypotheses

### Hypothesis H1: Multi-Dimensional Trajectory Evaluation vs. Outcome-Only Evaluation
- **Hypothesis:** outcome-only metrics (e.g. final answer string match) fail to catch silent failures, unsafe tool calls, inefficient loops, and cost overruns. Evaluators measuring step efficiency, tool-argument validity, and state integrity produce significantly higher correlation with human expert judgment.
- **Baseline:** Standard string exact match & BLEU/ROUGE on final answer.
- **Metrics:** Precision, Recall, F1, AUROC of failure prediction, human correlation coefficient (Spearman's $\rho$).
- **Status:** PLANNED (Phase 6 / Phase 12).

---

## Experiment Registry

| Experiment ID | Date | Objective | Baseline | Model / Dataset | Result | Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP-001** | 2026-08-28 | SDK Telemetry Overhead Measurement | Raw Python execution | Simulated 50-span trace | <1.2ms latency overhead | `PERFORMANCE_LOG.md` |
