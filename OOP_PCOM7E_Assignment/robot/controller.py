"""Robot orchestrator: guards, auto-docking/charging and mode commands."""
from __future__ import annotations

import logging
from typing import Dict, Optional

from robot.domain.models import RobotState, Waypoint, Environment, MemoryStore
from robot.services.navigation import Navigator
from robot.services.actuators import Manipulator, Communicator

logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.addHandler(logging.NullHandler())
logger.setLevel(logging.INFO)


class Robot:
    """High-level façade aggregating subsystems and control logic."""
    # pylint: disable=too-many-instance-attributes

    def __init__(self, robot_id: str):
        self.id = robot_id
        self.state = RobotState.OFF
        self.battery_level = 100
        self.env = Environment()
        self.memory = MemoryStore()
        self.nav = Navigator()                 # default A* Strategy
        self.manip = Manipulator()
        self.comms = Communicator()

        # Auto-docking / charging flags
        self.charging = False
        self.navigating_to_charger = False
        self.charger_pos = Waypoint(0, -1)

    def power_on(self) -> bool:
        """Transition OFF→IDLE on first power-on."""
        if self.state == RobotState.OFF:
            self.state = RobotState.IDLE
            return True
        return False

    def power_off(self) -> bool:
        """Transition to OFF and clear charging/docking flags."""
        if self.state != RobotState.OFF:
            self.state = RobotState.OFF
            self.charging = False
            self.navigating_to_charger = False
            return True
        return False

    def _maybe_start_autodock(self) -> Optional[str]:
        """Start docking when battery is low; return status message or None."""
        if self.battery_level < 10:
            _ = self.nav.plan_path(Waypoint(0, 0), self.charger_pos, self.env)
            self.navigating_to_charger = True
            self.charging = True
            self.state = RobotState.MOVING
            return "AUTO: Low battery – docking to charger"
        return None

    def tick(self, command: Dict[str, str]) -> str:
        """Process one control-loop step for the current robot state.
        TODO(Unit 12): State/Command refactor to reduce branches/returns.
        """
        # pylint: disable=too-many-return-statements,too-many-branches,too-many-statements
        if self.state == RobotState.OFF:
            return "ERROR: Robot is off"

        cmd_type = str(command.get("type", "")).strip().lower()
        args = command.get("args") or ""

        if self.state == RobotState.CHARGING and cmd_type != "tick":
            return "ERROR: Robot is charging"
        if self.navigating_to_charger and cmd_type != "tick":
            return "ERROR: Docking in progress"

        if cmd_type == "tick":
            if self.state == RobotState.ERROR:
                if self.battery_level >= 10:
                    self.state = RobotState.IDLE
                    return "OK: Recovered to IDLE"
                return "ERROR: Cannot recover (low battery)"

            if self.navigating_to_charger:
                step = self.nav.next_step()
                if step is None:
                    self.navigating_to_charger = False
                    self.state = RobotState.CHARGING
                    return "Docked: charging started"
                return f"Auto-docking step {step}"

            if self.state == RobotState.CHARGING:
                if self.battery_level >= 100:
                    self.state = RobotState.IDLE
                    self.charging = False
                    return "Charging complete (100%)"
                self.battery_level = min(100, self.battery_level + 10)
                if self.battery_level >= 100:
                    self.state = RobotState.IDLE
                    self.charging = False
                    return "Charging complete (100%)"
                return f"Charging... {self.battery_level}%"

            return "Tick executed"

        if cmd_type == "navigate":
            if self.state != RobotState.IDLE:
                self.state = RobotState.IDLE
                return "ERROR: Cannot navigate, robot is busy"
            self.state = RobotState.MOVING
            try:
                x, y = map(int, args.split(","))
                start = Waypoint(0, 0)
                target = Waypoint(x, y)
                if self.battery_level < 10:
                    self.state = RobotState.IDLE
                    return "ERROR: Low battery – please charge"

                if self.nav.timeout_counter >= 1000:
                    self.state = RobotState.ERROR
                    return "ERROR: No path to target"

                if (not self.nav.plan_path(start, target, self.env)
                        or self.nav.timeout_counter >= 1000):
                    self.state = RobotState.ERROR
                    return "ERROR: No path to target"

                step = self.nav.next_step()
                self.memory.push_action("NAVIGATE")
                self.battery_level -= 5
                self.state = RobotState.IDLE
                msg = f"Navigating to {step}" if step else "ERROR: No path"
                auto = self._maybe_start_autodock()
                return f"{msg} | {auto}" if auto else msg
            except ValueError:
                self.state = RobotState.IDLE
                return "ERROR: Invalid coordinates"
            except Exception as exc:  # pylint: disable=broad-exception-caught
                logger.exception("Unexpected error in navigate %s", exc)
                self.state = RobotState.ERROR
                return "ERROR: Internal planning error"

        if cmd_type == "pick":
            if self.state != RobotState.IDLE:
                self.state = RobotState.IDLE
                return "ERROR: Cannot pick, robot is busy"
            self.state = RobotState.MANIPULATING
            try:
                if self.battery_level < 10:
                    self.state = RobotState.IDLE
                    return "ERROR: Low battery – please charge"

                obj = self.env.find_nearest_object(args)
                if not obj:
                    self.state = RobotState.IDLE
                    return "ERROR: Object not found"

                if self.nav.timeout_counter >= 1000:
                    self.state = RobotState.ERROR
                    return "ERROR: No path to target"

                if (not self.nav.plan_path(Waypoint(0, 0), obj.position, self.env)
                        or self.nav.timeout_counter >= 1000):
                    self.state = RobotState.ERROR
                    return "ERROR: No path to target"

                if not self.manip.pick(args):
                    self.state = RobotState.ERROR
                    return "ERROR: Grasp failed"

                self.memory.push_action("PICK")
                self.state = RobotState.IDLE
                self.battery_level -= 5
                msg = "OK: Picked object"
                auto = self._maybe_start_autodock()
                return f"{msg} | {auto}" if auto else msg
            except Exception as exc:  # pylint: disable=broad-exception-caught
                logger.exception("Unexpected error in pick: %s", exc)
                self.state = RobotState.ERROR
                return "ERROR: Manipulator error"

        if cmd_type == "speak":
            if self.state != RobotState.IDLE:
                self.state = RobotState.IDLE
                return "ERROR: Cannot speak, robot is busy"
            self.state = RobotState.COMMUNICATING
            self.comms.speak(args)
            self.memory.push_action("SPEAK")
            self.state = RobotState.IDLE
            self.battery_level -= 2
            auto = self._maybe_start_autodock()
            return "OK: Spoken" if not auto else f"OK: Spoken | {auto}"

        self.state = RobotState.IDLE
        return "ERROR: Invalid command"
