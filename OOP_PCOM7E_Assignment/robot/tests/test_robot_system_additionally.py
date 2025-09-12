import unittest
from robot.robot_system import Robot, CLI, RobotState, Waypoint, EnvObject
# and in the other test:
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
