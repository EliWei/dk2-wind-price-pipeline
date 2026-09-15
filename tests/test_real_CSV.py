""" Note, you have to have ran the pipeline.py script first to generate the CSV files before running this test. """

import pandas as pd

from date_alignment import check_date_alignment


class CsvRowPrice:
    def __init__(self, TimeDK) -> None:
        self.TimeDK = TimeDK


class CsvRowWind:
    def __init__(self, Minutes5DK) -> None:
        self.Minutes5DK = Minutes5DK


def test_real_pipeline_output_is_aligned() -> None:
    # Arrange (reads whatever the pipeline most recently saved)
    prices_df = pd.read_csv("data/dk2_prices.csv", parse_dates=["TimeDK"])
    wind_df = pd.read_csv("data/dk2_wind.csv", parse_dates=["Minutes5DK"])

    prices = [CsvRowPrice(t) for t in prices_df["TimeDK"]]
    wind = [CsvRowWind(t) for t in wind_df["Minutes5DK"]]

    # Act
    result = check_date_alignment(prices, wind)

    # Assert
    assert result is True