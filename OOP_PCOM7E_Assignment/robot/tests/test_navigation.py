import unittest
from robot.services.navigation import Navigator

class FakePlanner:
    def plan(self, s, g): return [s, (1,1), g]

class SpyNavigator(Navigator):
    def __init__(self, planner): super().__init__(planner); self.called=[]
    def _drive_to(self, p): self.called.append(p)

class TestNavigator(unittest.TestCase):
    def test_navigate_reaches_goal(self):
        nav = SpyNavigator(FakePlanner())
        nav.navigate((0,0),(2,2))
        self.assertEqual(nav.called[-1], (2,2))

if __name__ == "__main__":
    unittest.main()
