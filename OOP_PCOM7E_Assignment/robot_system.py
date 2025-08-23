from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Tuple
import heapq
import random

# ----- Enums -----
class RobotState(Enum):
    OFF = "OFF"
    IDLE = "IDLE"
    MOVING = "MOVING"
    MANIPULATING = "MANIPULATING"
    COMMUNICATING = "COMMUNICATING"
    CHARGING = "CHARGING"
    ERROR = "ERROR"

class CmdType(Enum):
    NAVIGATE = "navigate"
    PICK = "pick"
    SPEAK = "speak"
    TICK = "tick"   # heartbeat / charging step

# ----- Value objects -----
@dataclass(frozen=True, eq=True)
class Waypoint:
    x: int
    y: int

@dataclass
class EnvObject:
    kind: str
    id: str
    position: Waypoint

# ----- Environment -----
class Environment:
    def __init__(self) -> None:
        self.objects: List[EnvObject] = []
        self.sensor_readings: List[float] = []

    def sense(self, noise: Optional[float] = None) -> None:
        # 0.5 ± Gaussian noise; clamp to [0,1]
        val = 0.5 + (noise if noise is not None else random.gauss(0, 0.1))
        self.sensor_readings.append(max(0.0, min(1.0, val)))

    def find_nearest_object(self, kind: str) -> Optional[EnvObject]:
        # Simple linear search (OK voor kleine sets)
        for obj in self.objects:
            if obj.kind == kind:
                return obj
        return None

# ----- MemoryStore (stack + list) -----
class MemoryStore:
    def __init__(self) -> None:
        self.facts: List[str] = []
        self.breadcrumbs: List[str] = []  # LIFO stack

    def push_action(self, action: str) -> None:
        self.breadcrumbs.append(action)

    def last_action(self) -> Optional[str]:
        return self.breadcrumbs.pop() if self.breadcrumbs else None

# ----- Navigation (A* met Manhattan) -----
class Navigation:
    def __init__(self) -> None:
        self.path_queue: deque[Tuple[int, int]] = deque()

    def plan_path(self, start: Waypoint, target: Waypoint) -> None:
        def h(a: Tuple[int, int], b: Tuple[int, int]) -> int:
            return abs(b[0]-a[0]) + abs(b[1]-a[1])

        s = (start.x, start.y)
        t = (target.x, target.y)
        openh: List[Tuple[int, Tuple[int, int]]] = [(0, s)]
        came: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g: Dict[Tuple[int, int], int] = {s: 0}
        seen = set()

        while openh:
            _, cur = heapq.heappop(openh)
            if cur in seen:
                continue
            seen.add(cur)
            if cur == t:
                path: List[Tuple[int, int]] = []
                while cur in came:
                    path.append(cur); cur = came[cur]
                path.reverse()
                self.path_queue = deque(path)
                return
            for dx, dy in ((0,1),(1,0),(0,-1),(-1,0)):
                nb = (cur[0]+dx, cur[1]+dy)
                tentative = g[cur] + 1
                if tentative < g.get(nb, 10**9):
                    came[nb] = cur
                    g[nb] = tentative
                    f = tentative + h(nb, t)
                    heapq.heappush(openh, (f, nb))

        self.path_queue.clear()  # geen pad

    def next_step(self) -> Optional[Tuple[int,int]]:
        return self.path_queue.popleft() if self.path_queue else None

# ----- Manipulator (stack + geforceerde fail voor tests) -----
class Manipulator:
    def __init__(self) -> None:
        self.grasp_history: List[str] = []
        self.force_fail_next: bool = False

    def pick(self, object_id: str) -> bool:
        if self.force_fail_next:
            self.force_fail_next = False
            return False
        self.grasp_history.append(object_id)
        return True

    def undo_last_grasp(self) -> bool:
        return bool(self.grasp_history.pop()) if self.grasp_history else False

# ----- Communicator -----
class Communicator:
    def speak(self, text: str) -> None: return
    def display(self, text: str) -> None: return

# ----- CLI (queue) -----
class CLI:
    def __init__(self) -> None:
        self.cmd_queue: deque[Dict[str, str]] = deque()
    def enqueue(self, cmd: Dict[str, str]) -> None:
        self.cmd_queue.append(cmd)
    def read_command(self) -> Optional[Dict[str, str]]:
        return self.cmd_queue.popleft() if self.cmd_queue else None

# ----- Robot -----
class Robot:
    def __init__(self, id: str) -> None:
        self.id = id
        self.position = Waypoint(0, 0)
        self.state = RobotState.OFF
        self.battery_level = 100
        self.env = Environment()
        self.memory = MemoryStore()
        self.nav = Navigation()
        self.manip = Manipulator()
        self.comms = Communicator()

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

    def tick(self, command: Dict[str, str]) -> str:
        # Keep walking if we're MOVING and we get a tick
        if self.state == RobotState.MOVING and command.get("type") == CmdType.TICK.value:
            step = self.nav.next_step()
            if step is None:
                self.state = RobotState.IDLE
                return "Arrived"
            self.position = Waypoint(step[0], step[1])
            return f"Step to {step}"

        # Charging loop
        if self.state == RobotState.CHARGING:
            if command.get("type") == CmdType.TICK.value:
                self.battery_level = min(100, self.battery_level + 10)
                if self.battery_level >= 95:
                    self.state = RobotState.IDLE
                    return "OK: Charged"
                return f"CHARGING: {self.battery_level}%"
            return "Robot is charging"

        # Low battery guard (except pure TICKs)
        if self.battery_level < 10 and command.get("type") != CmdType.TICK.value:
            self.state = RobotState.CHARGING
            return "LOW BATTERY: entering charging"

        ctype = command.get("type")

        if ctype == CmdType.NAVIGATE.value:
            try:
                x_str, y_str = command.get("args","").split(",")
                target = Waypoint(int(x_str.strip()), int(y_str.strip()))
            except Exception:
                return "ERROR: Invalid coordinates"
            # Plan route vanaf huidige positie, maar nog geen stap zetten.
            self.nav.plan_path(self.position, target)
            self.state = RobotState.MOVING
            self.memory.push_action("NAVIGATE")
            return f"Navigating to ({target.x}, {target.y})"
        
        if ctype == CmdType.PICK.value:
            self.state = RobotState.MANIPULATING
            if self.manip.pick(command.get("args","")):
                self.memory.push_action("PICK")
                self.state = RobotState.IDLE
                return "OK: Picked object"
            self.state = RobotState.ERROR
            return "ERROR: Grasp failed"

        if ctype == CmdType.SPEAK.value:
            self.state = RobotState.COMMUNICATING
            self.comms.speak(command.get("args",""))
            self.memory.push_action("SPEAK")
            self.state = RobotState.IDLE
            return "OK: Spoken"

        if ctype == CmdType.TICK.value:
            return "OK: Idle"

        return "ERROR: Invalid command"

# ----- interactieve CLI -----
def main():
    robot = Robot("R1")
    cli = CLI()
    print("Humanoid Robot CLI — 'power on', 'power off', 'navigate x,y', 'pick <obj>', 'speak <txt>', 'tick', 'exit'")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); break
        if not line: continue
        if line == "exit": break
        if line == "power on":  print("Power on:", robot.power_on());  continue
        if line == "power off": print("Power off:", robot.power_off()); continue
        parts = line.split(" ", 1)
        cmd = {"type": parts[0].lower(), "args": (parts[1] if len(parts)>1 else "")}
        cli.enqueue(cmd)
        print(robot.tick(cli.read_command()))

if __name__ == "__main__":
    main()
