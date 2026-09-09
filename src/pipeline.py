import logging

from pydantic import ValidationError
from fetch import fetch_day_ahead_prices, fetch_wind_production
from validate import DayAheadPrice, WindProduction
from validation_report import ValidationReport

from storage import save_to_csv

logger = logging.getLogger(__name__)

def validate_batch(records, model_class, report):
    """
    Validate every record in a batch against model_class.

    Records that pass are returned in a list. Records that fail are
    recorded on the given ValidationReport instead of stopping the
    whole batch.
    """
    valid_records = []
    for record in records:
        try:
            validated = model_class(**record)
            report.record_success()
            valid_records.append(validated)
        except ValidationError as e:
            report.record_failure(str(e))
    return valid_records


def run_pipeline():

    """Fetch, validate, and report on both DK2 datasets."""
    
    # Both spot prices and wind production go into the same pipeline, but are validated separately
    # and gets their own ValidationReport
    price_report = ValidationReport()
    wind_report = ValidationReport()

    #Limit set to 96 this is a full day of 15 min prices
    raw_prices = fetch_day_ahead_prices(limit=96)

    #Limit set to 288 this is a full day of 5 min wind production records
    raw_wind = fetch_wind_production(limit=288)

    valid_prices = validate_batch(
        raw_prices["records"], DayAheadPrice, price_report
    )
    valid_wind = validate_batch(
        raw_wind["records"], WindProduction, wind_report
    )

    logger.info("Price validation: %s", price_report.summary())
    logger.info("Wind validation: %s", wind_report.summary())

    # save the validated records to CSV in the data folder
    save_to_csv(valid_prices, "data/dk2_prices.csv")
    save_to_csv(valid_wind, "data/dk2_wind.csv")

    return valid_prices, valid_wind


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()