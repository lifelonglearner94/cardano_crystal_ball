import pytest

import pandas as pd

from apis.live_coin_watch.utils import get_api_limit, get_alot_of_data,\
        get_4_days_of_data, api_request, convert_timestamp_to_time_string

def test_get_api_limit():
    response = get_api_limit()
    assert (response <= 10000) and (response >= 0)


def test_get_alot_of_data():
    response = get_alot_of_data("2020-02-01 08:00:00", "2020-02-10 08:00:00")
    assert (type(response) == pd.DataFrame)
    assert(len(response) > 100)

def test_convert_timestamp_to_time_string ():

    assert ('2024-01-01 00:00:00' == convert_timestamp_to_time_string(1704067200, False))
