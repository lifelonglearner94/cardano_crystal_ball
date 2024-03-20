import requests
import json
from datetime import datetime
import pandas as pd
from time import sleep
import pytz
# from dotenv import load_dotenv
import os

# def get_apikey_from_env():
#     load_dotenv()
#     return os.environ.get("API_KEY")

API_KEY = "a8558c74-f457-4c85-bb47-e2772d339c94"
# API_KEY = get_apikey_from_env()

def api_request(start, end):
    """
    Sends a POST request to the Livecoinwatch API to retrieve historical data for a specific coin within a given time range.

    Parameters:
        start (int): Start timestamp for the data retrieval.
        end (int): End timestamp for the data retrieval.

    Returns:
        dict: Response containing historical data fetched from the API.
    """


    url = 'https://api.livecoinwatch.com/coins/single/history'

    payload = json.dumps({
    "currency": "USD",
    "code": "ADA",
    "start": start,
    "end": end,
    "meta": False
    })

    headers = {
    'content-type': 'application/json',
    'x-api-key': API_KEY
    }
    try:
        response = requests.request("POST",url, headers=headers, data=payload).json()
    except:
        sleep(10)
        response = requests.request("POST",url, headers=headers, data=payload).json()

    return response

def get_api_limit():
    """
    Retrieves the remaining daily API credits from Livecoinwatch API.

    Returns:
        int: Number of remaining daily credits.
    """
    url = "https://api.livecoinwatch.com/credits"

    payload={}
    headers = {
    'content-type': 'application/json',
    'x-api-key': API_KEY
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()


    return response["dailyCreditsRemaining"]


def convert_timestamp_to_time_string(timestamp, ms=True):
    """
    Converts a timestamp to a human-readable date and time string.

    Parameters:
        timestamp (int): Timestamp to be converted.
        ms (bool): Indicates whether the timestamp is in milliseconds. Default is True.

    Returns:
        str: Human-readable date and time string.
    """
    if ms:
        timestamp = int(timestamp) // 1000
    else:
        timestamp = int(timestamp)

    converted_datetime = datetime.utcfromtimestamp(timestamp) # always UTC (London time)

    human_readable_date = converted_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return human_readable_date


def convert_datetime_to_milliseconds(datetime_str):
    """
    Converts a datetime string to milliseconds since the epoch (January 1, 1970).

    Parameters:
        datetime_str (str): Datetime string in the format '%Y-%m-%d %H:%M:%S'.

    Returns:
        int: Timestamp in milliseconds.
    """
    # Parse the input datetime string
    dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    # Set the timezone to UTC
    utc_timezone = pytz.timezone('UTC')
    dt_obj_utc = utc_timezone.localize(dt_obj)

    # Convert to milliseconds
    timestamp_ms = int(dt_obj_utc.timestamp() * 1000)

    return timestamp_ms



def get_4_days_of_data(start, end):
    """
    Retrieves historical data for a 4-day period from the Livecoinwatch API.

    Parameters:
        start (int): Start timestamp for the data retrieval.
        end (int): End timestamp for the data retrieval.

    Returns:
        pandas.DataFrame: DataFrame containing historical data for the specified period.
    """
    try:
        response = api_request(start, end)

        df = pd.DataFrame()

        for i in range(  len(response["history"]) -1 ):

            line = pd.DataFrame.from_dict([response["history"][i]])

            df = pd.concat([df, line], ignore_index=True, axis=0)

    except:
        sleep(5)
        response = api_request(start, end)

        df = pd.DataFrame()

        for i in range(  len(response["history"])  ):

            line = pd.DataFrame.from_dict([response["history"][i]])

            df = pd.concat([df, line], ignore_index=True, axis=0)

    return df


def get_alot_of_data(start_date_as_string, end_date_as_string):
    """
    Retrieves historical data for a large time range by fetching data in 4-day intervals.

    Parameters:
        start_date_as_string (str): Start date in the format '%Y-%m-%d %H:%M:%S'.
        end_date_as_string (str): End date in the format '%Y-%m-%d %H:%M:%S'.

    Returns:
        pandas.DataFrame: DataFrame containing historical data for the specified time range.
    """

    date_start = convert_datetime_to_milliseconds(start_date_as_string)

    date_end = convert_datetime_to_milliseconds(end_date_as_string)

    rolling_date = date_start

    big_df = pd.DataFrame()

    while rolling_date <= date_end:


        period_df = get_4_days_of_data(rolling_date, rolling_date + 345600000) #345600000 ms == 4 days

        big_df = pd.concat([big_df, period_df], ignore_index=True, axis=0)

        print(f"data written in df from{convert_timestamp_to_time_string(rolling_date)} to {convert_timestamp_to_time_string(rolling_date + 345600000)}")

        rolling_date += 345600000

    big_df["date"] = big_df["date"].apply(convert_timestamp_to_time_string)

    return big_df
