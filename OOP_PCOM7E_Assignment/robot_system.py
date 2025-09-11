import random
from collections import deque
from typing import List, Optional, Dict
from enum import Enum
import heapq
import math


class RobotState(Enum):
    OFF = "OFF"
    IDLE = "IDLE"
    MOVING = "MOVING"
    MANIPULATING = "MANIPULATING"
    COMMUNICATING = "COMMUNICATING"
    ERROR = "ERROR"


class Waypoint:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


class EnvObject:
    def __init__(self, kind: str, id: str, position: Waypoint):
        self.kind = kind
        self.id = id
        self.position = position


class Environment:
    def __init__(self):
        self.objects: List[EnvObject] = []
        self.sensor_readings: List[float] = []

    def sense(self) -> None:
        print("Debug: Sensing environment")
        noise = random.gauss(mu=0, sigma=0.1)
        self.sensor_readings.append(0.5 + noise)
        for obj in self.objects:
            obj.position.x += int(random.gauss(0, 1))
            obj.position.y += int(random.gauss(0, 1))

    def find_nearest_object(self, kind: str) -> Optional[EnvObject]:
        print(f"Debug: Searching for object of kind {kind}")
        for obj in self.objects:
            if obj.kind == kind:
                return obj
        return None


class MemoryStore:
    def __init__(self):
        self.facts: List[str] = []
        self.breadcrumbs: List[str] = []

    def push_action(self, action: str) -> None:
        self.breadcrumbs.append(action)

    def last_action(self) -> Optional[str]:
        return self.breadcrumbs.pop() if self.breadcrumbs else None


class Navigation:
    def __init__(self):
        self.path_queue: deque = deque()
        self.timeout_counter = 0

    def plan_path(self, start: Waypoint, target: Waypoint) -> bool:
        print(f"Debug: Planning path from {start.x},{start.y} to "
              f"{target.x},{target.y}")
        def heuristic(a: Waypoint, b: Waypoint) -> float:
            return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, target)}
        self.timeout_counter = 0
        max_iterations = 1000

        while open_set and self.timeout_counter < max_iterations:
            self.timeout_counter += 1
            current_f, current = heapq.heappop(open_set)
            if current.x == target.x and current.y == target.y:
                print("Debug: Path found")
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                self.path_queue = deque([(p.x, p.y) for p in path])
                return True
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = Waypoint(current.x + dx, current.y + dy)
                tentative_g_score = g_score.get(current, float("inf")) + 1
                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = (tentative_g_score +
                                        heuristic(neighbor, target))
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        print("Debug: No path found, timeout reached")
        return False

    def next_step(self) -> Optional[tuple]:
        return self.path_queue.popleft() if self.path_queue else None


class Manipulator:
    def __init__(self):
        self.grasp_history: List[str] = []

    def pick(self, object_id: str) -> bool:
        print(f"Debug: Attempting to pick {object_id}")
        if random.random() < 0.1:
            return False
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
        self.cmd_queue: deque = deque()

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

    def tick(self, command: Dict[str, str]) -> str:
        print(f"Debug: Processing command {command}")
        if self.state == RobotState.OFF:
            return "ERROR: Robot is off"
        cmd_type = command.get("type")
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
                if (not self.nav.plan_path(start, target) or
                    self.nav.timeout_counter >= 1000):
                    self.state = RobotState.ERROR
                    return "ERROR: No path to target"
                step = self.nav.next_step()
                self.memory.push_action("NAVIGATE")
                self.battery_level -= 5
                self.state = RobotState.IDLE
                return f"Navigating to {step}" if step else "ERROR: No path"
            except ValueError:
                self.state = RobotState.IDLE
                return "ERROR: Invalid coordinates"
        elif cmd_type == "pick":
            if self.state != RobotState.IDLE:
                self.state = RobotState.IDLE
                return "ERROR: Cannot pick, robot is busy"
            self.state = RobotState.MANIPULATING
            if self.battery_level < 10:
                self.state = RobotState.IDLE
                return "ERROR: Low battery – please charge"
            obj = self.env.find_nearest_object(command["args"])
            if not obj:
                self.state = RobotState.IDLE
                return "ERROR: Object not found"
            if (not self.nav.plan_path(Waypoint(0, 0), obj.position) or
                self.nav.timeout_counter >= 1000):
                self.state = RobotState.ERROR
                return "ERROR: No path to target"
            if not self.manip.pick(command["args"]):
                self.state = RobotState.ERROR
                return "ERROR: Grasp failed"
            self.memory.push_action("PICK")
            self.state = RobotState.IDLE
            self.battery_level -= 5
            return "OK: Picked object"
        elif cmd_type == "speak":
            if self.state != RobotState.IDLE:
                self.state = RobotState.IDLE
                return "ERROR: Cannot speak, robot is busy"
            self.state = RobotState.COMMUNICATING
            self.comms.speak(command["args"])
            self.memory.push_action("SPEAK")
            self.state = RobotState.IDLE
            self.battery_level -= 2
            return "OK: Spoken"
        elif cmd_type == "tick":
            return "Tick executed"
        self.state = RobotState.IDLE
        return "ERROR: Invalid command"


# Interactive CLI loop
def main():
    robot = Robot("R1")
    cli = CLI()
    print("Humanoid Robot CLI: Type commands (e.g., 'navigate 5,5', "
          "'pick bottle', 'speak hello', 'power on/off', 'tick', "
          "'exit')")
    while True:
        cmd_input = input("> ")
        if cmd_input == "exit":
            break
        if cmd_input == "power on":
            print("Power on:", robot.power_on())
            continue
        if cmd_input == "power off":
            print("Power off:", robot.power_off())
            continue
        parts = cmd_input.split(" ", 1)
        cmd = {"type": parts[0], "args": parts[1] if len(parts) > 1
               else ""}
        cli.enqueue(cmd)
        if cmd := cli.read_command():
            print(robot.tick(cmd))


if __name__ == "__main__":
    main()

# Newline at end of file
