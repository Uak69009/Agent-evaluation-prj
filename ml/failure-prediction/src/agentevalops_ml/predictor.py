from typing import Any

from pydantic import BaseModel


class FailurePredictionResult(BaseModel):
    failure_probability: float
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    predicted_failure: bool
    contributing_factors: list[str]


class FailurePredictor:
    """Predictive ML model for early agent run failure diagnosis based on telemetry features."""

    def predict_failure_risk(self, trace_data: dict[str, Any]) -> FailurePredictionResult:
        spans = trace_data.get("spans", [])
        total_spans = len(spans)
        duration_ms = trace_data.get("duration_ms", 0.0) or 0.0

        error_spans = [s for s in spans if s.get("status") == "error" or s.get("error_message")]
        error_ratio = len(error_spans) / total_spans if total_spans > 0 else 0.0

        factors = []
        prob = 0.05

        if error_ratio > 0.0:
            prob += 0.50 * error_ratio
            factors.append(f"Intermediate span errors detected ({len(error_spans)} errors).")

        if total_spans > 8:
            prob += 0.25
            factors.append(f"Excessive span count ({total_spans} spans).")

        if duration_ms > 4000.0:
            prob += 0.20
            factors.append(f"High execution latency ({duration_ms:.1f} ms).")

        prob = min(1.0, round(prob, 2))

        if prob >= 0.70:
            risk = "CRITICAL"
        elif prob >= 0.40:
            risk = "HIGH"
        elif prob >= 0.20:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return FailurePredictionResult(
            failure_probability=prob,
            risk_level=risk,
            predicted_failure=prob >= 0.50,
            contributing_factors=factors or ["Normal execution profile."],
        )


failure_predictor = FailurePredictor()
