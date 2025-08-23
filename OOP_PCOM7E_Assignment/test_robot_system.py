import unittest
from hypothesis import given, strategies as st
from robot_system import Robot, RobotState, CLI, CmdType, Environment

class TestRobotSystem(unittest.TestCase):
    def setUp(self):
        self.robot = Robot("R1")
        self.cli = CLI()

    def test_power_cycle(self):
        self.assertEqual(self.robot.state, RobotState.OFF)
        self.assertTrue(self.robot.power_on())
        self.assertEqual(self.robot.state, RobotState.IDLE)
        self.assertTrue(self.robot.power_off())
        self.assertEqual(self.robot.state, RobotState.OFF)

    def test_charging_flow(self):
        self.robot.power_on()
        self.robot.battery_level = 5
        msg = self.robot.tick({"type": CmdType.SPEAK.value, "args":"hi"})
        self.assertIn("LOW BATTERY", msg)
        self.assertEqual(self.robot.state, RobotState.CHARGING)
        for _ in range(10):
            out = self.robot.tick({"type": CmdType.TICK.value})
            if "OK: Charged" in out:
                break
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_navigation(self):
        self.robot.power_on()
        out = self.robot.tick({"type": CmdType.NAVIGATE.value, "args":"2,2"})
        self.assertTrue(out.startswith("Navigating to"))
        self.assertEqual(self.robot.state, RobotState.MOVING)

    def test_pick_success_and_undo(self):
        self.robot.power_on()
        out = self.robot.tick({"type": CmdType.PICK.value, "args":"Bottle"})
        self.assertEqual(out, "OK: Picked object")
        self.assertTrue(self.robot.manip.undo_last_grasp())

    def test_pick_failure(self):
        self.robot.power_on()
        self.robot.manip.force_fail_next = True
        out = self.robot.tick({"type": CmdType.PICK.value, "args":"Box"})
        self.assertEqual(out, "ERROR: Grasp failed")
        self.assertEqual(self.robot.state, RobotState.ERROR)

    def test_environment_clip(self):
        env = Environment()
        env.sense(noise=10.0)
        self.assertLessEqual(env.sensor_readings[-1], 1.0)

    def test_navigation_ticks_progress_and_arrive(self):
        self.robot.power_on()
        # Navigeren verplaatst niet direct meer; alleen bevestigen van doel.
        out = self.robot.tick({"type": "navigate", "args": "0,3"})
        self.assertEqual(out, "Navigating to (0, 3)")
        # Eerste tick: eerste stap
        out = self.robot.tick({"type": "tick"})
        self.assertTrue(out.startswith("Step to "), f"Unexpected: {out}")
        # Ticks totdat we 'Arrived' zien (max 10 om infinite loops te voorkomen)
        for _ in range(10):
            out = self.robot.tick({"type": "tick"})
            if out == "Arrived":
                break
        self.assertEqual(out, "Arrived")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    @given(st.lists(st.text(), max_size=5))
    def test_memory_stack_lifo(self, xs):
        r = Robot("R2"); r.power_on()
        for a in xs: r.memory.push_action(a)
        for a in reversed(xs):
            if xs:
                self.assertEqual(r.memory.last_action(), a)

if __name__ == "__main__":
    unittest.main()
