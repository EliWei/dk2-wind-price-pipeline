# Needed on this Mac: Python's default certificate bundle (certifi) fails
# to verify this API's certificate chain, even though the connection is
# genuinely fine (curl and macOS trust it without issue). truststore
# makes Python use macOS's own certificate verification instead.

import truststore
truststore.inject_into_ssl()

import json
import requests
import logging

logger = logging.getLogger(f"dk2_pipeline.{__name__}")

DAY_AHEAD_URL = "https://api.energidataservice.dk/dataset/DayAheadPrices"
WIND_URL = "https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime"

# All fetch functions default to price area DK2 (Copenhagen/Sjælland area), the scope of this project.
# Setting limits to fetch prices and production here as a default, so that noone accidentally fetches
# too much data. However, this limit is overridden by calling the function at pipeline, where limits are also set 
# (Hängslen och livrem...)

def fetch_day_ahead_prices(price_area: str = "DK2", limit: int = 96):
    """
    Fetch day-ahead electricity spot prices from Danish Energi Data Service.
    Prices are quarter-hourly, so limit=96 returns a full day.

    """

    # The API expects the filter as a JSON string inside the query params, 
    # not as a normal Python dic (so filter=DK2 doesn't work). 
    # This is why we are building it manually here, using json.dumps().
    # (Coverts Python dict into a JSON string)

    params = {
        "limit": limit,
        "filter": json.dumps({"PriceArea": price_area})
    }
    logger.debug("Fetching day-ahead prices for %s, limit=%d", price_area, limit)
    response = requests.get(DAY_AHEAD_URL, params=params)
    response.raise_for_status()

    # returns a JSON dict,
    # one dictionary with a keys (total, filters, limit, dataset) 
    # plus one key, "records", which is a list of dictionaries (one dict per individual record)
    data = response.json()
    logger.info("Fetched %d price records for %s", len(data["records"]), price_area)
    return data


def fetch_wind_production(price_area: str = "DK2", limit: int = 5):

    """
    Fetch recent wind production data (5-minute intervals) from Energi Data Service.

    """

    params = {
        "limit": limit,
        "filter": json.dumps({"PriceArea": price_area})
    }
    response = requests.get(WIND_URL, params=params)
    response.raise_for_status()

    # returns a JSON dict
    return response.json()

# Only run the following code when this script is executed directly, not when imported as a module
if __name__ == "__main__":

    # Quick manual check that both functions work — not part of the
    # pipeline itself, only runs when this file is executed directly.
    prices = fetch_day_ahead_prices()
    print(f"Got {prices['total']} price records, showing {len(prices['records'])}")
    print(prices['records'][0])

    wind = fetch_wind_production()
    print(f"\nGot {wind['total']} wind production records, showing {len(wind['records'])}")
    print(wind['records'][0])