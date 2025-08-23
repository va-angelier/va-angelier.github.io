## Setup & Dependencies

### 1) Virtual environment (recommended)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
2) Install
bashpip install -r requirements.txt

requirements.txt includes hypothesis for property-based testing.

Project Structure
textOOP_PCOM7E_Assignment/
├── README.md
├── REPORT.md
├── robot_system.py
├── test_robot_system.py      # unittest discovery will pick this up automatically
├── assets/                  # Contains CLI screenshot and UML-rendered images
│   ├── cli_screenshot.png
│   └── *.png                # Additional UML images (e.g., pick_activity_diagram.png)
└── uml/
    ├── class_diagram.puml
    ├── pick_activity_diagram.puml    # Updated diagram with swimlanes, guards, exceptions
    ├── activity_diagram.puml         # Original diagram (optional, keep if distinct)
    ├── navigation_activity_diagram.puml  # For navigation use case
    ├── sequence_diagram.puml
    └── state_diagram.puml
Run the CLI
bashpython robot_system.py
Examples:

power on
navigate 5,5
pick bottle
speak hello
tick
exit

Run Tests (unittest + hypothesis)
Discovery (recommended)
From the folder containing robot_system.py and test_robot_system.py:
bashpython -m unittest -v
# or explicitly:
python -m unittest discover -s . -p "test*.py" -v
Run a single test
bashpython -m unittest -v test_robot_system.TestRobotSystem.test_power_management
Module path (if tests are inside a module)
bashpython -m unittest -v test_robot_system.TestRobotSystem
VS Code (Pylance / Test discovery)

Select interpreter
Ctrl/Cmd + Shift + P → Python: Select Interpreter → choose your .venv.
Configure tests
Ctrl/Cmd + Shift + P → Python: Configure Tests → unittest → pattern test*.py.
Fix Pylance “Import could not be resolved”


Activate the correct interpreter (step 1).
Install deps: pip install -r requirements.txt.


Note on New Implementation


The updated robot_system.py implements the pick_activity_diagram.puml with battery checks (< 10%) and timeout handling, tested in test_robot_system.py.

Common Issues

“Ran 0 tests”

Test filename must start with test_ (e.g., test_robot_system.py).
Ensure you run python -m unittest in the correct directory.
In VS Code: verify unittest is configured.


“Import ‘hypothesis’ could not be resolved (Pylance)”

venv not active or wrong interpreter selected.
Reinstall: pip install -r requirements.txt.


Render UML

Open .puml files via https://www.plantuml.com or the VS Code PlantUML extension.
Export to PNG/SVG and save in assets/ for inclusion in REPORT.md.