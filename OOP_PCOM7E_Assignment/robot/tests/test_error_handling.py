# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=multiple-statements,wrong-import-position,unused-import,duplicate-code
# pylint: disable=too-few-public-methods

from robot.robot_system import Robot, Navigation, PathPlanner, RobotState

class BoomPlanner(PathPlanner):
    def compute(self, start, target, env):
        raise RuntimeError("boom")

def test_unexpected_planning_error_is_handled():
    """Test when planning error occurs"""
    r = Robot("R1"); r.power_on()
    r.nav = Navigation(BoomPlanner())
    out = r.tick({"type": "navigate", "args": "1,1"})
    assert "Internal planning error" in out
    assert r.state == RobotState.ERROR
