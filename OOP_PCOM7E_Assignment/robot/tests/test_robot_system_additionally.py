import unittest
from collections import deque
from robot.robot_system import (
    Robot, RobotState, Navigation, Manipulator, Environment, EnvObject, Waypoint
)

# --- Stubs to force edge-cases ---
class NavNoPath(Navigation):
    def plan_path(self, start, target, env: Environment) -> bool:
        return False  # triggers "No path to target"

class NavTimeout(Navigation):
    def plan_path(self, start, target, env: Environment) -> bool:
        # Pretend planning succeeded, but hit the timeout branch in Robot.tick
        self.timeout_counter = 1000
        return True

class ManipFail(Manipulator):
    def pick(self, object_id: str) -> bool:
        return False  # triggers "Grasp failed"

# --- Tests ---

def test_off_state_requires_power_on():
    r = Robot("R1")  # default OFF
    out = r.tick({"type": "navigate", "args": "1,2"})
    assert "Robot is off" in out

def test_low_battery_guard_blocks_navigate():
    r = Robot("R1"); r.power_on()
    r.battery_level = 5
    out = r.tick({"type": "navigate", "args": "1,2"})
    assert "Low battery" in out

def test_no_path_sets_error_state():
    r = Robot("R1"); r.power_on()
    r.nav = NavNoPath()
    out = r.tick({"type": "navigate", "args": "9,9"})
    assert "No path to target" in out and r.state == RobotState.ERROR

def test_timeout_branch_sets_error_state():
    r = Robot("R1"); r.power_on()
    r.nav = NavTimeout()
    out = r.tick({"type": "navigate", "args": "2,3"})
    assert "No path to target" in out and r.state == RobotState.ERROR

def test_invalid_coordinates():
    r = Robot("R1"); r.power_on()
    out = r.tick({"type": "navigate", "args": "x"})
    assert "Invalid coordinates" in out and r.state == RobotState.IDLE

def test_busy_navigate_resets_to_idle():
    r = Robot("R1"); r.power_on()
    r.state = RobotState.MOVING
    out = r.tick({"type": "navigate", "args": "1,1"})
    assert "robot is busy" in out.lower() and r.state == RobotState.IDLE

def test_pick_object_not_found():
    r = Robot("R1"); r.power_on()
    out = r.tick({"type": "pick", "args": "bottle"})
    assert "Object not found" in out and r.state == RobotState.IDLE

def test_grasp_failure_sets_error_and_reports():
    r = Robot("R1"); r.power_on()
    # add an object so "find_nearest_object" succeeds
    obj = EnvObject(kind="bottle", id="b1", position=Waypoint(1, 1))
    r.env.objects.append(obj); r.env.object_index[obj.id] = obj
    r.nav = Navigation()     # plan_path likely True (unless obstacles)
    r.manip = ManipFail()    # force failure
    out = r.tick({"type": "pick", "args": "bottle"})
    assert "Grasp failed" in out and r.state == RobotState.ERROR

def test_speak_ok_and_memory_push():
    r = Robot("R1"); r.power_on()
    out = r.tick({"type": "speak", "args": "hello"})
    assert "OK: Spoken" in out
    assert r.state == RobotState.IDLE
    assert r.memory.breadcrumbs and r.memory.breadcrumbs[-1] == "SPEAK"

def test_navigation_timeout_sets_error():
    robot = Robot("R1")
    robot.power_on()
    robot.env.obstacles = [(x, y) for x in range(10) for y in range(10)]  # Block all paths
    result = robot.tick({"type": "navigate", "args": "5,5"})
    assert robot.state == RobotState.ERROR
    assert "No path to target" in result

def test_error_recovery_to_idle():
    robot = Robot("R1")
    robot.power_on()
    robot.battery_level = 20  # Ensure sufficient battery
    robot.state = RobotState.ERROR
    result = robot.tick({"type": "tick", "args": ""})
    assert robot.state == RobotState.IDLE
    assert "OK: Recovered to IDLE" in result

def test_error_recovery_low_battery_stays_error():
    r = Robot("R1"); r.power_on()
    r.state = RobotState.ERROR
    r.battery_level = 5
    out = r.tick({"type": "tick", "args": ""})
    assert "Cannot recover" in out
    assert r.state == RobotState.ERROR

# 1) A* heuristic penalty branch (target/start gemarkeerd als obstacle)
def test_astar_heuristic_penalty_branch():
    from robot.robot_system import AStarPlanner
    env = Environment()
    # Maak target een obstacle zodat heuristic() het penalty-pad neemt
    env.obstacles = [(0, 1)]
    nav = Navigation(AStarPlanner())
    ok = nav.plan_path(Waypoint(0, 0), Waypoint(0, 1), env)
    # Verwacht geen pad (target is obstacle), maar de heuristic-penalty is wel geraakt
    assert ok is False

# 2) Manipulator undo pad (True en False varianten)
def test_manipulator_undo_last_grasp_true_and_false():
    m = Manipulator()
    assert m.undo_last_grasp() is False  # leeg
    m.grasp_history.append("obj1")
    assert m.undo_last_grasp() is True   # nu verwijdert hij er één

# 3) Waypoint helpers dekken (__repr__ en to_tuple)
def test_waypoint_repr_and_tuple():
    w = Waypoint(2, 3)
    assert w.to_tuple() == (2, 3)
    r = repr(w)
    assert "Waypoint" in r and "2" in r and "3" in r

# 4) power_off reset van flags (charging/docking)
def test_power_off_clears_charging_and_docking_flags():
    r = Robot("R1"); r.power_on()
    r.state = RobotState.CHARGING
    r.charging = True
    r.navigating_to_charger = True
    assert r.power_off() is True
    assert r.state == RobotState.OFF
    assert r.charging is False and r.navigating_to_charger is False

# 5) Navigate succesvolle planning maar next_step() geeft None → "ERROR: No path"
class NavNoStep(Navigation):
    def plan_path(self, start, target, env):
        # Doe alsof planning gelukt is, maar geef geen stappen terug
        self.timeout_counter = 0
        self.path_queue = deque()  # leeg => next_step() -> None
        return True

def test_navigate_no_step_branch_returns_error_no_path():
    r = Robot("R1"); r.power_on()
    r.nav = NavNoStep()
    out = r.tick({"type": "navigate", "args": "1,1"})
    assert "ERROR: No path" in out
    assert r.state == RobotState.IDLE