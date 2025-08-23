# OOP_PCOM7E — Humanoid Robot (baseline)

UML (class, activity, sequence, state) + Python-implementatie met A* path planning,
CLI, en low battery charging (terug naar **IDLE** bij ≥95%).

## Quick start
```bash
pip install -r requirements.txt
python -m unittest -v
python robot_system.py

## CLI voorbeelden:

power on
navigate 5,5
pick bottle
speak hello
tick        # laat opladen vorderen in CHARGING
exit

## How to run

```bash
python -m unittest -v
python OOP_PCOM7E_Assignment/robot_system.py

# Robot diagrams
plantuml -tpng OOP_PCOM7E_Assignment/uml/*.puml
# Washing machine (e-portfolio)
plantuml -tpng ePortfolio_Unit4/uml/washing_machine_state.puml