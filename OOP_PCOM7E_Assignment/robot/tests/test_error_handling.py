# robot/tests/test_error_handling.py
from robot.robot_system import Robot, Navigation, PathPlanner, RobotState

class BoomPlanner(PathPlanner):
    def compute(self, start, target, env):
        raise RuntimeError("boom")

def test_unexpected_planning_error_is_handled():
    r = Robot("R1"); r.power_on()
    r.nav = Navigation(BoomPlanner())
    out = r.tick({"type": "navigate", "args": "1,1"})
    assert "Internal planning error" in out
    assert r.state == RobotState.ERROR
