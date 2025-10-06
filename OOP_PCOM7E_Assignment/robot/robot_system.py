"""Compatibility shim: re-export types from the layered modules."""
from __future__ import annotations

# Domain
from robot.domain.models import RobotState, Waypoint, EnvObject, Environment, MemoryStore

# Services
from robot.services.planning import PathPlanner, AStarPlanner, GreedyPlanner
from robot.services.navigation import Navigator as Navigation  # keep old name
from robot.services.actuators import Manipulator, Communicator
from robot.services.events import EventBus  # keep if you already have this file

# Controller
from robot.controller import Robot

# Interface
from robot.interface.cli import CLI

__all__ = [
    "RobotState",
    "Waypoint",
    "EnvObject",
    "Environment",
    "MemoryStore",
    "PathPlanner",
    "AStarPlanner",
    "GreedyPlanner",
    "Navigation",
    "Manipulator",
    "Communicator",
    "EventBus",
    "Robot",
    "CLI",
]
