import csv
import logging

logger = logging.getLogger(f"dk2_pipeline.{__name__}")


def save_to_csv(records: list, filepath: str) -> None:
    """
    Save a list of validated Pydantic records to a CSV file.

    """
    if not records:
        logger.warning("No records to save -- skipping write to %s", filepath)
        return

    # Each record's fields become columns. We take the first record [0]
    # to get the field names for the column headers
    fieldnames = list(records[0].model_dump().keys())

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:

    # model_dump() is a builtin Pydantic method
    # it returns a dict. This is needed to get the fieldnames for the CSV header
    # and to write the records as rows in the CSV file

            writer.writerow(record.model_dump())
    logger.info("Saved %d records to %s", len(records), filepath)

# doing a self-test with sample data, not part of the pipeline
# confirms save_to_csv writes records to a CSV file (saved in the data folder)
if __name__ == "__main__":
    from validate import DayAheadPrice

    sample_records = [
        DayAheadPrice(
            TimeUTC="2026-09-03T21:45:00",
            TimeDK="2026-09-03T23:45:00",
            PriceArea="DK2",
            DayAheadPriceEUR=134.94,
            DayAheadPriceDKK=1008.65,
        ),
        DayAheadPrice(
            TimeUTC="2026-09-03T21:30:00",
            TimeDK="2026-09-03T23:30:00",
            PriceArea="DK2",
            DayAheadPriceEUR=163.88,
            DayAheadPriceDKK=1225.02,
        ),
    ]
    save_to_csv(sample_records, "data/test_prices.csv")