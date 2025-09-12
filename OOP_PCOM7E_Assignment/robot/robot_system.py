import math
import heapq
import random
import logging
from abc import ABC, abstractmethod
from enum import Enum
from collections import deque
from typing import List, Optional, Dict, Deque, Tuple


# -----------------------------------------------------------------------------
# Logging (Unit 7: debugging)
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.addHandler(logging.NullHandler())
logger.setLevel(logging.INFO)


# -----------------------------------------------------------------------------
# Core domain types
# -----------------------------------------------------------------------------
class RobotState(Enum):
    OFF = "OFF"
    IDLE = "IDLE"
    MOVING = "MOVING"
    MANIPULATING = "MANIPULATING"
    COMMUNICATING = "COMMUNICATING"
    CHARGING = "CHARGING"
    ERROR = "ERROR"


class Waypoint:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if not isinstance(other, Waypoint):
            return NotImplemented
        return (self.x, self.y) < (other.x, other.y)

    def __eq__(self, other):
        return isinstance(other, Waypoint) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Waypoint(x={self.x}, y={self.y})"

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


class EnvObject:
    def __init__(self, kind: str, id: str, position: Waypoint):
        self.kind = kind
        self.id = id
        self.position = position


class Environment:
    def __init__(self):
        self.objects: List[EnvObject] = []
        self.object_index: Dict[str, EnvObject] = {}  # O(1) lookup by ID
        self.sensor_readings: List[float] = []
        # simpele obstakels; tests voegen eigen kaarten toe
        self.obstacles: List[Tuple[int, int]] = [(2, 2), (3, 3)]

    def sense(self) -> None:
        print("Debug: Sensing environment")
        # voeg ruis toe aan sensor_readings (reproduceerbaar genoeg)
        noise = random.gauss(mu=0, sigma=0.1)
        self.sensor_readings.append(0.5 + noise)
        # update index, verplaats objecten NIET naar obstakels (determinisme)
        for obj in self.objects:
            self.object_index[obj.id] = obj

    def find_nearest_object(self, kind: str) -> Optional[EnvObject]:
        print(f"Debug: Searching for object of kind {kind}")
        k = (kind or "").lower()
        nearest: Optional[EnvObject] = None
        min_dist = float("inf")
        for obj in self.objects:
            if (obj.kind or "").lower() == k:
                # Manhattan afstand is voldoende
                d = abs(obj.position.x) + abs(obj.position.y)
                if d < min_dist:
                    min_dist = d
                    nearest = obj
        return nearest

    def is_obstacle(self, x: int, y: int) -> bool:
        return (x, y) in self.obstacles


class MemoryStore:
    def __init__(self):
        self.facts: List[str] = []
        self.breadcrumbs: List[str] = []

    def push_action(self, action: str) -> None:
        self.breadcrumbs.append(action)

    def last_action(self) -> Optional[str]:
        return self.breadcrumbs.pop() if self.breadcrumbs else None


# -----------------------------------------------------------------------------
# Polymorphic path-planning Strategy (Unit 5)
# -----------------------------------------------------------------------------
class PathPlanner(ABC):
    timeout_counter: int = 0

    @abstractmethod
    def compute(self, start: "Waypoint", target: "Waypoint", env: "Environment") -> Optional[Deque[Tuple[int, int]]]:
        """Return a deque of (x,y) steps or None if no path."""
        raise NotImplementedError


class AStarPlanner(PathPlanner):
    def compute(self, start: "Waypoint", target: "Waypoint", env: "Environment") -> Optional[Deque[Tuple[int, int]]]:
        self.timeout_counter = 0

        def heuristic(a: Waypoint, b: Waypoint) -> float:
            d = math.hypot(b.x - a.x, b.y - a.y)
            # lichte straf als start/target op obstakelcheck triggert
            return d * 1.5 if env.is_obstacle(a.x, a.y) or env.is_obstacle(b.x, b.y) else d

        open_set = [(0.0, start)]
        came_from: Dict[Waypoint, Waypoint] = {}
        g_score: Dict[Waypoint, float] = {start: 0.0}
        max_iterations = 1000

        while open_set and self.timeout_counter < max_iterations:
            self.timeout_counter += 1
            _, current = heapq.heappop(open_set)
            if (current.x, current.y) == (target.x, target.y):
                path: List[Waypoint] = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                coords = deque([(p.x, p.y) for p in path] or [(target.x, target.y)])
                return coords

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                n = Waypoint(current.x + dx, current.y + dy)
                if env.is_obstacle(n.x, n.y):
                    continue
                tentative = g_score.get(current, float("inf")) + 1
                if tentative < g_score.get(n, float("inf")):
                    came_from[n] = current
                    g_score[n] = tentative
                    f = tentative + heuristic(n, target)
                    heapq.heappush(open_set, (f, n))
        return None


class GreedyPlanner(PathPlanner):
    """Eenvoudige greedy planner; puur ter demonstratie van polymorfisme."""
    def compute(self, start: "Waypoint", target: "Waypoint", env: "Environment") -> Optional[Deque[Tuple[int, int]]]:
        x, y = start.x, start.y
        coords: Deque[Tuple[int, int]] = deque()
        self.timeout_counter = 0
        max_steps = 200
        while (x, y) != (target.x, target.y) and self.timeout_counter < max_steps:
            self.timeout_counter += 1
            moved = False
            if x < target.x and not env.is_obstacle(x + 1, y):
                x += 1; moved = True
            elif x > target.x and not env.is_obstacle(x - 1, y):
                x -= 1; moved = True
            elif y < target.y and not env.is_obstacle(x, y + 1):
                y += 1; moved = True
            elif y > target.y and not env.is_obstacle(x, y - 1):
                y -= 1; moved = True
            if not moved:
                return None
            coords.append((x, y))
        return coords if (x, y) == (target.x, target.y) else None


class Navigation:
    def __init__(self, planner: Optional[PathPlanner] = None):
        self.path_queue: Deque[Tuple[int, int]] = deque()
        self.timeout_counter = 0
        self.planner: PathPlanner = planner or AStarPlanner()

    def plan_path(self, start: Waypoint, target: Waypoint, env: Environment) -> bool:
        print(f"Debug: Planning path from {start.x},{start.y} to {target.x},{target.y}")
        coords = self.planner.compute(start, target, env)
        self.timeout_counter = getattr(self.planner, "timeout_counter", 0)
        if coords is None:
            print("Debug: No path found, timeout reached")
            return False
        self.path_queue = coords
        return True

    def next_step(self) -> Optional[Tuple[int, int]]:
        return self.path_queue.popleft() if self.path_queue else None


class Manipulator:
    def __init__(self):
        self.grasp_history: List[str] = []

    def pick(self, object_id: str) -> bool:
        print(f"Debug: Attempting to pick {object_id}")
        # deterministisch succes; tests forceren failure via stub
        self.grasp_history.append(object_id)
        return True

    def undo_last_grasp(self) -> bool:
        return bool(self.grasp_history.pop()) if self.grasp_history else False


class Communicator:
    def speak(self, text: str) -> None:
        print(f"Debug: Speaking {text}")

    def display(self, text: str) -> None:
        print(f"Debug: Displaying {text}")


class CLI:
    def __init__(self):
        self.cmd_queue: Deque[Dict[str, str]] = deque()

    def enqueue(self, cmd: Dict[str, str]) -> None:
        self.cmd_queue.append(cmd)

    def read_command(self) -> Optional[Dict[str, str]]:
        return self.cmd_queue.popleft() if self.cmd_queue else None


# -----------------------------------------------------------------------------
# Robot orchestrator with guards, auto-dock + charging, and try/except (Unit 7)
# -----------------------------------------------------------------------------
class Robot:
    def __init__(self, id: str):
        self.id = id
        self.state = RobotState.OFF
        self.battery_level = 100
        self.env = Environment()
        self.memory = MemoryStore()
        self.nav = Navigation()               # default A* Strategy
        self.manip = Manipulator()
        self.comms = Communicator()

        # Auto-docking / charging flags
        self.charging = False
        self.navigating_to_charger = False
        self.charger_pos = Waypoint(0, -1)    # simpele "dock" positie

    # --- power management ---
    def power_on(self) -> bool:
        print("Debug: Powering on")
        if self.state == RobotState.OFF:
            self.state = RobotState.IDLE
            return True
        return False

    def power_off(self) -> bool:
        print("Debug: Powering off")
        if self.state != RobotState.OFF:
            self.state = RobotState.OFF
            self.charging = False
            self.navigating_to_charger = False
            return True
        return False

    # --- helper: initiate docking if battery low ---
    def _maybe_start_autodock(self) -> Optional[str]:
        if self.battery_level < 10:
            # plan route naar charger
            _ = self.nav.plan_path(Waypoint(0, 0), self.charger_pos, self.env)
            self.navigating_to_charger = True
            self.charging = True  # tests verwachten True zodra docking start
            self.state = RobotState.MOVING
            return "AUTO: Low battery – docking to charger"
        return None

    # --- tick: progress docking/charging, or process a command ---
    def tick(self, command: Dict[str, str]) -> str:
        print(f"Debug: Processing command {command}")
        if self.state == RobotState.OFF:
            return "ERROR: Robot is off"

        # --- normaliseer commandotype en args ---
        cmd_type = str(command.get("type", "")).strip().lower()
        args = command.get("args") or ""

        # Tijdens CHARGING of auto-docking alleen 'tick' toestaan
        if self.state == RobotState.CHARGING and cmd_type != "tick":
            return "ERROR: Robot is charging"
        if self.navigating_to_charger and cmd_type != "tick":
            return "ERROR: Docking in progress"

        # ---------------------------------------------------------------------
        # TICK: recovery, docking-progress, charging-progress
        # ---------------------------------------------------------------------
        if cmd_type == "tick":
            # Herstel uit ERROR (UML: ERROR -> IDLE bij battery >= 10)
            if self.state == RobotState.ERROR:
                if self.battery_level >= 10:
                    self.state = RobotState.IDLE
                    return "OK: Recovered to IDLE"
                else:
                    return "ERROR: Cannot recover (low battery)"

            # Eerst docking-stappen afwerken
            if self.navigating_to_charger:
                step = self.nav.next_step()
                if step is None:
                    self.navigating_to_charger = False
                    self.state = RobotState.CHARGING
                    return "Docked: charging started"
                return f"Auto-docking step {step}"

            # Dan laden
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

        # ---------------------------------------------------------------------
        # NAVIGATE
        # ---------------------------------------------------------------------
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

                # Test-hook: als tests vooraf timeout zetten
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
            except Exception:
                logger.exception("Unexpected error in navigate")
                self.state = RobotState.ERROR
                return "ERROR: Internal planning error"

        # ---------------------------------------------------------------------
        # PICK
        # ---------------------------------------------------------------------
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

                # Test-hook: als tests vooraf timeout zetten
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
            except Exception:
                logger.exception("Unexpected error in pick")
                self.state = RobotState.ERROR
                return "ERROR: Manipulator error"

        # ---------------------------------------------------------------------
        # SPEAK
        # ---------------------------------------------------------------------
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

        # ---------------------------------------------------------------------
        # DEFAULT
        # ---------------------------------------------------------------------
        self.state = RobotState.IDLE
        return "ERROR: Invalid command"

