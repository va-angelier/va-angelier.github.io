import unittest
from robot_system import Robot, CLI, RobotState, Waypoint, EnvObject

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

    def test_pick_low_battery(self):
        self.robot.power_on()
        self.robot.battery_level = 5
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "ERROR: Low battery – please charge")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_pick_object_not_found(self):
        self.robot.power_on()
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "ERROR: Object not found")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_pick_timeout(self):
        self.robot.power_on()
        self.robot.env.objects = [EnvObject("Bottle", "B1", Waypoint(1000, 1000))]
        self.robot.nav.timeout_counter = 100  # Force timeout
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "ERROR: No path to target")
        self.assertEqual(self.robot.state, RobotState.ERROR)

    def test_pick_success(self):
        self.robot.power_on()
        self.robot.env.objects = [EnvObject("Bottle", "B1", Waypoint(1, 1))]
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "OK: Picked object")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_navigation(self):
        self.robot.power_on()
        cmd = {"type": "navigate", "args": "5,5"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertTrue(result.startswith("Navigating to"))
        self.assertEqual(self.robot.state, RobotState.MOVING)

    def test_tick_command(self):
        self.robot.power_on()
        cmd = {"type": "tick", "args": ""}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "Tick executed")
        self.assertEqual(self.robot.state, RobotState.IDLE)

if __name__ == "__main__":
    unittest.main()