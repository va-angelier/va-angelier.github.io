# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=multiple-statements,wrong-import-position,unused-import,duplicate-code

from robot.robot_system import (
    Navigation, AStarPlanner, GreedyPlanner, Environment, Waypoint,
    Robot, RobotState
)

def test_astar_success_and_blocked():
    env = Environment()
    # SUCCES: eenvoudige route
    nav = Navigation(AStarPlanner())
    assert nav.plan_path(Waypoint(0,0), Waypoint(1,1), env) is True
    assert nav.next_step() is not None

    # GEEN PAD: maak een muur rond target
    env2 = Environment()
    target = Waypoint(1, 1)
    # blokkeer alle buren van (1,1) plus de cel zelf
    env2.obstacles = [(1,1), (0,1), (2,1), (1,0), (1,2)]
    nav2 = Navigation(AStarPlanner())
    assert nav2.plan_path(Waypoint(0,0), target, env2) is False

def test_greedy_no_move_returns_none():
    env = Environment()
    # Greedy kan alleen 1 stap naar +x of +y, blok dat beide
    env.obstacles = [(1,0), (0,1)]
    nav = Navigation(GreedyPlanner())
    assert nav.plan_path(Waypoint(0,0), Waypoint(1,1), env) is False

def test_robot_with_injected_greedy_planner():
    r = Robot("R1"); r.power_on()
    r.nav = Navigation(GreedyPlanner())
    out = r.tick({"type": "navigate", "args": "1,0"})
    assert "Navigating" in out
    assert r.state in (RobotState.IDLE, RobotState.MOVING)
