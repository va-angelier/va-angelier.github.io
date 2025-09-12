## Design Rationale (≈500 words, UK English)

**Goal & scope.** The system provides a command‑line interface (CLI) for a humanoid robot to execute three core capabilities: navigation to grid targets, object manipulation (“pick <kind>”), and human‑facing communication (“speak <text>”). An environment model supplies obstacles, objects, and sensor readings. The design prioritises correctness (valid state transitions), maintainability (clear separation of concerns), and testability (deterministic flows and explicit error paths).

**Architecture & separation of concerns.** The core follows composition over inheritance. A single `Robot` **orchestrator** owns cohesive components: `Navigation` (A* path planning), `Manipulator` (grasp operations with history), `Communicator` (speech/display façade), `Environment` (objects/obstacles/sensors), and `MemoryStore` (breadcrumbs/facts). System state is captured by `RobotState` (an enum) with explicit lifecycle values: `OFF`, `IDLE`, `MOVING`, `MANIPULATING`, `COMMUNICATING`, `CHARGING`, `ERROR`. This organisation minimises coupling and enables **dependency substitution** in tests by replacing components with stubs (e.g., “no path”, “timeout”, “grasp fail”).

**States, guards, and safety.** Guards enforce operational safety and predictability. Commands are rejected when the robot is `OFF`, and any command other than `tick` is refused during `CHARGING`. After energy‑consuming actions, a **low‑battery guard** triggers **auto‑docking**: the robot plans a route to a charger and transitions from `MOVING` to `CHARGING` upon arrival. Charging progresses via periodic `tick` calls until the battery reaches **100%**, after which the robot returns to `IDLE`. These flows mirror the activity/state diagrams and are covered by unit tests (including “navigate during charging” and “no path to target”).

**Algorithms & data structures.** Navigation uses an A*‑style planner on a 4‑connected grid, with complexity **O(V log V + E)** and an admissible heuristic based on Euclidean distance. Obstacles are abstracted through `Environment.is_obstacle(x, y)`, allowing tests to inject maps and edge conditions. Data structures are purposeful: a **Queue** buffers CLI commands; **Lists** hold `Environment.objects` and `sensor_readings`; a **Dictionary** (`object_index`) provides O(1) object lookup by ID; and **Stacks** back action history (`MemoryStore.breadcrumbs`) and grasp history (`Manipulator.grasp_history`). Object search by kind is case‑insensitive for a better CLI experience.

**Determinism & testability.** The implementation avoids non‑determinism in core behaviours. `Manipulator.pick()` is deterministic by default; failure scenarios are tested through explicit stubs. `Environment.sense()` records sensor noise while maintaining stable, reachable object positions (never moving onto obstacles), ensuring reproducible tests. The `tick` command advances long‑running operational flows (auto‑docking and charging), which keeps behaviour scriptable and easy to assert.

**Error handling & UX.** The CLI returns stable, human‑readable status strings rather than raising exceptions. Typical responses include: “ERROR: Robot is off”, “ERROR: Low battery – please charge”, “ERROR: No path to target”, and “OK: Picked object”. This decision simplifies scripting and keeps tests focused on observable outcomes. Because the state machine is explicit, both success and error paths are documented in the sequence/activity diagrams and validated by unit tests.

**SDLC alignment.** 
- *Requirements*: expose user‑visible operations (power, navigate, pick, speak; auto‑charge when needed).  
- *Design*: model structure and behaviour with UML (class/sequence/activity/state) and specify guards/invariants.  
- *Implementation*: translate the model into cohesive Python classes with PEP‑8 naming and minimal dependencies.  
- *Testing*: derive scenarios from state transitions and sequence alternatives (low battery after action, timeout, busy during charging).  
- *Maintenance*: component boundaries and the explicit state machine make extensions predictable (e.g., alternate planners or richer manipulation), while tests act as a regression harness.

**Trade‑offs.** An explicit state machine is more verbose than ad‑hoc flags, but it gives stronger guarantees and clear recovery paths. Using in‑memory Lists/Stacks/Queues keeps the system lightweight and within scope; persistent storage or alternative planners can be introduced later without breaking the CLI contract. The CLI favours simplicity and determinism over a richer GUI.

**Conclusion.** The combination of a clear state model (`RobotState` incl. `CHARGING`), disciplined component boundaries, and purpose‑chosen data structures yields a design that is safe, testable, and extensible—fully aligned with the assignment objectives and the implemented code.

© Victor Angelier – OOP_PCOM7E Assignment