"""Renderers for Attack Trees: ASCII and Graphviz DOT."""
from __future__ import annotations

from typing import List, Tuple, Set, TYPE_CHECKING
from .nodes import Node

# Only for type hints; avoids runtime import/cycles
if TYPE_CHECKING:
    from .aggregation import AggregationStrategy

class AsciiRenderer:
    """Produce a readable ASCII view with per-node aggregates."""

    @classmethod
    def line_for_node(cls, node: Node, strategy: "AggregationStrategy", prefix: str) -> str:
        """Return one formatted line for a node."""
        a = node.aggregate(strategy)
        return (
            f"{prefix}{node.safe_label()} [{node.type_name}] "
            f"(p={a.probability:.4f}, impact={a.impact:.2f}, "
            f"exp_loss={a.expected_loss:.2f})\n"
        )

    @classmethod
    def render(cls, node: Node, strategy: "AggregationStrategy", prefix: str = "") -> str:
        """Render node and its subtree as ASCII."""
        line = cls.line_for_node(node, strategy, prefix)
        children = list(node.children())
        for idx, child in enumerate(children):
            last = idx == len(children) - 1
            child_prefix = prefix + ("    " if last else "│   ")
            line += cls.render(child, strategy, child_prefix)
        return line


class DotRenderer:
    """Build a Graphviz DOT body (without header/footer)."""

    @staticmethod
    def escape_label(text: str) -> str:
        """Escape quotes for DOT labels."""
        return text.replace('"', '\\"')

    @staticmethod
    def node_id(node: Node) -> str:
        """Create a stable DOT id for a node."""
        base = node.id or node.safe_label()
        return "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in base)

    @classmethod
    def render(cls, node: Node, strategy: "AggregationStrategy") -> str:
        """Render the subtree rooted at node to DOT edges and node labels."""
        lines: List[str] = []
        edges: List[Tuple[str, str]] = []
        seen: Set[str] = set()

        def visit(n: Node) -> None:
            nid = cls.node_id(n)
            if nid in seen:
                return
            seen.add(nid)
            a = n.aggregate(strategy)
            label = (
                f"{n.safe_label()}\\n{n.type_name}"
                f"\\np={a.probability:.4f}\\nexp={a.expected_loss:.2f}"
            )
            lines.append(
                f"\"{nid}\" [label=\"{cls.escape_label(label)}\", "
                "shape=box, style=rounded, fontsize=10];"
            )
            for c in n.children():
                cid = cls.node_id(c)
                edges.append((nid, cid))
                visit(c)

        visit(node)
        edge_lines = [f"\"{a}\" -> \"{b}\";" for a, b in edges]
        return "\n".join(lines + edge_lines)
