# Tester för date_alignment using fake data

import pytest

from date_alignment import check_date_alignment

from datetime import datetime

#class FakePrice:
    #def __init__(self, TimeDK: datetime) -> None:
    #    self.TimeDK = TimeDK

#class FakeWind:
    #def __init__(self, Minutes5DK: datetime) -> None:
    #    self.Minutes5DK = Minutes5DK

#def test_check_date_alignment_matching_dates() -> None:
    # Arrange
    #prices = [
    #    FakePrice(datetime(2026, 9, 14, 0, 0)),
    #    FakePrice(datetime(2026, 9, 14, 23, 45)),
    #]
    #wind = [
    #    FakeWind(datetime(2026, 9, 14, 0, 0)),
    #    FakeWind(datetime(2026, 9, 14, 23, 55)),
    #]

    # Act
    #result = check_date_alignment(prices, wind)

    # Assert
    #assert result is True

#def test_check_date_alignment_mismatched_dates() -> None:
    # Arrange
    #prices = [FakePrice(datetime(2026, 9, 15, 0, 0))]
    #wind = [FakeWind(datetime(2026, 9, 13, 14, 0))]

    # Act
    #result = check_date_alignment(prices, wind)

    # Assert
    #assert result is False

#def test_check_date_alignment_catches_mixed_dates_within_prices() -> None:
    # Arrange (prices span two different days, wind is only on one)
    #prices = [
    #    FakePrice(datetime(2026, 9, 14, 23, 45)),
    #    FakePrice(datetime(2026, 9, 15, 0, 0)),
    #]
    #wind = [
    #    FakeWind(datetime(2026, 9, 14, 0, 0)),
    #    FakeWind(datetime(2026, 9, 14, 23, 55)),
    #]

    # Act
    #result = check_date_alignment(prices, wind)

    # Assert
    #assert result is False