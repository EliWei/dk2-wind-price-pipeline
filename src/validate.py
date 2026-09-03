from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# Two separate Classes, one per dataset, rather than one shared Class.
# Each one has a single responsibility: check that one record from
# one specific API endpoint matches the expected shape. They don't share
# fields or logic, so combining them wouldn't simplify anything, it
# would just make one class responsible for two unrelated things.

# Using Pydantic's BaseModel here instead of a @dataclass, because
# Pydantic's BaseModel basically IS a dataclass, but with enforced validation.

class DayAheadPrice(BaseModel):
    """
    A single day-ahead spot price record, validated against the shape
    returned by the DayAheadPrices dataset.
    """

    # For example, if the API sent PriceArea as a string instead of an actual number, 
    # Pydantic would automatically convert it to a float.
    
    TimeUTC: datetime
    TimeDK: datetime
    PriceArea: str
    DayAheadPriceEUR: float
    DayAheadPriceDKK: float


class WindProduction(BaseModel):
    """
    Checks that a 5-minute production record matches the expected format.

    Exchange fields are kept even though some are always null for DK2
    (no direct connection to those countries) -- this keeps the model
    correct if the project is ever pointed at a different price area,
    such as DK1, where different connections apply.
    
    """
    Minutes5UTC: datetime
    Minutes5DK: datetime
    PriceArea: str
    ProductionLt100MW: float
    ProductionGe100MW: float
    OffshoreWindPower: float
    OnshoreWindPower: float
    SolarPower: float

    # GreatBelt, Germany, Sweden and Bornholm are connected to DK2
    # so these fields are always present. 
    # Netherlands, Great Britain and Norway are not connected and are
    # set to float or None, so that the Class can be used for other price areas as well. 

    ExchangeGreatBelt: float
    ExchangeGermany: float
    ExchangeNetherlands: Optional[float] = None
    ExchangeGreatBritain: Optional[float] = None
    ExchangeNorway: Optional[float] = None
    ExchangeSweden: float
    BornholmSE4: float


if __name__ == "__main__":

    # A standalone, quick manual check, using one real record from each dataset,
    # which I have copied from an earlier live API fetch, to make sure the validation works

    sample_price = {
        "TimeUTC": "2026-09-03T21:45:00",
        "TimeDK": "2026-09-03T23:45:00",
        "PriceArea": "DK2",
        "DayAheadPriceEUR": 134.940002,
        "DayAheadPriceDKK": 1008.649527,
    }
    validated_price = DayAheadPrice(**sample_price)
    print(validated_price)

    sample_wind = {
        "Minutes5UTC": "2026-09-02T13:35:00",
        "Minutes5DK": "2026-09-02T15:35:00",
        "PriceArea": "DK2",
        "ProductionLt100MW": 115.260002,
        "ProductionGe100MW": 57.119999,
        "OffshoreWindPower": 574.719971,
        "OnshoreWindPower": 203.740005,
        "SolarPower": 479.540009,
        "ExchangeGreatBelt": 51.259998,
        "ExchangeGermany": 20.16,
        "ExchangeNetherlands": None,
        "ExchangeGreatBritain": None,
        "ExchangeNorway": None,
        "ExchangeSweden": 335.329987,
        "BornholmSE4": -24.77,
    }
    validated_wind = WindProduction(**sample_wind)
    print(validated_wind)