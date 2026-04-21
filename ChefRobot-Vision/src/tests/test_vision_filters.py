"""Tests for class filtering in vision detector script."""

from __future__ import annotations

import pytest

from src.main import normalize_label, should_display_detection


@pytest.mark.parametrize(
    ("raw_label", "expected"),
    [
        (" Apple ", "apple"),
        ("BANANA", "banana"),
        ("  Strawberry", "strawberry"),
    ],
)
def test_normalize_label(raw_label: str, expected: str) -> None:
    """Normalize trims whitespace and lowercases labels."""
    assert normalize_label(raw_label) == expected


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("apple", True),
        ("egg", True),
        ("fork", True),
        ("person", False),
        ("dog", False),
        ("cell phone", False),
    ],
)
def test_should_display_detection(label: str, expected: bool) -> None:
    """Only required categories are allowed for rendering."""
    assert should_display_detection(label) is expected
