System Design Rationale (≈500 words, UK English)

The software implemented in robot/robot_system.py supports navigation, object manipulation, and communication for a warehouse humanoid robot, accessible via python -m robot. It prioritises safety, maintainability, and testability, aligning with SDLC principles (Sommerville, 2015). A composition-based architecture uses a Robot façade to orchestrate Navigation, Manipulator, Communicator, Environment, and MemoryStore, reducing coupling and enabling test-time substitution (stubs/mocks). This avoids inheritance hierarchies that often tighten coupling and blur responsibilities (Derezińska, 2015; Siciliano and Khatib, 2016).

The RobotState enum (OFF, IDLE, MOVING, MANIPULATING, COMMUNICATING, CHARGING, ERROR) encodes explicit transitions with guards. Commands are rejected during CHARGING (except tick for progress), while a low-battery guard triggers auto-docking by planning a path to the charger and switching to CHARGING until 100% state of charge; this behaviour is validated in robot/tests/test_auto_charge.py (Mukherjee et al., 2022). The state machine yields predictable recovery (e.g., tick from ERROR back to IDLE when safe), outperforming ad-hoc flags; the model is reflected in uml/state_diagram.puml (Rumbaugh, Jacobson and Booch, 2005).

Data structures are purpose-driven (Siciliano and Khatib, 2016):

List — Environment.objects and sensor_readings (dynamic append, O(1)).

Dictionary — object_index for O(1) ID lookups, trading memory for speed.

Stack — Manipulator.grasp_history and MemoryStore.breadcrumbs for LIFO undo (O(1)).

Queue — Navigation.path_queue and CLI.cmd_queue for FIFO processing (O(1)).

Navigation employs A* with a Euclidean heuristic (time complexity O(V log V + E)), chosen over Dijkstra’s (no heuristic) for faster convergence and over purely greedy approaches (which sacrifice optimality) (Russell and Norvig, 2020; Thrun, Burgard and Fox, 2005). Obstacle checks via Environment.is_obstacle() keep the planner decoupled from map representation. Polymorphism is explicit: Navigation depends on a PathPlanner Strategy; AStarPlanner is the default and GreedyPlanner an alternative. Tests inject planners and stubs to demonstrate substitutability without modifying Robot (DIP/OCP). Case-insensitive object lookup improves CLI ergonomics, at negligible overhead, matching HRI expectations (Ackerman, 2023).

Error handling covers low battery, no path, and grasp failure with stable operator messages (e.g., “ERROR: No path to target”), mirrored in activity/sequence diagrams and verified by robot/tests/test_* suites. Determinism is supported by narrow interfaces (is_obstacle, sense) and by isolating randomness in tests through stubs/fixed inputs (Derezińska, 2015; Kang, Lo and Lawall, 2019). Linting and coverage provide continuous feedback on quality.

Critical analysis. A* assumes a mostly static map; in dynamic settings D* Lite re-plans efficiently but increases complexity and test surface (Thrun, Burgard and Fox, 2005). In-memory Lists/Stacks/Queues are lightweight and perfectly adequate for the assignment, but lack persistence and durability guarantees (Sommerville, 2015). The CLI yields determinism and simplicity compared with a ROS-based GUI, at the cost of interactivity and richer visual feedback (Ackerman, 2023). An event-driven supervisor could overlap sensing and motion to reduce latency. For explore-space growth or continuous change, PRM/RRT families become relevant for manipulation, trading optimality for probabilistic completeness (Russell and Norvig, 2020).

For concrete traceability, the PlantUML sources live under uml/—uml/class_diagram.puml, uml/activity_navigate.puml, uml/activity_pick.puml, uml/activity_errors.puml, uml/sequence_diagram.puml, and uml/state_diagram.puml—and map 1-to-1 to the entries in the traceability matrix.

In summary, a guarded state machine, compositional boundaries, purposeful data structures, and a polymorphic planning Strategy deliver a system that is safe, testable, and extensible, directly addressing the assessment objectives and reflecting industry practice (Mukherjee et al., 2022; Ackerman, 2023; Russell and Norvig, 2020).