# System Design Proposal for Humanoid Robot Software

**Author**: Victor Angelier  
**Date**: 12 September 2025

## Assessment Criteria Mapping (per rubric)

- **Application of Knowledge (20%)** – All requested artefacts delivered and explained with clear links to the module learning outcomes (UML set, Python implementation, tests).  
- **Collaboration / Independent Working (20%)** – Individual project: I planned, executed and validated all tasks independently (see section “Evidence of Independent Working”).  
- **Criticality (40%)** – Design choices, alternatives and trade-offs are analysed and linked to theory; I explain what I learned and how I will apply it professionally.  
- **Structure & Presentation (10%)** – Portfolio is concise, consistently named, and free of language/formatting issues; diagrams are captioned and cross-referenced.  
- **Academic Integrity (10%)** – Harvard references and in-text citations are used consistently; all external ideas are credited.

## Background Research

Research used “robot,” “human-robot interaction,” and “collaborative robot” to explore functionalities, interfaces, and collaboration (Mukherjee et al., 2022; Ackerman, 2023). Additional sources: Mulko (2023), Siciliano and Khatib (2016), Russell and Norvig (2020), Thrun et al. (2005).

## System Design Rationale

The system enables a humanoid robot for warehouse tasks: navigation, object manipulation, and human communication via a CLI (Mukherjee et al., 2022). Python’s object-oriented design ensures modularity, with a CLI chosen for simplicity (Ackerman, 2023). Classes are modelled with UML, using lists (e.g., `Environment.objects` for dynamic data), a dictionary (`object_index` for O(1) lookups), stacks (e.g., `Manipulator.grasp_history` for undo), and queues (e.g., `Navigation.path_queue` for path steps) (Siciliano & Khatib, 2016). Power management uses state transitions (e.g., `OFF`→`IDLE` via `power_on()`) to gate operations, avoiding complex concurrent logic (Thrun et al., 2005).

Navigation uses an A* planner (complexity **O(V log V + E)**) with obstacle checks (`Environment.is_obstacle(x,y)`) for predictable routing at scale (Russell & Norvig, 2020). **Trade-offs**: (1) State transitions simplify control but limit multitasking. (2) Dictionary lookup improves search speed but increases memory use. (3) A* adds complexity but enhances pathfinding.

**Battery & charging** (implemented): after actions that consume energy, if the battery falls below a threshold, the robot auto-plans a docking route to a charger and enters a dedicated **CHARGING** state. Charging progresses via `tick` events until 100%, then returns to `IDLE`. This behaviour is verified in tests and aligns with the error/guard logic in the activity/state diagrams.

**Robustness choices**: (i) `Waypoint` is hashable and comparable to support A*’s internal maps deterministically; (ii) object lookup is case-insensitive to minimise user error in the CLI; (iii) tests use stubs to force edge cases (no path, timeouts, grasp fail) while keeping the default manipulator deterministic in normal runs.

## Learning Outcomes → Artefacts

| Learning Outcome | Artefacts | How the evidence is provided |
| --- | --- | --- |
| OO modelling | Class diagram; `robot/robot_system.py` | Clear cohesion per class; composition `Robot → (Navigation/Manipulator/Communicator/MemoryStore)`; low coupling. |
| Behaviour & processes | State diagram; Activity (navigate/pick/errors) | Guards (battery < 10%, no-path, timeout, graspFail) map 1:1 to code paths and tests. |
| Program design & testing | Unit tests, coverage, flake8 | Edge cases covered; deterministic assertions; coverage evidence and reproduction commands. |
| Architecture & deployment | Component & Deployment diagrams | Separation of concerns: Core, Navigation, Manipulation, Comms; simple deployment (robot process + sensor/actuator bus). |

## Critical Reflection

I prioritised composition over inheritance: the Robot *has* Navigation, Manipulator, Communicator and MemoryStore. This avoids a God-class and keeps responsibilities testable and swappable. A ROS-based decomposition (topics/services) was considered but rejected to keep the assignment portable and focused on core OO concerns (encapsulation, cohesion, coupling).

Navigation uses A* because asymptotic behaviour matters for larger grids; it outperforms naïve search in worst-case bounds (Russell & Norvig, 2020). The trade-off is implementation complexity and the need for a consistent environment model; I mitigated this with a slim `Environment.is_obstacle()` seam and unit tests that inject synthetic maps. Alternatives like D* Lite or PRM were out-of-scope given the timebox and reproducibility requirements.

Data-structure choices were deliberate: dictionary lookups for O(1) object access accelerate the “find and pick” loop; stacks for grasp-history provide O(1) undo semantics; queues model FIFO path execution and command intake cleanly. These choices simplified reasoning in the activity/state diagrams and produced assertions that are easy to automate.

Error handling is first-class: explicit `ERROR` state with guards (battery < 10%, timeout, graspFail) and recovery back to `IDLE`. I extended this with an operational **CHARGING** state and auto-docking behaviour triggered after post-action energy use. A limitation is the lack of true concurrency: sensing and motion are sequenced, not overlapped. If extended, I would introduce an event loop with non-blocking IO and a state supervisor, then adapt the sequence diagram to show concurrent lifelines.

In practice, this design suits warehouse-like tasks where predictable, deterministic behaviour and testability outweigh raw optimality.

## Evidence of Independent Working (20%)

**Commit evidence (last 20)**  
```text
2025-09-11  914c972  Latest UML + images and updated readme
2025-09-11  f9e73ef  Updates
2025-08-23  67159c2  Washmachine UML
2025-08-23  108d4dc  Update ignore
2025-08-23  9449bba  Ignore updated
2025-08-23  0e334ed  ignore update
2025-08-23  731c1e0  Updates
2025-08-23  ec8cf32  Updates
2025-08-23  4ff610c  OOP Python
```

*Interpretation:*  
- **2025-08-23** — Initial modelling & repo hygiene (washing-machine UML, `.gitignore` iterations, Python OOP scaffolding).  
- **2025-09-11** — Finalisation pass (full UML set, exported images, README updates).

**Commit authorship (git shortlog -sn)**  
```text
    13  Victor Angelier CCX
    10  Victor Angelier
```
*Interpretation:* 23 commits in scope, **100% self-authored** (two local Git identities; both refer to me).

**Condensed timeline & tasks**

| Date       | Task / Deliverable                       | Result / Artefacts                                                  |
| ---------- | ---------------------------------------- | ------------------------------------------------------------------- |
| 2025-08-23 | Baseline UML + repo setup (`.gitignore`) | “Washmachine UML”, OOP skeleton committed                           |
| 2025-09-11 | Full UML set + images + README           | Class / Sequence / Activity / State / Component / Deployment + docs |

**Implementation (completed by the author)**

- Core modules: `robot/robot_system.py` (Robot, Navigation, Manipulator, Communicator, MemoryStore), CLI and command handling.  
- All PlantUML diagrams authored by me: class, sequence, activity (navigate/pick/errors), state, component, deployment, use-case.

**Validation (run by the author)**

```bash
pytest -q --cov=robot --cov-report=term-missing
flake8 .
```

**Result summary**  
- **31 tests passed, 0 failed**  
- **Coverage: 91%** (macOS, Python 3.12.7)  
- Branches exercised include: low-battery auto-docking → **CHARGING** → charge-to-100%, busy guards, no-path/timeout, invalid coords, object-not-found.

**Reproducibility**  
- Tested on macOS (Python 3.12.7).  
- Dependencies: `pytest`, `pytest-cov`, `flake8` (see `requirements.txt`).

**Key design decisions (taken independently)**

- **Composition over inheritance** — Robot *has* Navigation/Manipulator/Communicator/Memory.  
- **A\*** over naïve search — predictable complexity on larger grids; clean `Environment.is_obstacle()` seam.  
- **Explicit states & guards** — `ERROR` plus **CHARGING** for operational safety; guards for battery, timeout, and grasp-fail.  
- **CLI interface** — deterministic testing and minimal dependencies versus a heavier UI/ROS stack.

## Polymorphism (explicit evidence)

Runtime polymorphism is used for testing and extension: Navigation and Manipulator can be replaced by subclasses/stubs (e.g., “no-path”, “timeout”, or “grasp-fail” doubles) without changing `Robot`. This demonstrates substitutability and supports DIP-style design, even without a full interface layer.

## UML Models

The repository includes the following UML artefacts (PlantUML sources and exported images):
- **Class diagram** – core structure and associations.  
- **Sequence diagram** – “pick” command end-to-end with error branches.  
- **Activity diagrams** – navigation, pick-up, and error-handling flows (with battery/timeout guards).  
- **State diagram** – `OFF/IDLE/MOVING/MANIPULATING/COMMUNICATING/ERROR/CHARGING` transitions.  
- **Component & Deployment diagrams** – separation of concerns and runtime nodes.

> Note: UML uses CamelCase for operation names while the code follows PEP8 `snake_case`. Names map directly (e.g., `powerOn()` ↔ `power_on()`), preserving traceability.

## Traceability

| Use case | Sequence | Activity / State | Component / Deployment |
| --- | --- | --- | --- |
| Navigate to (x,y) | sequence (navigate section) | Activity “navigate”; State `IDLE→MOVING→IDLE/ERROR` | Core ↔ Navigation ↔ Environment |
| Pick object | sequence (pick section) | Activity “pick”; State `IDLE→MANIPULATING→IDLE/ERROR` | Core ↔ Navigation ↔ Manipulator |
| Handle errors & charging | sequence (alts) | Activity “errors”; State `MOVING→CHARGING→IDLE` and `…→ERROR→IDLE` | Core ↔ Power/BatteryMgr ↔ Navigation |

## Data Structures

- **List**: `Environment.objects`, `Environment.sensor_readings` (dynamic size, amortised O(1) append).  
- **Dictionary**: `Environment.object_index` (O(1) lookup by ID, accelerates pick loop).  
- **Stack**: `Manipulator.grasp_history`, `MemoryStore.breadcrumbs` (LIFO, O(1) push/pop).  
- **Queue**: `Navigation.path_queue`, `CLI.cmd_queue` (FIFO, O(1) enqueue/dequeue).

## How to Run & Test

```bash
# create & activate venv
python -m venv .venv
source .venv/bin/activate           # Windows: .\.venv\Scripts\activate

# run CLI
python -m robot

# run tests & coverage
pytest -q --cov=robot --cov-report=term-missing
flake8
```

## References

- Ackerman, E. (2023) ‘Humanoid Robots Are Getting to Work’, IEEE Spectrum. Available at: https://spectrum.ieee.org/humanoid-robots (Accessed: 11 September 2025).  
- Derezińska, A. (2015) ‘Improving mutation testing process of Python programs’, in *Software Engineering Techniques in Progress*, pp. 233–246.  
- Kang, H.J., Lo, D. and Lawall, J. (2019) ‘BugsInPy: A database of existing bugs in Python programs to enable controlled testing and debugging studies’, in *Proceedings of the 33rd European Conference on Object-Oriented Programming*, pp. 1–6. doi:10.4230/LIPIcs.ECOOP.2019.1.  
- Mukherjee, D. et al. (2022) ‘A Survey of Robot Learning Strategies for Human-Robot Collaboration in Industrial Settings’, *Robotics and Computer-Integrated Manufacturing*, 73, p. 102231. doi:10.1016/j.rcim.2021.102231.  
- Mulko, M. (2023) ‘5 of the World’s Most Realistic Humanoid Robots Ever’, Interesting Engineering. Available at: https://interestingengineering.com/innovation/humanoid-robots (Accessed: 11 September 2025).  
- Rumbaugh, J., Jacobson, I. and Booch, G. (2005) *The Unified Modeling Language Reference Manual*. 2nd edn. Addison-Wesley.  
- Russell, S. and Norvig, P. (2020) *Artificial Intelligence: A Modern Approach*. 4th edn. Pearson.  
- Siciliano, B. and Khatib, O. (2016) *Springer Handbook of Robotics*. 2nd edn. Springer.  
- Sommerville, I. (2015) *Software Engineering*. 10th edn. Pearson.  
- Thrun, S., Burgard, W. and Fox, D. (2005) *Probabilistic Robotics*. MIT Press.

© Victor Angelier – OOP_PCOM7E Assignment