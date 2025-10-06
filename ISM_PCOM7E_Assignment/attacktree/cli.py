"""CLI entry point for the Attack Tree analyser."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from .tree import AttackTree
from .comparator import Comparator

def _render_with_graphviz(dot_path: str, png_path: str) -> None:
    """Render via Graphviz 'dot'."""
    import subprocess
    try:
        subprocess.run(["dot", "-Tpng", dot_path, "-o", png_path], check=True)
        print(f"Rendered PNG: {png_path}")
    except FileNotFoundError as exc:
        print(f"Graphviz 'dot' not found on PATH: {exc}")
    except subprocess.CalledProcessError as exc:
        print(f"'dot' failed for {dot_path}: {exc}")


def _render_with_matplotlib(tree: AttackTree, png_path: str) -> None:
    """Render via matplotlib+networkx (no Graphviz needed)."""
    from .png_renderer import render_png  # local import to keep optional deps
    render_png(tree.root, tree.strategy, png_path)
    print(f"Rendered PNG (matplotlib): {png_path}")

def _render_dot(dot_path: str, png_path: str) -> None:
    """Render a DOT file to PNG using Graphviz 'dot'."""
    try:
        subprocess.run(
            ["dot", "-Tpng", dot_path, "-o", png_path],
            check=True,
        )
        print(f"Rendered PNG: {png_path}")
    except FileNotFoundError as exc:
        print(f"Graphviz 'dot' not found on PATH: {exc}")
    except subprocess.CalledProcessError as exc:
        print(f"'dot' failed for {dot_path}: {exc}")


def main() -> None:
    """Parse CLI arguments and execute commands."""
    parser = argparse.ArgumentParser(
        prog="attacktree",
        description="Attack Tree Analyser (OOP, modular)",
    )
    parser.add_argument(
        "--input", "-i",
        help="Input attack tree JSON/YAML",
    )
    parser.add_argument(
        "--compare", nargs=2, metavar=("PRE", "POST"),
        help="Compare two trees (pre post)",
    )
    parser.add_argument(
        "--ascii", action="store_true",
        help="Print ASCII tree",
    )
    parser.add_argument(
        "--dot",
        help=("Write DOT to this path "
              "(or prefix if used with --compare)"),
    )
    parser.add_argument(
        "--render",
        help=("Render DOT to PNG (path). With --compare, "
              "treated as prefix."),
    )
    parser.add_argument(
        "--out",
        help="Write JSON output to file",
    )
    parser.add_argument(
        "--renderer",
        choices=["graphviz", "matplotlib"],
        default="graphviz",
        help="PNG renderer to use. 'graphviz' requires dot; 'matplotlib' needs matplotlib+networkx.",
    )
    args = parser.parse_args()

    if args.compare:
        pre = AttackTree.from_file(args.compare[0])
        post = AttackTree.from_file(args.compare[1])
        comp = Comparator.compare(pre, post).to_dict()
        print(json.dumps(comp, indent=2))
        if args.out:
            Path(args.out).write_text(
                json.dumps(comp, indent=2),
                encoding="utf-8",
            )
        if args.dot:
            pre_dot = args.dot + "_pre.dot"
            post_dot = args.dot + "_post.dot"
            pre.write_dot(pre_dot)
            post.write_dot(post_dot)
            print(f"Wrote DOT: {pre_dot}, {post_dot}")
            if args.render:
                if args.renderer == "graphviz":
                    _render_with_graphviz(pre_dot, args.render + "_pre.png")
                    _render_with_graphviz(post_dot, args.render + "_post.png")
                else:
                    _render_with_matplotlib(pre, args.render + "_pre.png")
                    _render_with_matplotlib(post, args.render + "_post.png")
        return

    if not args.input:
        parser.print_help()
        return

    tree = AttackTree.from_file(args.input)
    agg = tree.aggregate().to_dict()
    print(json.dumps(agg, indent=2))

    if args.ascii:
        print("\n" + tree.to_ascii())

    if args.dot:
        dot_path = tree.write_dot(args.dot)
        print(f"Wrote DOT: {dot_path}")
        if args.render:
            if args.renderer == "graphviz":
                _render_with_graphviz(dot_path, args.render)
            else:
                _render_with_matplotlib(tree, args.render)

    if args.out:
        Path(args.out).write_text(
            json.dumps({"aggregation": agg}, indent=2),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
