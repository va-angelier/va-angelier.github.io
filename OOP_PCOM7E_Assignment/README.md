# OOP_PCOM7E Assignment

This repository contains the system design for a humanoid robot software system, implemented in Python with automated tests and UML diagrams.

## Setup & Dependencies

### 1) Virtual environment (recommended)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2) Install
```bash
pip install -r requirements.txt
```
> `requirements.txt` includes **hypothesis** for property-based testing.

## Project Structure
```
OOP_PCOM7E_Assignment/
├── README.md
├── REPORT.md
├── robot_system.py
├── test_robot_system.py      # unittest discovery will pick this up automatically
└── uml/
    ├── class_diagram.puml
    ├── activity_diagram.puml
    ├── sequence_diagram.puml
    └── state_diagram.puml
```

## Run the CLI
```bash
python robot_system.py
```
Examples:
- `power on`
- `navigate 5,5`
- `pick bottle`
- `speak hello`
- `tick`
- `exit`

## Run Tests (unittest + hypothesis)

### Discovery (recommended)
From the folder containing `robot_system.py` and `test_robot_system.py`:
```bash
python -m unittest -v
# or explicitly:
python -m unittest discover -s . -p "test*.py" -v
```

### Run a single test
```bash
python -m unittest -v test_robot_system.TestRobotSystem.test_charging_returns_to_idle
```

### Module path (if tests are inside a module)
```bash
python -m unittest -v robot_system.TestRobotSystem
```

## VS Code (Pylance / Test discovery)

1) **Select interpreter**
`Ctrl/Cmd + Shift + P` → *Python: Select Interpreter* → choose your `.venv`.

2) **Configure tests**
`Ctrl/Cmd + Shift + P` → *Python: Configure Tests* → **unittest** → pattern `test*.py`.

3) **Fix Pylance “Import could not be resolved”**
- Activate the correct interpreter (step 1).
- Install deps: `pip install -r requirements.txt`.

## Common Issues

- **“Ran 0 tests”**
  - Test filename must start with `test_` (e.g., `test_robot_system.py`).
  - Ensure you run `python -m unittest` **in the correct directory**.
  - In VS Code: verify unittest is configured.

- **“Import ‘hypothesis’ could not be resolved (Pylance)”**
  - venv not active or wrong interpreter selected.
  - Reinstall: `pip install -r requirements.txt`.

## Render UML
- Open `.puml` files via https://www.plantuml.com or the VS Code PlantUML extension.
- Export to PNG/SVG for your report.
