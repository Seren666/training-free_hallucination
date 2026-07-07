from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class EvidenceWeights:
    probability: float = 1.0
    visual: float = 1.0
    attention: float = 0.5
    anchor: float = 0.5

    def total(self) -> float:
        return self.probability + self.visual + self.attention + self.anchor


def clamp01(value: float) -> float:
    if not isfinite(value):
        raise ValueError("risk evidence must be finite")
    return min(1.0, max(0.0, value))


def weighted_risk_score(
    *,
    probability_risk: float,
    visual_risk: float,
    attention_risk: float = 0.0,
    anchor_risk: float = 0.0,
    weights: EvidenceWeights | None = None,
) -> float:
    """Combine normalized evidence into a bounded risk score.

    Inputs are expected to be normalized to [0, 1], where larger means riskier.
    The default weights mirror the public method description: uncertainty and
    visual evidence are primary; attention evolution and anchoring are lighter
    contextual terms.
    """

    active_weights = weights or EvidenceWeights()
    total = active_weights.total()
    if total <= 0:
        raise ValueError("at least one evidence weight must be positive")

    score = (
        active_weights.probability * clamp01(probability_risk)
        + active_weights.visual * clamp01(visual_risk)
        + active_weights.attention * clamp01(attention_risk)
        + active_weights.anchor * clamp01(anchor_risk)
    ) / total
    return round(score, 6)
