import json
import requests

DAY_AHEAD_URL = "https://api.energidataservice.dk/dataset/DayAheadPrices"
WIND_URL = "https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime"

# All fetch functions default to price area DK2 (Copenhagen/Sjælland area),
# the scope of this project.

def fetch_day_ahead_prices(price_area: str = "DK2", limit: int = 24):
    """
    Fetch day-ahead electricity spot prices from Danish Energi Data Service.
    Prices are quarter-hourly, so limit=24 returns the most recent 6 hours,
    not a full day (a full day is 96 records). 

    """

    # The API expects the filter as a JSON string inside the query params, 
    # not as a normal Python dic (so filter=DK2 doesn't work). 
    # This is why we are building it manually here, using json.dumps().
    # (Coverts Python dict into a JSON string)

    params = {
        "limit": limit,
        "filter": json.dumps({"PriceArea": price_area})
    }
    response = requests.get(DAY_AHEAD_URL, params=params)
    response.raise_for_status()
    return response.json()


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