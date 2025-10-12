"""Path-planning strategies (Strategy pattern)."""
from __future__ import annotations

import heapq
import math
from abc import ABC, abstractmethod
from collections import deque
from typing import Deque, Dict, List, Optional, Tuple
from robot.domain.models import Waypoint, Environment

class PathPlanner(ABC):
    """Abstract base for path-planning strategies."""
    # pylint: disable=too-few-public-methods
    timeout_counter: int = 0

    @abstractmethod
    def compute(
        self, start: Waypoint, target: Waypoint, env: Environment
    ) -> Optional[Deque[Tuple[int, int]]]:
        """Return a deque of (x,y) steps or None if no path."""
        raise NotImplementedError


class AStarPlanner(PathPlanner):
    """A* path planner with obstacle-aware heuristic."""
    # pylint: disable=too-few-public-methods

    def compute(
        self, start: Waypoint, target: Waypoint, env: Environment
    ) -> Optional[Deque[Tuple[int, int]]]:
        # pylint: disable=too-many-locals
        self.timeout_counter = 0

        def heuristic(a: Waypoint, b: Waypoint) -> float:
            # Adaptive weight: increase when local obstacles are dense (simple 3x3 probe)
            blocked = 0
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if env.is_obstacle(a.x + dx, a.y + dy):
                        blocked += 1
            w = 1.0 + 0.05 * blocked  # 1.0..1.45
            d = math.hypot(b.x - a.x, b.y - a.y)
            return d * w

        open_set: List[Tuple[float, Waypoint]] = [(0.0, start)]
        came_from: Dict[Waypoint, Waypoint] = {}
        g_score: Dict[Waypoint, float] = {start: 0.0}
        max_iterations = 1000

        while open_set and self.timeout_counter < max_iterations:
            self.timeout_counter += 1
            _, current = heapq.heappop(open_set)
            if (current.x, current.y) == (target.x, target.y):
                path: List[Waypoint] = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                coords = deque([(p.x, p.y) for p in path] or [(target.x, target.y)])
                return coords

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                n = Waypoint(current.x + dx, current.y + dy)
                if env.is_obstacle(n.x, n.y):
                    continue
                tentative = g_score.get(current, float("inf")) + 1
                if tentative < g_score.get(n, float("inf")):
                    came_from[n] = current
                    g_score[n] = tentative
                    f = tentative + heuristic(n, target)
                    heapq.heappush(open_set, (f, n))
        return None


class GreedyPlanner(PathPlanner):
    """Simple greedy planner for demonstration (polymorphism)."""
    # pylint: disable=too-few-public-methods

    def compute(
        self, start: Waypoint, target: Waypoint, env: Environment
    ) -> Optional[Deque[Tuple[int, int]]]:
        x, y = start.x, start.y
        coords: Deque[Tuple[int, int]] = deque()
        self.timeout_counter = 0
        max_steps = 200
        while (x, y) != (target.x, target.y) and self.timeout_counter < max_steps:
            self.timeout_counter += 1
            moved = False
            if x < target.x and not env.is_obstacle(x + 1, y):
                x += 1
                moved = True
            elif x > target.x and not env.is_obstacle(x - 1, y):
                x -= 1
                moved = True
            elif y < target.y and not env.is_obstacle(x, y + 1):
                y += 1
                moved = True
            elif y > target.y and not env.is_obstacle(x, y - 1):
                y -= 1
                moved = True
            if not moved:
                return None
            coords.append((x, y))
        return coords if (x, y) == (target.x, target.y) else None
