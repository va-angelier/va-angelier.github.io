# Code quality improvements (Anaya, 2021)

This refactoring exercise applies three clean-code strategies from Anaya (2021) to improve the quality of an existing Python OOP codebase (Robot controller). The original tick() method handled multiple responsibilities (state gating, command parsing, navigation, manipulation, charging, and error handling), making it difficult to maintain and reason about.

## 1) Single responsibility

To reduce complexity, tick() was decomposed into small, focused command handlers:

_handle_tick()

_handle_navigate(args)

_handle_pick(args)

_handle_speak(args)

_guard_command(cmd_type) for charging/docking constraints

This reduces branching and improves readability by ensuring each function does one job.

## 2) Naming conventions and removal of magic numbers

Repeated numeric values were replaced with named constants to make intent explicit and changes safer:

LOW_BATTERY_THRESHOLD = 10

FULL_BATTERY = 100

PLANNING_TIMEOUT_LIMIT = 1000

NAV_BATTERY_COST = 5

SPEAK_BATTERY_COST = 2

This aligns with clean-code guidance on clarity and maintainability.

## 3) Documentation and purposeful comments

Short docstrings were added to the handlers to clarify intent, and comments were limited to “why” decisions (not restating obvious code).

### Minimal example (structure)
```python
LOW_BATTERY_THRESHOLD = 10
FULL_BATTERY = 100
PLANNING_TIMEOUT_LIMIT = 1000
NAV_BATTERY_COST = 5
SPEAK_BATTERY_COST = 2

class Robot:
    def tick(self, command: dict[str, str]) -> str:
        """Process one control-loop step based on current state and a command."""
        cmd_type = str(command.get("type", "")).strip().lower()
        args = command.get("args") or ""

        guard_msg = self._guard_command(cmd_type)
        if guard_msg:
            return guard_msg

        handlers = {
            "tick": self._handle_tick,
            "navigate": lambda: self._handle_navigate(args),
            "pick": lambda: self._handle_pick(args),
            "speak": lambda: self._handle_speak(args),
        }
        return handlers.get(cmd_type, self._handle_unknown)()

```

Result: improved readability, clearer intent, and reduced maintenance risk, while preserving the original behaviour.

Reference
Anaya, M. (2021) Clean Code in Python: Refactor your legacy code base. 2nd edn. Birmingham: Packt.