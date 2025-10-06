from typing import Protocol

class PathPlanner(Protocol):
    def plan(self, start: tuple[int,int], goal: tuple[int,int]) -> list[tuple[int,int]]: ...
