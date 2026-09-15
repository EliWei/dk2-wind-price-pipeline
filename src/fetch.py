# Needed on this Mac: Python's default certificate bundle (certifi) fails
# to verify this API's certificate chain, even though the connection is
# genuinely fine (curl and macOS trust it without issue). truststore
# makes Python use macOS's own certificate verification instead.

import truststore
truststore.inject_into_ssl()
import json
import requests
import logging

from typing import Optional

logger = logging.getLogger(f"dk2_pipeline.{__name__}")

DAY_AHEAD_URL = "https://api.energidataservice.dk/dataset/DayAheadPrices"
WIND_URL = "https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime"

# All fetch functions default to price area DK2 (Copenhagen/Sjælland area), the scope of this project.
# Setting limits to fetch prices and production here as a default, so that noone accidentally fetches
# too much data. However, this limit is overridden by calling the function at pipeline, where limits are also set 
# (Hängslen och livrem...)

# All fetch functions default to price area defaults to DK2 (Copenhagen/Sjælland area), the scope of
# this project. start/end have no default here (None) as pipeline.py calculates "yesterday". 
# (As there is expectations of this being a str, I have used Optional[str] to indicate that it can be None, 
# but if it is not None, it must be a str.) 

def fetch_day_ahead_prices(price_area: str = "DK2", start: Optional[str] = None, end: Optional[str] = None):   
    """
    Fetch day-ahead electricity spot prices from Danish Energi Data Service.
    Prices are quarter-hourly, so limit=96 returns a full day.

    """

    # The API expects the filter as a JSON string inside the query params, 
    # not as a normal Python dic (so filter=DK2 doesn't work). 
    # This is why we are building it manually here, using json.dumps().
    # (Coverts Python dict into a JSON string)

    params = {
    "start": start,
    "end": end,
    "filter": json.dumps({"PriceArea": price_area})
    }

    logger.debug("Fetching day-ahead prices for %s, %s to %s", price_area, start, end)

    response = requests.get(DAY_AHEAD_URL, params=params)
    response.raise_for_status()

    # returns a JSON dict,
    # one dictionary with a keys (total, filters, limit, dataset) 
    # plus one key, "records", which is a list of dictionaries (one dict per individual record)
    data = response.json()
    logger.info("Fetched %d price records for %s", len(data["records"]), price_area)
    return data


def fetch_wind_production(price_area: str = "DK2", start: Optional[str] = None, end: Optional[str] = None):
    """
    Fetch recent wind production data (5-minute intervals) from Energi Data Service.

    """

    params = {
    "start": start,
    "end": end,
    "filter": json.dumps({"PriceArea": price_area})
    }

    logger.debug("Fetching wind production for %s, %s to %s", price_area, start, end)
    
    response = requests.get(WIND_URL, params=params)
    response.raise_for_status()

    data = response.json()
    logger.info("Fetched %d wind production records for %s", len(data["records"]), price_area)
    return data

