"""AttackTree facade: loading, aggregation, and rendering."""
from __future__ import annotations

from pathlib import Path
from .nodes import Node, Aggregate
from .aggregation import AggregationStrategy, BasicAggregation
from .factory import NodeFactory
from .renderers import AsciiRenderer, DotRenderer


class AttackTree:
    """High-level API for working with attack trees."""

    def __init__(self, root: Node, strategy: AggregationStrategy | None = None) -> None:
        """Create an AttackTree with a root Node and an aggregation strategy."""
        self.root = root
        self.strategy = strategy or BasicAggregation()

    @classmethod
    def from_file(cls, path: str, strategy: AggregationStrategy | None = None) -> "AttackTree":
        """Load a tree from JSON/YAML."""
        root = NodeFactory.load(path)
        return cls(root, strategy=strategy)

    def aggregate(self) -> Aggregate:
        """Aggregate the full tree."""
        return self.root.aggregate(self.strategy)

    def to_ascii(self) -> str:
        """Render the tree as ASCII text."""
        return AsciiRenderer.render(self.root, self.strategy)

    def to_dot(self) -> str:
        """Render the tree as Graphviz DOT body (without header/footer)."""
        return DotRenderer.render(self.root, self.strategy)

    def write_dot(self, path: str) -> str:
        """Write a full DOT file including header/footer."""
        header = (
            "digraph AttackTree {\n"
            "rankdir=TB;\n"
            "node [shape=box, style=rounded, fontsize=10];\n"
        )
        content = header + self.to_dot() + "\n}\n"
        Path(path).write_text(content, encoding="utf-8")
        return path
