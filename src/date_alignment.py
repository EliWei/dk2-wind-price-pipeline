# A function to check that every record from the two datasets are from the same date
# so that there are no mismatches.

def check_date_alignment(prices: list, wind: list) -> bool:
    """
    Check that price and wind records are from the same day.
    Returns True or False.
    """

    # Loops through each record, gets the dates, collects them into a set, gets rid of duplicates
    # and hence ends up with just one date for each dataset.

    price_dates = {record.TimeDK.date() for record in prices}

    # Does the same for wind production, ending up with one date.
    wind_dates = {record.Minutes5DK.date() for record in wind}

    # Compares the two sets of dates. If they are the same, returns True, else False.
    return price_dates == wind_dates