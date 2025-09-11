## Design Rationale (≈500 words, UK English)

**Goal & scope.** The system provides a command-line interface (CLI) for a humanoid robot to execute three core operations (e.g., power cycle, navigate, charge), while a background component simulates environmental attributes (e.g., battery state-of-charge, sensor events). The design emphasises correctness (valid state transitions), maintainability (clear separation of concerns), and testability (deterministic command processing and explicit error paths).

**Architecture & separation of concerns.** The core is divided into: (1) a `RobotService` façade that exposes high-level operations, (2) a `StateMachine`/`RobotState` that governs valid transitions (IDLE, MOVING, CHARGING, ERROR), (3) domain components such as `BatteryManager` and `MotionController`, and (4) an event/sensor layer that records observations. This separation reduces coupling, clarifies responsibility boundaries, and allows components to evolve (e.g., replacing `BatteryManager` without altering the CLI). It also enables dependency injection in tests.

**States, guards, and safety.** The state model encodes the lifecycle and safety constraints. For example, `low_battery` triggers a transition to `CHARGING`, which automatically returns to `IDLE` once SoC ≥ 95%. Guards enforce invariants: attempting `navigate` while `CHARGING` is rejected with a specific error; similarly, movement requires `power_on`. Modelling these edges in UML (activity/state diagrams) improves reasoning about recovery and makes failure modes explicit, which in turn supports regression testing.

**Data structures and search.** Three data structures are used deliberately. A FIFO **Queue** buffers CLI commands for deterministic processing (one command per `tick`), making behaviour reproducible under test. A **List** holds `sensor_events` (timestamped dictionaries) for auditing and inspection. A LIFO **Stack** supports undo of recent user-level actions (e.g., last `navigate`), which is valuable for maintenance and experimental control. A simple **linear search** over `sensor_events` suffices at this scale (clarity over micro-optimisation). If the event volume grows, an indexed or time-partitioned store can be introduced without changing the external interface.

**Error handling & user experience.** The CLI maps domain exceptions (`PowerOffError`, `BusyChargingError`, `InvalidCommandError`) to stable exit codes and human-readable messages. This improves the learning curve and supports scripting. Activity/sequence diagrams include both success and error paths, making expected behaviour transparent.

**SDLC alignment.** 
- *Requirements*: identify user-visible operations (power, navigate, charge) and the need for environmental simulation.  
- *Design*: capture structure and behaviour with UML (class, sequence, activity, state) and document invariants/guards.  
- *Implementation*: translate the class diagram to Python modules with cohesive classes and explicit interfaces.  
- *Testing*: derive unit and integration tests from state transitions and sequence steps (including edge cases such as “navigate during charging”).  
- *Maintenance*: the state model and modular boundaries make extensions predictable (e.g., add `AVOIDING` for obstacle handling or a new `Sensor` type), while tests act as a regression harness.

**Trade-offs.** An explicit state machine is more verbose than ad-hoc flags, but it provides stronger guarantees and clearer failure handling. Using in-memory List/Stack/Queue keeps the solution lightweight and within scope; persistent storage or indexing can be added later without breaking the CLI contract. The CLI prioritises simplicity and assessment requirements over a rich UI.

**Conclusion.** The combination of a clear state model, disciplined component boundaries, and purposeful data structures yields a design that is safe, testable, and extensible, directly supporting the assignment’s objectives.
