"""Tests for robot controller behavior."""

from __future__ import annotations

import pytest

from src.controllers.robot_controller import RobotController

VALID_SPEED: float = 20.0
INVALID_HIGH_SPEED: float = 120.0
INVALID_LOW_SPEED: float = -150.0
MOVEMENT_DURATION: float = 2.5
EXPECTED_POSITION: float = 50.0
NEGATIVE_DURATION: float = -1.0
STOPPED_SPEED: float = 0.0


def test_set_speed_updates_state() -> None:
    """Controller sets valid speed to robot state."""
    controller: RobotController = RobotController()
    controller.set_speed(VALID_SPEED)
    assert controller.state.speed == VALID_SPEED


@pytest.mark.parametrize("speed", [INVALID_HIGH_SPEED, INVALID_LOW_SPEED])
def test_set_speed_raises_for_out_of_range_values(speed: float) -> None:
    """Controller rejects speed values outside allowed range."""
    controller: RobotController = RobotController()
    with pytest.raises(ValueError):
        controller.set_speed(speed)


def test_move_for_duration_updates_position() -> None:
    """Movement changes position according to speed and duration."""
    controller: RobotController = RobotController()
    controller.set_speed(VALID_SPEED)
    position: float = controller.move_for_duration(MOVEMENT_DURATION)
    assert position == EXPECTED_POSITION
    assert controller.state.position == EXPECTED_POSITION


def test_move_for_duration_raises_for_negative_duration() -> None:
    """Movement with negative duration is rejected."""
    controller: RobotController = RobotController()
    with pytest.raises(ValueError):
        controller.move_for_duration(NEGATIVE_DURATION)


def test_stop_resets_speed_to_zero() -> None:
    """Stop sets controller speed to zero."""
    controller: RobotController = RobotController()
    controller.set_speed(VALID_SPEED)
    controller.stop()
    assert controller.state.speed == STOPPED_SPEED
