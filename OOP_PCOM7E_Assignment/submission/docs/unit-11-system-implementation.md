# Unit 11 – System Implementation (Commentary)
## Overview

This iteration implements an extensible humanoid-robot controller in Python and documents how the object-oriented (OO) design is realised, tested and measured. The robot package separates concerns into domain entities, services (navigation, planning, events) and a controller façade. Core use-cases—navigating to a waypoint, picking an object, speaking, charging/docking—are executed through a thin CLI (python -m robot). The design maps to the submitted UML (State pattern for controller modes) and is engineered for incremental extension under test.

Run: python -m robot

UML: docs/uml_state.puml
 (PNG export available)

Quality evidence: Radon + Pylint in docs/ (see links below)

## Architecture & Design Patterns

Two behavioural patterns keep decision density local and coupling low:

Strategy encapsulates path-planning variability (AStarPlanner, RRTPlanner) behind a PathPlanner contract. Swapping algorithms does not introduce new conditional branches in the controller.

Observer/EventBus decouples event producers from consumers, reducing temporal coupling and avoiding nested control flow in the orchestration layer.

In addition, dependency injection allows collaborators to be substituted in tests without global state. Where complex mode logic concentrates, the project adopts a State approach (UML provided) to delegate tick() behaviour per mode (Off, Idle, Moving, Charging, etc.). These choices align with well-established design practice (Gamma et al., 1995; Romano and Kruger, 2021).

## Testing & Code Quality

Unit tests cover happy paths and edge cases (timeouts, low battery, blocked paths, manipulation failure). Code quality is measured with Radon and Pylint:

Cyclomatic Complexity (Radon): 139 blocks, average CC = 2.85 (A). One hotspot remains (Robot.tick, E-38) due to mode and error-handling branches; planning classes sit at B/C at worst.

Maintainability Index (Radon): average MI = 77.8, which indicates good maintainability overall.

Pylint: 9.91/10 at the time of submission; remaining warnings in tests are intentionally suppressed (docstrings/reimports/duplicate code) to keep production code strict.

Evidence and how to reproduce:

# From the project root
python -m pip install -r requirements-dev.txt  # if present; otherwise install radon/pylint
python -m radon cc -s -a robot > docs/radon_cc.txt
python -m radon mi -s -a robot > docs/radon_mi.txt
python -m pylint robot > docs/pylint.txt

## Links:

Radon CC: docs/radon_cc.txt

Radon MI: docs/radon_mi.txt

Pylint: docs/pylint.txt

Consolidated report: docs/Code_Quality_Report.md

These measures operationalise McCabe’s (1976) view that decision points correlate with test effort and maintenance risk, while complementary OO reasoning (e.g., keeping class-level WMC/CBO/RFC modest) follows Chidamber and Kemerer (1994).

## Sustainability & Maintainability

In an IoT/edge context, branchy control paths can add latency in tight loops and inflate energy cost. Strategy/Observer reduce control branching and promote cohesion; keeping per-method CC ≤10 supports readability and targeted unit testing. The planned State/Command refactor for the controller will further reduce branching and improve locality, which benefits both maintainability and run-time efficiency.

## Limitations & Next Steps

Controller hotspot: Robot.tick is scheduled for refactor to State/Command with guard clauses and small “extract method” helpers for charging/docking/error recovery. Target: remove the E-rank and bring remaining C-ranks to B/A.

Quality gates: keep MI ≥ 70 per production file, no E/D/C in production code, and Pylint ≥ 8.0.

Metrics breadth (optional): track a small subset of CK indicators (WMC at class level; CBO/RFC at module seams) to complement CC.

How to Run & Contribute
# Windows (venv recommended)
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m robot


Contributions should include unit tests and pass the quality gates above.

## References (Harvard)

Chidamber, S.R. and Kemerer, C.F. (1994) ‘A metrics suite for object-oriented design’, IEEE Transactions on Software Engineering, 20(6), pp. 476–493.
Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1995) Design Patterns: Elements of Reusable Object-Oriented Software. Reading, MA: Addison-Wesley.
McCabe, T.J. (1976) ‘A complexity measure’, IEEE Transactions on Software Engineering, SE-2(4), pp. 308–320.
Romano, F. and Kruger, H. (2021) Learn Python Programming: An In-Depth Introduction to the Fundamentals of Python. 3rd edn. Birmingham: Packt Publishing.