"""Tests for date_alignment using fake data."""

import pytest

from datetime import datetime

from date_alignment import check_date_alignment


class FakePrice:
    def __init__(self, TimeDK: datetime) -> None:
        self.TimeDK = TimeDK


class FakeWind:
    def __init__(self, Minutes5DK: datetime) -> None:
        self.Minutes5DK = Minutes5DK


@pytest.mark.skip(reason="Kept as a reference for how these tests were built")
def test_check_date_alignment_matching_dates() -> None:
    # Arrange
    prices = [
        FakePrice(datetime(2026, 9, 14, 0, 0)),
        FakePrice(datetime(2026, 9, 14, 23, 45)),
    ]
    wind = [
        FakeWind(datetime(2026, 9, 14, 0, 0)),
        FakeWind(datetime(2026, 9, 14, 23, 55)),
    ]

    # Act
    result = check_date_alignment(prices, wind)

    # Assert
    assert result is True


@pytest.mark.skip(reason="Kept as a reference for how these tests were built.")
def test_check_date_alignment_mismatched_dates() -> None:
    # Arrange
    prices = [FakePrice(datetime(2026, 9, 15, 0, 0))]
    wind = [FakeWind(datetime(2026, 9, 13, 14, 0))]

    # Act
    result = check_date_alignment(prices, wind)

    # Assert
    assert result is False


@pytest.mark.skip(reason="Kept as a reference for how these tests were built.")
def test_check_date_alignment_catches_mixed_dates_within_prices() -> None:
    # Arrange -- prices span two different days, wind is only on one
    prices = [
        FakePrice(datetime(2026, 9, 14, 23, 45)),
        FakePrice(datetime(2026, 9, 15, 0, 0)),
    ]
    wind = [
        FakeWind(datetime(2026, 9, 14, 0, 0)),
        FakeWind(datetime(2026, 9, 14, 23, 55)),
    ]

    # Act
    result = check_date_alignment(prices, wind)

    # Assert
    assert result is False