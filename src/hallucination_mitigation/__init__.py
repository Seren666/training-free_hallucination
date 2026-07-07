"""Lightweight utilities for training-free hallucination mitigation."""

from .post_decoding import SpanEdit, apply_span_edits
from .scoring import EvidenceWeights, weighted_risk_score

__all__ = [
    "EvidenceWeights",
    "SpanEdit",
    "apply_span_edits",
    "weighted_risk_score",
]
