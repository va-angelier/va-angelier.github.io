"""Factory and loaders for Attack Tree nodes (JSON/YAML)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Type, Optional
from .nodes import Node, LeafNode, AndNode, OrNode

# Optional PyYAML import; keep explicit name for pylint C0103
try:
    import yaml as YAML_MOD  # type: ignore  # pylint: disable=import-error
except ImportError:  # pragma: no cover
    YAML_MOD = None


def dread_to_probability(dread: dict, *, method: str = "mean", floor: float = 0.01, ceiling: float = 0.99) -> float:
    """
    Map a DREAD dict to probability in [floor, ceiling].
    Expected keys: damage, repro, exploit, affected, discover (0..10).
    Mapping: p = mean/10, clamped.
    """
    if not isinstance(dread, dict):
        return floor
    scores = []
    for key in ("damage", "repro", "exploit", "affected", "discover"):
        v = dread.get(key)
        try:
            if v is None:
                continue
            scores.append(float(v))
        except (TypeError, ValueError):
            continue
    if not scores:
        return floor
    p = (sum(scores) / len(scores)) / 10.0
    return max(float(floor), min(float(ceiling), p))


class NodeFactory:
    """Create Node instances from dictionaries or files."""
    TYPE_MAP: Dict[str, Type[Node]] = {
        "LEAF": LeafNode,
        "AND": AndNode,
        "OR": OrNode,
    }

    @staticmethod
    def dread_to_probability(dread: Dict[str, Any], *,
                             method: str = "mean",
                             floor: float = 0.01,
                             ceiling: float = 0.99) -> float:
        """
        Convert a DREAD dict into a probability in [floor, ceiling].

        dread expected keys: 'damage','repro','exploit','affected','discover'
        Values normally 0..10. Default mapping: mean/10.
        """
        if not dread or not isinstance(dread, dict):
            return floor
        scores = []
        for key in ("damage", "repro", "exploit", "affected", "discover"):
            v = dread.get(key)
            try:
                if v is None:
                    continue
                scores.append(float(v))
            except (TypeError, ValueError):
                continue
        if not scores:
            return floor
        if method == "mean":
            mean_score = sum(scores) / len(scores)
            p = mean_score / 10.0
        else:
            # fallback to mean
            p = sum(scores) / (len(scores) * 10.0)
        # clamp
        p = max(float(floor), min(float(ceiling), p))
        return p

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Node:
        """Build a Node from a JSON/YAML dict with optional DREAD -> probability."""
        ntype = str(data.get("type", "LEAF")).upper()
        node_cls = cls.TYPE_MAP.get(ntype, OrNode)
        node_id = str(data.get("id") or data.get("label") or "node")
        label = str(data.get("label") or node_id)

        def _get_probability(d: Dict[str, Any]) -> float:
            # If an explicit probability is present and parsable, keep it.
            if "probability" in d and d.get("probability") is not None:
                try:
                    return float(d.get("probability"))
                except (TypeError, ValueError):
                    pass
            # Otherwise derive from DREAD (if present), else fallback small default.
            dread_obj = d.get("dread")
            if isinstance(dread_obj, dict):
                return dread_to_probability(dread_obj)
            return 0.01

        if node_cls is LeafNode:
            p = _get_probability(data)
            impact = float(data.get("impact", 0.0))
            return LeafNode(id=node_id, label=label, probability=p, impact=impact)

        raw_children = data.get("children", []) or []
        built_children: List[Node] = [cls.from_dict(c) for c in raw_children]
        if node_cls is AndNode:
            return AndNode(id=node_id, label=label, _children=built_children)
        return OrNode(id=node_id, label=label, _children=built_children)

    @staticmethod
    def _read_text(path: str) -> str:
        """Read a UTF-8 text file."""
        return Path(path).read_text(encoding="utf-8")

    @classmethod
    def load_json(cls, path: str) -> Node:
        """Load a Node tree from a JSON file."""
        data = json.loads(cls._read_text(path))
        return cls.from_dict(data)

    @classmethod
    def load_yaml(cls, path: str) -> Node:
        """Load a Node tree from a YAML file (requires PyYAML)."""
        if YAML_MOD is None:
            raise RuntimeError(
                "PyYAML not installed. Install with `pip install pyyaml`."
            )
        data = YAML_MOD.safe_load(cls._read_text(path))
        return cls.from_dict(data)

    @classmethod
    def load(cls, path: str) -> Node:
        """Load a Node tree from a JSON or YAML file."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)
        if p.suffix.lower() in (".yaml", ".yml"):
            return cls.load_yaml(path)
        return cls.load_json(path)
