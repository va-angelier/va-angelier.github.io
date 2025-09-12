# OOP_PCOM7E – Humanoid Robot System (Python)

This repository contains the **system design** and a **reference implementation** for a humanoid robot software system, including automated tests and UML diagrams (PlantUML).

## Project structure
```
.
├─ robot/
│  ├─ __init__.py
│  ├─ __main__.py          # entrypoint → run with: python -m robot
│  ├─ robot_system.py      # core implementation
│  └─ tests/               # unit tests (pytest)
├─ uml/                    # .puml sources (if included)
└─ assets/img/             # exported UML images (png)
```

## Setup
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
pip install flake8 pytest pytest-cov
```

## How to run (CLI)
Start the interactive CLI from the **repo root**:
```bash
python -m robot
```

## Examples (interactive session):
```
Humanoid Robot CLI: Type commands (e.g., 'navigate 5,5', 'pick bottle', 'speak hello', 'power on/off', 'tick', 'exit')
> power on
Power on: True
> navigate 3,5
Navigating to (0, 1)
> pick bottle
ERROR: Object not found
> speak hello
OK: Spoken
> exit
```

> Tip: For a quick demo of `pick`, add a sample object at startup (optional):
> ```python
> # in main(), right after robot = Robot("R1")
> robot.env.objects.append(EnvObject("bottle", "b1", Waypoint(1, 1)))
> robot.env.object_index["b1"] = robot.env.objects[-1]
> ```

## Testing & Quality
Run the test suite and coverage:
```bash
pytest -q --cov=robot --cov-report=term-missing
flake8
```

## REPORT – Result summary
```markdown
**Result summary** — 32 tests passed, 0 failed; Coverage **91%**.  
Branches exercised: low-battery auto-dock → **CHARGING** → charge-to-100%, busy guards, no-path/timeout, invalid coords, object-not-found.


## Architecture overview
- **Core**: `Robot` orchestrates **Navigation**, **Manipulator**, **Communicator**, **MemoryStore**, using **composition** for low coupling.
- **Navigation**: grid-based A* with obstacles (`Environment.is_obstacle`), queue of waypoints for execution.
- **Manipulator**: simple pick with grasp history (stack) for undo semantics in tests.
- **Power**: explicit guards for low battery; **auto-docking** followed by a dedicated **CHARGING** state until 100%.
- **CLI**: minimal, deterministic command interface (“navigate x,y”, “pick kind”, “speak text”).
- **Data structures**: list/dict/stack/queue chosen for clarity and algorithmic complexity.

## UML artefacts
PlantUML sources and exported images:
- **Class diagram** – domain model (`assets/img/class_diagram.png`)
- **Sequence diagram** – command flow (“navigate” & “pick”) (`assets/img/sequence_diagram.png`)
- **Activity diagrams** – navigation / pick / errors (`assets/img/navigation_activity_diagram.png`, `assets/img/activity_diagram-pickup.png`, `assets/img/activity_diagram-errors.png`)
- **State diagram** – lifecycle (`assets/img/state_diagram.png`)
- **Component diagram** – logical architecture (`assets/img/component_diagram.png`)
- **Deployment diagram** – runtime topology (`assets/img/deployment_diagram.png`)
- **Use case diagram** – scope & actors (`assets/img/use_case_diagram.png`)

> Naming in UML (CamelCase) maps directly to code (PEP8 snake_case), e.g. `powerOn()` ↔ `power_on()`.

## Commands (cheatsheet)
- `power on` / `power off`
- `navigate x,y`
- `pick <kind>`
- `speak <text>`
- `tick` *(progress docking/charging when applicable)*
- `exit`

## Reproducibility
- OS: macOS (tested), should be portable to Linux/Windows.
- Python: 3.12+ recommended.
- Dependencies: `pytest`, `pytest-cov`, `flake8`, PlantUML for diagram rendering.

---
© Victor Angelier – OOP_PCOM7E Assignment
