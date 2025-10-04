from .planning import AStarPlanner  # of RRTPlanner
from ..domain.contracts import PathPlanner

class Navigator:
    def __init__(self, planner: PathPlanner):
        self._planner = planner

    def navigate(self, start, goal):
        for p in self._planner.plan(start, goal):
            self._drive_to(p)

    def _drive_to(self, waypoint): pass
