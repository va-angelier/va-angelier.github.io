# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=multiple-statements,wrong-import-position,unused-import,duplicate-code

from robot.robot_system import Robot, RobotState, EnvObject, Waypoint, Environment, Navigation

def test_auto_charge_after_navigate_when_battery_drops():
    r = Robot("R1"); r.power_on()
    r.battery_level = 12  # na -5 zakt naar 7 < 10
    out = r.tick({"type": "navigate", "args": "1,1"})
    assert "Navigating" in out
    assert "AUTO: Low battery" in out
    assert r.charging is True
    assert r.state == RobotState.MOVING  # onderweg naar laadpunt

def test_auto_charge_after_pick_when_battery_drops():
    r = Robot("R1"); r.power_on()
    # voeg een object toe zodat pick-succespad bereikt wordt
    obj = EnvObject("bottle", "b1", Waypoint(1,1))
    r.env.objects.append(obj); r.env.object_index[obj.id] = obj
    r.battery_level = 12  # na -5 -> 7
    # zorg dat plan_path slaagt
    r.nav = Navigation()
    out = r.tick({"type": "pick", "args": "bottle"})
    # Pick blijft OK, maar meldt auto-laden erbij
    assert "OK: Picked object" in out
    assert "AUTO: Low battery" in out
    assert r.charging is True
    assert r.state == RobotState.MOVING

def _drive_to_charger(r: Robot):
    # voer enkele ticks uit om naar de dock te stappen
    for _ in range(10):
        out = r.tick({"type": "tick"})
        if "Docked: charging started" in out or r.state == RobotState.CHARGING:
            return out
    return out

def _charge_to_full(r: Robot):
    # laad door met ticks
    for _ in range(10):
        out = r.tick({"type": "tick"})
        if "complete" in out.lower() or r.battery_level >= 100:
            return out
    return out

def test_auto_charge_after_navigate_flow():
    r = Robot("R1"); r.power_on()
    r.battery_level = 12  # na -5 -> 7 < 10 → auto-dock
    out = r.tick({"type": "navigate", "args": "1,1"})
    assert "Navigating" in out and "AUTO: Low battery" in out
    assert r.navigating_to_charger is True
    assert r.state == RobotState.MOVING

    dock_out = _drive_to_charger(r)
    assert "Docked: charging started" in dock_out
    assert r.state == RobotState.CHARGING

    charge_out = _charge_to_full(r)
    assert "Charging complete" in charge_out
    assert r.battery_level == 100
    assert r.state == RobotState.IDLE

def test_auto_charge_after_pick_flow():
    r = Robot("R1"); r.power_on()
    # object toevoegen zodat pick slaagt
    obj = EnvObject("bottle", "b1", Waypoint(1, 1))
    r.env.objects.append(obj); r.env.object_index[obj.id] = obj
    r.battery_level = 12  # na -5 -> 7 < 10
    r.nav = Navigation()
    out = r.tick({"type": "pick", "args": "bottle"})
    assert "OK: Picked object" in out and "AUTO: Low battery" in out
    assert r.navigating_to_charger is True
