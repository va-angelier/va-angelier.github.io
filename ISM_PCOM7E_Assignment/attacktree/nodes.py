"""Domain model for Attack Trees: nodes and aggregation result container."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, TYPE_CHECKING

# Only for type hints (no runtime import, avoids cycles/lint noise)
if TYPE_CHECKING:
    from .aggregation import AggregationStrategy


@dataclass
class Aggregate:
    """Aggregated values for a node: probability, impact, expected loss."""
    probability: float
    impact: float
    expected_loss: float

    def to_dict(self) -> Dict[str, float]:
        """Return a serialisable dict representation."""
        return {
            "probability": self.probability,
            "impact": self.impact,
            "expected_loss": self.expected_loss,
        }


@dataclass
class Node:
    """Abstract base for all attack tree nodes."""
    id: str
    label: str
    type_name: str = field(default="LEAF")

    def children(self) -> Iterable["Node"]:
        """Return child nodes (empty for leaves)."""
        return []

    def aggregate(self, strategy: "AggregationStrategy") -> Aggregate:
        """Aggregate this node using the provided strategy."""
        raise NotImplementedError

    def safe_label(self) -> str:
        """Return a non-empty label for display."""
        return self.label or self.id


@dataclass
class LeafNode(Node):
    """Leaf node holding primitive probability and impact values."""
    probability: float = 0.0
    impact: float = 0.0

    def __post_init__(self) -> None:
        """Normalise types and clamp probability to [0,1]."""
        self.type_name = "LEAF"
        self.probability = max(0.0, min(1.0, float(self.probability)))
        self.impact = float(self.impact)

    def aggregate(self, strategy: "AggregationStrategy") -> Aggregate:
        """Delegate to strategy for leaf aggregation."""
        return strategy.aggregate_leaf(self)


@dataclass
class AndNode(Node):
    """AND node: all children conditions must hold."""
    _children: List[Node] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.type_name = "AND"

    def children(self) -> Iterable[Node]:
        return self._children

    def aggregate(self, strategy: "AggregationStrategy") -> Aggregate:
        return strategy.aggregate_and(self)


@dataclass
class OrNode(Node):
    """OR node: any child condition may hold."""
    _children: List[Node] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.type_name = "OR"

    def children(self) -> Iterable[Node]:
        return self._children

    def aggregate(self, strategy: "AggregationStrategy") -> Aggregate:
        return strategy.aggregate_or(self)
