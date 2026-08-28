from typing import Any

from pydantic import BaseModel, Field


class PolicyProfile(BaseModel):
    minimum_task_success: float = 0.90
    maximum_cost_increase_pct: float = 20.0
    maximum_latency_increase_pct: float = 25.0


class GateDecisionSchema(BaseModel):
    decision: str  # "PASS", "WARN", "BLOCK"
    policy_name: str = "default_release_policy"
    passed: bool
    reasons: list[str] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)


class DeploymentGateEngine:
    """Evaluates agent release candidate metrics against baseline and policy profile."""

    def evaluate_gate(
        self,
        candidate_metrics: dict[str, Any],
        baseline_metrics: dict[str, Any] | None = None,
        policy: PolicyProfile | None = None,
    ) -> GateDecisionSchema:
        pol = policy or PolicyProfile()
        base = baseline_metrics or {"accuracy": 0.92, "cost_usd": 0.01, "duration_ms": 1000.0}

        reasons = []
        is_blocked = False
        is_warned = False

        # 1. Accuracy Check
        cand_acc = candidate_metrics.get("accuracy", 1.0)
        if cand_acc < pol.minimum_task_success:
            is_blocked = True
            reasons.append(f"Accuracy ({cand_acc}) below minimum policy threshold ({pol.minimum_task_success}).")

        # 2. Cost Increase Check
        cand_cost = candidate_metrics.get("cost_usd", 0.0)
        base_cost = base.get("cost_usd", 0.001)
        cost_inc = ((cand_cost - base_cost) / base_cost) * 100 if base_cost > 0 else 0.0

        if cost_inc > pol.maximum_cost_increase_pct:
            is_warned = True
            reasons.append(f"Cost increased by {cost_inc:.1f}% (exceeds {pol.maximum_cost_increase_pct}% limit).")

        # 3. Latency Increase Check
        cand_lat = candidate_metrics.get("duration_ms", 0.0)
        base_lat = base.get("duration_ms", 100.0)
        lat_inc = ((cand_lat - base_lat) / base_lat) * 100 if base_lat > 0 else 0.0

        if lat_inc > pol.maximum_latency_increase_pct:
            is_warned = True
            reasons.append(f"Latency increased by {lat_inc:.1f}% (exceeds {pol.maximum_latency_increase_pct}% limit).")

        if is_blocked:
            decision = "BLOCK"
        elif is_warned:
            decision = "WARN"
        else:
            decision = "PASS"
            reasons.append("All policy thresholds met successfully. Ready for deployment.")

        return GateDecisionSchema(
            decision=decision,
            passed=not is_blocked,
            reasons=reasons,
            metrics={
                "candidate": candidate_metrics,
                "baseline": base,
                "cost_increase_pct": round(cost_inc, 1),
                "latency_increase_pct": round(lat_inc, 1),
            },
        )


deployment_gate_engine = DeploymentGateEngine()
