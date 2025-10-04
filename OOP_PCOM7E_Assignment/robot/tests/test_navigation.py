# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=multiple-statements,wrong-import-position,unused-import,duplicate-code
# pylint: disable=too-few-public-methods

import unittest
from robot.services.navigation import Navigator

class FakePlanner:
    def plan(self, s, g): return [s, (1,1), g]
    # pylint: disable=too-few-public-methods

class SpyNavigator(Navigator):
    # pylint: disable=too-few-public-methods
    def __init__(self, planner):
        super().__init__(planner)
        self.called = []

    def _drive_to(self, waypoint):
        self.called.append(waypoint)

class TestNavigator(unittest.TestCase):
    """Test Navigation"""
    # pylint: disable=too-few-public-methods
    def test_navigate_reaches_goal(self):
        nav = SpyNavigator(FakePlanner())
        nav.navigate((0,0),(2,2))
        self.assertEqual(nav.called[-1], (2,2))

if __name__ == "__main__":
    unittest.main()
