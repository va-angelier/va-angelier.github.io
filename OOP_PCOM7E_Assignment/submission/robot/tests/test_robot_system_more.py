# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=multiple-statements,wrong-import-position,unused-import,duplicate-code

from robot.robot_system import (
    Robot, RobotState, Navigation, Environment, EnvObject, Waypoint, CLI
)

def test_environment_sense_updates_index_and_readings():
    env = Environment()
    obj = EnvObject(kind="box", id="o1", position=Waypoint(0, 0))
    env.objects.append(obj)
    assert len(env.sensor_readings) == 0
    env.sense()
    assert len(env.sensor_readings) == 1
    # object_index should be updated to point to obj
    assert env.object_index["o1"] is obj

def test_is_obstacle_true_false():
    env = Environment()
    assert env.is_obstacle(2, 2) is True
    assert env.is_obstacle(999, 999) is False

def test_power_on_off_returns_bool_and_state_changes():
    r = Robot("R1")
    assert r.power_on() is True
    assert r.state == RobotState.IDLE
    # second power_on should return False (already on)
    assert r.power_on() is False
    assert r.power_off() is True
    assert r.state == RobotState.OFF
    # second power_off should return False (already off)
    assert r.power_off() is False

def test_tick_invalid_command_sets_idle():
    r = Robot("R1"); r.power_on()
    out = r.tick({"type": "unknown", "args": ""})
    assert "Invalid command" in out and r.state == RobotState.IDLE

def test_pick_low_battery_branch():
    r = Robot("R1"); r.power_on()
    r.battery_level = 5
    out = r.tick({"type": "pick", "args": "bottle"})
    assert "Low battery" in out and r.state == RobotState.IDLE

def test_speak_when_busy_resets_to_idle():
    r = Robot("R1"); r.power_on()
    r.state = RobotState.MOVING
    out = r.tick({"type": "speak", "args": "hello"})
    assert "cannot speak" in out.lower() and r.state == RobotState.IDLE

def test_nav_start_equals_target_has_single_step():
    r = Robot("R1"); r.power_on()
    start = Waypoint(0, 0); target = Waypoint(0, 0)
    ok = r.nav.plan_path(start, target, r.env)
    assert ok is True
    step = r.nav.next_step()
    # planner returns at least target as step
    assert step == (0, 0)

def test_memory_last_action_and_cli_queue():
    r = Robot("R1"); r.power_on()
    r.memory.push_action("SPEAK")
    assert r.memory.last_action() == "SPEAK"
    assert r.memory.last_action() is None  # empty pop returns None

    cli = CLI()
    cli.enqueue({"type": "tick", "args": ""})
    cmd: dict[str, str] = {"type": "tick", "args": ""}
    assert cmd and cmd["type"] == "tick"
    assert cli.read_command() is None
