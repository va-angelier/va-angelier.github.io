from robot.robot_system import (
    Robot, RobotState, Navigation, Environment, EnvObject, Waypoint, Manipulator
)

# 1) ERROR -> IDLE recovery faalt bij lage batterij (negatieve pad)
def test_error_recovery_low_battery_stays_error():
    r = Robot("R1"); r.power_on()
    r.state = RobotState.ERROR
    r.battery_level = 5
    out = r.tick({"type": "tick", "args": ""})
    assert "Cannot recover" in out
    assert r.state == RobotState.ERROR

# 2) Guard: docking in progress blokkeert andere commands
def test_guard_docking_in_progress_blocks_commands():
    r = Robot("R1"); r.power_on()
    # Trigger auto-dock via pick -> batterij zakt <10
    obj = EnvObject("bottle", "b1", Waypoint(1, 1))
    r.env.objects.append(obj); r.env.object_index[obj.id] = obj
    r.battery_level = 12
    r.tick({"type": "pick", "args": "bottle"})
    # We zitten nu in docking of direct charging; forceer specifiek docking:
    # als pad al leeg is kan CHARGING zijn; zet dan nog 1 stap in de queue
    if not r.navigating_to_charger and r.state == RobotState.CHARGING:
        # zet terug naar docking met 1 kunststap
        r.navigating_to_charger = True
        r.state = RobotState.MOVING
        r.nav.path_queue.clear()
        r.nav.path_queue.append((0, -1))
    # Probeer een ander command dan 'tick'
    out = r.tick({"type": "speak", "args": "hi"})
    assert "Docking in progress" in out

# 3) Guard: robot is charging blokkeert non-tick
def test_guard_robot_is_charging_blocks_non_tick():
    r = Robot("R1"); r.power_on()
    r.state = RobotState.CHARGING
    r.charging = True
    out = r.tick({"type": "navigate", "args": "1,1"})
    assert "Robot is charging" in out
    assert r.state == RobotState.CHARGING

# 4) Generic except-pad in pick: manipulator gooit exception
class BoomManip(Manipulator):
    def pick(self, object_id: str) -> bool:
        raise RuntimeError("boom")

def test_manipulator_exception_is_handled():
    r = Robot("R1"); r.power_on()
    obj = EnvObject("bottle", "b1", Waypoint(1, 1))
    r.env.objects.append(obj); r.env.object_index[obj.id] = obj
    r.manip = BoomManip()
    out = r.tick({"type": "pick", "args": "bottle"})
    assert "Manipulator error" in out
    assert r.state == RobotState.ERROR

# 5) Speak triggert auto-dock (de speak-variant van je auto-charge tests)
def test_speak_can_trigger_auto_dock():
    r = Robot("R1"); r.power_on()
    r.battery_level = 11  # speak trekt -2 => 9 (<10) => auto-dock
    out = r.tick({"type": "speak", "args": "hello"})
    assert "OK: Spoken" in out and "AUTO: Low battery" in out
    assert r.charging is True or r.navigating_to_charger is True
