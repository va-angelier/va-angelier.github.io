"""Lightweight CLI command queue."""
from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Optional


class CLI:
    """Minimal command queue for interactive CLI."""

    def __init__(self):
        self.cmd_queue: Deque[Dict[str, str]] = deque()

    def enqueue(self, cmd: Dict[str, str]) -> None:
        """Push a command onto the queue."""
        self.cmd_queue.append(cmd)

    def read_command(self) -> Optional[Dict[str, str]]:
        """Pop a command from the queue, if any."""
        return self.cmd_queue.popleft() if self.cmd_queue else None
