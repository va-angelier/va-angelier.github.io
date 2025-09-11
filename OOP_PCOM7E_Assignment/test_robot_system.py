import unittest
from robot_system import Robot, CLI, RobotState, Waypoint, EnvObject


class TestRobotSystem(unittest.TestCase):
    def setUp(self):
        self.robot = Robot("R1")
        self.cli = CLI()

    def test_power_management(self):
        print("Debug: Testing power management")
        self.assertEqual(self.robot.state, RobotState.OFF)
        self.assertTrue(self.robot.power_on())
        self.assertEqual(self.robot.state, RobotState.IDLE)
        self.assertTrue(self.robot.power_off())
        self.assertEqual(self.robot.state, RobotState.OFF)

    def test_pick_low_battery(self):
        print("Debug: Testing pick with low battery")
        self.robot.power_on()
        self.robot.battery_level = 5
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "ERROR: Low battery – please charge")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_pick_object_not_found(self):
        print("Debug: Testing pick with object not found")
        self.robot.power_on()
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "ERROR: Object not found")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_pick_timeout(self):
        print("Debug: Testing pick with timeout")
        self.robot.power_on()
        self.robot.env.objects = [EnvObject("Bottle", "B1",
                                          Waypoint(1000, 1000))]
        self.robot.nav.timeout_counter = 1000
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "ERROR: No path to target")
        self.assertEqual(self.robot.state, RobotState.ERROR)

    def test_pick_success(self):
        print("Debug: Testing pick success")
        self.robot.power_on()
        self.robot.env.objects = [EnvObject("Bottle", "B1",
                                          Waypoint(1, 1))]
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "OK: Picked object")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_navigation(self):
        print("Debug: Testing navigation")
        self.robot.power_on()
        cmd = {"type": "navigate", "args": "5,5"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertTrue(result.startswith("Navigating to"))
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_navigation_during_manipulating(self):
        print("Debug: Testing navigation during manipulation")
        self.robot.power_on()
        self.robot.state = RobotState.MANIPULATING
        cmd = {"type": "navigate", "args": "5,5"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "ERROR: Cannot navigate, robot is busy")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_tick_command(self):
        print("Debug: Testing tick command")
        self.robot.power_on()
        cmd = {"type": "tick", "args": ""}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "Tick executed")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_navigation_with_obstacle(self):
        print("Debug: Testing navigation with obstacle")
        self.robot.power_on()
        self.robot.env.obstacles = [(1, 1)]
        cmd = {"type": "navigate", "args": "2,2"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertTrue(result.startswith("Navigating to") or
                        result == "ERROR: No path to target")
        self.assertEqual(self.robot.state, RobotState.IDLE)

    def test_object_lookup_by_id(self):
        print("Debug: Testing object lookup by ID")
        self.robot.power_on()
        obj = EnvObject("Bottle", "B1", Waypoint(1, 1))
        self.robot.env.objects.append(obj)
        self.robot.env.sense()
        # Test if object_index works (indirectly via find_nearest_object)
        cmd = {"type": "pick", "args": "Bottle"}
        self.cli.enqueue(cmd)
        result = self.robot.tick(self.cli.read_command())
        self.assertEqual(result, "OK: Picked object")
        self.assertEqual(self.robot.state, RobotState.IDLE)


if __name__ == "__main__":
    unittest.main()

# Newline at end of file
