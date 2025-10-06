"""Comparison helpers for pre/post attack trees."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any

from .tree import AttackTree
from .nodes import Aggregate


@dataclass
class Comparison:
    """Comparison result between two trees."""
    pre: Aggregate
    post: Aggregate
    delta_expected_loss: float
    percent_change_expected_loss: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the comparison result."""
        return {
            "pre": self.pre.to_dict(),
            "post": self.post.to_dict(),
            "delta_expected_loss": self.delta_expected_loss,
            "percent_change_expected_loss": self.percent_change_expected_loss,
        }


class Comparator:
    """Create comparison metrics for two trees (pre vs post)."""

    @staticmethod
    def compare(pre_tree: AttackTree, post_tree: AttackTree) -> Comparison:
        """Compute delta and percentage change in expected loss."""
        pre = pre_tree.aggregate()
        post = post_tree.aggregate()
        delta = post.expected_loss - pre.expected_loss
        pct = None if pre.expected_loss == 0 else (delta / pre.expected_loss) * 100.0
        return Comparison(pre, post, delta, pct)

    @staticmethod
    def compare_dict(pre_tree: AttackTree, post_tree: AttackTree) -> Dict[str, Any]:
        """Convenience wrapper returning a dict directly."""
        return Comparator.compare(pre_tree, post_tree).to_dict()
