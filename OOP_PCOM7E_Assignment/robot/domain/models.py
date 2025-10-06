"""Domain entities and state for the humanoid robot."""
from __future__ import annotations

import random
from enum import Enum
from typing import Dict, List, Optional, Tuple


class RobotState(Enum):
    """Finite set of operational modes for the robot."""
    OFF = "OFF"
    IDLE = "IDLE"
    MOVING = "MOVING"
    MANIPULATING = "MANIPULATING"
    COMMUNICATING = "COMMUNICATING"
    CHARGING = "CHARGING"
    ERROR = "ERROR"


class Waypoint:
    """Immutable waypoint used by planners and navigation."""
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if not isinstance(other, Waypoint):
            return NotImplemented
        return (self.x, self.y) < (other.x, other.y)

    def __eq__(self, other):
        return isinstance(other, Waypoint) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Waypoint(x={self.x}, y={self.y})"

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


class EnvObject:
    """Environment object with an identifier and position."""
    # pylint: disable=too-few-public-methods

    def __init__(self, kind: str, id: str, position: Waypoint):  # pylint: disable=redefined-builtin
        self.kind = kind
        self.id = id
        self.position = position


class Environment:
    """Holds world state, objects and obstacle grid, and exposes sensing APIs."""

    def __init__(self):
        self.objects: List[EnvObject] = []
        self.object_index: Dict[str, EnvObject] = {}
        self.sensor_readings: List[float] = []
        self.obstacles: List[Tuple[int, int]] = [(2, 2), (3, 3)]

    def sense(self) -> None:
        """Append a noisy sensor reading and rebuild the object index."""
        noise = random.gauss(mu=0, sigma=0.1)
        self.sensor_readings.append(0.5 + noise)
        for obj in self.objects:
            self.object_index[obj.id] = obj

    def find_nearest_object(self, kind: str) -> Optional[EnvObject]:
        """Return closest object of the given kind (Manhattan distance) or None."""
        k = (kind or "").lower()
        nearest: Optional[EnvObject] = None
        min_dist = float("inf")
        for obj in self.objects:
            if (obj.kind or "").lower() == k:
                d = abs(obj.position.x) + abs(obj.position.y)
                if d < min_dist:
                    min_dist = d
                    nearest = obj
        return nearest

    def is_obstacle(self, x: int, y: int) -> bool:
        return (x, y) in self.obstacles


class MemoryStore:
    """Very small store for actions and facts."""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.facts: List[str] = []
        self.breadcrumbs: List[str] = []

    def push_action(self, action: str) -> None:
        self.breadcrumbs.append(action)

    def last_action(self) -> Optional[str]:
        return self.breadcrumbs.pop() if self.breadcrumbs else None
