# Unit 4 – e-Portfolio

## Which UML models fit which SDLC stage?
**Requirements.** Use-case diagrams capture actors/goals; activity diagrams describe flows incl. alternates and error paths.  
**Design.** Class diagrams define static structure (attributes/operations/associations); sequence diagrams show message order per use-case; state machine diagrams suit components with explicit life-cycles (e.g., power/charging).  
**Implementation.** Class/Component diagrams map to code modules; sequence diagrams inform method boundaries and interfaces.  
**Testing.** Sequence + activity flows become test scenarios; state machines yield transition and boundary tests.  
**Maintenance.** Updated class/state diagrams help impact analysis and regression planning.

**References (Harvard):**  
Rumbaugh, J., Jacobson, I. and Booch, G. (2005) *The Unified Modeling Language Reference Manual*, 2nd edn. Addison-Wesley.  
Sommerville, I. (2015) *Software Engineering*, 10th edn. Pearson.

## Washing-machine state machine (after Rumbaugh et al., Ch.21, Figs. 3–7)
See the diagram below (rendered from `uml/washingmachine_state_diagram.puml`).

![Washing machine state machine](uml/washingmachine_state_diagram.png)

© Victor Angelier – OOP_PCOM7E Assignment
