import unittest
from hypothesis import given
from hypothesis.strategies import text, lists, floats

# Import uit je module onder test
from robot_system import (
    Robot, CLI, RobotState, EnvObject, Waypoint, MemoryStore, Environment
)

class TestRobotSystem(unittest.TestCase):
    def setUp(self):
        self.robot = Robot("R1")
        self.cli = CLI()

    def test_power_management(self):
        self.assertEqual(self.robot.state, RobotState.OFF)
        self.assertTrue(self.robot.power_on())
        self.assertEqual(self.robot.state, RobotState.IDLE)
        self.assertTrue(self.robot.power_off())
        self.assertEqual(self.robot.state, RobotState.OFF)

    def test_navigation_returns_steps(self):
        self.robot.power_on()
        cmd = {"type": "navigate", "args": "5,5"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertTrue(result.startswith("Navigating to"))
        nxt = self.robot.nav.next_step()
        self.assertTrue((nxt is None) or isinstance(nxt, tuple))

    def test_manipulation_failure_deterministic(self):
        self.robot.power_on()
        self.robot.manip.force_fail_next = True  # deterministische failure
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "ERROR: Grasp failed")
        self.assertEqual(self.robot.state, RobotState.ERROR)

    def test_manipulation_success_and_undo(self):
        self.robot.power_on()
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        if result == "ERROR: Grasp failed":
            # retry één keer als we net 10% pech hadden
            self.robot.state = RobotState.IDLE
            self.cli.enqueue(cmd)
            result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "OK: Picked object")
        self.assertTrue(self.robot.manip.undo_last_grasp())

    def test_communication(self):
        self.robot.power_on()
        cmd = {"type": "speak", "args": "Hello"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "OK: Spoken")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_environment_search(self):
        self.robot.env.objects = [EnvObject("Bottle", "B1", Waypoint(1, 1))]
        self.robot.env.sense()  # update positions
        result = self.robot.env.find_nearest_object("Bottle")
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "B1")

    def test_error_recovery(self):
        self.robot.power_on()
        self.robot.manip.force_fail_next = True
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        self.robot.tick(self.cli.read_command())
        self.assertEqual(self.robot.state, RobotState.ERROR)
        # herstel
        self.robot.state = RobotState.IDLE
        cmd = {"type": "speak", "args": "Recovered"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "OK: Spoken")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_charging_returns_to_idle(self):
        self.robot.power_on()
        self.robot.battery_level = 5
        out = self.robot.tick({"type": "speak", "args": "trigger low battery"})
        self.assertEqual(self.robot.state, RobotState.CHARGING)
        self.assertIn("LOW BATTERY", out)
        # laden via ticks
        while self.robot.state == RobotState.CHARGING:
            out = self.robot.tick({"type": "tick", "args": ""})
        self.assertEqual(self.robot.state, RobotState.IDLE)
        self.assertIn("Charged", out)

    # ---- Property-based tests (Hypothesis) ----

    @given(lists(text(), max_size=5))
    def test_memory_stack_lifo_property(self, actions):
        memory = MemoryStore()
        for a in actions:
            memory.push_action(a)
        for a in reversed(actions):
            self.assertEqual(memory.last_action(), a)

    @given(floats(min_value=-0.2, max_value=0.2))
    def test_sensor_noise_property(self, z):
        env = Environment()
        env.sense(noise=z)  # deterministische injectie
        r = env.sensor_readings[-1]
        expected = max(0.0, min(1.0, 0.5 + z))
        self.assertTrue
