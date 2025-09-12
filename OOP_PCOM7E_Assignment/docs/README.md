# OOP_PCOM7E – Humanoid Robot System (Python)

This repository contains the system design and reference implementation for a humanoid robot software system, including automated tests and UML diagrams (PlantUML). All documentation lives under docs/.

## Setup
python -m venv .venv
### Windows
.venv\Scripts\activate
### macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
pip install flake8 pytest pytest-cov

## How to run (CLI)
python -m robot  # start interactive CLI
# Examples
# > power on
# > navigate 3,5
# > pick bottle
# > speak hello
# > tick

## Quality & Debug
flake8
pytest -q --cov=robot --cov-report=term-missing   # ~95%
python -m robot

## Architecture overview

**Components:** CLI, Robot Core, Navigation, Manipulator, Communicator, MemoryStore, Environment (sensing/obstacles), Power/Charging.

**Responsibilities:** Orchestration in Robot Core; composition over inheritance; clear separation of concerns.

**Polymorphism (Unit 5):** Navigation uses a PathPlanner Strategy (AStarPlanner default, GreedyPlanner optional), enabling DI in tests without changing Robot.

## UML artefacts

Images are referenced from docs/assets/img/ with captions:

docs/assets/img/class_diagram.png: Class diagram illustrating composition and attributes (Rumbaugh et al., 2005).

docs/assets/img/sequence_diagram.png: Sequence diagram for “pick” command with error and auto-charging branches.

docs/assets/img/activity_navigate.png: Activity diagram for navigation with power and battery guards.

docs/assets/img/activity_pick.png: Activity diagram for object pickup with sensor and grasp logic.

docs/assets/img/activity_errors.png: Activity diagram for error handling (low battery, no path).

docs/assets/img/state_diagram.png: State transition diagram for robot lifecycle, including CHARGING.

docs/assets/img/component_diagram.png: Component diagram showing logical architecture.

docs/assets/img/deployment_diagram.png: Deployment diagram for runtime topology.

docs/assets/img/use_case_diagram.png: Use case diagram defining system scope and actors.

## Module Unit Mapping (evidence)
| Unit | Thema (kort)                               | Wat laten we zien                                      | Waar (bestanden) |
|-----:|--------------------------------------------|--------------------------------------------------------|------------------|
| 1    | OOP & UML-basics                           | Class/Sequence/Activity/State-diagrams                 | `docs/assets/img/*.png`, `uml/*.puml` |
| 2    | Requirements & Use-cases                   | Use-case diagram + CLI-flows                           | `docs/assets/img/use_case_diagram.png`, `robot/robot_system.py` |
| 3    | Abstraction/Encapsulation                  | Cohesieve classes, compositie over overerving          | `robot/robot_system.py` |
| 4    | Design principles (SRP, DIP, OCP)          | Injecteerbare planner (Strategy), losse concerns       | `robot/robot_system.py`, `robot/tests/test_polymorphism.py` |
| 5    | Polymorphism                               | `PathPlanner` Strategy (`AStarPlanner`, `GreedyPlanner`)| `robot/tests/test_polymorphism.py` |
| 6    | Algorithms & Search                        | A* (heuristic), obstakel-checks                        | `robot/robot_system.py` (Navigation) |
| 7    | Debugging, Error handling & Data structures| Guards/ERROR/CHARGING, List/Dict/Stack/Queue, tests    | `robot/robot_system.py`, `robot/tests/*.py`, coverage ~95% |
Dit is compact, leesbaar, en verwijst direct naar je artefacten.

## Repo layout
OOP_PCOM7E_Assignment/
├─ docs/
│  ├─ index.md
│  ├─ README.md
│  ├─ REPORT.md
│  ├─ CHANGELOG.md
│  └─ assets/img/*.png
├─ robot/
│  ├─ __init__.py
│  ├─ __main__.py
│  ├─ robot_system.py
│  └─ tests/*.py
└─ uml/*.puml

## Testing
pytest -q --cov=robot --cov-report=term-missing
# Expect: all tests pass, coverage ~95% (robot package)

## Reproducibility

OS: macOS; Python 3.12.x (Anaconda OK).

Commands: see “Setup”, “Quality & Debug” above.

Outputs (latest): all tests passed, coverage 95%.