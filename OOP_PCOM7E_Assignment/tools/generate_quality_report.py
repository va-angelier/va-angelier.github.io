from __future__ import annotations
import sys, os, datetime, platform
from pathlib import Path
from typing import Dict, List, Tuple

# Radon API (geen shell parsing nodig)
from radon.complexity import cc_visit, cc_rank
from radon.metrics import mi_visit, mi_rank

EXCLUDES = {".venv", "venv", "__pycache__", ".git", "build", "dist"}

def iter_py_files(root: Path) -> List[Path]:
    files = []
    for p, dnames, fnames in os.walk(root):
        # exclude dirs
        dnames[:] = [d for d in dnames if d not in EXCLUDES]
        for f in fnames:
            if f.endswith(".py"):
                files.append(Path(p) / f)
    return files

def analyse_cc(pyfile: Path):
    src = pyfile.read_text(encoding="utf-8", errors="ignore")
    try:
        blocks = cc_visit(src)
    except Exception:
        return []
    results = []
    for b in blocks:
        # b: Class or Function block
        results.append({
            "name": f"{b.name}",
            "type": b.__class__.__name__,
            "lineno": b.lineno,
            "complexity": b.complexity,
            "rank": cc_rank(b.complexity),
        })
    return results

def analyse_mi(pyfile: Path):
    src = pyfile.read_text(encoding="utf-8", errors="ignore")
    try:
        mi = mi_visit(src, True)  # multi=True -> line-count sensitive
    except Exception:
        mi = 0.0
    return float(mi), mi_rank(mi)

def main(target: str = ".", out: str = "docs"):
    root = Path(target).resolve()
    out_dir = Path(out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "Code_Quality_Report.md"

    pyfiles = iter_py_files(root)
    cc_all: Dict[Path, List[dict]] = {}
    rank_counts = {r: 0 for r in list("ABCDEF")}
    hotspots: List[Tuple[float, Path, int, str]] = []
    mi_map: Dict[Path, Tuple[float, str]] = {}

    for f in pyfiles:
        blocks = analyse_cc(f)
        cc_all[f] = blocks
        for b in blocks:
            rank_counts[b["rank"]] = rank_counts.get(b["rank"], 0) + 1
            hotspots.append((b["complexity"], f, b["lineno"], b["name"]))
        mi_val, mi_r = analyse_mi(f)
        mi_map[f] = (mi_val, mi_r)

    hotspots.sort(reverse=True, key=lambda x: x[0])
    top_hotspots = hotspots[:10]

    # Averages
    mi_values = [v for v, _ in mi_map.values() if v > 0]
    avg_mi = sum(mi_values) / len(mi_values) if mi_values else 0.0

    # Mermaid pie from rank_counts
    total_blocks = sum(rank_counts.values()) or 0

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    pyver = platform.python_version()

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(root))
        except ValueError:
            return str(p)

    with report_path.open("w", encoding="utf-8") as w:
        w.write(f"# Code Quality Report\n\n")
        w.write(f"**Generated:** {now}  \n")
        w.write(f"**Environment:** Python {pyver}  \n")
        w.write(f"**Target:** `{rel(root)}`\n\n")

        w.write("## Executive Summary\n")
        w.write(f"- Cyclomatic Complexity blocks analysed: **{total_blocks}**  \n")
        w.write(f"- Maintainability Index (average): **{avg_mi:.1f}**  \n\n")

        w.write("## Cyclomatic Complexity — Rank Distribution\n")
        w.write("```mermaid\npie showData\n")
        for rank in "ABCDEF":
            if rank_counts[rank] > 0:
                w.write(f'  "{rank}" : {rank_counts[rank]}\n')
        w.write("```\n\n")

        w.write("## Maintainability Index per file\n")
        w.write("| File | MI | Rank |\n|---|---:|:---:|\n")
        for f, (mi_val, mi_r) in sorted(mi_map.items(), key=lambda kv: kv[0].as_posix()):
            w.write(f"| `{rel(f)}` | {mi_val:.1f} | {mi_r} |\n")
        w.write("\n")

        w.write("## Top 10 Complexity Hotspots\n")
        if top_hotspots:
            w.write("| Complexity | File | Line | Block |\n|---:|---|---:|---|\n")
            for c, f, ln, name in top_hotspots:
                w.write(f"| {c:.1f} | `{rel(f)}` | {ln} | `{name}` |\n")
        else:
            w.write("_No functions/classes detected._\n")
        w.write("\n")

        w.write("## Interpretation (for Unit 10)\n")
        w.write("- **A/B ranks** indicate simple, testable blocks; **D/E/F** zijn refactor-kandidaten.  \n")
        w.write("- **Strategy/Observer + dependency injection** helpen CC laag te houden door logica te splitsen en koppelingsgraad te verlagen.  \n")
        w.write("- **MI** onder ~65 duidt vaak op technische schuld; prioriteer die bestanden voor opschoning.  \n\n")

        w.write("## How to Reproduce\n")
        w.write("```bash\n")
        w.write("# from project root (contains 'robot' package)\n")
        w.write("py -m pip install radon\n")
        w.write("py tools/generate_quality_report.py robot\n")
        w.write("```\n\n")

        w.write("## References (Harvard)\n")
        w.write("- McCabe, T.J. (1976) ‘A complexity measure’, *IEEE TSE*, SE-2(4), pp. 308–320.\n")
        w.write("- Chidamber, S.R. and Kemerer, C.F. (1994) ‘A metrics suite for object-oriented design’, *IEEE TSE*, 20(6), pp. 476–493.\n")
        w.write("- Gamma, E. et al. (1995) *Design Patterns*. Addison-Wesley.\n")
        w.write("- Romano, F. and Kruger, H. (2021) *Learn Python Programming*. Packt.\n")

    print(f"Wrote {report_path}")
    return 0

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    out = sys.argv[2] if len(sys.argv) > 2 else "docs"
    raise SystemExit(main(target, out))
