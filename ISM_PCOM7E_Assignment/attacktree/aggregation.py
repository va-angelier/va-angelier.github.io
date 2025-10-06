"""Aggregation strategies for Attack Trees."""

from __future__ import annotations
from typing import List
from .nodes import Aggregate, LeafNode, AndNode, OrNode


class AggregationStrategy:
    """Base strategy interface (subclass to implement other models)."""
    def aggregate_leaf(self, node: LeafNode) -> Aggregate:  # pragma: no cover
        """Aggregate a leaf node."""
        raise NotImplementedError

    def aggregate_and(self, node: AndNode) -> Aggregate:  # pragma: no cover
        """Aggregate an AND node."""
        raise NotImplementedError

    def aggregate_or(self, node: OrNode) -> Aggregate:  # pragma: no cover
        """Aggregate an OR node."""
        raise NotImplementedError


class BasicAggregation(AggregationStrategy):
    """Explainable default aggregation.

    - LEAF: EL = p * impact
    - AND : P = ∏ p_i ; Impact = Σ impact_i
    - OR  : P = 1 − ∏ (1 − p_i) ; Impact = max(impact_i)
    """

    def aggregate_leaf(self, node: LeafNode) -> Aggregate:
        p = node.probability
        impact = node.impact
        return Aggregate(p, impact, p * impact)

    def aggregate_and(self, node: AndNode) -> Aggregate:
        ps: List[float] = []
        impacts: List[float] = []
        for child in node.children():
            a = child.aggregate(self)
            ps.append(a.probability)
            impacts.append(a.impact)
        p = 1.0
        for v in ps:
            p *= v
        impact = sum(impacts) if impacts else 0.0
        return Aggregate(p, impact, p * impact)

    def aggregate_or(self, node: OrNode) -> Aggregate:
        prod = 1.0
        impacts: List[float] = []
        for child in node.children():
            a = child.aggregate(self)
            prod *= (1.0 - a.probability)
            impacts.append(a.impact)
        p = 1.0 - prod
        impact = max(impacts) if impacts else 0.0
        return Aggregate(p, impact, p * impact)
