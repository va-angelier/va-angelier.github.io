# System Design Proposal for Humanoid Robot Software

**Author**: Victor Angelier  
**Date**: 23 August 2025

## Background Research

Research used “robot,” “human-robot interaction,” and “collaborative robot” to explore functionalities, interfaces, and collaboration (Mukherjee et al., 2022; Ackerman, 2023). Additional sources: Mulko (2023), Siciliano and Khatib (2016), Russell and Norvig (2020), Thrun et al. (2005).

## System Design Rationale

The system enables a humanoid robot for warehouse tasks: navigation, object manipulation, and human communication via a CLI (Mukherjee et al., 2022). Python’s object-oriented design ensures modularity, with a CLI for simplicity (Ackerman, 2023). Classes are modeled with UML, using lists, stacks, and queues (Siciliano and Khatib, 2016). Power management is a state transition (Thrun et al., 2005). UML models and tests ensure robustness (Derezińska, 2015).

## UML Models

### Traceability (UML ↔ Code)
| UML element        | Code (file/class/method)                | Opmerking |
|--------------------|------------------------------------------|-----------|
| Robot              | robot_system.py / class Robot            | Orkestreert subsystems; power/tick/battery |
| Navigation         | robot_system.py / class Navigation       | A*; pathQueue (Queue) |
| Manipulator        | robot_system.py / class Manipulator      | graspHistory (Stack); undo |
| Communicator       | robot_system.py / class Communicator     | speak/display |
| Environment        | robot_system.py / class Environment      | objects/sensorReadings (List) |
| MemoryStore        | robot_system.py / class MemoryStore      | breadcrumbs (Stack) |
| CLI                | robot_system.py / class CLI              | cmdQueue (Queue) |
| RobotState         | robot_system.py / Enum RobotState        | OFF…CHARGING… |
| Waypoint/EnvObject | robot_system.py / classes Waypoint/EnvObject | Value objects |


### Class Diagram
Defines structure, implemented in `robot_system.py` (Rumbaugh et al., 2005).

```plantuml
@startuml
package "Robot System" {
  class Robot {
    - id: String
    - state: RobotState
    - batteryLevel: Integer
    - env: Environment
    - memory: MemoryStore
    - nav: Navigation
    - manip: Manipulator
    - comms: Communicator
    + powerOn(): Boolean
    + powerOff(): Boolean
    + tick(command: Command): String
  }
  enum RobotState {
    OFF
    IDLE
    MOVING
    MANIPULATING
    COMMUNICATING
    ERROR
  }
  class Navigation {
    - pathQueue: Queue<Waypoint>
    + planPath(start: Waypoint, target: Waypoint): Boolean
    + nextStep(): Waypoint
  }
  class Manipulator {
    - graspHistory: Stack<String>
    + pick(objectId: String): Boolean
    + undoLastGrasp(): Boolean
  }
  class Communicator {
    + speak(text: String): void
    + display(text: String): void
  }
  class Environment {
    - objects: List<EnvObject>
    - sensorReadings: List<Float>
    + sense(): void
    + findNearestObject(kind: String): EnvObject
  }
  class CLI {
    - cmdQueue: Queue<Command>
    + enqueue(cmd: Command): void
    + readCommand(): Command
  }
  class MemoryStore {
    - facts: List<String>
    - breadcrumbs: Stack<String>
    + pushAction(action: String): void
    + lastAction(): String
  }
  class Command {
    + type: String
    + args: Map<String,String>
  }
  class Waypoint {
    + x: Integer
    + y: Integer
  }
  class EnvObject {
    + kind: String
    + id: String
    + position: Waypoint
  }
  Robot "1" --> "1" Navigation
  Robot "1" --> "1" Manipulator
  Robot "1" --> "1" Communicator
  Robot "1" --> "1" Environment
  Robot "1" --> "1" MemoryStore
  Environment "1" --> "*" EnvObject
  CLI --> Robot : "sends Command"
}
@enduml


### Activity Diagram (Pick Up Object)
Models the “pick up object” use case with swimlanes, guards, and exceptions (Rumbaugh et al., 2005).

@startuml
skinparam activity { BackgroundColor White; BorderColor Black }
skinparam shadowing false

partition "User" as U { start :Type "pick <objectKind>" in CLI; }
partition "CLI" as C { :Enqueue Command; }
partition "Robot" as R1 {
  :Read Command;
  if (state == OFF) then (yes)
    :Reply: "Power on first"; stop
  else (no) endif
  :Environment.sense();
}
partition "Environment" as E { :Collect sensor data; }
partition "Robot" as R2 {
  if (objectFound) then (yes)
    if (battery < 10%) then (yes) :Reply: "Low battery – please charge"; stop
    else (no) endif
  else (no) :Reply: "Object not found"; stop endif
}
partition "Navigation" as N { :planPath(targetPos); repeat :nextStep(); repeat while (not at object) }
partition "Robot" as R3 {
  if (no path or timeout) then (yes) :state = ERROR; :Notify: "No path to target"; stop
  else (no) :state = MANIPULATING; endif
}
partition "Manipulator" as M {
  :pick(objectId);
  if (graspSuccess) then (yes)
    :MemoryStore.pushAction(PICK);
    :state = IDLE; :Ack success to CLI; stop
  else (no) :state = ERROR; :Notify: "Grasp failed"; stop endif
}
@enduml

### Sequence Diagram
Illustrates the “pick” command flow (Russell and Norvig, 2020).

@startuml
actor User
participant CLI
participant Robot
participant Environment
participant Navigation
participant Manipulator
participant MemoryStore
User -> CLI : type "pick bottle"
CLI -> CLI : enqueue(Command)
CLI -> Robot : deliver(Command)
Robot -> Environment : sense()
Environment --> Robot : sensor snapshot
Robot -> Navigation : planPath(target)
Navigation --> Robot : path planned
loop until at target
  Robot -> Navigation : nextStep()
  Navigation --> Robot : Waypoint
end
Robot -> Manipulator : pick(objectId)
Manipulator --> Robot : success/fail
alt success
  Robot -> MemoryStore : pushAction(PICK)
  Robot -> CLI : "OK: picked"
else fail
  Robot -> CLI : "ERROR: grasp failed"
end
@enduml

### State Transition Diagram
Models power management and operational states (Thrun et al., 2005).

@startuml
[*] --> OFF
OFF --> IDLE : powerOn()
IDLE --> OFF : powerOff()
IDLE --> MOVING : planPath/step()
MOVING --> IDLE : arrived()
IDLE --> MANIPULATING : pick()/place()
MANIPULATING --> IDLE : done()/cancel()
IDLE --> COMMUNICATING : speak()/display()
COMMUNICATING --> IDLE : done()
state ERROR
MOVING --> ERROR : obstacle/fault
MANIPULATING --> ERROR : graspFail
COMMUNICATING --> ERROR : deviceFail
ERROR --> IDLE : recover()
ERROR --> OFF : criticalFailure()
@enduml

Data Structures

List: Environment.objects, Environment.sensorReadings (linear search, O(n)).
Stack: Manipulator.graspHistory, MemoryStore.breadcrumbs (LIFO, O(1)).
Queue: Navigation.pathQueue, CLI.cmdQueue (FIFO, O(1)).

Automated Testing and Implementation
Developed in PyCharm, robot_system.py implements the UML models. Tests in test_robot_system.py cover all scenarios.
References

Ackerman, E. (2023) ‘Humanoid Robots Are Getting to Work’, IEEE Spectrum. Available at: https://spectrum.ieee.org/humanoid-robots (Accessed: 23 August 2025).
Derezińska, A. (2015) ‘Improving mutation testing process of Python programs’, in Software Engineering Techniques in Progress, pp. 233–246.
Kang, H.J., Lo, D. and Lawall, J. (2019) ‘BugsInPy: A database of existing bugs in Python programs to enable controlled testing and debugging studies’, in Proceedings of the 33rd European Conference on Object-Oriented Programming, pp. 1–6. doi:10.4230/LIPIcs.ECOOP.2019.1.
Mukherjee, D. et al. (2022) ‘A Survey of Robot Learning Strategies for Human-Robot Collaboration in Industrial Settings’, Robotics and Computer-Integrated Manufacturing, 73, p. 102231. doi:10.1016/j.rcim.2021.102231.
Mulko, M. (2023) ‘5 of the World’s Most Realistic Humanoid Robots Ever’, Interesting Engineering. Available at: https://interestingengineering.com/innovation/humanoid-robots (Accessed: 23 August 2025).
Rumbaugh, J., Jacobson, I. and Booch, G. (2005) The Unified Modeling Language Reference Manual. 2nd edn. Addison-Wesley.
Russell, S. and Norvig, P. (2020) Artificial Intelligence: A Modern Approach. 4th edn. Pearson.
Siciliano, B. and Khatib, O. (2016) Springer Handbook of Robotics. 2nd edn. Springer.
Sommerville, I. (2015) Software Engineering. 10th edn. Pearson.
Thrun, S., Burgard, W. and Fox, D. (2005) Probabilistic Robotics. MIT Press.