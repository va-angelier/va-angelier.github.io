# Code Quality improvements, clean code Anaya (2021)

Looking at your Robot controller, tick() is doing too many things (state gating, command parsing, navigation, manipulation, charging, error handling) in one method.
This code comes from the OOP Python module.

### The controller

So we can apply your three Anaya-style strategies cleanly:

The 3 methods to apply (to your OOP code)
1) Single responsibility

Refactor tick() into small command handlers:

handle_tick()

handle_navigate(args)

handle_pick(args)

handle_speak(args)

guard_command(cmd_type) (charging/docking rules)

Why: tick() is currently a long, branch-heavy “god method” 


### The controller

2) Naming conventions + remove magic numbers

Replace repeated thresholds/values like 10, 100, 1000, 5, 2 with named constants:

LOW_BATTERY_THRESHOLD = 10

FULL_BATTERY = 100

PLANNING_TIMEOUT_LIMIT = 1000

NAV_BATTERY_COST = 5

SPEAK_BATTERY_COST = 2

Those values are scattered throughout the method today 


### The controller


3) Proper documentation/comments (docstrings, explain “why”)

Add short docstrings to each handler and keep comments for non-obvious intent (e.g., why you force IDLE in some error paths).

What this looks like (minimal example refactor)

Below is the shape of the change (not the whole file), showing the three methods applied to controller.py 


# controller.py

```python
LOW_BATTERY_THRESHOLD = 10
FULL_BATTERY = 100
PLANNING_TIMEOUT_LIMIT = 1000
NAV_BATTERY_COST = 5
SPEAK_BATTERY_COST = 2
CHARGE_STEP = 10


class Robot:
    def tick(self, command: dict[str, str]) -> str:
        """Process one control-loop step based on current state and command."""
        if self.state == RobotState.OFF:
            return "ERROR: Robot is off"

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

    def _guard_command(self, cmd_type: str) -> str | None:
        """Reject commands that would interrupt charging/docking safety behaviour."""
        if self.state == RobotState.CHARGING and cmd_type != "tick":
            return "ERROR: Robot is charging"
        if self.navigating_to_charger and cmd_type != "tick":
            return "ERROR: Docking in progress"
        return None

```

### Demonstrates:

SRP: each command gets its own handler
Naming: no unexplained numbers
Documentation: docstrings clarify intent