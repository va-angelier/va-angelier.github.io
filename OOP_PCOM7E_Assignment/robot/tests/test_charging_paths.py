from robot.robot_system import Robot, RobotState

def test_docking_to_charging_and_complete():
    r = Robot("R1"); r.power_on()
    r.battery_level = 12  # na actie zakt hij onder drempel

    # Triggere auto-dock via navigate
    out = r.tick({"type": "navigate", "args": "1,1"})
    assert "AUTO: Low battery" in out
    assert r.navigating_to_charger is True
    assert r.charging is True
    assert r.state == RobotState.MOVING

    # Dock: voer ticks uit tot CHARGING start
    while r.state != RobotState.CHARGING:
        out = r.tick({"type": "tick"})
        # "Auto-docking step ..." of "Docked: charging started"
        assert "Auto-docking" in out or "Docked: charging started" in out

    # Charge to 100%
    seen_progress = False
    while r.state == RobotState.CHARGING:
        out = r.tick({"type": "tick"})
        if "Charging..." in out:
            seen_progress = True

    assert seen_progress, "expect at least one charging progress message"
    assert r.battery_level == 100
    assert r.state == RobotState.IDLE
