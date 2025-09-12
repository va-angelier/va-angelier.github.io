# robot/robot_system.py
import random
from collections import deque
from typing import List, Optional, Dict
from enum import Enum
import heapq
import math
LOW_BATTERY = 10
CHARGE_RATE_PER_TICK = 20


# UML-compatible command type (optional convenience)
class Command:
    def __init__(self, type: str, args: str):
        self.type = type
        self.args = args


class RobotState(Enum):
    OFF = "OFF"
    IDLE = "IDLE"
    MOVING = "MOVING"
    MANIPULATING = "MANIPULATING"
    COMMUNICATING = "COMMUNICATING"
    ERROR = "ERROR"
    CHARGING = "CHARGING"


class Waypoint:
    __slots__ = ("x", "y")  # optional; saves memory

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # for heapq ordering only
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


class EnvObject:
    def __init__(self, kind: str, id: str, position: Waypoint):
        self.kind = kind
        self.id = id
        self.position = position


class Environment:
    def __init__(self):
        self.charging_dock = Waypoint(0, -1)

        self.objects: List[EnvObject] = []
        self.object_index: Dict[str, EnvObject] = {}  # O(1) lookup by ID
        self.sensor_readings: List[float] = []
        self.obstacles = [(2, 2), (3, 3)]

    def sense(self) -> None:
        print("Debug: Sensing environment")
        noise = random.gauss(mu=0, sigma=0.1)
        self.sensor_readings.append(0.5 + noise)
        for obj in self.objects:
            dx = int(random.gauss(0, 1))
            dy = int(random.gauss(0, 1))
            nx, ny = obj.position.x + dx, obj.position.y + dy
            # verplaats alleen als het GEEN obstakel is
            if not self.is_obstacle(nx, ny):
                obj.position.x, obj.position.y = nx, ny
            self.object_index[obj.id] = obj

    # --- UML compatibility aliases ---
    def findNearestObject(self, kind: str):
        return self.find_nearest_object(kind)

    def isObstacle(self, x: int, y: int) -> bool:
        return self.is_obstacle(x, y)

    def find_nearest_object(self, kind: str) -> Optional[EnvObject]:
        print(f"Debug: Searching for object of kind {kind}")
        min_distance = float("inf")
        nearest = None
        for obj in self.objects:
            if obj.kind.lower() == kind.lower():
                distance = (abs(obj.position.x) + abs(obj.position.y))
                if distance < min_distance:
                    min_distance = distance
                    nearest = obj
        return nearest

    def is_obstacle(self, x: int, y: int) -> bool:
        return (x, y) in self.obstacles


class MemoryStore:
    def __init__(self):
        self.facts: List[str] = []
        self.breadcrumbs: List[str] = []

    def pushAction(self, action: str) -> None:
        return self.push_action(action)

    def push_action(self, action: str) -> None:
        self.breadcrumbs.append(action)

    def lastAction(self):
        return self.last_action()
    
    def last_action(self) -> Optional[str]:
        return self.breadcrumbs.pop() if self.breadcrumbs else None


class Navigation:
    def __init__(self):
        self.path_queue: deque = deque()
        self.timeout_counter = 0

    # --- UML compatibility aliases ---
    def planPath(self, start: Waypoint, target: Waypoint, env: "Environment") -> bool:
        return self.plan_path(start, target, env)

    def nextStep(self):
        return self.next_step()

    @property
    def pathQueue(self):
        return self.path_queue

    def plan_path(self, start: Waypoint, target: Waypoint, env: Environment) -> bool:
        print(f"Debug: Planning path from {start.x},{start.y} to {target.x},{target.y}")

        def heuristic(a: Waypoint, b: Waypoint) -> float:
            distance = math.hypot(b.x - a.x, b.y - a.y)
            if env.is_obstacle(a.x, a.y) or env.is_obstacle(b.x, b.y):
                return distance * 1.5
            return distance

        open_set = [(0, start)]
        came_from: Dict[Waypoint, Waypoint] = {}
        g_score: Dict[Waypoint, float] = {start: 0.0}
        f_score: Dict[Waypoint, float] = {start: heuristic(start, target)}
        self.timeout_counter = 0
        max_iterations = 1000

        while open_set and self.timeout_counter < max_iterations:
            self.timeout_counter += 1
            _, current = heapq.heappop(open_set)
            if (current.x, current.y) == (target.x, target.y):
                print("Debug: Path found")
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                # at least include target if path empty
                coords = [(p.x, p.y) for p in path] or [(target.x, target.y)]
                self.path_queue = deque(coords)
                return True

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = Waypoint(current.x + dx, current.y + dy)
                if env.is_obstacle(neighbor.x, neighbor.y):
                    continue
                tentative_g = g_score.get(current, float("inf")) + 1
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, target)
                    f_score[neighbor] = f
                    heapq.heappush(open_set, (f, neighbor))

        print("Debug: No path found, timeout reached")
        return False

    def next_step(self) -> Optional[tuple]:
        return self.path_queue.popleft() if self.path_queue else None


class Manipulator:
    def __init__(self):
        self.grasp_history: List[str] = []

    def pick(self, object_id: str) -> bool:
        print(f"Debug: Attempting to pick {object_id}")
        # deterministisch: slaag altijd; 'grasp failed' tests gebruiken toch een stub
        self.grasp_history.append(object_id)
        return True

    def undoLastGrasp(self) -> bool:
        return self.undo_last_grasp()

    def undo_last_grasp(self) -> bool:
        return bool(self.grasp_history.pop()) if self.grasp_history else False


class Communicator:
    def speak(self, text: str) -> None:
        print(f"Debug: Speaking {text}")

    def display(self, text: str) -> None:
        print(f"Debug: Displaying {text}")


class CLI:
    def __init__(self):
        self.cmd_queue: deque = deque()

    @property
    def cmdQueue(self):
        return self.cmd_queue
    
    def enqueue(self, cmd: Dict[str, str]) -> None:
        self.cmd_queue.append(cmd)

    def read_command(self) -> Optional[Dict[str, str]]:
        return self.cmd_queue.popleft() if self.cmd_queue else None


class Robot:
    def __init__(self, id: str):
        self.charging = False
        self.navigating_to_charger = False
        self.id = id
        self.state = RobotState.OFF
        self.battery_level = 100
        self.env = Environment()
        self.memory = MemoryStore()
        self.nav = Navigation()
        self.manip = Manipulator()
        self.comms = Communicator()

    def _auto_charge_if_low(self) -> str | None:
        if self.battery_level < LOW_BATTERY and not self.navigating_to_charger and self.state != RobotState.CHARGING:
            return self._start_docking()
        return None

    def _start_docking(self) -> str:
        dock = getattr(self.env, "charging_dock", Waypoint(0, -1))
        self.nav.plan_path(Waypoint(0, 0), dock, self.env)
        self.navigating_to_charger = True
        self.charging = True
        self.state = RobotState.MOVING
        return "AUTO: Low battery – docking initiated"

    def _charging_tick(self) -> str:
        if self.state != RobotState.CHARGING:
            return "Tick executed"
        self.battery_level = min(100, self.battery_level + CHARGE_RATE_PER_TICK)
        if self.battery_level >= 100:
            self.charging = False
            self.state = RobotState.IDLE
            return "Charging complete (100%)"
        return f"Charging... ({self.battery_level}%)"

    # --- UML compatibility aliases ---
    def powerOn(self) -> bool:     # UML name
        return self.power_on()

    def powerOff(self) -> bool:    # UML name
        return self.power_off()

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
            return True
        return False

    def tick(self, command: Dict[str, str] | Command) -> str:
        print(f"Debug: Processing command {command}")
        if self.state == RobotState.OFF:
            return "ERROR: Robot is off"

        if isinstance(command, Command):
            command = {"type": command.type, "args": command.args}

        cmd_type = command.get("type")

        # Auto-docking / charging achtergrondlogica via 'tick'
        if cmd_type == "tick":
            if self.navigating_to_charger:
                step = self.nav.next_step()
                if step is None:
                    # Aangekomen bij de dock
                    self.navigating_to_charger = False
                    self.charging = True
                    self.state = RobotState.CHARGING
                    return "Docked: charging started"
                return f"Auto-docking step {step}"
            if self.state == RobotState.CHARGING:
                return self._charging_tick()
            return "Tick executed"

        if cmd_type == "navigate":
            if self.state != RobotState.IDLE:
                self.state = RobotState.IDLE
                return "ERROR: Cannot navigate, robot is busy"
            self.state = RobotState.MOVING
            try:
                x, y = map(int, command["args"].split(","))
                start = Waypoint(0, 0)
                target = Waypoint(x, y)
                if self.battery_level < 10:
                    self.state = RobotState.IDLE
                    return "ERROR: Low battery – please charge"
                if (not self.nav.plan_path(start, target, self.env) or
                        self.nav.timeout_counter >= 1000):
                    self.state = RobotState.ERROR
                    return "ERROR: No path to target"
                step = self.nav.next_step()
                self.memory.push_action("NAVIGATE")
                self.battery_level -= 5
                charge_msg = self._auto_charge_if_low()
                self.state = self.state if charge_msg else RobotState.IDLE
                base = f"Navigating to {step}" if step else "ERROR: No path"
                return f"{base} | {charge_msg}" if charge_msg else base
            except ValueError:
                self.state = RobotState.IDLE
                return "ERROR: Invalid coordinates"

        elif cmd_type == "pick":
            if self.state != RobotState.IDLE:
                self.state = RobotState.IDLE
                return "ERROR: Cannot pick, robot is busy"
            if self.battery_level < 10:
                self.state = RobotState.IDLE
                return "ERROR: Low battery – please charge"
            obj = self.env.find_nearest_object(command["args"])
            if not obj:
                self.state = RobotState.IDLE
                return "ERROR: Object not found"
            if (not self.nav.plan_path(Waypoint(0, 0), obj.position, self.env) or
                    self.nav.timeout_counter >= 1000):
                self.state = RobotState.ERROR
                return "ERROR: No path to target"
            self.state = RobotState.MANIPULATING
            if not self.manip.pick(command["args"]):
                self.state = RobotState.ERROR
                return "ERROR: Grasp failed"
            self.memory.push_action("PICK")
            self.state = RobotState.IDLE
            self.battery_level -= 5
            charge_msg = self._auto_charge_if_low()
            self.state = self.state if charge_msg else RobotState.IDLE
            return "OK: Picked object" if not charge_msg else "OK: Picked object | " + charge_msg


        elif cmd_type == "speak":
            if self.state != RobotState.IDLE:
                self.state = RobotState.IDLE
                return "ERROR: Cannot speak, robot is busy"
            self.state = RobotState.COMMUNICATING
            self.comms.speak(command["args"])
            self.memory.push_action("SPEAK")
            self.state = RobotState.IDLE
            self.battery_level -= 2
            charge_msg = self._auto_charge_if_low()
            self.state = self.state if charge_msg else RobotState.IDLE
            return "OK: Spoken" if not charge_msg else "OK: Spoken | " + charge_msg


        elif cmd_type == "tick":
            return "Tick executed"

        self.state = RobotState.IDLE
        return "ERROR: Invalid command"
