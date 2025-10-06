"""Navigation service that orchestrates planning and path execution."""
from __future__ import annotations

from collections import deque
from typing import Deque, Optional, Tuple, Iterable

from robot.domain.models import Waypoint, Environment
from robot.services.planning import PathPlanner, AStarPlanner


class Navigator:
    """Orchestrates planning via an injected PathPlanner."""

    def __init__(self, planner: Optional[PathPlanner] = None):
        self.path_queue: Deque[Tuple[int, int]] = deque()
        self.timeout_counter = 0
        self.planner: PathPlanner = planner or AStarPlanner()

    # ---------- Backwards-compatible one-shot navigation for tests ----------
    def navigate(self, start: Tuple[int, int] | Waypoint,
                 goal: Tuple[int, int] | Waypoint) -> None:
        """Compatibility helper used by tests:
        - If planner provides `.plan(start, goal)`, iterate over returned path
          and call `_drive_to` for each step.
        - Otherwise, fall back to computing a path with an ephemeral Environment.
        """
        # normalise naar platte tuples
        s = start.to_tuple() if hasattr(start, "to_tuple") else tuple(start)  # type: ignore[arg-type]
        g = goal.to_tuple() if hasattr(goal, "to_tuple") else tuple(goal)    # type: ignore[arg-type]

        # 1) Oud pad: planner heeft .plan()
        if hasattr(self.planner, "plan"):
            path: Iterable[Tuple[int, int]] = self.planner.plan(s, g)  # type: ignore[attr-defined]
            for p in path:
                self._drive_to(p)
            return

        # 2) Nieuwe pad: gebruik compute via plan_path()
        env = Environment()
        if self.plan_path(Waypoint(*s), Waypoint(*g), env):
            while True:
                step = self.next_step()
                if step is None:
                    break
                self._drive_to(step)

    # ----------------------------------------------------------------------
    def plan_path(self, start: Waypoint, target: Waypoint, env: Environment) -> bool:
        """Plan a path and store it in the internal queue."""
        coords = self.planner.compute(start, target, env)
        self.timeout_counter = getattr(self.planner, "timeout_counter", 0)
        if coords is None:
            return False
        self.path_queue = coords
        return True

    def next_step(self) -> Optional[Tuple[int, int]]:
        """Pop next (x,y) waypoint if available."""
        return self.path_queue.popleft() if self.path_queue else None

    # Protected hook — tests kunnen deze overriden (Spy pattern)
    def _drive_to(self, p: Tuple[int, int]) -> None:  # pragma: no cover
        """Drive to a single (x,y) coordinate (no-op by default)."""
        # In productie zou hier een echte driver-call zitten; tests overriden deze.
        return
