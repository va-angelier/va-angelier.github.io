import unittest
from collections import deque
from typing import List, Optional, Dict, Tuple
from enum import Enum
import random
import heapq
import itertools

# Property-based testing (pip install -r requirements.txt)
from hypothesis import given
from hypothesis.strategies import text, lists, floats


# ---------- Domain model ----------

class RobotState(Enum):
    OFF = "OFF"
    IDLE = "IDLE"
    MOVING = "MOVING"
    MANIPULATING = "MANIPULATING"
    COMMUNICATING = "COMMUNICATING"
    CHARGING = "CHARGING"     # NEW
    ERROR = "ERROR"


class Waypoint:
    """Value object for grid coordinates."""
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return isinstance(other, Waypoint) and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Waypoint({self.x},{self.y})"


class EnvObject:
    """Value object for an object in the environment."""
    __slots__ = ("kind", "id", "position")

    def __init__(self, kind: str, id: str, position: Waypoint):
        self.kind = kind
        self.id = id
        self.position = position


class Environment:
    """Simulates environment and sensor readings."""
    def __init__(self):
        self.objects: List[EnvObject] = []           # LIST
        self.sensor_readings: List[float] = []       # LIST

    def sense(self, noise: Optional[float] = None) -> None:
        """
        Simulate dynamic data with Gaussian noise (μ=0, σ≈0.1) unless a noise value is injected.
        Reading is clipped to [0, 1] for realism.
        """
        z = noise if noise is not None else random.gauss(0, 0.1)
        reading = 0.5 + z
        reading = max(0.0, min(1.0, reading))  # clip to [0,1]
        self.sensor_readings.append(reading)

        # Update object positions dynamically (simple random walk)
        for obj in self.objects:
            obj.position.x += int(round(random.gauss(0, 1)))
            obj.position.y += int(round(random.gauss(0, 1)))

    def find_nearest_object(self, kind: str) -> Optional[EnvObject]:
        # Linear search (O(n)) for simplicity
        for obj in self.objects:
            if obj.kind == kind:
                return obj
        return None


class MemoryStore:
    """Facts (LIST) + breadcrumbs as STACK for undo/trace."""
    def __init__(self):
        self.facts: List[str] = []       # LIST
        self.breadcrumbs: List[str] = [] # STACK

    def push_action(self, action: str) -> None:
        self.breadcrumbs.append(action)  # O(1)

    def last_action(self) -> Optional[str]:
        return self.breadcrumbs.pop() if self.breadcrumbs else None  # O(1)


class Navigation:
    """
    A* on a 4-neighbour grid. Uses a queue of waypoints for the next steps.
    """
    def __init__(self):
        self.path_queue: deque[Tuple[int, int]] = deque()  # QUEUE
        self._counter = itertools.count()  # tie-breaker for heapq

    @staticmethod
    def _heuristic(a: Waypoint, b: Waypoint) -> float:
        # Manhattan distance is admissible & consistent on a 4-neighbour grid
        return abs(b.x - a.x) + abs(b.y - a.y)

    def plan_path(self, start: Waypoint, target: Waypoint) -> None:
        open_set: List[Tuple[float, int, Waypoint]] = []
        heapq.heappush(open_set, (0.0, next(self._counter), start))
        came_from: Dict[Waypoint, Waypoint] = {}
        g_score: Dict[Waypoint, float] = {start: 0.0}
        visited: set[Tuple[int, int]] = set()

        while open_set:
            _, _, current = heapq.heappop(open_set)
            key = (current.x, current.y)
            if key in visited:
                continue
            visited.add(key)

            if current == target:
                # reconstruct path (excluding start, including target)
                path: List[Waypoint] = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                self.path_queue = deque([(p.x, p.y) for p in path])
                return

            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                neighbor = Waypoint(current.x + dx, current.y + dy)
                tentative = g_score[current] + 1.0
                if tentative < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative
                    f = tentative + self._heuristic(neighbor, target)
                    heapq.heappush(open_set, (f, next(self._counter), neighbor))

        # For open grid this won't happen; if it does, path_queue becomes empty
        self.path_queue.clear()

    def next_step(self) -> Optional[Tuple[int, int]]:
        return self.path_queue.popleft() if self.path_queue else None  # O(1)


class Manipulator:
    """
    Simple manipulator with a STACK of grasp events.
    Includes a test hook to force next pick to fail deterministically.
    """
    def __init__(self):
        self.grasp_history: List[str] = []  # STACK
        self.force_fail_next: bool = False  # test hook

    def pick(self, object_id: str) -> bool:
        if self.force_fail_next:
            self.force_fail_next = False
            return False
        # Simulate occasional failure (10%)
        if random.random() < 0.1:
            return False
        self.grasp_history.append(object_id)
        return True

    def undo_last_grasp(self) -> bool:
        return bool(self.grasp_history.pop()) if self.grasp_history else False


class Communicator:
    def speak(self, text: str) -> None:
        return

    def display(self, text: str) -> None:
        return


class CLI:
    """Front-end command queue for the robot."""
    def __init__(self):
        self.cmd_queue: deque[Dict[str, str]] = deque()  # QUEUE

    def enqueue(self, cmd: Dict[str, str]) -> None:
        self.cmd_queue.append(cmd)

    def read_command(self) -> Optional[Dict[str, str]]:
        return self.cmd_queue.popleft() if self.cmd_queue else None


class Robot:
    def __init__(self, id: str):
        self.id = id
        self.state = RobotState.OFF
        self.battery_level = 100
        self.env = Environment()
        self.memory = MemoryStore()
        self.nav = Navigation()
        self.manip = Manipulator()
        self.comms = Communicator()

    # ---- power & battery helpers ----
    def power_on(self) -> bool:
        if self.state == RobotState.OFF:
            self.state = RobotState.IDLE
            return True
        return False

    def power_off(self) -> bool:
        if self.state != RobotState.OFF:
            self.state = RobotState.OFF
            return True
        return False

    def _drain(self, amount: int) -> None:
        self.battery_level = max(0, self.battery_level - amount)

    def _maybe_enter_charging(self) -> Optional[str]:
        if self.battery_level < 10 and self.state != RobotState.CHARGING:
            self.state = RobotState.CHARGING
            return "LOW BATTERY: entering charging"
        return None

    def tick(self, command: Dict[str, str]) -> str:
        if self.state == RobotState.OFF:
            return "ERROR: Robot is off"

        # Charging progresses regardless of command type
        if self.state == RobotState.CHARGING:
            self.battery_level = min(100, self.battery_level + 5)  # charge 5% per tick
            if self.battery_level >= 95:
                self.state = RobotState.IDLE     # always return to IDLE (predictable)
                return "OK: Charged"
            return f"CHARGING: {self.battery_level}%"

        # If low battery, go charging before processing any command
        low = self._maybe_enter_charging()
        if low:
            return low

        cmd_type = command.get("type")
        if cmd_type == "navigate":
            self._drain(5)
            low = self._maybe_enter_charging()
            if low:
                return low
            self.state = RobotState.MOVING
            try:
                x, y = map(int, command["args"].split(","))
                start = Waypoint(0, 0)
                target = Waypoint(x, y)
                self.nav.plan_path(start, target)
                step = self.nav.next_step()
                self.memory.push_action("NAVIGATE")
                return f"Navigating to {step}" if step else "ERROR: No path"
            except ValueError:
                return "ERROR: Invalid coordinates"

        elif cmd_type == "pick":
            self._drain(5)
            low = self._maybe_enter_charging()
            if low:
                return low
            self.state = RobotState.MANIPULATING
            if self.manip.pick(command["args"]):
                self.memory.push_action("PICK")
                self.state = RobotState.IDLE
                return "OK: Picked object"
            self.state = RobotState.ERROR
            return "ERROR: Grasp failed"

        elif cmd_type == "speak":
            self._drain(1)
            low = self._maybe_enter_charging()
            if low:
                return low
            self.state = RobotState.COMMUNICATING
            self.comms.speak(command["args"])
            self.memory.push_action("SPEAK")
            self.state = RobotState.IDLE
            return "OK: Spoken"

        elif cmd_type == "tick":
            # Background progression (e.g., sensing/charging handled above)
            self.env.sense()
            return "OK: Ticked"

        return "ERROR: Invalid command"


# ---------- Interactive CLI ----------

def main():
    robot = Robot("R1")
    cli = CLI()
    print("Humanoid Robot CLI: 'navigate x,y' | 'pick <object>' | 'speak <text>' | 'power on/off' | 'tick' | 'exit'")
    while True:
        try:
            cmd_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not cmd_input:
            continue
        if cmd_input.lower() == "exit":
            break
        if cmd_input == "power on":
            print("Power on:", robot.power_on())
            continue
        if cmd_input == "power off":
            print("Power off:", robot.power_off())
            continue
        parts = cmd_input.split(" ", 1)
        cmd = {"type": parts[0], "args": parts[1] if len(parts) > 1 else ""}
        cli.enqueue(cmd)
        if cmd := cli.read_command():
            print(robot.tick(cmd))


# ---------- Tests ----------

class TestRobotSystem(unittest.TestCase):
    def setUp(self):
        self.robot = Robot("R1")
        self.cli = CLI()

    def test_power_management(self):
        self.assertEqual(self.robot.state, RobotState.OFF)
        self.assertTrue(self.robot.power_on())
        self.assertEqual(self.robot.state, RobotState.IDLE)
        self.assertTrue(self.robot.power_off())
        self.assertEqual(self.robot.state, RobotState.OFF)

    def test_navigation_returns_steps(self):
        self.robot.power_on()
        cmd = {"type": "navigate", "args": "5,5"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertTrue(result.startswith("Navigating to"))
        nxt = self.robot.nav.next_step()
        self.assertTrue((nxt is None) or isinstance(nxt, tuple))

    def test_manipulation_failure_deterministic(self):
        self.robot.power_on()
        self.robot.manip.force_fail_next = True  # deterministic failure
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "ERROR: Grasp failed")
        self.assertEqual(self.robot.state, RobotState.ERROR)

    def test_manipulation_success_and_undo(self):
        self.robot.power_on()
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        if result == "ERROR: Grasp failed":
            # retry once if random 10% failure hit
            self.robot.state = RobotState.IDLE
            self.cli.enqueue(cmd)
            result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "OK: Picked object")
        self.assertTrue(self.robot.manip.undo_last_grasp())

    def test_communication(self):
        self.robot.power_on()
        cmd = {"type": "speak", "args": "Hello"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "OK: Spoken")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_environment_search(self):
        self.robot.env.objects = [EnvObject("Bottle", "B1", Waypoint(1, 1))]
        self.robot.env.sense()  # update positions
        result = self.robot.env.find_nearest_object("Bottle")
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "B1")

    def test_error_recovery(self):
        self.robot.power_on()
        self.robot.manip.force_fail_next = True
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        self.robot.tick(self.cli.read_command())
        self.assertEqual(self.robot.state, RobotState.ERROR)
        # Recover
        self.robot.state = RobotState.IDLE
        cmd = {"type": "speak", "args": "Recovered"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "OK: Spoken")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_charging_returns_to_idle(self):  # NEW
        self.robot.power_on()
        self.robot.battery_level = 5
        # any command should trigger charging before execution
        out = self.robot.tick({"type": "speak", "args": "trigger low battery"})
        self.assertEqual(self.robot.state, RobotState.CHARGING)
        self.assertIn("LOW BATTERY", out)
        # progress charging via ticks
        while self.robot.state == RobotState.CHARGING:
            out = self.robot.tick({"type": "tick", "args": ""})
        self.assertEqual(self.robot.state, RobotState.IDLE)
        self.assertIn("Charged", out)

    # ---- Property-based tests (Hypothesis) ----

    @given(lists(text(), max_size=5))
    def test_memory_stack_lifo_property(self, actions):
        memory = MemoryStore()
        for a in actions:
            memory.push_action(a)
        for a in reversed(actions):
            self.assertEqual(memory.last_action(), a)

    @given(floats(min_value=-0.2, max_value=0.2))
    def test_sensor_noise_property(self, z):
        env = Environment()
        env.sense(noise=z)  # use injected noise for determinism
        r = env.sensor_readings[-1]
        expected = max(0.0, min(1.0, 0.5 + z))
        self.assertTrue(0.0 <= r <= 1.0)
        self.assertAlmostEqual(r, expected, places=9)


if __name__ == "__main__":
    # If run directly, start CLI. For tests, run: python -m unittest -v
    main()
