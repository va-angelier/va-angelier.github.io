# test_robot_system.py
import unittest
from robot_system import Robot, RobotState

class TestSmoke(unittest.TestCase):
    def test_power_cycle(self):
        r = Robot("R1")
        self.assertTrue(r.power_on())
        self.assertEqual(r.state, RobotState.IDLE)
