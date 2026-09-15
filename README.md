# dk2-wind-price-pipeline
Validated data pipeline for Danish (DK2) wind production and day-ahead electricity spot prices, built with Pydantic.

# DK2 Wind & Price Pipeline

A validated data pipeline for Danish DK2 price area wind production and 
day-ahead electricity spot prices, built with Pydantic. 
Built as part of a Python project for a Data Science course, focused on 
robust handling of API data with validation, logging, and data quality,
rather than on the analysis itself.

## What it does

The pipeline:
1. **Fetches** wind production and day-ahead spot price data for DK2
   (Copenhagen/Sjælland area) from Denmark's Energi Data Service 
   (https://www.energidataservice.dk/), for "yesterday". 
   ("Yesterday" is used to ensure that each run gets a full day's 
   worth of data, as wind data has a short reporting lag and prices 
   are published a day ahead.)
2. **Validates** every record against a Pydantic schema, catching
   malformed or unexpected data before it's used.
3. **Logs** the whole process to a summary to the console and full detail
   to dk2_pipeline.log.
4. **Saves** the validated data to CSV files in data.

A separate analysis notebook (analysis.ipynb) compares wind production 
against spot price for a given day.

## Setup
Requires Python 3.13.

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the pipeline

```bash
python src/pipeline.py
```

This fetches, validates, logs, and saves fresh data for the most
recent fully-settled day. Check the console output for a summary, or
dk2_pipeline.log for full detail.

## Running the tests

```bash
pytest
```

One test that checks the real, most-recently saved CSV data is date aligned. Run
pipeline.py first if you want that one to reflect current data. 
Tests also includes unit tests for the date-alignment check (using fake data,
covering matching, mismatched, and mixed-date cases).

## Data source

All data comes from Denmark's Energi Data Service, a free, open API
requiring no authentication:
- [`DayAheadPrices`](https://www.energidataservice.dk/) — day-ahead
  electricity spot prices, quarter-hourly.
- [`ElectricityProdex5MinRealtime`](https://www.energidataservice.dk/)
  — wind and solar production, 5-minute intervals.

## Project structure
src/
fetch.py                            # API calls
validate.py                         # Pydantic models
validation_report.py                # Tracks validation outcomes for a batch
date_alignment.py                   # Checks two datasets cover the same day
storage.py                          # Saves validated records to CSV
logging_config.py                   # Console + file logging setup
pipeline.py                         # Runs pipeline
tests/
test_date_alignment.py              # Unit tests, fake data
test_real_CSV.py                    # Checks real, current pipeline output
data/                               # Output CSVs 
analysis.ipynb                      # Wind vs. price comparison
pyproject.toml                      # pytest configuration (adds src/ to path)
requirements.txt                    # Python dependencies
.gitignore                          # Excludes venv/, data outputs, logs, etc.


## Notes

On some Mac setups, Python's default certificate bundle fails to
verify this API's certificate chain even though the connection is
fine. fetch.py uses truststore to fall back on macOS's own 
certificate verification instead — see the comment in that file.