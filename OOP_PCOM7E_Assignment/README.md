# OOP_PCOM7E – Humanoid Robot System (Python)

This repository contains the system design and reference implementation for a humanoid robot software system, including automated tests and UML diagrams (PlantUML).

## Setup
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
pip install flake8 pytest pytest-cov

# How to run
python -m robot.cli --help
# Examples
python -m robot.cli "power on"
Debug: Powering on
Power on: True
python -m robot.cli "navigate 3,5"
Debug: Processing command {'type': 'navigate', 'args': '3,5'}
Debug: Planning path from 0,0 to 3,5
Debug: Path found
Navigating to (0, 1)
python -m robot.cli "pick cup"
> pick cup
Debug: Processing command {'type': 'pick', 'args': 'cup'}
Debug: Searching for object of kind cup
ERROR: Object not found


## Architecture overview

Key components: CLI, Command Parser, Robot Core, Navigation, Manipulator, Communicator, MemoryStore, Power/Battery.

Key responsibilities: Orchestration in Robot Core; composition over inheritance; clear separation of concerns.

## UML artefacts

All diagrams are under /assets/img (PNG) and /uml (PUML)

class_diagram.png – domain model

sequence_diagram.png – command flow (navigate & pick)

navigation_activity_diagram.png – activity flow with lanes

activity-diagram-pickup.png & activity-diagram-errors.png

state_diagram.png – Robot lifecycle (OFF/IDLE/MOVING/…)

component_diagram.png – logical architecture

deployment_diagram.png – runtime topology

use_case_diagram.png – scope & actors