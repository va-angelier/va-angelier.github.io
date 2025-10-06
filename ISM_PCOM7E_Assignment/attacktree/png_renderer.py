"""PNG rendering without Graphviz, using matplotlib + networkx.

This is a simple fallback: it converts the tree to a directed graph and plots it.
Layout uses spring_layout; for strict hierarchies you could implement a custom
layered layout if desired.
"""
from __future__ import annotations
from typing import Tuple, List, Dict

import matplotlib.pyplot as plt
import networkx as nx

from .nodes import Node, Aggregate
from .aggregation import AggregationStrategy


def _collect_edges(node: Node, strategy: AggregationStrategy) -> Tuple[nx.DiGraph, Dict[str, str]]:
    """Traverse the tree and build a NetworkX DiGraph with labels."""
    g = nx.DiGraph()
    labels: Dict[str, str] = {}

    def nid(n: Node) -> str:
        base = n.id or n.safe_label()
        return "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in base)

    def visit(n: Node) -> str:
        this_id = nid(n)
        a: Aggregate = n.aggregate(strategy)
        label = f"{n.safe_label()}\n{n.type_name}\np={a.probability:.4f}\nexp={a.expected_loss:.2f}"
        labels[this_id] = label
        if this_id not in g:
            g.add_node(this_id)
        for c in n.children():
            cid = visit(c)
            g.add_edge(this_id, cid)
        return this_id

    visit(node)
    return g, labels


def render_png(node: Node, strategy: AggregationStrategy, out_png: str) -> str:
    """Render the tree to a PNG using matplotlib (no Graphviz required)."""
    g, labels = _collect_edges(node, strategy)

    # Layout (spring_layout works generally; for trees consider graphviz_layout if available)
    pos = nx.spring_layout(g, seed=42, k=0.8)

    plt.figure(figsize=(12, 8), dpi=150)
    nx.draw_networkx_edges(g, pos, arrows=True, arrowstyle="-|>", arrowsize=10)
    nx.draw_networkx_nodes(g, pos, node_size=1500, node_shape="s")
    nx.draw_networkx_labels(g, pos, labels=labels, font_size=8)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    return out_png
