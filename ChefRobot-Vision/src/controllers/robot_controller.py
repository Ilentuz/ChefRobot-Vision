"""Robot controller with validation and logging."""

from __future__ import annotations

from src.models.robot_state import RobotState
from src.utils.logger import get_project_logger

MAX_ALLOWED_SPEED: float = 100.0
MIN_ALLOWED_SPEED: float = -100.0
MIN_ALLOWED_DURATION: float = 0.0
STOP_SPEED: float = 0.0


class RobotController:
    """Control robot movement through state transitions."""

    def __init__(self) -> None:
        """Initialize controller with a default robot state."""
        self._state: RobotState = RobotState()
        self._logger = get_project_logger(__name__)
        self._logger.info("RobotController initialized")

    @property
    def state(self) -> RobotState:
        """Return the current robot state."""
        return self._state

    def set_speed(self, speed: float) -> None:
        """Set robot speed after validation."""
        if not MIN_ALLOWED_SPEED <= speed <= MAX_ALLOWED_SPEED:
            self._logger.error("Invalid speed value: %s", speed)
            raise ValueError(
                f"Speed must be between {MIN_ALLOWED_SPEED} and {MAX_ALLOWED_SPEED}"
            )
        self._state.speed = speed
        self._logger.info("Speed updated to %s", speed)

    def move_for_duration(self, duration_seconds: float) -> float:
        """Move robot for the given duration and return new position."""
        if duration_seconds < MIN_ALLOWED_DURATION:
            self._logger.error("Invalid movement duration: %s", duration_seconds)
            raise ValueError("Duration must be non-negative")
        displacement: float = self._state.speed * duration_seconds
        self._state.position += displacement
        self._logger.info(
            "Robot moved for %.3f seconds with speed %.3f, displacement %.3f",
            duration_seconds,
            self._state.speed,
            displacement,
        )
        return self._state.position

    def stop(self) -> None:
        """Stop robot movement by setting speed to zero."""
        self._state.speed = STOP_SPEED
        self._logger.info("Robot stopped")
