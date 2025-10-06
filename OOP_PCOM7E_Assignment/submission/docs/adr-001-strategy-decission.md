# ADR 0001 — Interaction/control architecture
**Context.** We need clear seams for swapping planners and testing; control flow currently centralised in `Robot.tick`.

**Options.** (A) Layered + Strategy (current); (B) Layered + Strategy + State (planned); (C) Hexagonal/Ports–Adapters + State.

**Decision.** Adopt (B): maintain layers and Strategy; incrementally move control into State objects to reduce complexity and expose ports later if needed.

**Consequences.** Lower cyclomatic complexity locally; easier test seams; later migration path to hexagonal if integrating external adapters (ROS).