"""Domain model for robot state."""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_SPEED: float = 0.0
DEFAULT_POSITION: float = 0.0


@dataclass(slots=True)
class RobotState:
    """Store robot speed and one-dimensional position."""

    speed: float = DEFAULT_SPEED
    position: float = DEFAULT_POSITION
