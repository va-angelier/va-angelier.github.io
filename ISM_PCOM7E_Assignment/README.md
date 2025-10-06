# Attack Tree Visualiser (Python) — SolarWinds Case Study

> Quantify and visualise cyber risk using attack trees with DREAD-based probabilities and financial impact aggregation. Built for the **Executive Summary & App Presentation** assessment (UoE ISMS Units 4–6).

---

## Overview

This tool ingests an **attack tree specification** (JSON or YAML), visualises the tree, and **aggregates** leaf-node probabilities and monetary impacts to an **expected loss** at the root.
It supports two scenarios out of the box:

* **Pre-mitigation** (original system)
* **Post-mitigation** (after recommended digitalisation controls)

The provided example models the **SolarWinds/SUNBURST** supply-chain compromise.

---

## Key Features

* **Input formats:** JSON and YAML attack trees.
* **DREAD → probability:** Optional `dread` block on leaf nodes; app computes `p = mean(D,R,E,A,Discover)/10` (clamped to `[0.01, 0.99]`).
* **Aggregation:**

  * **AND** nodes: probability = product of child `p`; impact = sum of child impacts.
  * **OR** nodes: probability = `1 − ∏(1 − p_i)`; impact = max of child impacts.
  * Root **expected loss** = `p × impact`.
* **Visualisation:** ASCII tree, Graphviz **DOT** (and PNG via `dot`), or **Matplotlib PNG** fallback (no Graphviz required).
* **CLI-first design:** Clean, reproducible outputs for screenshots and submission.
* **Quality:** Documented, type-hinted, linted (`pylint`) and ready for tests (`pytest`).

---

## Installation

> Use a virtual environment.

### Windows (PowerShell)

```powershell
cd "<your-project-root>"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
cd "<your-project-root>"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Optional: Graphviz (for DOT → PNG)

* Install Graphviz from the official packages (ensure `dot` is on your PATH).
* Verify:

```bash
dot -V
```

If Graphviz is unavailable, use the Matplotlib renderer (`--renderer matplotlib`).

---

## Quick Start

### 1) Run the CLI with examples (ASCII output)

```bash
python -m attacktree.cli --input examples/solarwinds_pre_dread.json --ascii
python -m attacktree.cli --input examples/solarwinds_post_dread.json --ascii
```

### 2) Compare scenarios and write JSON results

```bash
mkdir -p outputs
python -m attacktree.cli \
  --compare examples/solarwinds_pre_dread.json examples/solarwinds_post_dread.json \
  --out outputs/solarwinds_compare.json --ascii
```

### 3) Produce DOT and PNG diagrams

**Graphviz (recommended layout)**

```bash
# single scenario
python -m attacktree.cli --input examples/solarwinds_pre_dread.json --dot outputs/pre --render outputs/pre.png

# compare (produces *_pre.* and *_post.*)
python -m attacktree.cli \
  --compare examples/solarwinds_pre_dread.json examples/solarwinds_post_dread.json \
  --dot outputs/solarwinds --render outputs/solarwinds
```

**Without Graphviz (Matplotlib fallback)**

```bash
pip install matplotlib
python -m attacktree.cli \
  --compare examples/solarwinds_pre_dread.json examples/solarwinds_post_dread.json \
  --dot outputs/solarwinds --render outputs/solarwinds --renderer matplotlib
```

---

## Command Line Interface

```bash
python -m attacktree.cli --help
```

Common options:

* `--input PATH` … single scenario file (JSON/YAML).
* `--compare PRE POST` … compare two files.
* `--ascii` … print the annotated tree to stdout.
* `--out FILE.json` … write aggregation/compare JSON to file.
* `--dot PREFIX` … write Graphviz DOT (e.g., `PREFIX.dot` or `PREFIX_pre.dot`/`_post.dot`).
* `--render PATH[.png]` … render PNG(s). With `--compare`, renders `_pre.png` and `_post.png`.
* `--renderer {graphviz,matplotlib}` … select PNG renderer (default `graphviz`).

> The CLI automatically creates parent directories for `--out` if they do not exist.

---

## Input Format

### Minimal JSON (leaf with explicit probability/impact)

```json
{
  "id": "root",
  "label": "Example",
  "type": "OR",
  "children": [
    { "id": "phish", "label": "Phishing", "type": "LEAF", "probability": 0.4, "impact": 10000 }
  ]
}
```

### With DREAD (probability derived automatically)

```json
{
  "id": "phish",
  "label": "Phishing",
  "type": "LEAF",
  "dread": { "damage": 7, "repro": 6, "exploit": 5, "affected": 6, "discover": 7 },
  "impact": 10000
}
```

* If `probability` is **absent or invalid**, it is computed from `dread`.
* If `probability` is **present and valid**, it **takes precedence** by default (you can invert this behaviour in `NodeFactory.from_dict` if desired).

---

## Example Datasets (included)

* `examples/solarwinds_pre_dread.json`
* `examples/solarwinds_post_dread.json`

These encode the **SolarWinds/SUNBURST** scenario with DREAD blocks on leaf nodes and monetary impacts on consequence leaves. They produce:

* **Pre**: `p ≈ 0.9992`, impact `£750,000`, expected loss `£749,384.70`.
* **Post**: `p ≈ 0.9590`, impact `£300,000`, expected loss `£287,707.40`.
* **Reduction**: `−£461,677.30` (≈ `−61.6%`).

Use these for screenshots and verification.

---

## Project Structure

```
attacktree/
  __init__.py
  cli.py                 # command-line interface
  nodes.py               # Node, LeafNode, AndNode, OrNode
  aggregation.py         # Aggregation strategies (e.g., BasicAggregation)
  factory.py             # NodeFactory (JSON/YAML parsing, DREAD mapping)
  renderers.py           # ASCII and Graphviz DOT renderers
  streamlit_app.py       # optional UI (if included)
examples/
  solarwinds_pre_dread.json
  solarwinds_post_dread.json
outputs/                 # created at runtime for PNG/JSON results
```

---

## Development, Linting, and Tests

### Lint (pylint)

```bash
pip install pylint
python -m pylint attacktree
```

* Target score: **≥ 9.5/10** (project tuned for ~9.8/10).

### Tests (pytest)

```bash
pip install pytest
pytest -q
```

> Include screenshots of the CLI output, PNGs, and linter report in your submission ZIP.

---

## Troubleshooting

* **`Graphviz 'dot' not found`**
  Install Graphviz and ensure `dot` is on PATH, or use `--renderer matplotlib`.

* **`FileNotFoundError: .../outputs/*.json`**
  Create the folder (`mkdir outputs`) or rely on CLI’s auto-folder creation (enabled in this project).

* **PowerShell script not running (Windows)**
  Run PowerShell as Administrator and:
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

* **Encoding paths on Windows**
  Avoid special characters in paths or run from a simple directory (e.g., `C:\projects\attacktree`).

---

## Design Notes

* **DREAD mapping**: `p = mean(D,R,E,A,Discover)/10`, clamped to `[0.01, 0.99]`.
* **Aggregation**: AND = product/ sum; OR = `1 − ∏(1 − p)` / max.
* **Interpretation**: Results are **scenario estimates**; consider sensitivity analysis (e.g., Monte Carlo) for uncertainty bounds.

---

## Academic References (Harvard style)

Delinea. (2023) *SolarWinds Sunburst: A supply chain cyberattack reshapes the software industry*. Available at: [https://delinea.com/blog/solarwinds-sunburst-supply-chain-cyber-attack-software-industry](https://delinea.com/blog/solarwinds-sunburst-supply-chain-cyber-attack-software-industry) (Accessed: 15 June 2025).
ENISA. (2023) *ENISA Threat Landscape 2023*. Available at: [https://www.enisa.europa.eu/publications](https://www.enisa.europa.eu/publications) (Accessed: 6 October 2025).
ISO/IEC. (2022) *ISO/IEC 27005:2022 Information Security, Cybersecurity and Privacy Protection – Guidance on Managing Information Security Risks*. International Organization for Standardization.
Kordy, B., Mauw, S., Radomirovic, S. and Schweitzer, P. (2014) ‘Attack trees and attack–defence trees’, *Journal of Logic and Computation*, 24(1), pp. 55–87.
NIST. (2012) *SP 800-30 Rev. 1 – Guide for Conducting Risk Assessments*. National Institute of Standards and Technology.
Reuters. (2021) *China exploited SolarWinds flaw, as well as Russians, sources say*. Available at: [https://www.reuters.com/article/us-cyber-solarwinds-china-exclusive-idUSKBN2A22K8](https://www.reuters.com/article/us-cyber-solarwinds-china-exclusive-idUSKBN2A22K8) (Accessed: 15 June 2025).
Schneier, B. (1999) ‘Attack Trees’, *Dr Dobb’s Journal*, 24(12), pp. 21–29.
SolarWinds. (2021) *New Findings From Our Investigation of SUNBURST*. Available at: [https://www.solarwinds.com/blog/new-findings-from-our-investigation-of-sunburst](https://www.solarwinds.com/blog/new-findings-from-our-investigation-of-sunburst) (Accessed: 16 June 2025).
TechTarget. (2021) *SolarWinds hack explained: Everything you need to know*. Available at: [https://www.techtarget.com/whatis/feature/SolarWinds-hack-explained-Everything-you-need-to-know](https://www.techtarget.com/whatis/feature/SolarWinds-hack-explained-Everything-you-need-to-know) (Accessed: 15 June 2025).
Temple-Raston, D. (2021a) *The SolarWinds Attack: The Untold Story*. NPR. Available at: [https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack](https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack) (Accessed: 17 June 2025).
Temple-Raston, D. (2021b) *The SolarWinds Attack: The Story Behind the Hack*. NPR. Available at: [https://www.npr.org/2021/04/20/989015617/the-solarwinds-attack-the-story-behind-the-hack](https://www.npr.org/2021/04/20/989015617/the-solarwinds-attack-the-story-behind-the-hack) (Accessed: 17 June 2025).

---

## Licence & Acknowledgements

* Source code © You (student author).
* Graphviz is © AT&T/Graphviz authors (licences apply).
* This project is an academic artefact for the University of Essex ISMS Units 4–6 assessment.
