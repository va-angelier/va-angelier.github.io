"""Actuator adapters: manipulator and communicator."""
from __future__ import annotations

from typing import List


class Manipulator:
    """Demo manipulator API (pick/undo)."""

    def __init__(self):
        self.grasp_history: List[str] = []

    def pick(self, object_id: str) -> bool:
        """Attempt to grasp the given object id."""
        self.grasp_history.append(object_id)
        return True

    def undo_last_grasp(self) -> bool:
        """Undo the previous grasp if any."""
        return bool(self.grasp_history.pop()) if self.grasp_history else False


class Communicator:
    """Demo communications adapter (speak/display)."""

    def speak(self, text: str) -> None:
        """Say the given text (debug output)."""
        print(f"Debug: Speaking {text}")

    def display(self, text: str) -> None:
        """Display the given text (debug output)."""
        print(f"Debug: Displaying {text}")
